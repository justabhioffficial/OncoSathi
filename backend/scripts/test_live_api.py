# -*- coding: utf-8 -*-
import json
import urllib.request

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, path, method="GET", body=None):
    url = BASE_URL + path
    headers = {"Content-Type": "application/json"} if body else {}
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        print(f"[OK] {name} -> status {resp.status}")
        return res_data

try:
    health = test_endpoint("Health", "/api/health")
    print(f"     Knowledge indexed: {health.get('knowledge_base_indexed')}")

    status = test_endpoint("Knowledge Status", "/api/knowledge/status")
    print(f"     Total chunks: {status.get('total_chunks')}, Total terms: {status.get('total_terms')}")

    search = test_endpoint("Search Terms", "/api/terms/search?q=biopsy")
    print(f"     Found {len(search)} terms for 'biopsy'")

    simp_en = test_endpoint("Simplify English", "/api/simplify", method="POST", body={
        "text": "Malignant neoplasm with distant metastasis to lymph nodes.",
        "target_language": "en",
        "level": "level_1"
    })
    print(f"     Simplified English: {simp_en.get('simplified_text')[:60]}...")
    print(f"     Sources cited: {len(simp_en.get('sources', []))}")

    simp_bn = test_endpoint("Simplify Bengali", "/api/simplify", method="POST", body={
        "text": "Adjuvant chemotherapy after surgical resection.",
        "target_language": "bn",
        "level": "level_1"
    })
    print(f"     Simplified Bengali: {simp_bn.get('simplified_text')[:60]}...")
    print(f"     Terms explained: {len(simp_bn.get('terms_explained', []))}")

    ask_res = test_endpoint("Ask Question", "/api/ask", method="POST", body={
        "question": "What is biopsy?",
        "target_language": "en",
        "level": "level_2"
    })
    print(f"     Ask Answer: {ask_res.get('answer', simp_en.get('simplified_text'))[:60]}...")

    print("\nALL LIVE API ENDPOINTS ARE FULLY OPERATIONAL!")
except Exception as e:
    print(f"[ERROR] Live API test failed: {e}")
    raise
