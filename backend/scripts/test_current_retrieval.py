# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

BACKEND = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend")
sys.path.insert(0, str(BACKEND))

from app.services.retrieval_service import RetrievalService

ret = RetrievalService()

def test_query(q):
    print(f"\n==========================================")
    print(f"QUERY: {q}")
    chunks = ret.hybrid_retrieve(q, top_k=4)
    print(f"Retrieved {len(chunks)} chunks:")
    for i, c in enumerate(chunks):
        print(f"  {i+1}. [{c.get('source_document')}] Term: {c.get('term')} (Score: {c.get('final_score'):.3f})")
        print(f"     Excerpt: {c.get('text')[:110]}...")

test_queries = [
    "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?",
    "What are lymph nodes?",
    "What is chemotherapy?",
    "What is a biopsy?",
    "What is the difference between benign and malignant tumors?",
    "Explain cancer staging in simple English.",
    "Explain breast cancer in simple language.",
    "What is alopecia?",
    "What is the capital of France?"
]

for q in test_queries:
    test_query(q)
