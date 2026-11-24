# -*- coding: utf-8 -*-
"""
Generate complete modular TypeScript/React frontend files for Vite + Tailwind + Lucide.
"""
import os
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
FRONTEND_DIR = WORKSPACE / "frontend"
SRC_DIR = FRONTEND_DIR / "src"

files = {}

# 1. types/index.ts
files[SRC_DIR / "types" / "index.ts"] = """// TypeScript type definitions for OncoSathi AI
export type Language = 'english' | 'bengali';
export type SimplificationLevel = 1 | 2 | 3;

export interface SourceReference {
  source_document: string;
  document_title?: string;
  section_or_page?: string;
  chunk_text: string;
  similarity_score?: number;
  category?: string;
}

export interface TermExplanation {
  term: string;
  simple_meaning: string;
  bengali_term?: string;
  category?: string;
}

export interface SimplifyResponse {
  simplified_text: string;
  original_text: string;
  language: string;
  level: number;
  reading_level: string;
  key_points: string[];
  terms_explained: TermExplanation[];
  sources: SourceReference[];
  disclaimer: string;
  confidence_score: number;
}

export interface MedicalTermItem {
  id: string;
  term: string;
  definition: string;
  simple_meaning?: string;
  bengali_term?: string;
  category: string;
  source_document: string;
  abbreviation?: string;
}

export interface HistoryItem {
  id: number;
  timestamp: string;
  originalText: string;
  simplifiedText: string;
  language: string;
  level: number;
  keyPoints: string[];
}
"""

# 2. services/api.ts
files[SRC_DIR / "services" / "api.ts"] = """// API Client for OncoSathi Backend
import { SimplifyResponse, MedicalTermItem, Language, SimplificationLevel } from '../types';

const API_BASE = (import.meta as any).env?.VITE_API_BASE || '';

export const simplifyText = async (
  text: string,
  targetLanguage: Language,
  simplificationLevel: SimplificationLevel
): Promise<SimplifyResponse> => {
  const res = await fetch(`${API_BASE}/api/simplify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      target_language: targetLanguage,
      simplification_level: simplificationLevel
    })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to simplify medical text');
  }
  return res.json();
};

export const searchTerms = async (query: string = '', category: string = ''): Promise<MedicalTermItem[]> => {
  let url = `${API_BASE}/api/terms/search?q=${encodeURIComponent(query)}`;
  if (category && category !== 'All') {
    url += `&category=${encodeURIComponent(category)}`;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch terms');
  const data = await res.json();
  return data.terms || [];
};

export const sendFeedback = async (
  queryText: string,
  simplifiedText: string,
  isHelpful: boolean,
  rating: number = 5
) => {
  return fetch(`${API_BASE}/api/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query_text: queryText,
      simplified_text: simplifiedText,
      is_helpful: isHelpful,
      rating,
      feedback_type: 'asha_simplification'
    })
  });
};
"""

# 3. components/Navbar.tsx
files[SRC_DIR / "components" / "Navbar.tsx"] = """import React from 'react';
import { Language } from '../types';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  targetLang: Language;
  setTargetLang: (lang: Language) => void;
  historyCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  targetLang,
  setTargetLang,
  historyCount
}) => {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          
          {/* Logo */}
          <div 
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => setActiveTab('home')}
          >
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-tr from-teal-600 to-cyan-400 flex items-center justify-center text-white shadow-md shadow-teal-500/20 group-hover:scale-105 transition-transform">
              <span className="text-xl sm:text-2xl">❤️</span>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-xl sm:text-2xl tracking-tight text-slate-900">
                  Onco<span className="text-teal-600">Sathi</span>
                </span>
                <span className="bg-teal-100 text-teal-800 text-xs px-2 py-0.5 rounded-full font-semibold border border-teal-200">
                  AI for ASHA
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                Simplifying Cancer Knowledge for Community Healthcare • <span className="font-serif font-medium text-teal-700">অনকোসাথী এআই</span>
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
            {[
              { id: 'home', label: 'Home' },
              { id: 'simplify', label: 'Simplifier' },
              { id: 'dictionary', label: 'Medical Dictionary' },
              { id: 'guide', label: 'ASHA Field Guide' },
              { id: 'history', label: `History ${historyCount > 0 ? `(${historyCount})` : ''}` },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3 py-2 rounded-lg font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'bg-teal-50 text-teal-700 font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          {/* Language Toggle */}
          <div className="flex items-center space-x-2">
            <div className="flex bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-medium">
              <button
                onClick={() => setTargetLang('english')}
                className={`px-2.5 py-1 rounded-md transition-all ${
                  targetLang === 'english'
                    ? 'bg-white shadow text-teal-900 font-bold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                English
              </button>
              <button
                onClick={() => setTargetLang('bengali')}
                className={`px-2.5 py-1 rounded-md transition-all font-serif ${
                  targetLang === 'bengali'
                    ? 'bg-teal-600 shadow text-white font-bold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                বাংলা
              </button>
            </div>
          </div>

        </div>
      </div>
    </header>
  );
};
"""

# 4. components/AudioPlayer.tsx
files[SRC_DIR / "components" / "AudioPlayer.tsx"] = """import React, { useState } from 'react';

interface AudioPlayerProps {
  text: string;
  language: string;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ text, language }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const playSpeech = () => {
    if (!('speechSynthesis' in window)) {
      alert('Your browser does not support Web Speech Text-to-Speech.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const isBn = language === 'bengali' || /[\\u0980-\\u09FF]/.test(text);
    utterance.lang = isBn ? 'bn-IN' : 'en-IN';
    utterance.rate = isBn ? 0.85 : 0.95;

    const voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
      const match = voices.find(v => isBn ? v.lang.startsWith('bn') : v.lang.startsWith('en'));
      if (match) utterance.voice = match;
    }

    utterance.onstart = () => { setIsPlaying(true); setIsPaused(false); };
    utterance.onend = () => { setIsPlaying(false); setIsPaused(false); };
    utterance.onerror = () => { setIsPlaying(false); setIsPaused(false); };

    window.speechSynthesis.speak(utterance);
  };

  const pauseSpeech = () => {
    if (window.speechSynthesis.speaking && !isPaused) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    } else if (isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    }
  };

  const stopSpeech = () => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
    setIsPaused(false);
  };

  return (
    <div className="flex items-center justify-between bg-white p-2.5 px-4 rounded-xl border border-teal-200/60 shadow-sm text-xs">
      <div className="flex items-center space-x-2">
        <span className="text-teal-600 font-bold">🔊</span>
        <span className="font-semibold text-slate-700">
          Listen to Audio Explanation ({language === 'bengali' ? 'বাংলা কন্ঠ' : 'Spoken English'}):
        </span>
      </div>
      <div className="flex items-center space-x-1.5">
        {!isPlaying ? (
          <button
            onClick={playSpeech}
            className="px-3 py-1 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-bold flex items-center space-x-1 transition-all"
          >
            <span>▶ Play Audio</span>
          </button>
        ) : (
          <>
            <button
              onClick={pauseSpeech}
              className="px-2.5 py-1 rounded-lg bg-amber-500 text-white font-bold text-xs"
            >
              {isPaused ? '▶ Resume' : '⏸ Pause'}
            </button>
            <button
              onClick={stopSpeech}
              className="px-2.5 py-1 rounded-lg bg-red-500 text-white font-bold text-xs"
            >
              ⏹ Stop
            </button>
          </>
        )}
      </div>
    </div>
  );
};
"""

# 5. components/Disclaimer.tsx
files[SRC_DIR / "components" / "Disclaimer.tsx"] = """import React from 'react';

interface DisclaimerProps {
  customText?: string;
}

export const Disclaimer: React.FC<DisclaimerProps> = ({ customText }) => {
  return (
    <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/80 text-amber-900 text-xs flex items-start space-x-2.5">
      <span className="text-amber-600 text-base">⚠️</span>
      <div className="space-y-1">
        <span className="font-bold">Medical Safety Notice for ASHA Workers:</span>
        <p className="leading-relaxed text-amber-800/90">
          {customText ||
            "This simplified explanation is strictly for educational guidance and patient communication. It is not a clinical prescription or medical diagnosis. Please direct patients to a certified oncologist or Medical Officer at the Primary Health Centre for diagnostic confirmation and clinical treatment decisions."}
        </p>
      </div>
    </div>
  );
};
"""

# 6. vite.config.ts
files[FRONTEND_DIR / "vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
});
"""

# 7. tailwind.config.js
files[FRONTEND_DIR / "tailwind.config.js"] = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
        }
      }
    },
  },
  plugins: [],
}
"""

# 8. postcss.config.js
files[FRONTEND_DIR / "postcss.config.js"] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

# Write all files
for p, content in files.items():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"Created: {p.relative_to(WORKSPACE)}")

print("All modular frontend files created successfully!")
