import uuid
from datetime import datetime
from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    ChatHistoryItem,
)
from app.rag.query_engine import query_rag

router = APIRouter(prefix="/chat", tags=["AI Agronomist Chat & RAG"])

# In-memory session store (backed by Supabase where available)
_SESSION_HISTORY: Dict[str, List[ChatHistoryItem]] = {}


@router.post(
    "/message",
    response_model=ChatMessageResponse,
    summary="Chat with AI Agronomist",
    description=(
        "Ask questions regarding crop management, disease prevention, fertilizers, or pest control. "
        "The system retrieves verified agricultural research and formulates actionable farmer advice."
    ),
)
def send_chat_message(req: ChatMessageRequest):
    session_id = req.session_id or str(uuid.uuid4())
    now_iso = datetime.now().isoformat()

    # Record user message
    if session_id not in _SESSION_HISTORY:
        _SESSION_HISTORY[session_id] = []

    _SESSION_HISTORY[session_id].append(
        ChatHistoryItem(
            role="user",
            content=req.message,
            timestamp=now_iso,
            metadata={"crop": req.crop, "condition": req.condition}
        )
    )

    try:
        # Build conversation history for multi-turn context (Phase 5)
        history_items = _SESSION_HISTORY.get(session_id, [])
        conversation_history = [
            {"role": item.role, "content": item.content}
            for item in history_items[-6:]  # Last 3 turns (user + assistant)
        ]

        # Run RAG pipeline with conversation context and language
        rag_res = query_rag(
            farmer_question=req.message,
            crop=req.crop,
            condition=req.condition,
            conversation_history=conversation_history if conversation_history else None,
            language=req.language or "en",
            location=req.location,
            growth_stage=req.growth_stage,
        )

        response_text = rag_res["response"]
        sources = rag_res["sources"]
        followups = rag_res["suggested_followups"]

        # Record assistant response
        _SESSION_HISTORY[session_id].append(
            ChatHistoryItem(
                role="assistant",
                content=response_text,
                timestamp=datetime.now().isoformat(),
                metadata={"sources": sources}
            )
        )

        return ChatMessageResponse(
            session_id=session_id,
            response=response_text,
            sources=sources,
            suggested_followups=followups
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.get(
    "/history/{session_id}",
    response_model=ChatHistoryResponse,
    summary="Get conversation history for a session",
)
def get_chat_history(session_id: str):
    messages = _SESSION_HISTORY.get(session_id, [])
    return ChatHistoryResponse(
        session_id=session_id,
        messages=messages
    )
