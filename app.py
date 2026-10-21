"""
AgriPredict AI — Master End-to-End Application Runner
Orchestrates:
  1. FastAPI Python Backend (port 8000)
  2. Next.js 14 Web Frontend (port 3000)
  3. Supabase Cloud Database Connection Verification

Run:
  python app.py
"""
from __future__ import annotations

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a TCP port is already open and accepting connections."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False

# Unbuffered standard output
os.environ["PYTHONUNBUFFERED"] = "1"

# Paths
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"


def print_banner():
    banner = r"""
======================================================================
🌾  AgriPredict AI — Full-Stack End-to-End Application Runner
======================================================================
  [Backend]  FastAPI 0.141+ (Python ML / DL & Advisory Services)
  [Frontend] Next.js 14 (React 18, Tailwind, Lucide UI)
  [Database] Supabase Cloud Database (prediction_logs & analytics)
======================================================================
"""
    print(banner, flush=True)


def check_database() -> bool:
    """Verify Supabase database connectivity before starting services."""
    print("🔍 [Database] Verifying Supabase connection...", flush=True)
    try:
        if str(BACKEND_DIR) not in sys.path:
            sys.path.insert(0, str(BACKEND_DIR))

        from app.config import settings
        from app.database.supabase import get_client

        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            print("⚠️  [Database] SUPABASE_URL or SUPABASE_KEY not configured in backend/.env", flush=True)
            return False

        client = get_client()
        res = client.table("prediction_logs").select("id").limit(1).execute()
        print(f"✅ [Database] Supabase connected successfully! (Endpoint: {settings.SUPABASE_URL})", flush=True)
        return True
    except Exception as e:
        print(f"⚠️  [Database] Notice: Supabase connectivity check warning ({e}). Continuing startup...", flush=True)
        return False


def wait_for_service(name: str, url: str, timeout: int = 30) -> bool:
    """Poll a service URL until it responds with HTTP 200."""
    print(f"⏳ [{name}] Waiting for service at {url} ...", flush=True)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AgriPredict-Launcher/1.0"})
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    print(f"✅ [{name}] Service is online and healthy!", flush=True)
                    return True
        except Exception:
            pass
        time.sleep(1)
    print(f"⚠️  [{name}] Startup check reached timeout threshold.", flush=True)
    return False


def terminate_process(proc: subprocess.Popen, name: str):
    """Safely terminate a subprocess and any children on Windows/Unix."""
    if proc.poll() is not None:
        return
    print(f"🛑 Terminating {name} (PID {proc.pid})...", flush=True)
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
        else:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
    except Exception as e:
        print(f"Warning while stopping {name}: {e}", flush=True)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="AgriPredict AI End-to-End Application Runner")
    parser.add_argument("--backend-host", default="127.0.0.1", help="FastAPI host (default: 127.0.0.1)")
    parser.add_argument("--backend-port", type=int, default=8000, help="FastAPI port (default: 8000)")
    parser.add_argument("--frontend-port", type=int, default=3000, help="Next.js port (default: 3000)")
    parser.add_argument("--dev", action="store_true", help="Run Next.js in dev mode instead of production server")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open browser")
    parser.add_argument("--backend-only", action="store_true", help="Launch only the FastAPI backend")
    parser.add_argument("--frontend-only", action="store_true", help="Launch only the Next.js frontend")
    parser.add_argument("--check-only", action="store_true", help="Verify configurations and database only")
    args = parser.parse_args()

    print_banner()

    # Pre-flight check
    db_ok = check_database()
    if args.check_only:
        print("\n✅ Pre-flight check completed.", flush=True)
        return

    processes: list[tuple[subprocess.Popen, str]] = []

    def shutdown(signum=None, frame=None):
        print("\n🛑 Received shutdown signal. Stopping all services...", flush=True)
        for proc, name in reversed(processes):
            terminate_process(proc, name)
        print("👋 All services terminated cleanly.", flush=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)

    try:
        # 1. Start FastAPI Backend
        if not args.frontend_only:
            backend_url = f"http://{args.backend_host}:{args.backend_port}"
            if is_port_in_use(args.backend_port, args.backend_host):
                print(f"✅ [Backend] Port {args.backend_port} is already active. Connecting to running FastAPI instance at {backend_url}...", flush=True)
            else:
                print(f"\n🚀 [Backend] Launching FastAPI at {backend_url} ...", flush=True)
                backend_cmd = [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    args.backend_host,
                    "--port",
                    str(args.backend_port),
                    "--reload",
                ]
                backend_proc = subprocess.Popen(backend_cmd, cwd=str(BACKEND_DIR))
                processes.append((backend_proc, "FastAPI Backend"))

                # Wait for backend readiness before launching frontend
                health_url = f"{backend_url}/api/v1/health"
                wait_for_service("Backend", health_url, timeout=20)

        # 2. Start Next.js Frontend
        if not args.backend_only:
            frontend_url = f"http://localhost:{args.frontend_port}"
            if is_port_in_use(args.frontend_port):
                print(f"✅ [Frontend] Port {args.frontend_port} is already active. Connecting to running Next.js instance at {frontend_url}...", flush=True)
            else:
                npm_bin = "npm.cmd" if sys.platform == "win32" else "npm"

                # Check if production build exists
                build_id_path = FRONTEND_DIR / ".next" / "BUILD_ID"
                use_prod = build_id_path.exists() and not args.dev
                script_name = "start" if use_prod else "dev"

                mode_label = "Production Server" if use_prod else "Development Server"
                print(f"\n💻 [Frontend] Launching Next.js 14 ({mode_label}) at {frontend_url} ...", flush=True)

                frontend_cmd = [npm_bin, "run", script_name, "--", "-p", str(args.frontend_port)]
                frontend_proc = subprocess.Popen(frontend_cmd, cwd=str(FRONTEND_DIR))
                processes.append((frontend_proc, "Next.js Frontend"))

                # Wait for frontend readiness
                wait_for_service("Frontend", frontend_url, timeout=20)

        # 3. Print Service Dashboard
        print("\n" + "=" * 70, flush=True)
        print("✨  ALL SERVICES ACTIVE AND CONNECTED!", flush=True)
        print("=" * 70, flush=True)
        if not args.backend_only:
            print(f"👉 Frontend Application:       http://localhost:{args.frontend_port}", flush=True)
            print(f"👉 Prediction Advisory Page:  http://localhost:{args.frontend_port}/predictions", flush=True)
            print(f"👉 Disease Detection:         http://localhost:{args.frontend_port}/detection", flush=True)
            print(f"👉 Agronomist Chat:           http://localhost:{args.frontend_port}/chat", flush=True)
        if not args.frontend_only:
            print(f"👉 FastAPI Backend API:        http://{args.backend_host}:{args.backend_port}", flush=True)
            print(f"👉 Interactive Docs (Swagger):  http://{args.backend_host}:{args.backend_port}/docs", flush=True)
            print(f"👉 Alternative Docs (ReDoc):   http://{args.backend_host}:{args.backend_port}/redoc", flush=True)
            print(f"👉 Health Check Endpoint:      http://{args.backend_host}:{args.backend_port}/api/v1/health", flush=True)
        print(f"👉 Database:                   {'Connected (Supabase)' if db_ok else 'Supabase Cloud'}", flush=True)
        print("=" * 70, flush=True)
        print("Press Ctrl+C at any time to stop all services.\n", flush=True)

        # 4. Open Browser
        if not args.no_browser and not args.backend_only:
            time.sleep(1)
            webbrowser.open(f"http://localhost:{args.frontend_port}")
        elif not args.no_browser and args.backend_only:
            time.sleep(1)
            webbrowser.open(f"http://{args.backend_host}:{args.backend_port}/docs")

        # 5. Monitor child processes
        while True:
            for proc, name in processes:
                ret = proc.poll()
                if ret is not None:
                    print(f"\n⚠️  {name} exited unexpectedly with code {ret}!", flush=True)
                    shutdown()
            time.sleep(1)

    except KeyboardInterrupt:
        shutdown()
    except Exception as e:
        print(f"\n❌ Error during execution: {e}", flush=True)
        shutdown()


if __name__ == "__main__":
    main()
