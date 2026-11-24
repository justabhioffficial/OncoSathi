import React from 'react';

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
