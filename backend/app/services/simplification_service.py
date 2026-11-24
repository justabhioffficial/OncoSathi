# -*- coding: utf-8 -*-
"""
Simplification Service for OncoSathi AI.
Coordinates hybrid knowledge retrieval, terminology matching, prompt engineering,
and multi-level medical simplification in English and Bengali.
"""
import uuid
from typing import Dict, Any, List
from app.config import MEDICAL_DISCLAIMER
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.models.schemas import SimplifyResponse, AskResponse, SourceReference, ExplainedTerm

LEVEL_LABELS = {
    "level_1": "Level 1 — Basic (Ultra-Simple)",
    "level_2": "Level 2 — Easy (Community Health)",
    "level_3": "Level 3 — Detailed (Clinical Summary)"
}

class SimplificationService:
    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service
        self.llm_service = LLMService()

    def simplify_text(self, text: str, target_language: str = "en", level: str = "level_2") -> SimplifyResponse:
        query_id = f"sim_{uuid.uuid4().hex[:8]}"

        # 1. Retrieve relevant oncology knowledge chunks
        retrieved_chunks = self.retrieval_service.hybrid_retrieve(text, top_k=4)

        # 2. Extract matching oncology terms present in the query
        matched_terms = self.retrieval_service.find_relevant_terms(text, max_terms=4)

        # 3. Generate simplification via Grounded Engine or Gemini
        simplified_text, key_points, is_offline = self.llm_service.generate_simplification(
            text=text,
            context_chunks=retrieved_chunks,
            explained_terms=matched_terms,
            target_language=target_language,
            level=level
        )

        # 4. Construct grounded source references
        sources = []
        for c in retrieved_chunks:
            sources.append(SourceReference(
                document_name=c.get("source_document", "Verified Medical Source"),
                section=c.get("section", "General Oncology"),
                page_or_slide=str(c.get("page", "1")),
                excerpt=c.get("text", ""),
                category=c.get("category", "Oncology Reference"),
                similarity_score=round(c.get("final_score", 0.88), 3)
            ))

        # 5. Format explained terms
        explained = []
        for t in matched_terms:
            explained.append(ExplainedTerm(
                term=t.get("term", ""),
                original_medical_definition=t.get("medical_definition", ""),
                simplified_explanation_en=t.get("simplified_en") or t.get("simple_meaning", ""),
                simplified_explanation_bn=t.get("simplified_bn") or t.get("bengali_term", ""),
                simple_meaning=t.get("simple_meaning") or t.get("simplified_en", ""),
                bengali_term=t.get("bengali_term", ""),
                category=t.get("category", "General Oncology")
            ))

        return SimplifyResponse(
            query_id=query_id,
            original_text=text,
            simplified_text=simplified_text,
            target_language=target_language,
            level=level,
            reading_level_label=LEVEL_LABELS.get(level, "Level 2 — Easy (Community Health)"),
            key_points=key_points,
            explained_terms=explained,
            sources=sources,
            safety_notice=MEDICAL_DISCLAIMER,
            is_offline_fallback=is_offline
        )

    def answer_question(self, question: str, target_language: str = "en", level: str = "level_2") -> AskResponse:
        query_id = f"ask_{uuid.uuid4().hex[:8]}"

        retrieved_chunks = self.retrieval_service.hybrid_retrieve(question, top_k=4)
        matched_terms = self.retrieval_service.find_relevant_terms(question, max_terms=4)

        answer_text, key_points, is_offline = self.llm_service.generate_simplification(
            text=question,
            context_chunks=retrieved_chunks,
            explained_terms=matched_terms,
            target_language=target_language,
            level=level
        )

        sources = []
        for c in retrieved_chunks:
            sources.append(SourceReference(
                document_name=c.get("source_document", "Verified Medical Source"),
                section=c.get("section", "General Oncology"),
                page_or_slide=str(c.get("page", "1")),
                excerpt=c.get("text", ""),
                category=c.get("category", "Oncology Reference"),
                similarity_score=round(c.get("final_score", 0.88), 3)
            ))

        explained = []
        for t in matched_terms:
            explained.append(ExplainedTerm(
                term=t.get("term", ""),
                original_medical_definition=t.get("medical_definition", ""),
                simplified_explanation_en=t.get("simplified_en") or t.get("simple_meaning", ""),
                simplified_explanation_bn=t.get("simplified_bn") or t.get("bengali_term", ""),
                simple_meaning=t.get("simple_meaning") or t.get("simplified_en", ""),
                bengali_term=t.get("bengali_term", ""),
                category=t.get("category", "General Oncology")
            ))

        return AskResponse(
            query_id=query_id,
            question=question,
            answer=answer_text,
            simplified_text=answer_text,
            target_language=target_language,
            level=level,
            reading_level_label=LEVEL_LABELS.get(level, "Level 2 — Easy (Community Health)"),
            key_points=key_points,
            explained_terms=explained,
            sources=sources,
            safety_notice=MEDICAL_DISCLAIMER,
            is_offline_fallback=is_offline
        )
