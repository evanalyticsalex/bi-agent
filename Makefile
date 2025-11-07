# === Makefile for Phase 5 automation ===

# Step 0: Load CSVs into Postgres
load:
	python scripts/load_csvs.py --file $(file)

# Step 4–5: Generate KPI views, apply to Postgres, and embed docs
activate:
	python scripts/generate_views_from_yaml.py --dataset $(dataset)
	psql "$$DB_URL" -f build/$(dataset)/views.sql
	python scripts/embed_docs.py --dataset $(dataset) \
	  --docs data/datasets/$(dataset)/glossary.md data/datasets/$(dataset)/kpis.yaml \
	  --tag dataset=$(dataset) --tag version=$$(date +%F)

# Step 7 only: Re-embed docs (no views)
embed:
	python scripts/embed_docs.py --dataset $(dataset) \
	  --docs data/datasets/$(dataset)/glossary.md data/datasets/$(dataset)/kpis.yaml \
	  --tag dataset=$(dataset) --tag version=$$(date +%F)