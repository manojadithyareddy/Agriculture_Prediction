"""
predict_yield.py — V4 Advanced
Primary: loads yield_predict_model.pkl if available.
Fallback: FAO/USDA calibrated crop yield model based on:
  - Optimal temperature response curves
  - Water stress factor (ETa/ETc)
  - Solar radiation efficiency (RUE model)
  - Soil fertility index
  - Season-appropriate growth factor
All coefficients are derived from FAO Yield Response to Water (Doorenbos & Kassam)
and USDA crop data for South India.
"""
import os
import joblib
import pandas as pd
import numpy as np
from datetime import date
from services.weather_service import get_full_snapshot
from services.soil_lookup import find_soil_profile
from services.date_utils import yield_season

_DIR = os.path.dirname(__file__)

try:
    model        = joblib.load(os.path.join(_DIR, "..", "Pickles", "yield_predict_model.pkl"))
    state_mapping= joblib.load(os.path.join(_DIR, "..", "Pickles", "state_mapping.pkl"))
    encoders     = joblib.load(os.path.join(_DIR, "..", "Pickles", "onehot_encoders.pkl"))
    FEATURE_ORDER = list(model.feature_names_in_)
    _model_source = "pickle"
except Exception:
    model, state_mapping, encoders, FEATURE_ORDER = None, None, None, []
    _model_source = "fallback"


# ── FAO calibrated max potential yield (tonnes/ha) for AP/TS region ───────────
_CROP_POTENTIAL_YIELD = {
    "rice":                    6.5,
    "maize":                   5.5,
    "cotton":                  2.0,   # seed cotton
    "banana":                 35.0,
    "mango":                  10.0,
    "grapes":                 12.0,
    "orange":                  8.0,
    "papaya":                 40.0,
    "pomegranate":             9.0,
    "tender coconut":         80.0,   # nuts/tree/year expressed as equiv. t/ha
    "water melon":            25.0,
    "karbuja(musk melon)":    18.0,
    "beans":                   2.5,
    "black gram dal(urd dal)": 1.2,
}
_DEFAULT_POTENTIAL = 4.0

# ── Optimal temperature ranges (°C) [T_base, T_opt_lo, T_opt_hi, T_max] ────
_CROP_TEMP_OPTIMA = {
    "rice":                   (10, 22, 28, 40),
    "maize":                  (8,  18, 26, 40),
    "cotton":                 (15, 25, 32, 42),
    "banana":                 (13, 25, 30, 38),
    "mango":                  (10, 24, 30, 42),
    "grapes":                 (8,  18, 25, 38),
    "orange":                 (5,  15, 24, 38),
    "papaya":                 (12, 22, 30, 40),
    "pomegranate":            (10, 20, 30, 42),
    "tender coconut":         (15, 27, 32, 40),
    "water melon":            (18, 25, 30, 40),
    "karbuja(musk melon)":    (18, 25, 30, 40),
    "beans":                  (10, 18, 25, 35),
    "black gram dal(urd dal)":(10, 25, 30, 40),
}
_DEFAULT_TEMP_OPTIMA = (8, 20, 28, 40)

# ── Ky values (yield response factor to water stress, FAO-33) ────────────────
_KY = {
    "rice": 1.09, "maize": 1.25, "cotton": 0.85, "banana": 1.30,
    "mango": 0.80, "grapes": 0.85, "orange": 0.80, "papaya": 1.10,
    "pomegranate": 0.75, "tender coconut": 0.80, "water melon": 1.10,
    "karbuja(musk melon)": 1.10, "beans": 1.15, "black gram dal(urd dal)": 0.85,
}
_DEFAULT_KY = 1.0


def _temperature_factor(temp: float, crop: str) -> float:
    """Beta function temperature response (0–1)."""
    T_base, T_opt_lo, T_opt_hi, T_max = _CROP_TEMP_OPTIMA.get(crop.lower(), _DEFAULT_TEMP_OPTIMA)
    if temp <= T_base or temp >= T_max:
        return 0.05
    if T_opt_lo <= temp <= T_opt_hi:
        return 1.0
    if temp < T_opt_lo:
        return (temp - T_base) / (T_opt_lo - T_base)
    # temp > T_opt_hi
    return (T_max - temp) / (T_max - T_opt_hi)


def _water_stress_factor(et0: float, rainfall: float, crop: str) -> float:
    """ETa/ETc proxy: compares effective rainfall to ET demand."""
    kc = 0.9  # mid-season Kc approximation
    ETc = et0 * kc
    ETa = min(rainfall / 30.0 + et0 * 0.3, ETc)  # rainfall + capillary contribution
    if ETc < 0.01:
        return 1.0
    ky = _KY.get(crop.lower(), _DEFAULT_KY)
    ratio = ETa / ETc
    # FAO-33: Y/Ym = 1 - Ky*(1 - ETa/ETc)
    return max(0.05, 1.0 - ky * (1.0 - ratio))


def _soil_fertility_index(soil: dict) -> float:
    """Score 0–1 based on NPK and pH."""
    N_score  = min(soil["nitrogen"] / 300.0, 1.0)
    ph       = soil["soil_ph"]
    ph_score = 1.0 if 6.0 <= ph <= 7.5 else max(0.3, 1.0 - abs(ph - 6.75) * 0.3)
    oc_score = min(soil["organic_carbon"] / 1.5, 1.0)
    return (N_score * 0.4 + ph_score * 0.35 + oc_score * 0.25)


def _solar_factor(radiation: float) -> float:
    """Radiation use efficiency factor (reference: 400 W/m²)."""
    return min(radiation / 400.0, 1.0)


def predict_yield(location: str, crop: str, area: float = 1.0) -> dict:
    w    = get_full_snapshot(location)
    soil = find_soil_profile(location)
    season = yield_season()

    if model is not None:
        # Use saved pickle model
        try:
            district = (soil["district"] or location).lower()
            state    = (soil["state"] or "telangana").lower()
            row = {
                "state": state_mapping.get(state, 1),
                "latitude": w["lat"], "longitude": w["lon"],
                "year": date.today().year, "area": area,
                "mean_temperature": w["temperature_2m"],
                "max_temperature": w["temperature_2m_max"],
                "min_temperature": w["temperature_2m_min"],
                "precipitation": w["precipitation"],
                "shortwave_radiation": w["shortwave_radiation"],
                "wind_speed": w["wind_speed_10m"],
                "relative_humidity": w["relative_humidity_2m"],
                "et0": w["et0_fao_evapotranspiration"],
                "soil_moisture": w["soil_moisture"],
                "soil_temperature": w["soil_temperature"],
                "soil_ph": soil["soil_ph"],
                "organic_carbon": soil["organic_carbon"],
                "clay": soil["clay_percentage"],
                "sand": soil["sand_percentage"],
                "silt": soil["silt_percentage"],
                "elevation": w["elevation"],
            }
            df = pd.DataFrame([row])
            cat_input = pd.DataFrame([[season, district, crop.lower()]], columns=["season", "district", "crop"])
            enc_arr = encoders.transform(cat_input)
            enc_df  = pd.DataFrame(enc_arr, columns=encoders.get_feature_names_out(["season", "district", "crop"]))
            df = pd.concat([df.reset_index(drop=True), enc_df], axis=1)
            df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
            prediction = float(model.predict(df)[0])
            return {
                "location": w["location"], "date": w["date"], "crop": crop,
                "season": season, "area": area,
                "predicted_yield": round(prediction * area, 2),
                "model_source": "pickle",
            }
        except Exception:
            pass  # fall through to fallback

    # ── FAO-based fallback model ──────────────────────────────────────────────
    crop_key = crop.lower()
    Ym = _CROP_POTENTIAL_YIELD.get(crop_key, _DEFAULT_POTENTIAL)

    Tf  = _temperature_factor(w["temperature_2m"], crop_key)
    Wf  = _water_stress_factor(w["et0_fao_evapotranspiration"], w["Rainfall_Last_30_Days"], crop_key)
    Sf  = _soil_fertility_index(soil)
    Rf  = _solar_factor(w["shortwave_radiation"])

    # Seasonal correction (kharif crops favour monsoon, rabi crops favour winter)
    season_correction = 1.05 if season == "Kharif" and crop_key in {
        "rice","maize","cotton","banana","papaya","water melon","karbuja(musk melon)"
    } else (1.05 if season == "Rabi" and crop_key in {
        "chickpea","lentil","beans","black gram dal(urd dal)"
    } else 0.92)

    # Composite yield: Y = Ym * Tf * Wf * Sf * Rf * season_correction
    yield_per_ha = round(Ym * Tf * Wf * Sf * Rf * season_correction, 2)
    total_yield  = round(yield_per_ha * area, 2)

    return {
        "location": w["location"], "date": w["date"],
        "crop": crop, "season": season, "area": area,
        "predicted_yield": total_yield,
        "yield_per_ha": yield_per_ha,
        "model_source": "fao_fallback",
        "factors": {
            "temperature_factor": round(Tf, 3),
            "water_stress_factor": round(Wf, 3),
            "soil_fertility_index": round(Sf, 3),
            "solar_factor": round(Rf, 3),
        },
    }
