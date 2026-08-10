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
        "Soil_Moisture": w.get("soil_moisture", 0), # Added .get() for safety
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

    # Safely fetch dictionary values using .get() to prevent KeyErrors
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
            # OHE was fitted with a named DataFrame, so pass one to avoid UserWarning
            transform_result = enc.transform(pd.DataFrame([[value]], columns=[col_name]))
            enc_arr = transform_result.toarray() if hasattr(transform_result, 'toarray') else transform_result
        except ValueError:
            # Unknown category — fill zeros so the model can still run
            import numpy as _np
            enc_arr = _np.zeros((1, len(feat_names)))

        enc_df = pd.DataFrame(enc_arr, columns=feat_names)
        df = pd.concat([df.reset_index(drop=True), enc_df], axis=1)

    df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
    prediction = model.predict(df)[0]
    proba = dict(zip(model.classes_, model.predict_proba(df)[0].round(3)))

    return {
        "location": w.get("location", location), 
        "date": w.get("date"), 
        "crop": crop, 
        "season": season,
        "climate_risk": prediction, 
        "probabilities": proba,
    }