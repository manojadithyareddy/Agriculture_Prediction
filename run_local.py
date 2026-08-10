import subprocess
import sys
import time
import os

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print("🌾 Starting AgriPredict AI Full-Stack System...")
    print("==================================================")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "APP", "Backend")
    frontend_dir = os.path.join(root_dir, "APP", "Frontend")

    # 1. Start FastAPI Backend
    print("🚀 Launching FastAPI Backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir
    )
    
    # Wait briefly for backend to initialize
    time.sleep(2)
    
    # 2. Start Streamlit Frontend
    print("🚀 Launching Streamlit Frontend...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        cwd=frontend_dir
    )
    
    print("==================================================")
    print("✅ Backend running on: http://127.0.0.1:8000")
    print("✅ Frontend running on: http://localhost:8501")
    print("Press Ctrl+C to stop both servers.")
    print("==================================================")

    try:
        # Keep the script running until the user stops it
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    main()
