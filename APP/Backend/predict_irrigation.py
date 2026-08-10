"""
predict_irrigation.py — V4 Advanced
Primary: loads best_irrigation_model.pkl if available.
Fallback: FAO-56 Penman-Monteith reference evapotranspiration (ET₀)
          multiplied by crop coefficient (Kc) and adjusted for:
          - Soil available water
          - Effective rainfall deduction
          - Growth stage Kc values (from FAO-56 Table 12)
This is the SAME formula used by FAO, ICAR, and most global irrigation
planning tools — highly accurate for field use.
"""
import joblib
import pandas as pd
import os
import math
from services.weather_service import get_full_snapshot
from services.soil_lookup import find_soil_profile

_DIR = os.path.dirname(__file__)

try:
    model         = joblib.load(os.path.join(_DIR, "..", "Pickles", "best_irrigation_model.pkl"))
    encoders      = joblib.load(os.path.join(_DIR, "..", "Pickles", "onehot_encoders.pkl"))
    FEATURE_ORDER = list(model.feature_names_in_)
    _model_source = "pickle"
except Exception:
    model, encoders, FEATURE_ORDER = None, None, []
    _model_source = "fallback"

GROWTH_ORDER = {"Initial": 1, "Development": 3, "Mid-season": 4, "Late-season": 2}
STATE_MAP    = {"telangana": 0, "andhra pradesh": 1}
RISK_LABEL_TO_SCORE = {"low": 30.0, "moderate": 34.0, "high": 38.0, "extreme": 41.0}

# ── FAO-56 Kc values [Initial, Development, Mid-season, Late-season] ─────────
# Source: FAO Irrigation and Drainage Paper 56, Table 12
_FAO_KC = {
    "rice":                   {"Initial": 1.05, "Development": 1.15, "Mid-season": 1.20, "Late-season": 0.90},
    "maize":                  {"Initial": 0.30, "Development": 0.70, "Mid-season": 1.15, "Late-season": 0.60},
    "cotton":                 {"Initial": 0.35, "Development": 0.70, "Mid-season": 1.15, "Late-season": 0.70},
    "banana":                 {"Initial": 0.50, "Development": 0.90, "Mid-season": 1.10, "Late-season": 1.00},
    "mango":                  {"Initial": 0.40, "Development": 0.70, "Mid-season": 1.00, "Late-season": 0.90},
    "grapes":                 {"Initial": 0.30, "Development": 0.70, "Mid-season": 0.85, "Late-season": 0.45},
    "orange":                 {"Initial": 0.65, "Development": 0.65, "Mid-season": 0.70, "Late-season": 0.65},
    "papaya":                 {"Initial": 0.60, "Development": 0.90, "Mid-season": 1.05, "Late-season": 0.90},
    "pomegranate":            {"Initial": 0.40, "Development": 0.70, "Mid-season": 0.95, "Late-season": 0.75},
    "tender coconut":         {"Initial": 0.85, "Development": 0.90, "Mid-season": 1.00, "Late-season": 1.00},
    "water melon":            {"Initial": 0.40, "Development": 0.75, "Mid-season": 1.00, "Late-season": 0.75},
    "karbuja(musk melon)":    {"Initial": 0.40, "Development": 0.75, "Mid-season": 1.00, "Late-season": 0.75},
    "beans":                  {"Initial": 0.35, "Development": 0.70, "Mid-season": 1.10, "Late-season": 0.30},
    "black gram dal(urd dal)":{"Initial": 0.35, "Development": 0.70, "Mid-season": 1.10, "Late-season": 0.50},
}
_DEFAULT_KC = {"Initial": 0.40, "Development": 0.75, "Mid-season": 1.00, "Late-season": 0.70}

# ── Root depths (m) per growth stage ─────────────────────────────────────────
_ROOT_DEPTH = {
    "Initial": 0.3, "Development": 0.5, "Mid-season": 0.7, "Late-season": 0.6
}


def _penman_monteith_et0(Tmax, Tmin, RH, Rs, u2, elevation=450.0) -> float:
    """
    FAO-56 Penman-Monteith ET₀ (mm/day).
    Tmax, Tmin in °C; RH in %; Rs in W/m²; u2 in m/s; elevation in m.
    """
    Tmean = (Tmax + Tmin) / 2.0
    Rs_MJ = Rs * 0.0864          # W/m² → MJ/m²/day

    # Psychrometric constant (kPa/°C)
    P = 101.3 * ((293 - 0.0065 * elevation) / 293) ** 5.26
    gamma = 0.000665 * P

    # Slope of vapour pressure curve (kPa/°C)
    delta = 4098 * (0.6108 * math.exp(17.27 * Tmean / (Tmean + 237.3))) / (Tmean + 237.3) ** 2

    # Saturation and actual vapour pressure
    es = (0.6108 * math.exp(17.27 * Tmax / (Tmax + 237.3)) +
          0.6108 * math.exp(17.27 * Tmin / (Tmin + 237.3))) / 2.0
    ea = es * (RH / 100.0)

    # Net radiation (approx)
    Rns = (1 - 0.23) * Rs_MJ
    sigma = 4.903e-9
    Rnl = sigma * ((Tmax + 273.16) ** 4 + (Tmin + 273.16) ** 4) / 2 * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * (Rs_MJ / (0.75 * Rs_MJ + 0.01)) - 0.35)
    Rn = Rns - Rnl

    G = 0  # Soil heat flux ≈ 0 for daily
    et0 = (0.408 * delta * (Rn - G) + gamma * (900 / (Tmean + 273)) * u2 * (es - ea)) / \
          (delta + gamma * (1 + 0.34 * u2))
    return max(0.0, round(et0, 2))


def predict_irrigation(location: str, crop: str, growth_stage: str = "Development") -> dict:
    w    = get_full_snapshot(location)
    soil = find_soil_profile(location)
    state = (soil["state"] or "telangana").lower()

    if model is not None:
        try:
            from predict_climate_risk import predict_climate_risk
            try:
                risk_out   = predict_climate_risk(location, crop)
                risk_label = risk_out["climate_risk"]
            except Exception:
                risk_label = "low"

            kc = _FAO_KC.get(crop.lower(), _DEFAULT_KC).get(growth_stage, 0.75)
            kc_band = ("low" if kc <= 0.5 else "medium" if kc <= 0.9 else "high" if kc <= 1.2 else "very_high")
            root_depth = _ROOT_DEPTH.get(growth_stage, 0.5)
            city = soil.get("city") or location
            climate_risk_score  = RISK_LABEL_TO_SCORE.get(risk_label, 33.8)
            climate_risk_binary = 0 if risk_label == "low" else 1

            row = {
                "state": STATE_MAP.get(state, 0),
                "temperature": w["temperature_2m"],
                "relative_humidity": w["relative_humidity_2m"],
                "rainfall": w["precipitation"],
                "wind_speed": w["wind_speed_10m"],
                "solar_radiation": w["shortwave_radiation"],
                "et0": w["et0_fao_evapotranspiration"],
                "climate_risk_score": climate_risk_score,
                "climate_risk": climate_risk_binary,
                "soil_ph": soil["soil_ph"],
                "organic_carbon": soil["organic_carbon"],
                "sand_percentage": soil["sand_percentage"],
                "silt_percentage": soil["silt_percentage"],
                "clay_percentage": soil["clay_percentage"],
                "cec": soil["cec"],
                "bulk_density": soil["bulk_density"],
                "field_capacity": soil["field_capacity"],
                "wilting_point": soil["wilting_point"],
                "available_water": soil["available_water"],
                "nitrogen": soil["nitrogen"],
                "growth_stage": GROWTH_ORDER.get(growth_stage, 3),
                "root_depth_m": root_depth,
            }
            df = pd.DataFrame([row])
            cat_input = pd.DataFrame([[city, crop, soil["soil_type"], kc_band]],
                                     columns=["city", "crop", "soil_type", "kc_band"])
            for col in ["city", "crop", "soil_type", "kc_band"]:
                enc = encoders[col]
                enc_arr = enc.transform(cat_input[[col]])
                enc_df  = pd.DataFrame(enc_arr, columns=enc.get_feature_names_out([col]))
                df = pd.concat([df.reset_index(drop=True), enc_df], axis=1)
            df = df.reindex(columns=FEATURE_ORDER, fill_value=0)
            prediction = float(model.predict(df)[0])
            return {
                "location": w["location"], "date": w["date"],
                "crop": crop, "growth_stage": growth_stage,
                "predicted_water_requirement_mm_per_day": round(prediction, 2),
                "model_source": "pickle",
            }
        except Exception:
            pass  # fall through to FAO fallback

    # ── FAO-56 Penman-Monteith fallback ──────────────────────────────────────
    # Compute accurate ET₀ from weather data
    et0 = _penman_monteith_et0(
        Tmax=w["temperature_2m_max"],
        Tmin=w["temperature_2m_min"],
        RH=w["relative_humidity_2m"],
        Rs=w["shortwave_radiation"],
        u2=w["wind_speed_10m"],
        elevation=w.get("elevation", 450.0),
    )

    # Crop coefficient for this growth stage
    kc_table = _FAO_KC.get(crop.lower(), _DEFAULT_KC)
    kc = kc_table.get(growth_stage, 0.75)

    # Effective rainfall deduction (≈80% of daily rainfall is plant-available)
    rain_mm_day = w["precipitation"] * 0.8

    # ETc = ET₀ × Kc  (crop evapotranspiration)
    ETc = et0 * kc

    # Net irrigation = ETc - effective rainfall (min 0)
    net_irrigation = max(0.0, ETc - rain_mm_day)

    # Soil available water correction (if soil holds more water, less irrigation needed)
    fc  = soil.get("field_capacity", 0.30)
    wp  = soil.get("wilting_point", 0.14)
    aw  = fc - wp  # available water capacity
    rd  = _ROOT_DEPTH.get(growth_stage, 0.5)
    # Total readily available water in root zone (mm)
    RAW = aw * rd * 1000 * 0.5  # 50% depletion threshold
    # If RAW is large (good soil), slightly reduce irrigation recommendation
    soil_correction = max(0.85, 1.0 - (RAW / 150.0) * 0.1)

    final_req = round(net_irrigation * soil_correction, 2)

    return {
        "location": w["location"], "date": w["date"],
        "crop": crop, "growth_stage": growth_stage,
        "predicted_water_requirement_mm_per_day": final_req,
        "model_source": "fao56_penman_monteith",
        "details": {
            "ET0_mm_day":    et0,
            "Kc":            kc,
            "ETc_mm_day":    round(ETc, 2),
            "effective_rain": round(rain_mm_day, 2),
            "net_irrigation": round(net_irrigation, 2),
        },
    }
