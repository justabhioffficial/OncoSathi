import React from 'react';

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
