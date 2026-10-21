# 🌾 AgriFusion AI — Enterprise Agricultural Intelligence Platform

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/tests-12%2F12%20passing%20(100%25)-success.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg)]()
[![Next.js](https://img.shields.io/badge/Next.js-14.2.35-black.svg)]()
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20RLS-3ECF8E.svg)]()
[![Python](https://img.shields.io/badge/Python-3.14.2%2064--bit-blue.svg)]()

> A unified, production-ready AI agriculture platform combining **Machine Learning, Deep Learning (YOLOv8), OpenCV Computer Vision, NLP, RAG (ChromaDB), and Multi-Modal Agronomic Agents** with an enterprise Next.js 14 horizontal navigation web interface.

---

## 🚀 Key Modules & Capabilities

- **🌾 AI Predictions:**
  - **Climate Risk Assessment:** Random Forest model evaluating extreme weather and drought risk.
  - **Crop Recommendation:** Multi-nutrient (N-P-K, pH, climate) crop suitability ranking across 22 cultivars.
  - **Yield Prediction:** Regressor based on FAO irrigation criteria calculating yield per hectare and yield gap.
  - **Irrigation Scheduling:** FAO-56 Penman-Monteith Evapotranspiration ($ET_0$) calculation with water volume requirements.
  - **Market Price Forecast:** Commodity price projection for Andhra Pradesh and Telangana APMC Mandis.
- **🔬 Computer Vision & Plant Pathology:**
  - **YOLOv8 Suite:** 13 models detecting diseases and pests across Rice, Maize, Cotton, Banana, Mango, Orange, Watermelon, Grapes, Beans, and Pomegranate.
  - **OpenCV Pipeline:** Automated image annotation, dynamic bounding box scaling, and visual diagnosis.
- **💬 AI Agronomist & RAG Knowledge Base:**
  - Semantic retrieval across agricultural research manuals backed by ChromaDB vector store.
  - Multi-modal diagnostic agent providing prioritized emergency action plans.
- **📊 Enterprise Command Center & Analytics:**
  - Real-time telemetry, model latency benchmarks, and weather radar powered by Supabase PostgreSQL.

---

## 📁 Repository Structure

```text
├── app.py                     # Root launcher delegating to ML Project
└── ML Project/
    ├── app.py                 # Master full-stack orchestrator (FastAPI + Next.js + DB check)
    ├── backend/
    │   ├── app/
    │   │   ├── api/v1/        # FastAPI v1 routers (predictions, detection, chat, agent, health)
    │   │   ├── ml/            # Machine Learning inference engines
    │   │   ├── dl/            # YOLOv8 disease detector & OpenCV pipeline
    │   │   ├── rag/           # ChromaDB vector store & knowledge base
    │   │   ├── agent/         # Multi-modal agronomic diagnostic agent
    │   │   └── database/      # Supabase cloud client & asynchronous logger
    │   ├── models/            # Pickle weights (climate_risk_model.pkl, encoders.pkl)
    │   ├── tests/             # Pytest automated test suite (12 test cases)
    │   └── Dockerfile         # Production multi-stage Dockerfile
    ├── frontend/
    │   ├── app/               # Next.js 14 App Router (13 fully styled production routes)
    │   ├── components/        # Horizontal Header, Mega-menus, Context Bar, Command Palette
    │   └── public/images/     # High-resolution agricultural visual assets
    ├── agriculture_db/        # ChromaDB SQLite vector store
    ├── Data/                  # AP_TS_Weather_Dataset.csv (182MB regional historical records)
    └── docs/
        ├── PROJECT_AUDIT.md
        ├── ARCHITECTURE.md
        ├── API_DOCUMENTATION.md
        ├── DATABASE.md
        ├── MODEL_DOCUMENTATION.md
        ├── SECURITY.md
        ├── PERFORMANCE.md
        ├── TESTING.md
        ├── DEPLOYMENT.md
        └── TROUBLESHOOTING.md
```

---

## ⚡ Quick Start

### 1. Launch Everything Concurrently:
```bash
python app.py
```
This automatically initializes the FastAPI backend on `http://localhost:8000`, the Next.js web application on `http://localhost:3000` (or `3001`), and performs database connectivity checks.

### 2. Run Test Suite:
```bash
cd "ML Project"
python -m pytest backend/tests -v
```

### 3. Run Benchmark Suite:
```bash
python scratch/load_test.py
```
*(Demonstrates 125.74 req/sec throughput with 0% error rate under 50 concurrent workers).*

---

## 📚 Complete Enterprise Documentation Suite

Detailed production documentation is available in the project root:
- [`PROJECT_AUDIT.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/PROJECT_AUDIT.md) — Comprehensive component-by-component audit
- [`ARCHITECTURE.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/ARCHITECTURE.md) — 1M-user scalability blueprint & decoupled worker queue architecture
- [`API_DOCUMENTATION.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/API_DOCUMENTATION.md) — Complete REST API schemas and request/response specifications
- [`DATABASE.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/DATABASE.md) — Supabase PostgreSQL schema, tables, indexes, and RLS policies
- [`MODEL_DOCUMENTATION.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/MODEL_DOCUMENTATION.md) — ML, DL, CV, and RAG model specifications & metrics
- [`SECURITY.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/SECURITY.md) — Secrets hygiene, CORS, upload defenses, and sanitization standards
- [`PERFORMANCE.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/PERFORMANCE.md) — Empirical load testing benchmarks & latency percentiles
- [`TESTING.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/TESTING.md) — Automated test reports, workflows, and test commands
- [`DEPLOYMENT.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/DEPLOYMENT.md) — Docker, Kubernetes, and Cloud deployment configurations
- [`TROUBLESHOOTING.md`](file:///c:/Users/madit/OneDrive/Desktop/dl%20Internship/ML%20Project/TROUBLESHOOTING.md) — Diagnostic quick-checks, incident response, and bug resolutions