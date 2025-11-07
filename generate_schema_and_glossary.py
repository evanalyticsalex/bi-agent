import pandas as pd
from sqlalchemy import create_engine, inspect
import os, argparse, zipfile, glob, shutil, subprocess

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Auto generate schema & glossary from Kaggle or local CSV.")
parser.add_argument("--kaggle", type=str, help="Kaggle dataset URL (optional)")
parser.add_argument("--file", type=str, help="Path to local CSV (optional)")
args = parser.parse_args()

# --- Postgres connection ---
DB_URL = os.getenv("DB_URL", "postgresql://localhost/bi_agent")
engine = create_engine(DB_URL)

# --- Working folders ---
os.makedirs("data/seed", exist_ok=True)
os.makedirs("data/docs", exist_ok=True)
os.makedirs("db", exist_ok=True)

def download_from_kaggle(url):
    """Download dataset from Kaggle using its slug."""
    print("📦 Downloading dataset from Kaggle...")
    slug = url.split("datasets/")[-1]
    subprocess.run(["kaggle", "datasets", "download", "-d", slug, "-p", "data/seed", "--unzip"], check=True)
    print("✅ Download complete.")

# --- Step 1: download dataset if Kaggle URL provided ---
if args.kaggle:
    download_from_kaggle(args.kaggle)
    csv_files = glob.glob("data/seed/*.csv")
elif args.file:
    csv_files = [args.file]
else:
    csv_files = glob.glob("data/seed/*.csv")

if not csv_files:
    raise FileNotFoundError("No CSV files found in data/seed. Please provide a Kaggle link or a local file path.")

# --- Step 2: process each CSV ---
for csv_path in csv_files:
    table_name = os.path.splitext(os.path.basename(csv_path))[0].lower()
    print(f"\n🧩 Processing {table_name}...")

    # Load CSV to DataFrame
    df = pd.read_csv(csv_path)

    # Upload to Postgres
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    # Inspect columns
    insp = inspect(engine)
    columns = insp.get_columns(table_name)

    # Generate schema.sql
    schema_lines = [f"  {col['name']} {col['type']}" for col in columns]
    schema_sql = f"CREATE TABLE {table_name} (\n" + ",\n".join(schema_lines) + "\n);"
    with open(f"db/{table_name}_schema.sql", "w") as f:
        f.write(schema_sql)

    # Generate glossary.md
    glossary = [f"# Glossary for table: {table_name}\n\n"]
    for col in columns:
        glossary.append(f"- **{col['name']}**: column of type `{col['type']}` (auto-generated)\n")
    with open(f"data/docs/{table_name}_glossary.md", "w") as f:
        f.writelines(glossary)

    print(f"✅ Created schema + glossary for: {table_name}")

print("\n🎉 All datasets processed successfully.")
