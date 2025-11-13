import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database URL
DB_URL = os.getenv("DB_URL")

# Chroma vectorstore directory
CHROMA_DIR = os.getenv("CHROMA_DIR")

# LLM model name (default fallback kept for safety)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini-2024-07-18")
