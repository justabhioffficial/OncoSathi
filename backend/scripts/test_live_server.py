# -*- coding: utf-8 -*-
"""
Full-stack Verification Test Suite using FastAPI TestClient and HTTPX.
Tests all endpoints, static file serving, knowledge base, RAG retrieval,
simplification in English and Bengali, safety fallbacks, and dictionary search.
"""
import sys
import os
import json
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
BACKEND_DIR = WORKSPACE / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from app.main import app

def main():
    print("=" * 70)
    print("  ONCOSATHI AI — FULL-STACK VERIFICATION TEST SUITE")
    print("=" * 70)
    
    client = TestClient(app)
    results = []

    # 1. Health Check
    try:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["knowledge_base_ready"] is True
        print(f"[PASS] 1. Health Check: {data['app']} v{data['version']} (Terms: {data['total_terms']})")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 1. Health Check: {e}")
        results.append(False)

    # 2. Frontend SPA Web Page Serving
    try:
        resp = client.get("/")
        assert resp.status_code == 200
        content = resp.text
        assert "<title>OncoSathi AI" in content
        assert "React" in content or "react" in content
        assert "IJPC Cancer Glossary" in content
        print(f"[PASS] 2. Frontend SPA Web Page Serving: HTTP 200 ({len(content)} bytes)")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 2. Frontend SPA: {e}")
        results.append(False)

    # 3. Knowledge Status
    try:
        resp = client.get("/api/knowledge/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["chunks_count"] == 419
        assert len(data["source_documents"]) == 4
        print(f"[PASS] 3. Knowledge Base Status: {data['chunks_count']} Chunks from 4 verified primary sources")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 3. Knowledge Base Status: {e}")
        results.append(False)

    # 4. Terminology Search (English: 'biopsy')
    try:
        resp = client.get("/api/terms/search?q=biopsy")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["terms"]) > 0
        term_names = [t["term"] for t in data["terms"]]
        print(f"[PASS] 4. Terminology Search ('biopsy'): Found {len(data['terms'])} terms -> {term_names[:3]}")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 4. Terminology Search: {e}")
        results.append(False)

    # 5. Terminology Search (Bengali: 'বায়োপসি')
    try:
        resp = client.get("/api/terms/search?q=বায়োপসি")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["terms"]) > 0
        first = data["terms"][0]
        print(f"[PASS] 5. Bengali Term Search ('বায়োপসি'): Found {len(data['terms'])} terms -> {first['term']} ({first.get('bengali_term')})")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 5. Bengali Term Search: {e}")
        results.append(False)

    # 6. Simplification API (English Level 2)
    try:
        payload = {
            "text": "Malignant neoplasms are characterized by uncontrolled cellular proliferation with potential invasion and metastasis.",
            "target_language": "english",
            "simplification_level": 2
        }
        resp = client.post("/api/simplify", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["simplified_text"]) > 20
        assert len(data["key_points"]) > 0
        assert len(data["sources"]) > 0
        assert data["level"] == 2
        print(f"[PASS] 6. Simplification API (English Level 2): Generated {len(data['simplified_text'])} chars with {len(data['sources'])} sources")
        print(f"       -> Sample text: {data['simplified_text'][:80]}...")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 6. Simplification API (English): {e}")
        results.append(False)

    # 7. Simplification API (Bengali Level 1)
    try:
        payload = {
            "text": "What is chemotherapy and how does it affect cells in the body?",
            "target_language": "bengali",
            "simplification_level": 1
        }
        resp = client.post("/api/simplify", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["simplified_text"]) > 20
        assert data["language"] == "bengali"
        assert data["level"] == 1
        print(f"[PASS] 7. Simplification API (Bengali Level 1): Generated {len(data['simplified_text'])} chars")
        print(f"       -> Sample text: {data['simplified_text'][:80]}...")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 7. Simplification API (Bengali): {e}")
        results.append(False)

    # 8. Out-of-Domain Safety Guardrail
    try:
        payload = {
            "text": "What is the stock price of Apple computers in New York?",
            "target_language": "english",
            "simplification_level": 2
        }
        resp = client.post("/api/simplify", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "not available in the verified oncology sources" in data["simplified_text"]
        print(f"[PASS] 8. Medical Safety Guardrail: Successfully triggered clinical fallback for out-of-domain query")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 8. Medical Safety Guardrail: {e}")
        results.append(False)

    # 9. Feedback Recording API
    try:
        payload = {
            "query_text": "Malignant neoplasms test",
            "simplified_text": "Cancer cells grow uncontrollably.",
            "is_helpful": True,
            "rating": 5,
            "feedback_type": "asha_simplification"
        }
        resp = client.post("/api/feedback", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "recorded"
        print(f"[PASS] 9. Feedback API: Feedback recorded successfully")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 9. Feedback API: {e}")
        results.append(False)

    # 10. Text-to-Speech API
    try:
        payload = {
            "text": "ক্যানসার হলে শরীরের কোষ অনিয়ন্ত্রিতভাবে বাড়ে।",
            "language": "bengali",
            "speech_rate": 0.85
        }
        resp = client.post("/api/tts/speak", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["language_code"] == "bn-IN"
        print(f"[PASS] 10. Text-to-Speech API: Verified TTS config (Voice: {data['voice_name']}, Lang: {data['language_code']})")
        results.append(True)
    except Exception as e:
        print(f"[FAIL] 10. Text-to-Speech API: {e}")
        results.append(False)

    print("\n" + "=" * 70)
    if all(results):
        print(f" ALL {len(results)}/{len(results)} TESTS PASSED WITH 100% SUCCESS!")
    else:
        print(f" TESTS FAILED: {results.count(True)}/{len(results)} passed")
    print("=" * 70)

if __name__ == "__main__":
    main()
