import subprocess
import sys

print("Starting Streamlit...")
p = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "true"])
p.wait()
print("Streamlit exited with code", p.returncode)
