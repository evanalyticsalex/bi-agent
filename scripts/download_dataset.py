import kagglehub
import shutil
from pathlib import Path

# Download latest version
print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("pavansubhasht/ibm-hr-analytics-attrition-dataset")

print(f"Downloaded to: {path}")

# Create data/seed directory if it doesn't exist
seed_dir = Path("data/seed")
seed_dir.mkdir(parents=True, exist_ok=True)

# Find and copy the CSV file
downloaded_path = Path(path)
csv_files = list(downloaded_path.glob("*.csv"))

if csv_files:
    source_file = csv_files[0]
    dest_file = seed_dir / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    shutil.copy(source_file, dest_file)
    print(f"✅ Copied to: {dest_file}")
else:
    print("❌ No CSV files found in downloaded dataset")
