"""
rag.py — RAG Management & Evaluation API Endpoints
=====================================================
Phase 6: Document management, store statistics, and evaluation.

Endpoints:
    POST /api/v1/rag/ingest      — Upload & ingest new documents
    GET  /api/v1/rag/stats       — Vector store health & statistics
    POST /api/v1/rag/evaluate    — Run evaluation queries and score results
    GET  /api/v1/rag/documents   — List all ingested document IDs
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field

from app.rag.vector_store import vector_store
from app.rag.document_loader import load_documents_from_directory
from app.rag.query_engine import query_rag
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Management"])


# ── Schemas ──────────────────────────────────────────────────

class RAGStatsResponse(BaseModel):
    total_documents: int
    chroma_available: bool
    chroma_count: int
    embeddings_available: bool
    embedding_model: str
    bm25_vocab_size: int
    queries_served: int
    avg_latency_ms: float


class IngestResponse(BaseModel):
    status: str
    documents_added: int
    total_documents: int
    message: str


class EvalQuestion(BaseModel):
    question: str = Field(..., description="Test question")
    expected_crop: Optional[str] = Field(None, description="Expected crop in result")
    expected_condition: Optional[str] = Field(None, description="Expected condition in result")


class EvalRequest(BaseModel):
    questions: List[EvalQuestion] = Field(
        ..., description="List of evaluation questions"
    )


class EvalResultItem(BaseModel):
    question: str
    top_crop: str
    top_condition: str
    top_score: float
    crop_match: bool
    condition_match: bool
    latency_ms: float
    retrieval_method: str


class EvalResponse(BaseModel):
    total_questions: int
    crop_accuracy: float
    condition_accuracy: float
    avg_latency_ms: float
    results: List[EvalResultItem]


class DocumentListResponse(BaseModel):
    total: int
    documents: List[Dict[str, Any]]


# ── Endpoints ────────────────────────────────────────────────

@router.get(
    "/stats",
    response_model=RAGStatsResponse,
    summary="RAG Vector Store Statistics",
    description="Returns health and performance statistics for the RAG retrieval system.",
)
def get_rag_stats():
    """Return vector store health stats."""
    stats = vector_store.get_stats()
    return RAGStatsResponse(**stats)


@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest Documents into RAG",
    description="Trigger ingestion of documents from the configured PDF directory.",
)
def ingest_documents(
    directory: Optional[str] = Form(None, description="Custom directory path (optional)"),
):
    """Ingest documents from a directory into the vector store."""
    target_dir = directory or settings.PDF_DIR

    try:
        chunks = load_documents_from_directory(target_dir)
        if chunks:
            vector_store.add_documents(chunks)

        return IngestResponse(
            status="success",
            documents_added=len(chunks),
            total_documents=vector_store.document_count,
            message=f"Ingested {len(chunks)} document chunks from '{target_dir}'.",
        )
    except Exception as e:
        logger.error(f"Document ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.get(
    "/documents",
    response_model=DocumentListResponse,
    summary="List Ingested Documents",
    description="Returns a summary of all documents currently in the vector store.",
)
def list_documents(limit: int = 50, offset: int = 0):
    """List document summaries in the vector store."""
    docs = vector_store.documents[offset : offset + limit]
    summaries = []
    for doc in docs:
        summaries.append({
            "id": doc.get("id", "unknown"),
            "title": doc.get("title", "Untitled"),
            "crop": doc.get("crop", ""),
            "condition": doc.get("condition", ""),
            "category": doc.get("category", ""),
            "source": doc.get("source", ""),
            "content_length": len(doc.get("content", "")),
        })

    return DocumentListResponse(
        total=vector_store.document_count,
        documents=summaries,
    )


@router.post(
    "/evaluate",
    response_model=EvalResponse,
    summary="Evaluate RAG Retrieval Quality",
    description=(
        "Run a batch of test questions against the RAG pipeline and measure "
        "retrieval accuracy (crop match, condition match) and latency."
    ),
)
def evaluate_rag(req: EvalRequest):
    """
    Phase 6: Evaluation endpoint.
    Measures how well the RAG retrieves correct crops/conditions.
    """
    results: List[EvalResultItem] = []
    crop_matches = 0
    cond_matches = 0
    total_latency = 0.0

    for eq in req.questions:
        t_start = time.perf_counter()
        rag_result = query_rag(farmer_question=eq.question, k=3)
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        total_latency += elapsed_ms

        retrieved = rag_result.get("retrieved_docs", [])
        top_doc = retrieved[0] if retrieved else {}

        top_crop = top_doc.get("crop", "")
        top_condition = top_doc.get("condition", "")
        top_score = top_doc.get("relevance_score", 0.0)

        crop_ok = (
            eq.expected_crop is not None
            and eq.expected_crop.lower() in top_crop.lower()
        ) if eq.expected_crop else True

        cond_ok = (
            eq.expected_condition is not None
            and eq.expected_condition.lower() in top_condition.lower()
        ) if eq.expected_condition else True

        if crop_ok:
            crop_matches += 1
        if cond_ok:
            cond_matches += 1

        results.append(
            EvalResultItem(
                question=eq.question,
                top_crop=top_crop,
                top_condition=top_condition,
                top_score=top_score,
                crop_match=crop_ok,
                condition_match=cond_ok,
                latency_ms=round(elapsed_ms, 1),
                retrieval_method=rag_result.get("retrieval_method", "unknown"),
            )
        )

    total = len(req.questions) or 1

    return EvalResponse(
        total_questions=len(req.questions),
        crop_accuracy=round(crop_matches / total, 3),
        condition_accuracy=round(cond_matches / total, 3),
        avg_latency_ms=round(total_latency / total, 1),
        results=results,
    )


# ────────────────────────────────────────────────────────────
# Built-in Evaluation Dataset (20 curated farmer questions)
# ────────────────────────────────────────────────────────────
BUILTIN_EVAL_QUESTIONS: List[Dict[str, Any]] = [
    {"question": "My rice leaves have spindle-shaped spots with gray centers", "expected_crop": "Rice", "expected_condition": "Blast"},
    {"question": "Circular brown patches in my rice field, plants drying from base", "expected_crop": "Rice", "expected_condition": "Brown Plant Hopper"},
    {"question": "Banana leaves have dark streaks turning into black spots", "expected_crop": "Banana", "expected_condition": "Black Sigatoka"},
    {"question": "Maize whorl has ragged holes with sawdust-like frass", "expected_crop": "Maize", "expected_condition": "Fall Armyworm"},
    {"question": "Long gray-green lesions on maize leaves starting from bottom", "expected_crop": "Maize", "expected_condition": "Turcicum Leaf Blight"},
    {"question": "Orange tree has raised corky lesions with yellow halos on leaves", "expected_crop": "Orange", "expected_condition": "Citrus Canker"},
    {"question": "Mango flowers are drying and dropping, black soot on leaves", "expected_crop": "Mango", "expected_condition": "Mango Hopper"},
    {"question": "Mango fruit has circular sunken dark spots after harvest", "expected_crop": "Mango", "expected_condition": "Anthracnose"},
    {"question": "Cotton bolls have small holes and stained lint inside", "expected_crop": "Cotton", "expected_condition": "Pink Bollworm"},
    {"question": "Pomegranate fruit has dark L-shaped cracks", "expected_crop": "Pomegranate", "expected_condition": "Bacterial Blight"},
    {"question": "Watermelon leaves have angular yellow spots with purplish mold underneath", "expected_crop": "Watermelon", "expected_condition": "Downy Mildew"},
    {"question": "White powdery patches on grape berries that crack open", "expected_crop": "Grapes", "expected_condition": "Powdery Mildew"},
    {"question": "Lower leaves of my plants are turning yellow, stunted growth", "expected_crop": "General", "expected_condition": "Nutrient Deficiency"},
    {"question": "What chemical spray for rice blast disease?", "expected_crop": "Rice", "expected_condition": "Blast"},
    {"question": "How to manage fall armyworm in maize organically?", "expected_crop": "Maize", "expected_condition": "Fall Armyworm"},
    {"question": "Citrus leaf miner damage and canker spreading", "expected_crop": "Orange", "expected_condition": "Citrus Canker"},
    {"question": "Best fungicide for grape powdery mildew?", "expected_crop": "Grapes", "expected_condition": "Powdery Mildew"},
    {"question": "How to control BPH hopper burn in paddy?", "expected_crop": "Rice", "expected_condition": "Brown Plant Hopper"},
    {"question": "Pomegranate oily spot Telya treatment", "expected_crop": "Pomegranate", "expected_condition": "Bacterial Blight"},
    {"question": "Zinc deficiency khaira disease in rice", "expected_crop": "General", "expected_condition": "Nutrient Deficiency"},
]


@router.post(
    "/evaluate/builtin",
    response_model=EvalResponse,
    summary="Run Built-in RAG Evaluation",
    description="Execute the 20-question built-in evaluation suite to benchmark retrieval quality.",
)
def evaluate_builtin():
    """Run the built-in 20-question evaluation suite."""
    eval_questions = [
        EvalQuestion(**q) for q in BUILTIN_EVAL_QUESTIONS
    ]
    return evaluate_rag(EvalRequest(questions=eval_questions))
