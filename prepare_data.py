import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

print("=" * 70)
print("Data set preparation")

SOURCE_DIR="IDC_regular_ps50_idx5"
OUTPUT_DIR="data/split_data"

print(f"\n[1/4] Checking source directory: {SOURCE_DIR}")

if not os.path.isdir(SOURCE_DIR):#verifying if source directory exists
    print(f"\n❌ ERROR: Directory '{SOURCE_DIR}' not found!")
    print(f"Current directory: {os.getcwd()}")
    print(f"Please navigate to the correct folder.")
    for item in os.listdir(".")[:20]:
        print(f" - {item}")
    exit(1)

print(f"\n[2/4] Scanning PNG Files and classifying")
#finding all png files and classify them
benign_files=[]
malignant_files=[]


png_files=list(Path(SOURCE_DIR).glob("**/*.png"))
print(f" Found {len(benign_files)} benign PNG files")

#parse filename to determine class
for file_path in png_files:
    filename=file_path.name

    if "_class0.png" in filename:
        benign_files.append(file_path)
    elif "_class1.png" in filename:
        malignant_files.append(file_path)
    else:
        if "_0.png" in filename:
            benign_files.append(file_path)
        elif "_1.png" in filename:
            malignant_files.append(file_path)
print(f"Found {len(benign_files)} benign PNG files")
print(f"Found {len(malignant_files)} malignant PNG files")

print(f"\n Classification Complete: ")
print(f"- Benign: {len(benign_files)}")
print(f"- Malignant: {len(malignant_files)}")

if len(benign_files) == 0 or len(malignant_files) == 0:
    print(f"\n❌ ERROR: Could not classify files into benign and malignant.")
    print(f"Please check the filename patterns in the source directory.")
    for f in list(Path(SOURCE_DIR).glob("**/*.png"))[:20]:
        print(f" - {f.name}")

    sample = list(Path(SOURCE_DIR).glob("*.png"))[0]
    print(f"\nExpected pattern: PATIENT_idx5_xCOORD_yCOORD_classLABEL.png")
    print(f"Actual sample:   {sample.name}")
 
# Step 3: Create output directory structure
print(f"\n[3/4] Creating output directories...")
 
os.makedirs(f"{OUTPUT_DIR}/train/benign", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/train/malignant", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/val/benign", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/val/malignant", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/test/benign", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/test/malignant", exist_ok=True)
 
print(f"✓ Created directory structure in {OUTPUT_DIR}/")

print(f"\n[4/4] splitting data into 70% train /15% val /15% test")

def split_and_copy(file_list,class_name):
    if len(file_list) == 0:
        print(f"\n❌ ERROR: No files found for class '{class_name}'. Skipping split and copy.")
        return
    train,temp=train_test_split(file_list,test_size=0.3,random_state=42)
    val,test=train_test_split(temp,test_size=0.5,random_state=42)

    for src_file in train:
        dst_file=f'{OUTPUT_DIR}/train/{class_name}/{src_file.name}'
        shutil.copy2(src_file,dst_file)
        print(f" Train {len(train):5,} files copied to {OUTPUT_DIR}/train/{class_name}/")
    for src_file in val:
        dst_file=f'{OUTPUT_DIR}/val/{class_name}/{src_file.name}'
        shutil.copy2(src_file,dst_file)
        print(f" Validation {len(val):5,} files copied to {OUTPUT_DIR}/val/{class_name}/")
    for src_file in test:
        dst_file=f'{OUTPUT_DIR}/test/{class_name}/{src_file.name}'
        shutil.copy2(src_file,dst_file)
        print(f" Test {len(test):5,} files copied to {OUTPUT_DIR}/test/{class_name}/")
    return len(train),len(val),len(test)
print("\n Copyingbenignimages..")
benign_counts=split_and_copy(benign_files,"benign")
print(f"\n Benign images split and copied. Counts: Train={benign_counts[0]}, Val={benign_counts[1]}, Test={benign_counts[2]}")
print("\n Copying malignant images..")
malignant_counts=split_and_copy(malignant_files,"malignant")
print(f"\n Malignant images split and copied. Counts: Train={malignant_counts[0]}, Val={malignant_counts[1]}, Test={malignant_counts[2]}")

for split in ['train', 'val', 'test']:
    benign_path = Path(f"{OUTPUT_DIR}/{split}/benign")
    malignant_path = Path(f"{OUTPUT_DIR}/{split}/malignant")
    
    benign_count = len(list(benign_path.glob("*.png")))
    malignant_count = len(list(malignant_path.glob("*.png")))
    total = benign_count + malignant_count
    
    if total > 0:
        benign_pct = benign_count / total * 100
        malignant_pct = malignant_count / total * 100
        print(f"\n{split.upper()}: {total:,} images total")
        print(f"  Benign:     {benign_count:6,} ({benign_pct:5.1f}%)")
        print(f"  Malignant:  {malignant_count:6,} ({malignant_pct:5.1f}%)")
 
print("\n" + "=" * 70)
print("✅ DATA PREPARATION COMPLETE!")
print("=" * 70)
print(f"\nDataset ready at: {OUTPUT_DIR}/")
print("\nNext step: Run 'python train_cancer_cnn.py'")