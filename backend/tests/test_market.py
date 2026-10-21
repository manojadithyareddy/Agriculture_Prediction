import pytest
from fastapi.testclient import TestClient
import sys
import os

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app

client = TestClient(app)


def test_market_quotes_endpoint():
    response = client.get("/api/v1/market/quotes?commodity=Rice&district=Warangal")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "mandi_quotes" in data
    assert len(data["mandi_quotes"]) > 0
    first = data["mandi_quotes"][0]
    assert "modal_price" in first
    assert first["modal_price"] > 0
    assert "min_price" in first
    assert "max_price" in first
    assert "source" in first
    assert "freshness_timestamp" in first
    assert "msp_comparison" in data
    assert data["msp_comparison"]["has_msp"] is True


def test_market_quotes_non_msp():
    response = client.get("/api/v1/market/quotes?commodity=Banana")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["msp_comparison"]["has_msp"] is False


def test_market_forecast_endpoint():
    response = client.get("/api/v1/market/forecast?commodity=Cotton&location=Guntur&days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "forecast_trajectory" in data
    assert len(data["forecast_trajectory"]) == 7
    first_pt = data["forecast_trajectory"][0]
    assert "predicted_modal_price" in first_pt
    assert "lower_confidence_bound_95" in first_pt
    assert "upper_confidence_bound_95" in first_pt
    assert first_pt["lower_confidence_bound_95"] <= first_pt["predicted_modal_price"] <= first_pt["upper_confidence_bound_95"]
    assert "model_validation_metrics" in data
    assert "mean_absolute_percentage_error" in data["model_validation_metrics"]


def test_market_history_endpoint():
    response = client.get("/api/v1/market/history?commodity=Maize&location=Nizamabad&days=14")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "historical_records" in data
    assert len(data["historical_records"]) == 14


def test_market_msp_registry():
    response = client.get("/api/v1/market/msp")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "commodities" in data
    assert "rice" in data["commodities"]


def test_market_mandis_directory():
    response = client.get("/api/v1/market/mandis")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_mandis"] > 0


def test_market_export_csv():
    response = client.get("/api/v1/market/export/csv?commodity=Rice")
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert "Mandi Name" in response.text
