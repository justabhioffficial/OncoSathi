# -*- coding: utf-8 -*-
"""
Generate complete React pages and App component for Vite/React structure.
"""
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
SRC_DIR = WORKSPACE / "frontend" / "src"

files = {}

# 1. pages/Home.tsx
files[SRC_DIR / "pages" / "Home.tsx"] = """import React from 'react';

interface HomeProps {
  onStartSimplifier: () => void;
  onOpenDictionary: () => void;
  onSelectPrompt: (text: string) => void;
}

export const Home: React.FC<HomeProps> = ({ onStartSimplifier, onOpenDictionary, onSelectPrompt }) => {
  const samplePrompts = [
    {
      title: "Cellular Proliferation & Neoplasm",
      text: "Malignant neoplasms are characterized by uncontrolled cellular proliferation with potential invasion and metastasis."
    },
    {
      title: "Chemotherapy Cycles",
      text: "Patient scheduled for adjuvant chemotherapy regimens following surgical resection to eradicate microscopic metastases."
    },
    {
      title: "TNM Staging Assessment",
      text: "Histopathology shows Stage IIIA invasive ductal carcinoma classified as T3 N1 M0 with positive lymph nodes."
    }
  ];

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-teal-900 text-white p-8 sm:p-12 shadow-xl">
        <div className="max-w-3xl space-y-4">
          <span className="inline-block bg-teal-500/20 text-teal-300 text-xs px-3 py-1 rounded-full font-semibold border border-teal-400/30">
            Empowering Community Healthcare & ASHA Workers
          </span>
          <h1 className="text-3xl sm:text-5xl font-black tracking-tight leading-tight">
            Simplifying Cancer Knowledge for Grassroots Care.
          </h1>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            OncoSathi AI transforms complex oncology terms, staging protocols, and biopsy reports into clear, compassionate, literacy-appropriate language in Simple English and সহজ বাংলা.
          </p>
          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={onStartSimplifier}
              className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold px-6 py-3 rounded-xl shadow-lg transition-transform hover:scale-105"
            >
              Start Medical Simplifier
            </button>
            <button
              onClick={onOpenDictionary}
              className="bg-white/10 hover:bg-white/20 text-white font-semibold px-5 py-3 rounded-xl border border-white/20 transition-colors"
            >
              Browse 252+ Oncology Terms
            </button>
          </div>
        </div>
      </div>

      {/* 4 Ingested Sources */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-lg font-bold text-slate-900">Grounded Knowledge Base (4 Ingested Primary Sources)</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-xs font-bold text-red-600 bg-red-100 px-2 py-0.5 rounded">PDF</span>
            <h4 className="font-bold text-sm text-slate-800 mt-2">1. IJPC Cancer Glossary</h4>
            <p className="text-xs text-slate-500 mt-1">4 extracted pages of oncology healthcare terminology.</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-xs font-bold text-blue-600 bg-blue-100 px-2 py-0.5 rounded">PDF</span>
            <h4 className="font-bold text-sm text-slate-800 mt-2">2. Medical Oncology (Ba)</h4>
            <p className="text-xs text-slate-500 mt-1">4 extracted slides of oncology presentation concepts.</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-xs font-bold text-amber-700 bg-amber-100 px-2 py-0.5 rounded">DOCX</span>
            <h4 className="font-bold text-sm text-slate-800 mt-2">3. Bengali-English Terms</h4>
            <p className="text-xs text-slate-500 mt-1">157 parallel medical terms with accurate Bengali translations.</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-xs font-bold text-emerald-600 bg-emerald-100 px-2 py-0.5 rounded">XLSX</span>
            <h4 className="font-bold text-sm text-slate-800 mt-2">4. Comprehensive Tables</h4>
            <p className="text-xs text-slate-500 mt-1">171 structured rows of oncology categories and symptoms.</p>
          </div>
        </div>
      </div>

      {/* Quick Prompts */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
        <h3 className="font-bold text-sm text-slate-700">Sample Medical Queries</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {samplePrompts.map((p, idx) => (
            <button
              key={idx}
              onClick={() => onSelectPrompt(p.text)}
              className="text-left p-3.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-teal-50 hover:border-teal-300 transition-all"
            >
              <div className="font-bold text-xs text-slate-800">{p.title}</div>
              <div className="text-[11px] text-slate-500 line-clamp-2 mt-1">{p.text}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
"""

# 2. pages/Simplify.tsx
files[SRC_DIR / "pages" / "Simplify.tsx"] = """import React, { useState } from 'react';
import { Language, SimplificationLevel, SimplifyResponse } from '../types';
import { simplifyText, sendFeedback } from '../services/api';
import { AudioPlayer } from '../components/AudioPlayer';
import { Disclaimer } from '../components/Disclaimer';

interface SimplifyProps {
  initialText?: string;
  targetLang: Language;
  setTargetLang: (lang: Language) => void;
  onSaveToHistory: (res: SimplifyResponse) => void;
}

export const Simplify: React.FC<SimplifyProps> = ({
  initialText = '',
  targetLang,
  setTargetLang,
  onSaveToHistory
}) => {
  const [inputText, setInputText] = useState(initialText);
  const [level, setLevel] = useState<SimplificationLevel>(2);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SimplifyResponse | null>(null);
  const [copied, setCopied] = useState(false);
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handleRun = async () => {
    if (!inputText.trim()) {
      setError('Please enter oncology text or question to simplify.');
      return;
    }
    setError(null);
    setLoading(true);
    setResult(null);
    setFeedbackSent(false);

    try {
      const data = await simplifyText(inputText, targetLang, level);
      setResult(data);
      onSaveToHistory(data);
    } catch (err: any) {
      setError(err.message || 'Simplification failed');
    } finally {
      setLoading(false);
    }
  };

  const copyText = () => {
    if (result) {
      navigator.clipboard.writeText(result.simplified_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Card */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900">Medical Information Simplifier</h2>
          <p className="text-xs sm:text-sm text-slate-500">Paste complex oncology reports, staging, or medical questions.</p>
        </div>

        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows={4}
          placeholder="Paste medical text here (e.g. 'Malignant neoplasms are characterized by uncontrolled cellular proliferation...')"
          className="w-full p-4 rounded-2xl border border-slate-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-200 outline-none text-sm text-slate-800"
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Language */}
          <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200 space-y-2">
            <label className="block text-xs font-bold text-slate-700 uppercase">Target Language</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setTargetLang('english')}
                className={`py-2 px-3 rounded-xl text-xs font-semibold ${targetLang === 'english' ? 'bg-white border-2 border-teal-500 text-teal-900 shadow-sm' : 'bg-slate-200 text-slate-600'}`}
              >
                Simple English
              </button>
              <button
                type="button"
                onClick={() => setTargetLang('bengali')}
                className={`py-2 px-3 rounded-xl text-xs font-semibold ${targetLang === 'bengali' ? 'bg-teal-600 text-white shadow-sm' : 'bg-slate-200 text-slate-600'}`}
              >
                সহজ বাংলা
              </button>
            </div>
          </div>

          {/* Level */}
          <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200 space-y-2">
            <label className="block text-xs font-bold text-slate-700 uppercase">Reading Level</label>
            <div className="grid grid-cols-3 gap-2">
              {[1, 2, 3].map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  onClick={() => setLevel(lvl as SimplificationLevel)}
                  className={`py-2 px-1 text-center rounded-xl text-xs font-bold ${level === lvl ? 'bg-white border-2 border-teal-500 text-teal-900 shadow-sm' : 'bg-slate-200 text-slate-600'}`}
                >
                  {lvl === 1 ? '1. Basic' : lvl === 2 ? '2. Easy' : '3. Detail'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && <div className="p-4 rounded-xl bg-red-50 text-red-700 text-xs">{error}</div>}

        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={() => setInputText('')}
            className="px-4 py-2.5 rounded-xl border border-slate-300 text-slate-600 hover:bg-slate-100 text-xs font-semibold"
          >
            Clear
          </button>
          <button
            type="button"
            disabled={loading || !inputText.trim()}
            onClick={handleRun}
            className="px-6 py-3 rounded-xl font-bold text-sm bg-teal-600 hover:bg-teal-500 text-white shadow-lg transition-transform hover:scale-105 disabled:bg-slate-300 disabled:cursor-not-allowed"
          >
            {loading ? 'Simplifying...' : 'Simplify Medical Information'}
          </button>
        </div>
      </div>

      {/* Result Card */}
      {result && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-teal-200 shadow-md space-y-6">
          <div className="flex justify-between items-center pb-4 border-b border-slate-100">
            <h3 className="font-black text-lg text-slate-900">Simplified Medical Explanation</h3>
            <span className="text-xs font-bold px-2.5 py-1 bg-teal-50 text-teal-800 rounded-md">
              Level {result.level} ({result.reading_level})
            </span>
          </div>

          <AudioPlayer text={result.simplified_text} language={result.language} />

          <div className="p-6 rounded-2xl bg-teal-50/50 border border-teal-200 text-slate-900 text-base leading-relaxed whitespace-pre-line">
            {result.simplified_text}
          </div>

          {result.key_points && result.key_points.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-xs font-bold uppercase text-slate-700">Key Points</h4>
              <ul className="space-y-1 text-xs sm:text-sm text-slate-700 list-disc list-inside">
                {result.key_points.map((kp, idx) => (
                  <li key={idx}>{kp}</li>
                ))}
              </ul>
            </div>
          )}

          <Disclaimer customText={result.disclaimer} />

          <div className="flex justify-between items-center pt-4 border-t border-slate-100">
            <button
              onClick={copyText}
              className="px-3 py-1.5 rounded-lg border text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700"
            >
              {copied ? 'Copied!' : 'Copy Explanation'}
            </button>
            {!feedbackSent ? (
              <div className="flex items-center space-x-2 text-xs">
                <span>Helpful for patient counseling?</span>
                <button
                  onClick={() => {
                    sendFeedback(inputText, result.simplified_text, true);
                    setFeedbackSent(true);
                  }}
                  className="px-2 py-1 bg-teal-50 text-teal-700 rounded hover:bg-teal-100 font-bold"
                >
                  Yes
                </button>
                <button
                  onClick={() => {
                    sendFeedback(inputText, result.simplified_text, false);
                    setFeedbackSent(true);
                  }}
                  className="px-2 py-1 bg-red-50 text-red-700 rounded hover:bg-red-100 font-bold"
                >
                  No
                </button>
              </div>
            ) : (
              <span className="text-xs text-teal-700 font-bold">Feedback recorded. Thank you!</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
"""

# 3. pages/Dictionary.tsx
files[SRC_DIR / "pages" / "Dictionary.tsx"] = """import React, { useState, useEffect } from 'react';
import { MedicalTermItem } from '../types';
import { searchTerms } from '../services/api';

export const Dictionary: React.FC = () => {
  const [terms, setTerms] = useState<MedicalTermItem[]>([]);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchList = async () => {
      setLoading(true);
      try {
        const list = await searchTerms(query, category);
        setTerms(list);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    const t = setTimeout(fetchList, 300);
    return () => clearTimeout(t);
  }, [query, category]);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900">Medical Terminology Dictionary</h2>
        <p className="text-xs sm:text-sm text-slate-500">252+ verified oncology terms extracted from 4 primary medical sources.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search oncology terms, abbreviations, Bengali words..."
            className="md:col-span-2 p-2.5 rounded-xl border border-slate-300 text-sm focus:border-teal-500 outline-none"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="p-2.5 rounded-xl border border-slate-300 text-sm bg-white"
          >
            <option value="All">All Categories</option>
            <option value="General Oncology">General Oncology</option>
            <option value="Diagnosis & Pathology">Diagnosis & Pathology</option>
            <option value="Treatment & Chemotherapy">Treatment & Chemotherapy</option>
            <option value="Anatomy & Staging">Anatomy & Staging</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading terms...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {terms.map((item) => (
            <div key={item.id} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
              <div className="flex justify-between items-start">
                <h3 className="font-bold text-base text-slate-900">{item.term}</h3>
                <span className="text-[10px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full">{item.category}</span>
              </div>
              {item.bengali_term && <div className="text-sm font-bold text-teal-700">বাংলা: {item.bengali_term}</div>}
              <div className="text-xs text-slate-600 line-clamp-3"><span className="font-semibold">Definition: </span>{item.definition}</div>
              {item.simple_meaning && (
                <div className="text-xs text-teal-900 bg-teal-50 p-2.5 rounded-xl"><span className="font-semibold">In simple words: </span>{item.simple_meaning}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
"""

# 4. pages/FieldGuide.tsx
files[SRC_DIR / "pages" / "FieldGuide.tsx"] = """import React from 'react';

export const FieldGuide: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900">ASHA Oncology Communication & Field Guide</h2>
        <p className="text-xs sm:text-sm text-slate-500">Practical counseling protocols and warning signs for community visits.</p>
      </div>

      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-red-200 shadow-sm space-y-4">
        <h3 className="font-black text-lg text-red-900">Cancer Warning Signs (C-A-U-T-I-O-N Protocol)</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {[
            { l: 'C', t: 'Change in bowel or bladder habits', b: 'মল বা মূত্রের অভ্যাসে দীর্ঘস্থায়ী পরিবর্তন।' },
            { l: 'A', t: 'A sore that does not heal', b: 'দীর্ঘদিনেও না সারা কোনো ক্ষত বা ঘা।' },
            { l: 'U', t: 'Unusual bleeding or discharge', b: 'অস্বাভাবিক রক্তপাত বা স্রাব নির্গমন।' },
            { l: 'T', t: 'Thickening or lump in breast / elsewhere', b: 'স্তন বা শরীরের যে কোনো অংশে চাকা।' },
            { l: 'I', t: 'Indigestion or difficulty in swallowing', b: 'খাবার গিলতে কষ্ট বা বদহজম।' },
            { l: 'O', t: 'Obvious change in wart or mole', b: 'তিল বা আঁচিলের আকার বা রঙের পরিবর্তন।' },
            { l: 'N', t: 'Nagging cough or hoarseness', b: 'টানা কাশি বা গলার স্বরের স্থায়ী পরিবর্তন।' },
          ].map((item, idx) => (
            <div key={idx} className="p-3.5 rounded-xl bg-red-50/50 border border-red-200">
              <div className="font-black text-red-700 text-lg">{item.l}</div>
              <div className="font-bold text-xs text-slate-800">{item.t}</div>
              <p className="text-[11px] text-slate-600 mt-1">{item.b}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
"""

# 5. pages/History.tsx
files[SRC_DIR / "pages" / "History.tsx"] = """import React from 'react';
import { HistoryItem } from '../types';

interface HistoryProps {
  history: HistoryItem[];
  onClear: () => void;
  onSelect: (item: HistoryItem) => void;
}

export const History: React.FC<HistoryProps> = ({ history, onClear, onSelect }) => {
  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900">Session History</h2>
          <p className="text-xs sm:text-sm text-slate-500">Past medical simplifications from this session.</p>
        </div>
        {history.length > 0 && (
          <button
            onClick={onClear}
            className="text-xs text-red-600 hover:text-red-700 font-semibold px-3 py-1.5 rounded-lg border border-red-200 hover:bg-red-50"
          >
            Clear History
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="p-12 text-center text-slate-400">No previous simplifications saved yet.</div>
      ) : (
        <div className="space-y-3">
          {history.map((item) => (
            <div key={item.id} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex justify-between text-xs text-slate-500">
                <span>{item.timestamp}</span>
                <span className="font-bold">{item.language} (Level {item.level})</span>
              </div>
              <div className="text-xs font-mono text-slate-600 line-clamp-1">Q: {item.originalText}</div>
              <div className="text-sm text-slate-800 line-clamp-2">{item.simplifiedText}</div>
              <button
                onClick={() => onSelect(item)}
                className="text-xs text-teal-700 font-bold hover:underline"
              >
                Reload in Simplifier →
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
"""

# 6. App.tsx
files[SRC_DIR / "App.tsx"] = """import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Simplify } from './pages/Simplify';
import { Dictionary } from './pages/Dictionary';
import { FieldGuide } from './pages/FieldGuide';
import { History } from './pages/History';
import { Language, HistoryItem, SimplifyResponse } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [targetLang, setTargetLang] = useState<Language>('english');
  const [queryText, setQueryText] = useState('');
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    try {
      const saved = localStorage.getItem('oncosathi_history');
      if (saved) setHistory(JSON.parse(saved));
    } catch (e) {}
  }, []);

  const handleSaveToHistory = (res: SimplifyResponse) => {
    const item: HistoryItem = {
      id: Date.now(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      originalText: res.original_text,
      simplifiedText: res.simplified_text,
      language: res.language,
      level: res.level,
      keyPoints: res.key_points || []
    };
    const updated = [item, ...history.slice(0, 19)];
    setHistory(updated);
    localStorage.setItem('oncosathi_history', JSON.stringify(updated));
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800 font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        targetLang={targetLang}
        setTargetLang={setTargetLang}
        historyCount={history.length}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'home' && (
          <Home
            onStartSimplifier={() => setActiveTab('simplify')}
            onOpenDictionary={() => setActiveTab('dictionary')}
            onSelectPrompt={(text) => {
              setQueryText(text);
              setActiveTab('simplify');
            }}
          />
        )}
        {activeTab === 'simplify' && (
          <Simplify
            initialText={queryText}
            targetLang={targetLang}
            setTargetLang={setTargetLang}
            onSaveToHistory={handleSaveToHistory}
          />
        )}
        {activeTab === 'dictionary' && <Dictionary />}
        {activeTab === 'guide' && <FieldGuide />}
        {activeTab === 'history' && (
          <History
            history={history}
            onClear={() => {
              setHistory([]);
              localStorage.removeItem('oncosathi_history');
            }}
            onSelect={(item) => {
              setQueryText(item.originalText);
              setTargetLang(item.language as Language);
              setActiveTab('simplify');
            }}
          />
        )}
      </main>

      <footer className="bg-white border-t border-slate-200 py-6 text-xs text-slate-500 text-center">
        OncoSathi AI — Simplifying Cancer Knowledge for Community Healthcare • Designed for ASHA Workers
      </footer>
    </div>
  );
};

export default App;
"""

# 7. main.tsx
files[SRC_DIR / "main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

# 8. index.css
files[SRC_DIR / "index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
}
"""

# Write all files
for p, content in files.items():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"Created: {p.relative_to(WORKSPACE)}")

print("All React pages & App created successfully!")
