# -*- coding: utf-8 -*-
import sys, os
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.config import SOURCE_DOCS_DIR
from app.services.extraction_service import ExtractionService
from app.services.retrieval_service import RetrievalService
from app.services.simplification_service import SimplificationService
from app.services.terminology_service import TerminologyService

def test_source_extraction():
    f1 = os.path.join(SOURCE_DOCS_DIR, "1_ijpc_cancer_glossary.pdf")
    f2 = os.path.join(SOURCE_DOCS_DIR, "2_medical_oncology_terminology_ba.pdf")
    f3 = os.path.join(SOURCE_DOCS_DIR, "3_cancer_terminology_bengali_english.docx")
    f4 = os.path.join(SOURCE_DOCS_DIR, "4_oncology_comprehensive_tables.csv")
    assert os.path.exists(f1) and os.path.exists(f2) and os.path.exists(f3) and os.path.exists(f4)
    raw1 = ExtractionService.extract_from_pdf(f1)
    raw3 = ExtractionService.extract_from_docx(f3)
    raw4 = ExtractionService.extract_from_csv(f4)
    assert len(raw1) > 0 and len(raw3) > 50 and len(raw4) > 50
    print("test_source_extraction passed!")

def test_retrieval_service():
    retriever = RetrievalService()
    assert retriever.load_processed_data() is True
    r1 = retriever.hybrid_retrieve("biopsy needle histopathology", top_k=3)
    assert len(r1) > 0 and any("biopsy" in r["text"].lower() for r in r1)
    b_query = "\u09b8\u09cd\u09a4\u09a8\u09c7\u09b0 \u0995\u09cd\u09af\u09be\u09a8\u09b8\u09be\u09b0"
    r2 = retriever.hybrid_retrieve(b_query, top_k=3)
    assert len(r2) > 0
    print("test_retrieval_service passed!")

def test_simplification_service_english():
    retriever = RetrievalService()
    retriever.load_processed_data()
    sim_service = SimplificationService(retriever)
    res_en = sim_service.simplify_text(
        text="Malignant neoplasms are characterized by uncontrolled cellular proliferation with potential invasion and metastasis.",
        target_language="en",
        level="level_2"
    )
    assert len(res_en.simplified_text) > 10 and len(res_en.key_points) > 0 and len(res_en.sources) > 0
    print("test_simplification_service_english passed!")

def test_simplification_service_bengali():
    retriever = RetrievalService()
    retriever.load_processed_data()
    sim_service = SimplificationService(retriever)
    res_bn = sim_service.simplify_text(
        text="Patient diagnosed with invasive ductal carcinoma requiring core needle biopsy and chemotherapy.",
        target_language="bn",
        level="level_1"
    )
    assert res_bn.target_language == "bn" and len(res_bn.simplified_text) > 10 and len(res_bn.key_points) > 0
    print("test_simplification_service_bengali passed!")

def test_terminology_service():
    term_service = TerminologyService()
    tot, items = term_service.search_terms(query="biopsy")
    assert tot > 0 and any("biopsy" in i.term.lower() for i in items)
    tot_b, items_b = term_service.search_terms(query="\u0995\u09cd\u09af\u09be\u09a8\u09b8\u09be\u09b0")
    assert tot_b > 0
    print("test_terminology_service passed!")

def test_missing_info_safety_fallback():
    retriever = RetrievalService()
    retriever.load_processed_data()
    sim_service = SimplificationService(retriever)
    res_missing = sim_service.answer_question(
        question="What is the stock price of Apple on NASDAQ tomorrow?",
        target_language="en",
        level="level_2"
    )
    assert "couldn't find enough reliable information" in res_missing.answer.lower()
    print("test_missing_info_safety_fallback passed!")

if __name__ == "__main__":
    test_source_extraction()
    test_retrieval_service()
    test_simplification_service_english()
    test_simplification_service_bengali()
    test_terminology_service()
    test_missing_info_safety_fallback()
    print("\nALL 6 CORE SYSTEM PIPELINE TESTS COMPLETED 100% OK!")
