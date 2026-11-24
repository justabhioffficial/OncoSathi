import os
# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error

api_key = os.environ.get("GEMINI_API_KEY", "")

tests = [
    ("v1beta", "models/gemini-flash-latest"),
    ("v1beta", "models/gemini-2.5-flash"),
    ("v1", "models/gemini-flash-latest"),
    ("v1beta", "models/gemini-2.5-pro"),
    ("v1beta", "models/gemini-pro-latest"),
]

payload = {
    "contents": [{"parts": [{"text": "Hello, respond with ONLY the word OK."}]}]
}

for ver, m in tests:
    url = f"https://generativelanguage.googleapis.com/{ver}/{m}:generateContent?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[SUCCESS] {ver} {m} -> {data['candidates'][0]['content']['parts'][0]['text'].strip()}")
            break
    except urllib.error.HTTPError as e:
        print(f"[ERROR] {ver} {m} -> HTTP {e.code}: {e.read().decode('utf-8')[:200]}")
    except Exception as e:
        print(f"[FAIL] {ver} {m} -> {e}")
