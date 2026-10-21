from app.ml.predict_crop import predict_crop
from app.ml.predict_climate_risk import predict_climate_risk
from app.ml.predict_yield import predict_yield
from app.ml.predict_irrigation import predict_irrigation
from app.ml.predict_market import predict_price

__all__ = [
    "predict_crop",
    "predict_climate_risk",
    "predict_yield",
    "predict_irrigation",
    "predict_price",
]
