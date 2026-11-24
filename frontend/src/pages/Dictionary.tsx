import React, { useState, useEffect } from 'react';
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
