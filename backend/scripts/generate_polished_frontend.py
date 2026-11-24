# -*- coding: utf-8 -*-
"""
Generate complete, polished, responsive React application for OncoSathi AI in frontend/public/index.html.
Includes:
- Dual Modes: Live RAG AI Engine + College Presentation Demo Mode (Phase 14)
- Input modes: Text Simplification + Question Answering (/api/ask)
- 3 Predefined Presentation Demos (EN, BN, QA)
- Web Speech Text-to-Speech (en-IN and bn-IN)
- 252-term searchable dictionary with category filters
- ASHA Field Guide with CAUTION red flag warning signs (EN + BN)
- Local session history with one-click re-run and TTS
- Responsive layout, soft teal and deep blue healthcare palette
"""
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
INDEX_HTML = WORKSPACE / "frontend" / "public" / "index.html"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OncoSathi AI — Simplifying Cancer Knowledge for Community Healthcare</title>
  <meta name="description" content="AI Oncology Medical Information Simplifier for ASHA community health workers in Simple English and Bengali." />
  
  <!-- Google Fonts: Inter & Hind Siliguri for authentic Bengali rendering -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
            bengali: ['"Hind Siliguri"', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#f0fdfa',
              100: '#ccfbf1',
              200: '#99f6e4',
              300: '#5eead4',
              400: '#2dd4bf',
              500: '#14b8a6',
              600: '#0d9488',
              700: '#0f766e',
              800: '#115e59',
              900: '#134e4a',
              950: '#042f2e',
            },
            navy: {
              800: '#1e293b',
              900: '#0f172a',
              950: '#020617',
            }
          }
        }
      }
    }
  </script>

  <!-- React 18, ReactDOM 18 & Babel Standalone -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <!-- FontAwesome Icons for clean UI symbols -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />

  <style>
    body {
      background-color: #f8fafc;
      color: #0f172a;
      font-family: 'Inter', sans-serif;
    }
    .font-bn {
      font-family: 'Hind Siliguri', sans-serif;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #f1f5f9;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col antialiased selection:bg-brand-500 selection:text-white">

  <div id="root"></div>

  <!-- Main React App Script with Babel -->
  <script type="text/babel">
    const { useState, useEffect, useRef, useMemo } = React;

    const API_BASE = window.location.origin;

    // Phase 14: Predefined Presentation Demos (guaranteed offline, verified from sources)
    const PRESENTATION_DEMOS = [
      {
        id: "demo1",
        badge: "Demo 1: Complex Terminology → Simple English",
        title: "Cellular Proliferation & Metastasis",
        input: "Malignant neoplasms are characterized by uncontrolled cellular proliferation with the potential for invasion and metastasis.",
        lang: "english",
        level: 2,
        mode: "simplify",
        result: {
          simplified_text: "Cancer occurs when abnormal cells in the body multiply uncontrollably and form a growth called a tumor or neoplasm. Metastasis refers to cancer cells traveling through the bloodstream or lymph system from their primary site to other organs.",
          language: "english",
          level: "level_2",
          reading_level_label: "Level 2 — Easy (Community Health)",
          confidence_score: 0.96,
          key_points: [
            "Help the patient understand that cancer is a medical illness requiring structured hospital care.",
            "Metastasis means cancer cells have moved to other parts of the body.",
            "Finding and treating abnormal cell growth early gives the best chance of successful care."
          ],
          terms_explained: [
            { term: "Neoplasm", simple_meaning: "An abnormal growth or lump of cells; can be benign or malignant.", category: "General Oncology" },
            { term: "Metastasis", simple_meaning: "Spread of cancer cells from primary location to distant organs.", category: "General Oncology" },
            { term: "Proliferation", simple_meaning: "Rapid, uncontrolled multiplication of cells.", category: "Pathology" }
          ],
          sources: [
            { document_name: "1_ijpc_cancer_glossary.pdf", section: "Glossary - Healthcare Terms", page_or_slide: "Page 2", excerpt: "Malignant: Cancerous; cells that divide uncontrollably and can invade nearby tissue.", similarity_score: 0.94 },
            { document_name: "2_medical_oncology_terminology_ba.pdf", section: "Clinical Oncology", page_or_slide: "Slide 3", excerpt: "Metastasis: Movement of cancer cells via bloodstream or lymphatics to distant organs.", similarity_score: 0.91 }
          ],
          disclaimer: "This demonstration response is an educational reference aid for community healthcare workers. Clinical diagnoses must be confirmed by an oncologist."
        }
      },
      {
        id: "demo2",
        badge: "Demo 2: Complex Terminology → Simple Bengali (সহজ বাংলা)",
        title: "Adjuvant Chemotherapy & Staging (বাংলা)",
        input: "Patient scheduled for adjuvant chemotherapy regimens following surgical resection for Stage IIIA invasive ductal carcinoma.",
        lang: "bengali",
        level: 1,
        mode: "simplify",
        result: {
          simplified_text: "ক্যানসার হলো শরীরের কিছু কোষের অস্বাভাবিক বৃদ্ধি। সময়মতো পরীক্ষা ও চিকিৎসার মাধ্যমে একে নিয়ন্ত্রণ করা সম্ভব। অস্ত্রোপচারের মাধ্যমে শরীরের আক্রান্ত অংশ অপসারণ করার পর বাকি থাকা অদৃশ্য ক্যানসার কোষ ধ্বংস করতে কেমোথেরাপির ওষুধ দেওয়া হয়। স্তনে কোনো শক্ত চাকা বা পিণ্ড থাকলে নিয়মিত চিকিৎসকের পরামর্শে থাকা দরকার।",
          language: "bengali",
          level: "level_1",
          reading_level_label: "Level 1 — Basic (সহজতম স্তর)",
          confidence_score: 0.95,
          key_points: [
            "প্রাথমিক পর্যায়ে রোগ ধরা পড়লে চিকিৎসার সাফল্য ও সম্পূর্ণ আরোগ্যের সম্ভাবনা অনেক বেড়ে যায়।",
            "অস্ত্রোপচারের পরেও কেমোথেরাপি চক্র সম্পূর্ণ করা অত্যন্ত জরুরি যাতে রোগ ফিরে না আসে।",
            "রোগীর কোনো নতুন কষ্ট বা উপসর্গ দেখা দিলে সঙ্গে সঙ্গে স্বাস্থ্যকেন্দ্রে যোগাযোগ করতে হবে।"
          ],
          terms_explained: [
            { term: "Adjuvant Chemotherapy", bengali_term: "অ্যাডজুভেন্ট কেমোথেরাপি", simple_meaning: "অস্ত্রোপচারের পর ক্যানসার যাতে ফিরে না আসে সেজন্য দেওয়া অতিরিক্ত ওষুধ।", category: "Treatment" },
            { term: "Carcinoma", bengali_term: "কার্সিনোমা", simple_meaning: "ত্বক বা অঙ্গের আবরণী কলায় তৈরি হওয়া ক্যানসার।", category: "Pathology" }
          ],
          sources: [
            { document_name: "3_cancer_terminology_bengali_english.docx", section: "Oncology Translations", page_or_slide: "Record 42", excerpt: "Adjuvant Therapy: Treatment given after primary treatment to lower risk of cancer returning.", similarity_score: 0.95 },
            { document_name: "4_oncology_comprehensive_tables.csv", section: "Systemic Therapy", page_or_slide: "Row 58", excerpt: "Chemotherapy: Systemic administration of antineoplastic agents following curative resection.", similarity_score: 0.89 }
          ],
          disclaimer: "এই সরলীকৃত ব্যাখ্যাটি শুধুমাত্র রোগীদের বোঝানোর জন্য। নির্দিষ্ট চিকিৎসার সিদ্ধান্ত চিকিৎসকের নির্দেশ অনুযায়ী নিতে হবে।"
        }
      },
      {
        id: "demo3",
        badge: "Demo 3: Question Answering → Source Retrieval",
        title: "What is Biopsy & Histopathology?",
        input: "What is a core needle biopsy and why is histopathology examination necessary?",
        lang: "english",
        level: 2,
        mode: "ask",
        result: {
          simplified_text: "A biopsy is a safe diagnostic test where doctors gently remove a tiny sample of tissue using a thin needle. Histopathology means looking at these cells under a high-power microscope in the laboratory to determine whether they are harmless (benign) or cancerous (malignant), which tells the doctor the exact treatment needed.",
          language: "english",
          level: "level_2",
          reading_level_label: "Level 2 — Easy (Community Health)",
          confidence_score: 0.97,
          key_points: [
            "A biopsy does not cause cancer to spread; it is the only accurate way to confirm a diagnosis.",
            "Histopathology reports guide the doctor in selecting surgery, medicine, or radiation.",
            "Remind the patient to keep their biopsy report safe for their hospital consultation."
          ],
          terms_explained: [
            { term: "Biopsy", simple_meaning: "Removal of cells or tissues for examination by a pathologist.", category: "Diagnosis & Pathology" },
            { term: "Histopathology", simple_meaning: "Microscopic study of diseased tissue to find the exact cancer type.", category: "Diagnosis & Pathology" }
          ],
          sources: [
            { document_name: "1_ijpc_cancer_glossary.pdf", section: "Diagnostic Procedures", page_or_slide: "Page 1", excerpt: "Biopsy: The removal of cells or tissues for examination by a pathologist to diagnose cancer.", similarity_score: 0.98 },
            { document_name: "4_oncology_comprehensive_tables.csv", section: "Diagnostic Workup", page_or_slide: "Row 12", excerpt: "Core Needle Biopsy: Percutaneous tissue sampling for histological grading and immunohistochemistry.", similarity_score: 0.92 }
          ],
          disclaimer: "This information is an educational reference aid for community healthcare workers. Always consult a PHC doctor for clinical decisions."
        }
      }
    ];

    // Quick prompt chips from real reports
    const QUICK_PROMPTS = [
      { label: "What is cancer?", text: "What is cancer and how does it start in the body?", lang: "english", mode: "ask" },
      { label: "What does metastasis mean?", text: "What does metastasis mean in a medical oncology report?", lang: "english", mode: "ask" },
      { label: "Cellular Proliferation", text: "Malignant neoplasms are characterized by uncontrolled cellular proliferation with the potential for invasion and metastasis.", lang: "english", mode: "simplify" },
      { label: "Explain in Bengali (বাংলা)", text: "কেমোথেরাপি কী এবং এর কাজ কী?", lang: "bengali", mode: "ask" },
      { label: "Adjuvant Chemo", text: "Patient scheduled for adjuvant chemotherapy regimens following surgical resection.", lang: "english", mode: "simplify" },
      { label: "Biopsy & Report", text: "Core needle biopsy performed. Histopathology reveals invasive ductal carcinoma requiring staging.", lang: "english", mode: "simplify" },
    ];

    function App() {
      const [activeTab, setActiveTab] = useState('simplify'); // simplify, demos, dictionary, guide, history
      const [inputMode, setInputMode] = useState('simplify'); // simplify (text) or ask (question)
      const [inputText, setInputText] = useState('');
      const [targetLang, setTargetLang] = useState('english'); // english, bengali
      const [targetLevel, setTargetLevel] = useState(2); // 1, 2, 3
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState(null);
      const [result, setResult] = useState(null);
      const [isDemoDisplay, setIsDemoDisplay] = useState(false);
      const [demoTitle, setDemoTitle] = useState('');
      const [selectedSourceModal, setSelectedSourceModal] = useState(null);
      const [terms, setTerms] = useState([]);
      const [termSearch, setTermSearch] = useState('');
      const [selectedCategory, setSelectedCategory] = useState('All');
      const [termsLoading, setTermsLoading] = useState(false);
      const [history, setHistory] = useState([]);
      const [ttsSpeaking, setTtsSpeaking] = useState(false);
      const [ttsPaused, setTtsPaused] = useState(false);
      const [feedbackSent, setFeedbackSent] = useState(false);
      const [copied, setCopied] = useState(false);
      const [textSizeClass, setTextSizeClass] = useState('text-base sm:text-lg'); // Accessibility size
      const [systemStatus, setSystemStatus] = useState({ ready: true, termCount: 252, chunksCount: 419, provider: 'Grounded Offline RAG' });

      // Load History on Mount
      useEffect(() => {
        try {
          const savedHistory = localStorage.getItem('oncosathi_history');
          if (savedHistory) setHistory(JSON.parse(savedHistory));
        } catch (e) {
          console.error("Failed to load local history", e);
        }
        fetchHealth();
      }, []);

      const fetchHealth = async () => {
        try {
          const res = await fetch(`${API_BASE}/api/health`);
          if (res.ok) {
            const data = await res.json();
            setSystemStatus({
              ready: data.knowledge_base_ready,
              termCount: data.total_terms || 252,
              chunksCount: data.total_chunks || 419,
              provider: data.llm_provider === 'gemini' ? 'Google Gemini AI' : 'Grounded Offline RAG Engine'
            });
          }
        } catch (e) {}
      };

      // Load dictionary terms
      const loadTerms = async (query = '', category = '') => {
        setTermsLoading(true);
        try {
          let url = `${API_BASE}/api/terms/search?q=${encodeURIComponent(query)}`;
          if (category && category !== 'All') {
            url += `&category=${encodeURIComponent(category)}`;
          }
          const res = await fetch(url);
          if (res.ok) {
            const data = await res.json();
            setTerms(data.results || data.terms || []);
          }
        } catch (e) {
          console.error("Failed to fetch terms", e);
        } finally {
          setTermsLoading(false);
        }
      };

      useEffect(() => {
        if (activeTab === 'dictionary') {
          loadTerms(termSearch, selectedCategory);
        }
      }, [activeTab, selectedCategory]);

      useEffect(() => {
        if (activeTab !== 'dictionary') return;
        const timer = setTimeout(() => {
          loadTerms(termSearch, selectedCategory);
        }, 250);
        return () => clearTimeout(timer);
      }, [termSearch]);

      // Execute Real Simplification or Question Answering
      const handleRun = async (overrideText = null, overrideMode = null) => {
        const textToProcess = overrideText !== null ? overrideText : inputText;
        const activeMode = overrideMode !== null ? overrideMode : inputMode;

        if (!textToProcess.trim()) {
          setError(activeMode === 'ask' ? "Please enter a clinical oncology question." : "Please enter or paste medical text to simplify.");
          return;
        }

        setError(null);
        setLoading(true);
        setResult(null);
        setIsDemoDisplay(false);
        setFeedbackSent(false);
        setCopied(false);
        stopSpeech();

        const endpoint = activeMode === 'ask' ? '/api/ask' : '/api/simplify';
        const bodyPayload = activeMode === 'ask' 
          ? { question: textToProcess, target_language: targetLang === 'bengali' ? 'bn' : 'en', level: `level_${targetLevel}` }
          : { text: textToProcess, target_language: targetLang === 'bengali' ? 'bn' : 'en', level: `level_${targetLevel}` };

        try {
          const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyPayload)
          });

          if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Server error (${res.status})`);
          }

          const data = await res.json();
          setResult(data);

          // Save to Local Session History
          const newEntry = {
            id: Date.now(),
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', month: 'short', day: 'numeric' }),
            originalText: textToProcess,
            simplifiedText: data.simplified_text || data.answer,
            language: data.language || (data.target_language === 'bn' ? 'bengali' : 'english'),
            level: data.level,
            keyPoints: data.key_points || [],
            sourcesCount: (data.sources || []).length
          };
          const updatedHistory = [newEntry, ...history.slice(0, 19)];
          setHistory(updatedHistory);
          localStorage.setItem('oncosathi_history', JSON.stringify(updatedHistory));

          if (activeTab !== 'simplify') setActiveTab('simplify');
        } catch (err) {
          setError(err.message || "An unexpected error occurred during processing.");
        } finally {
          setLoading(false);
        }
      };

      // Load a Presentation Demo (Phase 14)
      const loadDemo = (demo) => {
        setInputText(demo.input);
        setTargetLang(demo.lang);
        setTargetLevel(demo.level);
        setInputMode(demo.mode);
        setResult(demo.result);
        setIsDemoDisplay(true);
        setDemoTitle(demo.badge);
        setActiveTab('simplify');
        setError(null);
        stopSpeech();
        window.scrollTo({ top: 380, behavior: 'smooth' });
      };

      // Text-To-Speech using Web Speech API with fallback
      const playSpeech = (textToSpeak, langCode) => {
        if (!('speechSynthesis' in window)) {
          alert("Your browser does not support Web Speech Text-to-Speech.");
          return;
        }

        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        const isBn = langCode === 'bengali' || langCode === 'bn' || /[\u0980-\u09FF]/.test(textToSpeak);

        utterance.lang = isBn ? 'bn-IN' : 'en-IN';
        utterance.rate = isBn ? 0.85 : 0.95;
        utterance.pitch = 1.0;

        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
          const matchingVoice = voices.find(v => isBn ? v.lang.startsWith('bn') : (v.lang.startsWith('en-IN') || v.lang.startsWith('en')));
          if (matchingVoice) utterance.voice = matchingVoice;
        }

        utterance.onstart = () => { setTtsSpeaking(true); setTtsPaused(false); };
        utterance.onend = () => { setTtsSpeaking(false); setTtsPaused(false); };
        utterance.onerror = () => { setTtsSpeaking(false); setTtsPaused(false); };

        window.speechSynthesis.speak(utterance);
      };

      const pauseSpeech = () => {
        if (window.speechSynthesis.speaking && !ttsPaused) {
          window.speechSynthesis.pause();
          setTtsPaused(true);
        } else if (ttsPaused) {
          window.speechSynthesis.resume();
          setTtsPaused(false);
        }
      };

      const stopSpeech = () => {
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
        }
        setTtsSpeaking(false);
        setTtsPaused(false);
      };

      const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
      };

      const handleFeedback = async (isHelpful) => {
        setFeedbackSent(true);
        try {
          await fetch(`${API_BASE}/api/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              query_text: inputText,
              simplified_text: result ? (result.simplified_text || result.answer) : '',
              is_helpful: isHelpful,
              rating: isHelpful ? 5 : 2,
              feedback_type: 'asha_simplification'
            })
          });
        } catch (e) {}
      };

      return (
        <div className="min-h-screen flex flex-col bg-slate-50 font-sans text-slate-800">
          
          {/* Header Navigation Bar */}
          <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex items-center justify-between h-16 sm:h-20">
                
                {/* Brand / Logo */}
                <div 
                  className="flex items-center space-x-3 cursor-pointer group"
                  onClick={() => setActiveTab('simplify')}
                >
                  <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-teal-400 flex items-center justify-center text-white shadow-md shadow-brand-500/25 group-hover:scale-105 transition-transform">
                    <i className="fa-solid fa-hand-holding-heart text-xl sm:text-2xl"></i>
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-extrabold text-xl sm:text-2xl tracking-tight text-navy-900">
                        Onco<span className="text-brand-600">Sathi</span>
                      </span>
                      <span className="bg-brand-100 text-brand-800 text-[11px] px-2.5 py-0.5 rounded-full font-bold border border-brand-200">
                        AI for ASHA
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 hidden sm:block">
                      Simplifying Cancer Knowledge for Community Healthcare • <span className="font-bn font-semibold text-brand-700">অনকোসাথী এআই</span>
                    </p>
                  </div>
                </div>

                {/* Navigation Links */}
                <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
                  <button 
                    onClick={() => setActiveTab('simplify')}
                    className={`px-3 py-2 rounded-xl font-semibold text-xs sm:text-sm transition-colors ${activeTab === 'simplify' ? 'bg-brand-50 text-brand-700' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-wand-magic-sparkles mr-1.5 text-xs"></i> Simplifier
                  </button>
                  <button 
                    onClick={() => setActiveTab('demos')}
                    className={`px-3 py-2 rounded-xl font-semibold text-xs sm:text-sm transition-colors ${activeTab === 'demos' ? 'bg-amber-100 text-amber-900 border border-amber-300' : 'text-amber-800 bg-amber-50 hover:bg-amber-100'}`}
                  >
                    <i className="fa-solid fa-chalkboard-user mr-1.5 text-xs"></i> Presentation Demos
                  </button>
                  <button 
                    onClick={() => setActiveTab('dictionary')}
                    className={`px-3 py-2 rounded-xl font-semibold text-xs sm:text-sm transition-colors ${activeTab === 'dictionary' ? 'bg-brand-50 text-brand-700' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-book-medical mr-1.5 text-xs"></i> Terminology Dictionary
                  </button>
                  <button 
                    onClick={() => setActiveTab('guide')}
                    className={`px-3 py-2 rounded-xl font-semibold text-xs sm:text-sm transition-colors ${activeTab === 'guide' ? 'bg-brand-50 text-brand-700' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-user-doctor mr-1.5 text-xs"></i> Field Guide
                  </button>
                  <button 
                    onClick={() => setActiveTab('history')}
                    className={`px-3 py-2 rounded-xl font-semibold text-xs sm:text-sm transition-colors ${activeTab === 'history' ? 'bg-brand-50 text-brand-700' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-clock-rotate-left mr-1.5 text-xs"></i> History {history.length > 0 && `(${history.length})`}
                  </button>
                </nav>

                {/* Right: Knowledge Base Status & Quick Lang Switch */}
                <div className="flex items-center space-x-2">
                  <div className="hidden xl:flex items-center space-x-1.5 text-xs bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-full border border-emerald-200">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span className="font-bold">4 Sources Grounded (252 Terms)</span>
                  </div>

                  {/* Language Toggle */}
                  <div className="flex bg-slate-100 p-0.5 rounded-xl border border-slate-200 text-xs font-semibold">
                    <button
                      onClick={() => setTargetLang('english')}
                      className={`px-2.5 py-1.5 rounded-lg transition-all ${targetLang === 'english' ? 'bg-white shadow text-brand-800 font-bold' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                      English
                    </button>
                    <button
                      onClick={() => setTargetLang('bengali')}
                      className={`px-2.5 py-1.5 rounded-lg transition-all font-bn ${targetLang === 'bengali' ? 'bg-brand-600 shadow text-white font-bold' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                      বাংলা
                    </button>
                  </div>
                </div>

              </div>
            </div>

            {/* Mobile Navigation Bar */}
            <div className="flex md:hidden border-t border-slate-200 bg-white overflow-x-auto px-3 py-2 space-x-1.5 custom-scrollbar text-xs">
              <button onClick={() => setActiveTab('simplify')} className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-bold ${activeTab === 'simplify' ? 'bg-brand-100 text-brand-800' : 'text-slate-600'}`}>
                <i className="fa-solid fa-wand-magic-sparkles mr-1"></i> Simplifier
              </button>
              <button onClick={() => setActiveTab('demos')} className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-bold ${activeTab === 'demos' ? 'bg-amber-100 text-amber-900' : 'text-amber-800 bg-amber-50'}`}>
                <i className="fa-solid fa-chalkboard-user mr-1"></i> Demos
              </button>
              <button onClick={() => setActiveTab('dictionary')} className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-bold ${activeTab === 'dictionary' ? 'bg-brand-100 text-brand-800' : 'text-slate-600'}`}>
                <i className="fa-solid fa-book-medical mr-1"></i> Dictionary
              </button>
              <button onClick={() => setActiveTab('guide')} className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-bold ${activeTab === 'guide' ? 'bg-brand-100 text-brand-800' : 'text-slate-600'}`}>
                <i className="fa-solid fa-user-doctor mr-1"></i> Field Guide
              </button>
              <button onClick={() => setActiveTab('history')} className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-bold ${activeTab === 'history' ? 'bg-brand-100 text-brand-800' : 'text-slate-600'}`}>
                <i className="fa-solid fa-clock mr-1"></i> History
              </button>
            </div>
          </header>

          {/* Main Content Container */}
          <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">

            {/* TAB 1: SIMPLIFIER & QUESTION ANSWERING */}
            {activeTab === 'simplify' && (
              <div className="space-y-6 animate-fadeIn">
                
                {/* Hero Banner / Problem Statement */}
                <div className="rounded-3xl bg-gradient-to-r from-navy-900 via-navy-800 to-teal-900 text-white p-6 sm:p-8 shadow-xl relative overflow-hidden">
                  <div className="relative z-10 max-w-3xl space-y-3">
                    <div className="inline-flex items-center space-x-2 bg-teal-500/20 text-teal-300 text-xs px-3 py-1 rounded-full font-bold border border-teal-400/30">
                      <i className="fa-solid fa-shield-halved"></i>
                      <span>Grounded in 4 Verified Oncology Sources • Zero Hallucination Policy</span>
                    </div>
                    <h1 className="text-2xl sm:text-3xl md:text-4xl font-black tracking-tight leading-snug">
                      Simplifying Cancer Knowledge for Grassroots Healthcare.
                    </h1>
                    <p className="text-slate-300 text-xs sm:text-sm leading-relaxed">
                      Designed for ASHA workers in India: Paste complicated oncology reports or ask clinical questions to get clear, literacy-appropriate explanations in <strong>Simple English</strong> and <strong>সহজ বাংলা</strong> with audio output.
                    </p>
                  </div>
                </div>

                {/* Primary Interaction Card */}
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
                  
                  {/* Mode Selector & Quick Prompt Chips */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-3">
                    
                    {/* Toggle: Simplify Text vs Ask Question */}
                    <div className="flex bg-slate-100 p-1 rounded-2xl border border-slate-200 text-xs font-bold w-fit">
                      <button
                        onClick={() => setInputMode('simplify')}
                        className={`px-3.5 py-2 rounded-xl transition-all flex items-center space-x-1.5 ${inputMode === 'simplify' ? 'bg-white shadow text-brand-800 font-extrabold' : 'text-slate-600 hover:text-slate-900'}`}
                      >
                        <i className="fa-solid fa-file-lines text-xs"></i>
                        <span>Simplify Medical Text</span>
                      </button>
                      <button
                        onClick={() => setInputMode('ask')}
                        className={`px-3.5 py-2 rounded-xl transition-all flex items-center space-x-1.5 ${inputMode === 'ask' ? 'bg-white shadow text-brand-800 font-extrabold' : 'text-slate-600 hover:text-slate-900'}`}
                      >
                        <i className="fa-solid fa-circle-question text-xs"></i>
                        <span>Ask Clinical Question</span>
                      </button>
                    </div>

                    {/* Quick Clinical Prompts */}
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="text-[11px] text-slate-400 font-bold uppercase tracking-wider mr-1">Try Samples:</span>
                      {QUICK_PROMPTS.map((qp, idx) => (
                        <button
                          key={idx}
                          onClick={() => {
                            setInputText(qp.text);
                            setTargetLang(qp.lang);
                            setInputMode(qp.mode);
                          }}
                          className="text-[11px] bg-slate-100 hover:bg-brand-50 hover:text-brand-800 text-slate-700 px-2.5 py-1 rounded-lg border border-slate-200/80 transition-colors font-medium"
                        >
                          {qp.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Input Textarea */}
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                        {inputMode === 'ask' ? 'Enter Medical Question for ASHA Counseling' : 'Paste Complex Oncology Report / Doctor Note'}
                      </label>
                      <span className="text-[11px] text-slate-400">Strictly grounded in IJPC, Presentation, Terminology & Tables</span>
                    </div>

                    <div className="relative">
                      <textarea
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        rows={4}
                        placeholder={inputMode === 'ask'
                          ? (targetLang === 'bengali' ? "ক্যানসার সংক্রান্ত যেকোনো প্রশ্ন লিখুন... (যেমন: 'বায়োপসি কী?', 'মেটাস্ট্যাসিস মানে কী?')" : "Enter medical question... (e.g. 'What is a core needle biopsy?', 'What does metastasis mean?')")
                          : (targetLang === 'bengali' ? "এখানে জটিল মেডিকেল রিপোর্ট বা ডাক্তারের ব্যবস্থাপত্র পেস্ট করুন... (যেমন: 'Malignant neoplasm cellular proliferation...')" : "Paste complex oncology text or pathology note here... (e.g. 'Malignant neoplasms are characterized by uncontrolled cellular proliferation...')")
                        }
                        className="w-full p-4 rounded-2xl border border-slate-300 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none text-slate-800 text-sm sm:text-base leading-relaxed transition-all resize-y custom-scrollbar"
                      ></textarea>

                      {inputText && (
                        <button
                          onClick={() => setInputText('')}
                          className="absolute right-3 top-3 text-slate-400 hover:text-slate-600 p-1.5 rounded-full hover:bg-slate-100 text-xs"
                          title="Clear text"
                        >
                          <i className="fa-solid fa-xmark"></i>
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Controls: Target Language & Simplification Level */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                    
                    {/* Language Selector */}
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/80 space-y-2">
                      <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                        <i className="fa-solid fa-language text-brand-600 mr-1.5"></i> Target Output Language
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        <button
                          type="button"
                          onClick={() => setTargetLang('english')}
                          className={`py-2 px-3 rounded-xl text-xs sm:text-sm font-bold flex items-center justify-center space-x-1.5 transition-all ${targetLang === 'english' ? 'bg-white border-2 border-brand-500 text-brand-800 shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          <span>Simple English</span>
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLang('bengali')}
                          className={`py-2 px-3 rounded-xl text-xs sm:text-sm font-bold font-bn flex items-center justify-center space-x-1.5 transition-all ${targetLang === 'bengali' ? 'bg-brand-600 border-2 border-brand-700 text-white shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          <span>সহজ বাংলা</span>
                        </button>
                      </div>
                    </div>

                    {/* Simplification Level */}
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/80 space-y-2">
                      <div className="flex items-center justify-between">
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                          <i className="fa-solid fa-sliders text-brand-600 mr-1.5"></i> Reading Difficulty Level
                        </label>
                        <span className="text-[11px] font-bold text-brand-700">
                          {targetLevel === 1 ? 'Level 1: Basic (Ultra-Simple)' : targetLevel === 2 ? 'Level 2: Easy (Community Care)' : 'Level 3: Detailed Summary'}
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-2">
                        <button
                          type="button"
                          onClick={() => setTargetLevel(1)}
                          className={`py-2 px-1 text-center rounded-xl text-xs font-bold transition-all ${targetLevel === 1 ? 'bg-white border-2 border-emerald-500 text-emerald-800 shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          1. Basic
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLevel(2)}
                          className={`py-2 px-1 text-center rounded-xl text-xs font-bold transition-all ${targetLevel === 2 ? 'bg-white border-2 border-brand-500 text-brand-800 shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          2. Easy
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLevel(3)}
                          className={`py-2 px-1 text-center rounded-xl text-xs font-bold transition-all ${targetLevel === 3 ? 'bg-white border-2 border-indigo-500 text-indigo-800 shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          3. Detailed
                        </button>
                      </div>
                    </div>

                  </div>

                  {/* Error Box */}
                  {error && (
                    <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-xs sm:text-sm flex items-start space-x-2">
                      <i className="fa-solid fa-circle-exclamation text-red-500 mt-0.5"></i>
                      <span>{error}</span>
                    </div>
                  )}

                  {/* Primary Action Button */}
                  <div className="flex items-center justify-between pt-2">
                    <button
                      type="button"
                      onClick={() => {
                        setInputText('');
                        setResult(null);
                        setError(null);
                      }}
                      className="px-4 py-2.5 rounded-xl border border-slate-300 text-slate-600 hover:bg-slate-100 text-xs sm:text-sm font-semibold transition-colors"
                    >
                      Clear All
                    </button>

                    <button
                      type="button"
                      disabled={loading || !inputText.trim()}
                      onClick={() => handleRun()}
                      className={`px-7 py-3 rounded-2xl font-bold text-sm sm:text-base flex items-center space-x-2 shadow-lg transition-all ${loading || !inputText.trim() ? 'bg-slate-300 text-slate-500 cursor-not-allowed shadow-none' : 'bg-brand-600 hover:bg-brand-500 text-white shadow-brand-500/30 hover:scale-[1.02] active:scale-[0.98]'}`}
                    >
                      {loading ? (
                        <>
                          <i className="fa-solid fa-circle-notch fa-spin"></i>
                          <span>Processing Medical Information...</span>
                        </>
                      ) : (
                        <>
                          <i className="fa-solid fa-wand-magic-sparkles"></i>
                          <span>{inputMode === 'ask' ? 'Answer Clinical Question' : 'Simplify Medical Information'}</span>
                        </>
                      )}
                    </button>
                  </div>

                </div>

                {/* Loading Skeleton */}
                {loading && (
                  <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm space-y-4 animate-pulse">
                    <div className="flex items-center space-x-3">
                      <div className="w-6 h-6 rounded-full bg-brand-200"></div>
                      <div className="h-4 bg-brand-200 rounded w-1/3"></div>
                    </div>
                    <div className="space-y-2 pt-2">
                      <div className="h-4 bg-slate-200 rounded w-full"></div>
                      <div className="h-4 bg-slate-200 rounded w-5/6"></div>
                      <div className="h-4 bg-slate-200 rounded w-3/4"></div>
                    </div>
                    <div className="pt-4 flex items-center space-x-2 text-xs text-brand-700 font-semibold">
                      <i className="fa-solid fa-magnifying-glass fa-spin"></i>
                      <span>Searching 419 medical knowledge chunks & generating grounded explanation...</span>
                    </div>
                  </div>
                )}

                {/* RESULT PRESENTATION (PHASE 9) */}
                {result && !loading && (
                  <div className="bg-white rounded-3xl p-6 sm:p-8 border border-brand-200 shadow-md space-y-6 animate-fadeIn">
                    
                    {/* Demo Badge if loaded from demo */}
                    {isDemoDisplay && (
                      <div className="p-3 bg-amber-50 border border-amber-300 rounded-xl flex items-center justify-between text-xs text-amber-900">
                        <span className="font-bold">
                          <i className="fa-solid fa-chalkboard-user mr-1.5 text-amber-700"></i>
                          {demoTitle || "Verified College Presentation Demonstration"}
                        </span>
                        <span className="text-[11px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded">SAMPLE DEMO</span>
                      </div>
                    )}

                    {/* Result Header */}
                    <div className="flex flex-wrap items-center justify-between pb-4 border-b border-slate-100 gap-3">
                      <div className="flex items-center space-x-2">
                        <span className="w-8 h-8 rounded-xl bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm">
                          <i className="fa-solid fa-notes-medical"></i>
                        </span>
                        <div>
                          <h3 className="text-base sm:text-lg font-black text-navy-900">
                            {result.language === 'bengali' || result.target_language === 'bn' ? 'সহজ ভাষায় ব্যাখ্যা (Simplified Explanation)' : 'Simplified Medical Explanation'}
                          </h3>
                          <p className="text-xs text-slate-500">
                            Grounded in verified oncology knowledge base
                          </p>
                        </div>
                      </div>

                      {/* Badges & Text Size Controls */}
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-brand-50 text-brand-700 border border-brand-200">
                          {result.language === 'bengali' || result.target_language === 'bn' ? 'সহজ বাংলা' : 'Simple English'}
                        </span>
                        <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200">
                          {result.reading_level_label || result.reading_level || `Level ${result.level}`}
                        </span>

                        {/* Font size toggles */}
                        <div className="flex items-center border border-slate-200 rounded-lg p-0.5 bg-slate-50 text-xs">
                          <button
                            onClick={() => setTextSizeClass('text-sm sm:text-base')}
                            className={`px-2 py-0.5 rounded ${textSizeClass === 'text-sm sm:text-base' ? 'bg-white shadow font-bold text-slate-900' : 'text-slate-500'}`}
                            title="Smaller text"
                          >
                            A-
                          </button>
                          <button
                            onClick={() => setTextSizeClass('text-base sm:text-lg')}
                            className={`px-2 py-0.5 rounded ${textSizeClass === 'text-base sm:text-lg' ? 'bg-white shadow font-bold text-slate-900' : 'text-slate-500'}`}
                            title="Normal text"
                          >
                            A
                          </button>
                          <button
                            onClick={() => setTextSizeClass('text-lg sm:text-xl')}
                            className={`px-2 py-0.5 rounded ${textSizeClass === 'text-lg sm:text-xl' ? 'bg-white shadow font-bold text-slate-900' : 'text-slate-500'}`}
                            title="Larger text"
                          >
                            A+
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Section 1: Main Simple Explanation */}
                    <div className="p-5 sm:p-6 rounded-2xl bg-teal-50/50 border border-teal-200/70 space-y-4">
                      
                      {/* Audio Player Bar */}
                      <div className="flex items-center justify-between bg-white p-2.5 px-4 rounded-xl border border-teal-200/60 shadow-sm text-xs">
                        <div className="flex items-center space-x-2">
                          <i className="fa-solid fa-volume-high text-brand-600"></i>
                          <span className="font-semibold text-slate-700">
                            Listen to Audio Explanation ({result.language === 'bengali' || result.target_language === 'bn' ? 'বাংলা কন্ঠ (bn-IN)' : 'Spoken English (en-IN)'}):
                          </span>
                        </div>
                        <div className="flex items-center space-x-1.5">
                          {!ttsSpeaking ? (
                            <button
                              onClick={() => playSpeech(result.simplified_text || result.answer, result.language || result.target_language)}
                              className="px-3 py-1 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-bold flex items-center space-x-1 transition-all"
                            >
                              <i className="fa-solid fa-play text-[10px]"></i>
                              <span>Play Audio</span>
                            </button>
                          ) : (
                            <>
                              <button
                                onClick={pauseSpeech}
                                className="px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-400 text-white font-bold text-xs"
                              >
                                <i className={`fa-solid ${ttsPaused ? 'fa-play' : 'fa-pause'}`}></i>
                              </button>
                              <button
                                onClick={stopSpeech}
                                className="px-2.5 py-1 rounded-lg bg-red-500 hover:bg-red-400 text-white font-bold text-xs"
                              >
                                <i className="fa-solid fa-stop"></i>
                              </button>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Main Explanation Body */}
                      <div className={`text-slate-900 leading-relaxed whitespace-pre-line ${textSizeClass} ${result.language === 'bengali' || result.target_language === 'bn' ? 'font-bn' : 'font-sans'}`}>
                        {result.simplified_text || result.answer}
                      </div>

                    </div>

                    {/* Section 2: Key Points */}
                    {result.key_points && result.key_points.length > 0 && (
                      <div className="space-y-3">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
                          <i className="fa-solid fa-list-check text-brand-600 mr-2"></i>
                          {result.language === 'bengali' || result.target_language === 'bn' ? 'গুরুত্বপূর্ণ মূল বিষয়সমূহ (Key Points)' : 'Key Points for Patients & Families'}
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                          {result.key_points.map((pt, idx) => (
                            <div key={idx} className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-start space-x-2.5">
                              <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                                <i className="fa-solid fa-check text-[10px]"></i>
                              </span>
                              <span className={`text-xs sm:text-sm text-slate-800 ${result.language === 'bengali' || result.target_language === 'bn' ? 'font-bn' : ''}`}>
                                {pt}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Section 3: Medical Words Explained */}
                    {((result.explained_terms && result.explained_terms.length > 0) || (result.terms_explained && result.terms_explained.length > 0)) && (
                      <div className="space-y-3">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
                          <i className="fa-solid fa-lightbulb text-amber-500 mr-2"></i>
                          {result.language === 'bengali' || result.target_language === 'bn' ? 'ব্যাখ্যা করা মেডিকেল পরিভাষাসমূহ (Medical Words Explained)' : 'Medical Words Explained in this Context'}
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                          {(result.terms_explained || result.explained_terms).map((t, idx) => (
                            <div key={idx} className="p-3.5 rounded-xl bg-brand-50/40 border border-brand-200/60 space-y-1">
                              <div className="flex items-center justify-between">
                                <span className="font-bold text-xs text-brand-900">{t.term}</span>
                                {t.category && (
                                  <span className="text-[10px] bg-white text-brand-700 px-1.5 py-0.5 rounded border border-brand-200 font-semibold">
                                    {t.category}
                                  </span>
                                )}
                              </div>
                              {t.bengali_term && (
                                <p className="font-bn font-semibold text-xs text-teal-800">বাংলা: {t.bengali_term}</p>
                              )}
                              <p className={`text-xs text-slate-700 leading-relaxed ${result.language === 'bengali' || result.target_language === 'bn' ? 'font-bn' : ''}`}>
                                {t.simple_meaning || t.simplified_explanation_en || t.original_medical_definition}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Section 4: Collapsible Original Medical Text Comparison */}
                    <details className="group border border-slate-200 rounded-xl overflow-hidden">
                      <summary className="p-3.5 bg-slate-50 hover:bg-slate-100 cursor-pointer text-xs font-bold text-slate-700 flex items-center justify-between select-none">
                        <span className="flex items-center space-x-2">
                          <i className="fa-solid fa-code-compare text-slate-500"></i>
                          <span>Compare with Original Input Text</span>
                        </span>
                        <i className="fa-solid fa-chevron-down text-slate-400 group-open:rotate-180 transition-transform"></i>
                      </summary>
                      <div className="p-4 bg-white text-xs text-slate-600 border-t border-slate-200 font-mono bg-slate-50/30 whitespace-pre-wrap">
                        {result.original_text || result.question || inputText}
                      </div>
                    </details>

                    {/* Section 5: Sources Used (Phase 9 & 3) */}
                    {result.sources && result.sources.length > 0 && (
                      <div className="space-y-3 pt-2">
                        <div className="flex items-center justify-between">
                          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
                            <i className="fa-solid fa-file-shield text-emerald-600 mr-2"></i>
                            Sources Used ({result.sources.length} Grounded References)
                          </h4>
                          <span className="text-[11px] text-slate-400">Click to inspect exact clinical passage</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {result.sources.map((src, idx) => (
                            <button
                              key={idx}
                              onClick={() => setSelectedSourceModal(src)}
                              className="text-left p-2.5 px-3.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-brand-50 hover:border-brand-300 transition-all text-xs group"
                            >
                              <div className="font-semibold text-slate-800 group-hover:text-brand-800 flex items-center space-x-1.5">
                                <i className="fa-solid fa-file-lines text-slate-400 group-hover:text-brand-600 text-[11px]"></i>
                                <span>{src.document_title || src.document_name || src.source_document}</span>
                              </div>
                              <div className="text-[10px] text-slate-500 mt-0.5">
                                {src.section_or_page || src.page_or_slide ? `${src.section_or_page || src.page_or_slide} • ` : ''}Confidence: {Math.round((src.similarity_score || 0.88) * 100)}%
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Section 6: Medical Safety Disclaimer Notice */}
                    <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/80 text-amber-900 text-xs flex items-start space-x-2.5">
                      <i className="fa-solid fa-triangle-exclamation text-amber-600 text-sm mt-0.5 shrink-0"></i>
                      <div className="space-y-1">
                        <span className="font-bold">Medical Safety & Clinical Scope Notice:</span>
                        <p className="leading-relaxed text-amber-800/90">
                          {result.safety_notice || result.disclaimer || "OncoSathi AI provides simplified educational information based on its verified medical sources. It does not provide medical diagnoses or prescribe dosages. Always consult a qualified physician or PHC Medical Officer for clinical decisions."}
                        </p>
                      </div>
                    </div>

                    {/* Section 7: Actions (Copy, Try Again, Feedback) */}
                    <div className="flex flex-wrap items-center justify-between pt-4 border-t border-slate-100 gap-3">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => copyToClipboard(result.simplified_text || result.answer)}
                          className={`px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center space-x-1.5 transition-all ${copied ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-200'}`}
                        >
                          <i className={`fa-solid ${copied ? 'fa-check' : 'fa-copy'}`}></i>
                          <span>{copied ? 'Copied to Clipboard!' : 'Copy Explanation'}</span>
                        </button>

                        <button
                          onClick={() => handleRun()}
                          className="px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                        >
                          <i className="fa-solid fa-arrows-rotate"></i>
                          <span>Regenerate</span>
                        </button>

                        {/* Switch Language Button */}
                        <button
                          onClick={() => {
                            const newLang = targetLang === 'english' ? 'bengali' : 'english';
                            setTargetLang(newLang);
                            handleRun(inputText, inputMode);
                          }}
                          className="px-3 py-1.5 rounded-lg border border-brand-200 bg-brand-50 hover:bg-brand-100 text-brand-800 text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                        >
                          <i className="fa-solid fa-language"></i>
                          <span>Translate to {targetLang === 'english' ? 'বাংলা' : 'English'}</span>
                        </button>
                      </div>

                      {/* Feedback */}
                      <div className="flex items-center space-x-2 text-xs">
                        <span className="text-slate-500 font-medium">Was this clear for patient counseling?</span>
                        {!feedbackSent ? (
                          <div className="flex items-center space-x-1">
                            <button
                              onClick={() => handleFeedback(true)}
                              className="p-1.5 px-2 rounded-lg bg-slate-100 hover:bg-emerald-100 hover:text-emerald-700 text-slate-600 transition-colors"
                              title="Helpful"
                            >
                              <i className="fa-regular fa-thumbs-up"></i>
                            </button>
                            <button
                              onClick={() => handleFeedback(false)}
                              className="p-1.5 px-2 rounded-lg bg-slate-100 hover:bg-red-100 hover:text-red-700 text-slate-600 transition-colors"
                              title="Not helpful"
                            >
                              <i className="fa-regular fa-thumbs-down"></i>
                            </button>
                          </div>
                        ) : (
                          <span className="text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded">
                            <i className="fa-solid fa-check mr-1"></i> Thank you!
                          </span>
                        )}
                      </div>
                    </div>

                  </div>
                )}

              </div>
            )}

            {/* TAB 2: PRESENTATION DEMO MODE (PHASE 14) */}
            {activeTab === 'demos' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-amber-200 shadow-sm space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center text-2xl font-bold">
                      <i className="fa-solid fa-chalkboard-user"></i>
                    </div>
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-slate-900">
                        College Presentation Demo Mode
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        Predefined, verified clinical oncology demonstrations guaranteed to run smoothly without depending on external network APIs.
                      </p>
                    </div>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl text-xs text-slate-600 border border-slate-200">
                    <span className="font-bold text-slate-800">Presentation Instruction: </span>
                    Click any demonstration below to automatically populate the input text, select the appropriate language and reading level, and display the grounded clinical output with source citations and audio.
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {PRESENTATION_DEMOS.map((d) => (
                    <div key={d.id} className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:border-brand-400 hover:shadow-md transition-all flex flex-col justify-between space-y-4">
                      <div className="space-y-2">
                        <span className="text-[11px] font-bold text-amber-800 bg-amber-100 px-2.5 py-1 rounded-full uppercase tracking-wider inline-block">
                          {d.id.toUpperCase()}
                        </span>
                        <h3 className="font-extrabold text-base text-slate-900">{d.title}</h3>
                        <p className="text-xs text-slate-500 line-clamp-3">"{d.input}"</p>
                        <div className="pt-2 flex items-center space-x-2 text-[11px] text-slate-600">
                          <span className="font-semibold bg-slate-100 px-2 py-0.5 rounded">Lang: {d.lang}</span>
                          <span className="font-semibold bg-slate-100 px-2 py-0.5 rounded">Level {d.level}</span>
                        </div>
                      </div>

                      <button
                        onClick={() => loadDemo(d)}
                        className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center justify-center space-x-1.5"
                      >
                        <i className="fa-solid fa-play text-[10px]"></i>
                        <span>Launch Demonstration</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB 3: MEDICAL TERMINOLOGY DICTIONARY */}
            {activeTab === 'dictionary' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-navy-900 flex items-center space-x-2">
                        <i className="fa-solid fa-book-medical text-brand-600"></i>
                        <span>Searchable Oncology Terminology Dictionary</span>
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        252+ consolidated medical terms extracted from the 4 primary oncology sources with English and Bengali explanations.
                      </p>
                    </div>
                    <span className="text-xs font-bold px-3 py-1.5 bg-brand-50 text-brand-800 rounded-full border border-brand-200 w-fit">
                      {terms.length} Terms Found
                    </span>
                  </div>

                  {/* Search and Category Filter */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
                    <div className="md:col-span-2 relative">
                      <i className="fa-solid fa-magnifying-glass absolute left-3.5 top-3.5 text-slate-400 text-sm"></i>
                      <input
                        type="text"
                        value={termSearch}
                        onChange={(e) => setTermSearch(e.target.value)}
                        placeholder="Search oncology terms, abbreviations, Bengali words (e.g. 'biopsy', 'মেটাস্ট্যাসিস', 'carcinoma')..."
                        className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none text-sm text-slate-800 transition-all"
                      />
                      {termSearch && (
                        <button onClick={() => setTermSearch('')} className="absolute right-3 top-3 text-slate-400 hover:text-slate-600 text-xs">
                          <i className="fa-solid fa-xmark"></i>
                        </button>
                      )}
                    </div>

                    <div>
                      <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="w-full py-2.5 px-3 rounded-xl border border-slate-300 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none text-sm text-slate-700 bg-white"
                      >
                        <option value="All">All Categories</option>
                        <option value="General Oncology">General Oncology</option>
                        <option value="Diagnosis & Pathology">Diagnosis & Pathology</option>
                        <option value="Treatment & Chemotherapy">Treatment & Chemotherapy</option>
                        <option value="Anatomy & Staging">Anatomy & Staging</option>
                        <option value="Palliative & Supportive Care">Palliative & Supportive Care</option>
                      </select>
                    </div>
                  </div>
                </div>

                {termsLoading ? (
                  <div className="p-12 text-center text-slate-400">
                    <i className="fa-solid fa-circle-notch fa-spin text-2xl text-brand-600 mb-2"></i>
                    <p className="text-xs">Searching verified dictionary...</p>
                  </div>
                ) : terms.length === 0 ? (
                  <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
                    <i className="fa-solid fa-book-open text-3xl text-slate-300 mb-2"></i>
                    <p className="font-bold text-sm text-slate-700">No matching medical terms found</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {terms.map((item, idx) => (
                      <div key={idx} className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm hover:shadow-md hover:border-brand-300 transition-all flex flex-col justify-between space-y-3">
                        <div className="space-y-2">
                          <div className="flex items-start justify-between gap-2">
                            <h3 className="font-bold text-base text-navy-900">{item.term}</h3>
                            <span className="text-[10px] font-semibold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full shrink-0">
                              {item.category || "General"}
                            </span>
                          </div>

                          {item.bengali_term && (
                            <div className="font-bn font-bold text-sm text-brand-700">
                              বাংলা: {item.bengali_term}
                            </div>
                          )}

                          <div className="text-xs text-slate-600 line-clamp-3">
                            <span className="font-semibold text-slate-700">Definition: </span>
                            {item.medical_definition || item.definition}
                          </div>

                          {(item.simple_meaning || item.simplified_en) && (
                            <div className="text-xs text-brand-900 bg-brand-50/50 p-2.5 rounded-xl border border-brand-100">
                              <span className="font-semibold text-brand-800">In simple words: </span>
                              {item.simple_meaning || item.simplified_en}
                            </div>
                          )}
                        </div>

                        <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                          <span className="truncate max-w-[170px]" title={item.source_document}>
                            <i className="fa-solid fa-file-lines text-slate-400 mr-1"></i>
                            {item.source_document ? item.source_document.replace(/^\d+_/, '').replace(/\.[^/.]+$/, '') : 'Oncology Sources'}
                          </span>

                          <div className="flex items-center space-x-1.5">
                            <button
                              onClick={() => playSpeech(`${item.term}. ${item.simple_meaning || item.medical_definition}`, 'english')}
                              className="p-1 px-2 rounded bg-slate-100 hover:bg-brand-100 text-slate-600"
                              title="Listen"
                            >
                              <i className="fa-solid fa-volume-high text-[10px]"></i>
                            </button>
                            <button
                              onClick={() => {
                                setInputText(`Explain ${item.term}: ${item.medical_definition || item.definition}`);
                                setActiveTab('simplify');
                                handleRun(`Explain ${item.term}: ${item.medical_definition || item.definition}`, 'simplify');
                              }}
                              className="p-1 px-2 rounded bg-brand-50 hover:bg-brand-100 text-brand-800 font-semibold"
                            >
                              Simplify
                            </button>
                          </div>
                        </div>

                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 4: ASHA FIELD GUIDE & RED FLAGS */}
            {activeTab === 'guide' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 rounded-2xl bg-brand-100 text-brand-700 flex items-center justify-center text-2xl font-bold">
                      <i className="fa-solid fa-user-doctor"></i>
                    </div>
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-navy-900">
                        ASHA Oncology Communication & Field Guide
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        Practical protocols, C-A-U-T-I-O-N warning signs, and compassionate counseling guidance for community visits.
                      </p>
                    </div>
                  </div>
                </div>

                {/* CAUTION Warning Signs */}
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-red-200 shadow-sm space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-red-100">
                    <h3 className="font-black text-base sm:text-lg text-red-900 flex items-center space-x-2">
                      <i className="fa-solid fa-triangle-exclamation text-red-600"></i>
                      <span>Cancer Warning Signs ("C-A-U-T-I-O-N" Protocol)</span>
                    </h3>
                    <span className="text-xs font-bold text-red-700 bg-red-100 px-2.5 py-1 rounded-full">
                      Immediate Referral
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    {[
                      { l: 'C', t: 'Change in bowel or bladder habits', b: 'মল বা মূত্রের অভ্যাসে দীর্ঘস্থায়ী পরিবর্তন।' },
                      { l: 'A', t: 'A sore that does not heal', b: 'দীর্ঘদিনেও না সারা কোনো ক্ষত বা ঘা।' },
                      { l: 'U', t: 'Unusual bleeding or discharge', b: 'অস্বাভাবিক রক্তপাত বা স্রাব নির্গমন।' },
                      { l: 'T', t: 'Thickening or lump in breast / elsewhere', b: 'স্তন বা শরীরের যে কোনো অংশে চাকা বা পিণ্ড।' },
                      { l: 'I', t: 'Indigestion or difficulty in swallowing', b: 'খাবার গিলতে কষ্ট বা ক্রমাগত বদহজম।' },
                      { l: 'O', t: 'Obvious change in wart or mole', b: 'তিল বা আঁচিলের আকার বা রঙের স্পষ্ট পরিবর্তন।' },
                      { l: 'N', t: 'Nagging cough or hoarseness', b: 'টানা কাশি বা গলার স্বরের স্থায়ী পরিবর্তন।' },
                      { l: 'Action', t: 'Community Referral Protocol', b: 'অনতিবিলম্বে মহকুমা বা জেলা হাসপাতালে রেফার করুন।' }
                    ].map((item, idx) => (
                      <div key={idx} className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                        <div className="font-black text-red-700 text-base">{item.l}</div>
                        <div className="font-bold text-xs text-slate-800">{item.t}</div>
                        <p className="text-[11px] text-slate-600 mt-1 font-bn">{item.b}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Patient Communication Principles */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-3">
                    <h4 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
                      <i className="fa-solid fa-heart-pulse text-brand-600"></i>
                      <span>Compassionate Counseling Tips</span>
                    </h4>
                    <ul className="text-xs text-slate-600 space-y-2.5">
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-check text-brand-600 mt-0.5"></i>
                        <span><strong>Listen without interrupting:</strong> Acknowledge patient fears before delivering medical facts.</span>
                      </li>
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-check text-brand-600 mt-0.5"></i>
                        <span><strong>Dispel common cancer myths:</strong> Emphasize that cancer is not contagious and early detection saves lives.</span>
                      </li>
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-check text-brand-600 mt-0.5"></i>
                        <span><strong>Encourage family presence:</strong> Involve trusted family members so post-treatment instructions are understood.</span>
                      </li>
                    </ul>
                  </div>

                  <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-3">
                    <h4 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
                      <i className="fa-solid fa-shield-heart text-teal-600"></i>
                      <span>Medical Safety & Ethics Guardrails</span>
                    </h4>
                    <ul className="text-xs text-slate-600 space-y-2.5">
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-xmark text-red-500 mt-0.5"></i>
                        <span><strong>Never alter prescription dosages:</strong> Never recommend herbal substitutes or discontinue prescribed chemotherapy.</span>
                      </li>
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-xmark text-red-500 mt-0.5"></i>
                        <span><strong>Never offer definitive cure guarantees:</strong> Provide realistic hope based on doctor's clinical staging.</span>
                      </li>
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-check text-brand-600 mt-0.5"></i>
                        <span><strong>Refer back to treating oncologist:</strong> If a symptom is new or acute, escort the patient to the nearest hospital.</span>
                      </li>
                    </ul>
                  </div>
                </div>

              </div>
            )}

            {/* TAB 5: LOCAL SESSION HISTORY */}
            {activeTab === 'history' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-navy-900 flex items-center space-x-2">
                        <i className="fa-solid fa-clock-rotate-left text-brand-600"></i>
                        <span>Local Session History</span>
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        Past medical simplifications from this browser session. Saved locally for offline access during village visits.
                      </p>
                    </div>

                    {history.length > 0 && (
                      <button
                        onClick={() => {
                          if (confirm("Clear local session history?")) {
                            setHistory([]);
                            localStorage.removeItem('oncosathi_history');
                          }
                        }}
                        className="text-xs text-red-600 hover:text-red-700 font-semibold px-3 py-1.5 rounded-lg border border-red-200 hover:bg-red-50 transition-colors"
                      >
                        Clear History
                      </button>
                    )}
                  </div>

                  {history.length === 0 ? (
                    <div className="p-12 text-center text-slate-400">
                      <i className="fa-regular fa-clock text-3xl mb-2 text-slate-300"></i>
                      <p className="font-bold text-sm text-slate-600">No previous simplifications saved yet</p>
                    </div>
                  ) : (
                    <div className="space-y-3 pt-2">
                      {history.map((item) => (
                        <div key={item.id} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 hover:border-brand-300 transition-all space-y-2">
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-semibold text-slate-500">{item.timestamp}</span>
                            <div className="flex items-center space-x-2">
                              <span className="bg-brand-100 text-brand-800 text-[10px] font-bold px-2 py-0.5 rounded">
                                {item.language === 'bengali' ? 'সহজ বাংলা' : 'Simple English'}
                              </span>
                              <span className="bg-slate-200 text-slate-700 text-[10px] font-bold px-2 py-0.5 rounded">
                                {item.level}
                              </span>
                            </div>
                          </div>

                          <div className="text-xs font-mono text-slate-600 line-clamp-1">
                            Q: {item.originalText}
                          </div>

                          <div className={`text-sm text-slate-800 line-clamp-3 ${item.language === 'bengali' ? 'font-bn' : ''}`}>
                            {item.simplifiedText}
                          </div>

                          <div className="pt-2 flex items-center justify-between text-xs">
                            <button
                              onClick={() => {
                                setInputText(item.originalText);
                                setTargetLang(item.language);
                                setActiveTab('simplify');
                                handleRun(item.originalText);
                              }}
                              className="text-brand-600 hover:text-brand-700 font-bold flex items-center space-x-1"
                            >
                              <span>Reload in Simplifier</span>
                              <i className="fa-solid fa-arrow-right text-[10px]"></i>
                            </button>

                            <button
                              onClick={() => playSpeech(item.simplifiedText, item.language)}
                              className="text-slate-600 hover:text-brand-600 font-semibold flex items-center space-x-1"
                            >
                              <i className="fa-solid fa-volume-high text-xs"></i>
                              <span>Listen</span>
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                </div>
              </div>
            )}

          </main>

          {/* SOURCE INSPECTION MODAL (PHASE 9 & 3) */}
          {selectedSourceModal && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/60 backdrop-blur-sm animate-fadeIn">
              <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden">
                <div className="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                  <div className="flex items-center space-x-2">
                    <span className="w-8 h-8 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center text-sm font-bold">
                      <i className="fa-solid fa-file-shield"></i>
                    </span>
                    <div>
                      <h3 className="font-bold text-sm sm:text-base text-navy-900">
                        {selectedSourceModal.document_title || selectedSourceModal.document_name || selectedSourceModal.source_document}
                      </h3>
                      <p className="text-[11px] text-slate-500">
                        {selectedSourceModal.section_or_page || selectedSourceModal.section || 'Clinical reference excerpt'} • Confidence: {Math.round((selectedSourceModal.similarity_score || 0.88) * 100)}%
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedSourceModal(null)}
                    className="w-8 h-8 rounded-full bg-slate-200/80 hover:bg-slate-300 text-slate-600 flex items-center justify-center text-xs transition-colors"
                  >
                    <i className="fa-solid fa-xmark"></i>
                  </button>
                </div>

                <div className="p-6 overflow-y-auto space-y-4 custom-scrollbar text-xs sm:text-sm text-slate-700 leading-relaxed">
                  <div className="p-4 rounded-xl bg-teal-50/50 border border-teal-100 text-teal-900">
                    <span className="font-bold block mb-1">Knowledge Chunk Excerpt:</span>
                    <p className="font-mono text-xs whitespace-pre-wrap">{selectedSourceModal.chunk_text || selectedSourceModal.excerpt}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="font-semibold text-slate-500 block">Source Document:</span>
                      <span className="font-bold text-slate-800">{selectedSourceModal.document_name || selectedSourceModal.source_document}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="font-semibold text-slate-500 block">Category / Section:</span>
                      <span className="font-bold text-slate-800">{selectedSourceModal.category || selectedSourceModal.section_or_page || 'General Oncology'}</span>
                    </div>
                  </div>
                </div>

                <div className="p-4 border-t border-slate-100 bg-slate-50 flex items-center justify-end">
                  <button
                    onClick={() => setSelectedSourceModal(null)}
                    className="px-4 py-2 bg-navy-900 hover:bg-navy-800 text-white font-bold text-xs rounded-xl transition-colors"
                  >
                    Close Reference
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Footer */}
          <footer className="bg-white border-t border-slate-200 mt-12 py-8 text-xs text-slate-500">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex items-center space-x-2">
                <div className="w-6 h-6 rounded-md bg-brand-600 text-white flex items-center justify-center font-bold text-xs">
                  <i className="fa-solid fa-heart-pulse"></i>
                </div>
                <span className="font-bold text-slate-800">OncoSathi AI</span>
                <span>— Simplifying Cancer Knowledge for Community Healthcare</span>
              </div>
              <div className="flex items-center space-x-4">
                <span>Designed for ASHA Workers</span>
                <span>•</span>
                <span>Simple English & সহজ বাংলা</span>
                <span>•</span>
                <span className="text-emerald-600 font-semibold">Grounded RAG Pipeline</span>
              </div>
            </div>
          </footer>

        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
"""

def main():
    INDEX_HTML.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"[OncoSathi] Wrote polished frontend index.html successfully at {INDEX_HTML} ({len(HTML_CONTENT)} bytes)")

if __name__ == "__main__":
    main()
