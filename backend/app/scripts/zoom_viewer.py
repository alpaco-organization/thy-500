#!/usr/bin/env python3
"""Shows outlier persons on the full texture image with crosshairs."""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image, ImageDraw, ImageFont

# Allow large images
Image.MAX_IMAGE_PIXELS = None

# ============== CONFIGURE HERE ==============
INPUT_SIZE = 64000
TEXTURE_SIZE = 32000
OUTPUT_SIZE = 4000  # Resize to this for viewing
SAVE_OUTPUT = True  # Set to True to save the image
OUTPUT_FILENAME = "outliers_visualization.png"
# ============================================

SCRIPT_DIR = Path(__file__).parent
IMAGE_PATH = SCRIPT_DIR / "datas" / "raw_data" / "32k_texture.png"
CSV_PATH = SCRIPT_DIR / "datas/mapped_data/outliers_x_above_5.csv"
JSON_PATH = SCRIPT_DIR / "datas/raw_data/40223_facerec_output.json"

# Colors for different markers
COLORS = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'orange', 'lime', 'pink', 'white']


def normalize_id(value) -> str:
    """Normalize an ID value to string, handling int/str types."""
    if value is None:
        return ''
    return str(value).strip().lstrip('0')


def load_outliers_csv() -> List[Dict]:
    """Load outlier persons from CSV file."""
    outliers = []
    
    if not CSV_PATH.exists():
        print(f"❌ CSV file not found: {CSV_PATH}")
        return outliers
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            outliers.append({
                'personId': row['personId'],
                'name': row['name'],
                'x': float(row['x']),
                'y': float(row['y']),
                'z': float(row['z']),
            })
    
    print(f"✓ Loaded {len(outliers)} outliers from CSV")
    return outliers


def load_facerec_json() -> List[Dict]:
    """Load face recognition data from JSON file."""
    if not JSON_PATH.exists():
        print(f"❌ JSON file not found: {JSON_PATH}")
        return []
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✓ Loaded {len(data)} records from JSON")
    return data


def find_person_in_json(person_id: str, facerec_data: List[Dict]) -> Optional[Dict]:
    """Find a person in the facerec JSON by personId/sicil."""
    person_id_normalized = normalize_id(person_id)
    person_id_raw = str(person_id).strip()
    
    for record in facerec_data:
        # Check assigned_sicil
        assigned = record.get('assigned_sicil')
        if assigned:
            if normalize_id(assigned) == person_id_normalized:
                return record
            if str(assigned).strip() == person_id_raw:
                return record
        
        # Check matched_person fields
        matched = record.get('matched_person', {})
        if matched:
            # Check sicil
            sicil = matched.get('sicil')
            if sicil:
                if normalize_id(sicil) == person_id_normalized:
                    return record
                if str(sicil).strip() == person_id_raw:
                    return record
            
            # Check id
            matched_id = matched.get('id')
            if matched_id:
                if normalize_id(matched_id) == person_id_normalized:
                    return record
                if str(matched_id).strip() == person_id_raw:
                    return record
    
    return None


def match_outliers_to_pixels(outliers: List[Dict], facerec_data: List[Dict]) -> List[Dict]:
    """Match outliers from CSV to pixel coordinates from JSON."""
    matched = []
    
    for outlier in outliers:
        person_id = outlier['personId']
        record = find_person_in_json(person_id, facerec_data)
        
        if record:
            center = record.get('center_global', {})
            pixel_x = center.get('x')
            pixel_y = center.get('y')
            
            if pixel_x is not None and pixel_y is not None:
                matched.append({
                    'personId': person_id,
                    'name': outlier['name'],
                    'pixel_x': pixel_x,
                    'pixel_y': pixel_y,
                    '3d_x': outlier['x'],
                    '3d_y': outlier['y'],
                    '3d_z': outlier['z'],
                    'json_id': record.get('id'),
                    'filename': record.get('filename', '')
                })
                print(f"  ✓ {outlier['name']} ({person_id}) -> pixel ({pixel_x}, {pixel_y})")
            else:
                print(f"  ⚠ No pixel coords: {outlier['name']} ({person_id})")
        else:
            print(f"  ❌ Not found: {outlier['name']} ({person_id})")
    
    return matched


def draw_markers(img: Image.Image, matched_persons: List[Dict]) -> Image.Image:
    """Draw crosshair markers for each matched person."""
    draw = ImageDraw.Draw(img)
    scale = TEXTURE_SIZE / INPUT_SIZE
    
    # Try to load a font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 60)
            small_font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                # macOS fonts
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
                small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            except:
                font = ImageFont.load_default()
                small_font = font
    
    # Draw each person
    for i, person in enumerate(matched_persons):
        color = COLORS[i % len(COLORS)]
        
        scaled_x = int(person['pixel_x'] * scale)
        scaled_y = int(person['pixel_y'] * scale)
        
        line_width = 25
        line_length = 100
        radius = 200
        
        # Crosshair
        draw.line(
            [(scaled_x - line_length, scaled_y), (scaled_x + line_length, scaled_y)],
            fill=color, width=line_width
        )
        draw.line(
            [(scaled_x, scaled_y - line_length), (scaled_x, scaled_y + line_length)],
            fill=color, width=line_width
        )
        
        # Circle
        draw.ellipse(
            [(scaled_x - radius, scaled_y - radius), 
             (scaled_x + radius, scaled_y + radius)],
            outline=color, width=line_width
        )
        
        # Label with number
        label = f"{i+1}"
        label_x = scaled_x + radius + 50
        label_y = scaled_y - 50
        
        bbox = draw.textbbox((label_x, label_y), label, font=font)
        padding = 20
        draw.rectangle(
            [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
            fill='black'
        )
        draw.text((label_x, label_y), label, fill=color, font=font)
    
    # Legend at top-left (limit to first 20 for readability)
    display_count = min(len(matched_persons), 30)
    legend_y = 100
    legend_height = 100 + display_count * 100 + 50
    draw.rectangle([50, 50, 3500, legend_height], fill='black', outline='white', width=5)
    draw.text((100, legend_y), f"OUTLIERS (x > 5) - Showing {display_count}/{len(matched_persons)}:", fill='white', font=font)
    legend_y += 100
    
    for i in range(display_count):
        person = matched_persons[i]
        color = COLORS[i % len(COLORS)]
        text = f"{i+1}. {person['name'][:20]} | px:({person['pixel_x']}, {person['pixel_y']}) | 3D:({person['3d_x']:.1f}, {person['3d_y']:.1f}, {person['3d_z']:.1f})"
        draw.text((100, legend_y), text, fill=color, font=small_font)
        legend_y += 70
    
    return img


def main():
    print("=" * 60)
    print("OUTLIER VISUALIZATION")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading data...")
    outliers = load_outliers_csv()
    facerec_data = load_facerec_json()
    
    if not outliers or not facerec_data:
        print("❌ Missing data, exiting")
        return
    
    # Match outliers to pixels
    print("\n🔍 Matching outliers to pixel coordinates...")
    matched = match_outliers_to_pixels(outliers, facerec_data)
    
    if not matched:
        print("❌ No matches found")
        return
    
    print(f"\n✓ Matched {len(matched)}/{len(outliers)} outliers")
    
    # Load image
    print("\n🖼️ Loading texture image...")
    if not IMAGE_PATH.exists():
        print(f"❌ Image not found: {IMAGE_PATH}")
        return
    
    img = Image.open(IMAGE_PATH)
    print(f"   Size: {img.size}")
    
    # Draw markers
    print("\n✏️ Drawing markers...")
    img = draw_markers(img, matched)
    
    # Resize
    print(f"\n📐 Resizing to {OUTPUT_SIZE}x{OUTPUT_SIZE}...")
    img = img.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)
    
    # Save if enabled
    if SAVE_OUTPUT:
        output_path = SCRIPT_DIR / OUTPUT_FILENAME
        print(f"\n💾 Saving to {output_path}...")
        img.save(output_path)
        print("   ✓ Saved!")
    
    # Print summary (first 10)
    print("\n" + "=" * 60)
    print(f"SUMMARY (First 10 of {len(matched)})")
    print("=" * 60)
    for i, person in enumerate(matched[:10]):
        print(f"\n{i+1}. {person['name']}")
        print(f"   ID: {person['personId']}")
        print(f"   Pixel: ({person['pixel_x']}, {person['pixel_y']})")
        print(f"   3D: ({person['3d_x']:.3f}, {person['3d_y']:.3f}, {person['3d_z']:.3f})")
    
    if len(matched) > 10:
        print(f"\n... and {len(matched) - 10} more")
    
    # Show image
    print("\n🖥️ Displaying image...")
    img.show()


if __name__ == "__main__":
    main()