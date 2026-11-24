# -*- coding: utf-8 -*-
"""
Generate frontend/public/index.html
High-performance, modern, accessible React application for OncoSathi AI.
Zero-build required: runs directly out of FastAPI static serving.
"""
import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
FRONTEND_PUBLIC = WORKSPACE / "frontend" / "public"
FRONTEND_PUBLIC.mkdir(parents=True, exist_ok=True)
INDEX_HTML = FRONTEND_PUBLIC / "index.html"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OncoSathi AI — Simplifying Cancer Knowledge for Community Healthcare</title>
  <meta name="description" content="AI Oncology Medical Information Simplifier designed for ASHA community health workers in Simple English and Bengali." />
  
  <!-- Google Fonts: Inter & Hind Siliguri for Bengali -->
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

    // Sample oncology prompts from the 4 primary knowledge sources
    const SAMPLE_PROMPTS = [
      {
        title: "Cellular Proliferation & Neoplasm",
        text: "Malignant neoplasms are characterized by uncontrolled cellular proliferation with potential invasion and metastasis.",
        desc: "Cell growth & cancer spread"
      },
      {
        title: "Chemotherapy Cycles",
        text: "Patient scheduled for adjuvant chemotherapy regimens following surgical resection to eradicate microscopic metastases.",
        desc: "Post-surgery chemo treatment"
      },
      {
        title: "TNM Staging Assessment",
        text: "Histopathology shows Stage IIIA invasive ductal carcinoma classified as T3 N1 M0 with positive lymph nodes.",
        desc: "Cancer stage & lymph node involvement"
      },
      {
        title: "Biopsy & Histopathology",
        text: "Excisional biopsy performed. Histopathology reveals poorly differentiated carcinoma requiring immunohistochemistry.",
        desc: "Tissue test & cancer type verification"
      },
      {
        title: "Palliative & Supportive Care",
        text: "Palliative care consultation recommended for advanced stage management, pain alleviation, and supportive care.",
        desc: "Comfort and pain relief care"
      }
    ];

    function App() {
      const [activeTab, setActiveTab] = useState('home'); // home, simplify, dictionary, guide, history
      const [inputText, setInputText] = useState('');
      const [targetLang, setTargetLang] = useState('english'); // english, bengali
      const [targetLevel, setTargetLevel] = useState(2); // 1, 2, 3
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState(null);
      const [result, setResult] = useState(null);
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
      const [systemStatus, setSystemStatus] = useState({ ready: true, termCount: 252, chunksCount: 419 });

      // Load History on Mount
      useEffect(() => {
        try {
          const savedHistory = localStorage.getItem('oncosathi_history');
          if (savedHistory) {
            setHistory(JSON.parse(savedHistory));
          }
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
              chunksCount: 419,
              provider: data.llm_provider
            });
          }
        } catch (e) {
          console.log("Health check notice", e);
        }
      };

      // Load dictionary terms on demand
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
            setTerms(data.terms || []);
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

      // Debounced search for dictionary
      useEffect(() => {
        if (activeTab !== 'dictionary') return;
        const timer = setTimeout(() => {
          loadTerms(termSearch, selectedCategory);
        }, 300);
        return () => clearTimeout(timer);
      }, [termSearch]);

      // Handle Simplification Submission
      const handleSimplify = async (overrideText = null) => {
        const textToProcess = overrideText !== null ? overrideText : inputText;
        if (!textToProcess.trim()) {
          setError("Please enter or paste medical text to simplify.");
          return;
        }

        setError(null);
        setLoading(true);
        setResult(null);
        setFeedbackSent(false);
        setCopied(false);
        stopSpeech();

        try {
          const res = await fetch(`${API_BASE}/api/simplify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              text: textToProcess,
              target_language: targetLang,
              simplification_level: targetLevel
            })
          });

          if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Server error (${res.status})`);
          }

          const data = await res.json();
          setResult(data);

          // Save to Local History
          const newEntry = {
            id: Date.now(),
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', month: 'short', day: 'numeric' }),
            originalText: textToProcess,
            simplifiedText: data.simplified_text,
            language: data.language,
            level: data.level,
            keyPoints: data.key_points || [],
            sourcesCount: (data.sources || []).length
          };
          const updatedHistory = [newEntry, ...history.slice(0, 19)];
          setHistory(updatedHistory);
          localStorage.setItem('oncosathi_history', JSON.stringify(updatedHistory));

          if (activeTab !== 'simplify') {
            setActiveTab('simplify');
          }
        } catch (err) {
          setError(err.message || "An unexpected error occurred during simplification.");
        } finally {
          setLoading(false);
        }
      };

      // Text-To-Speech using Web Speech API with fallback
      const playSpeech = (textToSpeak, langCode) => {
        if (!('speechSynthesis' in window)) {
          alert("Your browser does not support Web Speech Text-to-Speech.");
          return;
        }

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        const isBn = langCode === 'bengali' || /[\u0980-\u09FF]/.test(textToSpeak);

        utterance.lang = isBn ? 'bn-IN' : 'en-IN';
        utterance.rate = isBn ? 0.85 : 0.95;
        utterance.pitch = 1.0;

        // Try to match appropriate voice if available
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
          const matchingVoice = voices.find(v => isBn ? v.lang.startsWith('bn') : (v.lang.startsWith('en-IN') || v.lang.startsWith('en-GB') || v.lang.startsWith('en-US')));
          if (matchingVoice) utterance.voice = matchingVoice;
        }

        utterance.onstart = () => {
          setTtsSpeaking(true);
          setTtsPaused(false);
        };
        utterance.onend = () => {
          setTtsSpeaking(false);
          setTtsPaused(false);
        };
        utterance.onerror = (e) => {
          console.warn("TTS error", e);
          setTtsSpeaking(false);
          setTtsPaused(false);
        };

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

      // Copy result to clipboard
      const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
      };

      // Send feedback
      const handleFeedback = async (isHelpful) => {
        setFeedbackSent(true);
        try {
          await fetch(`${API_BASE}/api/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              query_text: inputText,
              simplified_text: result ? result.simplified_text : '',
              is_helpful: isHelpful,
              rating: isHelpful ? 5 : 2,
              feedback_type: 'asha_simplification'
            })
          });
        } catch (e) {
          console.log("Feedback recorded locally");
        }
      };

      return (
        <div className="min-h-screen flex flex-col bg-slate-50 font-sans text-slate-800">
          
          {/* Top Banner & Accessibility Bar */}
          <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex items-center justify-between h-16 sm:h-20">
                
                {/* Brand / Logo */}
                <div 
                  className="flex items-center space-x-3 cursor-pointer group"
                  onClick={() => setActiveTab('home')}
                >
                  <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-tr from-brand-600 to-teal-400 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
                    <i className="fa-solid fa-hand-holding-heart text-xl sm:text-2xl"></i>
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-extrabold text-xl sm:text-2xl tracking-tight text-navy-900">
                        Onco<span className="text-brand-600">Sathi</span>
                      </span>
                      <span className="bg-brand-100 text-brand-800 text-xs px-2 py-0.5 rounded-full font-semibold border border-brand-200">
                        AI for ASHA
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 hidden sm:block">
                      Simplifying Cancer Knowledge for Community Healthcare • <span className="font-bn font-medium text-brand-700">অনকোসাথী এআই</span>
                    </p>
                  </div>
                </div>

                {/* Desktop Navigation Links */}
                <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
                  <button 
                    onClick={() => setActiveTab('home')}
                    className={`px-3 py-2 rounded-lg font-medium text-sm transition-colors ${activeTab === 'home' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-house mr-1.5 text-xs"></i> Home
                  </button>
                  <button 
                    onClick={() => setActiveTab('simplify')}
                    className={`px-3 py-2 rounded-lg font-medium text-sm transition-colors ${activeTab === 'simplify' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-wand-magic-sparkles mr-1.5 text-xs"></i> Simplifier
                  </button>
                  <button 
                    onClick={() => setActiveTab('dictionary')}
                    className={`px-3 py-2 rounded-lg font-medium text-sm transition-colors ${activeTab === 'dictionary' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-book-medical mr-1.5 text-xs"></i> Medical Dictionary
                  </button>
                  <button 
                    onClick={() => setActiveTab('guide')}
                    className={`px-3 py-2 rounded-lg font-medium text-sm transition-colors ${activeTab === 'guide' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-user-doctor mr-1.5 text-xs"></i> ASHA Field Guide
                  </button>
                  <button 
                    onClick={() => setActiveTab('history')}
                    className={`px-3 py-2 rounded-lg font-medium text-sm transition-colors ${activeTab === 'history' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    <i className="fa-solid fa-clock-rotate-left mr-1.5 text-xs"></i> History {history.length > 0 && `(${history.length})`}
                  </button>
                </nav>

                {/* Right: Language Indicator & Knowledge Status */}
                <div className="flex items-center space-x-2">
                  <div className="hidden lg:flex items-center space-x-1.5 text-xs bg-emerald-50 text-emerald-700 px-2.5 py-1.5 rounded-full border border-emerald-200">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span className="font-semibold">4 Sources Grounded ({systemStatus.termCount} Terms)</span>
                  </div>

                  {/* Quick Language Toggle */}
                  <div className="flex bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-medium">
                    <button
                      onClick={() => setTargetLang('english')}
                      className={`px-2.5 py-1 rounded-md transition-all ${targetLang === 'english' ? 'bg-white shadow text-brand-800 font-bold' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                      English
                    </button>
                    <button
                      onClick={() => setTargetLang('bengali')}
                      className={`px-2.5 py-1 rounded-md transition-all font-bn ${targetLang === 'bengali' ? 'bg-brand-600 shadow text-white font-bold' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                      বাংলা
                    </button>
                  </div>
                </div>

              </div>
            </div>

            {/* Mobile Navigation bar */}
            <div className="flex md:hidden border-t border-slate-200 bg-white overflow-x-auto px-2 py-1.5 space-x-1 custom-scrollbar text-xs">
              <button onClick={() => setActiveTab('home')} className={`px-2.5 py-1 rounded-md whitespace-nowrap ${activeTab === 'home' ? 'bg-brand-100 text-brand-800 font-bold' : 'text-slate-600'}`}>
                <i className="fa-solid fa-house mr-1"></i> Home
              </button>
              <button onClick={() => setActiveTab('simplify')} className={`px-2.5 py-1 rounded-md whitespace-nowrap ${activeTab === 'simplify' ? 'bg-brand-100 text-brand-800 font-bold' : 'text-slate-600'}`}>
                <i className="fa-solid fa-wand-magic-sparkles mr-1"></i> Simplifier
              </button>
              <button onClick={() => setActiveTab('dictionary')} className={`px-2.5 py-1 rounded-md whitespace-nowrap ${activeTab === 'dictionary' ? 'bg-brand-100 text-brand-800 font-bold' : 'text-slate-600'}`}>
                <i className="fa-solid fa-book-medical mr-1"></i> Dictionary
              </button>
              <button onClick={() => setActiveTab('guide')} className={`px-2.5 py-1 rounded-md whitespace-nowrap ${activeTab === 'guide' ? 'bg-brand-100 text-brand-800 font-bold' : 'text-slate-600'}`}>
                <i className="fa-solid fa-user-doctor mr-1"></i> Field Guide
              </button>
              <button onClick={() => setActiveTab('history')} className={`px-2.5 py-1 rounded-md whitespace-nowrap ${activeTab === 'history' ? 'bg-brand-100 text-brand-800 font-bold' : 'text-slate-600'}`}>
                <i className="fa-solid fa-clock mr-1"></i> History
              </button>
            </div>
          </header>

          {/* Main Content Area */}
          <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">

            {/* TAB 1: HOME DASHBOARD */}
            {activeTab === 'home' && (
              <div className="space-y-8 animate-fadeIn">
                
                {/* Hero Card */}
                <div className="relative rounded-3xl bg-gradient-to-r from-navy-900 via-navy-800 to-teal-900 text-white p-6 sm:p-10 shadow-xl overflow-hidden">
                  <div className="absolute right-0 top-0 bottom-0 w-1/3 opacity-10 bg-[radial-gradient(#2dd4bf_1px,transparent_1px)] [background-size:16px_16px]"></div>
                  
                  <div className="relative z-10 max-w-3xl space-y-4">
                    <div className="inline-flex items-center space-x-2 bg-teal-500/20 text-teal-300 text-xs px-3 py-1 rounded-full border border-teal-400/30">
                      <i className="fa-solid fa-stethoscope"></i>
                      <span>Empowering Community Healthcare & ASHA Workers</span>
                    </div>

                    <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight leading-tight">
                      Simplifying Cancer Knowledge for Grassroots Care.
                    </h1>

                    <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
                      OncoSathi AI transforms complex oncology terms, staging protocols, and biopsy reports into clear, compassionate, literacy-appropriate language in <strong>Simple English</strong> and <strong>সহজ বাংলা</strong>.
                    </p>

                    <div className="pt-2 flex flex-wrap gap-3">
                      <button 
                        onClick={() => setActiveTab('simplify')}
                        className="bg-brand-500 hover:bg-brand-400 text-navy-950 font-bold px-6 py-3 rounded-xl shadow-lg shadow-brand-500/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center space-x-2"
                      >
                        <i className="fa-solid fa-wand-magic-sparkles"></i>
                        <span>Start Medical Simplifier</span>
                      </button>

                      <button 
                        onClick={() => setActiveTab('dictionary')}
                        className="bg-white/10 hover:bg-white/20 text-white font-semibold px-5 py-3 rounded-xl border border-white/20 hover:border-white/40 transition-all flex items-center space-x-2"
                      >
                        <i className="fa-solid fa-book-medical"></i>
                        <span>Browse 252+ Oncology Terms</span>
                      </button>
                    </div>
                  </div>
                </div>

                {/* 4 Ingested Primary Sources Banner */}
                <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
                    <div>
                      <h2 className="text-lg font-bold text-navy-900 flex items-center space-x-2">
                        <i className="fa-solid fa-database text-brand-600"></i>
                        <span>Grounded Knowledge Base (4 Ingested Primary Sources)</span>
                      </h2>
                      <p className="text-xs text-slate-500">Every response is strictly verified and referenced against these clinical source documents.</p>
                    </div>
                    <span className="inline-flex items-center text-xs font-semibold px-2.5 py-1 rounded-md bg-teal-50 text-teal-700 border border-teal-200 w-fit">
                      <i className="fa-solid fa-shield-halved mr-1.5 text-teal-600"></i> Zero-Hallucination Guardrails
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-brand-300 transition-all">
                      <div className="w-8 h-8 rounded-lg bg-red-100 text-red-600 flex items-center justify-center font-bold text-xs mb-2">
                        PDF
                      </div>
                      <h4 className="font-bold text-sm text-slate-800 line-clamp-1">1. IJPC Cancer Glossary</h4>
                      <p className="text-xs text-slate-500 mt-1">Foundational oncology healthcare terminology & patient definitions.</p>
                      <span className="inline-block mt-2 text-[11px] font-semibold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">4 Extracted Pages</span>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-brand-300 transition-all">
                      <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-xs mb-2">
                        PDF
                      </div>
                      <h4 className="font-bold text-sm text-slate-800 line-clamp-1">2. Medical Oncology (Ba)</h4>
                      <p className="text-xs text-slate-500 mt-1">Presentation terminology, staging, chemotherapy & clinical concepts.</p>
                      <span className="inline-block mt-2 text-[11px] font-semibold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">4 Extracted Slides</span>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-brand-300 transition-all">
                      <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-xs mb-2">
                        DOCX
                      </div>
                      <h4 className="font-bold text-sm text-slate-800 line-clamp-1">3. Bengali-English Terminology</h4>
                      <p className="text-xs text-slate-500 mt-1">Curated English medical terms with accurate Bengali equivalents.</p>
                      <span className="inline-block mt-2 text-[11px] font-semibold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">157 Parallel Records</span>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-brand-300 transition-all">
                      <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold text-xs mb-2">
                        XLSX
                      </div>
                      <h4 className="font-bold text-sm text-slate-800 line-clamp-1">4. Comprehensive Tables</h4>
                      <p className="text-xs text-slate-500 mt-1">Tabular clinical definitions, categories, and symptom associations.</p>
                      <span className="inline-block mt-2 text-[11px] font-semibold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">171 Structured Rows</span>
                    </div>
                  </div>
                </div>

                {/* 3 Simplification Levels Explanation */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div className="w-2 h-full bg-emerald-500 absolute left-0 top-0"></div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded-full uppercase tracking-wider">Level 1</span>
                      <i className="fa-solid fa-child-reaching text-emerald-500 text-xl"></i>
                    </div>
                    <h3 className="font-bold text-base text-slate-900 mb-1">Basic (সহজতম স্তর)</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Short sentences, everyday analogies, very simple words. Ideal for patients with limited literacy or initial community awareness.
                    </p>
                  </div>

                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div className="w-2 h-full bg-brand-500 absolute left-0 top-0"></div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-bold text-brand-700 bg-brand-100 px-2.5 py-1 rounded-full uppercase tracking-wider">Level 2 (Recommended)</span>
                      <i className="fa-solid fa-users text-brand-500 text-xl"></i>
                    </div>
                    <h3 className="font-bold text-base text-slate-900 mb-1">Easy / Community Care</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Clear conversational explanations with short definitions. Balanced detail designed for ASHA worker counseling sessions.
                    </p>
                  </div>

                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div className="w-2 h-full bg-indigo-500 absolute left-0 top-0"></div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-bold text-indigo-700 bg-indigo-100 px-2.5 py-1 rounded-full uppercase tracking-wider">Level 3</span>
                      <i className="fa-solid fa-clipboard-check text-indigo-500 text-xl"></i>
                    </div>
                    <h3 className="font-bold text-base text-slate-900 mb-1">Detailed Understandable</h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Structured clinical breakdown of diagnostic terms, stages, and regimens while avoiding heavy, confusing medical jargon.
                    </p>
                  </div>
                </div>

                {/* Quick Clinical Prompts Section */}
                <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
                  <h3 className="font-bold text-sm text-slate-700 uppercase tracking-wider flex items-center">
                    <i className="fa-regular fa-lightbulb text-amber-500 mr-2"></i>
                    Try Sample Medical Queries from Real Reports
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {SAMPLE_PROMPTS.map((p, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setInputText(p.text);
                          handleSimplify(p.text);
                        }}
                        className="text-left p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-brand-50 hover:border-brand-300 transition-all group"
                      >
                        <div className="font-bold text-xs text-slate-800 group-hover:text-brand-800">{p.title}</div>
                        <div className="text-[11px] text-slate-500 line-clamp-2 mt-1">{p.text}</div>
                        <div className="text-[10px] text-brand-600 font-semibold mt-2 flex items-center">
                          <span>Simplify now</span>
                          <i className="fa-solid fa-arrow-right ml-1 text-[9px] group-hover:translate-x-0.5 transition-transform"></i>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

              </div>
            )}

            {/* TAB 2: SIMPLIFIER (MAIN ENGINE) */}
            {activeTab === 'simplify' && (
              <div className="space-y-6 animate-fadeIn">
                
                {/* Input Card */}
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
                  
                  {/* Card Header */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-3">
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-navy-900 flex items-center space-x-2">
                        <i className="fa-solid fa-wand-magic-sparkles text-brand-600"></i>
                        <span>Medical Information Simplifier</span>
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        Paste complicated oncology reports, doctor's notes, or clinical terms below.
                      </p>
                    </div>

                    {/* Quick Example Chips dropdown or buttons */}
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-slate-400 font-medium hidden sm:inline">Quick Fill:</span>
                      <button
                        onClick={() => setInputText("Malignant neoplasms are characterized by uncontrolled cellular proliferation with potential invasion and metastasis.")}
                        className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-2.5 py-1 rounded-md transition-colors font-medium"
                      >
                        Neoplasm
                      </button>
                      <button
                        onClick={() => setInputText("What is the difference between adjuvant chemotherapy and neoadjuvant chemotherapy?")}
                        className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-2.5 py-1 rounded-md transition-colors font-medium"
                      >
                        Adjuvant vs Neoadjuvant
                      </button>
                      <button
                        onClick={() => setInputText("Patient diagnosed with Stage IIIA invasive ductal carcinoma T3 N1 M0.")}
                        className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-2.5 py-1 rounded-md transition-colors font-medium"
                      >
                        TNM Stage
                      </button>
                    </div>
                  </div>

                  {/* Input Textarea */}
                  <div className="space-y-2">
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-600">
                      Medical Text / Oncology Query
                    </label>
                    <div className="relative">
                      <textarea
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        rows={4}
                        placeholder={targetLang === 'bengali' 
                          ? "এখানে জটিল মেডিকেল রিপোর্ট, ডাক্তারের ব্যবস্থাপত্রের নোট বা ক্যানসার সংক্রান্ত প্রশ্ন লিখুন বা পেস্ট করুন... (যেমন: 'বায়োপসি কী?', 'কেমোথেরাপির কাজ কী?')" 
                          : "Paste complex medical text, doctor's notes, or oncology questions here... (e.g. 'What does histopathology biopsy report mean?')"
                        }
                        className="w-full p-4 rounded-2xl border border-slate-300 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none text-slate-800 text-sm sm:text-base leading-relaxed transition-all resize-y custom-scrollbar"
                      ></textarea>

                      {inputText && (
                        <button
                          onClick={() => setInputText('')}
                          className="absolute right-3 top-3 text-slate-400 hover:text-slate-600 p-1 rounded-full hover:bg-slate-100 text-xs"
                          title="Clear text"
                        >
                          <i className="fa-solid fa-xmark"></i>
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Controls Row: Language & Simplification Level */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                    
                    {/* Target Language Selector */}
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/80 space-y-2">
                      <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                        <i className="fa-solid fa-language text-brand-600 mr-1.5"></i> Target Output Language
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        <button
                          type="button"
                          onClick={() => setTargetLang('english')}
                          className={`py-2 px-3 rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-center space-x-1.5 transition-all ${targetLang === 'english' ? 'bg-white border-2 border-brand-500 text-brand-800 shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          <span>Simple English</span>
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLang('bengali')}
                          className={`py-2 px-3 rounded-xl text-xs sm:text-sm font-semibold font-bn flex items-center justify-center space-x-1.5 transition-all ${targetLang === 'bengali' ? 'bg-brand-600 border-2 border-brand-700 text-white shadow-sm' : 'bg-slate-200/60 border border-transparent text-slate-600 hover:bg-slate-200'}`}
                        >
                          <span>সহজ বাংলা</span>
                        </button>
                      </div>
                    </div>

                    {/* Simplification Level Selector */}
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/80 space-y-2">
                      <div className="flex items-center justify-between">
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                          <i className="fa-solid fa-sliders text-brand-600 mr-1.5"></i> Reading Difficulty Level
                        </label>
                        <span className="text-[11px] font-bold text-brand-700">
                          {targetLevel === 1 ? 'Level 1: Basic' : targetLevel === 2 ? 'Level 2: Easy' : 'Level 3: Detailed'}
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

                  {/* Error Notification */}
                  {error && (
                    <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-xs sm:text-sm flex items-start space-x-2">
                      <i className="fa-solid fa-circle-exclamation text-red-500 mt-0.5"></i>
                      <span>{error}</span>
                    </div>
                  )}

                  {/* Primary Simplify Action Button */}
                  <div className="flex items-center justify-end space-x-3 pt-2">
                    <button
                      type="button"
                      onClick={() => setInputText('')}
                      className="px-4 py-2.5 rounded-xl border border-slate-300 text-slate-600 hover:bg-slate-100 text-xs sm:text-sm font-semibold transition-colors"
                    >
                      Clear
                    </button>

                    <button
                      type="button"
                      disabled={loading || !inputText.trim()}
                      onClick={() => handleSimplify()}
                      className={`px-6 py-3 rounded-xl font-bold text-sm sm:text-base flex items-center space-x-2 shadow-lg transition-all ${loading || !inputText.trim() ? 'bg-slate-300 text-slate-500 cursor-not-allowed shadow-none' : 'bg-brand-600 hover:bg-brand-500 text-white shadow-brand-500/30 hover:scale-[1.02] active:scale-[0.98]'}`}
                    >
                      {loading ? (
                        <>
                          <i className="fa-solid fa-circle-notch fa-spin"></i>
                          <span>Simplifying Medical Content...</span>
                        </>
                      ) : (
                        <>
                          <i className="fa-solid fa-wand-magic-sparkles"></i>
                          <span>Simplify Medical Information</span>
                        </>
                      )}
                    </button>
                  </div>

                </div>

                {/* Loading Skeleton Indicator */}
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
                      <span>Querying 419 knowledge chunks from 4 oncology sources & generating simplified response...</span>
                    </div>
                  </div>
                )}

                {/* RESULT PRESENTATION CARD */}
                {result && !loading && (
                  <div className="bg-white rounded-3xl p-6 sm:p-8 border border-brand-200/80 shadow-md space-y-6 animate-fadeIn">
                    
                    {/* Result Header & Metadata Badges */}
                    <div className="flex flex-wrap items-center justify-between pb-4 border-b border-slate-100 gap-3">
                      <div className="flex items-center space-x-2">
                        <span className="w-8 h-8 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm">
                          <i className="fa-solid fa-notes-medical"></i>
                        </span>
                        <div>
                          <h3 className="text-base sm:text-lg font-black text-navy-900">
                            {result.language === 'bengali' ? 'সহজ ভাষায় ব্যাখ্যা (Simplified Explanation)' : 'Simplified Medical Explanation'}
                          </h3>
                          <p className="text-xs text-slate-500">
                            Grounded in verified oncology knowledge base
                          </p>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-brand-50 text-brand-700 border border-brand-200">
                          {result.language === 'bengali' ? 'সহজ বাংলা' : 'Simple English'}
                        </span>
                        <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200">
                          Level {result.level} ({result.reading_level})
                        </span>
                        {result.confidence_score !== undefined && (
                          <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-100 text-slate-700">
                            Score: {Math.round(result.confidence_score * 100)}%
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Simplified Output Box */}
                    <div className="p-5 sm:p-6 rounded-2xl bg-teal-50/50 border border-teal-200/70 space-y-4">
                      
                      {/* TTS Voice Bar */}
                      <div className="flex items-center justify-between bg-white p-2.5 px-4 rounded-xl border border-teal-200/60 shadow-sm text-xs">
                        <div className="flex items-center space-x-2">
                          <i className="fa-solid fa-volume-high text-brand-600"></i>
                          <span className="font-semibold text-slate-700">
                            Listen to Audio Explanation ({result.language === 'bengali' ? 'বাংলা কন্ঠ' : 'Spoken English'}):
                          </span>
                        </div>
                        <div className="flex items-center space-x-1.5">
                          {!ttsSpeaking ? (
                            <button
                              onClick={() => playSpeech(result.simplified_text, result.language)}
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
                                title={ttsPaused ? "Resume" : "Pause"}
                              >
                                <i className={`fa-solid ${ttsPaused ? 'fa-play' : 'fa-pause'}`}></i>
                              </button>
                              <button
                                onClick={stopSpeech}
                                className="px-2.5 py-1 rounded-lg bg-red-500 hover:bg-red-400 text-white font-bold text-xs"
                                title="Stop audio"
                              >
                                <i className="fa-solid fa-stop"></i>
                              </button>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Main Simplified Text */}
                      <div className={`text-slate-900 leading-relaxed text-base sm:text-lg whitespace-pre-line ${result.language === 'bengali' ? 'font-bn text-lg sm:text-xl' : 'font-sans'}`}>
                        {result.simplified_text}
                      </div>

                    </div>

                    {/* Key Clinical Points */}
                    {result.key_points && result.key_points.length > 0 && (
                      <div className="space-y-3">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
                          <i className="fa-solid fa-list-check text-brand-600 mr-2"></i>
                          {result.language === 'bengali' ? 'গুরুত্বপূর্ণ মূল বিষয়সমূহ (Key Points)' : 'Important Key Points for Patients & Families'}
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                          {result.key_points.map((pt, idx) => (
                            <div key={idx} className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-start space-x-2.5">
                              <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                                <i className="fa-solid fa-check text-[10px]"></i>
                              </span>
                              <span className={`text-xs sm:text-sm text-slate-800 ${result.language === 'bengali' ? 'font-bn' : ''}`}>
                                {pt}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Important Medical Terms Explained */}
                    {result.terms_explained && result.terms_explained.length > 0 && (
                      <div className="space-y-3">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
                          <i className="fa-solid fa-lightbulb text-amber-500 mr-2"></i>
                          {result.language === 'bengali' ? 'ব্যাখ্যা করা মেডিকেল পরিভাষাসমূহ (Explained Medical Terms)' : 'Medical Terms Explained in this Context'}
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                          {result.terms_explained.map((t, idx) => (
                            <div key={idx} className="p-3 rounded-xl bg-brand-50/40 border border-brand-200/60">
                              <div className="flex items-center justify-between">
                                <span className="font-bold text-xs text-brand-900">{t.term}</span>
                                {t.category && (
                                  <span className="text-[10px] bg-white text-brand-700 px-1.5 py-0.5 rounded border border-brand-200">
                                    {t.category}
                                  </span>
                                )}
                              </div>
                              <p className={`text-xs text-slate-700 mt-1.5 ${result.language === 'bengali' ? 'font-bn' : ''}`}>
                                {t.simple_meaning}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Collapsible Original Text Comparison */}
                    <details className="group border border-slate-200 rounded-xl overflow-hidden">
                      <summary className="p-3.5 bg-slate-50 hover:bg-slate-100 cursor-pointer text-xs font-bold text-slate-700 flex items-center justify-between select-none">
                        <span className="flex items-center space-x-2">
                          <i className="fa-solid fa-code-compare text-slate-500"></i>
                          <span>Compare with Original Input Text</span>
                        </span>
                        <i className="fa-solid fa-chevron-down text-slate-400 group-open:rotate-180 transition-transform"></i>
                      </summary>
                      <div className="p-4 bg-white text-xs text-slate-600 border-t border-slate-200 font-mono bg-slate-50/30 whitespace-pre-wrap">
                        {result.original_text || inputText}
                      </div>
                    </details>

                    {/* Grounded Source References */}
                    {result.sources && result.sources.length > 0 && (
                      <div className="space-y-3 pt-2">
                        <div className="flex items-center justify-between">
                          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
                            <i className="fa-solid fa-file-shield text-emerald-600 mr-2"></i>
                            Verified Source Documents Used ({result.sources.length})
                          </h4>
                          <span className="text-[11px] text-slate-400">Click any source to view clinical excerpt</span>
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
                                <span>{src.document_title || src.source_document}</span>
                              </div>
                              <div className="text-[10px] text-slate-500 mt-0.5">
                                {src.section_or_page ? `${src.section_or_page} • ` : ''}Score: {Math.round((src.similarity_score || 0.8) * 100)}%
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Medical Safety Disclaimer Box */}
                    <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/80 text-amber-900 text-xs flex items-start space-x-2.5">
                      <i className="fa-solid fa-triangle-exclamation text-amber-600 text-sm mt-0.5 shrink-0"></i>
                      <div className="space-y-1">
                        <span className="font-bold">Medical Safety Notice for ASHA Workers:</span>
                        <p className="leading-relaxed text-amber-800/90">
                          {result.disclaimer || "This simplified explanation is strictly for educational guidance and patient communication. It is not a clinical prescription or medical diagnosis. Please direct patients to a certified oncologist or Medical Officer at the Primary Health Centre for diagnostic confirmation and clinical treatment decisions."}
                        </p>
                      </div>
                    </div>

                    {/* Bottom Action Bar: Copy, Regenerate, Feedback */}
                    <div className="flex flex-wrap items-center justify-between pt-4 border-t border-slate-100 gap-3">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => copyToClipboard(result.simplified_text)}
                          className={`px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center space-x-1.5 transition-all ${copied ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-200'}`}
                        >
                          <i className={`fa-solid ${copied ? 'fa-check' : 'fa-copy'}`}></i>
                          <span>{copied ? 'Copied to Clipboard!' : 'Copy Explanation'}</span>
                        </button>

                        <button
                          onClick={() => handleSimplify()}
                          className="px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                        >
                          <i className="fa-solid fa-arrows-rotate"></i>
                          <span>Regenerate</span>
                        </button>
                      </div>

                      {/* Helpful / Feedback */}
                      <div className="flex items-center space-x-2 text-xs">
                        <span className="text-slate-500 font-medium">Was this helpful for patient counseling?</span>
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

            {/* TAB 3: MEDICAL TERMINOLOGY DICTIONARY */}
            {activeTab === 'dictionary' && (
              <div className="space-y-6 animate-fadeIn">
                
                {/* Dictionary Header */}
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-navy-900 flex items-center space-x-2">
                        <i className="fa-solid fa-book-medical text-brand-600"></i>
                        <span>Searchable Oncology Terminology Dictionary</span>
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        Consolidated 252+ terms extracted from the 4 primary medical sources with Simple English & Bengali translations.
                      </p>
                    </div>

                    <span className="text-xs font-semibold px-3 py-1.5 bg-brand-50 text-brand-800 rounded-full border border-brand-200 w-fit">
                      {terms.length} Verified Terms
                    </span>
                  </div>

                  {/* Search and Filters */}
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
                        <button
                          onClick={() => setTermSearch('')}
                          className="absolute right-3 top-3 text-slate-400 hover:text-slate-600 text-xs"
                        >
                          <i className="fa-solid fa-xmark"></i>
                        </button>
                      )}
                    </div>

                    {/* Category Filter */}
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

                {/* Terminology Cards Grid */}
                {termsLoading ? (
                  <div className="p-12 text-center text-slate-400">
                    <i className="fa-solid fa-circle-notch fa-spin text-2xl text-brand-600 mb-2"></i>
                    <p className="text-xs">Searching verified medical dictionary...</p>
                  </div>
                ) : terms.length === 0 ? (
                  <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
                    <i className="fa-solid fa-book-open text-3xl text-slate-300 mb-2"></i>
                    <p className="font-bold text-sm text-slate-700">No matching medical terms found</p>
                    <p className="text-xs text-slate-500 mt-1">Try another search keyword or clear category filters.</p>
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

                          {/* Bengali Translation if present */}
                          {item.bengali_term && (
                            <div className="font-bn font-bold text-sm text-brand-700 flex items-center space-x-1.5">
                              <span>বাংলা: {item.bengali_term}</span>
                            </div>
                          )}

                          {/* Formal definition */}
                          <div className="text-xs text-slate-600 line-clamp-3">
                            <span className="font-semibold text-slate-700">Definition: </span>
                            {item.definition}
                          </div>

                          {/* Simplified meaning */}
                          {item.simple_meaning && (
                            <div className="text-xs text-brand-900 bg-brand-50/50 p-2.5 rounded-xl border border-brand-100">
                              <span className="font-semibold text-brand-800">In simple words: </span>
                              {item.simple_meaning}
                            </div>
                          )}
                        </div>

                        {/* Bottom Source & Audio Action */}
                        <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                          <span className="truncate max-w-[180px]" title={item.source_document}>
                            <i className="fa-solid fa-file-lines text-slate-400 mr-1"></i>
                            {item.source_document ? item.source_document.replace(/^\\d+_/, '').replace(/\\.[^/.]+$/, '') : 'Oncology Sources'}
                          </span>

                          <div className="flex items-center space-x-1.5">
                            <button
                              onClick={() => playSpeech(`${item.term}. ${item.simple_meaning || item.definition}`, 'english')}
                              className="p-1 px-2 rounded bg-slate-100 hover:bg-brand-100 hover:text-brand-800 text-slate-600 transition-colors"
                              title="Listen in English"
                            >
                              <i className="fa-solid fa-volume-high text-[10px]"></i>
                            </button>
                            <button
                              onClick={() => {
                                setInputText(`Explain ${item.term}: ${item.definition}`);
                                setActiveTab('simplify');
                                handleSimplify(`Explain ${item.term}: ${item.definition}`);
                              }}
                              className="p-1 px-2 rounded bg-brand-50 hover:bg-brand-100 text-brand-800 font-semibold transition-colors"
                              title="Send to Simplifier"
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
                
                {/* Guide Hero */}
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 rounded-2xl bg-brand-100 text-brand-700 flex items-center justify-center text-2xl font-bold">
                      <i className="fa-solid fa-user-doctor"></i>
                    </div>
                    <div>
                      <h2 className="text-xl sm:text-2xl font-black text-navy-900">
                        ASHA Worker Oncology Communication & Field Guide
                      </h2>
                      <p className="text-xs sm:text-sm text-slate-500">
                        Practical protocols, CAUTION warning signs, and compassionate counseling guidance for community visits.
                      </p>
                    </div>
                  </div>
                </div>

                {/* CAUTION Warning Signs Protocol */}
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-red-200/80 shadow-sm space-y-4">
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
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">C</div>
                      <div className="font-bold text-xs text-slate-800">Change in bowel or bladder habits</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">মল বা মূত্রের অভ্যাসে দীর্ঘস্থায়ী পরিবর্তন।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">A</div>
                      <div className="font-bold text-xs text-slate-800">A sore that does not heal</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">দীর্ঘদিনেও না সারা কোনো ক্ষত বা ঘা।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">U</div>
                      <div className="font-bold text-xs text-slate-800">Unusual bleeding or discharge</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">অস্বাভাবিক রক্তপাত বা স্রাব নির্গমন।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">T</div>
                      <div className="font-bold text-xs text-slate-800">Thickening or lump in breast / elsewhere</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">স্তন বা শরীরের যে কোনো অংশে চাকা বা পিণ্ড।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">I</div>
                      <div className="font-bold text-xs text-slate-800">Indigestion or difficulty in swallowing</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">খাবার গিলতে কষ্ট বা ক্রমাগত বদহজম।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">O</div>
                      <div className="font-bold text-xs text-slate-800">Obvious change in wart or mole</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">তিল বা আঁচিলের আকার বা রঙের স্পষ্ট পরিবর্তন।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
                      <div className="font-black text-red-700 text-base">N</div>
                      <div className="font-bold text-xs text-slate-800">Nagging cough or hoarseness</div>
                      <p className="text-[11px] text-slate-600 mt-1 font-bn">টানা কাশি বা গলার স্বরের স্থায়ী পরিবর্তন।</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200">
                      <div className="font-black text-amber-700 text-base">Action</div>
                      <div className="font-bold text-xs text-slate-800">Community Referral Protocol</div>
                      <p className="text-[11px] text-slate-600 mt-1">Direct patient to CHC/District Hospital for oncologist consultation.</p>
                    </div>
                  </div>
                </div>

                {/* Compassionate Patient Communication Principles */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-3">
                    <h4 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
                      <i className="fa-solid fa-heart-pulse text-brand-600"></i>
                      <span>Compassionate Counseling Tips</span>
                    </h4>
                    <ul className="text-xs text-slate-600 space-y-2.5">
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-check text-brand-600 mt-0.5"></i>
                        <span><strong>Listen without interrupting:</strong> Acknowledge patient fears and cultural concerns before delivering medical facts.</span>
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
                      <i className="fa-solid fa-hand-holding-medical text-teal-600"></i>
                      <span>Medical Safety & Ethics Guardrails</span>
                    </h4>
                    <ul className="text-xs text-slate-600 space-y-2.5">
                      <li className="flex items-start space-x-2">
                        <i className="fa-solid fa-xmark text-red-500 mt-0.5"></i>
                        <span><strong>Never alter prescription dosages:</strong> Never recommend herbal substitutes or discontinue prescribed chemotherapy regimens.</span>
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

            {/* TAB 5: LOCAL HISTORY */}
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
                        Past medical simplifications from this browser session. Saved locally for offline access.
                      </p>
                    </div>

                    {history.length > 0 && (
                      <button
                        onClick={() => {
                          if (confirm("Clear your local query history?")) {
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
                      <p className="font-bold text-sm text-slate-600">No previous simplifications yet</p>
                      <p className="text-xs text-slate-500 mt-1">Queries you simplify will be saved here for quick reference during community visits.</p>
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
                                Level {item.level}
                              </span>
                            </div>
                          </div>

                          <div className="text-xs font-mono text-slate-500 line-clamp-1">
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
                                setTargetLevel(item.level);
                                setActiveTab('simplify');
                                handleSimplify(item.originalText);
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

          {/* SOURCE INSPECTION MODAL */}
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
                        {selectedSourceModal.document_title || selectedSourceModal.source_document}
                      </h3>
                      <p className="text-[11px] text-slate-500">
                        {selectedSourceModal.section_or_page || 'Clinical reference excerpt'} • Grounding Confidence: {Math.round((selectedSourceModal.similarity_score || 0.8) * 100)}%
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
                    <p className="font-mono text-xs whitespace-pre-wrap">{selectedSourceModal.chunk_text}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="font-semibold text-slate-500 block">Source Document:</span>
                      <span className="font-bold text-slate-800">{selectedSourceModal.source_document}</span>
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
                <span>Simple English & Bengali</span>
                <span>•</span>
                <span className="text-emerald-600 font-semibold">Grounded RAG</span>
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
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"[OncoSathi] Generated frontend index.html successfully at: {INDEX_HTML} ({len(HTML_CONTENT)} bytes)")

if __name__ == "__main__":
    main()
