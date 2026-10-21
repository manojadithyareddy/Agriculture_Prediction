from fastapi import APIRouter
from app.api.v1.predictions import router as predictions_router
from app.api.v1.detection import router as detection_router
from app.api.v1.chat import router as chat_router
from app.api.v1.agent import router as agent_router
from app.api.v1.history import router as history_router
from app.api.v1.health import router as health_router
from app.api.v1.weather import router as weather_router
from app.api.v1.rag import router as rag_router
from app.api.v1.market import router as market_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(predictions_router)
api_v1_router.include_router(detection_router)
api_v1_router.include_router(chat_router)
api_v1_router.include_router(agent_router)
api_v1_router.include_router(history_router)
api_v1_router.include_router(health_router)
api_v1_router.include_router(weather_router)
api_v1_router.include_router(rag_router)
api_v1_router.include_router(market_router)
