// TypeScript type definitions for OncoSathi AI
export type Language = 'english' | 'bengali';
export type SimplificationLevel = 1 | 2 | 3;

export interface SourceReference {
  source_document: string;
  document_title?: string;
  section_or_page?: string;
  chunk_text: string;
  similarity_score?: number;
  category?: string;
}

export interface TermExplanation {
  term: string;
  simple_meaning: string;
  bengali_term?: string;
  category?: string;
}

export interface SimplifyResponse {
  simplified_text: string;
  original_text: string;
  language: string;
  level: number;
  reading_level: string;
  key_points: string[];
  terms_explained: TermExplanation[];
  sources: SourceReference[];
  disclaimer: string;
  confidence_score: number;
}

export interface MedicalTermItem {
  id: string;
  term: string;
  definition: string;
  simple_meaning?: string;
  bengali_term?: string;
  category: string;
  source_document: string;
  abbreviation?: string;
}

export interface HistoryItem {
  id: number;
  timestamp: string;
  originalText: string;
  simplifiedText: string;
  language: string;
  level: number;
  keyPoints: string[];
}
