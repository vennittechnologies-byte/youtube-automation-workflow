#!/usr/bin/env python3
"""
YouTube Upload Module
Uploads videos to YouTube using the YouTube Data API v3
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("⚠️  Google API libraries not installed.")
    print("    Install with: pip install google-api-python-client google-auth-oauthlib")

# Load environment variables
load_dotenv()


class YouTubeUploader:
    """Upload videos to YouTube"""
    
    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self):
        if not YOUTUBE_API_AVAILABLE:
            raise RuntimeError(
                "Google API libraries required. "
                "Install with: pip install google-api-python-client google-auth-oauthlib"
            )
        
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.client_secrets_file = os.getenv(
            'CLIENT_SECRETS_PATH',
            'config/client_secrets.json'
        )
        self.token_file = os.getenv(
            'TOKEN_PICKLE_PATH',
            'config/token.pickle'
        )
        
        self.category_id = os.getenv('YOUTUBE_CATEGORY_ID', '22')  # People & Blogs
        self.privacy_status = os.getenv('YOUTUBE_PRIVACY_STATUS', 'private')
        
        self.youtube = None
    
    def authenticate(self) -> None:
        """Authenticate with YouTube API"""
        
        credentials = None
        
        # Try to load saved credentials
        if os.path.exists(self.token_file):
            print("🔑 Loading saved credentials...")
            try:
                with open(self.token_file, 'rb') as token:
                    credentials = pickle.load(token)
            except Exception as e:
                print(f"⚠️  Failed to load credentials: {str(e)}")
                credentials = None
        
        # If credentials are invalid or don't exist, get new ones
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("🔄 Refreshing expired credentials...")
                try:
                    credentials.refresh(Request())
                except Exception as e:
                    print(f"⚠️  Refresh failed: {str(e)}")
                    credentials = None
            
            if not credentials:
                if not os.path.exists(self.client_secrets_file):
                    raise FileNotFoundError(
                        f"OAuth client secrets file not found: {self.client_secrets_file}\n"
                        "Please download it from Google Cloud Console and place it in config/"
                    )
                
                print("🔐 Starting OAuth authentication flow...")
                print("    A browser window will open for you to authorize the app.")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.SCOPES
                )
                
                credentials = flow.run_local_server(
                    port=8080,
                    authorization_prompt_message='Please visit this URL: {url}',
                    success_message='Authentication successful! You can close this window.',
                    open_browser=True
                )
            
            # Save credentials for future runs
            print("💾 Saving credentials for future use...")
            Path(self.token_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, 'wb') as token:
                pickle.dump(credentials, token)
        
        # Build YouTube API client
        self.youtube = build('youtube', 'v3', credentials=credentials)
        print("✅ Authentication successful!")
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list,
        category_id: Optional[str] = None,
        privacy_status: Optional[str] = None,
        thumbnail_path: Optional[str] = None
    ) -> Dict:
        """
        Upload a video to YouTube
        
        Args:
            video_path: Path to video file
            title: Video title (max 100 characters)
            description: Video description (max 5000 characters)
            tags: List of tags (max 500 characters total)
            category_id: YouTube category ID (default from env)
            privacy_status: public, private, or unlisted (default from env)
            thumbnail_path: Optional path to custom thumbnail
            
        Returns:
            Response dictionary with video details
        """
        
        if not self.youtube:
            self.authenticate()
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Use defaults if not specified
        if category_id is None:
            category_id = self.category_id
        if privacy_status is None:
            privacy_status = self.privacy_status
        
        # Prepare request body
        body = {
            'snippet': {
                'title': title[:100],  # Max 100 characters
                'description': description[:5000],  # Max 5000 characters
                'tags': tags[:15],  # Max 500 chars total, ~15 tags
                'categoryId': category_id,
                'defaultLanguage': 'en',
                'defaultAudioLanguage': 'en'
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False,
            }
        }
        
        # Create media file upload
        print(f"📤 Uploading video: {Path(video_path).name}")
        print(f"   Title: {title}")
        print(f"   Privacy: {privacy_status}")
        
        media = MediaFileUpload(
            video_path,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True,
            mimetype='video/mp4'
        )
        
        try:
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   Upload progress: {progress}%", end='\r', flush=True)
            
            print(f"\n✅ Upload complete!")
            
            video_id = response['id']
            video_url = f"https://youtu.be/{video_id}"
            
            print(f"🎉 Video published: {video_url}")
            
            # Upload thumbnail if provided
            if thumbnail_path and os.path.exists(thumbnail_path):
                try:
                    self._upload_thumbnail(video_id, thumbnail_path)
                except Exception as e:
                    print(f"⚠️  Thumbnail upload failed: {str(e)}")
            
            return {
                'id': video_id,
                'url': video_url,
                'title': title,
                'privacy_status': privacy_status
            }
            
        except HttpError as e:
            error_message = e.content.decode('utf-8')
            print(f"\n❌ Upload failed: {error_message}")
            raise
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str) -> None:
        """Upload custom thumbnail for video"""
        
        print(f"🖼️  Uploading thumbnail...")
        
        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            
            print("✅ Thumbnail uploaded successfully!")
            
        except HttpError as e:
            raise RuntimeError(f"Thumbnail upload failed: {str(e)}")
    
    def upload_from_pipeline_output(self) -> Dict:
        """
        Upload video using outputs from the pipeline
        
        Returns:
            Upload response dictionary
        """
        
        # Load script metadata
        try:
            with open(f'{self.output_dir}/script.json', 'r') as f:
                script_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Script metadata not found. Run the pipeline first.")
        
        # Load video metadata
        try:
            with open(f'{self.output_dir}/video_metadata.json', 'r') as f:
                video_meta = json.load(f)
                video_path = video_meta['video_path']
        except FileNotFoundError:
            raise FileNotFoundError("Video not found. Run compose.py first.")
        
        # Load thumbnail if available
        thumbnail_path = None
        try:
            with open(f'{self.output_dir}/thumbnail_metadata.json', 'r') as f:
                thumbnail_meta = json.load(f)
                thumbnail_path = thumbnail_meta['thumbnail_path']
        except:
            print("⚠️  No thumbnail found, proceeding without it.")
        
        # Prepare upload details
        title = script_data.get('title', 'Automated Video')
        
        # Create description
        script_text = script_data.get('script', '')
        description = f"""{script_text[:500]}...

🔔 Subscribe for more content!
👍 Like this video if you found it helpful!
💬 Comment below with your thoughts!

#automation #ai #technology
"""
        
        tags = script_data.get('tags', [])
        
        # Upload video
        response = self.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            thumbnail_path=thumbnail_path
        )
        
        # Save upload metadata
        upload_metadata = {
            **response,
            'script_file': f'{self.output_dir}/script.json',
            'video_file': video_path
        }
        
        with open(f'{self.output_dir}/upload_metadata.json', 'w') as f:
            json.dump(upload_metadata, f, indent=2)
        
        return response


def main():
    """Test the YouTube uploader"""
    
    try:
        uploader = YouTubeUploader()
        
        print("🚀 Starting YouTube upload...\n")
        
        # Upload from pipeline output
        response = uploader.upload_from_pipeline_output()
        
        print("\n" + "="*60)
        print("✅ Upload process complete!")
        print("="*60)
        print(f"🎬 Video ID: {response['id']}")
        print(f"🔗 Video URL: {response['url']}")
        print(f"📝 Title: {response['title']}")
        print(f"🔒 Privacy: {response['privacy_status']}")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n❌ Missing required files: {str(e)}")
        print("\n💡 Setup required:")
        print("   1. Create a Google Cloud project at console.cloud.google.com")
        print("   2. Enable YouTube Data API v3")
        print("   3. Create OAuth 2.0 credentials (Desktop app)")
        print("   4. Download client_secrets.json to config/")
        print("\n   Or run the full pipeline first:")
        print("   python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
