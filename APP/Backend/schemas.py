from pydantic import BaseModel
from typing import Optional


class LocationOnlyInput(BaseModel):
    location: str                           # e.g. "Hyderabad"
    crop: Optional[str] = None              # Optional target crop for evaluation
    phosphorus: Optional[float] = None      # soil-test P override (kg/ha index)
    potassium: Optional[float] = None       # soil-test K override (kg/ha index)
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)


class CropLocationInput(BaseModel):
    location: str
    crop: str                               # e.g. "rice"
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)


class YieldInput(BaseModel):
    location: str
    crop: str
    area: float = 1.0                       # hectares
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)


class IrrigationInput(BaseModel):
    location: str
    crop: str
    growth_stage: str = "Development"       # Initial | Development | Mid-season | Late-season
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)


class MarketInput(BaseModel):
    location: str
    commodity: str
    arrival_quantity: Optional[float] = None
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

