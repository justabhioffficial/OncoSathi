// API Client for OncoSathi Backend
import { SimplifyResponse, MedicalTermItem, Language, SimplificationLevel } from '../types';

const API_BASE = (import.meta as any).env?.VITE_API_BASE || '';

export const simplifyText = async (
  text: string,
  targetLanguage: Language,
  simplificationLevel: SimplificationLevel
): Promise<SimplifyResponse> => {
  const res = await fetch(`${API_BASE}/api/simplify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      target_language: targetLanguage,
      simplification_level: simplificationLevel
    })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to simplify medical text');
  }
  return res.json();
};

export const searchTerms = async (query: string = '', category: string = ''): Promise<MedicalTermItem[]> => {
  let url = `${API_BASE}/api/terms/search?q=${encodeURIComponent(query)}`;
  if (category && category !== 'All') {
    url += `&category=${encodeURIComponent(category)}`;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch terms');
  const data = await res.json();
  return data.terms || [];
};

export const sendFeedback = async (
  queryText: string,
  simplifiedText: string,
  isHelpful: boolean,
  rating: number = 5
) => {
  return fetch(`${API_BASE}/api/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query_text: queryText,
      simplified_text: simplifiedText,
      is_helpful: isHelpful,
      rating,
      feedback_type: 'asha_simplification'
    })
  });
};
