from __future__ import annotations
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Base directories
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BACKEND_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "AgriPredict AI & Agriculture Advisory API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Supabase credentials
    SUPABASE_URL: str = Field(default="https://xenrnczedenmvljzlbin.supabase.co")
    SUPABASE_KEY: str = Field(default="sb_publishable_BkmeBl1mAwJl6uQDOctAPw_gtrQwkC-")
    SUPABASE_SERVICE_KEY: str = Field(default="")

    # Roboflow for YOLO disease/pest detection
    ROBOFLOW_API_KEY: str = Field(default="piCQRV6hQpQMRRREQWpi")

    # LLM and Vision API Keys
    OPENAI_API_KEY: str = ""
    HF_TOKEN: str = ""
    LOCAL_LLM_MODEL: str = "google/flan-t5-base"

    # RAG & Embedding Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_CHUNK_SIZE: int = 800
    RAG_CHUNK_OVERLAP: int = 150
    RAG_TOP_K: int = 4

    # Paths
    MODELS_DIR: str = str(BACKEND_DIR / "models")
    DATA_DIR: str = str(PROJECT_ROOT / "Data")
    WEATHER_CSV_PATH: str = str(PROJECT_ROOT / "Data" / "AP_TS_Weather_Dataset.csv")
    CHROMA_DB_DIR: str = str(PROJECT_ROOT / "agriculture_db")
    PDF_DIR: str = str(BACKEND_DIR / "data" / "disease_pdfs")

    # Security & CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

settings = Settings()
