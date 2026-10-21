"""
start_production.py — Unified Production Launcher
Spawns both:
  1. FastAPI Python Backend on port 8000
  2. Next.js 14 Frontend on port 3000
"""
import os
import sys
import time
import subprocess
import webbrowser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

def main():
    print("=" * 65)
    print("🌾 AgriFusion AI — Unified Production Launcher")
    print("=" * 65)

    # 1. Start FastAPI Backend
    print("🚀 Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]
    backend_process = subprocess.Popen(backend_cmd, cwd=BACKEND_DIR)

    # Wait 2 seconds for backend to bind port
    time.sleep(2)

    # 2. Start Next.js Frontend
    print("💻 Starting Next.js Production Server on http://localhost:3000 ...")
    # Use npm run start (built production bundle) or npm run dev
    frontend_cmd = ["npm.cmd" if sys.platform == "win32" else "npm", "run", "start"]
    frontend_process = subprocess.Popen(frontend_cmd, cwd=FRONTEND_DIR)

    time.sleep(3)
    print("\n" + "=" * 65)
    print("✨ ALL SERVICES ONLINE!")
    print("👉 Frontend: http://localhost:3000")
    print("👉 Backend API: http://127.0.0.1:8000/docs")
    print("=" * 65)
    print("Press Ctrl+C to stop all services.\n")

    try:
        webbrowser.open("http://localhost:3000")
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
