# -*- coding: utf-8 -*-
import json
from pathlib import Path

DICT_PATH = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend\data\processed\terminology_dictionary.json")
with open(DICT_PATH, "r", encoding="utf-8") as f:
    terms = json.load(f)

print(f"Total dictionary terms: {len(terms)}")
for i, t in enumerate(terms[:8]):
    print(f"\nTerm {i+1}: {t.get('term')}")
    print(f"Keys: {list(t.keys())}")
    print(f"definition: {t.get('definition')}")
    print(f"medical_definition: {t.get('medical_definition')}")
    print(f"simple_meaning: {t.get('simple_meaning')}")
    print(f"bengali_term: {t.get('bengali_term')}")
