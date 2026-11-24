# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\frontend\public\index.html")
c = path.read_text(encoding="utf-8")

c = c.replace(
    '<span className="font-semibold text-lg text-slateText tracking-tight">OncoSathi</span>',
    '<span className="font-semibold text-lg text-slateText tracking-tight">OncoSathi <span className="text-forest-600 font-normal">AI</span></span>'
)
path.write_text(c, encoding="utf-8")
print("Updated brand text to OncoSathi AI in index.html")
