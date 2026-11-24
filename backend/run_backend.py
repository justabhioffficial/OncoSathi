# -*- coding: utf-8 -*-
"""
OncoSathi AI - Main Server Launcher
Starts the FastAPI application and serves both the REST API and the React SPA.
"""
import sys
import os
from pathlib import Path

# Add backend directory to sys.path so 'app' imports resolve properly
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import uvicorn
from app.config import APP_NAME, APP_TAGLINE, HOST, PORT

if __name__ == "__main__":
    print(f"================================================================")
    print(f"  Starting {APP_NAME}")
    print(f"  {APP_TAGLINE}")
    print(f"  Target URL: http://{HOST}:{PORT}")
    print(f"  API Docs:   http://{HOST}:{PORT}/docs")
    print(f"================================================================")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)
