import React, { useState } from 'react';
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
