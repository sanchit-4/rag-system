# # # from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from pydantic import BaseModel
# # # from engine import rag_service
# # # import shutil
# # # import os
# # # import json
# # # import requests

# # # app = FastAPI(title="Restaurant RAG API")

# # # # Professional CORS setup
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["http://localhost:3000"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # class QueryRequest(BaseModel):
# # #     query: str

# # # class QueryResponse(BaseModel):
# # #     answer: str
# # #     source: str

# # # @app.post("/ingest")
# # # async def ingest_documents(files: list[UploadFile]):
# # #     # Save files temporarily
# # #     os.makedirs("../data", exist_ok=True)
# # #     for file in files:
# # #         with open(f"../data/{file.filename}", "wb") as buffer:
# # #             shutil.copyfileobj(file.file, buffer)
    
# # #     # Trigger ingestion
# # #     rag_service.ingest_data("../data")
# # #     return {"status": "success", "message": "Knowledge base updated"}

# # # @app.post("/chat", response_model=QueryResponse)
# # # async def chat(request: QueryRequest):
# # #     chat_engine = rag_service.get_chat_engine()
# # #     response = chat_engine.chat(request.query)
    
# # #     # Extract sources for transparency
# # #     sources = [node.node.get_text()[:50] + "..." for node in response.source_nodes]
    
# # #     return {
# # #         "answer": response.response,
# # #         "source": str(sources)
# # #     }

# # # # --- WEBSOCKET FOR VOICE ---
# # # @app.websocket("/ws/voice")
# # # async def voice_endpoint(websocket: WebSocket):
# # #     await websocket.accept()
# # #     chat_engine = rag_service.get_chat_engine()
    
# # #     try:
# # #         while True:
# # #             # 1. Receive Audio Transcript (Simulated logic: Frontend sends text from Speech-to-Text)
# # #             # In a full audio implementation, you'd send bytes here and use OpenAI Whisper
# # #             data = await websocket.receive_text()
# # #             request_json = json.loads(data)
# # #             user_text = request_json.get("text")

# # #             if not user_text:
# # #                 continue

# # #             # 2. Get LLM Response
# # #             response = chat_engine.chat(user_text)
            
# # #             # 3. Send back text (Frontend handles Text-to-Speech)
# # #             await websocket.send_json({
# # #                 "type": "response",
# # #                 "text": response.response
# # #             })
# # #     except WebSocketDisconnect:
# # #         print("Client disconnected")

# # # @app.post("/trigger-call")
# # # async def trigger_call(phone_number: str):
# # #     # This instructs Bland AI to call the user and act as the restaurant agent
# # #     headers = {"authorization": "YOUR_BLAND_API_KEY"}
# # #     data = {
# # #         "phone_number": phone_number,
# # #         "task": "You are a restaurant assistant. Help the user with menu items using the knowledge base.",
# # #         # Bland allows you to inject knowledge snippets here or use their tools
# # #         "voice_id": 1,
# # #         "reduce_latency": True
# # #     }
# # #     response = requests.post("https://api.bland.ai/v1/calls", json=data, headers=headers)
# # #     return response.json()


# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # from app.my_engine import rag_service
# # import logging
# # import json
# # import nest_asyncio  # <--- NEW IMPORT

# # # <--- APPLY THE PATCH
# # # This allows the sync 'chat_engine.chat()' to run inside FastAPI's async loop
# # nest_asyncio.apply()
# # # Setup Logger
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger("uvicorn")

# # app = FastAPI(title="Professional Gemini RAG")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:3000"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # class ChatRequest(BaseModel):
# #     query: str

# # class ChatResponse(BaseModel):
# #     answer: str
# #     sources: list[str]

# # @app.get("/health")
# # def health_check():
# #     return {"status": "ok", "db_connected": rag_service.index is not None}

# # @app.post("/api/chat", response_model=ChatResponse)
# # async def chat_endpoint(request: ChatRequest):
# #     try:
# #         chat_engine = rag_service.get_chat_engine()
# #         response = chat_engine.chat(request.query)
        
# #         # Extract source text for UI citation
# #         sources = []
# #         for node in response.source_nodes:
# #             # Clean up newlines for display
# #             text_snippet = node.node.get_text()[:100].replace("\n", " ")
# #             sources.append(text_snippet + "...")

# #         return {
# #             "answer": response.response,
# #             "sources": sources
# #         }
# #     except Exception as e:
# #         logger.error(f"Chat Error: {str(e)}")
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.websocket("/ws/voice")
# # async def voice_websocket(websocket: WebSocket):
# #     await websocket.accept()
# #     try:
# #         chat_engine = rag_service.get_chat_engine()
# #         while True:
# #             data = await websocket.receive_text()
# #             payload = json.loads(data)
# #             user_text = payload.get("text")
            
# #             if user_text:
# #                 logger.info(f"Voice Query: {user_text}")
# #                 response = chat_engine.chat(user_text)
                
# #                 await websocket.send_json({
# #                     "type": "response",
# #                     "text": response.response
# #                 })
# #     except WebSocketDisconnect:
# #         logger.info("Voice client disconnected")
# #     except Exception as e:
# #         logger.error(f"WebSocket Error: {e}")
# #         await websocket.close()



# from fastapi import FastAPI
# from pydantic import BaseModel
# # Import the SDK we just made
# from rag_sdk import AutoRAG 
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# # 1. Initialize the Bot with THEIR credentials
# bot = AutoRAG(
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     index_name="MyRestaurant"
# )

# # Optional: Run ingestion on startup if needed
# # bot.ingest("./data") 

# class Query(BaseModel):
#     text: str

# @app.post("/api/chat")
# def chat_endpoint(q: Query):
#     # 2. Use the bot
#     response = bot.chat(
#         query=q.text, 
#         system_prompt="You are a waiter at a Pizza place. Be funny."
#     )
#     return {"answer": response}

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