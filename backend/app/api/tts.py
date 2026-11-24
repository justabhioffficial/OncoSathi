# -*- coding: utf-8 -*-
from fastapi import APIRouter, Response, HTTPException, Query
from app.models.schemas import TTSRequest, TTSResponse
from app.services.tts_service import TTSService

router = APIRouter()

@router.post("/tts", response_model=TTSResponse)
def generate_speech(request: TTSRequest):
    """
    Synthesizes and returns native speech audio (Base64 MP3) for Bengali or English.
    Falls back gracefully to client-side Web Speech API instructions if needed.
    """
    voice_lang = "bn-IN" if request.language in ["bn", "bengali"] else "en-IN"
    voice_label = "Google Bengali Voice (বাংলা কণ্ঠস্বর)" if "bn" in voice_lang.lower() else "Google Indian English Voice"
    
    # Synthesize native audio bytes
    b64_audio = TTSService.synthesize_audio_base64(request.text, request.language)
    
    if b64_audio:
        return TTSResponse(
            audio_base64=b64_audio,
            format="audio/mpeg",
            language=voice_lang,
            language_code="bn" if "bn" in voice_lang.lower() else "en",
            voice_name=voice_label,
            status="ready"
        )
    
    # Graceful fallback configuration for browser Web Speech API
    cfg = TTSService.get_speech_config(request.text, request.language)
    return TTSResponse(
        audio_base64=None,
        format="web-speech-api",
        language=cfg["language"],
        language_code="bn" if "bn" in cfg["language"].lower() else "en",
        voice_name=voice_label,
        status="ready"
    )

@router.get("/tts/stream")
def stream_speech(text: str = Query(..., min_length=1), language: str = Query("bn")):
    """
    Direct audio streaming endpoint returning audio/mpeg binary stream.
    Can be used directly in HTML5 <audio src="..."> or new Audio() in JavaScript.
    """
    audio_bytes = TTSService.synthesize_audio(text, language)
    if audio_bytes:
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=bengali_speech.mp3",
                "Cache-Control": "public, max-age=86400"
            }
        )
    raise HTTPException(status_code=500, detail="Could not synthesize speech audio stream.")
