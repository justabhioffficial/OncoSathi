# -*- coding: utf-8 -*-
from fastapi import APIRouter
from app.models.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter()
FEEDBACK_STORE = []

@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest):
    FEEDBACK_STORE.append(request.dict())
    return FeedbackResponse(
        success=True,
        message="Thank you! Your feedback has been recorded to improve ASHA healthcare simplifications."
    )
