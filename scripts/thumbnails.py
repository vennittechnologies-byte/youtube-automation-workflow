#!/usr/bin/env python3
"""
Thumbnail Generator Module
Creates eye-catching YouTube thumbnails programmatically
"""

import os
import json
from pathlib import Path
from typing import Tuple, Optional
from dotenv import load_dotenv

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Pillow not installed. Install with: pip install Pillow")

# Load environment variables
load_dotenv()


class ThumbnailGenerator:
    """Generate YouTube thumbnails"""
    
    # YouTube thumbnail recommended size
    THUMBNAIL_SIZE = (1280, 720)
    
    def __init__(self):
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow is required. Install with: pip install Pillow")
        
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.thumbnail_dir = Path(self.output_dir) / 'thumbnails'
        self.thumbnail_dir.mkdir(parents=True, exist_ok=True)
    
    def create_thumbnail(
        self,
        title: str,
        background_image: Optional[str] = None,
        background_color: Tuple[int, int, int] = (20, 25, 35),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        accent_color: Tuple[int, int, int] = (249, 115, 22),
        output_filename: str = "thumbnail.jpg"
    ) -> str:
        """
        Create a YouTube thumbnail
        
        Args:
            title: Video title text
            background_image: Path to background image (optional)
            background_color: RGB color for solid background if no image
            text_color: RGB color for title text
            accent_color: RGB color for accent elements
            output_filename: Output filename
            
        Returns:
            Path to generated thumbnail
        """
        
        print(f"🎨 Creating thumbnail...")
        
        # Create base image
        if background_image and os.path.exists(background_image):
            thumbnail = self._create_from_image(background_image)
        else:
            thumbnail = self._create_gradient_background(background_color, accent_color)
        
        # Add title text
        thumbnail = self._add_title_text(thumbnail, title, text_color, accent_color)
        
        # Add visual enhancements
        thumbnail = self._add_visual_polish(thumbnail)
        
        # Save thumbnail
        output_path = self.thumbnail_dir / output_filename
        thumbnail.save(output_path, "JPEG", quality=95, optimize=True)
        
        print(f"✅ Thumbnail saved to: {output_path}")
        
        return str(output_path)
    
    def _create_from_image(self, image_path: str) -> Image.Image:
        """Create thumbnail from existing image"""
        
        img = Image.open(image_path)
        
        # Resize to thumbnail dimensions
        img = img.resize(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        
        # Apply slight darkening for text readability
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.6)
        
        # Add slight blur to background
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        
        return img
    
    def _create_gradient_background(
        self, 
        base_color: Tuple[int, int, int],
        accent_color: Tuple[int, int, int]
    ) -> Image.Image:
        """Create a gradient background"""
        
        width, height = self.THUMBNAIL_SIZE
        img = Image.new('RGB', self.THUMBNAIL_SIZE)
        draw = ImageDraw.Draw(img)
        
        # Create vertical gradient
        for y in range(height):
            # Calculate color blend ratio
            ratio = y / height
            
            r = int(base_color[0] + (accent_color[0] - base_color[0]) * ratio * 0.3)
            g = int(base_color[1] + (accent_color[1] - base_color[1]) * ratio * 0.3)
            b = int(base_color[2] + (accent_color[2] - base_color[2]) * ratio * 0.3)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return img
    
    def _add_title_text(
        self,
        img: Image.Image,
        title: str,
        text_color: Tuple[int, int, int],
        accent_color: Tuple[int, int, int]
    ) -> Image.Image:
        """Add title text to thumbnail"""
        
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Try to load a bold font, fallback to default
        try:
            # Common font paths for different systems
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\arialbd.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ]
            
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 80)
                    break
            
            if font is None:
                font = ImageFont.load_default()
                print("⚠️  Using default font. Install TrueType fonts for better results.")
        except:
            font = ImageFont.load_default()
        
        # Split title into multiple lines if needed
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            
            # Check if line is too long
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > width * 0.85:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 3 lines
        lines = lines[:3]
        
        # Calculate total text height
        line_height = 100
        total_height = len(lines) * line_height
        
        # Starting Y position (vertically centered)
        y = (height - total_height) // 2
        
        # Draw each line
        for line in lines:
            # Get text bounding box
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center horizontally
            x = (width - text_width) // 2
            
            # Draw text shadow for better readability
            shadow_offset = 4
            draw.text(
                (x + shadow_offset, y + shadow_offset),
                line,
                font=font,
                fill=(0, 0, 0, 180)
            )
            
            # Draw main text
            draw.text((x, y), line, font=font, fill=text_color)
            
            y += line_height
        
        # Add accent bar at bottom
        bar_height = 8
        bar_y = height - 60
        draw.rectangle(
            [(width * 0.1, bar_y), (width * 0.9, bar_y + bar_height)],
            fill=accent_color
        )
        
        return img
    
    def _add_visual_polish(self, img: Image.Image) -> Image.Image:
        """Add final visual polish to thumbnail"""
        
        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Increase saturation slightly
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    def create_from_script(self, script_data: Dict = None) -> str:
        """
        Create thumbnail from script data
        
        Args:
            script_data: Dictionary containing script and metadata
            
        Returns:
            Path to generated thumbnail
        """
        
        # Load script if not provided
        if script_data is None:
            script_path = f"{self.output_dir}/script.json"
            try:
                with open(script_path, 'r') as f:
                    script_data = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Script file not found: {script_path}")
        
        title = script_data.get('title', 'Video Title')
        
        # Try to use first video clip as background
        background_image = None
        try:
            clips_dir = Path(self.output_dir) / 'clips'
            if clips_dir.exists():
                clip_files = list(clips_dir.glob('*.mp4'))
                if clip_files:
                    # Extract first frame from first video as background
                    # For now, skip this and use gradient
                    pass
        except:
            pass
        
        # Generate thumbnail
        thumbnail_path = self.create_thumbnail(
            title=title,
            background_image=background_image
        )
        
        # Save metadata
        thumbnail_metadata = {
            "thumbnail_path": thumbnail_path,
            "title": title
        }
        
        with open(f'{self.output_dir}/thumbnail_metadata.json', 'w') as f:
            json.dump(thumbnail_metadata, f, indent=2)
        
        return thumbnail_path


def main():
    """Test the thumbnail generator"""
    
    try:
        generator = ThumbnailGenerator()
        
        # Try to use existing script
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        script_path = f"{output_dir}/script.json"
        
        if os.path.exists(script_path):
            print(f"📄 Using script from: {script_path}\n")
            thumbnail_path = generator.create_from_script()
        else:
            print("⚠️  No script found. Creating sample thumbnail...\n")
            
            # Create sample thumbnail
            thumbnail_path = generator.create_thumbnail(
                title="The Future of AI Technology",
                output_filename="sample_thumbnail.jpg"
            )
        
        print("\n" + "="*60)
        print("✅ Thumbnail generation complete!")
        print("="*60)
        print(f"📁 Thumbnail saved to: {thumbnail_path}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
