# -*- coding: utf-8 -*-
"""
Text-to-Speech (TTS) Service for OncoSathi AI.
Provides authentic, native Bengali (বাংলা কণ্ঠস্বর) and Indian English audio synthesis.
Uses audio streaming and Base64 MP3 generation for immediate in-browser playback.
"""
import re
import base64
import hashlib
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional

class TTSService:
    _cache: Dict[str, bytes] = {}

    @classmethod
    def clean_text_for_speech(cls, text: str) -> str:
        """
        Strips markdown asterisks, hashes, brackets, and bullet symbols
        so the spoken voice sounds natural, clear, and clinical.
        """
        if not text:
            return ""
        # Remove markdown headers and emphasis
        t = re.sub(r'#+\s*', '', text)
        t = re.sub(r'\*{1,3}', '', t)
        t = re.sub(r'\[.*?\]\(.*?\)', '', t)
        t = re.sub(r'[_`~]', '', t)
        # Remove list bullet markers like - or • or 1.
        t = re.sub(r'^\s*[-*•\d+.)]\s*', '', t, flags=re.MULTILINE)
        # Normalize whitespace
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    @classmethod
    def synthesize_audio(cls, text: str, language: str = "bn") -> Optional[bytes]:
        """
        Synthesizes high-fidelity MP3 speech audio in actual native Bengali or English.
        """
        cleaned = cls.clean_text_for_speech(text)
        if not cleaned:
            return None

        is_bn = language.lower() in ["bn", "bengali", "bn-in", "bn-bd"] or bool(re.search(r'[\u0980-\u09FF]', cleaned))
        lang_code = "bn" if is_bn else "en"

        # Check in-memory cache
        cache_key = hashlib.md5(f"{lang_code}:{cleaned}".encode('utf-8')).hexdigest()
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        # Break text into spoken segments at sentence boundaries (max 160 characters)
        split_regex = r'([।\.\n\?!;]+)' if is_bn else r'([\.\n\?!;]+)'
        segments = re.split(split_regex, cleaned)
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

        if not chunks:
            chunks = [cleaned[:160]]

        audio_bytes = bytearray()
        try:
            for chunk in chunks:
                encoded_chunk = urllib.parse.quote(chunk)
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang_code}&client=tw-ob&q={encoded_chunk}"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    audio_bytes.extend(resp.read())

            result = bytes(audio_bytes)
            if result:
                # Cache up to 100 items
                if len(cls._cache) > 100:
                    cls._cache.clear()
                cls._cache[cache_key] = result
                return result
        except Exception as e:
            print(f"[TTSService] Speech synthesis warning: {e}")

        return None

    @classmethod
    def synthesize_audio_base64(cls, text: str, language: str = "bn") -> Optional[str]:
        audio_data = cls.synthesize_audio(text, language)
        if audio_data:
            return base64.b64encode(audio_data).decode("ascii")
        return None

    @staticmethod
    def get_speech_config(text: str, language: str = "en") -> Dict[str, Any]:
        """
        Returns parameters for text-to-speech.
        Both client-side Web Speech API and backend audio synthesis are supported.
        """
        voice_lang = "bn-IN" if language in ["bn", "bengali"] else "en-IN"
        return {
            "text": text,
            "language": voice_lang,
            "rate": 0.9,
            "pitch": 1.0,
            "instructions": "Use HTML5 Audio with /api/tts or fallback to window.speechSynthesis."
        }
