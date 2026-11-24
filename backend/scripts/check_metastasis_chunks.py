# -*- coding: utf-8 -*-
import json
from pathlib import Path

CHUNKS_PATH = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend\data\processed\knowledge_chunks.json")
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Total chunks: {len(chunks)}")
meta_chunks = [c for c in chunks if "metasta" in c["text"].lower() or "metasta" in c.get("term", "").lower()]
print(f"Chunks matching 'metasta': {len(meta_chunks)}")
for i, c in enumerate(meta_chunks[:6]):
    print(f"\n--- Match {i+1} ---")
    print(f"Doc: {c.get('source_document')}, Section: {c.get('section')}, Page: {c.get('page')}")
    print(f"Term: {c.get('term')}")
    print(f"Text: {c.get('text')[:200]}")
