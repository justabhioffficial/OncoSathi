import React from 'react';
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
    <header className="bg-[#FFFFFF] border-b border-[#E2E8E3] sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          
          <div 
            className="flex items-center space-x-3 cursor-pointer select-none"
            onClick={() => setActiveTab('home')}
          >
            <div className="w-9 h-9 rounded-md bg-[#246B64] flex items-center justify-center text-white shadow-sm">
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-3.5H7.5v-2H11V7.5h2V11h3.5v2H13v3.5h-2z" />
              </svg>
            </div>
            <div>
              <div className="flex items-baseline space-x-1.5">
                <span className="font-bold text-xl text-[#263B39] tracking-tight">OncoSathi</span>
                <span className="text-[11px] font-semibold text-[#246B64] uppercase tracking-wider hidden sm:inline">ASHA Care</span>
              </div>
              <div className="text-[11px] text-[#6E7C76] leading-none hidden md:block">
                Cancer Information, Made Easier to Understand
              </div>
            </div>
          </div>

          <nav className="hidden lg:flex items-center space-x-1 text-sm font-medium text-[#6E7C76]">
            {[
              { id: 'home', label: 'Home' },
              { id: 'simplify', label: 'Simplify Information' },
              { id: 'dictionary', label: 'Oncology Dictionary' },
              { id: 'guide', label: 'Field Guide' },
              { id: 'history', label: `History ${historyCount > 0 ? `(${historyCount})` : ''}` },
              { id: 'about', label: 'About' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3 py-1.5 rounded-md transition-colors ${
                  activeTab === tab.id
                    ? 'text-[#246B64] bg-[#EEF4EF] font-semibold'
                    : 'hover:text-[#25322F] hover:bg-[#F7F5EF]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          <div className="flex items-center space-x-3">
            <div className="flex bg-[#F7F5EF] p-1 rounded-md border border-[#E2E8E3] text-xs font-medium">
              <button
                onClick={() => setTargetLang('english')}
                className={`px-2.5 py-1 rounded transition-colors ${
                  targetLang === 'english'
                    ? 'bg-[#FFFFFF] text-[#246B64] font-semibold shadow-sm'
                    : 'text-[#6E7C76] hover:text-[#25322F]'
                }`}
              >
                English
              </button>
              <button
                onClick={() => setTargetLang('bengali')}
                className={`px-2.5 py-1 rounded transition-colors font-serif ${
                  targetLang === 'bengali'
                    ? 'bg-[#246B64] text-white font-semibold shadow-sm'
                    : 'text-[#6E7C76] hover:text-[#25322F]'
                }`}
              >
                বাংলা
              </button>
            </div>

            {activeTab !== 'simplify' && (
              <button
                onClick={() => setActiveTab('simplify')}
                className="hidden sm:inline-flex items-center space-x-1.5 bg-[#246B64] hover:bg-[#1D5751] text-white text-xs font-semibold px-3.5 py-2 rounded-md shadow-sm"
              >
                <span>Simplify Text</span>
                <span>→</span>
              </button>
            )}
          </div>

        </div>
      </div>
    </header>
  );
};
