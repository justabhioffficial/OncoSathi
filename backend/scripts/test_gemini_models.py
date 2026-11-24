import os
# -*- coding: utf-8 -*-
import json
import urllib.request

api_key = os.environ.get("GEMINI_API_KEY", "")

for model in ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro"]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": "Hello, respond with 'OK' and the model name."}]
            }
        ]
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"[{model}] SUCCESS: {text}")
    except Exception as e:
        print(f"[{model}] FAILED: {e}")
