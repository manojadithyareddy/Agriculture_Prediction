from pydantic import BaseModel
from typing import Optional, Any


# ═══════════════════════════════════════════════════════════════════════════════
#  REQUEST (Input) Models
# ═══════════════════════════════════════════════════════════════════════════════

class LocationOnlyInput(BaseModel):
    location: str                           # e.g. "Hyderabad"
    crop: Optional[str] = None              # Optional target crop for evaluation
    phosphorus: Optional[float] = None      # soil-test P override (kg/ha index)
    potassium: Optional[float] = None       # soil-test K override (kg/ha index)
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Hyderabad",
                    "crop": "rice",
                    "phosphorus": 45.0,
                    "potassium": 50.0,
                    "predict_date": None
                }
            ]
        }
    }


class CropLocationInput(BaseModel):
    location: str
    crop: str                               # e.g. "rice"
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Hyderabad",
                    "crop": "rice",
                    "predict_date": None
                }
            ]
        }
    }


class YieldInput(BaseModel):
    location: str
    crop: str
    area: float = 1.0                       # hectares
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Guntur",
                    "crop": "cotton",
                    "area": 5.0,
                    "predict_date": None
                }
            ]
        }
    }


class IrrigationInput(BaseModel):
    location: str
    crop: str
    growth_stage: str = "Development"       # Initial | Development | Mid-season | Late-season
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Warangal",
                    "crop": "maize",
                    "growth_stage": "Development",
                    "predict_date": None
                }
            ]
        }
    }


class MarketInput(BaseModel):
    location: str
    commodity: str
    arrival_quantity: Optional[float] = None
    predict_date: Optional[str] = None      # ISO date string "YYYY-MM-DD" (None = today)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Krishna",
                    "commodity": "banana",
                    "arrival_quantity": 100.0,
                    "predict_date": None
                }
            ]
        }
    }


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  RESPONSE (Output) Models
# ═══════════════════════════════════════════════════════════════════════════════

# ── Crop Recommendation ─────────────────────────────────────────────────────

class CropCandidate(BaseModel):
    """A single crop with its confidence score."""
    crop: str
    confidence: float


class TargetCropEval(BaseModel):
    """Evaluation of a user-requested target crop against the recommendation."""
    requested_crop: str
    rank: Any                               # int or "N/A"
    confidence: float
    suitability: str                        # "High" | "Moderate" | "Low"


class CropInputsUsed(BaseModel):
    """Input features fed into the crop recommendation model."""
    N: float
    P: float
    K: float
    ph: float
    temperature: float
    humidity: float
    rainfall: float


class CropRecommendationResponse(BaseModel):
    """Full response for the crop recommendation endpoint."""
    location: str
    date: str
    recommended_crop: str
    top_5: list[CropCandidate]
    target_crop_eval: Optional[TargetCropEval] = None
    model_source: str
    inputs_used: CropInputsUsed

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Hyderabad",
                    "date": "2026-09-16",
                    "recommended_crop": "pigeonpeas",
                    "top_5": [
                        {"crop": "pigeonpeas", "confidence": 0.062},
                        {"crop": "muskmelon", "confidence": 0.061},
                        {"crop": "blackgram", "confidence": 0.060},
                        {"crop": "mango", "confidence": 0.057},
                        {"crop": "pomegranate", "confidence": 0.055}
                    ],
                    "target_crop_eval": {
                        "requested_crop": "rice",
                        "rank": 19,
                        "confidence": 0.035,
                        "suitability": "Low"
                    },
                    "model_source": "fallback",
                    "inputs_used": {
                        "N": 280.0, "P": 45.0, "K": 50.0, "ph": 7.0,
                        "temperature": 30.0, "humidity": 60.0, "rainfall": 0.0
                    }
                }
            ]
        }
    }


# ── Climate Risk ─────────────────────────────────────────────────────────────

class ClimateRiskResponse(BaseModel):
    """Full response for the climate risk endpoint."""
    location: str
    date: str
    crop: str
    season: str
    climate_risk: str                       # "low" | "moderate" | "high" | "extreme"
    probabilities: dict[str, float]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Hyderabad",
                    "date": "2026-09-16",
                    "crop": "rice",
                    "season": "monsoon",
                    "climate_risk": "low",
                    "probabilities": {
                        "low": 0.894,
                        "moderate": 0.059,
                        "high": 0.032,
                        "extreme": 0.015
                    }
                }
            ]
        }
    }


# ── Yield Prediction ─────────────────────────────────────────────────────────

class YieldFactors(BaseModel):
    """Breakdown of environmental factors affecting predicted yield."""
    temperature_factor: float
    water_stress_factor: float
    soil_fertility_index: float
    solar_factor: float


class YieldPredictionResponse(BaseModel):
    """Full response for the yield prediction endpoint."""
    location: str
    date: str
    crop: str
    season: str
    area: float
    predicted_yield: float
    yield_per_ha: Optional[float] = None
    model_source: str
    factors: Optional[YieldFactors] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Guntur",
                    "date": "2026-09-16",
                    "crop": "cotton",
                    "season": "Kharif",
                    "area": 5.0,
                    "predicted_yield": 7.85,
                    "yield_per_ha": 1.57,
                    "model_source": "fao_fallback",
                    "factors": {
                        "temperature_factor": 0.95,
                        "water_stress_factor": 0.82,
                        "soil_fertility_index": 0.71,
                        "solar_factor": 1.0
                    }
                }
            ]
        }
    }


# ── Irrigation Prediction ───────────────────────────────────────────────────

class IrrigationDetails(BaseModel):
    """Detailed breakdown of irrigation calculation (FAO-56)."""
    ET0_mm_day: float
    Kc: float
    ETc_mm_day: float
    effective_rain: float
    net_irrigation: float


class IrrigationPredictionResponse(BaseModel):
    """Full response for the irrigation prediction endpoint."""
    location: str
    date: str
    crop: str
    growth_stage: str
    predicted_water_requirement_mm_per_day: float
    model_source: str
    details: Optional[IrrigationDetails] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Warangal",
                    "date": "2026-09-16",
                    "crop": "maize",
                    "growth_stage": "Development",
                    "predicted_water_requirement_mm_per_day": 6.42,
                    "model_source": "fao56_penman_monteith",
                    "details": {
                        "ET0_mm_day": 8.5,
                        "Kc": 0.7,
                        "ETc_mm_day": 5.95,
                        "effective_rain": 1.6,
                        "net_irrigation": 4.35
                    }
                }
            ]
        }
    }


# ── Market Price ─────────────────────────────────────────────────────────────

class PriceFactors(BaseModel):
    """Breakdown of factors used in the market price fallback model."""
    base_price_2023: float
    seasonal_multiplier: float
    district_premium: float
    inflation_factor: float


class MarketPriceResponse(BaseModel):
    """Full response for the market price prediction endpoint."""
    location: str
    date: str
    commodity: str
    arrival_quantity: float
    predicted_price_per_quintal: float
    model_source: str
    price_factors: Optional[PriceFactors] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "Krishna",
                    "date": "2026-09-16",
                    "commodity": "banana",
                    "arrival_quantity": 100.0,
                    "predicted_price_per_quintal": 2085.75,
                    "model_source": "calibrated_apmc_fallback",
                    "price_factors": {
                        "base_price_2023": 1800,
                        "seasonal_multiplier": 1.05,
                        "district_premium": 1.04,
                        "inflation_factor": 1.158
                    }
                }
            ]
        }
    }


# ── Root / Health Check ──────────────────────────────────────────────────────

class RootResponse(BaseModel):
    """Health check response listing all available endpoints."""
    status: str
    endpoints: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "ok",
                    "endpoints": [
                        "/predict/crop-recommendation",
                        "/predict/climate-risk",
                        "/predict/yield",
                        "/predict/irrigation",
                        "/predict/market-price"
                    ]
                }
            ]
        }
    }
