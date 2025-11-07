# app/tools/retriever.py
import os
from dotenv import load_dotenv
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ Load environment
load_dotenv(dotenv_path="/Users/alexalxndrpgmail.com/Projects/bi-agent/.env")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma")
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# ✅ Connect to persistent Chroma collection
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("docs")

# ✅ Local embedding model (no OpenAI quota)
emb = HuggingFaceEmbeddings(model_name=MODEL_NAME)

def retrieve(question: str, k: int = 4, dataset: str = "sales"):
    """
    Retrieve top-k chunks from the 'docs' collection filtered by dataset.
    Works for any dataset embedded with metadata {'dataset': <name>}.
    """
    # Embed query using local model
    q = emb.embed_query(question)

    # Query Chroma with dataset filter
    results = collection.query(
        query_embeddings=[q],
        n_results=k,
        where={"dataset": dataset},
        include=["documents", "metadatas"]
    )

    # Format output
    return [
        {"source": m.get("source"), "text": d}
        for d, m in zip(results["documents"][0], results["metadatas"][0])
    ]

# Optional diagnostic
print("📚 Available collections:")
for c in client.list_collections():
    print("  -", c.name, f"({c.count()} chunks)")