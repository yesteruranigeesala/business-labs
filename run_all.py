"""
=============================================================================
AI TECH CONSULTANT — MASTER ORCHESTRATION LAUNCHER
Runs Task 1 (Knowledge Brain), Task 2 (Inbox Agent), Task 3 (Meeting to Scope),
and the Frontend Executive Command Center with a single command.
=============================================================================
"""
import os
import sys
import time
import subprocess
import signal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

TASK1_DIR = BASE_DIR / "task1-knowledge-brain"
TASK2_DIR = BASE_DIR / "task2-inbox-agent"
TASK3_DIR = BASE_DIR / "task3-meeting-to-scope"
FRONTEND_DIR = BASE_DIR / "frontend-dashboard"

processes = []

def cleanup(sig=None, frame=None):
    print("\n[Shutting down AI Tech Consultant Services...]")
    for p in processes:
        try:
            p.terminate()
            p.kill()
        except Exception:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    print("=" * 80)
    print("           AI TECH CONSULTANT - EXECUTIVE LAUNCHER")
    print("   JD4 Capstone Architecture - BusinessLabs Applied AI Dev/Engineer")
    print("=" * 80)

    # 1. Start Task 1: Knowledge Brain (Python FastAPI)
    print("\n[1/4] Starting Task 1: Knowledge Brain Service (Python FastAPI, Port 8001)...")
    p1 = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd=str(TASK1_DIR)
    )
    processes.append(p1)

    # 2. Start Task 2: Inbox Agent (TypeScript / Node.js)
    print("[2/4] Starting Task 2: Autonomous Inbox Agent (TypeScript Node.js, Port 8002)...")
    p2 = subprocess.Popen(
        ["node", "dist/server.js"],
        cwd=str(TASK2_DIR),
        shell=True
    )
    processes.append(p2)

    # 3. Start Task 3: Meeting to Scope (Python FastAPI)
    print("[3/4] Starting Task 3: Meeting to Scope Service (Python FastAPI, Port 8003)...")
    p3 = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8003"],
        cwd=str(TASK3_DIR)
    )
    processes.append(p3)

    # 4. Start Executive Command Center Frontend (Port 8000)
    print("[4/4] Starting Executive Command Center Dashboard (Port 8000)...")
    p4 = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000", "--directory", str(FRONTEND_DIR)],
        cwd=str(BASE_DIR)
    )
    processes.append(p4)

    time.sleep(2)
    print("\n" + "=" * 80)
    print("                  ALL SERVICES ARE LIVE AND CONNECTED!")
    print("=" * 80)
    print("  -> Frontend Dashboard:     http://localhost:8000")
    print("  -> Task 1 Knowledge Brain: http://localhost:8001/docs")
    print("  -> Task 2 Inbox Agent:     http://localhost:8002/health")
    print("  -> Task 3 Meeting-to-Scope: http://localhost:8003/docs")
    print("=" * 80)
    print("Press Ctrl+C to terminate all services.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
