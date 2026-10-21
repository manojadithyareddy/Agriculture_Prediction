from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field


class DetectionItem(BaseModel):
    model: str = Field(..., description="Roboflow model used")
    class_name: str = Field(..., description="Detected class name / disorder")
    confidence: float = Field(..., description="Confidence percentage 0-100")
    bbox: List[float] = Field(..., description="Bounding box [x, y, width, height]")


class DetectionResponse(BaseModel):
    status: str = Field(default="success")
    crop: str = Field(..., description="Identified or target crop")
    condition: str = Field(..., description="Identified disease, pest, or condition")
    category: str = Field(..., description="'Disease', 'Pest', or 'Healthy'")
    confidence: float = Field(..., description="Confidence score 0.0 - 1.0")
    best_model: str = Field(..., description="Model that produced highest confidence match")
    total_detections: int = Field(default=0)
    all_detections: List[DetectionItem] = Field(default_factory=list)
    annotated_image_base64: Optional[str] = Field(
        default=None, description="Base64 encoded JPEG with visual bounding boxes and labels"
    )
    suggested_actions: List[str] = Field(
        default_factory=list, description="Immediate initial recommendations"
    )
