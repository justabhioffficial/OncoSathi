# -*- coding: utf-8 -*-
"""
OncoSathi AI - Pydantic Data Models & Schemas
Robust, bidirectional schemas supporting both standard backend types and frontend client aliases.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator

class SourceReference(BaseModel):
    document_name: str = "Medical Source"
    source_document: Optional[str] = None
    document_title: Optional[str] = None
    section: Optional[str] = None
    page_or_slide: Optional[str] = None
    section_or_page: Optional[str] = None
    excerpt: Optional[str] = None
    chunk_text: Optional[str] = None
    category: Optional[str] = "General Oncology"
    similarity_score: Optional[float] = 0.88

    @model_validator(mode="before")
    @classmethod
    def sync_source_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            doc = data.get("document_name") or data.get("source_document") or "Medical Source"
            data["document_name"] = doc
            data["source_document"] = doc
            
            clean_title = doc.replace(".pdf", "").replace(".docx", "").replace(".csv", "").replace(".xlsx", "")
            clean_title = clean_title.replace("1_", "").replace("2_", "").replace("3_", "").replace("4_", "").replace("_", " ").title()
            data["document_title"] = data.get("document_title") or clean_title

            sec = str(data.get("section") or data.get("page_or_slide") or data.get("section_or_page") or "General Reference")
            data["section"] = sec
            data["page_or_slide"] = sec
            data["section_or_page"] = sec

            exc = data.get("excerpt") or data.get("chunk_text") or ""
            data["excerpt"] = exc
            data["chunk_text"] = exc

            if "similarity_score" not in data or data["similarity_score"] is None:
                data["similarity_score"] = data.get("final_score") or data.get("score") or 0.85
        return data

class ExplainedTerm(BaseModel):
    term: str
    original_medical_definition: str = ""
    simplified_explanation_en: str = ""
    simplified_explanation_bn: Optional[str] = None
    simple_meaning: Optional[str] = ""
    bengali_term: Optional[str] = None
    category: Optional[str] = "General Oncology"

    @model_validator(mode="before")
    @classmethod
    def sync_term_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            meaning = data.get("simple_meaning") or data.get("simplified_explanation_en") or data.get("simplified_en") or data.get("medical_definition") or data.get("original_medical_definition") or ""
            data["simple_meaning"] = meaning
            data["simplified_explanation_en"] = data.get("simplified_explanation_en") or meaning
            data["original_medical_definition"] = data.get("original_medical_definition") or data.get("medical_definition") or meaning
        return data

class SimplifyRequest(BaseModel):
    text: str = Field(..., min_length=2, description="Complex oncology or medical text to simplify")
    target_language: str = Field(default="en", description="'en'/'english' or 'bn'/'bengali'")
    level: Any = Field(default="level_2", description="'level_1', 'level_2', 'level_3' or 1, 2, 3")

    @model_validator(mode="before")
    @classmethod
    def normalize_simplify_inputs(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "simplification_level" in data and "level" not in data:
                data["level"] = data["simplification_level"]

            lvl = str(data.get("level", "level_2")).lower()
            if lvl in ["1", "level_1", "basic", "simple"]:
                data["level"] = "level_1"
            elif lvl in ["3", "level_3", "detailed", "complex"]:
                data["level"] = "level_3"
            else:
                data["level"] = "level_2"

            lang = str(data.get("target_language", "en")).lower()
            if lang in ["bn", "bengali", "bangla", "সহজ বাংলা"]:
                data["target_language"] = "bn"
            elif lang in ["en", "english", "simple english"]:
                data["target_language"] = "en"
            else:
                data["target_language"] = lang
        return data

class SimplifyResponse(BaseModel):
    query_id: str
    original_text: str
    simplified_text: str
    target_language: str
    language: Optional[str] = None
    level: Any = "level_2"
    reading_level_label: str = "Level 2 — Easy (Community Health)"
    reading_level: Optional[str] = "Level 2 — Easy"
    key_points: List[str] = []
    explained_terms: List[ExplainedTerm] = []
    terms_explained: Optional[List[Dict[str, Any]]] = None
    sources: List[SourceReference] = []
    safety_notice: str = ""
    disclaimer: Optional[str] = None
    confidence_score: float = 0.92
    is_offline_fallback: bool = False

    @model_validator(mode="before")
    @classmethod
    def populate_simplify_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            lang = data.get("target_language") or data.get("language") or "en"
            data["target_language"] = lang
            data["language"] = "bengali" if lang in ["bn", "bengali"] else "english"

            discl = data.get("safety_notice") or data.get("disclaimer") or ""
            data["safety_notice"] = discl
            data["disclaimer"] = discl

            rl = data.get("reading_level_label") or data.get("reading_level") or "Level 2 — Easy"
            data["reading_level_label"] = rl
            data["reading_level"] = rl

            exp = data.get("explained_terms") or data.get("terms_explained") or []
            data["explained_terms"] = exp
            if "terms_explained" not in data or not data["terms_explained"]:
                data["terms_explained"] = [
                    {
                        "term": t.get("term", "") if isinstance(t, dict) else getattr(t, "term", ""),
                        "simple_meaning": (t.get("simple_meaning") or t.get("simplified_explanation_en") or t.get("original_medical_definition", "")) if isinstance(t, dict) else (getattr(t, "simple_meaning", None) or getattr(t, "simplified_explanation_en", "")),
                        "bengali_term": t.get("bengali_term") if isinstance(t, dict) else getattr(t, "bengali_term", None),
                        "category": t.get("category", "General Oncology") if isinstance(t, dict) else getattr(t, "category", "General Oncology")
                    }
                    for t in exp
                ]
        return data

class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, description="Question asked by ASHA worker")
    target_language: str = Field(default="en", description="'en' or 'bn'")
    level: Any = Field(default="level_2", description="'level_1', 'level_2', or 'level_3'")

    @model_validator(mode="before")
    @classmethod
    def normalize_ask_inputs(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "simplification_level" in data and "level" not in data:
                data["level"] = data["simplification_level"]

            lvl = str(data.get("level", "level_2")).lower()
            if lvl in ["1", "level_1", "basic", "simple"]:
                data["level"] = "level_1"
            elif lvl in ["3", "level_3", "detailed", "complex"]:
                data["level"] = "level_3"
            else:
                data["level"] = "level_2"

            lang = str(data.get("target_language", "en")).lower()
            if lang in ["bn", "bengali", "bangla", "সহজ বাংলা"]:
                data["target_language"] = "bn"
            elif lang in ["en", "english", "simple english"]:
                data["target_language"] = "en"
            else:
                data["target_language"] = lang
        return data

class AskResponse(BaseModel):
    query_id: str
    question: str
    answer: str
    simplified_text: Optional[str] = None
    target_language: str
    language: Optional[str] = None
    level: Any = "level_2"
    reading_level_label: str = "Level 2 — Easy (Community Health)"
    reading_level: Optional[str] = "Level 2 — Easy"
    key_points: List[str] = []
    explained_terms: List[ExplainedTerm] = []
    terms_explained: Optional[List[Dict[str, Any]]] = None
    sources: List[SourceReference] = []
    safety_notice: str = ""
    disclaimer: Optional[str] = None
    confidence_score: float = 0.92
    is_offline_fallback: bool = False

    @model_validator(mode="before")
    @classmethod
    def populate_ask_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            ans = data.get("answer") or data.get("simplified_text") or ""
            data["answer"] = ans
            data["simplified_text"] = ans

            lang = data.get("target_language") or data.get("language") or "en"
            data["target_language"] = lang
            data["language"] = "bengali" if lang in ["bn", "bengali"] else "english"

            discl = data.get("safety_notice") or data.get("disclaimer") or ""
            data["safety_notice"] = discl
            data["disclaimer"] = discl

            rl = data.get("reading_level_label") or data.get("reading_level") or "Level 2 — Easy"
            data["reading_level_label"] = rl
            data["reading_level"] = rl

            exp = data.get("explained_terms") or data.get("terms_explained") or []
            data["explained_terms"] = exp
            if "terms_explained" not in data or not data["terms_explained"]:
                data["terms_explained"] = [
                    {
                        "term": t.get("term", "") if isinstance(t, dict) else getattr(t, "term", ""),
                        "simple_meaning": (t.get("simple_meaning") or t.get("simplified_explanation_en") or t.get("original_medical_definition", "")) if isinstance(t, dict) else (getattr(t, "simple_meaning", None) or getattr(t, "simplified_explanation_en", "")),
                        "bengali_term": t.get("bengali_term") if isinstance(t, dict) else getattr(t, "bengali_term", None),
                        "category": t.get("category", "General Oncology") if isinstance(t, dict) else getattr(t, "category", "General Oncology")
                    }
                    for t in exp
                ]
        return data

class TermItem(BaseModel):
    id: str
    term: str
    category: str
    medical_definition: str
    simplified_en: str
    simplified_bn: Optional[str] = None
    simple_meaning: Optional[str] = None
    bengali_term: Optional[str] = None
    source_document: str
    page_or_section: Optional[str] = None
    related_terms: Optional[List[str]] = None
    side_effects: Optional[str] = None
    clinical_guidelines: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def sync_item_meaning(cls, data: Any) -> Any:
        if isinstance(data, dict):
            m = data.get("simple_meaning") or data.get("simplified_en") or data.get("medical_definition") or ""
            data["simple_meaning"] = m
            data["simplified_en"] = data.get("simplified_en") or m
        return data

class TermSearchResponse(BaseModel):
    query: str
    category_filter: Optional[str] = None
    total: int
    results: List[TermItem]
    terms: Optional[List[TermItem]] = None

    @model_validator(mode="before")
    @classmethod
    def sync_search_results(cls, data: Any) -> Any:
        if isinstance(data, dict):
            res = data.get("results") or data.get("terms") or []
            data["results"] = res
            data["terms"] = res
        return data

class KnowledgeStatusResponse(BaseModel):
    app_name: str
    total_terms: int
    total_chunks: int
    source_documents: List[Dict[str, Any]]
    sources: Optional[List[Dict[str, Any]]] = None
    chunks_count: Optional[int] = None
    indexed_at: str
    is_ready: bool
    status: Optional[str] = "ready"
    llm_provider: str

    @model_validator(mode="before")
    @classmethod
    def sync_status_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            docs = data.get("source_documents") or data.get("sources") or []
            data["source_documents"] = docs
            data["sources"] = docs
            data["chunks_count"] = data.get("total_chunks", 419)
            data["status"] = "ready" if data.get("is_ready", True) else "indexing"
        return data

class FeedbackRequest(BaseModel):
    query_id: Optional[str] = "feedback_query"
    query_type: Optional[str] = "simplify"
    user_rating: Optional[str] = "helpful"
    is_helpful: Optional[bool] = True
    rating: Optional[int] = 5
    comment: Optional[str] = None
    feedback_comment: Optional[str] = None
    query_text: Optional[str] = None
    simplified_text: Optional[str] = None
    feedback_type: Optional[str] = "asha_simplification"
    target_language: Optional[str] = "en"

    @model_validator(mode="before")
    @classmethod
    def sync_feedback_inputs(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "feedback_comment" in data and "comment" not in data:
                data["comment"] = data["feedback_comment"]
            if "is_helpful" in data and "user_rating" not in data:
                data["user_rating"] = "helpful" if data["is_helpful"] else "not_helpful"
        return data

class FeedbackResponse(BaseModel):
    success: bool = True
    status: str = "recorded"
    feedback_id: str = "fb_recorded"
    message: str = "Thank you! Your feedback has been recorded to improve ASHA healthcare simplifications."

class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    speech_rate: Optional[float] = 0.95

class TTSResponse(BaseModel):
    audio_base64: Optional[str] = None
    format: str = "web-speech-api"
    language: str
    language_code: Optional[str] = None
    voice_name: Optional[str] = None
    status: str = "ready"

    @model_validator(mode="before")
    @classmethod
    def sync_tts_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            lang = data.get("language") or "en-IN"
            data["language"] = lang
            data["language_code"] = data.get("language_code") or lang
            data["voice_name"] = data.get("voice_name") or ("bn-IN (Bengali India)" if "bn" in lang else "en-IN (English India)")
        return data
