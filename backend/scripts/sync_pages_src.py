# -*- coding: utf-8 -*-
from pathlib import Path

SRC = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\frontend\src")

about_code = """import React from 'react';

export const About: React.FC = () => {
  return (
    <div className="py-8 sm:py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 space-y-8">
        <div>
          <div className="text-xs font-semibold text-[#246B64] uppercase tracking-wider mb-1">
            Platform Overview
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[#263B39]">
            About OncoSathi
          </h1>
          <p className="text-sm text-[#6E7C76] mt-1">
            Making cancer information easier to understand and share in community healthcare.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 rounded-xl bg-white border border-[#E2E8E3] space-y-2.5">
            <h3 className="text-base font-bold text-[#263B39]">The Problem</h3>
            <p className="text-xs sm:text-sm text-[#6E7C76] leading-relaxed">
              Oncology reports and cancer explanations are filled with intimidating clinical jargon—such as 
              metastasis, carcinoma, adjuvant, and histopathology. In rural and semi-rural communities in India, 
              this terminology creates extreme fear, delays in seeking treatment, and confusion for patients and families.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-white border border-[#E2E8E3] space-y-2.5">
            <h3 className="text-base font-bold text-[#263B39]">Our Purpose</h3>
            <p className="text-xs sm:text-sm text-[#6E7C76] leading-relaxed">
              OncoSathi bridges this communication gap. It equips ASHA (Accredited Social Health Activists) and community 
              health workers with grounded, simplified explanations in plain English and authentic Bengali (বাংলা), 
              preserving accurate medical meaning while removing confusing vocabulary.
            </p>
          </div>
        </div>

        <div className="p-3 bg-white rounded-xl border border-[#E2E8E3]">
          <img 
            src="/images/clinic_consultation.jpg" 
            alt="Doctor consultation in healthcare clinic" 
            className="w-full h-[260px] sm:h-[320px] object-cover rounded-lg"
          />
          <div className="p-3 text-xs text-[#6E7C76]">
            Community healthcare consultation: Bridging clinical expertise with patient empathy and understanding.
          </div>
        </div>

        <div className="p-6 sm:p-8 rounded-xl bg-white border border-[#E2E8E3] space-y-6">
          <div className="space-y-2">
            <h3 className="text-lg font-bold text-[#263B39]">How Knowledge Retrieval Works</h3>
            <p className="text-xs sm:text-sm text-[#6E7C76] leading-relaxed">
              When an ASHA worker inputs a medical excerpt or question, OncoSathi indexes and matches the query against 
              4 verified oncology reference sources (IJPC Cancer Glossary, Oncology Terminology Presentation, 
              Medical Terminology DOCX, and Oncology Comprehensive Tables). The matched chunks are passed through a 
              rigorous simplification pipeline that generates patient-friendly counseling summaries without inventing unsupported information.
            </p>
          </div>

          <div className="pt-4 border-t border-[#E2E8E3] space-y-2">
            <span className="text-[11px] font-semibold text-[#C98269] uppercase tracking-wider bg-[#F1DED4] px-2 py-0.5 rounded">
              Medical Safety Boundary
            </span>
            <h4 className="text-sm font-bold text-[#263B39]">Educational Companion Notice</h4>
            <p className="text-xs text-[#6E7C76] leading-relaxed">
              OncoSathi is an educational and communication support platform designed exclusively for community health workers. 
              It is not a medical diagnostic tool and does not prescribe, modify, or replace treatments ordered by 
              qualified Medical Officers and oncologists. Community workers are advised to always escort suspected patients to their 
              nearest Primary Health Centre (PHC) or District Hospital.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
};
"""
(SRC / "pages" / "About.tsx").write_text(about_code, encoding="utf-8")
print("Updated About.tsx")
