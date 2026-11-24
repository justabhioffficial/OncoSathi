# -*- coding: utf-8 -*-
"""
Update frontend/src modular React/TypeScript files to match the new human-designed UI.
"""
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
SRC = WORKSPACE / "frontend" / "src"

files = {}

# 1. Navbar.tsx
files[SRC / "components" / "Navbar.tsx"] = """import React from 'react';
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
    <header className="bg-white border-b border-[#E3E8E5] sticky top-0 z-40">
      <div className="max-w-5xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          
          <div 
            className="flex items-center space-x-3 cursor-pointer select-none"
            onClick={() => setActiveTab('home')}
          >
            <div className="w-8 h-8 rounded-lg bg-[#176B63] flex items-center justify-center text-white text-sm font-semibold">
              +
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-lg text-[#202A2A] tracking-tight">OncoSathi</span>
              <span className="text-[11px] text-[#586563] bg-slate-100 px-2 py-0.5 rounded font-medium border border-[#E3E8E5]">ASHA Tool</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center space-x-1 text-sm font-medium text-[#586563]">
            {[
              { id: 'home', label: 'Home' },
              { id: 'simplify', label: 'Simplify Text' },
              { id: 'dictionary', label: 'Dictionary' },
              { id: 'guide', label: 'Field Guide' },
              { id: 'history', label: `History ${historyCount > 0 ? `(${historyCount})` : ''}` },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3 py-1.5 rounded-md transition-colors ${
                  activeTab === tab.id
                    ? 'text-[#176B63] bg-[#EBF3F2] font-semibold'
                    : 'hover:text-[#202A2A]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          <div className="flex items-center space-x-3">
            <div className="flex bg-slate-100 p-0.5 rounded-md border border-[#E3E8E5] text-xs font-medium">
              <button
                onClick={() => setTargetLang('english')}
                className={`px-2.5 py-1 rounded transition-colors ${
                  targetLang === 'english'
                    ? 'bg-white text-[#176B63] font-semibold shadow-sm'
                    : 'text-[#586563] hover:text-[#202A2A]'
                }`}
              >
                English
              </button>
              <button
                onClick={() => setTargetLang('bengali')}
                className={`px-2.5 py-1 rounded transition-colors font-serif ${
                  targetLang === 'bengali'
                    ? 'bg-[#176B63] text-white font-semibold shadow-sm'
                    : 'text-[#586563] hover:text-[#202A2A]'
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

# 2. AudioPlayer.tsx
files[SRC / "components" / "AudioPlayer.tsx"] = """import React, { useState } from 'react';

interface AudioPlayerProps {
  text: string;
  language: string;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ text, language }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const playSpeech = () => {
    if (!('speechSynthesis' in window)) {
      alert('Your browser does not support audio speech output.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const isBn = language === 'bengali' || language === 'bn' || /[\\u0980-\\u09FF]/.test(text);
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
    <div className="flex items-center justify-between p-2.5 bg-[#F7F8F6] rounded border border-[#E3E8E5] text-xs">
      <div className="flex items-center space-x-2 text-[#586563]">
        <span className="font-medium">Audio explanation ({language === 'bengali' ? 'বাংলা কন্ঠ' : 'English Voice'}):</span>
      </div>
      <div className="flex items-center space-x-1.5">
        {!isPlaying ? (
          <button
            onClick={playSpeech}
            className="px-2.5 py-1 bg-[#176B63] hover:bg-[#124E49] text-white rounded font-medium text-xs transition-colors"
          >
            Play audio
          </button>
        ) : (
          <>
            <button
              onClick={pauseSpeech}
              className="px-2 py-1 bg-slate-200 text-[#202A2A] rounded text-xs font-medium"
            >
              {isPaused ? 'Resume' : 'Pause'}
            </button>
            <button
              onClick={stopSpeech}
              className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs font-medium"
            >
              Stop
            </button>
          </>
        )}
      </div>
    </div>
  );
};
"""

# 3. Disclaimer.tsx
files[SRC / "components" / "Disclaimer.tsx"] = """import React from 'react';

interface DisclaimerProps {
  customText?: string;
}

export const Disclaimer: React.FC<DisclaimerProps> = ({ customText }) => {
  return (
    <div className="p-3 bg-slate-50 border border-[#E3E8E5] rounded text-[11px] text-[#586563] leading-relaxed">
      <strong className="text-[#202A2A]">Medical Notice:</strong>{' '}
      {customText ||
        "OncoSathi provides educational simplifications grounded in verified sources. It does not replace certified physician evaluation, clinical diagnosis, or prescriptions."}
    </div>
  );
};
"""

# 4. Home.tsx
files[SRC / "pages" / "Home.tsx"] = """import React from 'react';

interface HomeProps {
  onStartSimplifier: () => void;
  onOpenDictionary: () => void;
  onSelectPrompt: (text: string) => void;
}

export const Home: React.FC<HomeProps> = ({ onStartSimplifier, onOpenDictionary, onSelectPrompt }) => {
  return (
    <div className="space-y-10">
      {/* Editorial Introduction */}
      <div className="border-b border-[#E3E8E5] pb-8 space-y-4">
        <h1 className="text-2xl sm:text-3xl font-semibold text-[#202A2A] tracking-tight leading-snug">
          Understand medical information.<br />
          Explain it simply.
        </h1>
        <p className="text-[#586563] text-sm sm:text-base max-w-2xl leading-relaxed">
          OncoSathi helps community healthcare workers understand cancer-related reports, doctor notes, and staging terminology, and communicate them in clear language to patients and families.
        </p>
        <div className="pt-2 flex flex-wrap gap-3">
          <button
            onClick={onStartSimplifier}
            className="px-4 py-2.5 bg-[#176B63] hover:bg-[#124E49] text-white text-sm font-medium rounded-lg transition-colors"
          >
            Simplify medical text →
          </button>
          <button
            onClick={onOpenDictionary}
            className="px-4 py-2.5 bg-white hover:bg-slate-50 text-[#202A2A] border border-[#E3E8E5] text-sm font-medium rounded-lg transition-colors"
          >
            Browse oncology dictionary
          </button>
        </div>
      </div>

      {/* 3 Step Practical Workflow */}
      <div className="space-y-3">
        <h2 className="text-xs font-semibold text-[#586563] uppercase tracking-wider">How the tool works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-1">
          <div className="space-y-1.5">
            <div className="text-xs font-semibold text-[#176B63]">1. Input medical notes</div>
            <p className="text-xs text-[#586563] leading-relaxed">
              Paste pathology findings, doctor notes, or enter a question asked by a patient.
            </p>
          </div>
          <div className="space-y-1.5">
            <div className="text-xs font-semibold text-[#176B63]">2. Select audience level</div>
            <p className="text-xs text-[#586563] leading-relaxed">
              Choose Simple English or সহজ বাংলা, and select Basic, Community, or Detailed summaries.
            </p>
          </div>
          <div className="space-y-1.5">
            <div className="text-xs font-semibold text-[#176B63]">3. Review and counsel</div>
            <p className="text-xs text-[#586563] leading-relaxed">
              Get clear explanations with key points, verified definitions, and spoken audio output.
            </p>
          </div>
        </div>
      </div>

      {/* 4 Sources Panel */}
      <div className="bg-white rounded-lg border border-[#E3E8E5] p-5 space-y-4">
        <div className="pb-3 border-b border-[#E3E8E5]">
          <h3 className="text-sm font-semibold text-[#202A2A]">Grounded Medical Knowledge Base</h3>
          <p className="text-xs text-[#586563]">All explanations are strictly referenced against four primary oncology sources.</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div className="p-3 bg-[#F7F8F6] rounded border border-[#E3E8E5]">
            <div className="font-semibold text-[#202A2A]">1. IJPC Cancer Glossary</div>
            <p className="text-[#586563] mt-0.5">Foundational oncology definitions and patient terminology.</p>
          </div>
          <div className="p-3 bg-[#F7F8F6] rounded border border-[#E3E8E5]">
            <div className="font-semibold text-[#202A2A]">2. Medical Oncology Terminology (Ba)</div>
            <p className="text-[#586563] mt-0.5">Clinical staging protocols and chemotherapy concepts.</p>
          </div>
          <div className="p-3 bg-[#F7F8F6] rounded border border-[#E3E8E5]">
            <div className="font-semibold text-[#202A2A]">3. Cancer Terminology Bengali-English</div>
            <p className="text-[#586563] mt-0.5">157 bilingual parallel records with authentic Bengali medical translations.</p>
          </div>
          <div className="p-3 bg-[#F7F8F6] rounded border border-[#E3E8E5]">
            <div className="font-semibold text-[#202A2A]">4. Comprehensive Oncology Tables</div>
            <p className="text-[#586563] mt-0.5">171 structured rows across diagnostic workup and classifications.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
"""

# 5. Simplify.tsx
files[SRC / "pages" / "Simplify.tsx"] = """import React, { useState } from 'react';
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
      setError('Please enter oncology text or a question to simplify.');
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
    <div className="space-y-8">
      {/* Input Workspace */}
      <div className="bg-white rounded-lg border border-[#E3E8E5] p-5 sm:p-6 space-y-5 shadow-sm">
        <div className="flex items-center justify-between pb-3 border-b border-[#E3E8E5]">
          <h2 className="text-base font-semibold text-[#202A2A]">Medical Text Simplifier</h2>
          <span className="text-xs text-[#586563]">Grounded in 4 verified sources</span>
        </div>

        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-[#202A2A]">Enter or paste medical text</label>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={4}
            placeholder="Paste medical report, histology finding, or doctor notes here..."
            className="w-full p-3 rounded-lg border border-[#E3E8E5] text-sm text-[#202A2A] leading-relaxed resize-y"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-[#202A2A]">Output Language</label>
            <div className="flex bg-[#F7F8F6] p-1 rounded-md border border-[#E3E8E5] text-xs font-medium">
              <button
                type="button"
                onClick={() => setTargetLang('english')}
                className={`flex-1 py-1.5 text-center rounded transition-colors ${
                  targetLang === 'english' ? 'bg-white text-[#176B63] font-semibold shadow-sm' : 'text-[#586563]'
                }`}
              >
                Simple English
              </button>
              <button
                type="button"
                onClick={() => setTargetLang('bengali')}
                className={`flex-1 py-1.5 text-center rounded transition-colors ${
                  targetLang === 'bengali' ? 'bg-[#176B63] text-white font-semibold shadow-sm' : 'text-[#586563]'
                }`}
              >
                সহজ বাংলা
              </button>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-[#202A2A]">Explanation Level</label>
            <div className="flex bg-[#F7F8F6] p-1 rounded-md border border-[#E3E8E5] text-xs font-medium">
              {[1, 2, 3].map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  onClick={() => setLevel(lvl as SimplificationLevel)}
                  className={`flex-1 py-1.5 text-center rounded transition-colors ${
                    level === lvl ? 'bg-white text-[#176B63] font-semibold shadow-sm' : 'text-[#586563]'
                  }`}
                >
                  {lvl === 1 ? 'Basic' : lvl === 2 ? 'Easy' : 'Detailed'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && <div className="p-3 rounded bg-red-50 text-red-700 text-xs border border-red-200">{error}</div>}

        <div className="flex justify-between items-center pt-2 border-t border-[#E3E8E5]">
          <button
            type="button"
            onClick={() => setInputText('')}
            className="text-xs text-[#586563] hover:text-[#202A2A]"
          >
            Clear input
          </button>
          <button
            type="button"
            disabled={loading || !inputText.trim()}
            onClick={handleRun}
            className="px-5 py-2 text-sm font-medium rounded-lg bg-[#176B63] hover:bg-[#124E49] text-white transition-colors disabled:bg-slate-200 disabled:text-[#586563] disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : 'Simplify explanation'}
          </button>
        </div>
      </div>

      {/* Result Display */}
      {result && (
        <div className="bg-white rounded-lg border border-[#E3E8E5] p-6 space-y-6 shadow-sm">
          <div className="flex justify-between items-center pb-3 border-b border-[#E3E8E5]">
            <h3 className="font-semibold text-base text-[#202A2A]">Simplified Explanation</h3>
            <span className="text-xs font-medium px-2 py-0.5 bg-[#F7F8F6] rounded border border-[#E3E8E5]">
              Level {result.level} ({result.reading_level})
            </span>
          </div>

          <AudioPlayer text={result.simplified_text} language={result.language} />

          <div className="p-4 bg-[#F7F8F6] rounded-lg border border-[#E3E8E5] text-[#202A2A] text-sm sm:text-base leading-relaxed whitespace-pre-line">
            {result.simplified_text}
          </div>

          {result.key_points && result.key_points.length > 0 && (
            <div className="space-y-1.5">
              <h4 className="text-xs font-semibold text-[#586563] uppercase tracking-wider">Key Points</h4>
              <ul className="space-y-1 text-xs sm:text-sm text-[#202A2A] list-disc list-inside">
                {result.key_points.map((kp, idx) => (
                  <li key={idx}>{kp}</li>
                ))}
              </ul>
            </div>
          )}

          <Disclaimer customText={result.disclaimer} />

          <div className="flex justify-between items-center pt-3 border-t border-[#E3E8E5] text-xs">
            <button
              onClick={copyText}
              className="px-3 py-1.5 rounded border border-[#E3E8E5] bg-[#F7F8F6] text-[#202A2A] font-medium hover:bg-slate-200"
            >
              {copied ? 'Copied' : 'Copy explanation'}
            </button>
            {!feedbackSent ? (
              <div className="flex items-center space-x-2 text-[#586563]">
                <span>Helpful for counseling?</span>
                <button
                  onClick={() => {
                    sendFeedback(inputText, result.simplified_text, true);
                    setFeedbackSent(true);
                  }}
                  className="px-2 py-1 bg-[#F7F8F6] border border-[#E3E8E5] rounded hover:bg-slate-200 text-[#202A2A]"
                >
                  Yes
                </button>
                <button
                  onClick={() => {
                    sendFeedback(inputText, result.simplified_text, false);
                    setFeedbackSent(true);
                  }}
                  className="px-2 py-1 bg-[#F7F8F6] border border-[#E3E8E5] rounded hover:bg-slate-200 text-[#202A2A]"
                >
                  No
                </button>
              </div>
            ) : (
              <span className="text-[#176B63] font-medium">Feedback recorded.</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
"""

# Write all files
for p, content in files.items():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"Updated: {p.relative_to(WORKSPACE)}")

print("All modular frontend files updated cleanly!")
