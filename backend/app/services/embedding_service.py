# -*- coding: utf-8 -*-
import os, pickle
from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=5000
        )
        self.chunk_matrix = None
        self.chunks: List[Dict[str, Any]] = []
        self.is_fitted = False

    def fit_and_index(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        corpus = [c["text"] for c in chunks]
        if not corpus:
            return
        self.chunk_matrix = self.vectorizer.fit_transform(corpus)
        self.is_fitted = True

    def query_similarity(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.is_fitted or not self.chunks:
            return []
        
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.chunk_matrix)[0]
        
        ranked_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            score = float(scores[idx])
            chunk = dict(self.chunks[idx])
            chunk["score"] = score
            results.append(chunk)
            
        return results

    def save_index(self, file_path: str):
        with open(file_path, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "chunk_matrix": self.chunk_matrix,
                "chunks": self.chunks,
                "is_fitted": self.is_fitted
            }, f)

    def load_index(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        try:
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                self.vectorizer = data["vectorizer"]
                self.chunk_matrix = data["chunk_matrix"]
                self.chunks = data["chunks"]
                self.is_fitted = data["is_fitted"]
            return True
        except Exception as e:
            print(f"[EmbeddingService] Failed to load index: {e}")
            return False
