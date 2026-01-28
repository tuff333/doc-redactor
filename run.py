import subprocess
import time
import webbrowser
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

def main():
    env = os.environ.copy()

    # --- Start backend server ---
    backend_cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    backend_proc = subprocess.Popen(backend_cmd, cwd=BACKEND_DIR, env=env)

    # --- Start frontend HTTP server ---
    frontend_cmd = [
        sys.executable, "-m", "http.server", "5500"
    ]
    frontend_proc = subprocess.Popen(frontend_cmd, cwd=FRONTEND_DIR, env=env)

    # Give servers time to start
    time.sleep(3)

    # Open frontend in browser
    webbrowser.open("http://127.0.0.1:5500/index.html")

    print("Backend + Frontend running. Press Ctrl+C to stop both.")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
