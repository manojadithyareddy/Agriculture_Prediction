from __future__ import annotations

# ---------------------------------------------------------------------------
# Default / fallback values (if location is not found)
# ---------------------------------------------------------------------------
_DEFAULT_PROFILE: dict = {
    "soil_ph": 6.5,
    "organic_carbon": 1.0,
    "clay_percentage": 30.0,
    "sand_percentage": 40.0,
    "silt_percentage": 30.0,
    "nitrogen": 280.0,
    "cec": 18.0,
    "bulk_density": 1.3,
    "field_capacity": 0.30,
    "wilting_point": 0.14,
    "available_water": 0.16,
    "soil_type": "red loam",
    "state": "telangana",
}

# ---------------------------------------------------------------------------
# NEW: Real Soil Database Lookup (Dictionary)
# Add your real district data here!
# ---------------------------------------------------------------------------
_SOIL_DB: dict = {
    # ── Telangana ─────────────────────────────────────────────────────────────
    "hyderabad": {
        "soil_ph": 7.0, "nitrogen": 280.0, "organic_carbon": 0.9,
        "clay_percentage": 30.0, "sand_percentage": 42.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "warangal": {
        "soil_ph": 7.2, "nitrogen": 310.0, "organic_carbon": 1.1,
        "clay_percentage": 45.0, "sand_percentage": 25.0, "silt_percentage": 30.0,
        "soil_type": "black cotton", "state": "telangana",
    },
    "hanamkonda": {
        "soil_ph": 7.1, "nitrogen": 305.0, "organic_carbon": 1.0,
        "clay_percentage": 44.0, "sand_percentage": 26.0, "silt_percentage": 30.0,
        "soil_type": "black cotton", "state": "telangana",
    },
    "karimnagar": {
        "soil_ph": 6.8, "nitrogen": 260.0, "organic_carbon": 0.8,
        "clay_percentage": 25.0, "sand_percentage": 50.0, "silt_percentage": 25.0,
        "soil_type": "sandy loam", "state": "telangana",
    },
    "nizamabad": {
        "soil_ph": 7.0, "nitrogen": 270.0, "organic_carbon": 0.9,
        "clay_percentage": 35.0, "sand_percentage": 35.0, "silt_percentage": 30.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "adilabad": {
        "soil_ph": 6.5, "nitrogen": 320.0, "organic_carbon": 1.3,
        "clay_percentage": 40.0, "sand_percentage": 28.0, "silt_percentage": 32.0,
        "soil_type": "black cotton", "state": "telangana",
    },
    "khammam": {
        "soil_ph": 6.7, "nitrogen": 290.0, "organic_carbon": 1.1,
        "clay_percentage": 38.0, "sand_percentage": 30.0, "silt_percentage": 32.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "nalgonda": {
        "soil_ph": 7.3, "nitrogen": 240.0, "organic_carbon": 0.6,
        "clay_percentage": 28.0, "sand_percentage": 48.0, "silt_percentage": 24.0,
        "soil_type": "sandy loam", "state": "telangana",
    },
    "medak": {
        "soil_ph": 7.0, "nitrogen": 265.0, "organic_carbon": 0.8,
        "clay_percentage": 30.0, "sand_percentage": 42.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "sangareddy": {
        "soil_ph": 7.1, "nitrogen": 268.0, "organic_carbon": 0.8,
        "clay_percentage": 31.0, "sand_percentage": 41.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "rangareddy": {
        "soil_ph": 6.9, "nitrogen": 275.0, "organic_carbon": 0.9,
        "clay_percentage": 30.0, "sand_percentage": 42.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "medchal-malkajgiri": {
        "soil_ph": 6.9, "nitrogen": 270.0, "organic_carbon": 0.9,
        "clay_percentage": 30.0, "sand_percentage": 42.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "mahabubnagar": {
        "soil_ph": 7.5, "nitrogen": 220.0, "organic_carbon": 0.5,
        "clay_percentage": 22.0, "sand_percentage": 55.0, "silt_percentage": 23.0,
        "soil_type": "red sandy", "state": "telangana",
    },
    "nagarkurnool": {
        "soil_ph": 7.4, "nitrogen": 230.0, "organic_carbon": 0.6,
        "clay_percentage": 25.0, "sand_percentage": 50.0, "silt_percentage": 25.0,
        "soil_type": "red sandy", "state": "telangana",
    },
    "wanaparthy": {
        "soil_ph": 7.3, "nitrogen": 235.0, "organic_carbon": 0.6,
        "clay_percentage": 26.0, "sand_percentage": 49.0, "silt_percentage": 25.0,
        "soil_type": "red sandy", "state": "telangana",
    },
    "narayanpet": {
        "soil_ph": 7.4, "nitrogen": 220.0, "organic_carbon": 0.5,
        "clay_percentage": 22.0, "sand_percentage": 55.0, "silt_percentage": 23.0,
        "soil_type": "red sandy", "state": "telangana",
    },
    "jogulamba gadwal": {
        "soil_ph": 7.5, "nitrogen": 215.0, "organic_carbon": 0.5,
        "clay_percentage": 20.0, "sand_percentage": 57.0, "silt_percentage": 23.0,
        "soil_type": "red sandy", "state": "telangana",
    },
    "suryapet": {
        "soil_ph": 7.0, "nitrogen": 265.0, "organic_carbon": 0.85,
        "clay_percentage": 33.0, "sand_percentage": 38.0, "silt_percentage": 29.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "mahabubabad": {
        "soil_ph": 6.8, "nitrogen": 280.0, "organic_carbon": 1.0,
        "clay_percentage": 36.0, "sand_percentage": 34.0, "silt_percentage": 30.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "bhadradri kothagudem": {
        "soil_ph": 6.4, "nitrogen": 295.0, "organic_carbon": 1.2,
        "clay_percentage": 38.0, "sand_percentage": 30.0, "silt_percentage": 32.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "mulugu": {
        "soil_ph": 6.5, "nitrogen": 285.0, "organic_carbon": 1.1,
        "clay_percentage": 37.0, "sand_percentage": 32.0, "silt_percentage": 31.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "jayashankar bhupalpally": {
        "soil_ph": 6.6, "nitrogen": 300.0, "organic_carbon": 1.15,
        "clay_percentage": 40.0, "sand_percentage": 28.0, "silt_percentage": 32.0,
        "soil_type": "black cotton", "state": "telangana",
    },
    "peddapalli": {
        "soil_ph": 6.9, "nitrogen": 270.0, "organic_carbon": 0.9,
        "clay_percentage": 32.0, "sand_percentage": 38.0, "silt_percentage": 30.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "jagtial": {
        "soil_ph": 7.0, "nitrogen": 255.0, "organic_carbon": 0.85,
        "clay_percentage": 28.0, "sand_percentage": 44.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "rajanna sircilla": {
        "soil_ph": 6.8, "nitrogen": 260.0, "organic_carbon": 0.85,
        "clay_percentage": 28.0, "sand_percentage": 44.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "siddipet": {
        "soil_ph": 7.0, "nitrogen": 258.0, "organic_carbon": 0.82,
        "clay_percentage": 29.0, "sand_percentage": 43.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "jangaon": {
        "soil_ph": 6.9, "nitrogen": 265.0, "organic_carbon": 0.88,
        "clay_percentage": 32.0, "sand_percentage": 38.0, "silt_percentage": 30.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "vikarabad": {
        "soil_ph": 6.7, "nitrogen": 262.0, "organic_carbon": 0.87,
        "clay_percentage": 30.0, "sand_percentage": 40.0, "silt_percentage": 30.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "kamareddy": {
        "soil_ph": 7.1, "nitrogen": 255.0, "organic_carbon": 0.80,
        "clay_percentage": 28.0, "sand_percentage": 44.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "nirmal": {
        "soil_ph": 6.6, "nitrogen": 295.0, "organic_carbon": 1.1,
        "clay_percentage": 38.0, "sand_percentage": 30.0, "silt_percentage": 32.0,
        "soil_type": "black cotton", "state": "telangana",
    },
    "mancherial": {
        "soil_ph": 6.7, "nitrogen": 285.0, "organic_carbon": 1.05,
        "clay_percentage": 37.0, "sand_percentage": 32.0, "silt_percentage": 31.0,
        "soil_type": "red loam", "state": "telangana",
    },
    "komaram bheem asifabad": {
        "soil_ph": 6.4, "nitrogen": 315.0, "organic_carbon": 1.3,
        "clay_percentage": 42.0, "sand_percentage": 26.0, "silt_percentage": 32.0,
        "soil_type": "black cotton", "state": "telangana",
    },
    "yadadri bhuvanagiri": {
        "soil_ph": 7.0, "nitrogen": 268.0, "organic_carbon": 0.85,
        "clay_percentage": 30.0, "sand_percentage": 41.0, "silt_percentage": 29.0,
        "soil_type": "red loam", "state": "telangana",
    },
    # ── Andhra Pradesh ────────────────────────────────────────────────────────
    "guntur": {
        "soil_ph": 7.8, "nitrogen": 230.0, "organic_carbon": 0.6,
        "clay_percentage": 28.0, "sand_percentage": 45.0, "silt_percentage": 27.0,
        "soil_type": "black cotton", "state": "andhra pradesh",
    },
    "krishna": {
        "soil_ph": 7.6, "nitrogen": 245.0, "organic_carbon": 0.7,
        "clay_percentage": 30.0, "sand_percentage": 42.0, "silt_percentage": 28.0,
        "soil_type": "alluvial", "state": "andhra pradesh",
    },
    "east godavari": {
        "soil_ph": 6.8, "nitrogen": 290.0, "organic_carbon": 1.1,
        "clay_percentage": 35.0, "sand_percentage": 35.0, "silt_percentage": 30.0,
        "soil_type": "alluvial", "state": "andhra pradesh",
    },
    "west godavari": {
        "soil_ph": 6.7, "nitrogen": 295.0, "organic_carbon": 1.15,
        "clay_percentage": 36.0, "sand_percentage": 34.0, "silt_percentage": 30.0,
        "soil_type": "alluvial", "state": "andhra pradesh",
    },
    "kurnool": {
        "soil_ph": 7.8, "nitrogen": 210.0, "organic_carbon": 0.45,
        "clay_percentage": 20.0, "sand_percentage": 58.0, "silt_percentage": 22.0,
        "soil_type": "red sandy", "state": "andhra pradesh",
    },
    "anantapur": {
        "soil_ph": 7.9, "nitrogen": 195.0, "organic_carbon": 0.35,
        "clay_percentage": 18.0, "sand_percentage": 62.0, "silt_percentage": 20.0,
        "soil_type": "red sandy", "state": "andhra pradesh",
    },
    "chittoor": {
        "soil_ph": 6.8, "nitrogen": 250.0, "organic_carbon": 0.8,
        "clay_percentage": 28.0, "sand_percentage": 44.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "tirupati": {
        "soil_ph": 6.7, "nitrogen": 255.0, "organic_carbon": 0.82,
        "clay_percentage": 27.0, "sand_percentage": 45.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "visakhapatnam": {
        "soil_ph": 6.5, "nitrogen": 285.0, "organic_carbon": 1.05,
        "clay_percentage": 35.0, "sand_percentage": 34.0, "silt_percentage": 31.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "srikakulam": {
        "soil_ph": 6.4, "nitrogen": 275.0, "organic_carbon": 1.0,
        "clay_percentage": 33.0, "sand_percentage": 36.0, "silt_percentage": 31.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "vizianagaram": {
        "soil_ph": 6.5, "nitrogen": 278.0, "organic_carbon": 1.0,
        "clay_percentage": 33.0, "sand_percentage": 36.0, "silt_percentage": 31.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "ysr kadapa": {
        "soil_ph": 7.6, "nitrogen": 215.0, "organic_carbon": 0.5,
        "clay_percentage": 22.0, "sand_percentage": 54.0, "silt_percentage": 24.0,
        "soil_type": "red sandy", "state": "andhra pradesh",
    },
    "nandyal": {
        "soil_ph": 7.7, "nitrogen": 218.0, "organic_carbon": 0.5,
        "clay_percentage": 22.0, "sand_percentage": 55.0, "silt_percentage": 23.0,
        "soil_type": "red sandy", "state": "andhra pradesh",
    },
    "bapatla": {
        "soil_ph": 7.5, "nitrogen": 235.0, "organic_carbon": 0.65,
        "clay_percentage": 27.0, "sand_percentage": 46.0, "silt_percentage": 27.0,
        "soil_type": "black cotton", "state": "andhra pradesh",
    },
    "eluru": {
        "soil_ph": 7.0, "nitrogen": 265.0, "organic_carbon": 0.90,
        "clay_percentage": 32.0, "sand_percentage": 38.0, "silt_percentage": 30.0,
        "soil_type": "alluvial", "state": "andhra pradesh",
    },
    "sri potti sriramulu nellore": {
        "soil_ph": 7.4, "nitrogen": 240.0, "organic_carbon": 0.65,
        "clay_percentage": 28.0, "sand_percentage": 44.0, "silt_percentage": 28.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "prakasam": {
        "soil_ph": 7.5, "nitrogen": 225.0, "organic_carbon": 0.55,
        "clay_percentage": 25.0, "sand_percentage": 50.0, "silt_percentage": 25.0,
        "soil_type": "red sandy", "state": "andhra pradesh",
    },
    "alluri sitharama raju": {
        "soil_ph": 6.3, "nitrogen": 310.0, "organic_carbon": 1.3,
        "clay_percentage": 40.0, "sand_percentage": 28.0, "silt_percentage": 32.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "parvathipuram manyam": {
        "soil_ph": 6.2, "nitrogen": 315.0, "organic_carbon": 1.35,
        "clay_percentage": 42.0, "sand_percentage": 26.0, "silt_percentage": 32.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "anakapalli": {
        "soil_ph": 6.5, "nitrogen": 282.0, "organic_carbon": 1.05,
        "clay_percentage": 34.0, "sand_percentage": 35.0, "silt_percentage": 31.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "annamayya": {
        "soil_ph": 6.8, "nitrogen": 248.0, "organic_carbon": 0.78,
        "clay_percentage": 27.0, "sand_percentage": 46.0, "silt_percentage": 27.0,
        "soil_type": "red loam", "state": "andhra pradesh",
    },
    "kakinada": {
        "soil_ph": 6.9, "nitrogen": 285.0, "organic_carbon": 1.1,
        "clay_percentage": 34.0, "sand_percentage": 35.0, "silt_percentage": 31.0,
        "soil_type": "alluvial", "state": "andhra pradesh",
    },
    "kona seema": {
        "soil_ph": 6.8, "nitrogen": 290.0, "organic_carbon": 1.1,
        "clay_percentage": 35.0, "sand_percentage": 34.0, "silt_percentage": 31.0,
        "soil_type": "alluvial", "state": "andhra pradesh",
    },
    "palnadu": {
        "soil_ph": 7.6, "nitrogen": 232.0, "organic_carbon": 0.62,
        "clay_percentage": 26.0, "sand_percentage": 48.0, "silt_percentage": 26.0,
        "soil_type": "black cotton", "state": "andhra pradesh",
    },
    "ntr": {
        "soil_ph": 7.5, "nitrogen": 238.0, "organic_carbon": 0.67,
        "clay_percentage": 28.0, "sand_percentage": 45.0, "silt_percentage": 27.0,
        "soil_type": "black cotton", "state": "andhra pradesh",
    },
    "sri sathya sai": {
        "soil_ph": 7.8, "nitrogen": 200.0, "organic_carbon": 0.40,
        "clay_percentage": 19.0, "sand_percentage": 60.0, "silt_percentage": 21.0,
        "soil_type": "red sandy", "state": "andhra pradesh",
    },
}


def find_soil_profile(location: str) -> dict:
    """
    Return a soil profile dict for *location*.
    """
    # 1. Start with a copy of the default profile
    profile = dict(_DEFAULT_PROFILE)

    # 2. Format the location string safely
    safe_location = location.lower().strip() if location else ""

    # 3. If the location exists in our DB, update the profile with its specific values
    if safe_location in _SOIL_DB:
        district_data = _SOIL_DB[safe_location]
        # Overwrite defaults with specific district data
        profile.update(district_data)
    else:
        print(f"[WARNING]: Location '{location}' not found in soil DB. Using defaults.")

    # 4. Attach the location strings
    profile["city"] = location
    profile["district"] = safe_location

    return profile