#!/usr/bin/env python3
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

def parse_arg(flag, default=None):
    """Parse command line arguments"""
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default

# Get database URL from environment
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    print("❌ DB_URL environment variable not set")
    print("Set it with: export DB_URL='postgresql://username:password@localhost:5432/bi_agent'")
    sys.exit(1)

# Parse arguments
csv_file = parse_arg("--file")
kaggle_url = parse_arg("--kaggle")

if not csv_file and not kaggle_url:
    print("Usage: python scripts/load_csvs.py --file <path> OR --kaggle <url>")
    sys.exit(1)

# Create database engine
engine = create_engine(DB_URL)

# Read CSV
if csv_file:
    df = pd.read_csv(csv_file)
    table_name = Path(csv_file).stem.lower().replace("-", "_").replace(" ", "_")
else:
    # Kaggle dataset handling would go here
    print("❌ Kaggle loading not yet implemented")
    sys.exit(1)

# Load to Postgres
print(f"Loading {len(df)} rows into table '{table_name}'...")
df.to_sql(table_name, engine, if_exists="replace", index=False)
print(f"✅ Loaded {table_name} successfully")

# Create schema directory
os.makedirs("db", exist_ok=True)
os.makedirs("data/docs", exist_ok=True)

# Generate schema file
schema_lines = [f"# Schema: {table_name}\n\n"]
for col in df.columns:
    dtype = df[col].dtype
    schema_lines.append(f"- {col}: {dtype}\n")

schema_path = f"db/{table_name}_schema.txt"
with open(schema_path, "w") as f:
    f.writelines(schema_lines)
print(f"✅ Generated schema: {schema_path}")

# Generate basic glossary
glossary_lines = [f"# Glossary: {table_name}\n\n"]
for col in df.columns:
    glossary_lines.append(f"- **{col}**: [Auto-generated column]\n")

glossary_path = f"data/docs/{table_name}_glossary.md"
with open(glossary_path, "w") as f:
    f.writelines(glossary_lines)
print(f"✅ Generated glossary: {glossary_path}")

print(f"\n✅ Done! Next steps:")
print(f"1. Create dataset scaffold: mkdir -p data/datasets/{table_name}")
print(f"2. Define KPIs in data/datasets/{table_name}/kpis.yaml")
print(f"3. Update data/datasets/{table_name}/glossary.md")
