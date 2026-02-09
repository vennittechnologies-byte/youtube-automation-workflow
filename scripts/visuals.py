#!/usr/bin/env python3
"""
Visuals Fetcher Module
Downloads stock videos and images from Pexels API
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class VisualsFetcher:
    """Fetch stock videos and images from Pexels"""
    
    def __init__(self):
        self.api_key = os.getenv('PEXELS_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "PEXELS_API_KEY not found in environment variables. "
                "Get a free API key at https://www.pexels.com/api/"
            )
        
        self.headers = {"Authorization": self.api_key}
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        
        # API endpoints
        self.video_search_url = "https://api.pexels.com/videos/search"
        self.photo_search_url = "https://api.pexels.com/v1/search"
    
    def search_videos(
        self, 
        query: str, 
        count: int = 5,
        orientation: str = "landscape",
        size: str = "medium"
    ) -> List[Dict]:
        """
        Search for stock videos on Pexels
        
        Args:
            query: Search query (e.g., "technology", "nature")
            count: Number of videos to fetch (default: 5)
            orientation: Video orientation - landscape, portrait, or square
            size: Video quality - large, medium, or small
            
        Returns:
            List of video metadata dictionaries
        """
        
        print(f"🔍 Searching Pexels for videos: '{query}'")
        
        params = {
            "query": query,
            "per_page": min(count, 15),  # API max per page is 80
            "orientation": orientation
        }
        
        try:
            response = requests.get(
                self.video_search_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            videos = data.get('videos', [])
            
            if not videos:
                print(f"⚠️  No videos found for query: '{query}'")
                return []
            
            print(f"✅ Found {len(videos)} videos")
            
            # Extract relevant video files based on size preference
            video_metadata = []
            for video in videos[:count]:
                video_files = video.get('video_files', [])
                
                # Find the best matching video file
                best_file = self._select_best_video_file(video_files, size)
                
                if best_file:
                    video_metadata.append({
                        "id": video['id'],
                        "url": best_file['link'],
                        "width": best_file.get('width', 1920),
                        "height": best_file.get('height', 1080),
                        "duration": video.get('duration', 0),
                        "query": query
                    })
            
            return video_metadata
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch videos from Pexels: {str(e)}")
    
    def _select_best_video_file(self, video_files: List[Dict], preferred_size: str) -> Dict:
        """Select the best video file based on quality preferences"""
        
        if not video_files:
            return None
        
        # Size priority map
        size_priority = {
            "large": ["hd", "sd"],
            "medium": ["sd", "hd"],
            "small": ["sd"]
        }
        
        qualities = size_priority.get(preferred_size, ["sd", "hd"])
        
        # Try to find a file matching preferred quality
        for quality in qualities:
            for vf in video_files:
                if vf.get('quality') == quality:
                    return vf
        
        # Fallback to first available file
        return video_files[0]
    
    def download_video(self, url: str, filename: str, subfolder: str = "clips") -> str:
        """
        Download a video from URL
        
        Args:
            url: Video URL
            filename: Output filename
            subfolder: Subfolder in output directory (default: clips)
            
        Returns:
            Path to downloaded file
        """
        
        # Create output directory
        output_path = Path(self.output_dir) / subfolder
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / filename
        
        print(f"⬇️  Downloading: {filename}")
        
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            # Download with progress indication
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Simple progress indicator
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r   Progress: {progress:.1f}%", end='', flush=True)
            
            print(f"\n✅ Downloaded: {filepath}")
            return str(filepath)
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to download video: {str(e)}")
    
    def fetch_videos_for_script(self, script_data: Dict = None) -> List[str]:
        """
        Fetch videos based on script topics/keywords
        
        Args:
            script_data: Dictionary containing script and metadata
            
        Returns:
            List of downloaded video file paths
        """
        
        # Load script if not provided
        if script_data is None:
            script_path = f"{self.output_dir}/script.json"
            try:
                with open(script_path, 'r') as f:
                    script_data = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Script file not found: {script_path}")
        
        # Load topics for visual queries
        try:
            with open('config/topics.json', 'r') as f:
                topics_data = json.load(f)
            
            # Find matching topic
            script_topic = script_data.get('topic', '')
            visual_queries = []
            
            for topic in topics_data.get('topics', []):
                if topic['title'].lower() in script_topic.lower():
                    visual_queries = topic.get('visual_queries', [])
                    break
            
            # Fallback to script tags if no visual queries found
            if not visual_queries:
                visual_queries = script_data.get('tags', ['technology'])[:3]
        
        except:
            # Ultimate fallback
            visual_queries = ['technology', 'abstract', 'business']
        
        print(f"\n📹 Fetching videos for queries: {visual_queries}")
        
        downloaded_files = []
        
        # Fetch 2 videos per query (can be adjusted)
        videos_per_query = 2
        
        for idx, query in enumerate(visual_queries):
            videos = self.search_videos(query, count=videos_per_query)
            
            for vid_idx, video in enumerate(videos):
                filename = f"clip_{idx}_{vid_idx}.mp4"
                
                try:
                    filepath = self.download_video(video['url'], filename)
                    downloaded_files.append(filepath)
                    
                    # Rate limiting - be nice to the API
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"⚠️  Failed to download {filename}: {str(e)}")
                    continue
        
        # Save metadata
        visuals_metadata = {
            "downloaded_files": downloaded_files,
            "queries": visual_queries,
            "total_clips": len(downloaded_files)
        }
        
        with open(f'{self.output_dir}/visuals_metadata.json', 'w') as f:
            json.dump(visuals_metadata, f, indent=2)
        
        print(f"\n✅ Downloaded {len(downloaded_files)} video clips")
        
        return downloaded_files


def main():
    """Test the visuals fetcher"""
    
    try:
        fetcher = VisualsFetcher()
        
        # Try to fetch based on existing script, or use default
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        script_path = f"{output_dir}/script.json"
        
        if os.path.exists(script_path):
            print(f"📄 Using script from: {script_path}\n")
            video_files = fetcher.fetch_videos_for_script()
        else:
            print("⚠️  No script found. Fetching sample videos...\n")
            
            # Fetch some sample videos
            sample_queries = ["technology", "nature", "city"]
            video_files = []
            
            for query in sample_queries:
                videos = fetcher.search_videos(query, count=2)
                
                for idx, video in enumerate(videos):
                    filename = f"sample_{query}_{idx}.mp4"
                    filepath = fetcher.download_video(video['url'], filename)
                    video_files.append(filepath)
                    time.sleep(1)
        
        print("\n" + "="*60)
        print("✅ Video downloads complete!")
        print("="*60)
        print(f"📁 Total clips downloaded: {len(video_files)}")
        for f in video_files:
            print(f"   • {f}")
        print("="*60)
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\n💡 To fix this:")
        print("   1. Get a free API key at https://www.pexels.com/api/")
        print("   2. Add it to your .env file: PEXELS_API_KEY=your_key_here")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
