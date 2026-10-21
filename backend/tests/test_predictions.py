import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["endpoints"]) > 0


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "models" in data
    assert "climate_risk_model" in data["models"]


def test_crop_recommendation_v1():
    payload = {"location": "Hyderabad"}
    response = client.post("/api/v1/predict/crop-recommendation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_crop" in data
    assert "top_5" in data
    assert len(data["top_5"]) == 5
    assert data["location"].lower() == "hyderabad"


def test_climate_risk_v1():
    payload = {"location": "Hyderabad", "crop": "Rice"}
    response = client.post("/api/v1/predict/climate-risk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "climate_risk" in data
    assert data["climate_risk"] in ["low", "moderate", "high", "extreme"]
    assert "probabilities" in data


def test_yield_prediction_v1():
    payload = {"location": "Guntur", "crop": "Cotton", "area": 1.5}
    response = client.post("/api/v1/predict/yield", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_yield" in data
    assert data["predicted_yield"] > 0
    assert "yield_per_ha" in data


def test_irrigation_prediction_v1():
    payload = {"location": "Warangal", "crop": "Maize", "growth_stage": "Development"}
    response = client.post("/api/v1/predict/irrigation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_water_requirement_mm_per_day" in data
    assert data["predicted_water_requirement_mm_per_day"] > 0
    assert "details" in data


def test_market_price_v1():
    payload = {"location": "Krishna", "commodity": "Banana", "arrival_quantity": 100.0}
    response = client.post("/api/v1/predict/market-price", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price_per_quintal" in data
    assert data["predicted_price_per_quintal"] > 0


def test_legacy_routes_backwards_compatibility():
    """Verify legacy top-level routes (/predict/*) match v1 responses."""
    payload = {"location": "Hyderabad"}
    response = client.post("/predict/crop-recommendation", json=payload)
    assert response.status_code == 200
    assert "recommended_crop" in response.json()
