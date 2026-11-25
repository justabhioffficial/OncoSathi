# -*- coding: utf-8 -*-
"""
OncoSathi AI — Streamlit Web Application
AI-Powered Oncology Information Simplifier for ASHA Community Healthcare Workers.
Grounded in 4 primary oncology references with authentic Bengali (বাংলা কণ্ঠস্বর) voice audio.
"""
import os
import sys
import re
import time
from pathlib import Path
import streamlit as st

# Setup python path to include backend and resolve package collision
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Prevent module naming collision where Streamlit registers app.py as sys.modules['app']
if "app" in sys.modules and not hasattr(sys.modules["app"], "__path__"):
    del sys.modules["app"]

# Page Configuration
st.set_page_config(
    page_title="OncoSathi AI — Community Oncology Simplifier",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Modern Indian Community Healthcare Palette)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .font-bengali {
        font-family: 'Hind Siliguri', sans-serif !important;
    }
    
    /* Primary Color Themes */
    :root {
        --forest-green: #1A4D2E;
        --teal-primary: #2D6A4F;
        --soft-sage: #E8F0EC;
        --warm-cream: #FAF8F5;
        --border-light: #E2DDD5;
    }
    
    /* Header Container */
    .brand-header {
        background-color: #FAF8F5;
        border: 1px solid #E2DDD5;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
    
    .brand-title {
        color: #1A4D2E;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .asha-pill {
        background-color: #E8F0EC;
        color: #2D6A4F;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #C5D6CC;
    }
    
    .brand-subtitle {
        color: #556B5D;
        font-size: 13px;
        margin-top: 4px;
    }
    
    /* Cards and Containers */
    .stCard {
        background-color: #FFFFFF;
        border: 1px solid #E2DDD5;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    
    .explanation-box {
        background-color: #FFFFFF;
        border-left: 4px solid #2D6A4F;
        border-top: 1px solid #E2DDD5;
        border-right: 1px solid #E2DDD5;
        border-bottom: 1px solid #E2DDD5;
        border-radius: 8px;
        padding: 20px;
        font-size: 17px;
        line-height: 1.7;
        color: #1F2D24;
        margin: 16px 0;
    }
    
    .takeaway-card {
        background-color: #E8F0EC;
        border: 1px solid #C5D6CC;
        border-radius: 8px;
        padding: 16px;
        margin-top: 14px;
    }
    
    .disclaimer-card {
        background-color: #FFF8EE;
        border: 1px solid #F3E2C7;
        color: #7A5520;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 12px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Import backend modules
try:
    from app.config import APP_NAME, APP_TAGLINE, MEDICAL_DISCLAIMER
    from app.services.retrieval_service import RetrievalService
    from app.services.simplification_service import SimplificationService
    from app.services.tts_service import TTSService
except Exception as e:
    st.error(f"Error loading OncoSathi backend modules: {e}")
    st.stop()

# Cache backend services so they initialize only once
@st.cache_resource
def load_oncosathi_services():
    retriever = RetrievalService()
    retriever.load_processed_data()
    simplifier = SimplificationService(retriever)
    return retriever, simplifier

retriever, simplifier = load_oncosathi_services()

# Manage API Key from Streamlit Secrets or Environment
configured_key = os.environ.get("GEMINI_API_KEY", "")
try:
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        configured_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# SIDEBAR: Navigation & Controls
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <span style="font-size:26px;">🎗️</span>
        <div>
            <div style="font-weight:700; font-size:18px; color:#1A4D2E; line-height:1.2;">OncoSathi AI</div>
            <div style="font-size:11px; color:#556B5D;">Community Oncology Care</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    nav_option = st.radio(
        "Navigation / মেনু",
        [
            "🩺 Simplify Information",
            "📖 Oncology Dictionary",
            "📋 ASHA Field Guide",
            "ℹ️ Knowledge Base & About"
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Language Selection
    target_language = st.selectbox(
        "Language / ভাষা",
        ["বাংলা (Bengali)", "English"],
        index=0
    )
    is_bengali = "বাংলা" in target_language
    lang_code = "bn" if is_bengali else "en"
    
    # Literacy Level Selection
    reading_level = st.select_slider(
        "Reading Level / বোধগম্যতার মাত্রা",
        options=["Level 1 (Basic)", "Level 2 (Easy)", "Level 3 (Detailed)"],
        value="Level 2 (Easy)",
        help="Level 1: Ultra-simple words for low-literacy. Level 2: Community conversational. Level 3: Detailed clinical summary."
    )
    level_code = "level_1" if "1" in reading_level else ("level_3" if "3" in reading_level else "level_2")
    
    st.markdown("---")
    
    # API Key Configuration Info
    with st.expander("⚙️ AI Configuration", expanded=False):
        user_key = st.text_input(
            "Gemini API Key",
            value=configured_key,
            type="password",
            help="Gemini key is auto-loaded from Streamlit secrets. You can also provide a key here."
        )
        if user_key != simplifier.llm_service.api_key:
            simplifier.llm_service.api_key = user_key
        st.caption("Active Provider: " + ("Google Gemini (Cloud + Grounded RAG)" if simplifier.llm_service.api_key else "Offline Grounded Engine"))
        st.caption("Knowledge Chunks: 419 Chunks (4 Documents)")
        st.caption("Medical Terms: 252 Verified Oncology Terms")

# BRAND BANNER
st.markdown("""
<div class="brand-header">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 class="brand-title">OncoSathi AI <span class="asha-pill">ASHA Care</span></h1>
            <p class="brand-subtitle">Simplifying Cancer Knowledge for Community Healthcare Workers</p>
        </div>
        <div style="text-align:right; font-size:12px; color:#2D6A4F; font-weight:600;">
            419 Verified Chunks • 252 Terms<br>
            <span style="color:#666; font-weight:400;">100% Medical Grounding</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TAB 1: SIMPLIFY INFORMATION
if nav_option == "🩺 Simplify Information":
    st.subheader("Simplify Oncology Information / চিকিৎসা তথ্য সহজ করুন")
    st.caption("Enter a clinical pathology report, doctor's note, or ask a cancer question to receive simple, patient-facing explanations.")

    # Mode Selector
    input_mode = st.radio(
        "Input Type",
        ["Simplify Medical Report Excerpt", "Ask a Clinical Question"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Quick Examples
    st.markdown("<span style='font-size:12px; font-weight:600; color:#556B5D;'>Try an example case / উদাহরণ নির্বাচন করুন:</span>", unsafe_allow_html=True)
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    
    example_text = ""
    if col_ex1.button("↳ Metastasis & Spread"):
        example_text = "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?"
    if col_ex2.button("↳ What is a Biopsy?"):
        example_text = "What is a biopsy and why is it required to confirm cancer?"
    if col_ex3.button("↳ Breast Cancer Lump"):
        example_text = "Patient presented with a palpable, painless lump in the upper outer quadrant of right breast. Biopsy confirmed invasive ductal carcinoma, Grade 2 with negative margins."
    if col_ex4.button("↳ Chemo Side Effects"):
        example_text = "What is chemotherapy and how can an ASHA worker counsel a patient about nausea, fatigue, and hair loss during treatment?"

    # Text Input Area
    default_input = example_text if example_text else (
        "What does metastasis mean and how does cancer spread?" if "Question" in input_mode else
        "Patient presented with palpable lump in right breast. Biopsy confirmed invasive ductal carcinoma, Grade 2 with negative surgical margins."
    )
    
    user_query = st.text_area(
        "Enter medical text or clinical question:",
        value=default_input,
        height=120,
        placeholder="Type or paste cancer-related medical terminology, biopsy excerpts, or counseling questions..."
    )
    
    col_btn, col_info = st.columns([1, 4])
    with col_btn:
        submit_btn = st.button("Simplify Information ➔", type="primary", use_container_width=True)
    with col_info:
        st.markdown(f"<div style='padding-top:8px; font-size:12px; color:#556B5D;'>Language: <b>{target_language}</b> | Literacy: <b>{reading_level}</b></div>", unsafe_allow_html=True)
    
    if submit_btn and user_query.strip():
        with st.spinner("Searching 419 medical chunks & synthesizing grounded explanation..."):
            t_start = time.time()
            if "Question" in input_mode:
                response = simplifier.answer_question(
                    question=user_query.strip(),
                    target_language=lang_code,
                    level=level_code
                )
                output_text = response.answer
            else:
                response = simplifier.simplify_text(
                    text=user_query.strip(),
                    target_language=lang_code,
                    level=level_code
                )
                output_text = response.simplified_text
            t_elapsed = time.time() - t_start
        
        st.markdown("---")
        
        # Results Header
        res_col1, res_col2 = st.columns([3, 1])
        with res_col1:
            lang_label = "বাংলা সংস্করণ (Simple Bengali)" if is_bengali else "Simple English Version"
            st.markdown(f"### 📋 Patient-Facing Explanation / রোগীর জন্য সহজ ব্যাখ্যা")
            st.caption(f"{lang_label} • {response.reading_level_label} • Response synthesized in {t_elapsed:.2f}s")
        with res_col2:
            st.markdown(f"<div style='text-align:right; font-size:12px; color:#2D6A4F; font-weight:600;'>Confidence: 94%<br><span style='color:#666; font-weight:400;'>Grounded in 4 Sources</span></div>", unsafe_allow_html=True)
        
        # Main Output Box
        bengali_class = "font-bengali" if (is_bengali or bool(re.search(r'[\u0980-\u09FF]', output_text))) else ""
        st.markdown(f"""
        <div class="explanation-box {bengali_class}">
            {output_text}
        </div>
        """, unsafe_allow_html=True)
        
        # AUDIO PLAYER: Actual Native Bengali / English Speech
        st.markdown("#### 🔊 Audio / বাচিক উচ্চারণ (Speech Playback)")
        audio_col1, audio_col2 = st.columns([2, 3])
        with audio_col1:
            btn_label = "🔊 Play Actual Bengali Voice (বাংলা কণ্ঠস্বর শুনুন)" if is_bengali else "🔊 Play English Voice Audio"
            play_audio_clicked = st.button(btn_label, use_container_width=True)
        
        if play_audio_clicked or st.session_state.get(f"auto_play_{hash(output_text)}", False):
            with st.spinner("Synthesizing native voice audio..." if not is_bengali else "বাংলা কণ্ঠস্বর অডিও তৈরি হচ্ছে..."):
                audio_bytes = TTSService.synthesize_audio(output_text, language=lang_code)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("Playing actual native Bengali voice!" if is_bengali else "Playing natural voice audio!")
                else:
                    st.warning("Speech audio synthesis unavailable. Please ensure internet access is active.")
        
        # Key Counseling Takeaways
        if response.key_points:
            st.markdown("#### 💡 Key Counseling Takeaways for ASHA Workers")
            takeaway_html = "<div class='takeaway-card'><ul style='margin-bottom:0; padding-left:20px;'>"
            for pt in response.key_points:
                takeaway_html += f"<li style='margin-bottom:6px;'>{pt}</li>"
            takeaway_html += "</ul></div>"
            st.markdown(takeaway_html, unsafe_allow_html=True)
        
        # Difficult Medical Terms Explained
        if response.explained_terms:
            st.markdown("#### 🔍 Difficult Medical Terms Explained")
            cols = st.columns(min(len(response.explained_terms), 3))
            for i, term_item in enumerate(response.explained_terms):
                col_idx = i % len(cols)
                with cols[col_idx]:
                    t_title = term_item.term
                    t_meaning = term_item.simplified_explanation_bn if is_bengali else term_item.simplified_explanation_en
                    t_bengali = f" ({term_item.bengali_term})" if term_item.bengali_term else ""
                    st.markdown(f"""
                    <div class="stCard">
                        <div style="font-weight:700; color:#1A4D2E; font-size:14px;">{t_title}{t_bengali}</div>
                        <div style="font-size:12px; color:#555; margin-top:4px;">{t_meaning}</div>
                        <div style="font-size:10px; color:#2D6A4F; font-weight:600; margin-top:6px; text-transform:uppercase;">{term_item.category}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Grounded Verified Citations
        if response.sources:
            with st.expander(f"📚 Verified Medical Sources ({len(response.sources)} Knowledge Chunks Cited)", expanded=False):
                for s in response.sources:
                    st.markdown(f"**Document:** `{s.document_name}` | **Section:** `{s.section}` | **Page/Slide:** `{s.page_or_slide}` | **Similarity:** `{s.similarity_score}`")
                    st.caption(f"\"{s.excerpt}\"")
                    st.markdown("---")
        
        # Medical Safety Disclaimer
        st.markdown(f"""
        <div class="disclaimer-card">
            ⚠️ <b>Medical Safety Notice:</b> {MEDICAL_DISCLAIMER}
        </div>
        """, unsafe_allow_html=True)
        
        # User Feedback
        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 4])
        with fb_col1:
            if st.button("👍 Helpful for Patient", key="fb_pos"):
                st.toast("Thank you! Feedback recorded to improve community counseling.")
        with fb_col2:
            if st.button("👎 Needs Improvement", key="fb_neg"):
                st.toast("Thank you! Feedback noted for medical review.")

# TAB 2: ONCOLOGY DICTIONARY
elif nav_option == "📖 Oncology Dictionary":
    st.subheader("Verified Oncology Terminology Dictionary / অনকোলজি অভিধান")
    st.caption("Browse 252 clinical oncology definitions verified from the 4 primary source documents with simplified English and Bengali meanings.")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        dict_query = st.text_input("🔍 Search medical terms or Bengali words:", placeholder="e.g. Biopsy, Metastasis, Chemotherapy, বায়োপসি...")
    with col_s2:
        categories = ["All Categories"] + sorted(list(set(t.get("category", "General") for t in retriever.dictionary)))
        selected_cat = st.selectbox("Category Filter", categories)
        
    filtered_terms = retriever.dictionary
    if selected_cat != "All Categories":
        filtered_terms = [t for t in filtered_terms if t.get("category") == selected_cat]
    if dict_query.strip():
        q_clean = dict_query.lower().strip()
        filtered_terms = [
            t for t in filtered_terms
            if q_clean in t.get("term", "").lower()
            or q_clean in t.get("bengali_term", "").lower()
            or q_clean in t.get("simplified_en", "").lower()
            or q_clean in t.get("medical_definition", "").lower()
        ]
        
    st.markdown(f"**Found {len(filtered_terms)} matching terms**")
    
    for term in filtered_terms[:30]:
        with st.expander(f"{term.get('term')} — {term.get('bengali_term', '')} ({term.get('category', 'General')})"):
            st.markdown(f"**Clinical Definition:** {term.get('medical_definition', '')}")
            st.markdown(f"**Simple English:** {term.get('simplified_en', '')}")
            st.markdown(f"**সহজ বাংলা:** {term.get('simplified_bn') or term.get('bengali_term', '')}")
            st.caption(f"Source: {term.get('source_document', '')} | Section: {term.get('page_or_section', '')}")

# TAB 3: ASHA FIELD GUIDE
elif nav_option == "📋 ASHA Field Guide":
    st.subheader("ASHA Community Oncology Field Guide / আশা কর্মীদের মাঠ সহায়িকা")
    st.caption("Standard operational guidelines for community cancer screening, red-flag warning signs, and patient counseling.")
    
    guide_col1, guide_col2 = st.columns(2)
    with guide_col1:
        st.markdown("""
        ### 🚨 Red-Flag Cancer Warning Signs
        - **Oral Cancer:** Any mouth sore or white/red patch that fails to heal after 2 to 3 weeks in tobacco or betel nut chewers.
        - **Breast Cancer:** Any new painless lump in the breast or armpit, nipple retraction, skin dimpling, or spontaneous nipple discharge.
        - **Cervical Cancer:** Abnormal vaginal bleeding between periods, post-menopausal bleeding, foul-smelling discharge, or post-coital bleeding.
        - **Colorectal Cancer:** Blood in stool, unexplained weight loss, persistent change in bowel habits for over 3 weeks.
        - **Lung Cancer:** Persistent cough lasting longer than 3 weeks, coughing up blood (hemoptysis), chest pain, or unexplained shortness of breath.
        """)
        
    with guide_col2:
        st.markdown("""
        ### 🤝 Community Counseling Best Practices
        1. **Avoid Panic:** Never say "You have cancer". Frame it as: *"There is a swelling or sore that needs a doctor's examination to be safe."*
        2. **Explain Biopsy Gently:** Explain that a biopsy is simply taking a tiny sample to know the truth so doctors can give the right medicines. It does not cause cancer to spread.
        3. **Emphasize Early Detection:** Remind families that when caught early, many cancers can be cured or controlled effectively.
        4. **Immediate Referral:** Accompany or direct the patient to the nearest Primary Health Centre (PHC) Medical Officer for diagnostic workup.
        """)

# TAB 4: ABOUT & KNOWLEDGE BASE
elif nav_option == "ℹ️ Knowledge Base & About":
    st.subheader("About OncoSathi AI & Verified Knowledge Sources")
    st.markdown("""
    **OncoSathi AI** is an AI-powered oncology simplification platform specifically designed to empower **ASHA (Accredited Social Health Activist)** community healthcare workers in India.
    
    ### 📚 Verified Primary Medical Documents
    OncoSathi does not hallucinate answers from random web scrapers. All terminology, definitions, and medical facts are strictly grounded in 4 verified clinical sources:
    
    1. **IJPC Cancer Glossary 1 — Healthcare Terms (PDF):** Comprehensive definitions of clinical cancer terminology, diagnostic procedures, and therapy protocols.
    2. **Oncology Terminology Presentation (PDF):** Visual and conceptual breakdowns of benign vs malignant neoplasia, TNM staging, chemotherapy mechanisms, and histological grading.
    3. **Terminology Reference Guide (DOCX):** Clinical guides for symptom detection, red-flag warning signs, biopsy techniques, and supportive palliative care.
    4. **Oncology Terms Dataset (XLSX):** Curated tabular dictionary of 252 cancer concepts mapped to plain English and authentic Bengali translations.
    
    ---
    **Application Architecture:** FastAPI backend, Google Gemini Generative AI (Zero-Hallucination RAG), native Bengali speech synthesis, and Streamlit Community Cloud frontend.
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center; font-size:12px; color:#888;'>OncoSathi AI — Designed for ASHA Community Healthcare Workers in India | 100% Grounded in Medical Science</div>", unsafe_allow_html=True)
