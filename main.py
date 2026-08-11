"""
AgriPredict AI — Root Entrypoint for FastAPI Backend Deployment
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "APP", "Frontend")
BACKEND_DIR = os.path.join(ROOT_DIR, "APP", "Backend")

if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from APP.Backend.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
