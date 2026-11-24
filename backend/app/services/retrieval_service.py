# -*- coding: utf-8 -*-
"""
Retrieval Service for OncoSathi AI.
Implements intelligent hybrid search combining TF-IDF vector similarity
with clinical terminology extraction, query intent targeting, and document metadata scoring.
"""
import os, re, json
from typing import List, Dict, Any, Optional
from app.services.embedding_service import EmbeddingService
from app.config import PROCESSED_DIR

STOPWORDS = {
    "is", "of", "on", "at", "in", "to", "for", "and", "the", "with", "from",
    "that", "this", "what", "where", "when", "how", "why", "who", "which",
    "a", "an", "does", "do", "did", "mean", "meaning", "explain", "tell",
    "me", "about", "describe", "can", "could", "should", "would", "or", "by"
}

class RetrievalService:
    def __init__(self, auto_load: bool = True):
        self.embedding_service = EmbeddingService()
        self.dictionary: List[Dict[str, Any]] = []
        self.terms_by_name: Dict[str, Dict[str, Any]] = {}
        self.terms_by_bengali: Dict[str, Dict[str, Any]] = {}
        self.is_ready = False
        if auto_load:
            self.load_processed_data()

    def load_processed_data(self) -> bool:
        index_file = os.path.join(PROCESSED_DIR, "vector_index.pkl")
        dict_file = os.path.join(PROCESSED_DIR, "terminology_dictionary.json")
        chunks_file = os.path.join(PROCESSED_DIR, "knowledge_chunks.json")

        if os.path.exists(dict_file):
            try:
                with open(dict_file, "r", encoding="utf-8") as f:
                    self.dictionary = json.load(f)
                for t in self.dictionary:
                    norm = t["term"].strip().lower()
                    self.terms_by_name[norm] = t
                    if t.get("bengali_term"):
                        b_norm = t["bengali_term"].strip().lower()
                        self.terms_by_bengali[b_norm] = t
            except Exception as e:
                print(f"[RetrievalService] Error loading dictionary: {e}")

        # Load vector index
        loaded = self.embedding_service.load_index(index_file)
        if not loaded and os.path.exists(chunks_file):
            try:
                with open(chunks_file, "r", encoding="utf-8") as f:
                    chunks = json.load(f)
                self.embedding_service.fit_and_index(chunks)
                self.embedding_service.save_index(index_file)
                loaded = True
            except Exception as e:
                print(f"[RetrievalService] Error indexing chunks: {e}")

        self.is_ready = loaded and len(self.dictionary) > 0
        return self.is_ready

    def hybrid_retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval combining vector similarity with clinical term matching,
        question intent extraction, and section relevance boosting.
        """
        if not self.is_ready:
            self.load_processed_data()

        # Step 1: Pull top candidate chunks from vector space
        vector_results = self.embedding_service.query_similarity(query, top_k=min(len(self.embedding_service.chunks), 40))
        if not vector_results:
            return []

        q_clean = query.lower()

        # Step 2: Extract primary question subject if applicable
        # Examples: "What is metastasis?", "What are lymph nodes?", "Explain biopsy", "What does chemotherapy mean?"
        primary_target = ""
        target_match = re.search(
            r'(?:what\s+(?:is|are|does)|explain|meaning\s+of|tell\s+me\s+about)\s+(?:a|an|the)?\s*([a-zA-Zঀ-৿\s]{3,35}?)(?:\s+mean|\s+and|\s+in|\s+for|\?|$)',
            q_clean
        )
        if target_match:
            candidate = target_match.group(1).strip()
            # Remove any trailing connector words
            candidate = re.sub(r'\s+(?:in|and|or|of|to|with)$', '', candidate).strip()
            if candidate and candidate not in STOPWORDS:
                primary_target = candidate

        # Step 3: Score and re-rank candidates with hybrid domain intelligence
        scored_results = []
        seen_texts = set()

        for chunk in vector_results:
            text = chunk.get("text", "")
            if text in seen_texts:
                continue
            seen_texts.add(text)

            boost = 0.0
            term_raw = chunk.get("term", "").lower()
            chunk_text = text.lower()

            # Break compound terms into constituent medical tokens
            # Handles: "METASTASIS/METASTASIZED", "Staging & Grading Metastasis", "Basic Concepts Benign"
            term_parts = [
                re.sub(r'[^a-zA-Z0-9ঀ-৿]', '', p).strip()
                for p in re.split(r'[/&(),\-\|\s]', term_raw)
            ]
            term_parts = [p for p in term_parts if len(p) >= 3 and p not in STOPWORDS]

            # Check if any component of the term matches the user's query
            term_matched = False
            for tp in term_parts:
                pattern = r'\b' + re.escape(tp) + r'\b'
                if re.search(pattern, q_clean) or (len(tp) >= 5 and tp in q_clean):
                    boost += 0.45
                    term_matched = True

                    # Priority boost if this chunk defines the primary question target
                    if primary_target and (tp in primary_target or primary_target in tp):
                        boost += 0.60
                    break

            # Check if Bengali term matches
            bengali_term = (chunk.get("bengali_term") or "").strip().lower()
            if bengali_term and len(bengali_term) >= 2 and bengali_term in q_clean:
                boost += 0.60
                if primary_target and bengali_term in primary_target:
                    boost += 0.40

            # Substring / keyword matching in chunk text
            for word in query.strip().split():
                w_clean = re.sub(r'[^a-zA-Z0-9ঀ-৿]', '', word).lower()
                if len(w_clean) >= 3 and w_clean not in STOPWORDS:
                    # Non-ascii (Bengali/Indic word)
                    if any(ord(c) > 127 for c in w_clean) and w_clean in text:
                        boost += 0.35
                    elif w_clean in chunk_text:
                        boost += 0.12
                        if primary_target and w_clean in primary_target:
                            boost += 0.25

            # De-prioritize generic introductory slides if specific clinical terms exist
            if "slide 1 - title" in chunk_text and primary_target:
                boost -= 0.50

            final_score = chunk.get("score", 0.0) + boost
            chunk_copy = dict(chunk)
            chunk_copy["final_score"] = round(final_score, 4)
            scored_results.append(chunk_copy)

        # Filter out chunks with negligible relevance (< 0.12) to catch out-of-domain queries
        filtered_results = [c for c in scored_results if c.get("final_score", 0.0) >= 0.12]
        filtered_results.sort(key=lambda x: x["final_score"], reverse=True)
        return filtered_results[:top_k]

    def find_relevant_terms(self, text: str, max_terms: int = 6) -> List[Dict[str, Any]]:
        """
        Extract medical terminology present in the query and enrich with definitions.
        """
        if not self.terms_by_name:
            self.load_processed_data()

        matched = []
        text_lower = " " + text.lower() + " "
        
        # Primary terms first
        for item in self.dictionary:
            t_name = item["term"].lower()
            base_name = re.sub(r'\(.*?\)', '', t_name).strip()
            bengali = item.get("bengali_term", "").strip()

            is_match = False
            # Check whole word boundary where possible
            if len(base_name) >= 3:
                pattern = r'\b' + re.escape(base_name) + r'\b'
                if re.search(pattern, text_lower):
                    is_match = True
            if not is_match and bengali and bengali in text:
                is_match = True

            if is_match:
                # Ensure simple_meaning and definitions are cleanly populated
                enriched = dict(item)
                if not enriched.get("simple_meaning"):
                    enriched["simple_meaning"] = enriched.get("simplified_en") or enriched.get("medical_definition")
                if not enriched.get("definition"):
                    enriched["definition"] = enriched.get("medical_definition") or enriched.get("simplified_en")
                matched.append(enriched)
                if len(matched) >= max_terms:
                    break

        return matched
