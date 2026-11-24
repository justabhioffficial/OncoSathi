# -*- coding: utf-8 -*-
import sys
from pathlib import Path

BACKEND = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend")
sys.path.insert(0, str(BACKEND))

from app.services.retrieval_service import RetrievalService
from app.services.simplification_service import SimplificationService

ret = RetrievalService()
query = "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?"
chunks = ret.hybrid_retrieve(query, top_k=4)
terms = ret.find_relevant_terms(query, max_terms=4)

print(f"CHUNKS RETRIEVED: {len(chunks)}")
for i, c in enumerate(chunks):
    print(f"Chunk {i+1}: doc={c.get('source_document')}, term={c.get('term')}, score={c.get('final_score')}")
    print(f"   Text: {c.get('text')[:120]}...")

print(f"\nTERMS FOUND: {len(terms)}")
for t in terms:
    print(f"Term: {t.get('term')}, BN: {t.get('bengali_term')}, Simple: {t.get('simple_meaning')}")

sim = SimplificationService(ret)
ans = sim.answer_question(query, target_language="en", level="level_2")
print("\nCURRENT ANSWER:")
print(ans.answer)
