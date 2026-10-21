import os
# Fix for OpenBLAS Memory allocation error
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OPENBLAS_CORETYPE"] = "HASWELL"

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    LocationOnlyInput, CropLocationInput, YieldInput, IrrigationInput, MarketInput,
    CropRecommendationResponse, ClimateRiskResponse, YieldPredictionResponse,
    IrrigationPredictionResponse, MarketPriceResponse, RootResponse,
)

from predict_crop import predict_crop
from predict_climate_risk import predict_climate_risk
from predict_yield import predict_yield
from predict_irrigation import predict_irrigation
from predict_market import predict_price

API_DESCRIPTION = """
## 🌾 Agriculture Prediction API

A comprehensive AI-powered agriculture advisory system for **Andhra Pradesh & Telangana**
that provides actionable predictions across five key domains:

- **Crop Recommendation** — Suggests the best crops based on soil, weather, and nutrient data.
- **Climate Risk Assessment** — Evaluates climate hazards (drought, flood, heat stress) for a crop.
- **Yield Prediction** — Estimates expected crop yield using FAO-calibrated models.
- **Irrigation Scheduling** — Computes daily water requirements via FAO-56 Penman-Monteith.
- **Market Price Forecast** — Predicts APMC mandi prices using seasonal and supply factors.

All endpoints accept a **location name** (city/district) and return real-time predictions
derived from live weather data, soil profiles, and trained ML models.
"""

app = FastAPI(
    title="Agriculture Prediction API",
    description=API_DESCRIPTION,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/predict/crop-recommendation",
    response_model=CropRecommendationResponse,
    tags=["Predictions"],
    summary="Recommend the best crop for a location",
    description=(
        "Analyses soil nutrients (N, P, K), weather conditions (temperature, humidity, rainfall), "
        "and soil pH to recommend the most suitable crop. Returns the top 5 candidates with "
        "confidence scores. Optionally evaluates a user-specified target crop."
    ),
)
def crop_recommendation(data: LocationOnlyInput):
    try:
        return predict_crop(data.location, crop=data.crop, phosphorus=data.phosphorus, potassium=data.potassium)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/predict/climate-risk",
    response_model=ClimateRiskResponse,
    tags=["Predictions"],
    summary="Assess climate risk for a crop at a location",
    description=(
        "Evaluates the climate risk (low / moderate / high / extreme) for growing a specific crop "
        "at a given location. Uses weather data, soil properties, and a trained Random Forest "
        "classifier to predict risk probabilities."
    ),
)
def climate_risk(data: CropLocationInput):
    try:
        return predict_climate_risk(data.location, data.crop)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/predict/yield",
    response_model=YieldPredictionResponse,
    tags=["Predictions"],
    summary="Predict crop yield for a given area",
    description=(
        "Estimates the expected crop yield (in tonnes) using FAO-calibrated factors: "
        "temperature response, water stress, soil fertility, and solar radiation efficiency. "
        "Supports both trained ML models and a physics-based fallback."
    ),
)
def yield_prediction(data: YieldInput):
    try:
        return predict_yield(data.location, data.crop, data.area)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/predict/irrigation",
    response_model=IrrigationPredictionResponse,
    tags=["Predictions"],
    summary="Calculate irrigation water requirement",
    description=(
        "Computes the daily irrigation water requirement (mm/day) for a crop at a specific "
        "growth stage using the FAO-56 Penman-Monteith reference evapotranspiration method. "
        "Accounts for crop coefficient (Kc), effective rainfall, and soil water capacity."
    ),
)
def irrigation_prediction(data: IrrigationInput):
    try:
        return predict_irrigation(data.location, data.crop, data.growth_stage)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/predict/market-price",
    response_model=MarketPriceResponse,
    tags=["Predictions"],
    summary="Forecast market price for a commodity",
    description=(
        "Predicts the APMC mandi price (₹/quintal) for an agricultural commodity at a location. "
        "Uses seasonal demand multipliers, arrival quantity elasticity, district demand tiers, "
        "and year-on-year inflation adjustments calibrated from Agmarknet / e-NAM data."
    ),
)
def market_price(data: MarketInput):
    try:
        return predict_price(data.location, data.commodity, data.arrival_quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/",
    response_model=RootResponse,
    tags=["Health"],
    summary="API health check",
    description="Returns the API status and a list of all available prediction endpoints.",
)
def root():
    return {"status": "ok", "endpoints": [
        "/predict/crop-recommendation", "/predict/climate-risk",
        "/predict/yield", "/predict/irrigation", "/predict/market-price",
    ]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)