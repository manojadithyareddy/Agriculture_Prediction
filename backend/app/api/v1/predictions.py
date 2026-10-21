from fastapi import APIRouter, HTTPException
from app.schemas.predictions import (
    LocationOnlyInput,
    CropLocationInput,
    YieldInput,
    IrrigationInput,
    MarketInput,
    CropRecommendationResponse,
    ClimateRiskResponse,
    YieldPredictionResponse,
    IrrigationPredictionResponse,
    MarketPriceResponse,
)
from app.ml.predict_crop import predict_crop
from app.ml.predict_climate_risk import predict_climate_risk
from app.ml.predict_yield import predict_yield
from app.ml.predict_irrigation import predict_irrigation
from app.ml.predict_market import predict_price

router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post(
    "/crop-recommendation",
    response_model=CropRecommendationResponse,
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


@router.post(
    "/climate-risk",
    response_model=ClimateRiskResponse,
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


@router.post(
    "/yield",
    response_model=YieldPredictionResponse,
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


@router.post(
    "/irrigation",
    response_model=IrrigationPredictionResponse,
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


@router.post(
    "/market-price",
    response_model=MarketPriceResponse,
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
