# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

# Ensure backend directory is in sys.path so 'app.*' imports work from any working directory
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import APP_NAME, APP_TAGLINE, APP_VERSION, LLM_PROVIDER
from app.api import simplify, ask, terminology, knowledge, feedback, tts
from app.services.retrieval_service import RetrievalService

app = FastAPI(
    title=APP_NAME,
    description=APP_TAGLINE,
    version=APP_VERSION
)

# Enable CORS for local dev, Netlify, and custom domains
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "*")
if allowed_origins_env == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup: initialize knowledge base and retrieval engine
@app.on_event("startup")
def startup_event():
    print(f"[{APP_NAME}] Initializing oncology retrieval and terminology engine...")
    retriever = RetrievalService()
    success = retriever.load_processed_data()
    print(f"[{APP_NAME}] Retrieval engine ready: {success}")

# Include API routes
app.include_router(simplify.router, prefix="/api", tags=["Simplification"])
app.include_router(ask.router, prefix="/api", tags=["Question Answering"])
app.include_router(terminology.router, prefix="/api", tags=["Terminology Dictionary"])
app.include_router(knowledge.router, prefix="/api", tags=["Knowledge Base"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(tts.router, prefix="/api", tags=["Text-to-Speech"])

@app.get("/api/health")
def health_check():
    retriever = RetrievalService()
    is_ready = retriever.load_processed_data()
    return {
        "status": "healthy",
        "app": APP_NAME,
        "tagline": APP_TAGLINE,
        "version": APP_VERSION,
        "knowledge_base_ready": is_ready,
        "total_terms": len(retriever.dictionary),
        "total_chunks": 419,
        "sources_count": 4,
        "llm_provider": LLM_PROVIDER
    }

# Frontend static serving
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
FRONTEND_PUBLIC = Path(__file__).resolve().parent.parent.parent / "frontend" / "public"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(FRONTEND_DIST / "index.html"))
elif FRONTEND_PUBLIC.exists() and (FRONTEND_PUBLIC / "index.html").exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PUBLIC)), name="static")

    @app.get("/{full_path:path}")
    def serve_public_spa(full_path: str):
        file_path = FRONTEND_PUBLIC / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(FRONTEND_PUBLIC / "index.html"))
