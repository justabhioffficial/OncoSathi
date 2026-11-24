# -*- coding: utf-8 -*-
import os, json, datetime
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks
from app.models.schemas import KnowledgeStatusResponse
from app.config import PROCESSED_DIR, SOURCE_DOCS_DIR, APP_NAME, LLM_PROVIDER

router = APIRouter()

@router.get("/knowledge/status", response_model=KnowledgeStatusResponse)
def get_knowledge_status():
    dict_file = Path(PROCESSED_DIR) / "terminology_dictionary.json"
    chunks_file = Path(PROCESSED_DIR) / "knowledge_chunks.json"

    total_terms = 0
    total_chunks = 0
    indexed_at = "Not yet indexed"
    is_ready = False

    if dict_file.exists():
        with open(dict_file, "r", encoding="utf-8") as f:
            total_terms = len(json.load(f))
        mtime = os.path.getmtime(str(dict_file))
        indexed_at = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    if chunks_file.exists():
        with open(chunks_file, "r", encoding="utf-8") as f:
            total_chunks = len(json.load(f))
        is_ready = total_terms > 0 and total_chunks > 0

    source_files = []
    source_dir = Path(SOURCE_DOCS_DIR)
    if source_dir.exists():
        for fpath in sorted(source_dir.iterdir()):
            if fpath.is_file():
                source_files.append({
                    "filename": fpath.name,
                    "size_bytes": fpath.stat().st_size,
                    "format": fpath.suffix.lstrip(".").upper()
                })

    return KnowledgeStatusResponse(
        app_name=APP_NAME,
        total_terms=total_terms,
        total_chunks=total_chunks,
        source_documents=source_files,
        indexed_at=indexed_at,
        is_ready=is_ready,
        llm_provider=LLM_PROVIDER
    )

@router.post("/knowledge/ingest")
def trigger_ingestion(background_tasks: BackgroundTasks):
    from scripts.ingest_documents import run_ingestion
    background_tasks.add_task(run_ingestion)
    return {"message": "Knowledge base ingestion triggered in background.", "status": "processing"}
