"""
predict_market.py — V4 Advanced
Primary: loads market_price_rf_model.pkl if available.
Fallback: Calibrated seasonal price model based on:
  - APMC / e-NAM historical price ranges for AP & Telangana
  - Seasonal demand multipliers (Q1-Q4 patterns)
  - Arrival quantity elasticity (more supply → lower price)
  - District demand tier (urban premium for closer mandis)
All base prices sourced from Agmarknet / NHB data (2022-2024 averages).
"""
import joblib
import pandas as pd
import os
import math
from datetime import date
from services.soil_lookup import find_soil_profile

_DIR = os.path.dirname(__file__)

_PICKLE_DIR_CANDIDATES = [
    os.path.join(_DIR, "..", "Pickles"),
    os.path.join(_DIR, "..", "pickles"),
]

def _load_model():
    for base_dir in _PICKLE_DIR_CANDIDATES:
        candidate = os.path.join(base_dir, "market_price_rf_model.pkl")
        if os.path.exists(candidate):
            return joblib.load(candidate)
    return None

try:
    model = _load_model()
    _model_source = "pickle"
except Exception:
    model = None
    _model_source = "fallback"

# ── Label mappings (unchanged from original) ─────────────────────────────────
COMMODITY_MAPPING = {
    "cotton": 14, "black gram dal(urd dal)": 13, "beans": 12, "pomegranate": 11,
    "grapes": 10, "rice": 9, "banana": 8, "orange": 7, "mango": 6,
    "tender coconut": 5, "maize": 4, "papaya": 3, "karbuja(musk melon)": 2, "water melon": 1,
    "muskmelon": 2, "watermelon": 1, "coconut": 5, "blackgram": 13,
    "jute": 15, "coffee": 16, "chickpea": 17, "pigeonpeas": 18, "lentil": 19,
    "mungbean": 20, "mothbeans": 21, "kidneybeans": 22, "apple": 23
}
STATE_MAPPING    = {"telangana": 1, "andhra pradesh": 0}
DISTRICT_MAPPING = {
    "guntur": 46, "rajanna siricilla": 45, "nalgonda": 44, "spsr nellore": 43,
    "peddapalli": 42, "hanumakonda": 41, "chittor": 40, "alluri sitharama raju": 39,
    "bhupalapally": 38, "mancherial": 37, "mulugu": 36, "kurnool": 35, "asifabad": 34,
    "karimnagar": 33, "khammam": 32, "mahabubabad": 31, "warangal": 30, "nagarkurnool": 29,
    "adilabad": 28, "ntr": 27, "nirmal": 26, "bhadradri kothagudem": 25, "suryapet": 24,
    "siddipet": 23, "vikarabad": 22, "jogulamba gadwal": 21, "east godavari": 20,
    "nandyal": 19, "sri sathya sai": 18, "dr.b.r.a.konaseema": 17, "ranga reddy": 16,
    "jagtial": 15, "eluru": 14, "mahbubnagar": 13, "ysr kadapa": 12, "wanaparthy": 11,
    "sangareddy": 10, "bapatla": 9, "ananthapuramu": 8, "medak": 7, "jangaon": 6,
    "kamareddy": 5, "medchal malkajgiri": 4, "nizamabad": 3, "tirupathi": 2, "vijayanagaram": 1,
}

# Alias resolution mapping to standard keys
_ALIAS_MAP = {
    "muskmelon": "karbuja(musk melon)",
    "musk melon": "karbuja(musk melon)",
    "karbuja": "karbuja(musk melon)",
    "watermelon": "water melon",
    "water melon": "water melon",
    "coconut": "tender coconut",
    "tender coconut": "tender coconut",
    "blackgram": "black gram dal(urd dal)",
    "urd dal": "black gram dal(urd dal)",
    "black gram": "black gram dal(urd dal)",
    "pigeonpeas": "pigeonpeas",
    "mungbean": "mungbean",
    "mothbeans": "mothbeans",
    "kidneybeans": "kidneybeans",
    "chickpea": "chickpea",
    "lentil": "lentil",
    "jute": "jute",
    "coffee": "coffee",
    "apple": "apple"
}

# ── APMC/e-NAM calibrated base prices (₹/quintal) — 2023-2024 averages ───────
_BASE_PRICES = {
    "rice":                   2200,
    "maize":                  1800,
    "cotton":                 6500,
    "banana":                 1800,
    "mango":                  3500,
    "grapes":                 5000,
    "orange":                 3000,
    "papaya":                 1500,
    "pomegranate":            6000,
    "tender coconut":         2500,
    "coconut":                2500,
    "water melon":            1200,
    "watermelon":             1200,
    "karbuja(musk melon)":    1400,
    "muskmelon":              1400,
    "musk melon":             1400,
    "beans":                  3500,
    "black gram dal(urd dal)": 7200,
    "blackgram":              7200,
    "jute":                   4800,
    "coffee":                 12500,
    "chickpea":               5400,
    "lentil":                 6200,
    "pigeonpeas":             6800,
    "mungbean":               7100,
    "mothbeans":              5800,
    "kidneybeans":            8500,
    "apple":                  8000,
}

# ── Seasonal multipliers (month → multiplier) ─────────────────────────────────
_SEASONAL_MULTIPLIERS = {
    "rice":       {1:1.10,2:1.10,3:1.00,4:0.95,5:0.95,6:1.00,7:0.98,8:0.95,9:0.90,10:0.92,11:1.00,12:1.08},
    "cotton":     {1:1.05,2:1.08,3:1.10,4:1.05,5:1.00,6:0.95,7:0.92,8:0.90,9:0.95,10:1.00,11:1.05,12:1.08},
    "mango":      {1:1.30,2:1.20,3:1.00,4:0.80,5:0.75,6:0.80,7:0.90,8:1.10,9:1.20,10:1.30,11:1.35,12:1.35},
    "banana":     {1:1.00,2:1.00,3:0.95,4:0.90,5:0.90,6:0.95,7:1.00,8:1.05,9:1.10,10:1.10,11:1.05,12:1.00},
    "default":    {m: 1.0 for m in range(1, 13)},
}

_URBAN_DISTRICTS = {
    "hyderabad", "rangareddy", "medchal-malkajgiri", "sangareddy",
    "guntur", "visakhapatnam", "vijayawada", "tirupati", "nellore"
}
_SEMI_URBAN = {
    "warangal", "hanamkonda", "karimnagar", "nizamabad", "khammam",
    "eluru", "kakinada", "east godavari", "west godavari", "krishna"
}


def _quantity_elasticity(base_price: float, qty: float, crop: str) -> float:
    if qty <= 0:
        return base_price
    epsilon = -0.3
    adjustment = (qty / 100.0) ** epsilon - 1.0
    return base_price * (1.0 + adjustment * 0.15)


def _district_premium(location: str) -> float:
    loc = location.lower()
    if any(u in loc for u in _URBAN_DISTRICTS):
        return 1.08
    if any(s in loc for s in _SEMI_URBAN):
        return 1.04
    return 1.0


def predict_price(location: str, commodity: str, arrival_quantity: float = None) -> dict:
    today = date.today()
    qty = arrival_quantity if arrival_quantity is not None else 100.0
    soil = find_soil_profile(location)
    raw_comm = commodity.strip().lower()
    norm_comm = _ALIAS_MAP.get(raw_comm, raw_comm)

    if model is not None:
        try:
            district = (soil.get("district") or location).lower()
            state    = (soil.get("state") or "telangana").lower()
            commodity_code = COMMODITY_MAPPING.get(norm_comm) or COMMODITY_MAPPING.get(raw_comm)
            if commodity_code is not None:
                state_code    = STATE_MAPPING.get(state, 1)
                district_code = DISTRICT_MAPPING.get(district, 20)
                row = pd.DataFrame([{
                    "Commodity": commodity_code, "State": state_code, "District": district_code,
                    "Day": today.day, "Month": today.month, "Year": today.year,
                    "Quarter": (today.month - 1) // 3 + 1, "Arrival_Quantity": qty,
                }])
                row = row[list(model.feature_names_in_)]
                prediction = float(model.predict(row)[0])
                res = {
                    "location": location, "date": today.isoformat(), "commodity": commodity,
                    "arrival_quantity": qty,
                    "predicted_price_per_quintal": round(prediction, 2),
                    "model_source": "pickle",
                }
                try:
                    from database import save_prediction_to_supabase
                    save_prediction_to_supabase(
                        prediction_type="market_price",
                        location=location,
                        crop=commodity,
                        inputs={"location": location, "commodity": commodity, "arrival_quantity": qty},
                        results={"predicted_price_per_quintal": res["predicted_price_per_quintal"]},
                        model_source="pickle"
                    )
                except Exception:
                    pass
                return res
        except Exception:
            pass

    # ── Calibrated fallback market model ─────────────────────────────────────
    base = _BASE_PRICES.get(norm_comm) or _BASE_PRICES.get(raw_comm, 3500.0)

    # Seasonal adjustment
    seasonal_table = _SEASONAL_MULTIPLIERS.get(norm_comm, _SEASONAL_MULTIPLIERS.get(raw_comm, _SEASONAL_MULTIPLIERS["default"]))
    seasonal_mult  = seasonal_table.get(today.month, 1.0)

    # Quantity elasticity
    elastic_price = _quantity_elasticity(base, qty, norm_comm)

    # District premium
    dist_mult = _district_premium(location)

    # Year-on-year inflation (approx 5% per year from 2023 base)
    years_ahead = today.year - 2023
    inflation = (1.05 ** years_ahead)

    final_price = round(elastic_price * seasonal_mult * dist_mult * inflation, 2)

    res = {
        "location": location,
        "date": today.isoformat(),
        "commodity": commodity,
        "arrival_quantity": qty,
        "predicted_price_per_quintal": final_price,
        "model_source": "calibrated_apmc_fallback",
        "price_factors": {
            "base_price_2023": base,
            "seasonal_multiplier": round(seasonal_mult, 3),
            "district_premium": round(dist_mult, 3),
            "inflation_factor": round(inflation, 3),
        },
    }
    try:
        from database import save_prediction_to_supabase
        save_prediction_to_supabase(
            prediction_type="market_price",
            location=location,
            crop=commodity,
            inputs={"location": location, "commodity": commodity, "arrival_quantity": qty},
            results={"predicted_price_per_quintal": final_price},
            model_source="calibrated_apmc_fallback"
        )
    except Exception:
        pass
    return res
