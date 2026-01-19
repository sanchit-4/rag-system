import os
from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Gemini Restaurant RAG"
    DEBUG_MODE: bool = True
    
    # API Keys
    GOOGLE_API_KEY: str
    
    # Database
    WEAVIATE_URL: str = "http://localhost:8080"
    INDEX_NAME: str = "RestaurantData"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

settings = Settings()