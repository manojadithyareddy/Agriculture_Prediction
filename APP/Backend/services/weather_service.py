from __future__ import annotations
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# NEW: Mock Weather Database for Testing
# ---------------------------------------------------------------------------
_WEATHER_DB: dict = {
    # ── Telangana ────────────────────────────────────────────────────────────
    "hyderabad": {
        "lat": 17.38, "lon": 78.48,
        "temperature_2m": 30.0, "temperature_2m_max": 35.0, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 60.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.3, "Rainfall_Last_30_Days": 50.0,
    },
    "warangal": {
        "lat": 17.97, "lon": 79.60,
        "temperature_2m": 29.5, "temperature_2m_max": 34.0, "temperature_2m_min": 24.0,
        "relative_humidity_2m": 65.0, "precipitation_sum_today": 2.0,
        "precipitation": 2.0, "soil_moisture": 0.35, "Rainfall_Last_30_Days": 80.0,
    },
    "hanamkonda": {
        "lat": 17.99, "lon": 79.55,
        "temperature_2m": 29.0, "temperature_2m_max": 33.5, "temperature_2m_min": 24.0,
        "relative_humidity_2m": 66.0, "precipitation_sum_today": 1.5,
        "precipitation": 1.5, "soil_moisture": 0.36, "Rainfall_Last_30_Days": 75.0,
    },
    "karimnagar": {
        "lat": 18.43, "lon": 79.12,
        "temperature_2m": 28.8, "temperature_2m_max": 33.0, "temperature_2m_min": 23.5,
        "relative_humidity_2m": 62.0, "precipitation_sum_today": 3.0,
        "precipitation": 3.0, "soil_moisture": 0.32, "Rainfall_Last_30_Days": 90.0,
    },
    "nizamabad": {
        "lat": 18.67, "lon": 78.10,
        "temperature_2m": 28.0, "temperature_2m_max": 33.0, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 60.0, "precipitation_sum_today": 1.0,
        "precipitation": 1.0, "soil_moisture": 0.30, "Rainfall_Last_30_Days": 70.0,
    },
    "adilabad": {
        "lat": 19.67, "lon": 78.53,
        "temperature_2m": 27.5, "temperature_2m_max": 32.5, "temperature_2m_min": 22.0,
        "relative_humidity_2m": 68.0, "precipitation_sum_today": 5.0,
        "precipitation": 5.0, "soil_moisture": 0.40, "Rainfall_Last_30_Days": 120.0,
    },
    "khammam": {
        "lat": 17.25, "lon": 80.15,
        "temperature_2m": 30.0, "temperature_2m_max": 34.5, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 70.0, "precipitation_sum_today": 4.0,
        "precipitation": 4.0, "soil_moisture": 0.38, "Rainfall_Last_30_Days": 110.0,
    },
    "nalgonda": {
        "lat": 17.05, "lon": 79.27,
        "temperature_2m": 31.0, "temperature_2m_max": 36.0, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 55.0, "precipitation_sum_today": 0.5,
        "precipitation": 0.5, "soil_moisture": 0.28, "Rainfall_Last_30_Days": 45.0,
    },
    "medak": {
        "lat": 18.05, "lon": 78.27,
        "temperature_2m": 29.0, "temperature_2m_max": 34.0, "temperature_2m_min": 24.0,
        "relative_humidity_2m": 58.0, "precipitation_sum_today": 1.0,
        "precipitation": 1.0, "soil_moisture": 0.30, "Rainfall_Last_30_Days": 60.0,
    },
    "sangareddy": {
        "lat": 17.62, "lon": 78.07,
        "temperature_2m": 29.5, "temperature_2m_max": 34.0, "temperature_2m_min": 24.5,
        "relative_humidity_2m": 57.0, "precipitation_sum_today": 1.0,
        "precipitation": 1.0, "soil_moisture": 0.29, "Rainfall_Last_30_Days": 55.0,
    },
    "rangareddy": {
        "lat": 17.20, "lon": 78.43,
        "temperature_2m": 30.0, "temperature_2m_max": 35.0, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 59.0, "precipitation_sum_today": 0.5,
        "precipitation": 0.5, "soil_moisture": 0.29, "Rainfall_Last_30_Days": 48.0,
    },
    "medchal-malkajgiri": {
        "lat": 17.57, "lon": 78.53,
        "temperature_2m": 30.0, "temperature_2m_max": 35.0, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 60.0, "precipitation_sum_today": 0.5,
        "precipitation": 0.5, "soil_moisture": 0.30, "Rainfall_Last_30_Days": 50.0,
    },
    "mahabubnagar": {
        "lat": 16.73, "lon": 77.98,
        "temperature_2m": 32.0, "temperature_2m_max": 37.5, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 50.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.22, "Rainfall_Last_30_Days": 35.0,
    },
    "nagarkurnool": {
        "lat": 16.48, "lon": 78.33,
        "temperature_2m": 31.5, "temperature_2m_max": 37.0, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 52.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.24, "Rainfall_Last_30_Days": 40.0,
    },
    "wanaparthy": {
        "lat": 16.36, "lon": 78.07,
        "temperature_2m": 31.0, "temperature_2m_max": 36.5, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 53.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.25, "Rainfall_Last_30_Days": 40.0,
    },
    "narayanpet": {
        "lat": 16.74, "lon": 77.50,
        "temperature_2m": 32.0, "temperature_2m_max": 37.5, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 48.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.21, "Rainfall_Last_30_Days": 33.0,
    },
    "jogulamba gadwal": {
        "lat": 16.23, "lon": 77.80,
        "temperature_2m": 32.5, "temperature_2m_max": 38.0, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 47.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.20, "Rainfall_Last_30_Days": 30.0,
    },
    "suryapet": {
        "lat": 17.15, "lon": 79.63,
        "temperature_2m": 30.5, "temperature_2m_max": 35.5, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 63.0, "precipitation_sum_today": 2.0,
        "precipitation": 2.0, "soil_moisture": 0.33, "Rainfall_Last_30_Days": 70.0,
    },
    "mahabubabad": {
        "lat": 17.60, "lon": 80.00,
        "temperature_2m": 29.5, "temperature_2m_max": 34.0, "temperature_2m_min": 24.5,
        "relative_humidity_2m": 67.0, "precipitation_sum_today": 3.5,
        "precipitation": 3.5, "soil_moisture": 0.37, "Rainfall_Last_30_Days": 95.0,
    },
    "bhadradri kothagudem": {
        "lat": 17.55, "lon": 80.62,
        "temperature_2m": 29.0, "temperature_2m_max": 33.5, "temperature_2m_min": 24.0,
        "relative_humidity_2m": 72.0, "precipitation_sum_today": 6.0,
        "precipitation": 6.0, "soil_moisture": 0.42, "Rainfall_Last_30_Days": 130.0,
    },
    "mulugu": {
        "lat": 18.20, "lon": 80.08,
        "temperature_2m": 28.5, "temperature_2m_max": 33.0, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 70.0, "precipitation_sum_today": 5.0,
        "precipitation": 5.0, "soil_moisture": 0.40, "Rainfall_Last_30_Days": 115.0,
    },
    "jayashankar bhupalpally": {
        "lat": 18.47, "lon": 79.90,
        "temperature_2m": 28.0, "temperature_2m_max": 33.0, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 69.0, "precipitation_sum_today": 4.5,
        "precipitation": 4.5, "soil_moisture": 0.39, "Rainfall_Last_30_Days": 110.0,
    },
    "peddapalli": {
        "lat": 18.60, "lon": 79.37,
        "temperature_2m": 28.5, "temperature_2m_max": 33.0, "temperature_2m_min": 23.5,
        "relative_humidity_2m": 63.0, "precipitation_sum_today": 3.0,
        "precipitation": 3.0, "soil_moisture": 0.33, "Rainfall_Last_30_Days": 85.0,
    },
    "jagtial": {
        "lat": 18.80, "lon": 78.92,
        "temperature_2m": 28.5, "temperature_2m_max": 33.5, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 61.0, "precipitation_sum_today": 2.5,
        "precipitation": 2.5, "soil_moisture": 0.32, "Rainfall_Last_30_Days": 80.0,
    },
    "rajanna sircilla": {
        "lat": 18.38, "lon": 78.83,
        "temperature_2m": 28.0, "temperature_2m_max": 33.0, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 62.0, "precipitation_sum_today": 2.0,
        "precipitation": 2.0, "soil_moisture": 0.31, "Rainfall_Last_30_Days": 78.0,
    },
    "siddipet": {
        "lat": 18.10, "lon": 78.85,
        "temperature_2m": 29.0, "temperature_2m_max": 34.0, "temperature_2m_min": 24.0,
        "relative_humidity_2m": 60.0, "precipitation_sum_today": 1.5,
        "precipitation": 1.5, "soil_moisture": 0.30, "Rainfall_Last_30_Days": 65.0,
    },
    "jangaon": {
        "lat": 17.72, "lon": 79.15,
        "temperature_2m": 29.5, "temperature_2m_max": 34.5, "temperature_2m_min": 24.5,
        "relative_humidity_2m": 62.0, "precipitation_sum_today": 2.0,
        "precipitation": 2.0, "soil_moisture": 0.32, "Rainfall_Last_30_Days": 72.0,
    },
    "vikarabad": {
        "lat": 17.33, "lon": 77.90,
        "temperature_2m": 29.0, "temperature_2m_max": 34.0, "temperature_2m_min": 24.0,
        "relative_humidity_2m": 58.0, "precipitation_sum_today": 1.0,
        "precipitation": 1.0, "soil_moisture": 0.28, "Rainfall_Last_30_Days": 55.0,
    },
    "kamareddy": {
        "lat": 18.32, "lon": 78.35,
        "temperature_2m": 29.0, "temperature_2m_max": 33.5, "temperature_2m_min": 23.5,
        "relative_humidity_2m": 57.0, "precipitation_sum_today": 1.5,
        "precipitation": 1.5, "soil_moisture": 0.29, "Rainfall_Last_30_Days": 62.0,
    },
    "nirmal": {
        "lat": 19.10, "lon": 78.35,
        "temperature_2m": 28.0, "temperature_2m_max": 33.0, "temperature_2m_min": 22.5,
        "relative_humidity_2m": 65.0, "precipitation_sum_today": 4.0,
        "precipitation": 4.0, "soil_moisture": 0.37, "Rainfall_Last_30_Days": 100.0,
    },
    "mancherial": {
        "lat": 18.87, "lon": 79.45,
        "temperature_2m": 28.5, "temperature_2m_max": 33.5, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 66.0, "precipitation_sum_today": 3.5,
        "precipitation": 3.5, "soil_moisture": 0.36, "Rainfall_Last_30_Days": 98.0,
    },
    "komaram bheem asifabad": {
        "lat": 19.37, "lon": 79.30,
        "temperature_2m": 27.5, "temperature_2m_max": 32.5, "temperature_2m_min": 22.0,
        "relative_humidity_2m": 70.0, "precipitation_sum_today": 6.0,
        "precipitation": 6.0, "soil_moisture": 0.42, "Rainfall_Last_30_Days": 125.0,
    },
    "yadadri bhuvanagiri": {
        "lat": 17.60, "lon": 79.08,
        "temperature_2m": 30.0, "temperature_2m_max": 35.0, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 60.0, "precipitation_sum_today": 1.5,
        "precipitation": 1.5, "soil_moisture": 0.31, "Rainfall_Last_30_Days": 60.0,
    },
    # ── Andhra Pradesh ────────────────────────────────────────────────────────
    "guntur": {
        "lat": 16.30, "lon": 80.43,
        "temperature_2m": 31.5, "temperature_2m_max": 36.0, "temperature_2m_min": 26.5,
        "relative_humidity_2m": 72.0, "precipitation_sum_today": 3.0,
        "precipitation": 3.0, "soil_moisture": 0.36, "Rainfall_Last_30_Days": 85.0,
    },
    "krishna": {
        "lat": 16.60, "lon": 80.80,
        "temperature_2m": 30.5, "temperature_2m_max": 35.5, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 75.0, "precipitation_sum_today": 4.0,
        "precipitation": 4.0, "soil_moisture": 0.38, "Rainfall_Last_30_Days": 95.0,
    },
    "east godavari": {
        "lat": 17.00, "lon": 81.78,
        "temperature_2m": 30.0, "temperature_2m_max": 34.5, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 78.0, "precipitation_sum_today": 6.0,
        "precipitation": 6.0, "soil_moisture": 0.42, "Rainfall_Last_30_Days": 140.0,
    },
    "west godavari": {
        "lat": 16.92, "lon": 81.33,
        "temperature_2m": 30.0, "temperature_2m_max": 35.0, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 76.0, "precipitation_sum_today": 5.5,
        "precipitation": 5.5, "soil_moisture": 0.41, "Rainfall_Last_30_Days": 130.0,
    },
    "kurnool": {
        "lat": 15.83, "lon": 78.05,
        "temperature_2m": 33.0, "temperature_2m_max": 38.0, "temperature_2m_min": 27.0,
        "relative_humidity_2m": 50.0, "precipitation_sum_today": 0.5,
        "precipitation": 0.5, "soil_moisture": 0.22, "Rainfall_Last_30_Days": 30.0,
    },
    "anantapur": {
        "lat": 14.68, "lon": 77.60,
        "temperature_2m": 33.5, "temperature_2m_max": 38.5, "temperature_2m_min": 27.5,
        "relative_humidity_2m": 45.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.18, "Rainfall_Last_30_Days": 20.0,
    },
    "chittoor": {
        "lat": 13.22, "lon": 79.10,
        "temperature_2m": 30.0, "temperature_2m_max": 35.0, "temperature_2m_min": 24.5,
        "relative_humidity_2m": 60.0, "precipitation_sum_today": 2.0,
        "precipitation": 2.0, "soil_moisture": 0.30, "Rainfall_Last_30_Days": 65.0,
    },
    "tirupati": {
        "lat": 13.63, "lon": 79.42,
        "temperature_2m": 30.5, "temperature_2m_max": 35.0, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 62.0, "precipitation_sum_today": 2.5,
        "precipitation": 2.5, "soil_moisture": 0.31, "Rainfall_Last_30_Days": 70.0,
    },
    "visakhapatnam": {
        "lat": 17.72, "lon": 83.30,
        "temperature_2m": 29.5, "temperature_2m_max": 33.5, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 78.0, "precipitation_sum_today": 8.0,
        "precipitation": 8.0, "soil_moisture": 0.45, "Rainfall_Last_30_Days": 160.0,
    },
    "srikakulam": {
        "lat": 18.30, "lon": 83.90,
        "temperature_2m": 29.0, "temperature_2m_max": 33.0, "temperature_2m_min": 24.5,
        "relative_humidity_2m": 80.0, "precipitation_sum_today": 9.0,
        "precipitation": 9.0, "soil_moisture": 0.47, "Rainfall_Last_30_Days": 170.0,
    },
    "vizianagaram": {
        "lat": 18.12, "lon": 83.42,
        "temperature_2m": 29.0, "temperature_2m_max": 33.5, "temperature_2m_min": 24.5,
        "relative_humidity_2m": 78.0, "precipitation_sum_today": 8.5,
        "precipitation": 8.5, "soil_moisture": 0.45, "Rainfall_Last_30_Days": 165.0,
    },
    "ysr kadapa": {
        "lat": 14.47, "lon": 78.82,
        "temperature_2m": 32.0, "temperature_2m_max": 37.0, "temperature_2m_min": 26.5,
        "relative_humidity_2m": 52.0, "precipitation_sum_today": 1.0,
        "precipitation": 1.0, "soil_moisture": 0.23, "Rainfall_Last_30_Days": 35.0,
    },
    "nandyal": {
        "lat": 15.48, "lon": 78.48,
        "temperature_2m": 32.0, "temperature_2m_max": 37.5, "temperature_2m_min": 26.5,
        "relative_humidity_2m": 50.0, "precipitation_sum_today": 0.5,
        "precipitation": 0.5, "soil_moisture": 0.23, "Rainfall_Last_30_Days": 32.0,
    },
    "bapatla": {
        "lat": 15.90, "lon": 80.47,
        "temperature_2m": 31.0, "temperature_2m_max": 35.5, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 72.0, "precipitation_sum_today": 4.0,
        "precipitation": 4.0, "soil_moisture": 0.37, "Rainfall_Last_30_Days": 95.0,
    },
    "eluru": {
        "lat": 16.72, "lon": 81.10,
        "temperature_2m": 30.5, "temperature_2m_max": 35.0, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 74.0, "precipitation_sum_today": 4.5,
        "precipitation": 4.5, "soil_moisture": 0.39, "Rainfall_Last_30_Days": 105.0,
    },
    "sri potti sriramulu nellore": {
        "lat": 14.45, "lon": 79.98,
        "temperature_2m": 31.0, "temperature_2m_max": 36.0, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 70.0, "precipitation_sum_today": 3.0,
        "precipitation": 3.0, "soil_moisture": 0.34, "Rainfall_Last_30_Days": 80.0,
    },
    "prakasam": {
        "lat": 15.37, "lon": 79.87,
        "temperature_2m": 31.5, "temperature_2m_max": 36.5, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 68.0, "precipitation_sum_today": 2.5,
        "precipitation": 2.5, "soil_moisture": 0.32, "Rainfall_Last_30_Days": 70.0,
    },
    "alluri sitharama raju": {
        "lat": 18.00, "lon": 82.00,
        "temperature_2m": 28.0, "temperature_2m_max": 32.5, "temperature_2m_min": 23.5,
        "relative_humidity_2m": 78.0, "precipitation_sum_today": 9.0,
        "precipitation": 9.0, "soil_moisture": 0.46, "Rainfall_Last_30_Days": 175.0,
    },
    "parvathipuram manyam": {
        "lat": 18.78, "lon": 83.42,
        "temperature_2m": 27.5, "temperature_2m_max": 32.0, "temperature_2m_min": 23.0,
        "relative_humidity_2m": 80.0, "precipitation_sum_today": 10.0,
        "precipitation": 10.0, "soil_moisture": 0.48, "Rainfall_Last_30_Days": 185.0,
    },
    "anakapalli": {
        "lat": 17.70, "lon": 83.00,
        "temperature_2m": 29.5, "temperature_2m_max": 33.5, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 77.0, "precipitation_sum_today": 7.5,
        "precipitation": 7.5, "soil_moisture": 0.44, "Rainfall_Last_30_Days": 155.0,
    },
    "annamayya": {
        "lat": 13.97, "lon": 79.00,
        "temperature_2m": 30.5, "temperature_2m_max": 35.5, "temperature_2m_min": 25.0,
        "relative_humidity_2m": 58.0, "precipitation_sum_today": 1.5,
        "precipitation": 1.5, "soil_moisture": 0.28, "Rainfall_Last_30_Days": 55.0,
    },
    "kakinada": {
        "lat": 16.98, "lon": 82.24,
        "temperature_2m": 30.0, "temperature_2m_max": 34.5, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 80.0, "precipitation_sum_today": 7.0,
        "precipitation": 7.0, "soil_moisture": 0.44, "Rainfall_Last_30_Days": 150.0,
    },
    "kona seema": {
        "lat": 16.73, "lon": 81.90,
        "temperature_2m": 30.0, "temperature_2m_max": 34.5, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 80.0, "precipitation_sum_today": 6.5,
        "precipitation": 6.5, "soil_moisture": 0.43, "Rainfall_Last_30_Days": 145.0,
    },
    "palnadu": {
        "lat": 16.47, "lon": 79.57,
        "temperature_2m": 31.0, "temperature_2m_max": 36.0, "temperature_2m_min": 25.5,
        "relative_humidity_2m": 64.0, "precipitation_sum_today": 2.0,
        "precipitation": 2.0, "soil_moisture": 0.31, "Rainfall_Last_30_Days": 65.0,
    },
    "ntr": {
        "lat": 16.58, "lon": 80.68,
        "temperature_2m": 31.0, "temperature_2m_max": 35.5, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 72.0, "precipitation_sum_today": 3.5,
        "precipitation": 3.5, "soil_moisture": 0.36, "Rainfall_Last_30_Days": 90.0,
    },
    "sri sathya sai": {
        "lat": 14.17, "lon": 77.67,
        "temperature_2m": 32.5, "temperature_2m_max": 38.0, "temperature_2m_min": 26.5,
        "relative_humidity_2m": 47.0, "precipitation_sum_today": 0.5,
        "precipitation": 0.5, "soil_moisture": 0.20, "Rainfall_Last_30_Days": 25.0,
    },
    # ── Legacy city names ─────────────────────────────────────────────────────
    "mumbai": {
        "lat": 19.07, "lon": 72.87,
        "temperature_2m": 28.0, "temperature_2m_max": 31.0, "temperature_2m_min": 26.0,
        "relative_humidity_2m": 85.0, "precipitation_sum_today": 12.5,
        "precipitation": 12.5, "soil_moisture": 0.8, "Rainfall_Last_30_Days": 300.0,
    },
    "delhi": {
        "lat": 28.70, "lon": 77.10,
        "temperature_2m": 40.0, "temperature_2m_max": 45.0, "temperature_2m_min": 32.0,
        "relative_humidity_2m": 20.0, "precipitation_sum_today": 0.0,
        "precipitation": 0.0, "soil_moisture": 0.1, "Rainfall_Last_30_Days": 5.0,
    },
}

# ---------------------------------------------------------------------------
# Default fallback (if location isn't in our mock DB)
# ---------------------------------------------------------------------------
_DEFAULT_WEATHER: dict = {
    "lat": 0.0, "lon": 0.0, "temperature_2m": 25.0, "temperature_2m_max": 30.0, 
    "temperature_2m_min": 20.0, "relative_humidity_2m": 50.0, "precipitation": 0.0, 
    "precipitation_sum_today": 0.0, "surface_pressure": 1010.0, "cloud_cover": 20.0, 
    "wind_speed_10m": 10.0, "wind_direction_10m": 180.0, "wind_gusts_10m": 15.0, 
    "shortwave_radiation": 500.0, "et0_fao_evapotranspiration": 5.0, "soil_moisture": 0.3, 
    "soil_temperature": 25.0, "elevation": 500.0, "Rainfall_Last_7_Days": 10.0, 
    "Rainfall_Last_30_Days": 50.0, "Consecutive_Dry_Days": 5
}


_DATASET_CACHE = None

def _get_csv_weather_db():
    global _DATASET_CACHE
    if _DATASET_CACHE is not None:
        return _DATASET_CACHE

    _DIR = os.path.dirname(__file__)
    csv_path = os.path.abspath(os.path.join(_DIR, "..", "..", "..", "Data", "AP_TS_Weather_Dataset.csv"))
    if os.path.exists(csv_path):
        try:
            import pandas as pd
            cols = [
                'city', 'latitude', 'longitude', 'temperature_2m', 'relative_humidity_2m',
                'precipitation', 'et0_fao_evapotranspiration', 'Soil_Moisture',
                'Rainfall_Last_30_Days', 'surface_pressure', 'cloud_cover', 'wind_speed_10m',
                'Heat_Index', 'Growing_Degree_Days', 'Consecutive_Dry_Days'
            ]
            df = pd.read_csv(csv_path, usecols=cols)
            grouped = df.groupby(df['city'].astype(str).str.lower())
            db = {}
            for city_name, group in grouped:
                latest = group.iloc[-1].to_dict()
                db[city_name] = {
                    "lat": float(latest.get("latitude", 0.0)),
                    "lon": float(latest.get("longitude", 0.0)),
                    "temperature_2m": float(latest.get("temperature_2m", 28.0)),
                    "temperature_2m_max": float(latest.get("temperature_2m", 33.0)) + 4.0,
                    "temperature_2m_min": float(latest.get("temperature_2m", 25.0)) - 4.0,
                    "relative_humidity_2m": float(latest.get("relative_humidity_2m", 60.0)),
                    "precipitation_sum_today": float(latest.get("precipitation", 0.0)),
                    "precipitation": float(latest.get("precipitation", 0.0)),
                    "soil_moisture": float(latest.get("Soil_Moisture", 0.3)),
                    "Rainfall_Last_30_Days": float(latest.get("Rainfall_Last_30_Days", 50.0)),
                    "et0_fao_evapotranspiration": float(latest.get("et0_fao_evapotranspiration", 5.0)),
                    "surface_pressure": float(latest.get("surface_pressure", 1010.0)),
                    "cloud_cover": float(latest.get("cloud_cover", 20.0)),
                    "wind_speed_10m": float(latest.get("wind_speed_10m", 10.0)),
                    "Heat_Index": float(latest.get("Heat_Index", 30.0)),
                    "Growing_Degree_Days": float(latest.get("Growing_Degree_Days", 10.0)),
                    "Consecutive_Dry_Days": int(latest.get("Consecutive_Dry_Days", 5)),
                    "data_source": "AP_TS_Weather_Dataset.csv (Direct Link)"
                }
            _DATASET_CACHE = db
            return _DATASET_CACHE
        except Exception as e:
            print(f"[WARNING]: Failed reading CSV weather dataset: {e}")

    _DATASET_CACHE = {}
    return _DATASET_CACHE


def get_full_snapshot(location: str) -> dict:
    """
    Return a weather snapshot dict for *location*.
    Directly queries AP_TS_Weather_Dataset.csv if available.
    """
    today = datetime.today().strftime("%Y-%m-%d")
    safe_location = location.lower().strip() if location else ""

    # 1. Start with the defaults
    snapshot = dict(_DEFAULT_WEATHER)

    # 2. Check direct CSV dataset first
    csv_db = _get_csv_weather_db()
    if safe_location in csv_db:
        snapshot.update(csv_db[safe_location])
    # 3. Fallback to mock dictionary if not in CSV
    elif safe_location in _WEATHER_DB:
        snapshot.update(_WEATHER_DB[safe_location])
    else:
        print(f"[WARNING]: Location '{location}' not found in weather DB or CSV dataset. Using defaults.")

    # 4. Attach metadata
    snapshot["location"] = location
    snapshot["date"] = today

    return snapshot


def get_7_day_forecast(location: str) -> list[dict]:
    """
    Return a 7-day mock weather forecast for *location*.
    """
    import datetime
    base = get_full_snapshot(location)
    
    forecast = []
    base_temp = base["temperature_2m"]
    base_rain = base["precipitation_sum_today"]
    
    for i in range(7):
        target_date = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        
        # Add some random variance
        import random
        temp_var = random.uniform(-2.0, 2.0)
        rain_chance = random.random()
        rain_var = random.uniform(0.0, 5.0) if rain_chance > 0.7 else 0.0
        
        forecast.append({
            "date": target_date,
            "temperature_2m": round(base_temp + temp_var, 1),
            "precipitation": round(base_rain + rain_var, 1),
            "relative_humidity_2m": round(base["relative_humidity_2m"] + random.uniform(-5, 5), 1)
        })
        
    return forecast