#!/usr/bin/env python3
"""
Extract outliers from persons_mapped.json
Creates CSV files for people outside cabin boundaries:
- outliers_x_above_5.csv: X > 5
- outliers_x_below_minus5.csv: X < -5
"""

import json
import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / "datas" / "mapped_data" / "persons_mapped.json"
OUTPUT_DIR = SCRIPT_DIR / "datas" / "mapped_data"


def main():
    print("=" * 60)
    print("EXTRACT OUTLIERS")
    print("=" * 60)

    # Load data
    print("\nLoading persons_mapped.json...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        persons = json.load(f)

    print(f"Total persons: {len(persons)}")

    # Extract outliers
    outliers_above_5 = [p for p in persons if p['x'] > 5]
    outliers_below_minus5 = [p for p in persons if p['x'] < -5]
    inliers = [p for p in persons if -5 <= p['x'] <= 5]

    print(f"X > 5: {len(outliers_above_5)}")
    print(f"X < -5: {len(outliers_below_minus5)}")
    print(f"In range [-5, 5]: {len(inliers)}")

    # Save outliers_x_above_5.csv
    print(f"\nSaving outliers_x_above_5.csv...")
    csv_path_above = OUTPUT_DIR / "outliers_x_above_5.csv"
    with open(csv_path_above, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['personId', 'name', 'x', 'y', 'z', 'grid_filename'])
        writer.writeheader()
        for p in outliers_above_5:
            writer.writerow({
                'personId': p['personId'],
                'name': p['name'],
                'x': p['x'],
                'y': p['y'],
                'z': p['z'],
                'grid_filename': p.get('grid_filename', 'grid_1.png')
            })
    print(f"  Saved: {csv_path_above}")

    # Save outliers_x_below_minus5.csv
    print(f"\nSaving outliers_x_below_minus5.csv...")
    csv_path_below = OUTPUT_DIR / "outliers_x_below_minus5.csv"
    with open(csv_path_below, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['personId', 'name', 'x', 'y', 'z', 'grid_filename'])
        writer.writeheader()
        for p in outliers_below_minus5:
            writer.writerow({
                'personId': p['personId'],
                'name': p['name'],
                'x': p['x'],
                'y': p['y'],
                'z': p['z'],
                'grid_filename': p.get('grid_filename', 'grid_1.png')
            })
    print(f"  Saved: {csv_path_below}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total persons: {len(persons)}")
    print(f"Outliers (X > 5): {len(outliers_above_5)}")
    print(f"Outliers (X < -5): {len(outliers_below_minus5)}")
    print(f"Total outliers: {len(outliers_above_5) + len(outliers_below_minus5)}")
    print(f"In-range: {len(inliers)}")

    print("\nDone!")


if __name__ == "__main__":
    main()
