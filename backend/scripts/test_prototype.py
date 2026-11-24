# -*- coding: utf-8 -*-
"""
Test script to prototype the dynamic intelligent generator
for all required topics and confirm exact query relevance.
"""
import sys
from pathlib import Path

BACKEND = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\backend")
sys.path.insert(0, str(BACKEND))

from app.services.retrieval_service import RetrievalService

ret = RetrievalService()

test_cases = [
    {
        "id": "A",
        "query": "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "B",
        "query": "What are lymph nodes?",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "C",
        "query": "What is chemotherapy?",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "D",
        "query": "What is a biopsy?",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "E",
        "query": "What is the difference between benign and malignant tumors?",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "F",
        "query": "Explain cancer staging in simple English.",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "G",
        "query": "Explain breast cancer in simple language.",
        "lang": "en",
        "level": "level_2"
    },
    {
        "id": "H",
        "query": "What does metastasis mean? (বাংলা)",
        "query_bn": "মেটাস্ট্যাসিস বলতে কী বোঝায় এবং ক্যানসার কীভাবে শরীরের অন্যান্য অংশে ছড়ায়?",
        "lang": "bn",
        "level": "level_1"
    },
    {
        "id": "I",
        "query": "What is the capital of France?",
        "lang": "en",
        "level": "level_2"
    }
]

print("Ready to implement dynamic generation engine!")
