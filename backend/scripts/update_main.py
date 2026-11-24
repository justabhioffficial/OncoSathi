# -*- coding: utf-8 -*-
from pathlib import Path

main_py = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend\app\main.py")
content = main_py.read_text(encoding="utf-8")

old_part = """elif FRONTEND_PUBLIC.exists() and (FRONTEND_PUBLIC / "index.html").exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PUBLIC)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(FRONTEND_PUBLIC / "index.html"))"""

new_part = """elif FRONTEND_PUBLIC.exists() and (FRONTEND_PUBLIC / "index.html").exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PUBLIC)), name="static")

    @app.get("/{full_path:path}")
    async def serve_public_spa(full_path: str):
        file_path = FRONTEND_PUBLIC / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(FRONTEND_PUBLIC / "index.html"))"""

if old_part in content:
    content = content.replace(old_part, new_part)
    main_py.write_text(content, encoding="utf-8")
    print("Replaced successfully!")
else:
    print("Could not find old_part, checking content...")
    lines = content.splitlines()
    print("Last 10 lines:")
    for l in lines[-10:]:
        print(l)
