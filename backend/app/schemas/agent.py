from __future__ import annotations
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentDiagnoseRequest(BaseModel):
    image_result: Dict[str, Any] = Field(
        ...,
        description="Detection result containing crop, condition, confidence, and category"
    )
    farmer_question: str = Field(
        default="What are the symptoms, treatment, and preventive measures for this condition?",
        description="Farmer's specific inquiry"
    )


class AgentDiagnoseResponse(BaseModel):
    status: str = Field(default="success")
    crop: str
    condition: str
    category: str
    confidence: float
    urgency_level: str = Field(..., description="'High', 'Moderate', or 'Low'")
    final_answer: str
    sources: List[str] = Field(default_factory=list)
    action_plan: List[str] = Field(default_factory=list)
