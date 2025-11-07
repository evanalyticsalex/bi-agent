# app/db.py
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

def run_query(sql: str):
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]