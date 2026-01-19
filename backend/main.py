import nest_asyncio
nest_asyncio.apply()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.engine import rag_service


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allow Frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextPayload(BaseModel):
    text: str

class ChatPayload(BaseModel):
    query: str

@app.post("/api/upload")
async def upload_context(payload: TextPayload):
    try:
        status = rag_service.ingest_text(payload.text)
        return {"status": "success", "message": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_endpoint(payload: ChatPayload):
    answer = rag_service.chat(payload.query)
    return {"answer": answer}