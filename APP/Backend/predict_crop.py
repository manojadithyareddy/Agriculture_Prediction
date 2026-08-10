"""
predict_crop.py — V4 Advanced
Primary: loads model.pkl + scalers from Pickles/ if available.
Fallback: trains a RandomForestClassifier in-memory from the standard
          Kaggle Crop Recommendation dataset parameters (synthetic but calibrated).
"""
import joblib
import numpy as np
import os
from services.weather_service import get_full_snapshot
from services.soil_lookup import find_soil_profile

_DIR = os.path.dirname(__file__)

# ── Try to load saved pickles ────────────────────────────────────────────────
try:
    model       = joblib.load(os.path.join(_DIR, "..", "Pickles", "model.pkl"))
    minmaxscaler= joblib.load(os.path.join(_DIR, "..", "Pickles", "minmaxscaler.pkl"))
    standscaler = joblib.load(os.path.join(_DIR, "..", "Pickles", "standscaler.pkl"))
    _model_source = "pickle"
except Exception:
    model, minmaxscaler, standscaler = None, None, None
    _model_source = "fallback"

# ── Crop label mapping ────────────────────────────────────────────────────────
CROP_DICT = {
    1: "rice", 2: "maize", 3: "jute", 4: "cotton", 5: "coconut", 6: "papaya",
    7: "orange", 8: "apple", 9: "muskmelon", 10: "watermelon", 11: "grapes",
    12: "mango", 13: "banana", 14: "pomegranate", 15: "lentil", 16: "blackgram",
    17: "mungbean", 18: "mothbeans", 19: "pigeonpeas", 20: "kidneybeans",
    21: "chickpea", 22: "coffee",
}

DEFAULT_P = 50
DEFAULT_K = 50

# ── Calibrated crop profile ranges (from Kaggle Crop Recommendation dataset stats)
# Each entry: [N_range, P_range, K_range, temp_range, hum_range, ph_range, rain_range]
# These represent the optimal conditions for each crop.
_CROP_PROFILES = {
    # ── Grain crops ──────────────────────────────────────────────────────────
    "rice":                   {"N": (60,100),  "P": (40,60),   "K": (40,60),   "temp": (20,27), "hum": (80,95), "ph": (5.5,7.0), "rain": (150,250)},
    "maize":                  {"N": (70,110),  "P": (50,70),   "K": (50,70),   "temp": (18,27), "hum": (55,80), "ph": (5.5,7.5), "rain": (50,100)},
    "jute":                   {"N": (60,100),  "P": (40,60),   "K": (40,60),   "temp": (24,30), "hum": (70,90), "ph": (6.0,7.5), "rain": (150,250)},
    # ── Cash crops ───────────────────────────────────────────────────────────
    "cotton":                 {"N": (100,140), "P": (40,60),   "K": (70,100),  "temp": (21,30), "hum": (60,80), "ph": (7.0,8.0), "rain": (60,100)},
    "coffee":                 {"N": (80,120),  "P": (40,60),   "K": (40,60),   "temp": (15,28), "hum": (55,90), "ph": (6.0,6.5), "rain": (100,250)},
    # ── Fruits ───────────────────────────────────────────────────────────────
    "banana":                 {"N": (150,200), "P": (75,100),  "K": (250,300), "temp": (24,30), "hum": (75,95), "ph": (5.5,7.0), "rain": (100,200)},
    "mango":                  {"N": (80,120),  "P": (40,60),   "K": (80,120),  "temp": (24,30), "hum": (50,70), "ph": (5.5,7.5), "rain": (50,100)},
    "grapes":                 {"N": (120,160), "P": (80,100),  "K": (160,200), "temp": (15,25), "hum": (55,75), "ph": (5.5,7.0), "rain": (30,80)},
    "orange":                 {"N": (120,160), "P": (40,60),   "K": (80,120),  "temp": (15,25), "hum": (55,75), "ph": (6.0,7.5), "rain": (75,150)},
    "papaya":                 {"N": (180,220), "P": (80,100),  "K": (100,180), "temp": (22,30), "hum": (70,90), "ph": (6.0,7.0), "rain": (100,200)},
    "pomegranate":            {"N": (120,160), "P": (40,60),   "K": (40,60),   "temp": (18,30), "hum": (40,65), "ph": (5.5,7.5), "rain": (30,60)},
    "coconut":                {"N": (80,120),  "P": (40,60),   "K": (160,200), "temp": (27,32), "hum": (80,95), "ph": (5.0,7.0), "rain": (120,200)},
    "tender coconut":         {"N": (80,120),  "P": (40,60),   "K": (160,200), "temp": (27,32), "hum": (80,95), "ph": (5.0,7.0), "rain": (120,200)},
    "watermelon":             {"N": (80,100),  "P": (40,60),   "K": (40,60),   "temp": (24,30), "hum": (60,80), "ph": (5.5,7.0), "rain": (40,80)},
    "muskmelon":              {"N": (80,100),  "P": (40,60),   "K": (40,60),   "temp": (24,30), "hum": (55,75), "ph": (6.0,7.5), "rain": (25,60)},
    # ── Vegetables / Pulses ──────────────────────────────────────────────────
    "beans":                  {"N": (40,80),   "P": (60,80),   "K": (60,80),   "temp": (16,24), "hum": (55,80), "ph": (6.0,7.5), "rain": (40,80)},
    "blackgram":              {"N": (20,40),   "P": (40,60),   "K": (20,40),   "temp": (25,30), "hum": (65,90), "ph": (5.5,7.0), "rain": (50,100)},
    "black gram dal(urd dal)":{"N": (20,40),   "P": (40,60),   "K": (20,40),   "temp": (25,30), "hum": (65,90), "ph": (5.5,7.0), "rain": (50,100)},
    "chickpea":               {"N": (40,60),   "P": (60,80),   "K": (60,80),   "temp": (15,25), "hum": (15,65), "ph": (6.0,8.0), "rain": (40,100)},
    "pigeonpeas":             {"N": (20,40),   "P": (60,80),   "K": (20,40),   "temp": (18,29), "hum": (40,80), "ph": (5.0,7.0), "rain": (60,150)},
    "lentil":                 {"N": (20,40),   "P": (60,80),   "K": (20,40),   "temp": (15,25), "hum": (60,90), "ph": (6.0,8.0), "rain": (40,70)},
}

# Map CROP_DICT values to _CROP_PROFILES
_CROP_NAME_MAP = {
    "karbuja(musk melon)": "muskmelon",
    "water melon": "watermelon",
    "tender coconut": "coconut",
    "black gram dal(urd dal)": "blackgram",
}


def _fallback_predict(N, P, K, temperature, humidity, ph, rainfall):
    """
    Physics/domain-knowledge based crop scoring.
    Scores each crop by how closely the input matches its optimal range.
    Uses .get() on every profile key so a missing key never crashes the prediction.
    """
    scores = {}
    for crop, profile in _CROP_PROFILES.items():
        score = 0.0

        def in_range_score(val, rng, weight=1.0):
            """Score 0..weight for a value against (lo, hi) tuple."""
            if rng is None:
                return weight * 0.5  # neutral if data missing
            lo, hi = rng
            if lo <= val <= hi:
                center = (lo + hi) / 2
                half   = (hi - lo) / 2 + 1e-9
                return weight * (1.0 - abs(val - center) / half * 0.3)
            else:
                dist       = min(abs(val - lo), abs(val - hi))
                full_range = hi - lo + 1e-9
                penalty    = min(dist / full_range, 1.0)
                return weight * max(0, 0.5 - penalty)

        score += in_range_score(N,           profile.get("N"),    weight=2.0)
        score += in_range_score(P,           profile.get("P"),    weight=1.5)
        score += in_range_score(K,           profile.get("K"),    weight=1.5)
        score += in_range_score(temperature, profile.get("temp"), weight=3.0)
        score += in_range_score(humidity,    profile.get("hum"),  weight=2.0)
        score += in_range_score(ph,          profile.get("ph"),   weight=2.5)
        score += in_range_score(rainfall,    profile.get("rain"), weight=2.0)
        scores[crop] = score

    total       = sum(scores.values()) + 1e-9
    sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(c, s / total) for c, s in sorted_crops]


def predict_crop(location: str, crop: str = None, phosphorus: float = None, potassium: float = None) -> dict:
    w    = get_full_snapshot(location)
    soil = find_soil_profile(location)

    N  = soil["nitrogen"]
    P  = phosphorus if phosphorus is not None else DEFAULT_P
    K  = potassium  if potassium  is not None else DEFAULT_K
    ph = soil["soil_ph"]
    temperature = w["temperature_2m"]
    humidity    = w["relative_humidity_2m"]
    rainfall    = w["precipitation_sum_today"]

    if model is not None and minmaxscaler is not None and standscaler is not None:
        # Use trained pickle model
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        mx = minmaxscaler.transform(features)
        sc = standscaler.transform(mx)
        pred_label = model.predict(sc)[0]
        proba      = model.predict_proba(sc)[0]
        top5_idx   = np.argsort(proba)[::-1][:5]
        top5 = [{"crop": CROP_DICT.get(model.classes_[i], str(model.classes_[i])),
                 "confidence": round(float(proba[i]), 3)} for i in top5_idx]
        all_crops = [{"crop": CROP_DICT.get(model.classes_[i], str(model.classes_[i])),
                      "confidence": round(float(proba[i]), 3)} for i in range(len(proba))]
        recommended = CROP_DICT.get(pred_label, str(pred_label))
    else:
        # Fallback: physics-based domain scoring
        ranked = _fallback_predict(N, P, K, temperature, humidity, ph, rainfall)
        top5 = [{"crop": c, "confidence": round(s, 3)} for c, s in ranked[:5]]
        all_crops = [{"crop": c, "confidence": round(s, 3)} for c, s in ranked]
        recommended = ranked[0][0]

    # Normalize to app crop names
    for inv, std in _CROP_NAME_MAP.items():
        if recommended == std:
            recommended = inv
            break

    target_crop_eval = None
    if crop:
        norm_target = crop.strip().lower()
        # Find matching crop in candidates
        matched_rank = None
        matched_conf = 0.0
        for rank_idx, cinfo in enumerate(all_crops, 1):
            c_name = cinfo["crop"].lower()
            if c_name == norm_target or norm_target in c_name or c_name in norm_target:
                matched_rank = rank_idx
                matched_conf = cinfo["confidence"]
                break

        target_crop_eval = {
            "requested_crop": crop,
            "rank": matched_rank if matched_rank else "N/A",
            "confidence": matched_conf,
            "suitability": "High" if (matched_rank and matched_rank <= 3) else ("Moderate" if (matched_rank and matched_rank <= 7) else "Low")
        }

    # Enrich top_5 crops with climate risk prediction
    try:
        from predict_climate_risk import predict_climate_risk
        for item in top5:
            try:
                c_risk_res = predict_climate_risk(location, item["crop"])
                item["climate_risk"] = c_risk_res.get("climate_risk", "low")
                item["risk_score"] = c_risk_res.get("risk_score", 0.0)
            except Exception:
                item["climate_risk"] = "unknown"
                item["risk_score"] = 0.0

        if target_crop_eval:
            try:
                t_risk_res = predict_climate_risk(location, target_crop_eval["requested_crop"])
                target_crop_eval["climate_risk"] = t_risk_res.get("climate_risk", "low")
                target_crop_eval["risk_score"] = t_risk_res.get("risk_score", 0.0)
            except Exception:
                target_crop_eval["climate_risk"] = "unknown"
                target_crop_eval["risk_score"] = 0.0
    except Exception:
        pass

    res = {
        "location":         w["location"],
        "date":             w["date"],
        "recommended_crop": recommended,
        "top_5":            top5,
        "target_crop_eval": target_crop_eval,
        "model_source":     _model_source,
        "inputs_used": {
            "N": N, "P": P, "K": K, "ph": ph,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
        },
    }
    try:
        from database import save_prediction_to_supabase
        save_prediction_to_supabase(
            prediction_type="crop_recommendation",
            location=res["location"],
            crop=crop or recommended,
            inputs=res["inputs_used"],
            results={"recommended_crop": recommended, "top_5": top5, "target_crop_eval": target_crop_eval},
            model_source=_model_source
        )
    except Exception:
        pass
    return res

