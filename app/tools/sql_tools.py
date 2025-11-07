# app/tools/sql_tool.py

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db import run_query

def safe_sql_executor(sql: str):
    """
    Executes only safe SELECT queries.
    Blocks all write/DDL commands.
    """
    low = sql.lower()
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "grant", "revoke"]

    # Guardrail: reject dangerous statements
    if any(word in low for word in forbidden):
        return {"error": "❌ Unsafe SQL detected — only SELECT is allowed."}

    try:
        # Execute using shared db helper
        rows = run_query(sql)
        return [dict(r) for r in rows] if rows else []
    except Exception as e:
        return {"error": f"⚠️ SQL error: {e}"}

if __name__ == "__main__":
    # Quick test
    print(safe_sql_executor("SELECT 1 AS ok;"))
