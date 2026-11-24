import React, { useState, useEffect } from 'react';
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
