from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="Farmer or user question")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    crop: Optional[str] = Field(None, description="Contextual crop name")
    condition: Optional[str] = Field(None, description="Contextual disease, pest, or condition")
    language: Optional[str] = Field(default="en", description="Language code: 'en' for English, 'te' for Telugu")
    location: Optional[str] = Field(None, description="District or farm location")
    growth_stage: Optional[str] = Field(None, description="Current crop growth stage")


class ChatMessageResponse(BaseModel):
    session_id: str = Field(..., description="Active session ID")
    response: str = Field(..., description="AI Agronomist answer")
    sources: List[str] = Field(default_factory=list, description="Retrieved knowledge sources or document excerpts")
    suggested_followups: List[str] = Field(
        default_factory=list, description="Suggested next questions for the farmer"
    )


class ChatHistoryItem(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message text")
    timestamp: str = Field(..., description="ISO timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatHistoryItem] = Field(default_factory=list)
