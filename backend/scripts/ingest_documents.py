# -*- coding: utf-8 -*-
import os, sys, json
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.config import SOURCE_DOCS_DIR, PROCESSED_DIR
from app.services.extraction_service import ExtractionService
from app.services.preprocessing_service import PreprocessingService
from app.services.embedding_service import EmbeddingService

def run_ingestion():
    print("=================================================================")
    print("      ONCOSATHI AI ? DOCUMENT INGESTION & KNOWLEDGE PIPELINE     ")
    print("=================================================================")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    f1_pdf = os.path.join(SOURCE_DOCS_DIR, "1_ijpc_cancer_glossary.pdf")
    f2_pdf = os.path.join(SOURCE_DOCS_DIR, "2_medical_oncology_terminology_ba.pdf")
    f3_docx = os.path.join(SOURCE_DOCS_DIR, "3_cancer_terminology_bengali_english.docx")
    f4_csv = os.path.join(SOURCE_DOCS_DIR, "4_oncology_comprehensive_tables.csv")

    print(f"[Step 1/5] Extracting Source 1: {os.path.basename(f1_pdf)}...")
    ijpc_raw = ExtractionService.extract_from_pdf(f1_pdf)
    print(f"  -> Extracted {len(ijpc_raw)} pages.")

    print(f"[Step 2/5] Extracting Source 2: {os.path.basename(f2_pdf)}...")
    ba_raw = ExtractionService.extract_from_pdf(f2_pdf)
    print(f"  -> Extracted {len(ba_raw)} pages.")

    print(f"[Step 3/5] Extracting Source 3: {os.path.basename(f3_docx)}...")
    bengali_docx_raw = ExtractionService.extract_from_docx(f3_docx)
    print(f"  -> Extracted {len(bengali_docx_raw)} items & table rows.")

    print(f"[Step 4/5] Extracting Source 4: {os.path.basename(f4_csv)}...")
    tables_csv_raw = ExtractionService.extract_from_csv(f4_csv)
    print(f"  -> Extracted {len(tables_csv_raw)} clinical records.")

    print("[Step 5/5] Normalizing, chunking, and consolidating knowledge...")
    dictionary_terms, chunks = PreprocessingService.consolidate_knowledge(
        ijpc_raw=ijpc_raw,
        ba_raw=ba_raw,
        bengali_docx_raw=bengali_docx_raw,
        tables_csv_raw=tables_csv_raw
    )

    dict_path = os.path.join(PROCESSED_DIR, "terminology_dictionary.json")
    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(dictionary_terms, f, indent=2, ensure_ascii=False)

    chunks_path = os.path.join(PROCESSED_DIR, "knowledge_chunks.json")
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"  -> Created {len(dictionary_terms)} unique consolidated medical terms.")
    print(f"  -> Created {len(chunks)} searchable knowledge chunks.")

    # Generate Embeddings & Vector Index
    print("Building vector index...")
    embedding_service = EmbeddingService()
    embedding_service.fit_and_index(chunks)
    index_path = os.path.join(PROCESSED_DIR, "vector_index.pkl")
    embedding_service.save_index(index_path)
    print(f"  -> Vector index saved to {index_path} ({os.path.getsize(index_path)} bytes).")

    print("\n[SUCCESS] Knowledge base ingestion complete and verified!")
    return len(dictionary_terms), len(chunks)

if __name__ == "__main__":
    run_ingestion()
