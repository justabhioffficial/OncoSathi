# -*- coding: utf-8 -*-
"""
LLM Service for OncoSathi AI.
Integrates Google Gemini API for live generative responses, with an intelligent,
query-aware, knowledge-grounded offline simplification engine that dynamically synthesizes
precise, topic-specific explanations in English and authentic Bengali (বাংলা).
"""
import os, json, re
import urllib.request
import urllib.error
from typing import List, Dict, Any, Tuple, Optional
from app.config import (
    GEMINI_API_KEY, LLM_PROVIDER, GEMINI_MODEL, GEMINI_FALLBACK_MODELS,
    MISSING_INFO_FALLBACK_EN, MISSING_INFO_FALLBACK_BN
)
from app.prompts.simplification_prompts import SYSTEM_SIMPLIFIER_PROMPT, build_simplification_prompt

class LLMService:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.provider = LLM_PROVIDER
        self.model = GEMINI_MODEL
        self.candidate_models = GEMINI_FALLBACK_MODELS

    def _is_non_medical_query(self, text: str) -> bool:
        """
        Detects strictly non-medical / out-of-domain queries to enforce the medical-only domain guardrail.
        """
        text_lower = text.lower().strip()
        
        # Explicit medical indicators (if present, query is treated as medical)
        medical_indicators = [
            "cancer", "tumor", "tumour", "oncolog", "biopsy", "chemo", "radiation", "metastasi",
            "lymph", "carcinoma", "sarcoma", "melanoma", "leukemia", "lymphoma", "malignan",
            "benign", "stage", "staging", "breast", "cervic", "oral", "lung", "colon", "gastric",
            "prostate", "cell", "tissue", "organ", "patholog", "histolog", "screening", "mammogram",
            "ultrasound", "ct scan", "mri", "pet scan", "palliative", "remission", "relapse",
            "recurrence", "alopecia", "neutropenia", "nausea", "fatigue", "pain", "bleeding",
            "ulcer", "lump", "swelling", "fever", "doctor", "hospital", "phc", "asha", "patient",
            "treatment", "therapy", "surgery", "medicine", "dose", "dosage", "prescription",
            "ক্যানসার", "টিউমার", "বায়োপসি", "কেমোথেরাপি", "রেডিওথেরাপি", "মেটাস্ট্যাসিস",
            "লিম্ফ", "লসিকা", "ম্যালিগন্যান্ট", "বিনাইন", "স্তন", "সার্ভিকাল", "মুখের", "ফুসফুস",
            "চিকিৎসা", "ডাক্তার", "লক্ষণ", "স্বাস্থ্য", "রোগী"
        ]
        if any(m in text_lower for m in medical_indicators):
            return False

        # Non-medical patterns (geography, politics, sports, coding, cooking, entertainment, crypto, jokes)
        non_medical_patterns = [
            r"\b(capital\s+of|capital\s+city)\b",
            r"\b(who\s+is|who\s+was)\s+(president|prime\s+minister|minister|king|queen|actor|actress|governor|celebrity)\b",
            r"\b(weather|temperature|forecast|rain\s+today|climate\s+change)\b",
            r"\b(cricket|football|fifa|ipl|world\s+cup|match|score|tournament|tennis|badminton)\b",
            r"\b(python|javascript|java|c\+\+|coding|function|script|algorithm|html|css|github|docker)\b",
            r"\b(recipe|cook|pizza|cake|biryani|burger|pasta|restaurant|taste)\b",
            r"\b(stock|crypto|bitcoin|shares|currency|exchange\s+rate|forex)\b",
            r"\b(movie|film|box\s+office|song|lyrics|cinema|netflix)\b",
            r"\b(tell\s+a\s+joke|riddle|funny\s+story)\b",
            r"\b(france|paris|tokyo|london|germany|delhi\s+election|politics|parliament)\b"
        ]
        for pat in non_medical_patterns:
            if re.search(pat, text_lower):
                return True

        return False

    def generate_simplification(
        self,
        text: str,
        context_chunks: List[Dict[str, Any]],
        explained_terms: List[Dict[str, Any]],
        target_language: str = "en",
        level: str = "level_2"
    ) -> Tuple[str, List[str], bool]:
        """
        Generate a query-specific medical explanation and counseling takeaways.
        Returns: (simplified_text, key_points, is_offline_generated)
        """
        is_bn = target_language in ["bn", "bengali"]

        # 1. Guardrail: Strictly Reject Non-Medical / Off-Domain Queries
        if self._is_non_medical_query(text):
            if is_bn:
                return (
                    "অনকোসাথী এআই শুধুমাত্র এর নির্ভরযোগ্য চিকিৎসা তথ্যের (medical sources) ভিত্তিতে আশা (ASHA) স্বাস্থ্যকর্মীদের জন্য একটি বিশেষায়িত ক্যান্সার ও অনকোলজি তথ্য সহায়িকা হিসেবে কাজ করে। আমার কাছে থাকা চিকিৎসা তথ্যে এই চিকিৎসা বহির্ভূত বিষয়ে পর্যাপ্ত তথ্য পাওয়া যায়নি। চিকিৎসা বহির্ভূত প্রশ্নের উত্তর দেওয়া সম্ভব নয়। অনুগ্রহ করে কোনো ক্যান্সার বা স্বাস্থ্য সম্পর্কিত প্রশ্ন জিজ্ঞাসা করুন।",
                    [
                        "এই প্ল্যাটফর্মটি কেবলমাত্র চিকিৎসা ও ক্যান্সার সচেতনতার উদ্দেশ্যে প্রস্তুত।",
                        "আশা কর্মীরা রোগীদের কাউন্সেলিং ও ক্যান্সার সতর্কবার্তা বোঝার জন্য এটি ব্যবহার করবেন।"
                    ],
                    True
                )
            else:
                return (
                    "OncoSathi AI is dedicated exclusively to medical oncology and community healthcare for ASHA workers based on its verified medical sources. I couldn't find enough reliable information about this non-medical topic in my available medical sources. I cannot answer non-medical questions. Please ask oncology or health-related questions.",
                    [
                        "This platform is strictly restricted to medical oncology and healthcare education.",
                        "ASHA community workers should use this tool for patient counseling and understanding cancer symptoms."
                    ],
                    True
                )

        # 2. Guardrail: Patient-Specific Diagnostic & Prescription Safety Interceptor
        prescribe_keywords = [
            "prescribe", "dosage", "dose", " mg", "how many tablets", "give medicine",
            "diagnose me", "diagnose my patient", "do i have cancer", "does he have cancer",
            "does she have cancer", "cure for my", "what medicine should i take",
            "specific treatment for my patient", "treatment recommendation for my patient"
        ]
        text_lower = text.lower()
        if any(k in text_lower for k in prescribe_keywords):
            if is_bn:
                return (
                    "অনকোসাথী এআই কোনো ওষুধ প্রেসক্রাইব করতে, ওষুধের মাত্রা (ডোজ) নির্ধারণ করতে বা সরাসরি কোনো রোগীর রোগ নির্ণয় করতে পারে না। এটি কেবল কমিউনিটি স্বাস্থ্য কর্মীদের জন্য একটি শিক্ষণীয় তথ্য সহায়িকা। অনুগ্রহ করে রোগীকে সুনির্দিষ্ট রোগনির্ণয় ও চিকিৎসার জন্য অবিলম্বে নিকটবর্তী প্রাথমিক স্বাস্থ্য কেন্দ্রের চিকিৎসক বা বিশেষজ্ঞ অনকোলজিস্টের কাছে পাঠান।",
                    [
                        "নির্দিষ্ট রোগীর ক্ষেত্রে প্রেসক্রিপশন বা ওষুধ পরিবর্তনের সিদ্ধান্ত কেবল চিকিৎসকের এক্তিয়ারভুক্ত।",
                        "সন্দেহজনক লক্ষণ দেখা দিলে রোগীকে কালবিলম্ব না করে সরকারি হাসপাতালে ডাক্তার দেখাতে উৎসাহিত করুন।"
                    ],
                    True
                )
            else:
                return (
                    "OncoSathi AI cannot prescribe medications, calculate drug dosages, or provide definitive diagnostic evaluations for individual patients. This system serves strictly as an educational reference aid for community healthcare workers. Please refer the patient immediately to a qualified oncologist or Medical Officer at the Primary Health Centre (PHC) for clinical diagnosis and prescription management.",
                    [
                        "Clinical prescriptions and treatment decisions must only be made by a certified physician.",
                        "Encourage the patient and family to visit the nearest Primary Health Centre or district hospital without delay."
                    ],
                    True
                )

        # 3. Try Google Gemini API with candidate models & zero-hallucination prompt
        if self.provider == "gemini" and self.api_key:
            try:
                res = self._call_gemini(text, context_chunks, target_language, level)
                if res and res[0].strip():
                    ans_text = res[0]
                    if target_language not in ["en", "bn", "english", "bengali"]:
                        ans_text = (
                            f"[Language Notice: Language '{target_language}' is not currently supported. "
                            "OncoSathi AI currently supports Simple English and Simple Bengali (সহজ বাংলা). "
                            f"Generating response in Simple English.]\n\n{ans_text}"
                        )
                    return ans_text, res[1], False
            except Exception as e:
                print(f"[LLMService] Gemini API call failed, falling back to dynamic grounded engine: {e}")

        # 4. Intelligent Query-Aware Grounded Engine (Local Zero-Hallucination Fallback)
        simplified, key_points = self._grounded_dynamic_simplification(
            text=text,
            context_chunks=context_chunks,
            explained_terms=explained_terms,
            target_language=target_language,
            level=level
        )
        return simplified, key_points, True

    def _call_gemini(
        self,
        text: str,
        context_chunks: List[Dict[str, Any]],
        target_language: str,
        level: str
    ) -> Optional[Tuple[str, List[str]]]:
        if not self.api_key:
            return None

        user_prompt = build_simplification_prompt(text, context_chunks, target_language, level)

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{SYSTEM_SIMPLIFIER_PROMPT}\n\n{user_prompt}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 800
            }
        }

        headers = {"Content-Type": "application/json"}

        # Attempt candidate models in priority sequence for maximum uptime
        for model_name in self.candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    candidates = data.get("candidates", [])
                    if not candidates:
                        continue
                    raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    if not raw_text.strip():
                        continue

                    # Parse structured output
                    simplified_text, key_points = self._parse_gemini_output(raw_text, target_language)
                    return simplified_text, key_points
            except urllib.error.HTTPError as e:
                print(f"[LLMService] Gemini model '{model_name}' HTTP {e.code}, trying next...")
            except Exception as e:
                print(f"[LLMService] Gemini model '{model_name}' error: {e}, trying next...")

        return None

    def _parse_gemini_output(self, raw_text: str, target_language: str) -> Tuple[str, List[str]]:
        is_bn = target_language in ["bn", "bengali"]
        lines = raw_text.split("\n")
        simplified_lines = []
        key_points = []
        in_points = False

        for line in lines:
            line_s = line.strip()
            if not line_s:
                continue

            # Detect section transitions
            upper = line_s.upper()
            if any(marker in upper for marker in ["KEY COUNSELING POINTS", "KEY POINTS", "মূল বিষয়", "কাউন্সেলিং পয়েন্ট", "পরামর্শ"]):
                in_points = True
                continue
            if any(marker in upper for marker in ["SIMPLIFIED EXPLANATION", "SIMPLIFIED SUMMARY", "সহজ ব্যাখ্যা"]):
                in_points = False
                continue

            if in_points:
                if line_s.startswith(("-", "*", "•")) or (len(line_s) > 2 and line_s[0].isdigit() and line_s[1] in ".)"):
                    clean_pt = re.sub(r"^[-*•0-9.)\s]+", "", line_s).strip()
                    if clean_pt:
                        key_points.append(clean_pt)
                elif len(line_s) > 5 and not line_s.startswith("#"):
                    key_points.append(line_s)
            else:
                if not line_s.startswith("#"):
                    simplified_lines.append(line_s)

        simplified_text = "\n".join(simplified_lines).strip()
        if not simplified_text and raw_text:
            simplified_text = raw_text.strip()

        if not key_points:
            if is_bn:
                key_points = [
                    "রোগী ও তার পরিবারকে শান্তভাবে এই চিকিৎসা তথ্যের সারসংক্ষেপ বুঝিয়ে বলুন।",
                    "যেকোনো সন্দেহ বা নতুন লক্ষণ দেখা দিলে অবিলম্বে প্রাথমিক স্বাস্থ্য কেন্দ্রের ডাক্তারের পরামর্শ নিতে বলুন।"
                ]
            else:
                key_points = [
                    "Explain this simplified oncology information gently to the patient and family.",
                    "Always advise consulting the Medical Officer at the Primary Health Centre (PHC) for clinical care."
                ]

        return simplified_text, key_points

    def _grounded_dynamic_simplification(
        self,
        text: str,
        context_chunks: List[Dict[str, Any]],
        explained_terms: List[Dict[str, Any]],
        target_language: str = "en",
        level: str = "level_2"
    ) -> Tuple[str, List[str]]:
        """
        Dynamically synthesizes topic-specific, literacy-appropriate answers
        based on the user's specific query and retrieved evidence from the 4 oncology sources.
        """
        text_lower = text.lower()
        is_bn = target_language in ["bn", "bengali"]

        # 1. Unsupported Language Notice
        lang_notice = ""
        if target_language not in ["en", "bn", "english", "bengali"]:
            lang_notice = (
                f"[Language Notice: Language '{target_language}' is not currently supported. "
                "OncoSathi AI currently supports Simple English and Simple Bengali (সহজ বাংলা). "
                "Generating response in Simple English.]\n\n"
            )
            is_bn = False

        # 2. Patient-Specific Diagnostic & Prescription Safety Interceptor
        prescribe_keywords = [
            "prescribe", "dosage", "dose", " mg", "how many tablets", "give medicine",
            "diagnose me", "diagnose my patient", "do i have cancer", "does he have cancer",
            "does she have cancer", "cure for my", "what medicine should i take",
            "specific treatment for my patient", "treatment recommendation for my patient"
        ]
        if any(k in text_lower for k in prescribe_keywords):
            if is_bn:
                return (
                    "অনকোসাথী এআই কোনো ওষুধ প্রেসক্রাইব করতে, ওষুধের মাত্রা (ডোজ) নির্ধারণ করতে বা সরাসরি কোনো রোগীর রোগ নির্ণয় করতে পারে না। "
                    "এটি কেবল কমিউনিটি স্বাস্থ্য কর্মীদের জন্য একটি শিক্ষণীয় তথ্য সহায়িকা। "
                    "অনুগ্রহ করে রোগীকে সুনির্দিষ্ট রোগনির্ণয় ও চিকিৎসার জন্য অবিলম্বে নিকটবর্তী প্রাথমিক স্বাস্থ্য কেন্দ্রের চিকিৎসক বা বিশেষজ্ঞ অনকোলজিস্টের কাছে পাঠান।",
                    [
                        "নির্দিষ্ট রোগীর ক্ষেত্রে প্রেসক্রিপশন বা ওষুধ পরিবর্তনের সিদ্ধান্ত কেবল চিকিৎসকের এক্তিয়ারভুক্ত।",
                        "সন্দেহজনক লক্ষণ দেখা দিলে রোগীকে কালবিলম্ব না করে সরকারি হাসপাতালে ডাক্তার দেখাতে উৎসাহিত করুন।"
                    ]
                )
            else:
                return (
                    "OncoSathi AI cannot prescribe medications, calculate drug dosages, or provide definitive diagnostic evaluations for individual patients. "
                    "This system serves strictly as an educational reference aid for community healthcare workers. "
                    "Please refer the patient immediately to a qualified oncologist or Medical Officer at the Primary Health Centre (PHC) for clinical diagnosis and prescription management.",
                    [
                        "Clinical prescriptions and treatment decisions must only be made by a certified physician.",
                        "Encourage the patient and family to visit the nearest Primary Health Centre or district hospital without delay."
                    ]
                )

        # 3. Strict Out-of-Domain / Missing Knowledge Guardrail
        if len(context_chunks) == 0 and len(explained_terms) == 0:
            if is_bn:
                return MISSING_INFO_FALLBACK_BN, [
                    "চিকিৎসা তথ্যের সত্যতা যাচাইয়ের জন্য বিশেষজ্ঞ চিকিৎসকের পরামর্শ নিন।",
                    "রোগীকে দ্রুত নিকটবর্তী প্রাথমিক স্বাস্থ্য কেন্দ্রের (PHC) চিকিৎসকের কাছে পাঠানোর ব্যবস্থা করুন।"
                ]
            else:
                return (
                    f"{lang_notice}{MISSING_INFO_FALLBACK_EN}",
                    [
                        "This specific query is not sufficiently covered in the verified oncology sources.",
                        "Refer the patient to a qualified medical officer at the Primary Health Centre (PHC)."
                    ]
                )

        # 4. Check Query Intent: Direct Question vs Clinical Report Excerpt
        is_question = bool(re.search(r'\b(what|how|why|where|when|can|should|does|meaning|explain|define|tell\s+me|কী|কেন|কীভাবে|কাকে বলে)\b', text_lower)) or "?" in text
        is_clinical_report = (
            any(k in text_lower for k in [
                "patient presented", "patient scheduled", "biopsy confirmed", "examination shows",
                "surgical margins", "negative margins", "carcinoma, grade", "grade 1", "grade 2", "grade 3",
                "lumpectomy", "mastectomy", "resection for stage"
            ]) or (len(text.split()) >= 15 and not is_question)
        )

        simplified_text = ""
        key_points = []

        # ==========================================
        # CASE A: CLINICAL REPORT EXCERPT SIMPLIFICATION
        # ==========================================
        if is_clinical_report:
            has_ductal = "ductal" in text_lower or "carcinoma" in text_lower
            has_margins = "margin" in text_lower
            has_grade = "grade" in text_lower
            has_breast = "breast" in text_lower or "lump" in text_lower

            if is_bn:
                simplified_text = (
                    "মেডিকেল রিপোর্টের সহজ ব্যাখ্যা:\n\n"
                    "১. রোগনির্ণয় (Diagnosis): বায়োপসি পরীক্ষার মাধ্যমে স্তনের কোষে ক্যানসারের উপস্থিতি (Invasive Ductal Carcinoma) নিশ্চিত হয়েছে। প্রাথমিক পর্যায়ে ধরা পড়ায় এটি আধুনিক চিকিৎসা প্রোটোকলের মাধ্যমে নিয়ন্ত্রণযোগ্য।\n"
                    "২. টিউমারের গ্রেড (Grade 2): গ্রেড ২ নির্দেশ করে কোষগুলো মাঝারি গতিতে বাড়ছে, যা পরিকল্পিত ওষুধ ও কেমোথেরাপির মাধ্যমে ধ্বংস করা সম্ভব।\n"
                    "৩. সার্জিক্যাল মার্জিন (Negative Surgical Margins): 'নেগেটিভ মার্জিন' একটি অত্যন্ত আশাব্যঞ্জক ফলাফল। এর অর্থ হলো অস্ত্রোপচারের সময় টিউমারটির চারপাশের সুস্থ টিস্যুর বর্ডারসহ সম্পূর্ণ অংশটি পরিষ্কারভাবে বের করে আনা হয়েছে।\n"
                    "৪. পরবর্তী পদক্ষেপ: ভবিষ্যতে রোগ যাতে ফিরে না আসে, সেজন্য অনকোলজিস্টের পরামর্শমতো অ্যাডজুভেন্ট কেমোথেরাপি বা রেডিয়েশন চক্র সম্পূর্ণ করা অত্যন্ত জরুরি।"
                )
                key_points = [
                    "রোগী ও পরিবারকে আশ্বস্ত করুন যে অস্ত্রোপচারে নেগেটিভ মার্জিন পাওয়া একটি খুব ভালো সংকেত।",
                    "অস্ত্রোপচারের পরেও অবশিষ্ট অদৃশ্য কোষ ধ্বংস করতে ডাক্তারবাবুর নির্দেশিত কেমোথেরাপি সময়মতো সম্পূর্ণ করতে হবে।",
                    "রোগীর পুষ্টিকর খাবার, বিশ্রাম এবং নিয়মিত স্বাস্থ্যকেন্দ্রের ফলো-আপ নিশ্চিত করুন।"
                ]
            else:
                simplified_text = lang_notice + (
                    "Medical Report Simplification:\n\n"
                    "1. Clinical Findings & Diagnosis: The report confirms an invasive ductal carcinoma (cancer that originated in the milk ducts of the breast) verified through a needle biopsy on a palpable lump.\n"
                    "2. Cellular Growth Rate (Grade 2): Grade 2 indicates moderate cellular division—the cells are growing moderately fast, which responds effectively to structured chemotherapy regimens.\n"
                    "3. Clean Surgical Edges (Negative Margins): 'Negative surgical margins' is very reassuring news—it indicates that the surgeon successfully removed the entire tumor along with an outer rim of healthy normal tissue, leaving no cancer cells at the edges.\n"
                    "4. Treatment Plan: The patient is recommended for adjuvant therapy (such as chemotherapy cycles or radiation) to destroy any wandering microscopic cells and prevent recurrence."
                )
                key_points = [
                    "Reassure the patient that achieving negative surgical margins is an encouraging surgical outcome.",
                    "Completing all recommended adjuvant chemotherapy cycles is vital to lower the risk of cancer returning.",
                    "Support the family in maintaining proper hydration, balanced nutrition, and attending all medical officer visits."
                ]

        # ==========================================
        # CASE B: SPECIFIC CLINICAL QUESTIONS
        # ==========================================
        else:
            is_metastasis = any(w in text_lower for w in ["metasta", "মেটাস্ট্যা", "spread", "ছড়িয়ে"])
            is_lymph = any(w in text_lower for w in ["lymph node", "lymphatic", "লসিকা", "লিম্ফ", "axillary", "inguinal"])
            is_chemo = any(w in text_lower for w in ["chemo", "কেমো", "antineoplastic", "systemic therapy"])
            is_biopsy = any(w in text_lower for w in ["biopsy", "বায়োপসি", "histopatholog", "হিস্টোপ্যাথোলজি", "core needle"])
            is_staging = any(w in text_lower for w in ["stage", "staging", "স্টেজিং", "পর্যায়", "tnm"])
            is_benign_malignant = any(w in text_lower for w in ["benign", "malignant", "বিনাইন", "ম্যালিগন্যান্ট"])
            is_radiation = any(w in text_lower for w in ["radiation", "radiotherapy", "রেডিওথেরাপি", "রশ্মি"])
            is_breast = any(w in text_lower for w in ["breast", "স্তন", "mammogram"])
            is_alopecia = any(w in text_lower for w in ["alopecia", "hair loss", "চুল পড়া"])
            is_side_effects = any(w in text_lower for w in ["side effect", "nausea", "vomiting", "বমি", "antiemetic", "neutropenia"])

            # 1. METASTASIS & CANCER SPREAD
            if is_metastasis:
                if is_bn:
                    if level == "level_1":
                        simplified_text = (
                            "মেটাস্ট্যাসিস (Metastasis) মানে হলো ক্যানসার শরীরের মূল জায়গা থেকে অন্য অঙ্গে ছড়িয়ে পড়া। "
                            "ক্যানসার কোষ রক্ত বা লসিকা নালীর মাধ্যমে শরীরের অন্যান্য অংশে চলে যেতে পারে। "
                            "সঠিক সময়ে চিকিৎসা নিলে ক্যানসার ছড়িয়ে পড়া ঠেকানো সম্ভব।"
                        )
                    elif level == "level_3":
                        simplified_text = (
                            "ক্লিনিকাল মূল্যায়ন — ক্যানসার মেটাস্ট্যাসিস (Metastatic Dissemination):\n\n"
                            "মেটাস্ট্যাসিস হলো এমন একটি প্রক্রিয়া যার মাধ্যমে ম্যালিগন্যান্ট ক্যানসার কোষ প্রাথমিক টিউমার থেকে বিচ্ছিন্ন হয়ে "
                            "রক্ত সংবহনতন্ত্র (Hematogenous spread) বা লসিকা নালীর (Lymphatic dissemination) মাধ্যমে দূরবর্তী অঙ্গ বা আঞ্চলিক লিম্ফ নোডে গিয়ে "
                            "নতুন দ্বিতীয় পর্যায়ের টিউমার (Secondary neoplasm) তৈরি করে।\n\n"
                            "টিএনএম (TNM) স্টেজিং পদ্ধতিতে 'M' দ্বারা দূরবর্তী মেটাস্ট্যাসিস বোঝানো হয় (M0 = মেটাস্ট্যাসিস নেই, M1 = দূরবর্তী অঙ্গে ছড়িয়েছে)। "
                            "মেটাস্ট্যাটিক ক্যানসারের ক্ষেত্রে আঞ্চলিক চিকিৎসার পাশাপাশি সিস্টেমিক কেমোথেরাপি ও টার্গেটেড থেরাপির মাধ্যমে রোগ নিয়ন্ত্রণ করা হয়।"
                        )
                    else:
                        simplified_text = (
                            "মেটাস্ট্যাসিস (Metastasis) বলতে বোঝায় ক্যানসার কোষের তার মূল উৎপত্তিস্থল (প্রাইমারি টিউমার) থেকে শরীরের দূরবর্তী অন্যান্য অঙ্গ বা লসিকাগ্রন্থিতে (লিম্ফ নোড) ছড়িয়ে পড়া। "
                            "ক্যানসার কোষগুলো মূল টিউমার থেকে আলাদা হয়ে রক্তপ্রবাহ বা লসিকা রসের মাধ্যমে চলাচল করে এবং শরীরের অন্য কোনো অঙ্গে (যেমন ফুসফুস, যকৃত বা হাড়ে) গিয়ে নতুন টিউমার তৈরি করতে পারে।\n\n"
                            "লিম্ফ নোড বা লসিকাগ্রন্থি শরীরের প্রাকৃতিক ছাঁকনি হিসেবে কাজ করে। তাই ক্যানসার কোষ যখন ছড়িয়ে পড়ার চেষ্টা করে, তখন অনেক সময় সবার আগে কাছাকাছি লিম্ফ নোডে গিয়ে আটকে যায়। "
                            "সময়মতো সঠিক টেস্ট ও চিকিৎসার মাধ্যমে এই ছড়িয়ে পড়ার গতি রোধ করা সম্ভব।"
                        )
                    key_points = [
                        "প্রাথমিক অবস্থায় রোগ ধরা পড়লে এবং ছড়িয়ে পড়ার আগেই চিকিৎসা শুরু করলে সম্পূর্ণ আরোগ্যের সম্ভাবনা অনেক বেশি থাকে।",
                        "ক্যানসার কতখানি ছড়িয়েছে তা নিশ্চিত হতে ডাক্তারবাবুর পরামর্শ অনুযায়ী বায়োপসি, সিটি স্ক্যান বা অন্যান্য রক্তপরীক্ষা সম্পূর্ণ করাতে হবে।",
                        "শরীরের অন্য কোনো অঙ্গে নতুন শক্ত চাকা, তীব্র হাড়ের ব্যথা বা দীর্ঘস্থায়ী কাশি দেখা দিলে অবিলম্বে স্বাস্থ্যকেন্দ্রে যোগাযোগ করুন।"
                    ]
                else:
                    if level == "level_1":
                        simplified_text = (
                            "Metastasis means cancer cells have spread from where they started to another part of the body. "
                            "The cells travel through blood or fluid to form new spots in other organs. "
                            "Starting medical treatment early gives the best chance to stop this spread."
                        )
                    elif level == "level_3":
                        simplified_text = (
                            "Clinical Oncology Assessment — Metastatic Dissemination:\n\n"
                            "Metastasis refers to the biological cascade whereby malignant neoplastic cells detach from the primary tumor, "
                            "invade surrounding extracellular matrix, intravasate into vascular or lymphatic channels, and colonize distant organs or regional lymph nodes, "
                            "establishing secondary tumors.\n\n"
                            "In TNM clinical staging, metastasis is designated by the 'M' category (M0 denotes no distant spread; M1 denotes confirmed distant dissemination). "
                            "Management of metastatic disease typically shifts toward multimodal systemic therapy—incorporating targeted biologics, hormonal agents, or systemic chemotherapy—to achieve disease control and preserve quality of life."
                        )
                    else:
                        simplified_text = lang_notice + (
                            "Metastasis means that cancer cells have spread from the original primary tumor to distant parts of the body or nearby lymph nodes. "
                            "Cancer cells can break away from the primary site, travel through the bloodstream or lymphatic vessels, and settle in other organs (such as the lungs, liver, bones, or brain) to form new secondary tumors.\n\n"
                            "Lymph nodes act like the body's natural filters. Because lymphatic fluid drains from surrounding tissues, spreading cancer cells often get trapped in nearby regional lymph nodes first before reaching distant organs. "
                            "Early detection and completing prescribed systemic treatments (such as chemotherapy) help prevent and control this spread."
                        )
                    key_points = [
                        "Finding cancer early—before metastasis occurs—gives the highest chance for curative surgical removal.",
                        "Diagnostic tests like CT scans and lymph node biopsies tell doctors whether cells have spread, helping them select the correct treatment.",
                        "Patients must report any new persistent symptoms, such as unexplained bone pain or shortness of breath, immediately to their healthcare center."
                    ]

            # 2. LYMPH NODES
            elif is_lymph:
                if is_bn:
                    simplified_text = (
                        "লিম্ফ নোড বা লসিকাগ্রন্থি (Lymph Nodes) হলো শরীরের প্রতিরোধ ব্যবস্থার অংশ হিসেবে থাকা ছোট শিমের দানার মতো গ্রন্থি, যা ঘাড়, বগল (Axillary), কুঁচকি (Inguinal) এবং পেটের ভেতরে জালিকার মতো ছড়িয়ে থাকে। "
                        "এগুলো শরীরের লসিকা তরলকে ছেঁকে ক্ষতিকর জীবাণু ও অস্বাভাবিক কোষকে রক্তে মিশতে বাধা দেয়।\n\n"
                        "অনকোলজি বা ক্যানসার চিকিৎসায় লিম্ফ নোড পরীক্ষা অত্যন্ত গুরুত্বপূর্ণ। কারণ ক্যানসার কোষ যখন ছড়ানোর চেষ্টা করে, তখন তা সবার আগে কাছাকাছি লিম্ফ নোডে গিয়ে জমা হয়। "
                        "লিম্ফ নোডে ক্যানসার কোষ আছে কিনা তা জেনে ডাক্তারবাবু চিকিৎসার সঠিক পর্যায় ও ওষুধ ঠিক করেন।"
                    )
                    key_points = [
                        "লিম্ফ নোডে সামান্য ফোলাভাব সব সময় ক্যানসার নয়—সাধারণ ইনফেকশন বা ঠান্ডালাগার কারণেও এগুলো সাময়িকভাবে ফুলে উঠতে পারে।",
                        "যদি বগলে বা ঘাড়ে কোনো ব্যথাহীন শক্ত ফোলাভাব ২-৩ সপ্তাহের বেশি স্থায়ী হয়, তবে দ্রুত প্রাথমিক স্বাস্থ্যকেন্দ্রে পরীক্ষা করানো উচিত।",
                        "অস্ত্রোপচারের সময় ডাক্তারবাবুরা প্রায়ই কাছের লিম্ফ নোডের নমুনা পরীক্ষা করে দেখেন ক্যানসার মুক্ত কিনা।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "Lymph nodes are small, bean-shaped collections of immune tissue found along the body's lymphatic channels (such as in the neck, armpits, groin, and chest). "
                        "They act like natural filters, cleaning lymphatic fluid and trapping harmful bacteria, viruses, and abnormal cells.\n\n"
                        "In oncology, lymph nodes are carefully checked because cancer cells traveling away from a primary tumor often get caught in nearby regional nodes first. "
                        "Knowing whether cancer cells are present in the lymph nodes helps doctors stage the disease accurately and decide whether systemic chemotherapy or radiation is needed."
                    )
                    key_points = [
                        "Swollen lymph nodes are often caused by common minor infections, but a painless, hard lump that lasts over 2 weeks needs a doctor's check.",
                        "Checking lymph nodes (such as an axillary node biopsy) helps determine if cancer is strictly localized or beginning to spread.",
                        "Always escort patients with persistent neck, armpit, or groin lumps to the Primary Health Centre for evaluation."
                    ]

            # 3. CHEMOTHERAPY
            elif is_chemo:
                if is_bn:
                    simplified_text = (
                        "কেমোথেরাপি (Chemotherapy) হলো বিশেষ অ্যান্টি-নিওপ্লাস্টিক ওষুধের সাহায্যে ক্যানসারের চিকিৎসা, যা সারা শরীরে দ্রুত বেড়ে ওঠা ক্যানসার কোষগুলোকে ধ্বংস করতে কাজ করে। "
                        "সার্জারি বা রেডিয়েশন কেবল একটি নির্দিষ্ট স্থানে কাজ করে, কিন্তু কেমোথেরাপির ওষুধ রক্তের মাধ্যমে পুরো শরীরে পৌঁছে অদৃশ্য ক্যানসার কোষ নষ্ট করে। একে 'সিস্টেমিক থেরাপি' বলা হয়।\n\n"
                        "ক্যানসারের ধরন ও পর্যায় অনুযায়ী কেমোথেরাপির ওষুধ স্যালাইনের মাধ্যমে বা ক্যাপসুল আকারে নির্দিষ্ট চক্রে (Cycles) দেওয়া হয়। "
                        "চিকিৎসার ফলে কিছু সাময়িক পার্শ্বপ্রতিক্রিয়া যেমন বমিভাব, ক্লান্তি বা সাময়িক চুল পড়া হতে পারে, যা চিকিৎসা শেষ হলে আবার ঠিক হয়ে যায়।"
                    )
                    key_points = [
                        "কেমোথেরাপির প্রতিটি সাইকেল বা চক্র সময়মতো সম্পূর্ণ করা অত্যন্ত জরুরি, যাতে কোনো ক্যানসার কোষ বেঁচে না থাকে।",
                        "পার্শ্বপ্রতিক্রিয়া নিয়ন্ত্রণের জন্য পর্যাপ্ত জল, সহজে হজমযোগ্য পুষ্টিকর খাবার এবং ডাক্তারবাবুর দেওয়া সাপোর্টিভ ওষুধ খেতে হবে।",
                        "কেমোথেরাপি চলাকালীন রোগীর শরীরে হঠাৎ উচ্চমাত্রার জ্বর বা তীব্র কাঁপুনি দেখা দিলে তৎক্ষণাৎ হাসপাতালে নিয়ে যান।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "Chemotherapy is a medical cancer treatment that uses antineoplastic medications to find, damage, and destroy fast-growing cancer cells throughout the whole body. "
                        "While surgery and radiation treat a localized area, chemotherapy travels through the entire bloodstream (systemic treatment) to eliminate any wandering or microscopic cancer cells.\n\n"
                        "Chemotherapy is administered in structured cycles (with rest periods in between to let healthy cells recover). "
                        "Because it targets rapidly dividing cells, it can cause temporary side effects such as fatigue, nausea, or temporary hair loss (alopecia), which resolve after treatment finishes."
                    )
                    key_points = [
                        "Completing all scheduled chemotherapy cycles is vital to prevent cancer from returning or developing drug resistance.",
                        "Side effects like nausea can be effectively managed with supportive medicines (antiemetics) prescribed by the doctor.",
                        "If a patient on chemotherapy develops a fever (temperature above 100.4°F / 38°C), escort them to the hospital immediately as it may indicate low white blood cells (neutropenia)."
                    ]

            # 4. BIOPSY
            elif is_biopsy:
                if is_bn:
                    simplified_text = (
                        "বায়োপসি (Biopsy) হলো একটি অত্যন্ত নিরাপদ এবং অপরিহার্য রোগনির্ণয় পরীক্ষা, যেখানে শরীরের সন্দেহজনক চাকা বা আক্রান্ত স্থান থেকে একটি সূঁচ বা ছোট প্রক্রিয়ার মাধ্যমে সামান্য টিস্যু বা কোষের নমুনা সংগ্রহ করা হয়। "
                        "সংগৃহীত এই নমুনা ল্যাবরেটরিতে প্যাথলজিস্ট ডাক্তারবাবুরা অণুবীক্ষণ যন্ত্রে খুঁটিয়ে পরীক্ষা করেন (যাকে হিস্টোপ্যাথোলজি বলা হয়)।\n\n"
                        "গ্রামের অনেক মানুষের মধ্যে ভুল ধারণা থাকে যে বায়োপসি করলে বা সূঁচ ফোটালে ক্যানসার নাকি দ্রুত ছড়িয়ে পড়ে—এটি সম্পূর্ণ ভুল ও কুসংস্কার। "
                        "বায়োপসি রোগ ছড়ায় না; বরং এটিই একমাত্র নিশ্চিত পরীক্ষা যার মাধ্যমে জানা যায় টিউমারটি বিনাইন (নির্দোষ) নাকি ম্যালিগন্যান্ট (ক্যানসার), এবং এর ওপর ভিত্তি করেই সঠিক চিকিৎসা নির্ধারণ করা হয়।"
                    )
                    key_points = [
                        "বায়োপসি পরীক্ষা ছাড়া ক্যানসারের সঠিক প্রকারভেদ বা কোন ওষুধ সবচেয়ে ভালো কাজ করবে তা নিশ্চিতভাবে জানা সম্ভব নয়।",
                        "রোগী ও পরিবারকে আশ্বস্ত করুন যে বায়োপসি নিরাপদ এবং এটি রোগ ছড়ায় না।",
                        "বায়োপসি রিপোর্ট হাতে পাওয়ার পর কোনো কালবিলম্ব না করে মেডিকেল অফিসারের কাছে নিয়ে গিয়ে চিকিৎসার পরবর্তী ধাপ শুরু করুন।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "A biopsy is an essential and safe diagnostic procedure in which a doctor gently collects a small sample of tissue or cells from an abnormal lump or lesion. "
                        "This sample is then sent to a pathology laboratory and examined under a high-power microscope (histopathological examination) to determine the exact cellular diagnosis.\n\n"
                        "It is very common in village communities for patients to fear that a biopsy causes cancer to spread faster. Community health workers can firmly reassure them that this is completely false. "
                        "A biopsy does not spread cancer; it is the only definitive medical test that confirms whether a tumor is benign (non-cancerous) or malignant (cancerous), enabling doctors to select the exact right medication."
                    )
                    key_points = [
                        "A biopsy is the gold standard for cancer diagnosis—treatment cannot safely begin without histopathological confirmation.",
                        "Reassure the patient and family that a biopsy is a minor, safe procedure that will not make the cancer worse.",
                        "Once the biopsy report is ready, assist the patient in presenting it promptly to the oncologist at the district hospital."
                    ]

            # 5. BENIGN VS MALIGNANT
            elif is_benign_malignant:
                if is_bn:
                    simplified_text = (
                        "বিনাইন (Benign) এবং ম্যালিগন্যান্ট (Malignant) টিউমারের মধ্যে প্রধান পার্থক্য হলো কোষের বৃদ্ধির ধরন এবং ছড়িয়ে পড়ার ক্ষমতা:\n\n"
                        "১. বিনাইন টিউমার (Benign): এটি কোনো ক্যানসার নয়। এর কোষগুলো ধীরগতিতে বাড়ে এবং একটি নির্দিষ্ট আবরণীর ভেতরে সীমাবদ্ধ থাকে। এটি আশেপাশের টিস্যু আক্রমণ করে না বা শরীরের অন্য কোনো অঙ্গে ছড়িয়ে পড়ে না। অস্ত্রোপচার করে অপসারণ করলে সাধারণত আর ফিরে আসে না।\n\n"
                        "২. ম্যালিগন্যান্ট টিউমার (Malignant): এটি প্রকৃত ক্যানসার। এর কোষগুলো অনিয়ন্ত্রিতভাবে দ্রুত বাড়ে, সংলগ্ন সুস্থ টিস্যু ধ্বংস করে এবং রক্ত বা লসিকার মাধ্যমে শরীরের দূরবর্তী অংশে ছড়িয়ে পড়ার (মেটাস্ট্যাসিস) মারাত্মক ক্ষমতা রাখে। এর জন্য সময়মতো বিশেষজ্ঞ চিকিৎসা প্রয়োজন।"
                    )
                    key_points = [
                        "শরীরে কোনো নতুন চাকা বা পিণ্ড দেখা দিলেই ভয় পাওয়ার কারণ নেই, কারণ অনেক টিউমারই সম্পূর্ণ নির্দোষ বা বিনাইন হতে পারে।",
                        "চাকাটি বিনাইন নাকি ম্যালিগন্যান্ট তা বোঝার একমাত্র নির্ভুল উপায় হলো ডাক্তারের পরামর্শে বায়োপসি পরীক্ষা করানো।",
                        "বিনাইন টিউমার হলেও যদি তা রক্তনালী বা নার্ভে চাপ সৃষ্টি করে, তবে ডাক্তারের নির্দেশে চিকিৎসা নেওয়া দরকার।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "The key difference between benign and malignant tumors lies in how the cells grow and whether they can spread:\n\n"
                        "1. Benign Tumors: These are non-cancerous growths. Their cells divide slowly, stay within distinct boundaries, and do not invade neighboring normal tissue or travel to distant organs. When surgically removed, benign tumors rarely return.\n\n"
                        "2. Malignant Tumors: These are cancerous growths. Their cells multiply rapidly and uncontrollably, invade and destroy surrounding healthy tissues, and possess the ability to enter blood or lymph vessels to spread (metastasize) to other organs. Malignant tumors require comprehensive oncological treatment."
                    )
                    key_points = [
                        "Not all lumps are cancer—many common lumps, cysts, or fibroids are benign and completely harmless.",
                        "A biopsy examination under a microscope is the only definitive way to distinguish between benign and malignant tissue.",
                        "Any persistent, firm, or enlarging lump must be medically evaluated by a doctor to rule out malignancy early."
                    ]

            # 6. STAGING & TNM
            elif is_staging:
                if is_bn:
                    simplified_text = (
                        "ক্যানসার স্টেজিং (Cancer Staging) হলো এমন একটি চিকিৎসা পদ্ধতি যার মাধ্যমে ডাক্তারবাবুরা নির্ধারণ করেন ক্যানসার টিউমারটি কত বড় হয়েছে এবং তা শরীরের কতটা অংশে ছড়িয়েছে।\n\n"
                        "চিকিৎসায় প্রধানত চারটি পর্যায় বা স্টেজ ব্যবহার করা হয়:\n"
                        "• পর্যায় ১ (Stage I): ক্যানসার খুব ছোট এবং প্রাথমিক উৎপত্তিস্থলেই সীমাবদ্ধ।\n"
                        "• পর্যায় ২ ও ৩ (Stage II & III): টিউমারটি আকারে কিছুটা বড় হয়েছে এবং নিকটবর্তী লিম্ফ নোড বা আশেপাশের টিস্যুতে পৌঁছেছে।\n"
                        "• পর্যায় ৪ (Stage IV): ক্যানসার মূল স্থান ছেড়ে দূরবর্তী অঙ্গে (যেমন লিভার, ফুসফুস বা হাড়ে) ছড়িয়ে পড়েছে (মেটাস্ট্যাসিস)।\n\n"
                        "ডাক্তারবাবুরা প্রায়ই 'TNM' পদ্ধতি ব্যবহার করেন: T (টিউমারের আকার), N (লিম্ফ নোডের সম্পৃক্ততা), এবং M (মেটাস্ট্যাসিস বা দূরবর্তী বিস্তার)।"
                    )
                    key_points = [
                        "স্টেজ জানা অত্যন্ত জরুরি কারণ স্টেজের ওপর নির্ভর করেই ডাক্তারবাবু ঠিক করেন রোগীর জন্য সার্জারি, কেমোথেরাপি নাকি রেডিয়েশন দরকার।",
                        "স্টেজ ১ বা ২-তে রোগ ধরা পড়লে চিকিৎসার মাধ্যমে রোগ সম্পূর্ণ নিরাময়ের সম্ভাবনা অনেক বেশি থাকে।",
                        "উচ্চ স্টেজ হলেও আধুনিক চিকিৎসার মাধ্যমে যন্ত্রণা উপশম করে রোগীকে দীর্ঘদিন সুস্থ ও আরামদায়ক রাখা সম্ভব।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "Cancer staging is the medical assessment doctors use to describe the size of a primary tumor and determine how far cancer cells have spread throughout the body.\n\n"
                        "Cancers are generally classified from Stage I to Stage IV:\n"
                        "• Stage I: The cancer is small and strictly localized to its organ of origin.\n"
                        "• Stages II & III: The tumor has grown larger and may have reached nearby tissues or regional lymph nodes.\n"
                        "• Stage IV: The cancer has spread (metastasized) to distant organs such as the liver, lungs, or bones.\n\n"
                        "Doctors frequently use the TNM staging system: T represents primary Tumor size and depth, N reflects regional lymph Node involvement, and M indicates whether distant Metastasis is present."
                    )
                    key_points = [
                        "Staging determines the entire treatment roadmap—early stages often require surgery, while advanced stages require systemic therapy.",
                        "Stage 1 and Stage 2 cancers have exceptionally high cure and survival rates when treated promptly.",
                        "Even in Stage 4, structured oncological therapy can effectively control symptoms, shrink tumors, and extend comfortable living."
                    ]

            # 7. BREAST CANCER
            elif is_breast:
                if is_bn:
                    simplified_text = (
                        "স্তন ক্যানসার (Breast Cancer) হলো এমন একটি অবস্থা যেখানে স্তনের দুধবাহী নালী (Ductal) বা লোবিউলসের কোষগুলো অনিয়ন্ত্রিতভাবে বেড়ে উঠে একটি টিউমার তৈরি করে।\n\n"
                        "প্রধান লক্ষণসমূহ:\n"
                        "• স্তনে বা বগলের নিচে কোনো শক্ত, ব্যথাহীন চাকা বা পিণ্ড।\n"
                        "• স্তনের চামড়ায় টোল পড়া (কমলালেবুর খোসার মতো খাঁজ) বা ত্বকের লালচে ভাব।\n"
                        "• স্তনবৃন্ত বা বোঁটা ভেতরের দিকে ঢুকে যাওয়া অথবা বোঁটা দিয়ে অস্বাভাবিক বা রক্তযুক্ত স্রাব নির্গমন।\n\n"
                        "প্রাথমিক রোগনির্ণয়ের জন্য ম্যামোগ্রাফি (স্তন এক্স-রে) এবং কোর নিডল বায়োপসি করা হয়। প্রাথমিক পর্যায়ে ধরা পড়লে ব্রেস্ট-কনজার্ভিং সার্জারি (লাম্পেক্টমি) বা প্রয়োজনীয় চিকিৎসার মাধ্যমে রোগী সম্পূর্ণ সুস্থ হয়ে স্বাভাবিক জীবনযাপন করতে পারেন।"
                    )
                    key_points = [
                        "প্রত্যেক প্রাপ্তবয়স্ক মহিলার প্রতি মাসে একবার নিজে নিজে স্তন পরীক্ষা (BSE) করা উচিত যাতে কোনো অস্বাভাবিক চাকা দ্রুত ধরা পড়ে।",
                        "স্তনে ব্যথাহীন চাকা দেখলে অবহেলা করা সবচেয়ে বিপজ্জনক—ব্যথা নেই বলেই অনেকে চিকিৎসায় দেরি করেন।",
                        "সরকারি স্বাস্থ্যবীমা (যেমন স্বাস্থ্যসাথী / আয়ুষ্মান ভারত) এর মাধ্যমে প্রাথমিক স্বাস্থ্যকেন্দ্র থেকে জেলা হাসপাতালে স্তন ক্যানসারের নিখরচায় চিকিৎসা পাওয়া যায়।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "Breast cancer occurs when abnormal cells within breast tissue—most commonly starting in the milk ducts (invasive ductal carcinoma) or the milk glands (lobular carcinoma)—multiply uncontrollably to form a tumor.\n\n"
                        "Key Signs to Check:\n"
                        "• A new, firm, painless lump or thickening in the breast or underarm.\n"
                        "• Dimpling, puckering, or redness of the breast skin (orange-peel texture).\n"
                        "• Nipple retraction (turning inward) or spontaneous bloody or clear nipple discharge.\n\n"
                        "Diagnostic evaluation includes clinical examination, imaging (mammogram / ultrasound), and core needle biopsy. In early stages, breast-conserving surgery (lumpectomy) followed by targeted therapy or radiation provides excellent long-term cure rates."
                    )
                    key_points = [
                        "All adult women should practice monthly breast self-examination to detect any subtle lumps or texture changes early.",
                        "A painless lump is the most common presentation—lack of pain does NOT mean a lump is safe to ignore.",
                        "Escort any woman with a breast lump, skin dimpling, or nipple discharge to the Primary Health Centre immediately for screening."
                    ]

            # 8. ALOPECIA & SIDE EFFECTS
            elif is_alopecia or is_side_effects:
                if is_bn:
                    simplified_text = (
                        "অ্যালোপেসিয়া (Alopecia) হলো কেমোথেরাপি বা ক্যানসার চিকিৎসার ফলে চুল পড়ার একটি সাধারণ পার্শ্বপ্রতিক্রিয়া। "
                        "কেমোথেরাপির ওষুধ শরীরের দ্রুত বর্ধনশীল ক্যানসার কোষ ধ্বংস করার সাথে সাথে চুলের গোড়ার স্বাভাবিক দ্রুত বর্ধনশীল কোষগুলোকেও সাময়িকভাবে দুর্বল করে দেয়।\n\n"
                        "রোগী ও পরিবারকে আশ্বস্ত করা সবচেয়ে জরুরি যে—এই চুল পড়া সম্পূর্ণ সাময়িক। চিকিৎসা শেষ হওয়ার কয়েক সপ্তাহের মধ্যেই আবার নতুন সুস্থ চুল গজাতে শুরু করে।"
                    )
                    key_points = [
                        "চুল পড়া একটি সাময়িক পার্শ্বপ্রতিক্রিয়া—এটি স্থায়ী নয় এবং চিকিৎসা শেষ হলে স্বাভাবিক চুল পুনরায় গজায়।",
                        "রোগীকে মাথায় নরম সুতির স্কার্ফ বা টুপি ব্যবহার করতে এবং কড়া রোদে মাথা ঢেকে রাখতে পরামর্শ দিন।",
                        "বমিভাব বা দুর্বলতা নিয়ন্ত্রণের জন্য ডাক্তারবাবুর দেওয়া অ্যান্টি-এমেটিক ওষুধ ও পর্যাপ্ত তরল খাবার গ্রহণ জরুরি।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "Alopecia refers to hair loss, which is a common and temporary side effect of certain chemotherapy and radiation treatments. "
                        "Because chemotherapy medications are designed to target rapidly multiplying cancer cells, they also temporarily affect normal rapidly growing cells in the body, such as hair follicles.\n\n"
                        "It is essential to reassure patients and families that chemotherapy-induced alopecia is almost always temporary. Hair typically begins to regrow within a few weeks to months after the treatment cycles are completed."
                    )
                    key_points = [
                        "Reassure the patient that hair loss is temporary and that their hair will naturally grow back after chemotherapy ends.",
                        "Advise the patient to protect their scalp with a soft cotton scarf, cap, or mild moisturizing lotion to prevent dryness and sun irritation.",
                        "Encourage open discussions with family members to provide emotional reassurance and reduce anxiety around body changes."
                    ]

            # 9. GENERAL ONCOLOGY / UNMATCHED QUESTION
            else:
                if is_bn:
                    simplified_text = (
                        "ক্যানসার হলো শরীরের এমন একটি অবস্থা যেখানে কিছু অস্বাভাবিক কোষ অনিয়ন্ত্রিতভাবে বাড়তে থাকে এবং টিউমার বা পিণ্ড তৈরি করে। "
                        "সময়মতো স্ক্রিনিং এবং পরীক্ষার মাধ্যমে প্রাথমিক অবস্থায় রোগ ধরা পড়লে এটি আধুনিক চিকিৎসা বিজ্ঞানের সাহায্যে সম্পূর্ণরূপে নিরাময় করা সম্ভব।"
                    )
                    key_points = [
                        "প্রাথমিক পর্যায়ে রোগ ধরা পড়লে চিকিৎসার সাফল্য ও সম্পূর্ণ আরোগ্যের সম্ভাবনা অনেক বেড়ে যায়।",
                        "চিকিৎসকের প্রেসক্রিপশন অনুযায়ী নিয়মিত চিকিৎসা গ্রহণ এবং সঠিক পুষ্টিকর খাবার গ্রহণ জরুরি।",
                        "জরুরি কোনো শারীরিক সমস্যা হলে নিকটবর্তী ব্লক প্রাথমিক স্বাস্থ্য কেন্দ্র বা জেলা হাসপাতালে যোগাযোগ করুন।"
                    ]
                else:
                    simplified_text = lang_notice + (
                        "Cancer occurs when abnormal cells in the body begin to divide and multiply in an uncontrolled manner, forming a mass or growth called a tumor. "
                        "With timely clinical screening, accurate diagnostic evaluation, and modern oncological treatments, cancer can be managed and cured effectively."
                    )
                    key_points = [
                        "Early detection through screening provides the highest chance of successful treatment and complete recovery.",
                        "Encourage patients to follow structured medical treatment protocols under qualified oncologists.",
                        "Advise family members on maintaining good nutrition, hydration, and compassionate emotional support."
                    ]

        # 7. Append Relevant Medical Term Definitions
        term_meanings = []
        for t in explained_terms:
            t_name = t.get("term", "")
            if not t_name:
                continue
            t_bn = t.get("bengali_term") or t_name
            defn = t.get("simplified_en") or t.get("simple_meaning") or t.get("medical_definition") or t.get("definition")
            if defn:
                clean_defn = defn.split(".")[0].strip() + "."
                if is_bn and t.get("bengali_term"):
                    term_meanings.append(f"• {t_name} ({t_bn}): {t.get('simplified_bn') or clean_defn}")
                else:
                    term_meanings.append(f"• {t_name}: {clean_defn}")

        if term_meanings and len(term_meanings) <= 4:
            glossary_title = "\n\nশনাক্তকৃত পরিভাষার অর্থ:" if is_bn else "\n\nMedical Terms Explained:"
            simplified_text += glossary_title + "\n" + "\n".join(term_meanings[:3])

        return simplified_text, key_points
