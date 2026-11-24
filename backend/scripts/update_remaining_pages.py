# -*- coding: utf-8 -*-
"""
Update remaining frontend/src pages (Dictionary.tsx, FieldGuide.tsx, History.tsx)
to match the human-designed healthcare design system.
"""
from pathlib import Path

WORKSPACE = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi")
SRC = WORKSPACE / "frontend" / "src"

DICT_CONTENT = """import React, { useState, useEffect } from 'react';
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
    const t = setTimeout(fetchList, 250);
    return () => clearTimeout(t);
  }, [query, category]);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 border border-[#E3E8E5]">
        <h2 className="text-lg font-semibold text-[#202A2A]">Medical Terminology Reference</h2>
        <p className="text-xs text-[#586563] mt-1">
          252 verified oncology terms indexed from the 4 primary medical sources with patient-friendly explanations.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
          <div className="md:col-span-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search terminology (e.g., Biopsy, Carcinoma, বায়োপসি)..."
              className="w-full px-3 py-2 text-sm rounded-md border border-[#E3E8E5] focus:outline-none focus:border-[#176B63] focus:ring-1 focus:ring-[#176B63] bg-white text-[#202A2A]"
            />
          </div>
          <div>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 text-sm rounded-md border border-[#E3E8E5] focus:outline-none focus:border-[#176B63] bg-white text-[#202A2A]"
            >
              <option value="All">All Categories</option>
              <option value="General Oncology">General Oncology</option>
              <option value="Diagnosis & Pathology">Diagnosis & Pathology</option>
              <option value="Treatment & Chemotherapy">Treatment & Chemotherapy</option>
              <option value="Anatomy & Staging">Anatomy & Staging</option>
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="bg-white rounded-lg p-12 text-center text-[#586563] border border-[#E3E8E5] text-sm">
          Searching terminology dictionary...
        </div>
      ) : terms.length === 0 ? (
        <div className="bg-white rounded-lg p-12 text-center text-[#586563] border border-[#E3E8E5] text-sm">
          No medical terms matched &quot;{query}&quot;. Try searching for common terms like biopsy, stage, metastasis, or tumor.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {terms.map((item) => (
            <div key={item.id} className="bg-white p-5 rounded-lg border border-[#E3E8E5] space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start gap-2">
                  <h3 className="font-semibold text-base text-[#202A2A]">{item.term}</h3>
                  <span className="text-[11px] bg-slate-100 text-[#586563] px-2 py-0.5 rounded font-medium border border-[#E3E8E5] shrink-0">
                    {item.category}
                  </span>
                </div>

                {item.bengali_term && (
                  <div className="text-sm font-medium text-[#176B63] mt-1 font-serif">
                    বাংলা: {item.bengali_term}
                  </div>
                )}

                <div className="text-xs text-[#586563] mt-2.5 leading-relaxed">
                  <span className="font-semibold text-[#202A2A]">Clinical Definition: </span>
                  {item.definition}
                </div>
              </div>

              {item.simple_meaning && (
                <div className="text-xs text-[#176B63] bg-[#EBF3F2] p-3 rounded-md border border-[#D5E6E4] leading-relaxed">
                  <span className="font-semibold text-[#124E49]">How to explain to family: </span>
                  {item.simple_meaning}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
"""

FIELD_GUIDE_CONTENT = """import React from 'react';

export const FieldGuide: React.FC = () => {
  const cautionSigns = [
    { letter: 'C', title: 'Change in bowel or bladder habits', bengali: 'মল বা মূত্রের অভ্যাসে দীর্ঘস্থায়ী পরিবর্তন।', detail: 'Chronic diarrhea, constipation, or change in stool caliber lasting weeks.' },
    { letter: 'A', title: 'A sore that does not heal', bengali: 'দীর্ঘদিনেও না সারা কোনো ক্ষত বা ঘা।', detail: 'Oral sores, skin ulcers, or lesions that do not heal with ordinary ointment.' },
    { letter: 'U', title: 'Unusual bleeding or discharge', bengali: 'অস্বাভাবিক রক্তপাত বা স্রাব নির্গমন।', detail: 'Post-menopausal bleeding, bleeding between cycles, blood in sputum or stool.' },
    { letter: 'T', title: 'Thickening or lump in breast or elsewhere', bengali: 'স্তন বা শরীরের যে কোনো অংশে শক্ত চাকা বা পিণ্ড।', detail: 'Painless hard lump in breast, underarm, groin, or neck lymph nodes.' },
    { letter: 'I', title: 'Indigestion or difficulty in swallowing', bengali: 'খাবার গিলতে কষ্ট বা বদহজম।', detail: 'Persistent dysphagia (food getting stuck), feeling full after small meals.' },
    { letter: 'O', title: 'Obvious change in wart or mole', bengali: 'তিল বা আঁচিলের আকার, রং বা আকারে অস্বাভাবিক পরিবর্তন।', detail: 'Asymmetry, border irregularity, color change, diameter > 6mm.' },
    { letter: 'N', title: 'Nagging cough or hoarseness', bengali: 'টানা কাশি বা গলার স্বরের স্থায়ী কর্কশতা।', detail: 'Cough lasting more than 3 weeks without infection, persistent voice change.' },
  ];

  const counselingPrinciples = [
    {
      title: '1. Establish Trust & Listen Actively',
      desc: 'Patients and families in rural communities often fear cancer diagnosis as an immediate death sentence. Allow them to express fears without interruption before introducing clinical terms.',
    },
    {
      title: '2. Demystify the Word "Biopsy"',
      desc: 'Many believe taking a sample makes cancer spread faster. Reassure them: "Biopsy is only a tiny test to identify the exact germ or cell type so doctors can prescribe the correct medication."',
    },
    {
      title: '3. Explain Staging Constructively',
      desc: 'Stage 1 or 2 means the condition is localized and has very high cure rates. Even for advanced stages, treatment eases suffering and extends comfortable life.',
    },
    {
      title: '4. Encourage Timely Referral to PHC',
      desc: 'Never prescribe or modify cancer treatments yourself. Help the patient arrange transportation, government health cards (e.g., Swasthya Sathi / Ayushman Bharat), and escort them to the medical officer.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg p-6 border border-[#E3E8E5]">
        <h2 className="text-lg font-semibold text-[#202A2A]">ASHA Oncology Field Guide</h2>
        <p className="text-xs text-[#586563] mt-1">
          Standardized counseling protocols, CAUTION early warning signs, and patient navigation guidelines for village visits.
        </p>
      </div>

      {/* CAUTION Protocol */}
      <div className="bg-white rounded-lg p-6 border border-[#E3E8E5] space-y-4">
        <div>
          <span className="text-[11px] font-semibold text-[#A33B32] uppercase tracking-wider bg-red-50 px-2 py-0.5 rounded border border-red-200">
            Early Detection Protocol
          </span>
          <h3 className="text-base font-semibold text-[#202A2A] mt-2">
            The C-A-U-T-I-O-N Cancer Warning Signs
          </h3>
          <p className="text-xs text-[#586563] mt-0.5">
            Memorize these 7 standard clinical flags. If a community member exhibits any symptom persisting over 2–3 weeks, advise prompt evaluation by a Medical Officer.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
          {cautionSigns.map((sign, idx) => (
            <div key={idx} className="p-3.5 rounded-md border border-[#E3E8E5] bg-[#F7F8F6] flex gap-3.5 items-start">
              <div className="w-8 h-8 rounded bg-[#176B63] text-white font-bold flex items-center justify-center shrink-0 text-sm">
                {sign.letter}
              </div>
              <div className="space-y-1">
                <div className="font-semibold text-xs text-[#202A2A]">{sign.title}</div>
                <div className="text-xs text-[#176B63] font-medium font-serif">{sign.bengali}</div>
                <p className="text-[11px] text-[#586563] leading-relaxed">{sign.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Counseling Guidelines */}
      <div className="bg-white rounded-lg p-6 border border-[#E3E8E5] space-y-4">
        <h3 className="text-base font-semibold text-[#202A2A]">
          Compassionate Patient Communication Guidelines
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {counselingPrinciples.map((rule, idx) => (
            <div key={idx} className="p-4 rounded-md border border-[#E3E8E5] bg-white space-y-1.5">
              <h4 className="text-xs font-semibold text-[#202A2A]">{rule.title}</h4>
              <p className="text-xs text-[#586563] leading-relaxed">{rule.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
"""

HISTORY_CONTENT = """import React from 'react';
import { HistoryItem } from '../types';

interface HistoryProps {
  history: HistoryItem[];
  onClear: () => void;
  onSelect: (item: HistoryItem) => void;
}

export const History: React.FC<HistoryProps> = ({ history, onClear, onSelect }) => {
  return (
    <div className="bg-white rounded-lg p-6 border border-[#E3E8E5] space-y-5">
      <div className="flex justify-between items-center pb-4 border-b border-[#E3E8E5]">
        <div>
          <h2 className="text-lg font-semibold text-[#202A2A]">Session History</h2>
          <p className="text-xs text-[#586563] mt-0.5">
            Previous medical simplifications from your current browser session.
          </p>
        </div>
        {history.length > 0 && (
          <button
            onClick={onClear}
            className="text-xs text-[#A33B32] hover:text-red-700 font-medium px-3 py-1.5 rounded-md border border-red-200 hover:bg-red-50 transition-colors"
          >
            Clear History
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="py-12 text-center text-[#586563] text-sm">
          No previous simplifications saved yet in this session.
        </div>
      ) : (
        <div className="space-y-3">
          {history.map((item) => (
            <div key={item.id} className="p-4 rounded-md border border-[#E3E8E5] bg-[#F7F8F6] space-y-2">
              <div className="flex justify-between items-center text-xs text-[#586563]">
                <span>{item.timestamp}</span>
                <span className="font-medium bg-white px-2 py-0.5 rounded border border-[#E3E8E5] text-[#202A2A] capitalize">
                  {item.language} · Level {item.level}
                </span>
              </div>
              <div className="text-xs text-[#586563] line-clamp-1">
                <span className="font-semibold text-[#202A2A]">Original: </span>
                {item.originalText}
              </div>
              <div className="text-xs text-[#202A2A] line-clamp-2 leading-relaxed">
                <span className="font-semibold text-[#176B63]">Simplified: </span>
                {item.simplifiedText}
              </div>
              <div className="pt-1">
                <button
                  onClick={() => onSelect(item)}
                  className="text-xs text-[#176B63] hover:text-[#124E49] font-medium hover:underline inline-flex items-center gap-1"
                >
                  Load in Simplifier →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
"""

(SRC / "pages" / "Dictionary.tsx").write_text(DICT_CONTENT, encoding="utf-8")
(SRC / "pages" / "FieldGuide.tsx").write_text(FIELD_GUIDE_CONTENT, encoding="utf-8")
(SRC / "pages" / "History.tsx").write_text(HISTORY_CONTENT, encoding="utf-8")

print("Successfully updated Dictionary.tsx, FieldGuide.tsx, History.tsx!")
