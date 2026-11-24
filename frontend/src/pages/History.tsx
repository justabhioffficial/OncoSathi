import React from 'react';
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
