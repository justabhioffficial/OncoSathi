import os
# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error

api_key = os.environ.get("GEMINI_API_KEY", "")

models_to_test = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite"
]

payload = {
    "contents": [
        {
            "parts": [{"text": "You are a medical assistant for community health workers. Briefly explain what biopsy means in one short sentence."}]
        }
    ]
}

for m in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"[SUCCESS] Model '{m}' responded:\n{text}\n")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')[:200]
        print(f"[HTTP {e.code}] Model '{m}': {err_body}")
    except Exception as e:
        print(f"[FAIL] Model '{m}': {e}")

