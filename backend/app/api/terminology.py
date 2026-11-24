# -*- coding: utf-8 -*-
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from app.models.schemas import TermSearchResponse, TermItem
from app.services.terminology_service import TerminologyService

router = APIRouter()
terminology_service = TerminologyService()

@router.get("/terms/search", response_model=TermSearchResponse)
def search_terms(
    q: Optional[str] = Query(default="", description="Search query in English or Bengali"),
    category: Optional[str] = Query(default=None, description="Category filter"),
    limit: int = Query(default=30, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    # Support both FastAPI dependency injection and direct function calls
    real_q = (q.default if hasattr(q, "default") else q) or ""
    real_cat = category.default if hasattr(category, "default") else category
    real_lim = int(limit.default if hasattr(limit, "default") else limit)
    real_off = int(offset.default if hasattr(offset, "default") else offset)

    total, items = terminology_service.search_terms(query=real_q, category=real_cat, limit=real_lim, offset=real_off)
    return TermSearchResponse(query=real_q, category_filter=real_cat, total=total, results=items)

@router.get("/terms/categories", response_model=List[str])
def get_categories():
    return terminology_service.get_all_categories()

@router.get("/terms/{term_id}", response_model=TermItem)
def get_term_details(term_id: str):
    item = terminology_service.get_term_by_id(term_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Medical term '{term_id}' not found.")
    return item
