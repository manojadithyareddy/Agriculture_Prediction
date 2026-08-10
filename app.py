"""
AgriPredict AI — Root Entrypoint for Streamlit & Streamlit Cloud Deployment
"""
import os
import sys
import runpy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "APP", "Frontend")
BACKEND_DIR = os.path.join(ROOT_DIR, "APP", "Backend")

if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

app_target = os.path.join(FRONTEND_DIR, "app.py")
runpy.run_path(app_target, run_name="__main__")
