import os, sys, yaml
from jinja2 import Template

print("🚀 Starting generate_views_from_yaml.py")

def parse_arg(flag, default):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default

# --- Parse dataset name ---
DATASET = parse_arg("--dataset", "sales")
YAML_PATH = f"data/datasets/{DATASET}/kpis.yaml"
BUILD_DIR = f"build/{DATASET}"

print(f"📂 Current working dir: {os.getcwd()}")
print(f"📁 YAML_PATH = {YAML_PATH}")
print(f"📁 BUILD_DIR = {BUILD_DIR}")

os.makedirs(BUILD_DIR, exist_ok=True)

# --- Check YAML existence and preview content ---
if os.path.exists(YAML_PATH):
    print("✅ YAML file found.")
    with open(YAML_PATH) as dbg:
        preview = dbg.read()
        print("📄 YAML content preview (first 300 chars):")
        print(preview[:300])
else:
    print("❌ YAML file not found! Check your dataset folder path.")
    sys.exit(1)

# --- SQL view template ---
tpl = Template("""
{% for k in kpis %}
CREATE OR REPLACE VIEW kpi_{{k.name}}_{{k.grain}} AS
SELECT
    DATE_TRUNC('{{k.grain}}', order_date) AS {{k.grain}},
    {{k.sql}} AS value
FROM orders
{% if k.filters %}WHERE {{' AND '.join(k.filters)}}{% endif %}
GROUP BY 1;
{% endfor %}
""")

# --- Load YAML ---
with open(YAML_PATH, "r") as f:
    cfg = yaml.safe_load(f)

print(f"🧠 Parsed YAML keys: {list(cfg.keys()) if cfg else 'EMPTY'}")

sql = tpl.render(kpis=cfg.get("kpis", []))
print(f"🧩 Rendered SQL length: {len(sql)} characters")

# --- Write output ---
out_path = f"{BUILD_DIR}/views.sql"
print(f"💾 Writing SQL to {out_path}")
with open(out_path, "w") as f:
    f.write(sql)

print(f"✅ Generated KPI views -> {out_path}")
