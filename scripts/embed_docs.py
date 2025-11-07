# scripts/embed_docs.py
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma")
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
os.makedirs(CHROMA_DIR, exist_ok=True)

# === Datasets and their documents ===
DATASETS = {
    "sales": ["data/docs/kpis.md", "data/docs/glossary.md"],
    "HR_analytics": ["data/docs/hr_policies.md", "data/docs/hr_kpis.md"],
}

emb = HuggingFaceEmbeddings(model_name=MODEL_NAME)
vec = Chroma(
    collection_name="docs",
    embedding_function=emb,
    persist_directory=CHROMA_DIR,
)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
total_chunks = 0

for dataset, paths in DATASETS.items():
    texts = []
    for p in paths:
        if os.path.exists(p):
            texts.extend(TextLoader(p, encoding="utf-8").load())
        else:
            print(f"⚠️  Missing file for dataset {dataset}: {p}")

    if not texts:
        print(f"❌ No docs for dataset {dataset}. Skipping.")
        continue

    docs = splitter.split_documents(texts)
    for d in docs:
        d.metadata["dataset"] = dataset
        d.metadata["source"] = d.metadata.get("source", os.path.basename(p))

    vec.add_documents(docs)
    total_chunks += len(docs)
    print(f"✅ Embedded {len(docs)} chunks for dataset '{dataset}'")

count = vec._collection.count()
print(f"📦 Total embedded chunks: {total_chunks}. Collection count: {count}. Dir: {CHROMA_DIR}")