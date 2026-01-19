import weaviate
from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
import weaviate.classes.init as auth # Add this import

load_dotenv()

# 1. Setup Models
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/text-embedding-004",
    api_key=os.getenv("GOOGLE_API_KEY")
)
Settings.llm = Gemini(
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