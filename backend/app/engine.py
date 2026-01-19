# # # import weaviate
# # # from llama_index.core import VectorStoreIndex, StorageContext, Settings as LlamaSettings
# # # from llama_index.vector_stores.weaviate import WeaviateVectorStore
# # # from llama_index.embeddings.google_genai import GoogleGenAIEmbedding as GeminiEmbedding
# # # from llama_index.llms.google_genai import GoogleGenAI as Gemini
# # # from llama_index.core.node_parser import SentenceSplitter
# # # from app.config import settings
# # # import logging
# # # import weaviate
# # # # Setup Logging
# # # logger = logging.getLogger("uvicorn")

# # # # --- CONFIGURE GEMINI ---
# # # # Gemini Pro is great for reasoning, Flash is faster.
# # # LlamaSettings.llm = Gemini(
# # #     model="models/gemini-2.5-flash", 
# # #     api_key=settings.GOOGLE_API_KEY,
# # #     temperature=0.0  # Zero temp to reduce hallucinations
# # # )

# # # # Gemini Embeddings
# # # LlamaSettings.embedding = GeminiEmbedding(
# # #     model_name="models/embedding-001", 
# # #     api_key=settings.GOOGLE_API_KEY
# # # )

# # # Settings.embed_model = GoogleGenAIEmbedding(
# # #     model_name="models/text-embedding-004", # Switched to newer, better model
# # #     api_key=settings.GOOGLE_API_KEY,
# # #     embed_batch_size=10  # <--- THIS IS THE KEY FIX (Sends 10 chunks at a time instead of 100)
# # # )

# # # Settings.llm = GoogleGenAI(
# # #     model_name="models/gemini-2.5-flash", 
# # #     api_key=settings.GOOGLE_API_KEY
# # # )
# # # class RAGService:
# # #     def __init__(self):
# # #         self.client = weaviate.connect_to_local(
# # #             host="localhost", # You might need to parse URL or change config to host/port
# # #             port=8080,
# # #             grpc_port=50051
# # #         )
# # #         self.index = None
# # #         self._load_index()

# # #     def _load_index(self):
# # #         """Attempts to load the index from Weaviate."""
# # #         try:
# # #             vector_store = WeaviateVectorStore(
# # #                 weaviate_client=self.client, 
# # #                 index_name=settings.INDEX_NAME
# # #             )
# # #             # We assume the index exists. If not, ingestion must be run.
# # #             self.index = VectorStoreIndex.from_vector_store(
# # #                 vector_store=vector_store
# # #             )
# # #             logger.info("✅ Connected to Weaviate Index successfully.")
# # #         except Exception as e:
# # #             logger.error(f"⚠️ Could not load index: {e}. Run ingestion first.")
# # #             self.index = None

# # #     def get_chat_engine(self):
# # #         if not self.index:
# # #             raise ValueError("Index not initialized. Please ingest data first.")

# # #         # STRICT SYSTEM PROMPT
# # #         system_prompt = (
# # #             "You are a specialized support agent for 'Gourmet Bistro'. "
# # #             "Your goal is to answer questions accurately based ONLY on the provided context. "
# # #             "1. If the answer is not in the context, strictly say 'I'm sorry, I don't have that information in my records.' "
# # #             "2. Do not invent menu items, prices, or policies. "
# # #             "3. Be polite and concise."
# # #         )

# # #         return self.index.as_chat_engine(
# # #             chat_mode="context",
# # #             system_prompt=system_prompt,
# # #             similarity_top_k=3, # Retrieve top 3 relevant chunks
# # #         )

# # # rag_service = RAGService()


# # import weaviate
# # from llama_index.core import VectorStoreIndex, StorageContext, Settings
# # from llama_index.vector_stores.weaviate import WeaviateVectorStore
# # # UPDATED IMPORTS FOR NEW GOOGLE SDK
# # from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
# # from llama_index.llms.google_genai import GoogleGenAI
# # from app.config import settings
# # import logging

# # logger = logging.getLogger("uvicorn")

# # # 1. CONFIGURE GEMINI (NEW SYNTAX)
# # gemini_embed_model = GoogleGenAIEmbedding(
# #     model_name="models/embedding-001", 
# #     api_key=settings.GOOGLE_API_KEY
# # )

# # FORCE_NEW_LLM = GoogleGenAI(
# #     model="models/gemini-2.5-flash", 
# #     api_key=settings.GOOGLE_API_KEY,
# #     temperature=0
# # )

# # # Apply Global Settings
# # Settings.llm = FORCE_NEW_LLM
# # Settings.embedding = gemini_embed_model

# # class RAGService:
# #     def __init__(self):
# #         # Weaviate v3 Client (Matches the requirements.txt pin)
# #         self.client = weaviate.Client(settings.WEAVIATE_URL)
# #         self.index = None
# #         self._load_index()

# #     def _load_index(self):
# #         try:
# #             vector_store = WeaviateVectorStore(
# #                 weaviate_client=self.client, 
# #                 index_name=settings.INDEX_NAME
# #             )
            
# #             storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
# #             self.index = VectorStoreIndex.from_vector_store(
# #                 vector_store, 
# #                 storage_context=storage_context,
# #                 embed_model=gemini_embed_model
# #             )
# #             logger.info("✅ Connected to Weaviate Index successfully.")
# #         except Exception as e:
# #             logger.error(f"⚠️ Could not load index: {e}. If this is the first run, ignore this. Run ingestion.")
# #             self.index = None

# #     def get_chat_engine(self):
# #         if not self.index:
# #             raise ValueError("Index not initialized. Run 'python -m app.ingest' first.")

# #         system_prompt = (
# #             "You are a helpful assistant for 'Gourmet Bistro'. "
# #             "Use ONLY the context provided to answer questions. "
# #             "If the answer is not in the context, say 'I do not have that information'."
# #         )

# #         return self.index.as_chat_engine(
# #             chat_mode="context",
# #             system_prompt=system_prompt,
# #             llm=FORCE_NEW_LLM
# #         )

# # rag_service = RAGService()


# import weaviate
# from llama_index.core import VectorStoreIndex, StorageContext, Settings
# from llama_index.vector_stores.weaviate import WeaviateVectorStore
# from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
# from llama_index.llms.google_genai import GoogleGenAI
# from app.config import settings
# import logging

# logger = logging.getLogger("uvicorn")

# # 1. CONFIGURE GEMINI
# # MUST match ingest.py exactly
# gemini_embed_model = GoogleGenAIEmbedding(
#     model_name="models/text-embedding-004", 
#     api_key=settings.GOOGLE_API_KEY
# )
# # print("DEBUG: Initinalizig GoogleGenAI...") # <--- ADD THIS
# FORCE_NEW_LLM = GoogleGenAI(
#     model_name="models/gemini-1.5-flash",  # <--- This is the important part
#     api_key=settings.GOOGLE_API_KEY,
#     temperature=0
# )
# # print(f"DEBUG: Model set to: {FORCE_NEW_LLM.model_name}") # <--- ADD THIS
# # Apply Global Settings
# Settings.llm = FORCE_NEW_LLM
# Settings.embedding = gemini_embed_model

# class RAGService:
#     def __init__(self):
#         # UPDATED: Weaviate v4 Connection
#         self.client = weaviate.connect_to_local(
#             host="localhost",
#             port=8080,
#             grpc_port=50051
#         )
#         self.index = None
#         self._load_index()

#     def _load_index(self):
#         try:
#             # Connect to specific index
#             vector_store = WeaviateVectorStore(
#                 weaviate_client=self.client, 
#                 index_name=settings.INDEX_NAME
#             )
            
#             storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
#             # Load the index
#             self.index = VectorStoreIndex.from_vector_store(
#                 vector_store, 
#                 storage_context=storage_context,
#                 embed_model=gemini_embed_model
#             )
#             logger.info("✅ Connected to Weaviate Index successfully.")
#         except Exception as e:
#             logger.error(f"⚠️ Could not load index: {e}. If this is the first run, ignore this. Run ingestion.")
#             self.index = None

#     def get_chat_engine(self):
#         if not self.index:
#             raise ValueError("Index not initialized.")
#         forced_llm = GoogleGenAI(
#             model="models/gemini-2.5-flash",
#             api_key=settings.GOOGLE_API_KEY,
#             temperature=0
#         )
        
#         system_prompt = (
#             "You are a helpful assistant for 'Gourmet Bistro'. "
#             "Use ONLY the context provided to answer questions. "
#         )

#         return self.index.as_chat_engine(
#             chat_mode="context",
#             system_prompt=system_prompt,
#             llm=forced_llm
#         )
# # Create singleton instance
# rag_service = RAGService()


import weaviate
from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
import os
from dotenv import load_dotenv
import weaviate.classes.init as auth # Add this import

load_dotenv()

# 1. Setup Models
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/text-embedding-004",
    api_key=os.getenv("GOOGLE_API_KEY")
)
Settings.llm = GoogleGenAI(
    model="models/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

class RAGService:
    def __init__(self):
        # Read from Environment Variables
        wcs_url = os.getenv("WEAVIATE_URL")
        wcs_api_key = os.getenv("WEAVIATE_API_KEY")

        if wcs_url and wcs_api_key:
            print("🌍 Connecting to Weaviate Cloud...")
            self.client = weaviate.connect_to_wcs(
                cluster_url=wcs_url,
                auth_credentials=auth.Auth.api_key(wcs_api_key)
            )
        else:
            print("🏠 Connecting to Localhost...")
            self.client = weaviate.connect_to_local()
        
        self.index_name = "EnterpriseKB"
        self.index = None
        self._connect_index()

    def _connect_index(self):
        try:
            # Weaviate v4 connection logic
            vector_store = WeaviateVectorStore(
                weaviate_client=self.client, 
                index_name=self.index_name
            )
            # Try to load existing index
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store
            )
        except Exception as e:
            print(f"Index not ready yet: {e}")

    def ingest_text(self, text: str):
        """Takes raw text from frontend and indexes it."""
        print("Processing new data...")
        documents = [Document(text=text)]
        
        vector_store = WeaviateVectorStore(
            weaviate_client=self.client, 
            index_name=self.index_name
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # This creates (or updates) the index in Weaviate
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context
        )
        return "Ingestion Complete"

    def chat(self, query: str):
        if not self.index:
            return "Knowledge Base is empty. Please upload data first."
        
        chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            system_prompt="You are a professional assistant. Answer using the context provided.",
            similarity_top_k=5
        )
        response = chat_engine.chat(query)
        return response.response

# Singleton
rag_service = RAGService()