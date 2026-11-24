# -*- coding: utf-8 -*-
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
retrieval_py = WORKSPACE / "backend" / "app" / "services" / "retrieval_service.py"
simplification_py = WORKSPACE / "backend" / "app" / "services" / "simplification_service.py"

# 1. Update retrieval_service.py
retrieval_code = retrieval_py.read_text(encoding="utf-8")
old_init = """    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.dictionary: List[Dict[str, Any]] = []
        self.terms_by_name: Dict[str, Dict[str, Any]] = {}
        self.terms_by_bengali: Dict[str, Dict[str, Any]] = {}
        self.is_ready = False"""

new_init = """    def __init__(self, auto_load: bool = True):
        self.embedding_service = EmbeddingService()
        self.dictionary: List[Dict[str, Any]] = []
        self.terms_by_name: Dict[str, Dict[str, Any]] = {}
        self.terms_by_bengali: Dict[str, Dict[str, Any]] = {}
        self.is_ready = False
        if auto_load:
            self.load_processed_data()"""

if old_init in retrieval_code:
    retrieval_code = retrieval_code.replace(old_init, new_init)
    retrieval_py.write_text(retrieval_code, encoding="utf-8")
    print("Updated retrieval_service.py successfully!")
else:
    print("Could not find old_init in retrieval_service.py")

# 2. Update simplification_service.py
sim_code = simplification_py.read_text(encoding="utf-8")
old_labels = """LEVEL_LABELS = {
    "level_1": "Level 1 ? Basic (Ultra-Simple)",
    "level_2": "Level 2 ? Easy (Community Health)",
    "level_3": "Level 3 ? Detailed but Understandable",
}"""

new_labels = """LEVEL_LABELS = {
    "level_1": "Level 1 — Basic (Ultra-Simple)",
    "level_2": "Level 2 — Easy (Community Health)",
    "level_3": "Level 3 — Detailed but Understandable",
}"""

if old_labels in sim_code:
    sim_code = sim_code.replace(old_labels, new_labels)
    simplification_py.write_text(sim_code, encoding="utf-8")
    print("Updated simplification_service.py LEVEL_LABELS successfully!")
else:
    print("Could not find old_labels in simplification_service.py")
