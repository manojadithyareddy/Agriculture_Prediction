"""
market.py — Agricultural Market Intelligence API Routes
=======================================================
Endpoints supporting the Market Intelligence Portal (/market):
- GET /api/v1/market/quotes
- GET /api/v1/market/forecast
- GET /api/v1/market/history
- GET /api/v1/market/msp
- GET /api/v1/market/mandis
- GET /api/v1/market/export/csv
"""
from __future__ import annotations

import io
import csv
from typing import Optional
from fastapi import APIRouter, Query, Response, HTTPException

from app.services.market_service import (
    get_mandi_quotes,
    get_price_forecast,
    get_historical_mandi_series,
    OFFICIAL_MSP_REGISTRY,
    APMC_MANDI_DIRECTORY,
)

router = APIRouter(prefix="/market", tags=["Market Intelligence & Pricing"])


@router.get(
    "/quotes",
    summary="Get observed APMC Mandi prices",
    description="Returns authentic daily reported prices (Min, Max, Modal) and MSP comparisons from Agmarknet & e-NAM.",
)
def get_quotes(
    commodity: str = Query(default="Rice", description="Commodity or crop name (e.g. Rice, Cotton, Maize, Banana)"),
    district: Optional[str] = Query(default=None, description="Optional district filter"),
    state: Optional[str] = Query(default=None, description="Optional state filter ('Telangana' or 'Andhra Pradesh')"),
):
    try:
        return get_mandi_quotes(commodity=commodity, district_filter=district, state_filter=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data lookup failed: {str(e)}")


@router.get(
    "/forecast",
    summary="Get multi-horizon commodity price forecast",
    description="Generates backtested 7, 14, or 30-day forecast curves with 95% confidence intervals and validation metrics.",
)
def get_forecast(
    commodity: str = Query(default="Rice", description="Commodity name"),
    location: str = Query(default="Warangal", description="District or mandi location"),
    days: int = Query(default=14, ge=3, le=30, description="Forecast horizon in days (3-30)"),
):
    try:
        return get_price_forecast(commodity=commodity, location=location, horizon_days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market forecast failed: {str(e)}")


@router.get(
    "/history",
    summary="Get historical daily mandi prices",
    description="Returns historical observed daily prices (min, max, modal, arrivals) for trend analysis.",
)
def get_history(
    commodity: str = Query(default="Rice", description="Commodity name"),
    location: str = Query(default="Warangal", description="District or mandi location"),
    days: int = Query(default=30, ge=7, le=90, description="Number of past days (7-90)"),
):
    try:
        return get_historical_mandi_series(commodity=commodity, location=location, days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Historical data lookup failed: {str(e)}")


@router.get(
    "/msp",
    summary="Get official Government MSP Benchmarks",
    description="Returns official CACP / Ministry of Agriculture Minimum Support Prices for AP/TS crops.",
)
def get_msp_benchmarks():
    return {
        "success": True,
        "official_source": "Commission for Agricultural Costs & Prices (CACP), Ministry of Agriculture & Farmers Welfare",
        "market_year": "2024-25 & 2023-24",
        "commodities": OFFICIAL_MSP_REGISTRY,
    }


@router.get(
    "/mandis",
    summary="List major APMC mandis in AP and Telangana",
    description="Returns directory of major terminal, regional, and district mandis with coordinates and coverage.",
)
def list_mandis():
    return {
        "success": True,
        "total_mandis": len(APMC_MANDI_DIRECTORY),
        "mandis": APMC_MANDI_DIRECTORY,
    }


@router.get(
    "/export/csv",
    summary="Download Market Intelligence CSV report",
    description="Exports observed mandi prices and MSP comparison as a downloadable CSV.",
)
def export_market_csv(
    commodity: str = Query(default="Rice", description="Commodity name"),
    district: Optional[str] = Query(default=None, description="Optional district filter"),
):
    data = get_mandi_quotes(commodity=commodity, district_filter=district)
    quotes = data.get("mandi_quotes", [])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Mandi ID", "Mandi Name", "District", "State", "Commodity",
        "Min Price (INR/Q)", "Modal Price (INR/Q)", "Max Price (INR/Q)",
        "Arrival Quantity (Tonnes)", "Reporting Date", "Data Source"
    ])

    for q in quotes:
        writer.writerow([
            q.get("mandi_id"),
            q.get("mandi_name"),
            q.get("district"),
            q.get("state"),
            q.get("commodity"),
            q.get("min_price"),
            q.get("modal_price"),
            q.get("max_price"),
            q.get("arrival_quantity_tonnes"),
            q.get("reporting_date"),
            q.get("source"),
        ])

    csv_content = output.getvalue()
    filename = f"mandi_report_{commodity.lower()}_{data.get('reporting_date')}.csv"

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
