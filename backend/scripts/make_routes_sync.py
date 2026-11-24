# -*- coding: utf-8 -*-
from pathlib import Path

API_DIR = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend\app\api")

for fname in ["knowledge.py", "terminology.py", "feedback.py", "tts.py"]:
    fpath = API_DIR / fname
    text = fpath.read_text(encoding="utf-8")
    updated = text.replace("async def ", "def ")
    fpath.write_text(updated, encoding="utf-8")
    print(f"Updated {fname} to synchronous def handlers.")

print("All API routes updated to sync handlers!")
