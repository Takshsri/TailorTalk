from fastapi import FastAPI
from pydantic import BaseModel
from agent import chat_with_drive_agent

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "TailorTalk AI Backend Running"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = chat_with_drive_agent(request.message)

    return response