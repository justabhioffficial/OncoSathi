# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path
BACKEND = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend")
sys.path.insert(0, str(BACKEND))

from app.services.retrieval_service import RetrievalService

ret = RetrievalService()

def improved_hybrid_retrieve(retriever, query: str, top_k: int = 5):
    # Retrieve top 40 candidates from vector similarity
    vector_results = retriever.embedding_service.query_similarity(query, top_k=40)
    
    q_clean = query.lower()
    stopwords = {"is", "of", "on", "at", "in", "to", "for", "and", "the", "with", "from", "that", "this", "what", "where", "when", "how", "a", "an", "does", "mean", "explain"}
    
    # Extract potential question target (e.g. "what does metastasis mean" -> "metastasis")
    target_match = re.search(r'(?:what\s+(?:is|are|does)|explain|meaning\s+of)\s+(?:a|an|the)?\s*([a-zA-Zঀ-৿\s]{3,30}?)(?:\s+mean|\s+and|\s+in|\s+for|\?|$)', q_clean)
    primary_target = target_match.group(1).strip() if target_match else ""
    
    scored_results = []
    seen_texts = set()
    
    for chunk in vector_results:
        text = chunk["text"]
        if text in seen_texts:
            continue
        seen_texts.add(text)
        
        boost = 0.0
        term_raw = chunk.get("term", "").lower()
        chunk_text = chunk.get("text", "").lower()
        
        # Split term by punctuation to handle compound terms like "METASTASIS/METASTASIZED", "Staging & Grading Metastasis"
        term_parts = [re.sub(r'[^a-zA-Z0-9ঀ-৿]', '', p).strip() for p in re.split(r'[/&(),\-\|]', term_raw)]
        term_parts = [p for p in term_parts if len(p) >= 3 and p not in stopwords]
        
        term_matched = False
        for tp in term_parts:
            pattern = r'\b' + re.escape(tp) + r'\b'
            if re.search(pattern, q_clean) or (len(tp) >= 5 and tp in q_clean):
                boost += 0.45
                term_matched = True
                # If this matches the primary target of the question, extra boost!
                if primary_target and (tp in primary_target or primary_target in tp):
                    boost += 0.40
                break
                
        # Also check bengali term
        bengali_term = (chunk.get("bengali_term") or "").strip()
        if bengali_term and bengali_term in query:
            boost += 0.50
            
        # Match keywords in chunk text
        for word in query.strip().split():
            w_clean = re.sub(r'[^a-zA-Z0-9ঀ-৿]', '', word).lower()
            if len(w_clean) >= 3 and w_clean not in stopwords:
                if w_clean in chunk_text:
                    boost += 0.15
                    if primary_target and w_clean in primary_target:
                        boost += 0.20
                        
        final_score = chunk.get("score", 0.0) + boost
        chunk_copy = dict(chunk)
        chunk_copy["final_score"] = final_score
        scored_results.append(chunk_copy)
        
    filtered = [c for c in scored_results if c.get("final_score", 0.0) >= 0.12]
    filtered.sort(key=lambda x: x["final_score"], reverse=True)
    return filtered[:top_k]

q = "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?"
chunks = improved_hybrid_retrieve(ret, q, top_k=4)
print(f"IMPROVED RETRIEVAL FOR: {q}\n")
for i, c in enumerate(chunks):
    print(f"{i+1}. [{c.get('source_document')}] Term: {c.get('term')} (Score: {c.get('final_score'):.3f})")
    print(f"   Excerpt: {c.get('text')[:120]}...\n")
