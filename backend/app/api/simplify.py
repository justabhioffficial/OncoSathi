# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import SimplifyRequest, SimplifyResponse
from app.services.retrieval_service import RetrievalService
from app.services.simplification_service import SimplificationService

router = APIRouter()
retrieval_service = RetrievalService()
simplification_service = SimplificationService(retrieval_service)

@router.post("/simplify", response_model=SimplifyResponse)
def simplify_text(request: SimplifyRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    
    return simplification_service.simplify_text(
        text=request.text.strip(),
        target_language=request.target_language,
        level=request.level
    )
