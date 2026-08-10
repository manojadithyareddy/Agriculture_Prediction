import os
# Fix for OpenBLAS Memory allocation error
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OPENBLAS_CORETYPE"] = "HASWELL"

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import LocationOnlyInput, CropLocationInput, YieldInput, IrrigationInput, MarketInput

from predict_crop import predict_crop
from predict_climate_risk import predict_climate_risk
from predict_yield import predict_yield
from predict_irrigation import predict_irrigation
from predict_market import predict_price

app = FastAPI(title="Agriculture Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict/crop-recommendation")
def crop_recommendation(data: LocationOnlyInput):
    try:
        return predict_crop(data.location, crop=data.crop, phosphorus=data.phosphorus, potassium=data.potassium)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/climate-risk")
def climate_risk(data: CropLocationInput):
    try:
        return predict_climate_risk(data.location, data.crop)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/yield")
def yield_prediction(data: YieldInput):
    try:
        return predict_yield(data.location, data.crop, data.area)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/irrigation")
def irrigation_prediction(data: IrrigationInput):
    try:
        return predict_irrigation(data.location, data.crop, data.growth_stage)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/market-price")
def market_price(data: MarketInput):
    try:
        return predict_price(data.location, data.commodity, data.arrival_quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def root():
    return {"status": "ok", "endpoints": [
        "/predict/crop-recommendation", "/predict/climate-risk",
        "/predict/yield", "/predict/irrigation", "/predict/market-price",
    ]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
