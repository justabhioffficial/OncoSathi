# -*- coding: utf-8 -*-
import os, json
from typing import List, Dict, Any, Optional, Tuple
from app.config import PROCESSED_DIR
from app.models.schemas import TermItem

class TerminologyService:
    def __init__(self):
        self.terms: List[Dict[str, Any]] = []
        self.categories: List[str] = []
        self._load_terms()

    def _load_terms(self):
        dict_file = os.path.join(PROCESSED_DIR, "terminology_dictionary.json")
        if os.path.exists(dict_file):
            try:
                with open(dict_file, "r", encoding="utf-8") as f:
                    self.terms = json.load(f)
                cats = set()
                for t in self.terms:
                    cat = t.get("category")
                    if cat:
                        cats.add(cat)
                self.categories = sorted(list(cats))
            except Exception as e:
                print(f"[TerminologyService] Error loading terms: {e}")

    def search_terms(self, query: str = "", category: Optional[str] = None, limit: int = 50, offset: int = 0) -> Tuple[int, List[TermItem]]:
        if not self.terms:
            self._load_terms()

        filtered = self.terms
        if category and category != "All":
            filtered = [t for t in filtered if t.get("category") == category]

        if query and query.strip():
            q_clean = query.strip().lower()
            results = []
            for t in filtered:
                t_name = t["term"].lower()
                b_name = (t.get("bengali_term") or "").lower()
                defn = (t.get("medical_definition") or "").lower()
                simp_en = (t.get("simplified_en") or "").lower()
                simp_bn = (t.get("simplified_bn") or "").lower()

                if (q_clean in t_name or q_clean in b_name or q_clean in defn or 
                    q_clean in simp_en or q_clean in simp_bn):
                    results.append(t)
            filtered = results

        total = len(filtered)
        paginated = filtered[offset : offset + limit]

        items = [TermItem(**t) for t in paginated]
        return total, items

    def get_term_by_id(self, term_id: str) -> Optional[TermItem]:
        if not self.terms:
            self._load_terms()
        for t in self.terms:
            if t.get("id") == term_id:
                return TermItem(**t)
        return None

    def get_all_categories(self) -> List[str]:
        if not self.categories:
            self._load_terms()
        return ["All"] + self.categories
