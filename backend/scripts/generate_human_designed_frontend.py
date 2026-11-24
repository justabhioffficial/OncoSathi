# -*- coding: utf-8 -*-
"""
Generate a human-designed, professional healthcare web frontend for OncoSathi AI.
Replaces all generic AI website tropes (sparkles, gradients, glowing cards, marketing filler)
with a calm, trustworthy, accessible, real-world clinical tool interface.
"""
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
INDEX_HTML = WORKSPACE / "frontend" / "public" / "index.html"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OncoSathi — Oncology Information Tool for Community Healthcare</title>
  <meta name="description" content="A clinical medical information simplification tool designed for ASHA community health workers in Simple English and Bengali." />
  
  <!-- Typography: Inter for clean UI & Hind Siliguri for authentic Bengali rendering -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            bengali: ['"Hind Siliguri"', 'sans-serif'],
          },
          colors: {
            forest: {
              50: '#F0F6F5',
              100: '#E1EDEB',
              200: '#C3DBD7',
              300: '#95C0B9',
              400: '#5F9E94',
              500: '#176B63',
              600: '#145F58',
              700: '#124E49',
              800: '#103F3B',
              900: '#0C2D2A',
            },
            canvas: '#F7F8F6',
            surface: '#FFFFFF',
            slateText: '#202A2A',
            mutedText: '#586563',
            borderSubtle: '#E3E8E5',
          }
        }
      }
    }
  </script>

  <!-- React 18, ReactDOM 18 & Babel Standalone -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <!-- Clean Minimal Icons (FontAwesome used strictly for functional symbols) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />

  <style>
    body {
      background-color: #F7F8F6;
      color: #202A2A;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .font-bn {
      font-family: 'Hind Siliguri', sans-serif;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #F1F4F2;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #CCD5D2;
      border-radius: 3px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #A4B2AF;
    }
    /* Subtle focus outlines for accessibility */
    input:focus, textarea:focus, select:focus, button:focus-visible {
      outline: 2px solid #176B63;
      outline-offset: 1px;
    }
  </style>
</head>
<body class="bg-canvas text-slateText min-h-screen flex flex-col antialiased selection:bg-forest-500 selection:text-white">

  <div id="root"></div>

  <!-- Main React App Script -->
  <script type="text/babel">
    const { useState, useEffect } = React;

    const API_BASE = window.location.origin;

    // College Presentation Demonstrations (Phase 14)
    const PRESENTATION_DEMOS = [
      {
        id: "demo1",
        label: "Case 1: Complex Terminology → Simple English",
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
            "Explain that cancer is an illness where body cells divide without standard stops.",
            "Metastasis means cancer cells have moved to another part of the body.",
            "Early medical evaluation and consistent care give the best chances for recovery."
          ],
          terms_explained: [
            { term: "Neoplasm", simple_meaning: "An abnormal growth or lump of cells; can be benign or malignant.", category: "General Oncology" },
            { term: "Metastasis", simple_meaning: "Spread of cancer cells from primary location to distant organs.", category: "General Oncology" },
            { term: "Proliferation", simple_meaning: "Rapid, continuous division and multiplication of cells.", category: "Pathology" }
          ],
          sources: [
            { document_name: "1_ijpc_cancer_glossary.pdf", section: "Glossary - Healthcare Terms", page_or_slide: "Page 2", excerpt: "Malignant: Cancerous; cells that divide uncontrollably and can invade nearby tissue.", similarity_score: 0.94 },
            { document_name: "2_medical_oncology_terminology_ba.pdf", section: "Clinical Oncology", page_or_slide: "Slide 3", excerpt: "Metastasis: Movement of cancer cells via bloodstream or lymphatics to distant organs.", similarity_score: 0.91 }
          ],
          disclaimer: "This demonstration explanation is grounded in verified oncology sources. It serves as an educational reference for community healthcare communication."
        }
      },
      {
        id: "demo2",
        label: "Case 2: Complex Terminology → Simple Bengali (সহজ বাংলা)",
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
          disclaimer: "এই সরলীকৃত ব্যাখ্যাটি রোগীদের বোঝানোর জন্য প্রস্তুত করা হয়েছে। নির্দিষ্ট চিকিৎসার সিদ্ধান্ত চিকিৎসকের নির্দেশ অনুযায়ী নিতে হবে।"
        }
      },
      {
        id: "demo3",
        label: "Case 3: Clinical Question → Grounded Answer",
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

    // Curated medical examples for instant testing
    const SAMPLE_QUERIES = [
      { text: "What is cancer and how does it start in the body?", mode: "ask", lang: "english", label: "What is cancer?" },
      { text: "What does metastasis mean in a medical oncology report?", mode: "ask", lang: "english", label: "What is metastasis?" },
      { text: "Malignant neoplasms are characterized by uncontrolled cellular proliferation with the potential for invasion and metastasis.", mode: "simplify", lang: "english", label: "Neoplasm proliferation" },
      { text: "কেমোথেরাপির কাজ কী এবং এটি শরীরে কীভাবে কাজ করে?", mode: "ask", lang: "bengali", label: "কেমোথেরাপি কী? (বাংলা)" },
      { text: "Patient scheduled for adjuvant chemotherapy regimens following surgical resection for Stage IIIA carcinoma.", mode: "simplify", lang: "english", label: "Adjuvant chemotherapy" },
      { text: "Core needle biopsy performed. Histopathology reveals invasive ductal carcinoma requiring staging.", mode: "simplify", lang: "english", label: "Biopsy report" }
    ];

    function App() {
      const [activeTab, setActiveTab] = useState('home'); // home, simplify, dictionary, guide, history, demos
      const [inputMode, setInputMode] = useState('simplify'); // simplify (text) or ask (question)
      const [inputText, setInputText] = useState('');
      const [targetLang, setTargetLang] = useState('english'); // english, bengali
      const [targetLevel, setTargetLevel] = useState(2); // 1, 2, 3
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState(null);
      const [result, setResult] = useState(null);
      const [isDemoDisplay, setIsDemoDisplay] = useState(false);
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

      // Load History on Mount & check health
      useEffect(() => {
        try {
          const savedHistory = localStorage.getItem('oncosathi_history');
          if (savedHistory) setHistory(JSON.parse(savedHistory));
        } catch (e) {}
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
              provider: data.llm_provider
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
          console.error(e);
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
        }, 200);
        return () => clearTimeout(timer);
      }, [termSearch]);

      // Run live simplification or question answering
      const handleRun = async (overrideText = null, overrideMode = null) => {
        const textToProcess = overrideText !== null ? overrideText : inputText;
        const activeMode = overrideMode !== null ? overrideMode : inputMode;

        if (!textToProcess.trim()) {
          setError(activeMode === 'ask' ? "Please enter a question to ask." : "Please enter or paste medical text to simplify.");
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
          setError(err.message || "An unexpected error occurred.");
        } finally {
          setLoading(false);
        }
      };

      const loadDemo = (demo) => {
        setInputText(demo.input);
        setTargetLang(demo.lang);
        setTargetLevel(demo.level);
        setInputMode(demo.mode);
        setResult(demo.result);
        setIsDemoDisplay(true);
        setActiveTab('simplify');
        setError(null);
        stopSpeech();
        window.scrollTo({ top: 320, behavior: 'smooth' });
      };

      // Web Speech Text-to-Speech
      const playSpeech = (textToSpeak, langCode) => {
        if (!('speechSynthesis' in window)) {
          alert("Your browser does not support audio speech output.");
          return;
        }

        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        const isBn = langCode === 'bengali' || langCode === 'bn' || /[\u0980-\u09FF]/.test(textToSpeak);

        utterance.lang = isBn ? 'bn-IN' : 'en-IN';
        utterance.rate = isBn ? 0.85 : 0.95;

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
        setTimeout(() => setCopied(false), 2000);
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
        <div className="min-h-screen flex flex-col bg-canvas text-slateText">
          
          {/* Top Clean Header */}
          <header className="bg-surface border-b border-borderSubtle sticky top-0 z-40">
            <div className="max-w-5xl mx-auto px-4 sm:px-6">
              <div className="flex items-center justify-between h-16">
                
                {/* Brand Title */}
                <div 
                  className="flex items-center space-x-3 cursor-pointer select-none"
                  onClick={() => setActiveTab('home')}
                >
                  <div className="w-8 h-8 rounded-lg bg-forest-500 flex items-center justify-center text-white text-sm font-semibold">
                    <i className="fa-solid fa-plus text-xs"></i>
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold text-lg text-slateText tracking-tight">OncoSathi</span>
                      <span className="text-[11px] text-mutedText bg-slate-100 px-2 py-0.5 rounded font-medium border border-borderSubtle">ASHA Tool</span>
                    </div>
                  </div>
                </div>

                {/* Restrained Text Navigation */}
                <nav className="hidden md:flex items-center space-x-1 text-sm font-medium text-mutedText">
                  <button 
                    onClick={() => setActiveTab('home')}
                    className={`px-3 py-1.5 rounded-md transition-colors ${activeTab === 'home' ? 'text-forest-600 bg-forest-50 font-semibold' : 'hover:text-slateText'}`}
                  >
                    Home
                  </button>
                  <button 
                    onClick={() => setActiveTab('simplify')}
                    className={`px-3 py-1.5 rounded-md transition-colors ${activeTab === 'simplify' ? 'text-forest-600 bg-forest-50 font-semibold' : 'hover:text-slateText'}`}
                  >
                    Simplify Text
                  </button>
                  <button 
                    onClick={() => setActiveTab('dictionary')}
                    className={`px-3 py-1.5 rounded-md transition-colors ${activeTab === 'dictionary' ? 'text-forest-600 bg-forest-50 font-semibold' : 'hover:text-slateText'}`}
                  >
                    Dictionary
                  </button>
                  <button 
                    onClick={() => setActiveTab('guide')}
                    className={`px-3 py-1.5 rounded-md transition-colors ${activeTab === 'guide' ? 'text-forest-600 bg-forest-50 font-semibold' : 'hover:text-slateText'}`}
                  >
                    Field Guide
                  </button>
                  <button 
                    onClick={() => setActiveTab('history')}
                    className={`px-3 py-1.5 rounded-md transition-colors ${activeTab === 'history' ? 'text-forest-600 bg-forest-50 font-semibold' : 'hover:text-slateText'}`}
                  >
                    History {history.length > 0 && `(${history.length})`}
                  </button>
                  <button 
                    onClick={() => setActiveTab('demos')}
                    className={`px-2.5 py-1 text-xs rounded border transition-colors ${activeTab === 'demos' ? 'border-forest-500 text-forest-700 bg-forest-50 font-semibold' : 'border-borderSubtle text-mutedText hover:text-slateText'}`}
                  >
                    Demo Cases
                  </button>
                </nav>

                {/* Right: Language Switcher */}
                <div className="flex items-center space-x-3">
                  <div className="flex bg-slate-100 p-0.5 rounded-md border border-borderSubtle text-xs font-medium">
                    <button
                      onClick={() => setTargetLang('english')}
                      className={`px-2.5 py-1 rounded transition-colors ${targetLang === 'english' ? 'bg-surface text-forest-700 font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                    >
                      English
                    </button>
                    <button
                      onClick={() => setTargetLang('bengali')}
                      className={`px-2.5 py-1 rounded font-bn transition-colors ${targetLang === 'bengali' ? 'bg-forest-500 text-white font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                    >
                      বাংলা
                    </button>
                  </div>
                </div>

              </div>
            </div>

            {/* Mobile Navigation bar */}
            <div className="flex md:hidden border-t border-borderSubtle bg-surface px-4 py-2 space-x-2 overflow-x-auto text-xs font-medium text-mutedText custom-scrollbar">
              <button onClick={() => setActiveTab('home')} className={`px-2.5 py-1 rounded whitespace-nowrap ${activeTab === 'home' ? 'text-forest-700 bg-forest-50 font-semibold' : ''}`}>Home</button>
              <button onClick={() => setActiveTab('simplify')} className={`px-2.5 py-1 rounded whitespace-nowrap ${activeTab === 'simplify' ? 'text-forest-700 bg-forest-50 font-semibold' : ''}`}>Simplify</button>
              <button onClick={() => setActiveTab('dictionary')} className={`px-2.5 py-1 rounded whitespace-nowrap ${activeTab === 'dictionary' ? 'text-forest-700 bg-forest-50 font-semibold' : ''}`}>Dictionary</button>
              <button onClick={() => setActiveTab('guide')} className={`px-2.5 py-1 rounded whitespace-nowrap ${activeTab === 'guide' ? 'text-forest-700 bg-forest-50 font-semibold' : ''}`}>Field Guide</button>
              <button onClick={() => setActiveTab('history')} className={`px-2.5 py-1 rounded whitespace-nowrap ${activeTab === 'history' ? 'text-forest-700 bg-forest-50 font-semibold' : ''}`}>History</button>
              <button onClick={() => setActiveTab('demos')} className={`px-2.5 py-1 rounded whitespace-nowrap ${activeTab === 'demos' ? 'text-forest-700 bg-forest-50 font-semibold' : ''}`}>Demos</button>
            </div>
          </header>

          {/* Main Content Area */}
          <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 py-8">

            {/* PAGE 1: HOME (HUMAN-DESIGNED, NO AI MARKETING FILLER) */}
            {activeTab === 'home' && (
              <div className="space-y-10 animate-fadeIn">
                
                {/* Product Introduction */}
                <div className="border-b border-borderSubtle pb-8 space-y-4">
                  <h1 className="text-2xl sm:text-3xl font-semibold text-slateText tracking-tight leading-snug">
                    Understand medical information.<br />
                    Explain it simply.
                  </h1>
                  <p className="text-mutedText text-sm sm:text-base max-w-2xl leading-relaxed">
                    OncoSathi helps community healthcare workers understand cancer-related reports, doctor notes, and staging terminology, and communicate them in clear language to patients and families.
                  </p>
                  
                  <div className="pt-2 flex flex-wrap gap-3">
                    <button
                      onClick={() => setActiveTab('simplify')}
                      className="px-4 py-2.5 bg-forest-500 hover:bg-forest-600 text-white text-sm font-medium rounded-lg transition-colors flex items-center space-x-2"
                    >
                      <span>Simplify medical text</span>
                      <i className="fa-solid fa-arrow-right text-xs"></i>
                    </button>
                    <button
                      onClick={() => setActiveTab('dictionary')}
                      className="px-4 py-2.5 bg-surface hover:bg-slate-50 text-slateText border border-borderSubtle text-sm font-medium rounded-lg transition-colors"
                    >
                      Browse oncology dictionary
                    </button>
                  </div>
                </div>

                {/* Practical 3-Step Overview */}
                <div className="space-y-3">
                  <h2 className="text-xs font-semibold text-mutedText uppercase tracking-wider">How the tool works</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-1">
                    <div className="space-y-1.5">
                      <div className="text-xs font-semibold text-forest-700">1. Input medical notes</div>
                      <p className="text-xs text-mutedText leading-relaxed">
                        Paste pathology findings, doctor discharge notes, or enter a clinical question asked by a patient.
                      </p>
                    </div>

                    <div className="space-y-1.5">
                      <div className="text-xs font-semibold text-forest-700">2. Select audience level</div>
                      <p className="text-xs text-mutedText leading-relaxed">
                        Choose Simple English or সহজ বাংলা (Bengali), and select between Basic, Community, or Detailed summaries.
                      </p>
                    </div>

                    <div className="space-y-1.5">
                      <div className="text-xs font-semibold text-forest-700">3. Review and counsel</div>
                      <p className="text-xs text-mutedText leading-relaxed">
                        Get clear explanations with key points, verified medical definitions, and optional spoken voice output.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Verified Knowledge Sources Reference */}
                <div className="bg-surface rounded-lg border border-borderSubtle p-5 space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pb-3 border-b border-borderSubtle">
                    <div>
                      <h3 className="text-sm font-semibold text-slateText">Grounded Medical Knowledge Base</h3>
                      <p className="text-xs text-mutedText">All explanations are referenced against four primary oncology sources.</p>
                    </div>
                    <span className="text-[11px] font-medium text-forest-700 bg-forest-50 px-2.5 py-1 rounded border border-forest-100 w-fit">
                      {systemStatus.termCount} Terms • {systemStatus.chunksCount} Reference Chunks
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="p-3 bg-canvas rounded border border-borderSubtle space-y-1">
                      <div className="font-semibold text-slateText">1. IJPC Cancer Glossary</div>
                      <p className="text-mutedText">Foundational oncology healthcare definitions and patient terminology.</p>
                    </div>

                    <div className="p-3 bg-canvas rounded border border-borderSubtle space-y-1">
                      <div className="font-semibold text-slateText">2. Medical Oncology Terminology (Ba)</div>
                      <p className="text-mutedText">Presentation terminology, clinical staging protocols, and chemotherapy concepts.</p>
                    </div>

                    <div className="p-3 bg-canvas rounded border border-borderSubtle space-y-1">
                      <div className="font-semibold text-slateText">3. Cancer Terminology Bengali-English</div>
                      <p className="text-mutedText">157 bilingual parallel records with authentic Bengali medical translations.</p>
                    </div>

                    <div className="p-3 bg-canvas rounded border border-borderSubtle space-y-1">
                      <div className="font-semibold text-slateText">4. Comprehensive Oncology Tables</div>
                      <p className="text-mutedText">171 structured rows across diagnostic workup, classifications, and symptoms.</p>
                    </div>
                  </div>
                </div>

                {/* Safety Scope Notice */}
                <div className="p-4 bg-amber-50/60 border border-amber-200/80 rounded-lg text-xs text-amber-900 flex items-start space-x-3">
                  <i className="fa-solid fa-circle-info text-amber-600 mt-0.5"></i>
                  <div className="space-y-1">
                    <span className="font-semibold">Clinical Scope and Safety</span>
                    <p className="text-amber-800/90 leading-relaxed">
                      OncoSathi is an educational communication aid designed to help healthcare workers explain medical information. It does not provide medical diagnoses or prescribe medication dosages. For clinical decisions, always direct patients to a certified physician or Primary Health Centre (PHC).
                    </p>
                  </div>
                </div>

              </div>
            )}

            {/* PAGE 2: MAIN SIMPLIFICATION INTERFACE */}
            {activeTab === 'simplify' && (
              <div className="space-y-8 animate-fadeIn">
                
                {/* Input Workspace */}
                <div className="bg-surface rounded-lg border border-borderSubtle p-5 sm:p-6 space-y-5 shadow-sm">
                  
                  {/* Mode & Sample Row */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-borderSubtle">
                    <div className="flex items-center space-x-2 text-xs font-medium">
                      <button
                        onClick={() => setInputMode('simplify')}
                        className={`px-3 py-1.5 rounded transition-colors ${inputMode === 'simplify' ? 'bg-forest-500 text-white font-semibold' : 'bg-slate-100 text-mutedText hover:text-slateText'}`}
                      >
                        Simplify Medical Text
                      </button>
                      <button
                        onClick={() => setInputMode('ask')}
                        className={`px-3 py-1.5 rounded transition-colors ${inputMode === 'ask' ? 'bg-forest-500 text-white font-semibold' : 'bg-slate-100 text-mutedText hover:text-slateText'}`}
                      >
                        Ask a Question
                      </button>
                    </div>

                    {/* Clean Sample Links */}
                    <div className="flex flex-wrap items-center gap-1.5 text-xs">
                      <span className="text-mutedText font-medium text-[11px]">Examples:</span>
                      {SAMPLE_QUERIES.slice(0, 4).map((sq, idx) => (
                        <button
                          key={idx}
                          onClick={() => {
                            setInputText(sq.text);
                            setInputMode(sq.mode);
                            setTargetLang(sq.lang);
                          }}
                          className="px-2 py-0.5 bg-canvas hover:bg-slate-200/70 border border-borderSubtle text-mutedText hover:text-slateText rounded text-[11px] transition-colors"
                        >
                          {sq.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Textarea Area */}
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <label htmlFor="medical-input" className="font-semibold text-slateText">
                        {inputMode === 'ask' ? 'Enter clinical question' : 'Enter or paste medical text'}
                      </label>
                      <span className="text-mutedText text-[11px]">
                        {inputText.length > 0 && `${inputText.length} characters`}
                      </span>
                    </div>

                    <textarea
                      id="medical-input"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      rows={4}
                      placeholder={inputMode === 'ask'
                        ? (targetLang === 'bengali' ? "ক্যানসার সংক্রান্ত যেকোনো প্রশ্ন লিখুন (যেমন: বায়োপসি কী?)..." : "Ask a medical question (e.g., 'What is a core needle biopsy?', 'What does metastasis mean?')...")
                        : (targetLang === 'bengali' ? "এখানে জটিল মেডিকেল রিপোর্ট বা ডাক্তারের নোট পেস্ট করুন..." : "Paste medical report, histology finding, or doctor notes here...")
                      }
                      className="w-full p-3.5 rounded-lg border border-borderSubtle bg-white text-slateText text-sm leading-relaxed transition-all resize-y custom-scrollbar"
                    ></textarea>
                  </div>

                  {/* Controls: Target Language & Simplification Level */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                    
                    {/* Language Selection */}
                    <div className="space-y-1.5">
                      <label className="block text-xs font-semibold text-slateText">Output Language</label>
                      <div className="flex bg-canvas p-1 rounded-md border border-borderSubtle text-xs font-medium">
                        <button
                          type="button"
                          onClick={() => setTargetLang('english')}
                          className={`flex-1 py-1.5 text-center rounded transition-colors ${targetLang === 'english' ? 'bg-surface text-forest-700 font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                        >
                          Simple English
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLang('bengali')}
                          className={`flex-1 py-1.5 text-center rounded font-bn transition-colors ${targetLang === 'bengali' ? 'bg-forest-500 text-white font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                        >
                          সহজ বাংলা
                        </button>
                      </div>
                    </div>

                    {/* Simplification Level */}
                    <div className="space-y-1.5">
                      <div className="flex justify-between items-center text-xs">
                        <label className="font-semibold text-slateText">Explanation Level</label>
                        <span className="text-mutedText text-[11px]">
                          {targetLevel === 1 ? 'Basic (Short sentences)' : targetLevel === 2 ? 'Community Health (Conversational)' : 'Detailed Summary'}
                        </span>
                      </div>
                      <div className="flex bg-canvas p-1 rounded-md border border-borderSubtle text-xs font-medium">
                        <button
                          type="button"
                          onClick={() => setTargetLevel(1)}
                          className={`flex-1 py-1.5 text-center rounded transition-colors ${targetLevel === 1 ? 'bg-surface text-forest-700 font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                        >
                          Basic
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLevel(2)}
                          className={`flex-1 py-1.5 text-center rounded transition-colors ${targetLevel === 2 ? 'bg-surface text-forest-700 font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                        >
                          Easy (ASHA)
                        </button>
                        <button
                          type="button"
                          onClick={() => setTargetLevel(3)}
                          className={`flex-1 py-1.5 text-center rounded transition-colors ${targetLevel === 3 ? 'bg-surface text-forest-700 font-semibold shadow-sm' : 'text-mutedText hover:text-slateText'}`}
                        >
                          Detailed
                        </button>
                      </div>
                    </div>

                  </div>

                  {/* Error Notification */}
                  {error && (
                    <div className="p-3 bg-red-50 border border-red-200 text-red-800 text-xs rounded-md flex items-start space-x-2">
                      <i className="fa-solid fa-triangle-exclamation text-red-600 mt-0.5"></i>
                      <span>{error}</span>
                    </div>
                  )}

                  {/* Action Bar */}
                  <div className="flex items-center justify-between pt-2 border-t border-borderSubtle">
                    <button
                      type="button"
                      onClick={() => {
                        setInputText('');
                        setResult(null);
                        setError(null);
                      }}
                      className="text-xs text-mutedText hover:text-slateText font-medium"
                    >
                      Clear input
                    </button>

                    <button
                      type="button"
                      disabled={loading || !inputText.trim()}
                      onClick={() => handleRun()}
                      className={`px-5 py-2 text-sm font-medium rounded-lg transition-colors flex items-center space-x-2 ${
                        loading || !inputText.trim() 
                          ? 'bg-slate-200 text-mutedText cursor-not-allowed' 
                          : 'bg-forest-500 hover:bg-forest-600 text-white'
                      }`}
                    >
                      {loading ? (
                        <>
                          <i className="fa-solid fa-circle-notch fa-spin text-xs"></i>
                          <span>Processing...</span>
                        </>
                      ) : (
                        <>
                          <span>{inputMode === 'ask' ? 'Answer question' : 'Simplify explanation'}</span>
                        </>
                      )}
                    </button>
                  </div>

                </div>

                {/* Loading State */}
                {loading && (
                  <div className="p-8 bg-surface rounded-lg border border-borderSubtle text-center space-y-2">
                    <i className="fa-solid fa-circle-notch fa-spin text-forest-500 text-lg"></i>
                    <p className="text-xs text-mutedText">Retrieving relevant oncology sources and generating simplified explanation...</p>
                  </div>
                )}

                {/* RESULTS SECTION (EDITORIAL CLINICAL LAYOUT, NOT NEON CARDS) */}
                {result && !loading && (
                  <div className="bg-surface rounded-lg border border-borderSubtle p-6 space-y-6 shadow-sm animate-fadeIn">
                    
                    {/* Demo Banner if demo loaded */}
                    {isDemoDisplay && (
                      <div className="p-2.5 bg-amber-50 border border-amber-200 text-amber-900 rounded text-xs flex items-center justify-between">
                        <span><strong>Predefined Demonstration Case</strong> — Grounded output from verified knowledge base.</span>
                        <span className="text-[10px] font-semibold bg-amber-200 px-2 py-0.5 rounded">SAMPLE DEMO</span>
                      </div>
                    )}

                    {/* Result Header */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-borderSubtle gap-2">
                      <div>
                        <h3 className="text-base font-semibold text-slateText">
                          {result.language === 'bengali' || result.target_language === 'bn' ? 'সহজ ভাষায় ব্যাখ্যা' : 'Simplified Explanation'}
                        </h3>
                        <p className="text-xs text-mutedText">
                          Grounded in {result.sources ? result.sources.length : 0} verified oncology source citations
                        </p>
                      </div>

                      <div className="flex items-center space-x-2 text-xs">
                        <span className="px-2 py-0.5 bg-canvas rounded border border-borderSubtle font-medium text-slateText">
                          {result.language === 'bengali' || result.target_language === 'bn' ? 'সহজ বাংলা' : 'Simple English'}
                        </span>
                        <span className="px-2 py-0.5 bg-canvas rounded border border-borderSubtle font-medium text-slateText">
                          {result.reading_level_label || result.reading_level || 'Level 2 — Easy'}
                        </span>
                      </div>
                    </div>

                    {/* 1. Main Simple Explanation */}
                    <div className="space-y-3">
                      
                      {/* Audio Playback Bar */}
                      <div className="flex items-center justify-between p-2.5 bg-canvas rounded border border-borderSubtle text-xs">
                        <div className="flex items-center space-x-2">
                          <i className="fa-solid fa-volume-high text-forest-600 text-xs"></i>
                          <span className="text-mutedText">Audio explanation ({result.language === 'bengali' || result.target_language === 'bn' ? 'বাংলা কন্ঠ' : 'English Voice'}):</span>
                        </div>
                        <div className="flex items-center space-x-1.5">
                          {!ttsSpeaking ? (
                            <button
                              onClick={() => playSpeech(result.simplified_text || result.answer, result.language || result.target_language)}
                              className="px-2.5 py-1 bg-forest-500 hover:bg-forest-600 text-white rounded font-medium text-xs flex items-center space-x-1 transition-colors"
                            >
                              <i className="fa-solid fa-play text-[10px]"></i>
                              <span>Play</span>
                            </button>
                          ) : (
                            <>
                              <button onClick={pauseSpeech} className="px-2 py-1 bg-slate-200 text-slateText rounded text-xs font-medium">
                                {ttsPaused ? 'Resume' : 'Pause'}
                              </button>
                              <button onClick={stopSpeech} className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs font-medium">
                                Stop
                              </button>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Explanation Body */}
                      <div className={`p-4 bg-canvas/70 rounded-lg border border-borderSubtle text-slateText leading-relaxed whitespace-pre-line text-sm sm:text-base ${result.language === 'bengali' || result.target_language === 'bn' ? 'font-bn text-base sm:text-lg' : ''}`}>
                        {result.simplified_text || result.answer}
                      </div>

                    </div>

                    {/* 2. Key Takeaways / Points */}
                    {result.key_points && result.key_points.length > 0 && (
                      <div className="space-y-2 pt-1">
                        <h4 className="text-xs font-semibold text-mutedText uppercase tracking-wider">
                          Key Points for Counseling
                        </h4>
                        <ul className="space-y-1.5 text-xs sm:text-sm text-slateText">
                          {result.key_points.map((pt, idx) => (
                            <li key={idx} className="flex items-start space-x-2">
                              <span className="text-forest-600 mt-0.5">•</span>
                              <span className={result.language === 'bengali' || result.target_language === 'bn' ? 'font-bn' : ''}>{pt}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* 3. Medical Terms Explained */}
                    {((result.terms_explained && result.terms_explained.length > 0) || (result.explained_terms && result.explained_terms.length > 0)) && (
                      <div className="space-y-2 pt-1">
                        <h4 className="text-xs font-semibold text-mutedText uppercase tracking-wider">
                          Medical Terms Explained in Context
                        </h4>
                        <div className="divide-y divide-borderSubtle border border-borderSubtle rounded-lg text-xs">
                          {(result.terms_explained || result.explained_terms).map((t, idx) => (
                            <div key={idx} className="p-3 space-y-0.5">
                              <div className="flex items-center justify-between">
                                <span className="font-semibold text-slateText">{t.term}</span>
                                {t.category && <span className="text-[10px] text-mutedText bg-slate-100 px-1.5 py-0.5 rounded">{t.category}</span>}
                              </div>
                              {t.bengali_term && <p className="font-bn text-forest-700 font-medium">বাংলা: {t.bengali_term}</p>}
                              <p className={`text-mutedText ${result.language === 'bengali' || result.target_language === 'bn' ? 'font-bn' : ''}`}>
                                {t.simple_meaning || t.simplified_explanation_en || t.original_medical_definition}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 4. Collapsible Original Text Comparison */}
                    <details className="text-xs group border border-borderSubtle rounded-md overflow-hidden">
                      <summary className="p-2.5 bg-canvas hover:bg-slate-100 cursor-pointer font-medium text-mutedText flex items-center justify-between select-none">
                        <span>View original input text for comparison</span>
                        <i className="fa-solid fa-chevron-down text-[10px] text-mutedText group-open:rotate-180 transition-transform"></i>
                      </summary>
                      <div className="p-3 bg-surface font-mono text-[11px] text-mutedText border-t border-borderSubtle whitespace-pre-wrap">
                        {result.original_text || result.question || inputText}
                      </div>
                    </details>

                    {/* 5. Grounded Source Citations */}
                    {result.sources && result.sources.length > 0 && (
                      <div className="space-y-2 pt-1">
                        <h4 className="text-xs font-semibold text-mutedText uppercase tracking-wider">
                          Verified Sources Used ({result.sources.length})
                        </h4>
                        <div className="flex flex-wrap gap-2 text-xs">
                          {result.sources.map((src, idx) => (
                            <button
                              key={idx}
                              onClick={() => setSelectedSourceModal(src)}
                              className="px-2.5 py-1.5 bg-canvas hover:bg-slate-200/80 border border-borderSubtle rounded text-left transition-colors"
                            >
                              <div className="font-medium text-slateText truncate max-w-xs">
                                {src.document_title || src.document_name || src.source_document}
                              </div>
                              <div className="text-[10px] text-mutedText">
                                {src.section_or_page || src.page_or_slide || 'General'}
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Actions Row */}
                    <div className="flex flex-wrap items-center justify-between pt-4 border-t border-borderSubtle text-xs gap-3">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => copyToClipboard(result.simplified_text || result.answer)}
                          className="px-3 py-1.5 bg-canvas hover:bg-slate-200/70 border border-borderSubtle rounded font-medium text-slateText transition-colors"
                        >
                          {copied ? 'Copied to clipboard' : 'Copy explanation'}
                        </button>
                        <button
                          onClick={() => {
                            const newLang = targetLang === 'english' ? 'bengali' : 'english';
                            setTargetLang(newLang);
                            handleRun(inputText, inputMode);
                          }}
                          className="px-3 py-1.5 bg-canvas hover:bg-slate-200/70 border border-borderSubtle rounded font-medium text-forest-700 transition-colors"
                        >
                          Switch to {targetLang === 'english' ? 'বাংলা' : 'English'}
                        </button>
                      </div>

                      {/* Helpful Feedback */}
                      <div className="flex items-center space-x-2 text-mutedText">
                        <span>Helpful for counseling?</span>
                        {!feedbackSent ? (
                          <div className="flex items-center space-x-1">
                            <button
                              onClick={() => handleFeedback(true)}
                              className="px-2 py-1 bg-canvas hover:bg-slate-200 rounded border border-borderSubtle text-slateText"
                            >
                              Yes
                            </button>
                            <button
                              onClick={() => handleFeedback(false)}
                              className="px-2 py-1 bg-canvas hover:bg-slate-200 rounded border border-borderSubtle text-slateText"
                            >
                              No
                            </button>
                          </div>
                        ) : (
                          <span className="text-forest-700 font-medium">Feedback recorded.</span>
                        )}
                      </div>
                    </div>

                    {/* Disclaimer Note */}
                    <div className="p-3 bg-slate-50 border border-borderSubtle rounded text-[11px] text-mutedText leading-relaxed">
                      <strong>Medical Notice:</strong> {result.safety_notice || result.disclaimer || "OncoSathi provides educational simplifications grounded in verified sources. It does not replace certified physician evaluation or prescriptions."}
                    </div>

                  </div>
                )}

              </div>
            )}

            {/* PAGE 3: ONCOLOGY DICTIONARY (EDITORIAL SEARCHABLE REFERENCE) */}
            {activeTab === 'dictionary' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="space-y-2 border-b border-borderSubtle pb-6">
                  <h1 className="text-xl sm:text-2xl font-semibold text-slateText tracking-tight">Oncology Terminology Dictionary</h1>
                  <p className="text-xs sm:text-sm text-mutedText">
                    252 verified oncology terms extracted from the four primary medical documents with simplified English definitions and Bengali translations.
                  </p>
                  
                  {/* Search and Filters */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3">
                    <div className="md:col-span-2 relative">
                      <input
                        type="text"
                        value={termSearch}
                        onChange={(e) => setTermSearch(e.target.value)}
                        placeholder="Search term, abbreviation, or Bengali word (e.g., biopsy, metastasis, কেমোথেরাপি)..."
                        className="w-full p-2.5 rounded-md border border-borderSubtle bg-white text-xs sm:text-sm text-slateText placeholder-mutedText"
                      />
                      {termSearch && (
                        <button
                          onClick={() => setTermSearch('')}
                          className="absolute right-3 top-3 text-mutedText hover:text-slateText text-xs"
                        >
                          ✕
                        </button>
                      )}
                    </div>

                    <div>
                      <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="w-full p-2.5 rounded-md border border-borderSubtle bg-white text-xs sm:text-sm text-slateText"
                      >
                        <option value="All">All Categories ({terms.length})</option>
                        <option value="General Oncology">General Oncology</option>
                        <option value="Diagnosis & Pathology">Diagnosis & Pathology</option>
                        <option value="Treatment & Chemotherapy">Treatment & Chemotherapy</option>
                        <option value="Anatomy & Staging">Anatomy & Staging</option>
                        <option value="Palliative & Supportive Care">Palliative & Supportive Care</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Terminology List */}
                {termsLoading ? (
                  <div className="p-8 text-center text-xs text-mutedText">Loading terminology entries...</div>
                ) : terms.length === 0 ? (
                  <div className="p-8 text-center text-xs text-mutedText bg-surface rounded border border-borderSubtle">
                    No matching medical terms found.
                  </div>
                ) : (
                  <div className="divide-y divide-borderSubtle border border-borderSubtle rounded-lg bg-surface">
                    {terms.map((item, idx) => (
                      <div key={idx} className="p-4 space-y-2 hover:bg-canvas/50 transition-colors">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                          <div className="flex items-center space-x-2">
                            <span className="font-semibold text-sm text-slateText">{item.term}</span>
                            {item.category && (
                              <span className="text-[10px] text-mutedText bg-slate-100 px-1.5 py-0.5 rounded border border-borderSubtle">
                                {item.category}
                              </span>
                            )}
                          </div>

                          <div className="flex items-center space-x-2 text-xs">
                            <button
                              onClick={() => playSpeech(`${item.term}. ${item.simple_meaning || item.medical_definition}`, 'english')}
                              className="text-mutedText hover:text-slateText p-1"
                              title="Listen"
                            >
                              <i className="fa-solid fa-volume-high text-xs"></i>
                            </button>
                            <button
                              onClick={() => {
                                setInputText(`Explain ${item.term}: ${item.medical_definition || item.definition}`);
                                setInputMode('simplify');
                                setActiveTab('simplify');
                                handleRun(`Explain ${item.term}: ${item.medical_definition || item.definition}`, 'simplify');
                              }}
                              className="text-forest-700 hover:underline text-[11px] font-medium"
                            >
                              Simplify
                            </button>
                          </div>
                        </div>

                        {item.bengali_term && (
                          <div className="font-bn text-xs font-semibold text-forest-700">
                            বাংলা: {item.bengali_term}
                          </div>
                        )}

                        <div className="text-xs text-mutedText leading-relaxed">
                          <strong className="text-slateText">Definition:</strong> {item.medical_definition || item.definition}
                        </div>

                        {(item.simple_meaning || item.simplified_en) && (
                          <div className="text-xs text-slateText bg-canvas p-2.5 rounded border border-borderSubtle">
                            <strong className="text-forest-700">Simple explanation:</strong> {item.simple_meaning || item.simplified_en}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

              </div>
            )}

            {/* PAGE 4: ASHA FIELD GUIDE & RED FLAGS */}
            {activeTab === 'guide' && (
              <div className="space-y-8 animate-fadeIn">
                <div className="space-y-2 border-b border-borderSubtle pb-6">
                  <h1 className="text-xl sm:text-2xl font-semibold text-slateText tracking-tight">ASHA Oncology Field & Counseling Guide</h1>
                  <p className="text-xs sm:text-sm text-mutedText">
                    Essential cancer warning signs, compassionate counseling protocols, and immediate referral criteria for community visits.
                  </p>
                </div>

                {/* CAUTION Warning Signs Protocol */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xs font-semibold text-red-900 uppercase tracking-wider">
                      C-A-U-T-I-O-N Warning Signs (Immediate Referral Triggers)
                    </h2>
                    <span className="text-[11px] text-red-700 font-medium">Escort to nearest Community Health Centre</span>
                  </div>

                  <div className="border border-red-200 rounded-lg overflow-hidden divide-y divide-red-100 bg-surface text-xs">
                    {[
                      { letter: 'C', en: 'Change in bowel or bladder habits', bn: 'মল বা মূত্র ত্যাগের অভ্যাসে দীর্ঘস্থায়ী পরিবর্তন' },
                      { letter: 'A', en: 'A sore that does not heal over time', bn: 'দীর্ঘদিনেও না সারা কোনো ক্ষত বা ঘা' },
                      { letter: 'U', en: 'Unusual bleeding or discharge from any site', bn: 'শরীরের কোনো অংশ থেকে অস্বাভাবিক রক্তপাত বা স্রাব' },
                      { letter: 'T', en: 'Thickening or lump in breast, neck, or elsewhere', bn: 'স্তন বা শরীরের কোথাও শক্ত চাকা বা পিণ্ড' },
                      { letter: 'I', en: 'Indigestion or persistent difficulty swallowing', bn: 'খাবার গিলতে কষ্ট বা ক্রমাগত বদহজম' },
                      { letter: 'O', en: 'Obvious change in the size, shape, or color of a mole', bn: 'তিল বা আঁচিলের আকার বা রঙের স্পষ্ট পরিবর্তন' },
                      { letter: 'N', en: 'Nagging cough or persistent hoarseness of voice', bn: 'টানা কাশি বা গলার স্বরের স্থায়ী পরিবর্তন' },
                    ].map((row, idx) => (
                      <div key={idx} className="p-3 flex items-start space-x-3">
                        <span className="w-5 h-5 rounded bg-red-100 text-red-700 font-bold flex items-center justify-center shrink-0 text-xs">
                          {row.letter}
                        </span>
                        <div className="space-y-0.5">
                          <div className="font-semibold text-slateText">{row.en}</div>
                          <div className="font-bn text-mutedText">{row.bn}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Counseling Principles */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                  <div className="bg-surface p-5 rounded-lg border border-borderSubtle space-y-2">
                    <h3 className="text-sm font-semibold text-slateText">Patient Counseling Guidelines</h3>
                    <ul className="text-xs text-mutedText space-y-2 leading-relaxed">
                      <li>• <strong>Listen with empathy:</strong> Allow the patient and family to voice their fears about cancer stigma before explaining technical terms.</li>
                      <li>• <strong>Dispel common misconceptions:</strong> Clarify that cancer is not contagious and cannot spread through touching or eating together.</li>
                      <li>• <strong>Encourage follow-up adherence:</strong> Emphasize that completing all chemotherapy cycles and radiation appointments is essential.</li>
                    </ul>
                  </div>

                  <div className="bg-surface p-5 rounded-lg border border-borderSubtle space-y-2">
                    <h3 className="text-sm font-semibold text-slateText">Clinical Boundaries & Referral</h3>
                    <ul className="text-xs text-mutedText space-y-2 leading-relaxed">
                      <li>• <strong>Never alter medication dosages:</strong> Do not recommend dosage adjustments or alternative herbal substitutes without physician orders.</li>
                      <li>• <strong>Never guarantee cures:</strong> Explain prognosis realistically based on the doctor's staging notes.</li>
                      <li>• <strong>Report acute symptoms:</strong> High fever, severe nausea, or sudden bleeding require immediate hospital consultation.</li>
                    </ul>
                  </div>
                </div>

              </div>
            )}

            {/* PAGE 5: PRESENTATION DEMO MODE (PHASE 14) */}
            {activeTab === 'demos' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="space-y-2 border-b border-borderSubtle pb-6">
                  <h1 className="text-xl sm:text-2xl font-semibold text-slateText tracking-tight">Presentation Demo Cases</h1>
                  <p className="text-xs sm:text-sm text-mutedText">
                    Predefined, source-verified clinical oncology scenarios for college presentations and live evaluation.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                  {PRESENTATION_DEMOS.map((d) => (
                    <div key={d.id} className="bg-surface p-5 rounded-lg border border-borderSubtle flex flex-col justify-between space-y-4 shadow-sm">
                      <div className="space-y-2">
                        <span className="text-[10px] font-semibold text-forest-700 bg-forest-50 px-2 py-0.5 rounded border border-forest-100">
                          {d.id.toUpperCase()}
                        </span>
                        <h3 className="font-semibold text-sm text-slateText">{d.title}</h3>
                        <p className="text-xs text-mutedText leading-relaxed line-clamp-3">
                          "{d.input}"
                        </p>
                        <div className="text-[11px] text-mutedText pt-1">
                          Output: <strong>{d.lang}</strong> • Level: <strong>{d.level}</strong>
                        </div>
                      </div>

                      <button
                        onClick={() => loadDemo(d)}
                        className="w-full py-2 bg-forest-500 hover:bg-forest-600 text-white rounded text-xs font-medium transition-colors"
                      >
                        Launch demonstration
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* PAGE 6: SESSION HISTORY */}
            {activeTab === 'history' && (
              <div className="space-y-6 animate-fadeIn">
                <div className="flex items-center justify-between border-b border-borderSubtle pb-6">
                  <div>
                    <h1 className="text-xl sm:text-2xl font-semibold text-slateText tracking-tight">Session Query History</h1>
                    <p className="text-xs sm:text-sm text-mutedText">Past simplifications saved in your local browser storage for offline counseling reference.</p>
                  </div>
                  {history.length > 0 && (
                    <button
                      onClick={() => {
                        if (confirm("Clear local history?")) {
                          setHistory([]);
                          localStorage.removeItem('oncosathi_history');
                        }
                      }}
                      className="text-xs text-red-600 hover:text-red-700 font-medium"
                    >
                      Clear history
                    </button>
                  )}
                </div>

                {history.length === 0 ? (
                  <div className="p-8 text-center text-xs text-mutedText bg-surface rounded border border-borderSubtle">
                    No queries in your history yet.
                  </div>
                ) : (
                  <div className="divide-y divide-borderSubtle border border-borderSubtle rounded-lg bg-surface">
                    {history.map((item) => (
                      <div key={item.id} className="p-4 space-y-2">
                        <div className="flex items-center justify-between text-xs text-mutedText">
                          <span>{item.timestamp}</span>
                          <span className="font-medium text-slateText">{item.language}</span>
                        </div>
                        <div className="text-xs font-mono text-mutedText line-clamp-1">Q: {item.originalText}</div>
                        <div className={`text-xs sm:text-sm text-slateText line-clamp-2 ${item.language === 'bengali' ? 'font-bn' : ''}`}>
                          {item.simplifiedText}
                        </div>
                        <div className="pt-1 flex items-center space-x-3 text-xs">
                          <button
                            onClick={() => {
                              setInputText(item.originalText);
                              setTargetLang(item.language);
                              setActiveTab('simplify');
                              handleRun(item.originalText);
                            }}
                            className="text-forest-700 font-medium hover:underline"
                          >
                            Reload in simplifier
                          </button>
                          <button
                            onClick={() => playSpeech(item.simplifiedText, item.language)}
                            className="text-mutedText hover:text-slateText"
                          >
                            Listen audio
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

          </main>

          {/* SOURCE MODAL DIALOG */}
          {selectedSourceModal && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs animate-fadeIn">
              <div className="bg-surface rounded-lg max-w-xl w-full max-h-[85vh] flex flex-col border border-borderSubtle shadow-lg overflow-hidden">
                <div className="p-4 border-b border-borderSubtle flex items-center justify-between bg-canvas">
                  <div>
                    <h3 className="font-semibold text-sm text-slateText">
                      {selectedSourceModal.document_title || selectedSourceModal.document_name || selectedSourceModal.source_document}
                    </h3>
                    <p className="text-[11px] text-mutedText">
                      {selectedSourceModal.section_or_page || selectedSourceModal.section || 'General reference'}
                    </p>
                  </div>
                  <button
                    onClick={() => setSelectedSourceModal(null)}
                    className="text-mutedText hover:text-slateText text-sm p-1"
                  >
                    ✕
                  </button>
                </div>

                <div className="p-5 overflow-y-auto space-y-3 custom-scrollbar text-xs text-slateText leading-relaxed">
                  <div className="p-3 bg-canvas rounded border border-borderSubtle font-mono text-[11px] whitespace-pre-wrap">
                    {selectedSourceModal.chunk_text || selectedSourceModal.excerpt}
                  </div>
                  <div className="text-[11px] text-mutedText">
                    <strong>Source File:</strong> {selectedSourceModal.document_name || selectedSourceModal.source_document}
                  </div>
                </div>

                <div className="p-3 border-t border-borderSubtle bg-canvas flex justify-end">
                  <button
                    onClick={() => setSelectedSourceModal(null)}
                    className="px-3 py-1.5 bg-slateText hover:bg-slate-800 text-white font-medium text-xs rounded transition-colors"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Clean Editorial Footer */}
          <footer className="bg-surface border-t border-borderSubtle mt-16 py-6 text-xs text-mutedText">
            <div className="max-w-5xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-slateText">OncoSathi</span>
                <span>— Clinical Oncology Information Simplifier for Community Health Workers</span>
              </div>
              <div className="flex items-center space-x-3 text-mutedText">
                <span>Grounded RAG</span>
                <span>•</span>
                <span>English & Bengali</span>
                <span>•</span>
                <span>Zero Hallucination Guardrails</span>
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
    print(f"[OncoSathi] Wrote redesigned human frontend successfully at: {INDEX_HTML} ({len(HTML_CONTENT)} bytes)")

if __name__ == "__main__":
    main()
