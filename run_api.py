# -*- coding: utf-8 -*-
"""
OncoSathi AI - Root API Launcher for Render / Cloud Hosting
Starts the FastAPI application and binds to 0.0.0.0 and $PORT.
"""
import sys
import os
from pathlib import Path

# Add backend directory to sys.path so 'app.*' imports resolve cleanly
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import uvicorn

if __name__ == "__main__":
    from app.config import HOST, PORT, APP_NAME
    port = int(os.environ.get("PORT", PORT))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"[{APP_NAME}] Starting production server on {host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
