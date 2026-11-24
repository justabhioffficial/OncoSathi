# -*- coding: utf-8 -*-
"""
OncoSathi AI - Root One-Click Launcher
Usage:
    python run.py
"""
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import uvicorn
from app.config import APP_NAME, APP_TAGLINE, HOST, PORT, LLM_PROVIDER

def main():
    print("=" * 70)
    print(f"  {APP_NAME} — {APP_TAGLINE}")
    print("=" * 70)
    print(f"  * Mode:          Offline Grounded Engine ({LLM_PROVIDER})")
    print(f"  * Web UI:        http://{HOST}:{PORT}")
    print(f"  * Interactive API: http://{HOST}:{PORT}/docs")
    print(f"  * Health Check:  http://{HOST}:{PORT}/api/health")
    print("=" * 70)
    print("  Server is launching. Press Ctrl+C to terminate.")
    print("=" * 70)
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)

if __name__ == "__main__":
    main()
