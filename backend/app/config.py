# -*- coding: utf-8 -*-
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
SOURCE_DOCS_DIR = DATA_DIR / "source_documents"
PROCESSED_DIR = DATA_DIR / "processed"

# Application Metadata
APP_NAME = "OncoSathi AI"
APP_TAGLINE = "Simplifying Cancer Knowledge for Community Healthcare"
APP_VERSION = "1.0.0"

# Host and Port
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

# AI / LLM Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "gemini" if GEMINI_API_KEY else "offline")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
GEMINI_FALLBACK_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-latest"
]

# Defaults
DEFAULT_LANGUAGE = "en"  # "en" or "bn"
DEFAULT_SIMPLIFICATION_LEVEL = "level_2"  # "level_1", "level_2", "level_3"

# Medical Safety
MEDICAL_DISCLAIMER = (
    "OncoSathi AI provides simplified educational information based on its available medical sources. "
    "It is not a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified doctor or Primary Health Centre (PHC) medical officer for patient-specific clinical decisions."
)

MISSING_INFO_FALLBACK_EN = (
    "I couldn't find enough reliable information about this in my available medical sources. "
    "Please consult a qualified healthcare professional or Primary Health Centre (PHC) doctor."
)

MISSING_INFO_FALLBACK_BN = (
    "আমার কাছে থাকা চিকিৎসা তথ্যে এই বিষয়ে পর্যাপ্ত নির্ভরযোগ্য তথ্য পাওয়া যায়নি। "
    "দয়া করে একজন অভিজ্ঞ ডাক্তার বা নিকটবর্তী প্রাথমিক স্বাস্থ্য কেন্দ্রের চিকিৎসকের সাথে পরামর্শ করুন।"
)
