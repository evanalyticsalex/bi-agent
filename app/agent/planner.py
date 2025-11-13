import re
from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_NAME
from app.tools.sql_tools import safe_sql_executor
from app.tools.retriever import retrieve_docs

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_sql(text: str):
    """Extract SELECT ... ; query from model output."""
    match = re.search(r"SELECT[\s\S]+?;", text, re.IGNORECASE)
    return match.group(0) if match else None

def ask_agent(question: str):
    """Main BI Agent logic: retrieve docs, get SQL, execute, return result."""
    context = "\n\n".join(retrieve_docs(question))

    messages = [
        {"role": "system", "content": "You are a BI analyst generating safe SQL."},
        {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
    ]

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    answer = completion.choices[0].message.content
    sql = extract_sql(answer)

    if not sql:
        return {"error": "No SQL found in response."}

    result = safe_sql_executor(sql)
    return {"sql": sql, "result": result}
