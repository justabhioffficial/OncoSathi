# -*- coding: utf-8 -*-
"""
Update frontend/public/index.html with:
1. Verified query handling (guaranteed fresh state, no stale responses).
2. Proper dictionary array parsing and fallback field handling.
3. Engaging, professional, modern CSS keyframe animations (fadeInUp, sound wave visualizer, hover-lift, pulsing indicators).
"""
from pathlib import Path

DEST = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\frontend\public\index.html")

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OncoSathi — Cancer Information, Made Easier to Understand</title>
  <meta name="description" content="A calm, reliable oncology communication tool designed for ASHA community health workers in Simple English and Bengali." />

  <!-- Typography: Inter for clean editorial UI & Hind Siliguri for authentic Bengali rendering -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            bn: ['"Hind Siliguri"', 'sans-serif'],
          },
          colors: {
            tealPrimary: '#246B64',
            tealDark: '#1D5751',
            forestGreen: '#263B39',
            mutedSage: '#DCEBE5',
            softSage: '#EEF4EF',
            warmCream: '#F7F5EF',
            pureWhite: '#FFFFFF',
            mutedTerracotta: '#C98269',
            softPeach: '#F1DED4',
            textDark: '#25322F',
            secondaryText: '#6E7C76',
            borderLight: '#E2E8E3',
          }
        }
      }
    }
  </script>

  <!-- React 18, ReactDOM 18 & Babel Standalone -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <!-- Clean Lucide / FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />

  <style>
    body {
      background-color: #F7F5EF;
      color: #25322F;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .font-bengali {
      font-family: 'Hind Siliguri', sans-serif;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #F7F5EF;
    }
    ::-webkit-scrollbar-thumb {
      background: #DCEBE5;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #246B64;
    }

    /* Keyframe Animations */
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(14px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    .animate-fade-in-up {
      animation: fadeInUp 0.35s ease-out forwards;
    }

    @keyframes pulseLive {
      0%, 100% {
        opacity: 1;
        transform: scale(1);
      }
      50% {
        opacity: 0.6;
        transform: scale(1.15);
      }
    }
    .animate-pulse-live {
      animation: pulseLive 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* Animated Soundwave Equalizer for Text-to-Speech */
    @keyframes soundWave {
      0%, 100% { height: 4px; }
      50% { height: 16px; }
    }
    .sound-bar {
      display: inline-block;
      width: 3px;
      background-color: #246B64;
      border-radius: 2px;
      margin: 0 1px;
      animation: soundWave 0.8s ease-in-out infinite;
    }
    .sound-bar-1 { animation-delay: 0.05s; }
    .sound-bar-2 { animation-delay: 0.25s; }
    .sound-bar-3 { animation-delay: 0.15s; }
    .sound-bar-4 { animation-delay: 0.35s; }

    /* Card Micro-interactions */
    .hover-lift {
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .hover-lift:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px -2px rgba(38, 59, 57, 0.07);
      border-color: #246B64;
    }

    button, a {
      transition: all 0.18s ease-in-out;
    }
  </style>
</head>
<body class="bg-warmCream text-textDark min-h-screen flex flex-col">

  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useRef } = React;

    const API_BASE = window.location.origin;

    // Verified Source Documents
    const VERIFIED_SOURCES = [
      {
        id: "src1",
        title: "IJPC Cancer Glossary",
        format: "PDF Document",
        coverage: "Healthcare Definitions & General Terminology",
        termsCount: "43 Terms"
      },
      {
        id: "src2",
        title: "Oncology Terminology Presentation",
        format: "Presentation PDF",
        coverage: "Clinical Oncology, Staging & Metastasis",
        termsCount: "58 Slides"
      },
      {
        id: "src3",
        title: "Medical Terminology Document",
        format: "DOCX Database",
        coverage: "Bilingual English & Bengali Reconciled Glossary",
        termsCount: "82 Records"
      },
      {
        id: "src4",
        title: "Oncology Comprehensive Tables",
        format: "Excel (XLSX)",
        coverage: "Systemic Therapy, Drug Classes & Analogies",
        termsCount: "69 Terms"
      }
    ];

    // Pre-curated verified sample scenarios for ASHA workers
    const SAMPLE_SCENARIOS = [
      {
        label: "What is Metastasis & Spread?",
        text: "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?",
        mode: "ask"
      },
      {
        label: "What is a Biopsy?",
        text: "What is a core needle biopsy and why is histopathology examination necessary?",
        mode: "ask"
      },
      {
        label: "Breast Cancer Lump & Staging",
        text: "Patient presented with a palpable, painless lump in the upper outer quadrant of the right breast. Core needle biopsy confirmed invasive ductal carcinoma. Histopathological examination shows Grade 2 malignancy with negative surgical margins.",
        mode: "simplify"
      },
      {
        label: "Chemotherapy & Side Effects",
        text: "What is chemotherapy, how does systemic medicine work, and what temporary side effects like hair loss (alopecia) should we explain to the patient?",
        mode: "ask"
      }
    ];

    function App() {
      const [activeTab, setActiveTab] = useState('home'); // home, simplify, dictionary, guide, history, about
      const [inputMode, setInputMode] = useState('simplify'); // simplify or ask
      const [inputText, setInputText] = useState('');
      const [targetLang, setTargetLang] = useState('english'); // english or bengali
      const [targetLevel, setTargetLevel] = useState(2); // 1: Basic, 2: Easy, 3: Detailed
      
      const [loading, setLoading] = useState(false);
      const [result, setResult] = useState(null);
      const [error, setError] = useState(null);
      const [copied, setCopied] = useState(false);
      const [feedbackSent, setFeedbackSent] = useState(false);

      // Audio / TTS state
      const [ttsSpeaking, setTtsSpeaking] = useState(false);
      const [ttsPaused, setTtsPaused] = useState(false);
      const [ttsRate, setTtsRate] = useState(1.0);

      // Dictionary state
      const [terms, setTerms] = useState([]);
      const [termSearch, setTermSearch] = useState('');
      const [selectedCategory, setSelectedCategory] = useState('All');
      const [dictLoading, setDictLoading] = useState(false);

      // Session history
      const [history, setHistory] = useState(() => {
        try {
          const saved = localStorage.getItem('oncosathi_session_history');
          return saved ? JSON.parse(saved) : [];
        } catch {
          return [];
        }
      });

      // Source modal state
      const [selectedSourceModal, setSelectedSourceModal] = useState(null);
      const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

      // Sync history to localStorage
      useEffect(() => {
        try {
          localStorage.setItem('oncosathi_session_history', JSON.stringify(history));
        } catch (e) {
          console.error(e);
        }
      }, [history]);

      // Fetch dictionary terms safely
      const loadTerms = async (query = '', cat = 'All') => {
        setDictLoading(true);
        try {
          const params = new URLSearchParams();
          if (query) params.append('q', query);
          if (cat && cat !== 'All') params.append('category', cat);
          params.append('limit', '50');
          const res = await fetch(`${API_BASE}/api/terms/search?${params.toString()}`);
          if (res.ok) {
            const data = await res.json();
            // Robust parsing for either Array or TermSearchResponse
            const list = Array.isArray(data) ? data : (data.results || []);
            setTerms(list);
          }
        } catch (err) {
          console.error('Error fetching terms:', err);
        } finally {
          setDictLoading(false);
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
        }, 220);
        return () => clearTimeout(timer);
      }, [termSearch]);

      // Run live query
      const handleRun = async (overrideText = null, overrideMode = null) => {
        const textToProcess = overrideText !== null ? overrideText : inputText;
        const activeMode = overrideMode !== null ? overrideMode : inputMode;

        if (!textToProcess.trim()) {
          setError(activeMode === 'ask' ? "Please enter a clinical question." : "Please enter or paste medical text to simplify.");
          return;
        }

        // Clean previous states to prevent any stale display
        setError(null);
        setResult(null);
        setLoading(true);
        setFeedbackSent(false);
        setCopied(false);
        stopSpeech();

        const endpoint = activeMode === 'ask' ? '/api/ask' : '/api/simplify';
        const bodyPayload = activeMode === 'ask' 
          ? { question: textToProcess.trim(), target_language: targetLang === 'bengali' ? 'bn' : 'en', level: `level_${targetLevel}` }
          : { text: textToProcess.trim(), target_language: targetLang === 'bengali' ? 'bn' : 'en', level: `level_${targetLevel}` };

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

          // Add to local session history
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
          setHistory(prev => [newEntry, ...prev.slice(0, 19)]);

        } catch (err) {
          setError(err.message || "Failed to communicate with OncoSathi service. Please ensure the server is active.");
        } finally {
          setLoading(false);
        }
      };

      // Native SpeechSynthesis TTS
      const speakText = (text) => {
        if (!('speechSynthesis' in window)) {
          alert('Speech synthesis is not supported in this browser.');
          return;
        }

        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        const isBn = targetLang === 'bengali' || /[\u0980-\u09FF]/.test(text);

        utterance.lang = isBn ? 'bn-BD' : 'en-IN';
        utterance.rate = ttsRate;

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
        setTimeout(() => setCopied(false), 2200);
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
        } catch (e) {
          console.error(e);
        }
      };

      return (
        <div className="flex flex-col min-h-screen">
          
          {/* TOP SOLID NAVBAR */}
          <header className="bg-pureWhite border-b border-borderLight sticky top-0 z-40 transition-shadow duration-200">
            <div className="max-w-6xl mx-auto px-4 sm:px-6">
              <div className="flex items-center justify-between h-16">
                
                {/* Brand Logo & Name */}
                <div 
                  className="flex items-center space-x-3 cursor-pointer select-none group"
                  onClick={() => setActiveTab('home')}
                >
                  <div className="w-9 h-9 rounded-md bg-tealPrimary flex items-center justify-center text-white shadow-sm group-hover:bg-tealDark transition-colors">
                    <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-3.5H7.5v-2H11V7.5h2V11h3.5v2H13v3.5h-2z" />
                    </svg>
                  </div>
                  <div>
                    <div className="flex items-baseline space-x-1.5">
                      <span className="font-bold text-xl text-forestGreen tracking-tight">OncoSathi</span>
                      <span className="text-[10px] font-bold text-tealPrimary uppercase tracking-wider bg-softSage px-1.5 py-0.5 rounded border border-mutedSage hidden sm:inline-flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-tealPrimary animate-pulse-live"></span>
                        ASHA Care
                      </span>
                    </div>
                    <div className="text-[11px] text-secondaryText leading-none hidden md:block">
                      Cancer Information, Made Easier to Understand
                    </div>
                  </div>
                </div>

                {/* Desktop Navigation Links */}
                <nav className="hidden lg:flex items-center space-x-1 text-sm font-medium text-secondaryText">
                  {[
                    { id: 'home', label: 'Home' },
                    { id: 'simplify', label: 'Simplify Information' },
                    { id: 'dictionary', label: 'Oncology Dictionary' },
                    { id: 'guide', label: 'Field Guide' },
                    { id: 'history', label: `History ${history.length > 0 ? `(${history.length})` : ''}` },
                    { id: 'about', label: 'About' },
                  ].map(tab => (
                    <button
                      key={tab.id}
                      onClick={() => { setActiveTab(tab.id); setMobileMenuOpen(false); }}
                      className={`px-3 py-1.5 rounded-md transition-all duration-150 ${
                        activeTab === tab.id
                          ? 'text-tealPrimary bg-softSage font-semibold shadow-sm'
                          : 'hover:text-textDark hover:bg-warmCream'
                      }`}
                    >
                      {tab.label}
                    </button>
                  ))}
                </nav>

                {/* Right: Language Toggle & Primary CTA */}
                <div className="flex items-center space-x-3">
                  <div className="flex bg-warmCream p-1 rounded-md border border-borderLight text-xs font-medium">
                    <button
                      onClick={() => setTargetLang('english')}
                      className={`px-2.5 py-1 rounded transition-colors ${
                        targetLang === 'english'
                          ? 'bg-pureWhite text-tealPrimary font-semibold shadow-sm'
                          : 'text-secondaryText hover:text-textDark'
                      }`}
                    >
                      English
                    </button>
                    <button
                      onClick={() => setTargetLang('bengali')}
                      className={`px-2.5 py-1 rounded transition-colors font-bengali ${
                        targetLang === 'bengali'
                          ? 'bg-tealPrimary text-white font-semibold shadow-sm'
                          : 'text-secondaryText hover:text-textDark'
                      }`}
                    >
                      বাংলা
                    </button>
                  </div>

                  {activeTab !== 'simplify' && (
                    <button
                      onClick={() => setActiveTab('simplify')}
                      className="hidden sm:inline-flex items-center space-x-1.5 bg-tealPrimary hover:bg-tealDark text-white text-xs font-semibold px-3.5 py-2 rounded-md shadow-sm hover:shadow transition-all"
                    >
                      <span>Simplify Text</span>
                      <i className="fa-solid fa-arrow-right text-[10px]"></i>
                    </button>
                  )}

                  {/* Mobile menu toggle */}
                  <button 
                    onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    className="lg:hidden p-2 text-secondaryText hover:text-textDark rounded-md border border-borderLight bg-warmCream"
                    aria-label="Toggle menu"
                  >
                    <i className={`fa-solid ${mobileMenuOpen ? 'fa-xmark' : 'fa-bars'}`}></i>
                  </button>
                </div>

              </div>

              {/* Mobile Drawer */}
              {mobileMenuOpen && (
                <div className="lg:hidden py-3 border-t border-borderLight bg-pureWhite space-y-1 animate-fade-in-up">
                  {[
                    { id: 'home', label: 'Home' },
                    { id: 'simplify', label: 'Simplify Information' },
                    { id: 'dictionary', label: 'Oncology Dictionary' },
                    { id: 'guide', label: 'ASHA Field Guide' },
                    { id: 'history', label: `Session History (${history.length})` },
                    { id: 'about', label: 'About OncoSathi' },
                  ].map(tab => (
                    <button
                      key={tab.id}
                      onClick={() => { setActiveTab(tab.id); setMobileMenuOpen(false); }}
                      className={`w-full text-left px-3 py-2 rounded text-sm font-medium ${
                        activeTab === tab.id
                          ? 'text-tealPrimary bg-softSage font-semibold'
                          : 'text-textDark hover:bg-warmCream'
                      }`}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>
              )}

            </div>
          </header>

          {/* MAIN BODY CONTENT ROUTED BY activeTab */}
          <main className="flex-1">

            {/* TAB 1: HOME PAGE */}
            {activeTab === 'home' && (
              <div className="space-y-16 pb-20 animate-fade-in-up">
                
                {/* HERO SECTION */}
                <section className="pt-8 sm:pt-14 pb-8">
                  <div className="max-w-6xl mx-auto px-4 sm:px-6">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
                      
                      {/* Left: Headline & Editorial Copy */}
                      <div className="lg:col-span-7 space-y-5">
                        
                        <div className="inline-flex items-center space-x-2 bg-mutedSage text-tealDark px-3 py-1 rounded text-xs font-semibold tracking-wide uppercase">
                          <span className="w-1.5 h-1.5 rounded-full bg-tealPrimary animate-pulse-live"></span>
                          <span>Community Healthcare • Cancer Information</span>
                        </div>

                        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-forestGreen tracking-tight leading-[1.18]">
                          Complex medical information. <br />
                          <span className="text-tealPrimary">Easier conversations.</span>
                        </h1>

                        <p className="text-base sm:text-lg text-secondaryText leading-relaxed max-w-xl">
                          OncoSathi helps ASHA community health workers understand complex cancer reports, 
                          biopsy notes, and treatment terminology—translating them into simple, compassionate explanations 
                          in <strong>English</strong> or <strong>বাংলা (Bengali)</strong> for patients and rural families.
                        </p>

                        <div className="pt-2 flex flex-wrap items-center gap-3.5">
                          <button
                            onClick={() => setActiveTab('simplify')}
                            className="bg-tealPrimary hover:bg-tealDark text-white font-semibold px-6 py-3 rounded-md text-sm shadow-sm hover:shadow inline-flex items-center space-x-2 transform hover:-translate-y-0.5"
                          >
                            <span>Simplify Medical Information</span>
                            <i className="fa-solid fa-arrow-right text-xs"></i>
                          </button>

                          <button
                            onClick={() => setActiveTab('dictionary')}
                            className="bg-pureWhite hover:bg-softSage text-textDark border border-borderLight font-semibold px-5 py-3 rounded-md text-sm inline-flex items-center space-x-2 hover-lift"
                          >
                            <i className="fa-solid fa-book-medical text-tealPrimary text-xs"></i>
                            <span>Explore Oncology Dictionary</span>
                          </button>
                        </div>

                        {/* Supported Language & Grounding Callout */}
                        <div className="pt-3 flex flex-wrap items-center gap-4 text-xs text-secondaryText">
                          <div className="flex items-center space-x-1.5 font-medium text-forestGreen">
                            <i className="fa-solid fa-circle-check text-tealPrimary"></i>
                            <span>Available in Simple English & Bengali (সহজ বাংলা)</span>
                          </div>
                          <span className="text-borderLight hidden sm:inline">|</span>
                          <div className="flex items-center space-x-1.5">
                            <i className="fa-solid fa-shield-halved text-mutedTerracotta"></i>
                            <span>Grounded strictly in 4 medical reference sources</span>
                          </div>
                        </div>

                      </div>

                      {/* Right: Authentic Community Healthcare Hero Image */}
                      <div className="lg:col-span-5">
                        <div className="relative p-2 bg-mutedSage rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-300">
                          <img 
                            src="/images/asha_hero.jpg" 
                            alt="Indian community healthcare worker counseling a woman" 
                            className="w-full h-[360px] sm:h-[420px] object-cover rounded-xl"
                            loading="eager"
                          />
                          <div className="mt-2.5 p-3.5 bg-pureWhite rounded-lg border border-borderLight flex items-center space-x-3">
                            <div className="w-8 h-8 rounded bg-softSage text-tealPrimary flex items-center justify-center shrink-0">
                              <i className="fa-solid fa-heart-pulse text-sm"></i>
                            </div>
                            <div className="text-xs">
                              <div className="font-semibold text-textDark">Village Health Companion</div>
                              <div className="text-secondaryText text-[11px]">Empowering compassionate counseling in every household</div>
                            </div>
                          </div>
                        </div>
                      </div>

                    </div>
                  </div>
                </section>

                {/* HOW IT WORKS SECTION */}
                <section className="py-12 bg-pureWhite border-y border-borderLight">
                  <div className="max-w-6xl mx-auto px-4 sm:px-6">
                    
                    <div className="max-w-2xl mb-10">
                      <div className="text-xs font-semibold text-mutedTerracotta uppercase tracking-wider">
                        Workflow Overview
                      </div>
                      <h2 className="text-2xl sm:text-3xl font-bold text-forestGreen mt-1">
                        A simpler way to understand medical information
                      </h2>
                      <p className="text-sm text-secondaryText mt-2">
                        Designed as a fast, reliable companion during home visits, health camps, and hospital escorting.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      
                      {/* Step 01 */}
                      <div className="p-6 rounded-lg bg-warmCream border border-borderLight flex flex-col justify-between hover-lift">
                        <div>
                          <div className="text-2xl font-bold text-tealPrimary mb-2">01</div>
                          <h3 className="text-base font-semibold text-forestGreen mb-1.5">Add information</h3>
                          <p className="text-xs sm:text-sm text-secondaryText leading-relaxed">
                            Paste a complex medical paragraph, biopsy report excerpt, discharge summary, or ask an oncology question directly.
                          </p>
                        </div>
                        <div className="mt-5 pt-4 border-t border-borderLight text-xs text-forestGreen font-medium flex items-center space-x-1.5">
                          <i className="fa-solid fa-file-lines text-tealPrimary"></i>
                          <span>Accepts clinical text or queries</span>
                        </div>
                      </div>

                      {/* Step 02 */}
                      <div className="p-6 rounded-lg bg-warmCream border border-borderLight flex flex-col justify-between hover-lift">
                        <div>
                          <div className="text-2xl font-bold text-tealPrimary mb-2">02</div>
                          <h3 className="text-base font-semibold text-forestGreen mb-1.5">Choose your language</h3>
                          <p className="text-xs sm:text-sm text-secondaryText leading-relaxed">
                            Select between Simple English or authentic Bengali (বাংলা), and pick a literacy level from Basic to Detailed.
                          </p>
                        </div>
                        <div className="mt-5 pt-4 border-t border-borderLight text-xs text-forestGreen font-medium flex items-center space-x-1.5 font-bengali">
                          <i className="fa-solid fa-language text-tealPrimary"></i>
                          <span>সহজ বাংলা ও ৩টি পড়ার স্তর</span>
                        </div>
                      </div>

                      {/* Step 03 */}
                      <div className="p-6 rounded-lg bg-warmCream border border-borderLight flex flex-col justify-between hover-lift">
                        <div>
                          <div className="text-2xl font-bold text-tealPrimary mb-2">03</div>
                          <h3 className="text-base font-semibold text-forestGreen mb-1.5">Understand and explain</h3>
                          <p className="text-xs sm:text-sm text-secondaryText leading-relaxed">
                            Receive an easy explanation, bulleted counseling points, audio read-aloud, and verified medical source citations.
                          </p>
                        </div>
                        <div className="mt-5 pt-4 border-t border-borderLight text-xs text-forestGreen font-medium flex items-center space-x-1.5">
                          <i className="fa-solid fa-volume-high text-tealPrimary"></i>
                          <span>Audio output & source verification</span>
                        </div>
                      </div>

                    </div>

                  </div>
                </section>

                {/* FEATURES SECTION */}
                <section className="py-6">
                  <div className="max-w-6xl mx-auto px-4 sm:px-6 space-y-10">
                    
                    <div className="max-w-2xl">
                      <div className="text-xs font-semibold text-tealPrimary uppercase tracking-wider">
                        Core Capabilities
                      </div>
                      <h2 className="text-2xl sm:text-3xl font-bold text-forestGreen mt-1">
                        Tools designed for everyday healthcare conversations
                      </h2>
                      <p className="text-sm text-secondaryText mt-2">
                        Everything an ASHA worker needs to demystify cancer diagnoses, reassure families, and guide timely care.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                      
                      {/* Left: 4 Feature Highlights */}
                      <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
                        
                        <div className="p-5 rounded-lg bg-pureWhite border border-borderLight space-y-2 hover-lift">
                          <div className="w-8 h-8 rounded bg-softSage text-tealPrimary flex items-center justify-center text-sm font-semibold">
                            <i className="fa-solid fa-feather"></i>
                          </div>
                          <h3 className="font-semibold text-sm text-forestGreen">Medical text simplification</h3>
                          <p className="text-xs text-secondaryText leading-relaxed">
                            Converts intimidating terms like "malignant neoplasm" or "carcinoma" into everyday, dignified language.
                          </p>
                        </div>

                        <div className="p-5 rounded-lg bg-pureWhite border border-borderLight space-y-2 hover-lift">
                          <div className="w-8 h-8 rounded bg-softPeach text-mutedTerracotta flex items-center justify-center text-sm font-semibold">
                            <i className="fa-solid fa-globe"></i>
                          </div>
                          <h3 className="font-semibold text-sm text-forestGreen">English and Bengali</h3>
                          <p className="text-xs text-secondaryText leading-relaxed">
                            Crafted in authentic Bengali script (Hind Siliguri) so community workers can speak naturally with village residents.
                          </p>
                        </div>

                        <div className="p-5 rounded-lg bg-pureWhite border border-borderLight space-y-2 hover-lift">
                          <div className="w-8 h-8 rounded bg-mutedSage text-tealDark flex items-center justify-center text-sm font-semibold">
                            <i className="fa-solid fa-spell-check"></i>
                          </div>
                          <h3 className="font-semibold text-sm text-forestGreen">252+ Oncology terms</h3>
                          <p className="text-xs text-secondaryText leading-relaxed">
                            A searchable clinical reference explaining diagnostic terms, staging, chemotherapy, and surgical concepts.
                          </p>
                        </div>

                        <div className="p-5 rounded-lg bg-pureWhite border border-borderLight space-y-2 hover-lift">
                          <div className="w-8 h-8 rounded bg-softSage text-tealPrimary flex items-center justify-center text-sm font-semibold">
                            <i className="fa-solid fa-headphones"></i>
                          </div>
                          <h3 className="font-semibold text-sm text-forestGreen">Speech audio playback</h3>
                          <p className="text-xs text-secondaryText leading-relaxed">
                            Listen to simplified explanations at adjustable speeds—ideal for bedside counseling or patients with limited literacy.
                          </p>
                        </div>

                      </div>

                      {/* Right: Editorial Image Panel */}
                      <div className="lg:col-span-5">
                        <div className="bg-pureWhite p-3 rounded-2xl border border-borderLight shadow-sm">
                          <img 
                            src="/images/doctor_explaining.jpg" 
                            alt="Healthcare professional explaining medical information" 
                            className="w-full h-[280px] object-cover rounded-xl"
                          />
                          <div className="p-3 text-xs text-secondaryText">
                            <div className="font-semibold text-textDark">Evidence-Based & Grounded</div>
                            <div>Retrieved directly from verified oncology references, eliminating artificial hallucinations.</div>
                          </div>
                        </div>
                      </div>

                    </div>

                  </div>
                </section>

                {/* FOUR VERIFIED MEDICAL SOURCE DOCUMENTS */}
                <section className="py-12 bg-pureWhite border-y border-borderLight">
                  <div className="max-w-6xl mx-auto px-4 sm:px-6 space-y-8">
                    
                    <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                      <div>
                        <div className="text-xs font-semibold text-tealPrimary uppercase tracking-wider">
                          Medical Knowledge Base
                        </div>
                        <h2 className="text-2xl sm:text-3xl font-bold text-forestGreen mt-1">
                          Verified Medical Source Documents
                        </h2>
                        <p className="text-sm text-secondaryText mt-1 max-w-xl">
                          OncoSathi does not query random internet sources. All simplifications are strictly grounded in 4 primary oncology references.
                        </p>
                      </div>
                      <div className="text-xs font-semibold bg-softSage text-tealPrimary px-3 py-1.5 rounded border border-mutedSage shrink-0 self-start md:self-auto">
                        419 Knowledge Chunks • 252 Terms
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                      {VERIFIED_SOURCES.map(src => (
                        <div key={src.id} className="p-4 rounded-lg bg-warmCream border border-borderLight flex flex-col justify-between hover-lift">
                          <div className="space-y-2">
                            <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-pureWhite text-forestGreen border border-borderLight">
                              {src.format}
                            </span>
                            <h3 className="font-semibold text-sm text-forestGreen">{src.title}</h3>
                            <p className="text-xs text-secondaryText">{src.coverage}</p>
                          </div>
                          <div className="mt-4 pt-3 border-t border-borderLight flex justify-between items-center text-[11px] text-tealPrimary font-medium">
                            <span>{src.termsCount}</span>
                            <i className="fa-solid fa-check text-xs"></i>
                          </div>
                        </div>
                      ))}
                    </div>

                  </div>
                </section>

                {/* BOTTOM CTA CALLOUT BANNER */}
                <section className="pt-4">
                  <div className="max-w-6xl mx-auto px-4 sm:px-6">
                    <div className="bg-forestGreen text-white p-8 sm:p-12 rounded-2xl shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
                      <div className="space-y-2 max-w-xl">
                        <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
                          Ready to simplify an oncology report?
                        </h2>
                        <p className="text-sm text-mutedSage leading-relaxed">
                          Paste your first medical paragraph or clinical question to generate an easy-to-understand explanation for community counseling.
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-3 shrink-0">
                        <button
                          onClick={() => setActiveTab('simplify')}
                          className="bg-tealPrimary hover:bg-tealDark text-white font-semibold px-6 py-3 rounded-md text-sm shadow-sm hover:shadow"
                        >
                          Open Simplifier
                        </button>
                        <button
                          onClick={() => setActiveTab('guide')}
                          className="bg-transparent hover:bg-white/10 text-white border border-mutedSage/40 font-semibold px-5 py-3 rounded-md text-sm"
                        >
                          View Field Guide
                        </button>
                      </div>
                    </div>
                  </div>
                </section>

              </div>
            )}

            {/* TAB 2: SIMPLIFICATION WORKSPACE */}
            {activeTab === 'simplify' && (
              <div className="py-8 sm:py-12 animate-fade-in-up">
                <div className="max-w-5xl mx-auto px-4 sm:px-6 space-y-8">
                  
                  {/* Header */}
                  <div>
                    <div className="inline-flex items-center space-x-1.5 text-xs font-semibold text-tealPrimary uppercase tracking-wider mb-1">
                      <span>Clinical Workspace</span>
                    </div>
                    <h1 className="text-2xl sm:text-3xl font-bold text-forestGreen">
                      Simplify Medical Information
                    </h1>
                    <p className="text-sm text-secondaryText mt-1">
                      Turn complex cancer-related information into explanations that are easier to understand and share.
                    </p>
                  </div>

                  {/* Mode Selector Toggle: Simplify Text vs Ask a Question */}
                  <div className="flex bg-pureWhite p-1 rounded-lg border border-borderLight max-w-md shadow-sm">
                    <button
                      onClick={() => setInputMode('simplify')}
                      className={`flex-1 py-2 text-xs sm:text-sm font-semibold rounded-md transition-all ${
                        inputMode === 'simplify'
                          ? 'bg-tealPrimary text-white shadow-sm'
                          : 'text-secondaryText hover:text-textDark'
                      }`}
                    >
                      <i className="fa-solid fa-file-medical mr-1.5"></i>
                      Simplify Medical Text
                    </button>
                    <button
                      onClick={() => setInputMode('ask')}
                      className={`flex-1 py-2 text-xs sm:text-sm font-semibold rounded-md transition-all ${
                        inputMode === 'ask'
                          ? 'bg-tealPrimary text-white shadow-sm'
                          : 'text-secondaryText hover:text-textDark'
                      }`}
                    >
                      <i className="fa-solid fa-circle-question mr-1.5"></i>
                      Ask a Question
                    </button>
                  </div>

                  {/* Main Input Panel (Solid White Surface) */}
                  <div className="bg-pureWhite rounded-xl border border-borderLight p-5 sm:p-6 shadow-sm space-y-4">
                    
                    <div className="flex justify-between items-center text-xs">
                      <label className="font-semibold text-textDark">
                        {inputMode === 'ask' ? 'Enter clinical question:' : 'Enter or paste medical report excerpt:'}
                      </label>
                      <div className="flex items-center space-x-3 text-secondaryText">
                        <span>{inputText.length} characters</span>
                        {inputText.length > 0 && (
                          <button 
                            onClick={() => { setInputText(''); setResult(null); setError(null); }}
                            className="hover:text-mutedTerracotta font-medium underline"
                          >
                            Clear
                          </button>
                        )}
                      </div>
                    </div>

                    <textarea
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      rows={5}
                      placeholder={
                        inputMode === 'ask'
                          ? "e.g. What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?"
                          : "e.g. Patient presented with a 2.5cm palpable lump in breast. Biopsy confirmed invasive ductal carcinoma, Grade II. Advised adjuvant chemotherapy..."
                      }
                      className="w-full p-3.5 text-sm rounded-md border border-borderLight focus:outline-none focus:border-tealPrimary focus:ring-1 focus:ring-tealPrimary bg-warmCream/30 text-textDark leading-relaxed placeholder:text-secondaryText/60"
                    />

                    {/* Quick Example Chips */}
                    <div className="pt-1">
                      <div className="text-xs font-semibold text-secondaryText mb-2">Try an example case:</div>
                      <div className="flex flex-wrap gap-2">
                        {SAMPLE_SCENARIOS.map((scenario, idx) => (
                          <button
                            key={idx}
                            onClick={() => {
                              setInputText(scenario.text);
                              setInputMode(scenario.mode);
                              setResult(null);
                              setError(null);
                            }}
                            className="text-xs bg-softSage hover:bg-mutedSage text-tealDark px-3 py-1.5 rounded-md border border-borderLight font-medium transition-all hover:-translate-y-0.5"
                          >
                            <i className="fa-solid fa-arrow-turn-down text-[10px] mr-1 text-tealPrimary"></i>
                            {scenario.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Controls Row: Language, Level & Action */}
                    <div className="pt-4 border-t border-borderLight flex flex-col md:flex-row md:items-center justify-between gap-4">
                      
                      {/* Language & Literacy Level Controls */}
                      <div className="flex flex-wrap items-center gap-3">
                        
                        {/* Language Selection */}
                        <div className="flex bg-warmCream p-1 rounded-md border border-borderLight text-xs font-medium">
                          <button
                            onClick={() => setTargetLang('english')}
                            className={`px-3 py-1.5 rounded transition-colors ${
                              targetLang === 'english'
                                ? 'bg-pureWhite text-tealPrimary font-semibold shadow-sm'
                                : 'text-secondaryText hover:text-textDark'
                            }`}
                          >
                            English
                          </button>
                          <button
                            onClick={() => setTargetLang('bengali')}
                            className={`px-3 py-1.5 rounded transition-colors font-bengali ${
                              targetLang === 'bengali'
                                ? 'bg-tealPrimary text-white font-semibold shadow-sm'
                                : 'text-secondaryText hover:text-textDark'
                            }`}
                          >
                            বাংলা (Bengali)
                          </button>
                        </div>

                        {/* Reading Level Selection */}
                        <div className="flex items-center space-x-1 text-xs">
                          <span className="text-secondaryText mr-1 hidden sm:inline">Level:</span>
                          {[
                            { lvl: 1, label: 'Basic' },
                            { lvl: 2, label: 'Easy' },
                            { lvl: 3, label: 'Detailed' },
                          ].map(item => (
                            <button
                              key={item.lvl}
                              onClick={() => setTargetLevel(item.lvl)}
                              className={`px-2.5 py-1.5 rounded border text-xs font-medium transition-all ${
                                targetLevel === item.lvl
                                  ? 'bg-forestGreen text-white border-forestGreen font-semibold shadow-sm'
                                  : 'bg-pureWhite text-secondaryText border-borderLight hover:text-textDark'
                              }`}
                            >
                              {item.label}
                            </button>
                          ))}
                        </div>

                      </div>

                      {/* Primary Simplify Action Button */}
                      <button
                        onClick={() => handleRun()}
                        disabled={loading}
                        className={`bg-tealPrimary hover:bg-tealDark text-white font-semibold px-6 py-2.5 rounded-md text-sm shadow-sm inline-flex items-center justify-center space-x-2 shrink-0 transform active:scale-95 transition-all ${
                          loading ? 'opacity-70 cursor-not-allowed' : ''
                        }`}
                      >
                        {loading ? (
                          <>
                            <i className="fa-solid fa-circle-notch fa-spin text-xs"></i>
                            <span>Retrieving & Simplifying...</span>
                          </>
                        ) : (
                          <>
                            <span>{inputMode === 'ask' ? 'Ask Question' : 'Simplify Information'}</span>
                            <i className="fa-solid fa-paper-plane text-xs"></i>
                          </>
                        )}
                      </button>

                    </div>

                  </div>

                  {/* Animated Loading Shimmer State */}
                  {loading && (
                    <div className="bg-pureWhite rounded-xl border border-borderLight p-8 text-center space-y-4 animate-fade-in-up shadow-sm">
                      <div className="flex justify-center items-center space-x-2 text-tealPrimary">
                        <span className="w-2.5 h-2.5 rounded-full bg-tealPrimary animate-bounce"></span>
                        <span className="w-2.5 h-2.5 rounded-full bg-tealPrimary animate-bounce [animation-delay:0.2s]"></span>
                        <span className="w-2.5 h-2.5 rounded-full bg-tealPrimary animate-bounce [animation-delay:0.4s]"></span>
                      </div>
                      <div className="text-sm font-semibold text-forestGreen">Searching 419 medical chunks & synthesizing explanation...</div>
                      <p className="text-xs text-secondaryText max-w-sm mx-auto">
                        Grounded in IJPC Cancer Glossary, Oncology Presentation, Terminology DOCX, and Clinical Tables.
                      </p>
                    </div>
                  )}

                  {/* Error Notification */}
                  {error && (
                    <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 text-sm flex items-start space-x-2 animate-fade-in-up">
                      <i className="fa-solid fa-triangle-exclamation mt-0.5 text-red-600"></i>
                      <span>{error}</span>
                    </div>
                  )}

                  {/* RESULTS DISPLAY PANEL */}
                  {result && !loading && (
                    <div className="bg-pureWhite rounded-xl border border-borderLight p-6 sm:p-8 shadow-sm space-y-6 animate-fade-in-up">
                      
                      {/* Result Header */}
                      <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-borderLight">
                        <div className="flex items-center space-x-2">
                          <span className="text-xs font-semibold px-2.5 py-1 rounded bg-softSage text-tealDark border border-mutedSage">
                            {result.language === 'bengali' || targetLang === 'bengali' ? 'বাংলা সংস্করণ' : 'Simple English'}
                          </span>
                          <span className="text-xs text-secondaryText">
                            {result.reading_level_label || `Level ${targetLevel}`}
                          </span>
                          {result.confidence_score && (
                            <span className="text-[11px] text-tealPrimary font-medium">
                              • {(result.confidence_score * 100).toFixed(0)}% Source Confidence
                            </span>
                          )}
                        </div>

                        {/* Top Utility Actions: Copy & Listen */}
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => copyToClipboard(result.simplified_text || result.answer)}
                            className="text-xs text-secondaryText hover:text-textDark px-2.5 py-1 rounded border border-borderLight hover:bg-warmCream inline-flex items-center space-x-1"
                          >
                            <i className={`fa-solid ${copied ? 'fa-check text-tealPrimary' : 'fa-copy'}`}></i>
                            <span>{copied ? 'Copied' : 'Copy'}</span>
                          </button>
                        </div>
                      </div>

                      {/* Main Simplified Explanation Text (18px, comfortable reading) */}
                      <div className="space-y-3">
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-tealPrimary">
                          Patient-Facing Explanation
                        </h3>
                        <div className={`text-base sm:text-[18px] leading-[1.75] text-textDark whitespace-pre-line ${targetLang === 'bengali' || result.language === 'bengali' ? 'font-bengali' : ''}`}>
                          {result.simplified_text || result.answer}
                        </div>
                      </div>

                      {/* Animated Audio Player Bar */}
                      <div className="p-3.5 rounded-lg bg-warmCream border border-borderLight flex flex-wrap items-center justify-between gap-3">
                        <div className="flex items-center space-x-3">
                          {!ttsSpeaking ? (
                            <button
                              onClick={() => speakText(result.simplified_text || result.answer)}
                              className="w-8 h-8 rounded bg-tealPrimary text-white flex items-center justify-center text-xs hover:bg-tealDark shadow-sm transform hover:scale-105"
                              title="Listen to explanation"
                            >
                              <i className="fa-solid fa-play ml-0.5"></i>
                            </button>
                          ) : (
                            <div className="flex items-center space-x-1.5">
                              <button
                                onClick={pauseSpeech}
                                className="w-8 h-8 rounded bg-forestGreen text-white flex items-center justify-center text-xs shadow-sm"
                                title={ttsPaused ? "Resume" : "Pause"}
                              >
                                <i className={`fa-solid ${ttsPaused ? 'fa-play' : 'fa-pause'}`}></i>
                              </button>
                              <button
                                onClick={stopSpeech}
                                className="w-8 h-8 rounded bg-white text-secondaryText border border-borderLight flex items-center justify-center text-xs hover:text-red-700"
                                title="Stop audio"
                              >
                                <i className="fa-solid fa-stop"></i>
                              </button>
                            </div>
                          )}

                          <div className="text-xs">
                            <div className="flex items-center space-x-2">
                              <span className="font-semibold text-textDark">
                                {ttsSpeaking ? (ttsPaused ? 'Audio Paused' : 'Reading Aloud...') : 'Listen to this explanation'}
                              </span>
                              {/* Audio Wave Visualizer */}
                              {ttsSpeaking && !ttsPaused && (
                                <span className="inline-flex items-center h-4">
                                  <span className="sound-bar sound-bar-1"></span>
                                  <span className="sound-bar sound-bar-2"></span>
                                  <span className="sound-bar sound-bar-3"></span>
                                  <span className="sound-bar sound-bar-4"></span>
                                </span>
                              )}
                            </div>
                            <div className="text-[11px] text-secondaryText">
                              {targetLang === 'bengali' ? 'বাংলা কন্ঠস্বর (Bengali TTS)' : 'Indian English Voice'}
                            </div>
                          </div>
                        </div>

                        {/* Speed Controls */}
                        <div className="flex items-center space-x-1 text-xs">
                          <span className="text-secondaryText text-[11px] mr-1">Speed:</span>
                          {[0.8, 1.0, 1.2].map(speed => (
                            <button
                              key={speed}
                              onClick={() => setTtsRate(speed)}
                              className={`px-2 py-0.5 rounded text-[11px] font-medium border transition-colors ${
                                ttsRate === speed
                                  ? 'bg-tealPrimary text-white border-tealPrimary font-semibold'
                                  : 'bg-pureWhite text-secondaryText border-borderLight hover:text-textDark'
                              }`}
                            >
                              {speed}x
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Key Points for Patient Counseling */}
                      {result.key_points && result.key_points.length > 0 && (
                        <div className="p-4 rounded-lg bg-softSage border border-mutedSage space-y-2.5">
                          <h4 className="text-xs font-semibold text-forestGreen uppercase tracking-wider">
                            Key Counseling Takeaways
                          </h4>
                          <ul className="space-y-1.5 text-xs sm:text-sm text-textDark">
                            {result.key_points.map((pt, idx) => (
                              <li key={idx} className="flex items-start space-x-2">
                                <span className="text-tealPrimary font-bold mt-0.5">•</span>
                                <span className={targetLang === 'bengali' ? 'font-bengali' : ''}>{pt}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Medical Terms Explained */}
                      {result.terms_explained && result.terms_explained.length > 0 && (
                        <div className="space-y-3">
                          <h4 className="text-xs font-semibold text-tealPrimary uppercase tracking-wider">
                            Difficult Medical Terms Explained
                          </h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {result.terms_explained.map((termItem, idx) => (
                              <div key={idx} className="p-3.5 rounded-lg bg-warmCream border border-borderLight space-y-1 hover-lift">
                                <div className="flex justify-between items-start">
                                  <span className="font-semibold text-xs text-forestGreen">{termItem.term}</span>
                                  {termItem.category && (
                                    <span className="text-[10px] bg-pureWhite text-secondaryText px-1.5 py-0.5 rounded border border-borderLight">
                                      {termItem.category}
                                    </span>
                                  )}
                                </div>
                                {termItem.bengali_term && (
                                  <div className="text-xs font-medium text-tealPrimary font-bengali">
                                    বাংলা: {termItem.bengali_term}
                                  </div>
                                )}
                                <p className="text-xs text-secondaryText leading-relaxed">
                                  {termItem.simple_meaning || termItem.definition || termItem.original_medical_definition}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Grounded Source Citations */}
                      {result.sources && result.sources.length > 0 && (
                        <div className="space-y-3 pt-2">
                          <div className="flex items-center justify-between">
                            <h4 className="text-xs font-semibold text-forestGreen uppercase tracking-wider">
                              Verified Source Citations ({result.sources.length})
                            </h4>
                            <span className="text-[11px] text-secondaryText">Strictly retrieved from indexed medical sources</span>
                          </div>
                          
                          <div className="flex flex-wrap gap-2">
                            {result.sources.map((src, idx) => (
                              <button
                                key={idx}
                                onClick={() => setSelectedSourceModal(src)}
                                className="text-left p-2.5 rounded-md bg-warmCream hover:bg-softSage border border-borderLight transition-all text-xs flex items-center space-x-2 hover-lift"
                              >
                                <i className="fa-solid fa-file-shield text-tealPrimary text-xs"></i>
                                <div>
                                  <div className="font-semibold text-textDark text-[11px]">{src.document_name}</div>
                                  <div className="text-[10px] text-secondaryText">{src.page_or_slide || src.section}</div>
                                </div>
                                <i className="fa-solid fa-magnifying-glass text-[10px] text-secondaryText ml-1"></i>
                              </button>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Feedback & Actions */}
                      <div className="pt-4 border-t border-borderLight flex flex-wrap items-center justify-between gap-3 text-xs text-secondaryText">
                        <div>
                          <span>Was this explanation helpful for your visit? </span>
                          {!feedbackSent ? (
                            <span className="space-x-1.5 ml-1">
                              <button
                                onClick={() => handleFeedback(true)}
                                className="px-2 py-0.5 rounded border border-borderLight hover:bg-softSage hover:text-tealPrimary"
                              >
                                <i className="fa-regular fa-thumbs-up mr-1"></i>Yes
                              </button>
                              <button
                                onClick={() => handleFeedback(false)}
                                className="px-2 py-0.5 rounded border border-borderLight hover:bg-red-50 hover:text-red-700"
                              >
                                <i className="fa-regular fa-thumbs-down mr-1"></i>No
                              </button>
                            </span>
                          ) : (
                            <span className="text-tealPrimary font-medium ml-1">✓ Thank you for your feedback!</span>
                          )}
                        </div>

                        <button
                          onClick={() => { setResult(null); setInputText(''); }}
                          className="text-tealPrimary hover:text-tealDark font-semibold hover:underline"
                        >
                          Simplify another case →
                        </button>
                      </div>

                    </div>
                  )}

                </div>
              </div>
            )}

            {/* TAB 3: ONCOLOGY DICTIONARY */}
            {activeTab === 'dictionary' && (
              <div className="py-8 sm:py-12 animate-fade-in-up">
                <div className="max-w-5xl mx-auto px-4 sm:px-6 space-y-6">
                  
                  {/* Header */}
                  <div>
                    <div className="text-xs font-semibold text-tealPrimary uppercase tracking-wider mb-1">
                      Reference Library
                    </div>
                    <h1 className="text-2xl sm:text-3xl font-bold text-forestGreen">
                      Oncology Dictionary
                    </h1>
                    <p className="text-sm text-secondaryText mt-1">
                      Understand cancer-related medical words in everyday language. 252+ terms reconciled across 4 sources.
                    </p>
                  </div>

                  {/* Search and Category Filter Bar */}
                  <div className="bg-pureWhite p-4 rounded-xl border border-borderLight shadow-sm space-y-3">
                    <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
                      
                      {/* Search Input */}
                      <div className="md:col-span-8 relative">
                        <i className="fa-solid fa-magnifying-glass absolute left-3.5 top-3 text-secondaryText text-xs"></i>
                        <input
                          type="text"
                          value={termSearch}
                          onChange={(e) => setTermSearch(e.target.value)}
                          placeholder="Search terminology (e.g. Biopsy, Carcinoma, Metastasis, বায়োপসি)..."
                          className="w-full pl-9 pr-8 py-2 text-sm rounded-md border border-borderLight focus:outline-none focus:border-tealPrimary bg-warmCream/30 text-textDark"
                        />
                        {termSearch && (
                          <button
                            onClick={() => setTermSearch('')}
                            className="absolute right-3 top-2.5 text-secondaryText hover:text-textDark text-xs"
                          >
                            <i className="fa-solid fa-xmark"></i>
                          </button>
                        )}
                      </div>

                      {/* Category Dropdown */}
                      <div className="md:col-span-4">
                        <select
                          value={selectedCategory}
                          onChange={(e) => setSelectedCategory(e.target.value)}
                          className="w-full py-2 px-3 text-sm rounded-md border border-borderLight focus:outline-none focus:border-tealPrimary bg-pureWhite text-textDark"
                        >
                          <option value="All">All Categories (252 terms)</option>
                          <option value="General Oncology">General Oncology</option>
                          <option value="Diagnosis & Pathology">Diagnosis & Pathology</option>
                          <option value="Treatment & Chemotherapy">Treatment & Chemotherapy</option>
                          <option value="Anatomy & Staging">Anatomy & Staging</option>
                        </select>
                      </div>

                    </div>
                  </div>

                  {/* Terms List / Reference Table */}
                  {dictLoading ? (
                    <div className="p-12 text-center text-secondaryText bg-pureWhite rounded-xl border border-borderLight text-sm animate-fade-in-up">
                      <i className="fa-solid fa-circle-notch fa-spin mr-2 text-tealPrimary"></i>
                      Searching oncology terms...
                    </div>
                  ) : terms.length === 0 ? (
                    <div className="p-12 text-center text-secondaryText bg-pureWhite rounded-xl border border-borderLight text-sm animate-fade-in-up">
                      No oncology terms matched &quot;{termSearch}&quot;. Try terms like biopsy, stage, metastasis, or tumor.
                    </div>
                  ) : (
                    <div className="space-y-3 animate-fade-in-up">
                      <div className="text-xs text-secondaryText font-medium px-1">
                        Showing {terms.length} medical terms
                      </div>

                      <div className="bg-pureWhite rounded-xl border border-borderLight divide-y divide-borderLight shadow-sm">
                        {terms.map((item) => (
                          <div key={item.id} className="p-5 hover:bg-warmCream/30 transition-colors space-y-2 hover-lift">
                            <div className="flex flex-wrap justify-between items-start gap-2">
                              <div>
                                <h3 className="font-bold text-base text-forestGreen">{item.term}</h3>
                                {item.bengali_term && (
                                  <div className="text-sm font-semibold text-tealPrimary font-bengali mt-0.5">
                                    বাংলা: {item.bengali_term}
                                  </div>
                                )}
                              </div>
                              <span className="text-[11px] font-medium bg-softSage text-tealDark px-2 py-0.5 rounded border border-mutedSage shrink-0">
                                {item.category}
                              </span>
                            </div>

                            <div className="text-xs text-secondaryText leading-relaxed">
                              <strong className="text-textDark font-semibold">Clinical Definition: </strong>
                              {item.definition || item.medical_definition}
                            </div>

                            {(item.simple_meaning || item.simplified_en) && (
                              <div className="p-2.5 rounded-md bg-softSage/60 border border-mutedSage text-xs text-tealDark leading-relaxed">
                                <strong className="font-semibold text-forestGreen">How to explain to family: </strong>
                                {item.simple_meaning || item.simplified_en}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                </div>
              </div>
            )}

            {/* TAB 4: ASHA FIELD GUIDE */}
            {activeTab === 'guide' && (
              <div className="py-8 sm:py-12 animate-fade-in-up">
                <div className="max-w-5xl mx-auto px-4 sm:px-6 space-y-8">
                  
                  <div>
                    <div className="text-xs font-semibold text-tealPrimary uppercase tracking-wider mb-1">
                      Field Protocols
                    </div>
                    <h1 className="text-2xl sm:text-3xl font-bold text-forestGreen">
                      ASHA Oncology Field Guide
                    </h1>
                    <p className="text-sm text-secondaryText mt-1">
                      Standardized counseling protocols, CAUTION early warning signs, and patient navigation guidelines.
                    </p>
                  </div>

                  {/* CAUTION Early Warning Signs */}
                  <div className="bg-pureWhite rounded-xl border border-borderLight p-6 sm:p-8 shadow-sm space-y-6">
                    <div>
                      <span className="text-xs font-semibold uppercase tracking-wider px-2.5 py-1 rounded bg-red-50 text-red-800 border border-red-200">
                        Early Detection Protocol
                      </span>
                      <h2 className="text-xl font-bold text-forestGreen mt-2">
                        The C-A-U-T-I-O-N Warning Signs
                      </h2>
                      <p className="text-xs text-secondaryText mt-1">
                        If a community resident exhibits any of these 7 symptoms persisting over 2–3 weeks, advise prompt evaluation by a Medical Officer.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                      {[
                        { letter: 'C', title: 'Change in bowel or bladder habits', bengali: 'মল বা মূত্রের অভ্যাসে দীর্ঘস্থায়ী পরিবর্তন।', detail: 'Chronic diarrhea, constipation, or change in stool caliber lasting weeks.' },
                        { letter: 'A', title: 'A sore that does not heal', bengali: 'দীর্ঘদিনেও না সারা কোনো ক্ষত বা ঘা।', detail: 'Oral sores, skin ulcers, or lesions that do not heal with ordinary ointment.' },
                        { letter: 'U', title: 'Unusual bleeding or discharge', bengali: 'অস্বাভাবিক রক্তপাত বা স্রাব নির্গমন।', detail: 'Post-menopausal bleeding, bleeding between cycles, blood in sputum or stool.' },
                        { letter: 'T', title: 'Thickening or lump in breast or elsewhere', bengali: 'স্তন বা শরীরের যে কোনো অংশে শক্ত চাকা বা পিণ্ড।', detail: 'Painless hard lump in breast, underarm, groin, or neck lymph nodes.' },
                        { letter: 'I', title: 'Indigestion or difficulty in swallowing', bengali: 'খাবার গিলতে কষ্ট বা বদহজম।', detail: 'Persistent dysphagia (food getting stuck), feeling full after small meals.' },
                        { letter: 'O', title: 'Obvious change in wart or mole', bengali: 'তিল বা আঁচিলের আকার, রং বা আকারে অস্বাভাবিক পরিবর্তন।', detail: 'Asymmetry, border irregularity, color change, diameter > 6mm.' },
                        { letter: 'N', title: 'Nagging cough or hoarseness', bengali: 'টানা কাশি বা গলার স্বরের স্থায়ী কর্কশতা।', detail: 'Cough lasting more than 3 weeks without infection, persistent voice change.' },
                      ].map((item, idx) => (
                        <div key={idx} className="p-3.5 rounded-lg border border-borderLight bg-warmCream/60 flex items-start space-x-3 hover-lift">
                          <div className="w-8 h-8 rounded bg-tealPrimary text-white font-bold flex items-center justify-center shrink-0 text-sm">
                            {item.letter}
                          </div>
                          <div className="space-y-1">
                            <div className="font-semibold text-xs text-forestGreen">{item.title}</div>
                            <div className="text-xs text-tealPrimary font-medium font-bengali">{item.bengali}</div>
                            <p className="text-[11px] text-secondaryText leading-relaxed">{item.detail}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Compassionate Counseling Guidelines */}
                  <div className="bg-pureWhite rounded-xl border border-borderLight p-6 sm:p-8 shadow-sm space-y-4">
                    <h3 className="text-lg font-bold text-forestGreen">
                      Compassionate Communication Principles
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {[
                        { title: '1. Establish Trust & Listen Actively', desc: 'Patients in rural areas frequently view cancer as an immediate death sentence. Allow them to express their fears completely before introducing medical terms.' },
                        { title: '2. Demystify the Word "Biopsy"', desc: 'Many believe taking a sample makes cancer spread faster. Clarify: "A biopsy is simply a tiny sample to identify the exact germ so doctors know the right medicine."' },
                        { title: '3. Explain Staging Constructively', desc: 'Stage 1 or 2 means the condition is localized and has very high cure rates. Even for advanced stages, treatment eases suffering and extends comfortable life.' },
                        { title: '4. Escort to Primary Health Centre (PHC)', desc: 'Never prescribe cancer treatments yourself. Help the patient arrange health cards (Swasthya Sathi / Ayushman Bharat) and consult the medical officer.' },
                      ].map((card, idx) => (
                        <div key={idx} className="p-4 rounded-lg bg-softSage/50 border border-borderLight space-y-1.5 hover-lift">
                          <h4 className="font-semibold text-xs text-forestGreen">{card.title}</h4>
                          <p className="text-xs text-secondaryText leading-relaxed">{card.desc}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                </div>
              </div>
            )}

            {/* TAB 5: HISTORY PAGE */}
            {activeTab === 'history' && (
              <div className="py-8 sm:py-12 animate-fade-in-up">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 space-y-6">
                  
                  <div className="flex justify-between items-center pb-4 border-b border-borderLight">
                    <div>
                      <div className="text-xs font-semibold text-tealPrimary uppercase tracking-wider mb-1">
                        Activity Log
                      </div>
                      <h1 className="text-2xl sm:text-3xl font-bold text-forestGreen">
                        Session History
                      </h1>
                      <p className="text-sm text-secondaryText mt-0.5">
                        Previous medical simplifications from your current browser session.
                      </p>
                    </div>

                    {history.length > 0 && (
                      <button
                        onClick={() => {
                          if (confirm('Clear all session history?')) {
                            setHistory([]);
                          }
                        }}
                        className="text-xs text-mutedTerracotta hover:text-red-700 font-semibold px-3 py-1.5 rounded border border-mutedTerracotta/40 hover:bg-red-50"
                      >
                        Clear History
                      </button>
                    )}
                  </div>

                  {history.length === 0 ? (
                    <div className="p-12 text-center bg-pureWhite rounded-xl border border-borderLight space-y-3">
                      <div className="w-12 h-12 rounded-full bg-softSage text-tealPrimary mx-auto flex items-center justify-center text-lg">
                        <i className="fa-solid fa-clock-rotate-left"></i>
                      </div>
                      <h3 className="text-base font-semibold text-forestGreen">No history saved yet</h3>
                      <p className="text-xs text-secondaryText max-w-sm mx-auto">
                        When you simplify medical text or ask clinical questions, your results will appear here for quick reference during your visit.
                      </p>
                      <button
                        onClick={() => setActiveTab('simplify')}
                        className="mt-2 text-xs font-semibold text-tealPrimary hover:underline"
                      >
                        Go to Simplifier →
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {history.map((item) => (
                        <div key={item.id} className="p-4 rounded-lg bg-pureWhite border border-borderLight space-y-2 shadow-sm hover-lift">
                          <div className="flex justify-between items-center text-xs text-secondaryText">
                            <span>{item.timestamp}</span>
                            <span className="font-semibold bg-softSage text-tealDark px-2 py-0.5 rounded border border-mutedSage capitalize">
                              {item.language} • {item.level}
                            </span>
                          </div>
                          
                          <div className="text-xs text-secondaryText line-clamp-1">
                            <strong className="text-textDark">Original: </strong>
                            {item.originalText}
                          </div>

                          <div className="text-xs text-textDark line-clamp-2 leading-relaxed">
                            <strong className="text-tealPrimary">Simplified: </strong>
                            {item.simplifiedText}
                          </div>

                          <div className="pt-2 flex justify-between items-center text-xs">
                            <button
                              onClick={() => {
                                setInputText(item.originalText);
                                setActiveTab('simplify');
                              }}
                              className="text-tealPrimary hover:text-tealDark font-semibold hover:underline"
                            >
                              Load in Simplifier →
                            </button>
                            <span className="text-[11px] text-secondaryText">{item.sourcesCount} sources cited</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                </div>
              </div>
            )}

            {/* TAB 6: ABOUT PAGE */}
            {activeTab === 'about' && (
              <div className="py-8 sm:py-12 animate-fade-in-up">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 space-y-8">
                  
                  <div>
                    <div className="text-xs font-semibold text-tealPrimary uppercase tracking-wider mb-1">
                      Platform Overview
                    </div>
                    <h1 className="text-2xl sm:text-3xl font-bold text-forestGreen">
                      About OncoSathi
                    </h1>
                    <p className="text-sm text-secondaryText mt-1">
                      Making cancer information easier to understand and share in community healthcare.
                    </p>
                  </div>

                  {/* The Problem & The Purpose */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-6 rounded-xl bg-pureWhite border border-borderLight space-y-2.5 hover-lift">
                      <div className="w-8 h-8 rounded bg-softPeach text-mutedTerracotta flex items-center justify-center text-sm font-semibold">
                        <i className="fa-solid fa-triangle-exclamation"></i>
                      </div>
                      <h3 className="text-base font-bold text-forestGreen">The Problem</h3>
                      <p className="text-xs sm:text-sm text-secondaryText leading-relaxed">
                        Oncology reports and cancer explanations are filled with intimidating clinical jargon—such as 
                        <em> "metastasis," "carcinoma," "adjuvant,"</em> and <em>"histopathology."</em> In rural and semi-rural 
                        communities in India, this terminology creates extreme fear, fatalism, delays in seeking treatment, and confusion for patients and their families.
                      </p>
                    </div>

                    <div className="p-6 rounded-xl bg-pureWhite border border-borderLight space-y-2.5 hover-lift">
                      <div className="w-8 h-8 rounded bg-mutedSage text-tealDark flex items-center justify-center text-sm font-semibold">
                        <i className="fa-solid fa-bullseye"></i>
                      </div>
                      <h3 className="text-base font-bold text-forestGreen">Our Purpose</h3>
                      <p className="text-xs sm:text-sm text-secondaryText leading-relaxed">
                        OncoSathi bridges this communication gap. It equips <strong>ASHA (Accredited Social Health Activists)</strong> 
                        and community health workers with grounded, simplified explanations in plain English and authentic Bengali (বাংলা), 
                        preserving accurate medical meaning while removing confusing vocabulary.
                      </p>
                    </div>
                  </div>

                  {/* Editorial Image & Documentary Setting */}
                  <div className="p-3 bg-pureWhite rounded-xl border border-borderLight shadow-sm">
                    <img 
                      src="/images/clinic_consultation.jpg" 
                      alt="Doctor consultation in healthcare clinic" 
                      className="w-full h-[260px] sm:h-[320px] object-cover rounded-lg"
                    />
                    <div className="p-3 text-xs text-secondaryText">
                      Community healthcare consultation: Bridging clinical expertise with patient empathy and understanding.
                    </div>
                  </div>

                  {/* How it Works & Medical Safety */}
                  <div className="p-6 sm:p-8 rounded-xl bg-pureWhite border border-borderLight space-y-6">
                    <div className="space-y-2">
                      <h3 className="text-lg font-bold text-forestGreen">How Knowledge Retrieval Works</h3>
                      <p className="text-xs sm:text-sm text-secondaryText leading-relaxed">
                        When an ASHA worker inputs a medical excerpt or question, OncoSathi indexes and matches the query against 
                        <strong> 4 verified oncology reference sources</strong> (IJPC Cancer Glossary, Oncology Terminology Presentation, 
                        Medical Terminology DOCX, and Oncology Comprehensive Tables). The matched chunks are passed through a 
                        rigorous simplification pipeline that generates patient-friendly counseling summaries without inventing unsupported information.
                      </p>
                    </div>

                    <div className="pt-4 border-t border-borderLight space-y-2">
                      <span className="text-[11px] font-semibold text-mutedTerracotta uppercase tracking-wider bg-softPeach px-2 py-0.5 rounded">
                        Medical Safety Boundary
                      </span>
                      <h4 className="text-sm font-bold text-forestGreen">Educational Companion Notice</h4>
                      <p className="text-xs text-secondaryText leading-relaxed">
                        OncoSathi is an educational and communication support platform designed exclusively for community health workers. 
                        It is <strong>not a medical diagnostic tool</strong> and does not prescribe, modify, or replace treatments ordered by 
                        qualified Medical Officers and oncologists. Community workers are advised to always escort suspected patients to their 
                        nearest Primary Health Centre (PHC) or District Hospital.
                      </p>
                    </div>
                  </div>

                </div>
              </div>
            )}

          </main>

          {/* SOLID FOOTER (Forest Green) */}
          <footer className="bg-forestGreen text-white border-t border-tealDark py-10 mt-16">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 space-y-8">
              
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 pb-6 border-b border-white/10">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <div className="w-6 h-6 rounded bg-tealPrimary flex items-center justify-center text-white text-xs">
                      +
                    </div>
                    <span className="font-bold text-lg text-white tracking-tight">OncoSathi</span>
                  </div>
                  <p className="text-xs text-mutedSage">
                    Making cancer information easier to understand and share.
                  </p>
                </div>

                <div className="flex flex-wrap gap-4 text-xs text-mutedSage">
                  <button onClick={() => setActiveTab('home')} className="hover:text-white">Home</button>
                  <button onClick={() => setActiveTab('simplify')} className="hover:text-white">Simplify Information</button>
                  <button onClick={() => setActiveTab('dictionary')} className="hover:text-white">Oncology Dictionary</button>
                  <button onClick={() => setActiveTab('guide')} className="hover:text-white">Field Guide</button>
                  <button onClick={() => setActiveTab('about')} className="hover:text-white">About</button>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-[11px] text-mutedSage/80">
                <div>
                  © 2026 OncoSathi AI • Designed for ASHA Community Health Workers in India.
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-tealPrimary"></span>
                  <span>Grounded in 4 Verified Oncology References</span>
                </div>
              </div>

            </div>
          </footer>

          {/* SOURCE CITATION EXCERPT MODAL */}
          {selectedSourceModal && (
            <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4 animate-fade-in-up">
              <div className="bg-pureWhite rounded-xl border border-borderLight max-w-lg w-full p-6 space-y-4 shadow-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-[10px] font-semibold uppercase tracking-wider bg-softSage text-tealDark px-2 py-0.5 rounded">
                      Grounded Medical Source
                    </span>
                    <h3 className="font-bold text-base text-forestGreen mt-1">
                      {selectedSourceModal.document_name}
                    </h3>
                    <div className="text-xs text-secondaryText">
                      {selectedSourceModal.page_or_slide || selectedSourceModal.section}
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedSourceModal(null)}
                    className="text-secondaryText hover:text-textDark p-1"
                  >
                    <i className="fa-solid fa-xmark text-sm"></i>
                  </button>
                </div>

                <div className="p-3.5 rounded-lg bg-warmCream border border-borderLight text-xs text-textDark leading-relaxed">
                  <div className="font-semibold text-tealPrimary text-[11px] mb-1">Passage Excerpt:</div>
                  &quot;{selectedSourceModal.excerpt}&quot;
                </div>

                {selectedSourceModal.similarity_score && (
                  <div className="text-[11px] text-secondaryText flex items-center justify-between">
                    <span>Relevance Match:</span>
                    <span className="font-semibold text-tealPrimary">{(selectedSourceModal.similarity_score * 100).toFixed(1)}%</span>
                  </div>
                )}

                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => setSelectedSourceModal(null)}
                    className="bg-forestGreen text-white text-xs font-semibold px-4 py-2 rounded-md hover:bg-tealDark transition-colors"
                  >
                    Close Excerpt
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
'''

DEST.write_text(HTML_CONTENT, encoding="utf-8")
print(f"Updated {DEST} with animated features, sound wave visualizer, and clean query flow ({len(HTML_CONTENT):,} chars)")
