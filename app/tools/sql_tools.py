# app/tools/sql_tool.py

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db import run_query

def safe_sql_executor(sql: str):
    low = sql.lower()
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "grant", "revoke"]
    if any(w in low for w in forbidden):
        return {"error": "Unsafe SQL detected"}
    try:
        print(f"[SQL LOG] Executing query: {sql}")  # ✅ minimal query logging
        rows = run_query(sql)
        return [dict(r) for r in rows]
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Quick test
    print(safe_sql_executor("SELECT 1 AS ok;"))
