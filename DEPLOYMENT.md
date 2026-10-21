# AgriFusion AI — Enterprise Deployment Guide
**Document ID:** `DEP-AGRI-2026-V1`  
**Deployment Models:** Docker Containers, Kubernetes (EKS/GKE), Render, Vercel, Supabase Cloud  

---

## 1. Local & Production Run Scripts

### 1.1 Master Full-Stack Launcher (`app.py`)
Runs both the FastAPI backend (port 8000) and Next.js frontend (port 3000/3001) concurrently with automatic Supabase connection verification:

```bash
# From repository root
python app.py
```

### 1.2 Dedicated Backend Launcher:
```bash
cd "ML Project/backend"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 1.3 Dedicated Frontend Production Build & Run:
```bash
cd "ML Project/frontend"
npm install
npm run build
npm run start -p 3000
```

---

## 2. Docker Containerization

The backend includes a production-grade multi-stage Dockerfile:

### `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run container:
```bash
docker build -t agrifusion-backend:1.0.0 ./backend
docker run -d -p 8000:8000 --env-file ./backend/.env agrifusion-backend:1.0.0
```

---

## 3. Render Deployment (`render.yaml`)

The repository provides a declarative `render.yaml` specification for zero-downtime deployment:

```yaml
services:
  - type: web
    name: agrifusion-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: APP_ENV
        value: production
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
```

---

## 4. Production Environment Variables Reference

| Variable Name | Environment | Required | Description |
| :--- | :--- | :---: | :--- |
| `APP_ENV` | Backend | Yes | `"production"`, `"staging"`, or `"development"` |
| `SUPABASE_URL` | Backend/Frontend | Yes | Supabase Project URL (`https://xyz.supabase.co`) |
| `SUPABASE_KEY` | Backend/Frontend | Yes | Supabase Anonymous Public API Key |
| `SUPABASE_SERVICE_KEY` | Backend | Optional | Supabase Admin Service Key for elevated operations |
| `ROBOFLOW_API_KEY` | Backend | Yes | API key for YOLO agricultural disease models |
| `CORS_ORIGINS` | Backend | Yes | Allowed domains (e.g. `["https://app.agrifusion.ai"]`) |
| `NEXT_PUBLIC_API_URL` | Frontend | Yes | URL to FastAPI backend (`http://localhost:8000` or production URL) |
