#!/usr/bin/env python3
"""
Voiceover Generator Module
Converts text scripts to natural-sounding speech using Edge-TTS
"""

import os
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

try:
    from edge_tts import Communicate, list_voices
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️  edge-tts not installed. Install with: pip install edge-tts")

# Load environment variables
load_dotenv()


class VoiceoverGenerator:
    """Generate voiceovers using Edge-TTS"""
    
    def __init__(self):
        if not EDGE_TTS_AVAILABLE:
            raise RuntimeError("edge-tts is required. Install with: pip install edge-tts")
        
        self.voice = os.getenv('TTS_VOICE', 'en-US-JennyNeural')
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        
    async def generate_voiceover(
        self, 
        text: str, 
        output_filename: str = "voiceover.mp3",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ) -> str:
        """
        Generate voiceover from text
        
        Args:
            text: The script text to convert to speech
            output_filename: Output filename (default: voiceover.mp3)
            rate: Speech rate adjustment (e.g., "+10%" for faster, "-10%" for slower)
            volume: Volume adjustment (e.g., "+50%" for louder)
            pitch: Pitch adjustment (e.g., "+5Hz" for higher pitch)
            
        Returns:
            Path to the generated audio file
        """
        
        print(f"🎙️  Generating voiceover with voice: {self.voice}")
        
        # Ensure output directory exists
        audio_dir = Path(self.output_dir) / 'audio'
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = audio_dir / output_filename
        
        try:
            # Create communicate instance
            communicate = Communicate(
                text=text,
                voice=self.voice,
                rate=rate,
                volume=volume,
                pitch=pitch
            )
            
            # Save audio
            await communicate.save(str(output_path))
            
            print(f"✅ Voiceover saved to: {output_path}")
            print(f"📏 Text length: {len(text)} characters")
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate voiceover: {str(e)}")
    
    async def get_available_voices(self, language: str = "en") -> list:
        """
        Get list of available voices for a language
        
        Args:
            language: Language code (e.g., "en", "es", "fr")
            
        Returns:
            List of voice dictionaries
        """
        
        voices = await list_voices()
        filtered_voices = [
            v for v in voices 
            if v["Locale"].startswith(language)
        ]
        
        return filtered_voices
    
    def display_voice_options(self):
        """Display available voice options"""
        
        print("\n🎤 Popular Voice Options:")
        print("-" * 60)
        
        popular_voices = [
            ("en-US-JennyNeural", "Friendly female (US)", "Best for: Tutorials, casual content"),
            ("en-US-GuyNeural", "Professional male (US)", "Best for: Business, formal content"),
            ("en-US-AriaNeural", "Natural female (US)", "Best for: Narration, storytelling"),
            ("en-GB-SoniaNeural", "British female", "Best for: Documentary style"),
            ("en-AU-NatashaNeural", "Australian female", "Best for: Energetic content"),
            ("en-US-DavisNeural", "Confident male (US)", "Best for: Tech, reviews"),
            ("en-GB-RyanNeural", "British male", "Best for: Education, podcasts"),
        ]
        
        for voice_id, description, best_for in popular_voices:
            print(f"• {voice_id}")
            print(f"  {description}")
            print(f"  {best_for}\n")


async def generate_from_script_file(script_path: str = None) -> str:
    """
    Generate voiceover from a saved script file
    
    Args:
        script_path: Path to script.json file
        
    Returns:
        Path to generated audio file
    """
    
    if script_path is None:
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        script_path = f"{output_dir}/script.json"
    
    # Load script
    try:
        with open(script_path, 'r') as f:
            script_data = json.load(f)
        
        text = script_data.get('script', '')
        
        if not text:
            raise ValueError("No script text found in file")
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Script file not found: {script_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in script file: {script_path}")
    
    # Generate voiceover
    generator = VoiceoverGenerator()
    audio_path = await generator.generate_voiceover(text)
    
    # Save metadata
    audio_metadata = {
        "audio_path": audio_path,
        "voice": generator.voice,
        "text_length": len(text),
        "script_file": script_path
    }
    
    output_dir = os.getenv('OUTPUT_DIR', 'output')
    with open(f'{output_dir}/audio_metadata.json', 'w') as f:
        json.dump(audio_metadata, f, indent=2)
    
    return audio_path


def main():
    """Main function for testing"""
    
    # Test with a sample script or load from file
    script_path = None
    
    # Try to load from saved script
    output_dir = os.getenv('OUTPUT_DIR', 'output')
    test_script_path = f"{output_dir}/script.json"
    
    if os.path.exists(test_script_path):
        print(f"📄 Found existing script at {test_script_path}")
        script_path = test_script_path
    else:
        print("⚠️  No script found. Generating sample voiceover...")
        
        # Create sample script
        sample_text = """
        Hey there! Welcome back to the channel. Today we're diving into something absolutely fascinating 
        that's reshaping our world as we speak. Have you ever wondered how AI is transforming the way 
        we work, create, and connect? Well, buckle up because what I'm about to share might just blow your mind.
        
        First off, artificial intelligence isn't just some sci-fi fantasy anymore. It's here, it's real, 
        and it's making waves across every industry you can think of. From healthcare to entertainment, 
        AI is becoming the invisible force that's making our lives easier, smarter, and more efficient.
        
        But here's the thing that really gets me excited - we're just scratching the surface. The innovations 
        happening right now are setting the stage for a future that seemed impossible just a few years ago.
        
        So if you found this interesting, smash that like button, subscribe for more mind-blowing content, 
        and drop a comment below telling me - what excites you most about AI? I read every single one, 
        and I'd love to hear your thoughts. See you in the next video!
        """
        
        # Save sample script
        os.makedirs(output_dir, exist_ok=True)
        sample_data = {
            "title": "Sample Video About AI",
            "script": sample_text.strip(),
            "tags": ["AI", "technology", "future"]
        }
        
        with open(test_script_path, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        script_path = test_script_path
    
    # Generate voiceover
    audio_path = asyncio.run(generate_from_script_file(script_path))
    
    print(f"\n✅ Voiceover generation complete!")
    print(f"📁 Audio file: {audio_path}")
    
    # Display voice options for reference
    generator = VoiceoverGenerator()
    generator.display_voice_options()


if __name__ == "__main__":
    main()
