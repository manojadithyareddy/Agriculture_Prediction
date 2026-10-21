import logging
from typing import Optional
from fastapi import APIRouter, Query, Depends
from app.schemas.history import PredictionHistoryResponse, PredictionLogItem, DashboardStatsResponse
from app.database.supabase import get_client
from app.utils.auth import get_optional_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/history", tags=["Prediction History & Analytics"])


@router.get(
    "/predictions",
    response_model=PredictionHistoryResponse,
    summary="Get recent predictions",
    description="Fetches recent prediction events from database with optional filters.",
)
def get_prediction_history(
    prediction_type: Optional[str] = Query(None, description="Filter by crop_recommendation, climate_risk, yield, etc."),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(20, ge=1, le=100),
    user: Optional[dict] = Depends(get_optional_user)
):
    try:
        client = get_client()
        query = client.table("prediction_logs").select("*").order("id", desc=True).limit(limit)

        if prediction_type:
            query = query.eq("prediction_type", prediction_type)
        if location:
            query = query.ilike("location", f"%{location}%")

        res = query.execute()
        rows = res.data if res and hasattr(res, "data") else []

        items = [
            PredictionLogItem(
                id=str(r.get("id", "")),
                prediction_type=r.get("prediction_type", ""),
                location=r.get("location"),
                crop=r.get("crop"),
                inputs=r.get("inputs") or {},
                results=r.get("results") or {},
                model_source=r.get("model_source"),
                created_at=r.get("created_at") or r.get("timestamp")
            )
            for r in rows
        ]
        return PredictionHistoryResponse(total=len(items), predictions=items)
    except Exception as e:
        logger.warning(f"Failed to fetch history from Supabase: {e}")
        # Return graceful empty list if database table or connection is restricted
        return PredictionHistoryResponse(total=0, predictions=[])


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    summary="Dashboard analytics & overview metrics",
)
def get_dashboard_stats():
    # Attempt to query live count from database
    total_count = 0
    categories = {
        "crop_recommendation": 0,
        "climate_risk": 0,
        "yield_forecast": 0,
        "irrigation_advisory": 0,
        "market_price": 0,
    }
    try:
        client = get_client()
        # Query prediction logs count
        res = client.table("prediction_logs").select("prediction_type", count="exact").execute()
        if res and hasattr(res, "count") and res.count is not None:
            total_count = res.count
        data_rows = res.data if res and hasattr(res, "data") else []
        for r in data_rows:
            pt = r.get("prediction_type", "")
            if pt in categories:
                categories[pt] += 1
            elif "crop" in pt:
                categories["crop_recommendation"] += 1
            elif "climate" in pt:
                categories["climate_risk"] += 1
            elif "yield" in pt:
                categories["yield_forecast"] += 1
            elif "irrigation" in pt:
                categories["irrigation_advisory"] += 1
            elif "market" in pt:
                categories["market_price"] += 1
    except Exception as e:
        logger.debug(f"Live stats count query skipped / fallback: {e}")

    # Real capability counts based on active codebase
    # 5 tabular models/heuristics (crop, climate, yield, irrigation, market) + 13 YOLO models
    return DashboardStatsResponse(
        total_predictions=total_count,
        active_models=18,
        covered_districts=57,  # 31 Telangana + 26 Andhra Pradesh
        supported_crops=24,    # Officially mapped crops
        categories=categories
    )

