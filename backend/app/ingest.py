import os
import weaviate
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Settings
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from app.config import settings
import logging

# REMOVED: from app.engine import LlamaSettings (This does not exist!)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURATION (Must match engine.py) ---
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/text-embedding-004", 
    api_key=settings.GOOGLE_API_KEY,
    embed_batch_size=10  # Keep this small for free tier
)

Settings.llm = GoogleGenAI(
    model_name="models/gemini-2.5-flash", 
    api_key=settings.GOOGLE_API_KEY
)
# --------------------------------------------

def ingest_documents():
    data_dir = "../data" # Ensure this path is correct relative to where you run the script
    
    if not os.path.exists(data_dir):
        logger.error(f"❌ Data directory '{data_dir}' not found.")
        return

    logger.info("📂 Loading documents...")
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    logger.info("🔌 Connecting to Weaviate...")
    # UPDATED: Weaviate v4 Syntax
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080,
        grpc_port=50051
    )
    
    try:
        vector_store = WeaviateVectorStore(
            weaviate_client=client, 
            index_name=settings.INDEX_NAME
        )
        
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        logger.info("🧠 Generating Embeddings & Indexing (This may take a moment)...")
        
        # Create Index
        VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        
        logger.info(f"✅ Ingestion Complete! {len(documents)} documents indexed.")
    
    finally:
        # v4 Good Practice: Close the connection
        client.close()

if __name__ == "__main__":
    ingest_documents()