import React from 'react';

export const Footer: React.FC<{ setActiveTab: (tab: string) => void }> = ({ setActiveTab }) => {
  return (
    <footer className="bg-[#263B39] text-white border-t border-[#1D5751] py-10 mt-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 space-y-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 pb-6 border-b border-white/10">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded bg-[#246B64] flex items-center justify-center text-white text-xs">
                +
              </div>
              <span className="font-bold text-lg text-white tracking-tight">OncoSathi</span>
            </div>
            <p className="text-xs text-[#DCEBE5]">
              Making cancer information easier to understand and share.
            </p>
          </div>

          <div className="flex flex-wrap gap-4 text-xs text-[#DCEBE5]">
            <button onClick={() => setActiveTab('home')} className="hover:text-white">Home</button>
            <button onClick={() => setActiveTab('simplify')} className="hover:text-white">Simplify Information</button>
            <button onClick={() => setActiveTab('dictionary')} className="hover:text-white">Oncology Dictionary</button>
            <button onClick={() => setActiveTab('guide')} className="hover:text-white">Field Guide</button>
            <button onClick={() => setActiveTab('about')} className="hover:text-white">About</button>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-[11px] text-[#DCEBE5]/80">
          <div>
            © 2026 OncoSathi AI • Designed for ASHA Community Health Workers in India.
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-[#246B64]"></span>
            <span>Grounded in 4 Verified Oncology References</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
