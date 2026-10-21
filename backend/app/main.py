import os
import sys
import logging
from contextlib import asynccontextmanager

# Fix for OpenBLAS Memory allocation error on Windows
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OPENBLAS_CORETYPE"] = "HASWELL"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import api_v1_router
from app.api.v1.predictions import router as legacy_predictions_router
from app.schemas.predictions import RootResponse

logger = logging.getLogger(__name__)

API_DESCRIPTION = """
## 🌾 AgriPredict AI — Agriculture Advisory API

A comprehensive production AI-powered agriculture platform for **Andhra Pradesh & Telangana**
providing actionable predictions across key agricultural domains:

- **Crop Recommendation** (`/api/v1/predict/crop-recommendation`)
- **Climate Risk Assessment** (`/api/v1/predict/climate-risk`)
- **Yield Prediction** (`/api/v1/predict/yield`)
- **Irrigation Scheduling** (`/api/v1/predict/irrigation`)
- **Market Price Forecast** (`/api/v1/predict/market-price`)
- **Disease & Pest Detection** (`/api/v1/detect/disease`)
- **AI Agronomist Chat & RAG** (`/api/v1/chat/message`)
- **Multi-modal AI Agent** (`/api/v1/agent/diagnose`)
- **RAG Knowledge Management** (`/api/v1/rag/stats`, `/api/v1/rag/ingest`, `/api/v1/rag/evaluate`)
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: auto-ingest PDF documents into the RAG vector store."""
    try:
        from app.rag.vector_store import vector_store
        from app.rag.document_loader import load_documents_from_directory

        pdf_dir = settings.PDF_DIR
        if os.path.exists(pdf_dir):
            docs = load_documents_from_directory(pdf_dir)
            if docs:
                vector_store.add_documents(docs)
                logger.info(
                    f"RAG startup: ingested {len(docs)} chunks from '{pdf_dir}'. "
                    f"Total documents: {vector_store.document_count}"
                )
        else:
            logger.info(
                f"RAG startup: no PDF directory found at '{pdf_dir}'; "
                f"using {vector_store.document_count} built-in knowledge entries."
            )
    except Exception as e:
        logger.warning(f"RAG startup ingestion failed (non-fatal): {e}")

    yield  # Application runs here

app = FastAPI(
    title=settings.APP_NAME,
    description=API_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Versioned API (v1)
app.include_router(api_v1_router)

# Mount legacy routes for backwards compatibility with existing frontend/tests
app.include_router(legacy_predictions_router)


@app.get(
    "/",
    response_model=RootResponse,
    tags=["Health"],
    summary="API status and discovery",
    description="Returns API status, version, and primary prediction endpoints.",
)
def root():
    return {
        "status": "ok",
        "endpoints": [
            "/api/v1/predict/crop-recommendation",
            "/api/v1/predict/climate-risk",
            "/api/v1/predict/yield",
            "/api/v1/predict/irrigation",
            "/api/v1/predict/market-price",
            "/api/v1/health",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
