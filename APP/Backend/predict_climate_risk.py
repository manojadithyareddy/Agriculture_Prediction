import joblib
import pandas as pd
import os
from services.weather_service import get_full_snapshot
from services.soil_lookup import find_soil_profile
from services.date_utils import climate_season

_DIR = os.path.dirname(__file__)
model = joblib.load(os.path.join(_DIR, "..", "Pickles", "climate_risk_model.pkl"))
encoders = joblib.load(os.path.join(_DIR, "..", "Pickles", "encoders.pkl"))

FEATURE_ORDER = list(model.feature_names_in_)


def _heat_index(temp_c: float, rh: float) -> float:
    """Simplified Steadman heat index (°C in, °C out). Requires RH in % (0-100)."""
    t_f = temp_c * 9 / 5 + 32
    hi_f = (
        -42.379 + 2.04901523 * t_f + 10.14333127 * rh
        - 0.22475541 * t_f * rh - 0.00683783 * t_f**2
        - 0.05481717 * rh**2 + 0.00122874 * t_f**2 * rh
        + 0.00085282 * t_f * rh**2 - 0.00000199 * t_f**2 * rh**2
    )
    return (hi_f - 32) * 5 / 9 if t_f >= 80 else temp_c


def _gdd(tmax: float, tmin: float, base: float = 10.0) -> float:
    return max(((tmax + tmin) / 2) - base, 0)


def predict_climate_risk(location: str, crop: str = "rice") -> dict:
    w = get_full_snapshot(location)
    soil = find_soil_profile(location)
    season = climate_season()

    row = {
        "latitude": w["lat"], "longitude": w["lon"],
        "temperature_2m": w["temperature_2m"],
        "relative_humidity_2m": w["relative_humidity_2m"],
        "precipitation": w["precipitation"],
        "surface_pressure": w["surface_pressure"],
        "cloud_cover": w["cloud_cover"],
        "wind_speed_10m": w["wind_speed_10m"],
        "wind_direction_10m": w["wind_direction_10m"],
        "wind_gusts_10m": w["wind_gusts_10m"],
        "shortwave_radiation": w["shortwave_radiation"],
        "et0_fao_evapotranspiration": w["et0_fao_evapotranspiration"],
        "Soil_Moisture": w.get("soil_moisture", 0),
        "Soil_Temperature": w.get("soil_temperature", 0),
        "Soil_pH": soil.get("soil_ph", 7.0),
        "Organic_Carbon": soil.get("organic_carbon", 0.5),
        "Clay": soil.get("clay_percentage", 33),
        "Sand": soil.get("sand_percentage", 33),
        "Silt": soil.get("silt_percentage", 34),
        "Elevation": w.get("elevation", 0),
        "Heat_Index": _heat_index(w["temperature_2m"], w["relative_humidity_2m"]),
        "Rainfall_Last_7_Days": w["Rainfall_Last_7_Days"],
        "Rainfall_Last_30_Days": w["Rainfall_Last_30_Days"],
        "Consecutive_Dry_Days": w["Consecutive_Dry_Days"],
        "Growing_Degree_Days": _gdd(w["temperature_2m_max"], w["temperature_2m_min"]),
    }
    df = pd.DataFrame([row])

    city_key = (soil.get("city") or location).lower()
    state_key = (soil.get("state") or "telangana").lower()
    
    for col_name, enc, value in [
        ("city", encoders["city"], city_key),
        ("state", encoders["state"], state_key),
        ("Crop", encoders["Crop"], crop.lower()),
        ("Season", encoders["Season"], season),
    ]:
        feat_names = enc.get_feature_names_out([col_name])
        try:
            transform_result = enc.transform(pd.DataFrame([[value]], columns=[col_name]))
            enc_arr = transform_result.toarray() if hasattr(transform_result, 'toarray') else transform_result
        except ValueError:
            import numpy as _np
            enc_arr = _np.zeros((1, len(feat_names)))

        enc_df = pd.DataFrame(enc_arr, columns=feat_names)
        df = pd.concat([df.reset_index(drop=True), enc_df], axis=1)

    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    prediction = model.predict(df)[0]
    raw_proba = model.predict_proba(df)[0]
    proba = {cls: round(float(p), 3) for cls, p in zip(model.classes_, raw_proba)}

    # Dynamic Environmental & Crop Sensitivity Analysis
    temp = w["temperature_2m"]
    rh = w["relative_humidity_2m"]
    precip = w["precipitation"]
    wind = w["wind_speed_10m"]
    heat_idx = row["Heat_Index"]
    rain_7d = w["Rainfall_Last_7_Days"]
    dry_days = w["Consecutive_Dry_Days"]

    temp_stress = 0.0
    if temp > 35 or heat_idx > 38:
        temp_stress = min(40, (max(temp, heat_idx) - 34) * 4.5)
    elif temp < 15:
        temp_stress = min(35, (15 - temp) * 4.0)

    water_stress = 0.0
    if precip > 10 or rain_7d > 60:
        water_stress = min(45, (max(precip, rain_7d / 4) - 8) * 3.5)
    elif dry_days > 10:
        water_stress = min(35, (dry_days - 8) * 3.0)

    crop_lower = crop.lower()
    crop_mult = 1.0
    if any(c in crop_lower for c in ["orange", "grapes", "banana", "papaya", "pomegranate"]):
        if rh > 75 or temp > 34 or precip > 8:
            crop_mult = 1.35
    elif "cotton" in crop_lower:
        if precip > 10 or rain_7d > 50:
            crop_mult = 1.4
    elif "maize" in crop_lower:
        if dry_days > 8:
            crop_mult = 1.3

    env_score = min(98.0, (temp_stress + water_stress) * crop_mult)

    ml_score = (
        float(proba.get("low", 0.7)) * 18.0 +
        float(proba.get("moderate", 0.2)) * 48.0 +
        float(proba.get("high", 0.05)) * 76.0 +
        float(proba.get("extreme", 0.05)) * 95.0
    )

    final_score = round(min(99.0, max(8.0, ml_score * 0.45 + env_score * 0.55)), 1)

    if final_score < 32:
        final_risk = "low"
    elif final_score < 62:
        final_risk = "moderate"
    elif final_score < 82:
        final_risk = "high"
    else:
        final_risk = "extreme"

    res = {
        "location": w.get("location", location), 
        "date": w.get("date"), 
        "crop": crop, 
        "season": season,
        "climate_risk": final_risk, 
        "risk_score": final_score,
        "probabilities": proba,
        "weather_details": {
            "temperature": round(temp, 1),
            "humidity": round(rh, 1),
            "rainfall": round(precip, 1),
            "wind_speed": round(wind, 1),
            "cloud_cover": round(w.get("cloud_cover", 40), 1),
            "solar_rad": round(w.get("shortwave_radiation", 18), 1),
            "heat_index": round(heat_idx, 1),
            "rainfall_7d": round(rain_7d, 1),
            "consecutive_dry_days": dry_days
        }
    }
    try:
        from database import save_prediction_to_supabase
        save_prediction_to_supabase(
            prediction_type="climate_risk",
            location=res["location"],
            crop=crop,
            inputs={"location": location, "crop": crop, "season": season},
            results={"climate_risk": final_risk, "risk_score": final_score, "probabilities": proba},
            model_source="random_forest"
        )
    except Exception:
        pass
    return res