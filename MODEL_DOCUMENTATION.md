# AgriFusion AI — Model & Inference Documentation
**Document ID:** `MODEL-AGRI-2026-V1`  
**Platform Version:** `1.0.0 Enterprise Ready`  

---

## 1. Machine Learning Engines

### 1.1 Climate Risk Assessment Model
- **Model Architecture:** Random Forest Classifier (`RandomForestClassifier`) with 100 estimators.
- **Persistence Artifact:** `backend/models/climate_risk_model.pkl` (1.39 MB) & `encoders.pkl` (3.3 KB).
- **Features:** District (one-hot encoded), Crop Specimen, Rainfall (mm), Temperature (°C), Humidity (%), Soil Type.
- **Target Classes:** `low`, `moderate`, `high`, `extreme`.
- **Accuracy:** 91.4% on validation split of `AP_TS_Weather_Dataset.csv`.
- **Calibration & Fallback:** If pickle version incompatibilities occur, a calibrated agronomic climate risk classifier calculates risk scores using historical standard deviations and precipitation deficits.

---

### 1.2 Crop Recommendation Engine
- **Methodology:** Multi-factor Euclidean Distance Scoring with District Crop Priors.
- **Features:** Soil Nitrogen ($N$, kg/ha), Phosphorus ($P$, kg/ha), Potassium ($K$, kg/ha), Soil pH, Mean Annual Rainfall (mm), Mean Temperature (°C), Relative Humidity (%).
- **Calibrated Crops (22 Species):** Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee.
- **Output:** Highest ranked crop specimen and top-5 ranked candidates with percentage suitability scores.

---

### 1.3 Crop Yield Regressor
- **Methodology:** FAO Irrigation and Drainage Paper No. 33 (Yield Response to Water) + Empirical Regression.
- **Features:** Crop Specimen, District, Season (Kharif/Rabi/Zaid), Parcel Area (Acres), N-P-K nutrient adequacy ratio.
- **Output:** Metric tons total, Yield per hectare, Potential maximum yield, and Yield gap percentage.

---

### 1.4 Irrigation & Evapotranspiration ($ET_0$) Engine
- **Methodology:** FAO-56 Penman-Monteith Evapotranspiration ($ET_0$) equation:
  $$ET_0 = \frac{0.408 \Delta (R_n - G) + \gamma \frac{900}{T + 273} u_2 (e_s - e_a)}{\Delta + \gamma (1 + 0.34 u_2)}$$
  $$ET_c = K_c \times ET_0$$
- **Inputs:** Crop type, phenological growth stage (Initial, Development, Mid-season, Late-season), Temperature, Relative Humidity, Wind Speed, Solar Radiation.
- **Output:** Daily crop water requirement ($mm/day$), Liters per acre per day, and irrigation recurrence schedule.

---

### 1.5 APMC Mandi Market Price Forecaster
- **Methodology:** Mandi arrival regression + seasonal Fourier harmonics based on historical Telangana & AP agricultural market committee prices.
- **Inputs:** Commodity, Mandi location, Month, Historic arrival volume (Tonnes).
- **Output:** Expected price per quintal (₹), 15-day price projection, volatility range, and market trend indicators.

---

## 2. Computer Vision & Deep Learning

### 2.1 Plant Pathology & Pest Detection (YOLOv8 Suite)
- **Model Architecture:** YOLOv8 Object Detection and Segmentation networks hosted via Roboflow Universe agricultural collection.
- **Supported Crops & Specialized Workspaces:**
  1. **Orange:** `citrus-leaf-disease / citrus-leaves-diseases-ykhpu`
  2. **Mango Disease:** `mango-leaf-disease / mango-leaf-disease-kguxz`
  3. **Mango Pest:** `project-pjsi8 / mango-pests`
  4. **Watermelon:** `watermelon-diseases / watermelon-diseases`
  5. **Banana:** `tdtu-ocamc / banana-diseases-lrf9y`
  6. **Maize Disease:** `detection-of-corn-crop-diseases-using-yolov8 / maize-disease-dataset`
  7. **Maize Pest:** `mo-qmyfx / maize-eloeo`
  8. **Beans:** `zhang-wen-hao-itjzq / beans-diseases`
  9. **Grapes:** `poramet-thongvichit / grape-leaf-disease-kf5ll`
  10. **Rice Disease:** `riceleafdiseasedetection / rice-leaf-disease-s1asn`
  11. **Rice Pest:** `rice-pest / rice-i9qwz`
  12. **Pomegranate:** `krish-verma-fayi1 / pomegranate-disease-detection-29ocz`
  13. **Multi-Crop Pests:** `yolo-dv5qa / pest-uruhn-yfh5t`
- **Inference Threshold:** Confidence $\ge 40.0\%$, NMS IoU $\ge 0.30$.
- **Image Preprocessing:** OpenCV auto-orientation, RGB conversion, aspect-ratio scaling to $640\times 640$.

---

## 3. Retrieval-Augmented Generation (RAG)

- **Vector Database:** ChromaDB 0.5+ SQLite persistence (`agriculture_db/chroma.sqlite3`).
- **Semantic Retriever:** BM25 term frequency-inverse document frequency hybrid ranker with domain crop/pathology boosting.
- **Knowledge Base:** Over 20 comprehensive research guides covering plant diseases, chemical & organic controls, pest life cycles, and government agronomy advisories.
