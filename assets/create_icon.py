#!/usr/bin/env python3
"""Create icon from eye emoji for cross-platform use."""

import sys
from PIL import Image, ImageDraw, ImageFont

def create_emoji_icon():
    """Create a PNG icon from the eye emoji."""
    # Create a 64x64 image with transparent background
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to use system font that supports emoji
    try:
        # macOS
        font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 48)
    except:
        try:
            # Windows
            font = ImageFont.truetype("seguiemj.ttf", 48)  
        except:
            try:
                # Linux/fallback
                font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 48)
            except:
                font = ImageFont.load_default()
    
    # Draw the eye emoji centered
    emoji = "👁️"
    bbox = draw.textbbox((0, 0), emoji, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), emoji, font=font, fill=(0, 0, 0, 255))
    
    # Save as PNG
    img.save('assets/icon.png')
    print("Icon created: assets/icon.png")

if __name__ == "__main__":
    try:
        create_emoji_icon()
    except ImportError:
        print("PIL not available. Creating simple text-based icon...")
        # Fallback: create a simple text file that can be used as reference
        with open('assets/icon.txt', 'w') as f:
            f.write('👁️')
        print("Created assets/icon.txt - install PIL to generate PNG")