# AgriFusion AI — REST API Documentation
**Base URL:** `http://localhost:8000` (Development) / `https://api.agrifusion.ai` (Production)  
**API Specification:** OpenAPI 3.1.0 / Interactive Swagger Docs at `/docs`  
**Authentication:** Bearer JWT Token or API Key in `Authorization` header  

---

## 1. System Health & Observability

### `GET /api/v1/health`
Checks overall platform health, latency of connected services, database state, and active ML models.

**Sample Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "app_name": "AgriPredict AI & Agriculture Advisory API",
  "version": "1.0.0",
  "environment": "development",
  "gateway_latency_ms": 4.2,
  "database": {
    "supabase": "connected",
    "latency_ms": 112.5
  },
  "models": {
    "climate_risk_model": "loaded",
    "crop_recommendation": "active (physics/dataset calibrated)",
    "yield_prediction": "active (FAO calibrated)",
    "irrigation": "active (FAO-56 Penman-Monteith)",
    "market_price": "active (APMC seasonal Prophet/baseline)"
  },
  "services": [
    { "name": "FastAPI Gateway", "status": "Operational" },
    { "name": "Supabase PostgreSQL", "status": "Operational" },
    { "name": "ChromaDB Store", "status": "Operational" }
  ]
}
```

---

## 2. Machine Learning Prediction Endpoints

### `POST /api/v1/predict/climate-risk`
Evaluates climate vulnerability, drought risk, and extreme weather risk for a given crop in Andhra Pradesh / Telangana.

**Request Body:**
```json
{
  "location": "Hyderabad",
  "crop": "Rice"
}
```

**Response (200 OK):**
```json
{
  "location": "Hyderabad",
  "crop": "Rice",
  "climate_risk": "moderate",
  "confidence": 0.88,
  "probabilities": {
    "low": 0.12,
    "moderate": 0.88,
    "high": 0.0,
    "extreme": 0.0
  },
  "key_factors": [
    "Monsoon deviation factor within normal baseline",
    "Soil moisture reserves adequate for current vegetative stage"
  ],
  "advisory": "Standard irrigation intervals recommended. Monitor for sudden temperature spikes."
}
```

---

### `POST /api/v1/predict/crop-recommendation`
Recommends optimal crop specimens based on soil macronutrients (N, P, K), pH, and regional climate.

**Request Body:**
```json
{
  "location": "Hyderabad",
  "n": 60.0,
  "p": 45.0,
  "k": 50.0,
  "ph": 6.8,
  "rainfall": 720.0,
  "temperature": 27.5,
  "humidity": 65.0
}
```

**Response (200 OK):**
```json
{
  "recommended_crop": "karbuja(musk melon)",
  "suitability_score": 94.2,
  "top_5": [
    { "crop": "karbuja(musk melon)", "score": 94.2 },
    { "crop": "cotton", "score": 88.5 },
    { "crop": "maize", "score": 84.1 },
    { "crop": "rice", "score": 79.8 },
    { "crop": "banana", "score": 76.3 }
  ],
  "location": "Hyderabad"
}
```

---

### `POST /api/v1/predict/yield`
Estimates total harvest yield in tons/quintals per hectare based on parcel size and agronomic conditions.

**Request Body:**
```json
{
  "location": "Guntur",
  "crop": "Cotton",
  "area": 1.5
}
```

**Response (200 OK):**
```json
{
  "crop": "Cotton",
  "location": "Guntur",
  "area_ha": 1.5,
  "predicted_yield": 4.12,
  "yield_per_ha": 2.75,
  "potential_max_yield": 5.20,
  "yield_gap_pct": 20.7,
  "limiting_factors": ["Sub-optimal potassium availability"]
}
```

---

### `POST /api/v1/predict/irrigation`
Computes evapotranspiration ($ET_0$) and daily crop water requirements based on FAO-56 Penman-Monteith methodology.

**Request Body:**
```json
{
  "location": "Warangal",
  "crop": "Maize",
  "growth_stage": "Development"
}
```

**Response (200 OK):**
```json
{
  "crop": "Maize",
  "location": "Warangal",
  "growth_stage": "Development",
  "predicted_water_requirement_mm_per_day": 5.4,
  "liters_per_acre_per_day": 21850,
  "irrigation_frequency_days": 3,
  "details": {
    "et0_reference": 5.14,
    "kc_coefficient": 1.05
  }
}
```

---

### `POST /api/v1/predict/market-price`
Forecasts expected APMC Mandi commodity market prices per quintal.

**Request Body:**
```json
{
  "location": "Krishna",
  "commodity": "Banana",
  "arrival_quantity": 100.0
}
```

**Response (200 OK):**
```json
{
  "location": "Krishna",
  "commodity": "Banana",
  "predicted_price_per_quintal": 2250.0,
  "min_expected_price": 1950.0,
  "max_expected_price": 2550.0,
  "trend": "Bullish (+3.2% expected over next 15 days)"
}
```

---

## 3. Computer Vision & Plant Pathology

### `POST /api/v1/detect/disease`
Accepts multipart image upload (`image/jpeg`, `image/png`, `image/webp` up to 15MB) and evaluates plant leaf pathologies against 13 YOLOv8 models.

**Request (Multipart Form):**
- `file`: Binary image data
- `target_crop`: (Optional) `"Rice"`, `"Maize"`, `"Banana"`, `"Mango"`, `"Orange"`, `"Watermelon"`, `"Grapes"`, `"Beans"`, `"Pomegranate"`

**Response (200 OK):**
```json
{
  "status": "detected",
  "crop": "Banana",
  "condition": "Black Sigatoka",
  "category": "Disease",
  "confidence": 0.88,
  "best_model": "Banana Disease YOLOv8",
  "total_detections": 2,
  "all_detections": [
    {
      "class_name": "Black Sigatoka",
      "confidence": 88.0,
      "bbox": [240, 180, 60, 80]
    }
  ],
  "annotated_image_base64": "data:image/jpeg;base64,...",
  "suggested_actions": [
    "Prune heavily infected lower leaves to minimize spore transmission.",
    "Apply systemic fungicide (e.g., Propiconazole or Azoxystrobin) under agronomist guidance."
  ]
}
```

---

## 4. AI Agronomist Chat & Multi-Modal Agent

### `POST /api/v1/chat/message`
Semantic retrieval-augmented advisory grounded in agricultural documentation.

**Request Body:**
```json
{
  "message": "What are the symptoms and treatment of Banana Black Sigatoka?",
  "crop": "Banana",
  "condition": "Black Sigatoka"
}
```

### `POST /api/v1/agent/diagnose`
Autonomous diagnostic engine receiving visual detection and farmer context to build actionable field remediation protocols.

**Request Body:**
```json
{
  "image_result": {
    "crop": "Banana",
    "condition": "Black Sigatoka",
    "category": "Disease",
    "confidence": 0.88
  },
  "farmer_question": "What immediate chemical spray should I use?"
}
```

---

## 5. Standard Error Codes

| Status Code | Code Name | Description |
| :--- | :--- | :--- |
| **400** | Bad Request | Invalid parameter ranges or unsupported file MIME type. |
| **404** | Not Found | Requested record, session, or route does not exist. |
| **422** | Unprocessable Entity | Pydantic payload validation error (missing required keys). |
| **429** | Too Many Requests | Rate limit exceeded (100 req/min per IP). |
| **500** | Internal Error | Sanitized error response; stack traces omitted from client output. |
