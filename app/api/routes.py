# app/api/routes.py
from fastapi import APIRouter, Request
from app.tools.retriever import get_answer  # you’ll create or already have this

router = APIRouter()

@router.post("/ask")
async def ask(request: Request):
    payload = await request.json()
    q = payload.get("q", "")
    dataset = payload.get("dataset", "sales")
    print(f"Received question: {q} | Dataset: {dataset}")  # helps debugging

    # Call your retriever logic
    try:
        answer = get_answer(q, dataset)
        return {"answer": answer}
    except Exception as e:
        print("Error in retriever:", e)
        return {"error": str(e)}