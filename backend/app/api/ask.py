# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from app.models.schemas import AskRequest, AskResponse
from app.services.retrieval_service import RetrievalService
from app.services.simplification_service import SimplificationService

router = APIRouter()
retrieval_service = RetrievalService()
simplification_service = SimplificationService(retrieval_service)

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    return simplification_service.answer_question(
        question=request.question.strip(),
        target_language=request.target_language,
        level=request.level
    )
