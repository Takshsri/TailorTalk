from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import chat_with_drive_agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

# Initialize FastAPI app
app = FastAPI(
    title="TailorTalk AI Backend",
    description="Conversational Google Drive File Discovery API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str


# Root route
@app.get("/")
def home():
    return {
        "message": "TailorTalk AI Backend Running 🚀"
    }


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    response = chat_with_drive_agent(request.message)

    return {
        "success": True,
        "query": response["query"],
        "result": response["result"]
    }