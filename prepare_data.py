import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

print("=" * 70)
print("Data set preparation")

SOURCE_DIR="IDC_regular_ps50_idx5"
OUTPUT_DIR="data/split_data"