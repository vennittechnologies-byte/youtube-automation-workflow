#!/usr/bin/env python3
"""
Main Pipeline Orchestrator
Runs the complete automated YouTube video creation and upload workflow
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

# Import pipeline modules
try:
    from script_generator import ScriptGenerator
    from voiceover import generate_from_script_file
    from visuals import VisualsFetcher
    from thumbnails import ThumbnailGenerator
    from compose import VideoComposer
    from upload import YouTubeUploader
except ImportError as e:
    print(f"❌ Failed to import pipeline modules: {str(e)}")
    print("   Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv()


class PipelineOrchestrator:
    """Orchestrate the full video creation pipeline"""
    
    def __init__(self):
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.run_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create timestamped run directory
        self.run_dir = Path(self.output_dir) / f'run_{self.run_timestamp}'
        
    def run_full_pipeline(self, topic: Optional[str] = None, upload_to_youtube: bool = True) -> dict:
        """
        Run the complete pipeline
        
        Args:
            topic: Optional topic override (uses topics.json if not provided)
            upload_to_youtube: Whether to upload the final video to YouTube
            
        Returns:
            Dictionary with pipeline results
        """
        
        print("\n" + "="*70)
        print("🚀 AUTOMATED YOUTUBE VIDEO PIPELINE")
        print("="*70)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        results = {
            'success': False,
            'timestamp': self.run_timestamp,
            'stages': {}
        }
        
        try:
            # Stage 1: Script Generation
            print("\n📝 STAGE 1: SCRIPT GENERATION")
            print("-" * 70)
            
            topic_to_use = topic or self._get_next_topic()
            print(f"Topic: {topic_to_use}\n")
            
            generator = ScriptGenerator()
            script_data = generator.generate_script(topic_to_use)
            
            # Save script
            with open(f'{self.output_dir}/script.json', 'w') as f:
                json.dump(script_data, f, indent=2)
            
            results['stages']['script'] = {
                'success': True,
                'title': script_data['title'],
                'word_count': script_data['word_count']
            }
            
            print(f"\n✅ Script generated: {script_data['title']}")
            
            # Stage 2: Voiceover Generation
            print("\n" + "="*70)
            print("🎙️  STAGE 2: VOICEOVER GENERATION")
            print("-" * 70 + "\n")
            
            audio_path = asyncio.run(generate_from_script_file())
            
            results['stages']['voiceover'] = {
                'success': True,
                'audio_path': audio_path
            }
            
            print(f"✅ Voiceover generated")
            
            # Stage 3: Visual Assets
            print("\n" + "="*70)
            print("📹 STAGE 3: FETCHING VISUAL ASSETS")
            print("-" * 70 + "\n")
            
            fetcher = VisualsFetcher()
            video_clips = fetcher.fetch_videos_for_script(script_data)
            
            results['stages']['visuals'] = {
                'success': True,
                'clips_downloaded': len(video_clips)
            }
            
            print(f"✅ Downloaded {len(video_clips)} video clips")
            
            # Stage 4: Thumbnail Generation
            print("\n" + "="*70)
            print("🎨 STAGE 4: THUMBNAIL GENERATION")
            print("-" * 70 + "\n")
            
            thumbnail_gen = ThumbnailGenerator()
            thumbnail_path = thumbnail_gen.create_from_script(script_data)
            
            results['stages']['thumbnail'] = {
                'success': True,
                'thumbnail_path': thumbnail_path
            }
            
            print(f"✅ Thumbnail created")
            
            # Stage 5: Video Composition
            print("\n" + "="*70)
            print("🎬 STAGE 5: VIDEO COMPOSITION")
            print("-" * 70 + "\n")
            
            composer = VideoComposer()
            video_path = composer.create_from_pipeline_output()
            
            results['stages']['composition'] = {
                'success': True,
                'video_path': video_path
            }
            
            print(f"✅ Video composed")
            
            # Stage 6: YouTube Upload (optional)
            if upload_to_youtube:
                print("\n" + "="*70)
                print("📤 STAGE 6: YOUTUBE UPLOAD")
                print("-" * 70 + "\n")
                
                try:
                    uploader = YouTubeUploader()
                    upload_response = uploader.upload_from_pipeline_output()
                    
                    results['stages']['upload'] = {
                        'success': True,
                        'video_url': upload_response['url'],
                        'video_id': upload_response['id']
                    }
                    
                    print(f"✅ Video uploaded: {upload_response['url']}")
                    
                except Exception as e:
                    print(f"⚠️  Upload failed: {str(e)}")
                    print("   Video saved locally, you can upload manually later.")
                    
                    results['stages']['upload'] = {
                        'success': False,
                        'error': str(e)
                    }
            else:
                print("\n⏭️  Skipping YouTube upload (disabled)")
                results['stages']['upload'] = {'success': True, 'skipped': True}
            
            # Pipeline complete
            results['success'] = True
            
            print("\n" + "="*70)
            print("🎉 PIPELINE COMPLETE!")
            print("="*70)
            
            # Summary
            print("\n📊 SUMMARY:")
            print(f"   Title: {script_data['title']}")
            print(f"   Video: {video_path}")
            if upload_to_youtube and results['stages']['upload'].get('success'):
                print(f"   YouTube: {results['stages']['upload'].get('video_url')}")
            
            print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Pipeline interrupted by user")
            results['success'] = False
            results['error'] = 'Interrupted by user'
            
        except Exception as e:
            print(f"\n\n❌ Pipeline failed: {str(e)}")
            results['success'] = False
            results['error'] = str(e)
            
            import traceback
            print("\n🔍 Full error traceback:")
            traceback.print_exc()
        
        # Save pipeline results
        results_path = Path(self.output_dir) / 'pipeline_results.json'
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def _get_next_topic(self) -> str:
        """Get next topic from topics.json"""
        
        topics_file = 'config/topics.json'
        
        try:
            with open(topics_file, 'r') as f:
                topics_data = json.load(f)
            
            topics = topics_data.get('topics', [])
            if not topics:
                return os.getenv('DEFAULT_TOPIC', 'Technology Trends')
            
            # Get current index
            last_index = topics_data.get('last_used_index', 0)
            
            # Rotate to next topic
            next_index = (last_index + 1) % len(topics)
            next_topic = topics[next_index]['title']
            
            # Update index
            topics_data['last_used_index'] = next_index
            with open(topics_file, 'w') as f:
                json.dump(topics_data, f, indent=2)
            
            return next_topic
            
        except Exception as e:
            print(f"⚠️  Could not load topics: {str(e)}")
            return os.getenv('DEFAULT_TOPIC', 'Technology Trends')


def main():
    """Main entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Automated YouTube Video Creation Pipeline'
    )
    parser.add_argument(
        '--topic',
        type=str,
        help='Topic for video (uses topics.json rotation if not specified)'
    )
    parser.add_argument(
        '--no-upload',
        action='store_true',
        help='Skip YouTube upload (create video only)'
    )
    
    args = parser.parse_args()
    
    # Run pipeline
    orchestrator = PipelineOrchestrator()
    results = orchestrator.run_full_pipeline(
        topic=args.topic,
        upload_to_youtube=not args.no_upload
    )
    
    # Exit with appropriate code
    sys.exit(0 if results['success'] else 1)


if __name__ == "__main__":
    main()
