# app/tools/retrieval_planner.py
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

# 1️⃣ Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini-2024-07-18")

# 2️⃣ Initialize components
embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY automatically
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

# 3️⃣ Define planner prompt
PLANNER_PROMPT = ChatPromptTemplate.from_template("""
You are a BI analyst assistant. You have:
- A vector database containing KPI definitions and glossary entries.
- A SQL database accessible via a read-only query tool.

Analyze the following user question:
---
{question}
---

Decide what information sources to use and why.
If SQL is needed, include a safe SELECT statement.
Return a short JSON-like plan, e.g.:

  "intent": "analyze AOV change",
  "action": "query_sql",
  "sql": "SELECT AVG(order_value) AS aov, DATE_TRUNC('month', order_date) AS month FROM orders GROUP BY month;",
  "reasoning": "AOV comes from transactional data."
""")

# 4️⃣ Modern pipeline syntax (RunnableSequence)
planner_chain = PLANNER_PROMPT | llm

def plan_query(question: str):
    """Generate a reasoning plan for how to handle the user question."""
    response = planner_chain.invoke({"question": question})
    return response.content

def retrieve_docs(question: str):
    """Retrieve top-relevant documents from ChromaDB."""
    results = retriever.invoke(question)  # ✅ pass string, not dict
    return [doc.page_content for doc in results]

# 5️⃣ Main execution
if __name__ == "__main__":
    q = "What is the definition of Average Order Value?"
    print("🔹 Plan:")
    print(plan_query(q))

    print("\n🔹 Retrieved context:")
    for d in retrieve_docs(q):
        print("-", d[:200], "...")