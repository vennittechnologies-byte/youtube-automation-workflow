#!/usr/bin/env python3
"""
Video Composer Module
Combines video clips, audio, and creates the final video using MoviePy
"""

import os
import json
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, concatenate_videoclips,
        CompositeVideoClip, TextClip, ColorClip
    )
    from moviepy.video.fx import resize, fadein, fadeout
    import moviepy.video.fx.all as vfx
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not installed. Install with: pip install moviepy")

# Load environment variables
load_dotenv()


class VideoComposer:
    """Compose final video from clips and audio"""
    
    def __init__(self):
        if not MOVIEPY_AVAILABLE:
            raise RuntimeError("MoviePy is required. Install with: pip install moviepy")
        
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.video_width = int(os.getenv('VIDEO_WIDTH', 1920))
        self.video_height = int(os.getenv('VIDEO_HEIGHT', 1080))
        self.video_fps = int(os.getenv('VIDEO_FPS', 30))
    
    def create_video(
        self,
        video_clips: List[str],
        audio_path: str,
        output_filename: str = "final_video.mp4",
        add_transitions: bool = True,
        transition_duration: float = 0.5
    ) -> str:
        """
        Create final video from clips and audio
        
        Args:
            video_clips: List of video clip file paths
            audio_path: Path to audio file
            output_filename: Output filename
            add_transitions: Whether to add fade transitions between clips
            transition_duration: Duration of transitions in seconds
            
        Returns:
            Path to final video file
        """
        
        print(f"🎬 Creating video from {len(video_clips)} clips...")
        
        if not video_clips:
            raise ValueError("No video clips provided")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load audio to get target duration
        audio = AudioFileClip(audio_path)
        target_duration = audio.duration
        
        print(f"🎵 Audio duration: {target_duration:.2f} seconds")
        
        # Load and process video clips
        clips = self._load_and_process_clips(
            video_clips,
            target_duration,
            add_transitions,
            transition_duration
        )
        
        # Concatenate clips
        print("🔗 Concatenating clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Ensure video matches audio duration
        if final_video.duration > target_duration:
            final_video = final_video.subclip(0, target_duration)
        elif final_video.duration < target_duration:
            # Loop the video if it's shorter than audio
            loops_needed = int(target_duration / final_video.duration) + 1
            final_video = concatenate_videoclips([final_video] * loops_needed)
            final_video = final_video.subclip(0, target_duration)
        
        # Add audio
        print("🎵 Adding audio track...")
        final_video = final_video.set_audio(audio)
        
        # Export final video
        output_path = Path(self.output_dir) / 'videos' / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"📤 Exporting video... (this may take a while)")
        
        final_video.write_videofile(
            str(output_path),
            fps=self.video_fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            threads=4,
            preset='medium',
            ffmpeg_params=['-crf', '23']  # Quality setting (lower = better, 18-28 recommended)
        )
        
        # Clean up
        audio.close()
        for clip in clips:
            clip.close()
        final_video.close()
        
        print(f"✅ Video exported to: {output_path}")
        
        # Get file size
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"📊 File size: {file_size_mb:.2f} MB")
        
        return str(output_path)
    
    def _load_and_process_clips(
        self,
        clip_paths: List[str],
        total_duration: float,
        add_transitions: bool,
        transition_duration: float
    ) -> List[VideoFileClip]:
        """Load and process video clips"""
        
        clips = []
        duration_per_clip = total_duration / len(clip_paths)
        
        print(f"⏱️  Target duration per clip: {duration_per_clip:.2f} seconds")
        
        for idx, clip_path in enumerate(clip_paths):
            if not os.path.exists(clip_path):
                print(f"⚠️  Clip not found: {clip_path}, skipping...")
                continue
            
            print(f"📹 Processing clip {idx + 1}/{len(clip_paths)}: {Path(clip_path).name}")
            
            # Load clip
            clip = VideoFileClip(clip_path)
            
            # Resize to target dimensions
            clip = clip.fx(resize.resize, height=self.video_height)
            
            # If clip is wider than target, crop it
            if clip.w > self.video_width:
                x_center = clip.w / 2
                x1 = x_center - self.video_width / 2
                clip = clip.crop(x1=x_center - self.video_width/2, 
                               x2=x_center + self.video_width/2)
            
            # Set duration for this clip
            if clip.duration > duration_per_clip:
                # Clip is longer, so trim it from the middle
                start_time = (clip.duration - duration_per_clip) / 2
                clip = clip.subclip(start_time, start_time + duration_per_clip)
            else:
                # Clip is shorter, so slow it down slightly
                speed_factor = clip.duration / duration_per_clip
                if speed_factor > 0.5:  # Don't slow down too much
                    clip = clip.fx(vfx.speedx, speed_factor)
                else:
                    # If too short, just use as is and let concatenate handle it
                    pass
            
            # Add transitions
            if add_transitions:
                if idx > 0:  # Fade in (except first clip)
                    clip = clip.fx(fadein, transition_duration)
                if idx < len(clip_paths) - 1:  # Fade out (except last clip)
                    clip = clip.fx(fadeout, transition_duration)
            
            clips.append(clip)
        
        return clips
    
    def create_from_pipeline_output(self) -> str:
        """
        Create video using outputs from previous pipeline steps
        
        Returns:
            Path to final video file
        """
        
        # Load metadata from previous steps
        try:
            with open(f'{self.output_dir}/visuals_metadata.json', 'r') as f:
                visuals_meta = json.load(f)
                video_clips = visuals_meta['downloaded_files']
        except FileNotFoundError:
            raise FileNotFoundError(
                "Visuals metadata not found. Run visuals.py first."
            )
        
        try:
            with open(f'{self.output_dir}/audio_metadata.json', 'r') as f:
                audio_meta = json.load(f)
                audio_path = audio_meta['audio_path']
        except FileNotFoundError:
            raise FileNotFoundError(
                "Audio metadata not found. Run voiceover.py first."
            )
        
        # Create video
        video_path = self.create_video(video_clips, audio_path)
        
        # Save video metadata
        with open(f'{self.output_dir}/script.json', 'r') as f:
            script_data = json.load(f)
        
        video_metadata = {
            "video_path": video_path,
            "title": script_data.get('title', 'Video'),
            "duration": AudioFileClip(audio_path).duration,
            "clips_used": len(video_clips),
            "resolution": f"{self.video_width}x{self.video_height}",
            "fps": self.video_fps
        }
        
        with open(f'{self.output_dir}/video_metadata.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        return video_path


def main():
    """Test the video composer"""
    
    try:
        composer = VideoComposer()
        
        # Create video from pipeline output
        print("🎬 Starting video composition...\n")
        
        video_path = composer.create_from_pipeline_output()
        
        print("\n" + "="*60)
        print("✅ Video composition complete!")
        print("="*60)
        print(f"📁 Final video: {video_path}")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n❌ Missing required files: {str(e)}")
        print("\n💡 Make sure to run the pipeline in order:")
        print("   1. python scripts/script_generator.py")
        print("   2. python scripts/voiceover.py")
        print("   3. python scripts/visuals.py")
        print("   4. python scripts/compose.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
