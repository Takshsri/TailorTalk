from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from drive_tool import search_drive

load_dotenv()

llm = ChatGroq(
    model_name=os.getenv("MODEL_NAME"),
    temperature=0
)


def generate_drive_query(user_input):

    prompt = f"""
You are an AI assistant that converts natural language
requests into valid Google Drive API q parameters.

Rules:

- PDF files:
  mimeType='application/pdf'

- Images:
  mimeType contains 'image/'

- Search by exact file name:
  name='filename'

- Search by partial name:
  name contains 'keyword'

- Search document text:
  fullText contains 'keyword'

- Search by modified date:
  modifiedTime > '2026-05-01T00:00:00'

- Combine conditions using and/or when needed.

Examples:

User: Find PDF reports
Query:
mimeType='application/pdf' and name contains 'report'

User: Find files containing budget
Query:
fullText contains 'budget'

User: Find invoices from April
Query:
name contains 'invoice'

Only return the Google Drive q query.
Do not explain anything.

User Request:
{user_input}
"""

    response = llm.invoke(prompt)

    return response.content.strip()


def chat_with_drive_agent(user_input):

    drive_query = generate_drive_query(user_input)

    result = search_drive(drive_query)

    return {
        "query": drive_query,
        "result": result
    }