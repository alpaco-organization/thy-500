#!/usr/bin/env python3
"""
Fix outliers by mapping them to the closest valid person in the cabin.
Reads outliers from outliers_x_above_5.csv and finds the closest person
from persons_mapped.json that is not an outlier.
"""

import csv
import json
from pathlib import Path
import math

SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "datas" / "mapped_data" / "outliers_x_above_5.csv"
JSON_PATH = SCRIPT_DIR / "datas" / "mapped_data" / "persons_mapped.json"
OUTPUT_PATH = SCRIPT_DIR / "datas" / "mapped_data" / "outliers_fixed.json"


def load_outliers() -> list[dict]:
    """Load outlier persons from CSV."""
    outliers = []
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
    return outliers


def load_persons() -> list[dict]:
    """Load all persons from JSON."""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def distance_3d(p1: dict, p2: dict) -> float:
    """Calculate 3D distance between two points."""
    return math.sqrt(
        (p1['x'] - p2['x']) ** 2 +
        (p1['y'] - p2['y']) ** 2 +
        (p1['z'] - p2['z']) ** 2
    )


def find_closest_valid_person(outlier: dict, valid_persons: list[dict]) -> dict:
    """Find the closest valid person to the outlier."""
    closest = None
    min_dist = float('inf')

    for person in valid_persons:
        dist = distance_3d(outlier, person)
        if dist < min_dist:
            min_dist = dist
            closest = person

    return {
        'closest_person': closest,
        'distance': min_dist
    }


def main():
    print("=" * 60)
    print("FIX OUTLIERS - Map to closest valid person")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    outliers = load_outliers()
    all_persons = load_persons()

    print(f"  Outliers: {len(outliers)}")
    print(f"  All persons: {len(all_persons)}")

    # Get outlier IDs
    outlier_ids = {o['personId'] for o in outliers}

    # Filter valid persons (not outliers, x between -4 and 4)
    valid_persons = [
        p for p in all_persons
        if p['personId'] not in outlier_ids and -4 <= p['x'] <= 4
    ]
    print(f"  Valid persons (not outliers, -4 <= x <= 4): {len(valid_persons)}")

    # Find closest valid person for each outlier
    print("\nMapping outliers to closest valid persons...")
    results = []

    for i, outlier in enumerate(outliers):
        match = find_closest_valid_person(outlier, valid_persons)
        closest = match['closest_person']

        result = {
            'personId': outlier['personId'],
            'name': outlier['name'],
            'original_x': outlier['x'],
            'original_y': outlier['y'],
            'original_z': outlier['z'],
            'new_x': closest['x'],
            'new_y': closest['y'],
            'new_z': closest['z'],
            'closest_personId': closest['personId'],
            'closest_name': closest['name'],
            'distance': match['distance']
        }
        results.append(result)

        if i < 10:
            print(f"  {outlier['name'][:25]:<25} -> {closest['name'][:25]:<25} (dist: {match['distance']:.2f})")

    if len(outliers) > 10:
        print(f"  ... and {len(outliers) - 10} more")

    # Save results
    print(f"\nSaving results to: {OUTPUT_PATH}")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Also save as CSV for easy viewing
    csv_output = OUTPUT_PATH.with_suffix('.csv')
    print(f"Saving CSV to: {csv_output}")
    with open(csv_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'personId', 'name',
            'original_x', 'original_y', 'original_z',
            'new_x', 'new_y', 'new_z',
            'closest_personId', 'closest_name', 'distance'
        ])
        writer.writeheader()
        writer.writerows(results)

    # Stats
    distances = [r['distance'] for r in results]
    print(f"\nStats:")
    print(f"  Min distance: {min(distances):.3f}")
    print(f"  Max distance: {max(distances):.3f}")
    print(f"  Avg distance: {sum(distances)/len(distances):.3f}")

    # Apply fixes to persons_mapped.json
    print("\n" + "=" * 60)
    print("APPLYING FIXES TO persons_mapped.json")
    print("=" * 60)

    # Create lookup for fixes
    fixes_lookup = {r['personId']: r for r in results}

    # Update positions in all_persons
    fixed_count = 0
    for person in all_persons:
        if person['personId'] in fixes_lookup:
            fix = fixes_lookup[person['personId']]
            person['x'] = fix['new_x']
            person['y'] = fix['new_y']
            person['z'] = fix['new_z']
            fixed_count += 1

    print(f"Fixed {fixed_count} outlier positions")

    # Save updated persons_mapped.json
    print(f"Saving updated persons to: {JSON_PATH}")
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_persons, f, indent=4, ensure_ascii=False)

    print("\nDone!")


if __name__ == "__main__":
    main()
