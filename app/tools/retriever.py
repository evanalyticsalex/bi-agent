from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import CHROMA_DIR, MODEL_NAME

# Load embeddings
emb = HuggingFaceEmbeddings(model_name=MODEL_NAME)

# Connect to your Chroma database
db = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=emb
)

def retrieve_docs(question: str, top_k: int = 3):
    """
    Retrieve the most relevant documents for the question.
    Returns list of page_content strings.
    """
    docs = db.similarity_search(question, k=top_k)
    return [d.page_content for d in docs]
