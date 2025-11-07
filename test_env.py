from dotenv import load_dotenv
import os
import sqlalchemy as sa

# Load environment variables from .env
load_dotenv()
print("ENV loaded from:", os.getcwd())
print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

# Check OpenAI key
print("🔑 OpenAI key starts with:", os.getenv("OPENAI_API_KEY")[:10], "...")

# Check database connection
db_url = os.getenv("DB_URL")
engine = sa.create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute(sa.text("SELECT version();"))
        print("🗄️ Database connection OK!")
        print("PostgreSQL version:", result.scalar())
except Exception as e:
    print("❌ Database connection failed:", e)
