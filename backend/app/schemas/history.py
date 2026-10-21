from __future__ import annotations
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class PredictionLogItem(BaseModel):
    id: Optional[str] = None
    prediction_type: str
    location: Optional[str] = None
    crop: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    results: Dict[str, Any] = Field(default_factory=dict)
    model_source: Optional[str] = None
    created_at: Optional[str] = None


class PredictionHistoryResponse(BaseModel):
    total: int
    predictions: List[PredictionLogItem]


class DashboardStatsResponse(BaseModel):
    total_predictions: int
    active_models: int
    covered_districts: int
    supported_crops: int
    categories: Dict[str, int] = Field(default_factory=dict)
