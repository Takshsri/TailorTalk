from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from drive_tool import search_drive

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)


def generate_drive_query(user_input):

    prompt = f"""
    Convert the user request into a Google Drive API q parameter.

    Examples:

    User: Find PDF files
    Query: mimeType='application/pdf'

    User: Find image files
    Query: mimeType contains 'image/'

    User: Find invoices
    Query: name contains 'invoice'

    User: Find QR code images
    Query: name contains 'qr'

    Only return the query.
    
    User: {user_input}
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