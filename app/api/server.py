from fastapi import FastAPI
from app.tools.sql_tools import safe_sql_executor
import traceback

app = FastAPI()

@app.post("/sql")
def sql(payload: dict):
    sql = payload.get("sql", "")
    try:
        result = safe_sql_executor(sql)
        print("DEBUG result:", result)
        return result
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        return {"error": str(e)}
