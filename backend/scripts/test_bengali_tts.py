# -*- coding: utf-8 -*-
"""
Test script for Bengali TTS audio generation
"""
import urllib.request
import urllib.parse
import re
import base64
import time

def clean_medical_text_for_speech(text: str) -> str:
    """Cleans markdown, bullets, symbols and prepares fluent Bengali text for speech synthesis."""
    # Remove markdown headers and formatting
    t = re.sub(r'#+\s*', '', text)
    t = re.sub(r'\*{1,3}', '', t)
    t = re.sub(r'\[.*?\]\(.*?\)', '', t)
    t = re.sub(r'[_`~]', '', t)
    # Remove bullet markers like - or • or 1.
    t = re.sub(r'^\s*[-*•\d+.)]\s*', '', t, flags=re.MULTILINE)
    # Normalize whitespaces
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def generate_bengali_audio(text: str) -> bytes:
    cleaned = clean_medical_text_for_speech(text)
    if not cleaned:
        return b""
    
    # Split text into bite-sized spoken segments (max 180 chars) at punctuation marks
    segments = re.split(r'([।\.\n\?!;]+)', cleaned)
    chunks = []
    curr = ""
    for s in segments:
        if not s:
            continue
        if len(curr) + len(s) < 160:
            curr += s
        else:
            if curr.strip():
                chunks.append(curr.strip())
            curr = s
    if curr.strip():
        chunks.append(curr.strip())
        
    audio_bytes = bytearray()
    for chunk in chunks:
        q = urllib.parse.quote(chunk)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=bn&client=tw-ob&q={q}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            audio_bytes.extend(resp.read())
            
    return bytes(audio_bytes)

# Test with actual text from user's screenshot:
test_bengali_text = """
ক্যান্সার কোষগুলো অনেক সময় মূল জায়গা থেকে ছুটে যায়। তারা রক্ত বা লসিকাতন্ত্রের মাধ্যমে শরীরের অন্য দূরে থাকা জায়গায় ছড়িয়ে পড়ে। একেই মেটাস্ট্যাসিস বা ক্যান্সারের বিস্তার বলা হয়।
"""

print("[*] Testing Bengali TTS Audio Synthesis...")
t0 = time.time()
audio = generate_bengali_audio(test_bengali_text)
elapsed = time.time() - t0
b64 = base64.b64encode(audio).decode("ascii")

print(f"[SUCCESS] Generated {len(audio)} bytes of Bengali MP3 in {elapsed:.2f}s!")
print(f"Base64 length: {len(b64)} chars (starts with: {b64[:30]}...)")
assert len(audio) > 10000
assert b64.startswith("SUQz") or b64.startswith("//") or b64.startswith("///") # MP3 header
print("[PASS] Bengali voice audio generation verified!")
