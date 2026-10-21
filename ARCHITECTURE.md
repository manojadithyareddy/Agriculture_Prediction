# AgriFusion AI — Enterprise System Architecture & 1M-User Scale Blueprint
**Document ID:** `ARCH-AGRI-2026-V1`  
**Platform Version:** `1.0.0 Enterprise Ready`  
**Target Concurrency:** 1,000,000 Registered Users / 10,000+ Active Peak Concurrency  

---

## 1. Architectural Overview

AgriFusion AI employs a decoupled, multi-tier asynchronous architecture designed to segregate lightweight API/BFF traffic from heavy machine learning, computer vision, and retrieval-augmented generation (RAG) workloads.

```
                                  CLIENT TIER
                 ┌──────────────────────────────────────────────┐
                 │ Next.js 14 Responsive Web Application        │
                 │ (React 18 SSR/CSR, TailwindCSS, Lucide UI)   │
                 └──────────────────────┬───────────────────────┘
                                        │ HTTPS / WSS
                                        ▼
                                 EDGE / CDN TIER
                 ┌──────────────────────────────────────────────┐
                 │ Cloudflare / CloudFront CDN                  │
                 │ • Static Assets & 3D Imagery Caching         │
                 │ • WAF & Rate Limiting (DDoS Mitigation)      │
                 │ • TLS 1.3 Termination & Geo-Routing          │
                 └──────────────────────┬───────────────────────┘
                                        │
                                        ▼
                                 API GATEWAY / BFF
                 ┌──────────────────────────────────────────────┐
                 │ FastAPI Core Asynchronous Gateway (Port 8000)│
                 │ • Input Validation via Pydantic v2           │
                 │ • JWT Authentication & RBAC                  │
                 │ • Circuit Breakers & Request Throttling      │
                 └───────┬──────────────┬───────────────┬───────┘
                         │              │               │
         ┌───────────────┘              │               └───────────────┐
         ▼                              ▼                               ▼
  SYNCHRONOUS ML ENGINES     ASYNCHRONOUS CV / RAG QUEUE       DATA & STORAGE TIER
┌─────────────────────────┐  ┌─────────────────────────┐  ┌───────────────────────────┐
│ In-Memory Model Cache   │  │ Redis / Celery Workers  │  │ Supabase PostgreSQL       │
│ • Climate Risk Forest   │  │ • Multi-Crop YOLOv8     │  │ (PgBouncer Connection Pool)│
│ • Crop Recommendation   │  │ • OpenCV Batch Pipeline │  │                           │
│ • FAO-56 Yield Regressor│  │ • ChromaDB Vector Store │  │ S3 / Supabase Storage     │
│ • Penman-Monteith ET0   │  │ • LLM Agronomist Agent  │  │ (Encrypted Leaf Imagery)  │
│ • Mandi Price Prophet   │  │                         │  │                           │
└─────────────────────────┘  └─────────────────────────┘  └───────────────────────────┘
```

---

## 2. 10 Lakh (1,000,000) User Scaling Strategy

Supporting 1,000,000 registered users with peak concurrent agronomic advisory demand (e.g., during monsoon sowing seasons) requires horizontal isolation of bottlenecks.

### 2.1 Stateless API Replicas & Auto-Scaling
- The FastAPI gateway is completely stateless; session tokens are validated cryptographically via JWT.
- Containerized instances run across Kubernetes (EKS/GKE) with Horizontal Pod Autoscaler (HPA) targeting CPU utilization at 70% and latency p95 < 250ms.

### 2.2 Inference Isolation & Queueing
- Machine learning models (`climate_risk_model.pkl`, Crop FAO engine, Yield regressor) are pre-warmed in-memory upon worker startup using singleton lifecycle events. Never reload weights per request.
- Heavy computer vision requests (15MB leaf photos) and multi-document RAG queries are queued through Redis/Celery background workers with worker pool autoscaling.
- The web client receives an asynchronous task ID (`/api/v1/tasks/{task_id}`) with live polling or WebSocket push, preventing HTTP timeout bottlenecks.

### 2.3 Multi-Tier Caching
1. **Edge CDN (L1):** Caches static images, crop 3D visuals, and landing page assets (Cache-Control: public, max-age=31536000).
2. **Redis Memory Cache (L2):** Caches regional weather metrics (`AP_TS_Weather_Dataset`) and Mandi market commodity averages with 1-hour TTL.
3. **Database Query Cache (L3):** Repeated agronomic lookups by district/season are served from in-memory LRU cache.

### 2.4 Database Connection Management
- Uses **Supabase Transaction Connection Pooling (PgBouncer)** to support thousands of concurrent connections while limiting active PostgreSQL server processes to 50-100 connections.
- Prediction log insertions are executed asynchronously via non-blocking background threads (`save_prediction_to_supabase`).

---

## 3. Resilience & SRE Patterns

1. **Circuit Breakers:** External integrations (e.g., Open-Meteo, Roboflow API) are wrapped with 3-second timeouts and fallback mechanisms. If the external weather API is degraded, the system automatically falls back to `AP_TS_Weather_Dataset.csv`.
2. **Graceful Degradation:** If heavy DL models experience peak queue depth, inference switches to fast local visual feature extraction and heuristic risk scoring.
3. **Health & Readiness Probes:**
   - `/api/v1/health` verifies gateway latency, Supabase connectivity, loaded ML models, and ChromaDB availability.
