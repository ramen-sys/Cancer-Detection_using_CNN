"""
Quick File Inspection - Check your actual dataset structure
Run this FIRST to understand your file naming
"""

import os
from pathlib import Path
from collections import defaultdict

print("=" * 70)
print("DATASET FILE INSPECTION")
print("=" * 70)

source_dir = "IDC_regular_ps50_idx5"

if not os.path.isdir(source_dir):
    print(f"\n❌ ERROR: Directory '{source_dir}' not found!")
    print(f"Current directory: {os.getcwd()}")
    print(f"Please navigate to the correct folder.")
    exit(1)

print(f"\n✓ Found directory: {source_dir}")

# Get all PNG files
all_files = list(Path(source_dir).glob("**/*.png"))
print(f"✓ Total PNG files: {len(all_files):,}")

# Show file structure
print(f"\n[DIRECTORY STRUCTURE]")
subdirs = set()
for root, dirs, files in os.walk(source_dir):
    level = root.replace(source_dir, "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files[:3]:  # Show first 3 files
        print(f"{subindent}{file}")
    if len(files) > 3:
        print(f"{subindent}... and {len(files) - 3} more files")
    for d in dirs:
        subdirs.add(d)

# Analyze filenames
print(f"\n[FILENAME PATTERNS]")
sample_files = list(all_files)[:10]
print(f"Sample filenames:")
for f in sample_files:
    print(f"  {f.name}")

# Try to classify by filename pattern
print(f"\n[CLASSIFICATION ATTEMPTS]")

# Method 1: Look for class in filename
class0_count = len([f for f in all_files if "_class0" in f.name or f.name.endswith("_0.png")])
class1_count = len([f for f in all_files if "_class1" in f.name or f.name.endswith("_1.png")])

print(f"\nMethod 1 - Filename parsing:")
print(f"  Files with 'class0' or ending '_0.png': {class0_count}")
print(f"  Files with 'class1' or ending '_1.png': {class1_count}")

# Method 2: Look for numeric suffix patterns
numeric_patterns = defaultdict(int)
for f in all_files:
    parts = f.name.replace(".png", "").split("_")
    if len(parts) > 0:
        last_part = parts[-1]
        if last_part.isdigit():
            numeric_patterns[last_part] += 1

if numeric_patterns:
    print(f"\nMethod 2 - Last numeric component in filename:")
    for pattern, count in sorted(numeric_patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  Ends with '_class{pattern}': {count} files")

# Method 3: Check subdirectories
print(f"\nMethod 3 - Subdirectory structure:")
if subdirs:
    for subdir in sorted(subdirs):
        subdir_path = Path(source_dir) / subdir
        files_in_subdir = len(list(subdir_path.glob("*.png"))) if subdir_path.is_dir() else 0
        print(f"  /{subdir}/: {files_in_subdir} PNG files")
else:
    print(f"  No subdirectories found (all files in root)")

print("\n" + "=" * 70)
print("RECOMMENDATION")
print("=" * 70)

if class0_count > 0 or class1_count > 0:
    print(f"\n✓ Can classify by 'class0'/'class1' in filename")
    print(f"  Benign (class 0):    {class0_count:,} images")
    print(f"  Malignant (class 1): {class1_count:,} images")
    print(f"\n  Ready to use: prepare_data_actual.py")
elif numeric_patterns:
    print(f"\n⚠️ Files have numeric suffix but not clearly labeled")
    print(f"  Patterns found: {dict(numeric_patterns)}")
    print(f"\n  You may need to manually inspect and create class folders:")
    print(f"    - IDC_regular_ps50_idx5/0/  (benign images)")
    print(f"    - IDC_regular_ps50_idx5/1/  (malignant images)")
elif subdirs:
    print(f"\n✓ Subdirectories found: {sorted(subdirs)}")
    print(f"  Check if these represent class labels")
    print(f"  If yes, rename accordingly and re-run this script")
else:
    print(f"\n❌ Cannot determine class from filename pattern")
    print(f"  You may need to reorganize files into:")
    print(f"    - IDC_regular_ps50_idx5/0/  (benign images)")
    print(f"    - IDC_regular_ps50_idx5/1/  (malignant images)")

print("\n" + "=" * 70)