import os
# -*- coding: utf-8 -*-
"""
Test script for Gemini API with medical guardrails and zero hallucination
"""
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-flash-lite-latest"

SYSTEM_PROMPT = """You are OncoSathi AI, an expert medical oncology simplifier for ASHA (Accredited Social Health Activist) community healthcare workers in India.

STRICT MEDICAL DOMAIN RESTRICTION:
You must ONLY answer questions directly related to oncology, cancer care, medical terminology, diagnostic tests, staging, cancer treatments, and community healthcare. If the question is outside the medical domain (e.g. politics, coding, recipes, sports, finance), refuse politely.

STRICT ZERO-HALLUCINATION GROUNDING:
Rely strictly and exclusively on the provided Medical Reference Context. Never invent clinical data, drug dosages, survival numbers, or unsupported claims. If the context does not contain the answer, state:
"I couldn't find enough reliable information about this in my available medical sources. Please consult a qualified healthcare professional."

FORMAT YOUR RESPONSE AS:
SIMPLIFIED EXPLANATION:
<clear explanation in simple words>

KEY COUNSELING POINTS:
- <Point 1>
- <Point 2>
- <Point 3>
"""

def test_query(prompt_text, context_text=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    user_content = f"Medical Reference Context:\n{context_text}\n\nUser Question:\n{prompt_text}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_PROMPT}\n\n{user_content}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 600
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"ERROR: {e}"

print("--- TEST 1: Medical Question (Metastasis) ---")
q1 = "What does metastasis mean and how does cancer spread from its original organ?"
ctx1 = "Metastasis: The spread of cancer cells from the place where they first formed to another part of the body. In metastasis, cancer cells break away from the original (primary) tumor, travel through the blood or lymph system, and form a new tumor in other organs or tissues."
print(test_query(q1, ctx1))
print("\n" + "="*50 + "\n")

print("--- TEST 3: Bengali Medical Question (Biopsy) ---")
q3 = "বায়োপসি কী এবং এটি কেন করা হয়?"
ctx3 = "Biopsy (বায়োপসি): একটি মেডিকেল পরীক্ষা যেখানে শরীর থেকে টিস্যু বা তরল নমুনা নিয়ে মাইক্রোস্কোপের নিচে পরীক্ষা করা হয় ক্যানসার আছে কিনা তা নিশ্চিত করার জন্য।"
print(test_query(q3 + "\nPlease answer in Simple Bengali (সহজ বাংলা).", ctx3))

