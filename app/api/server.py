import os
print("🔥 SERVER LOADED — WORKING DIR:", os.getcwd())

from fastapi import FastAPI, Query
from app.agent.planner import ask_agent

app = FastAPI(title="BI Agent", version="1.0")

@app.get("/ask")
def ask(question: str = Query(..., description="Type your BI question here")):
    return ask_agent(question)

@app.get("/health")
def health():
    return {"status": "ok"}


