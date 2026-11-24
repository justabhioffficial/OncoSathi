# -*- coding: utf-8 -*-
import sys
from pathlib import Path
BACKEND = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend")
sys.path.insert(0, str(BACKEND))

from app.services.retrieval_service import RetrievalService

ret = RetrievalService()
query = "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?"
vec_res = ret.embedding_service.query_similarity(query, top_k=20)

print(f"Top 20 from vectorizer for query: {query}")
for i, c in enumerate(vec_res):
    print(f"Rank {i+1}: score={c['score']:.4f}, term={c.get('term')}, doc={c.get('source_document')}")
    print(f"   text: {c.get('text')[:100]}")
