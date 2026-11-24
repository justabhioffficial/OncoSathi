# -*- coding: utf-8 -*-
import os, json, csv
from pathlib import Path
from typing import List, Dict, Any

class ExtractionService:
    @staticmethod
    def extract_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
        results = []
        path_obj = Path(pdf_path)
        doc_name = path_obj.name
        
        # Try pypdfium2 first
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(pdf_path)
            for i, page in enumerate(pdf):
                textpage = page.get_textpage()
                text = textpage.get_text_range()
                if text and text.strip():
                    results.append({
                        "source": doc_name,
                        "page": i + 1,
                        "text": text.strip()
                    })
            if results:
                return results
        except Exception as e:
            print(f"[ExtractionService] pypdfium2 error on {doc_name}: {e}")

        # Fallback to PyPDF2
        try:
            import PyPDF2
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text and text.strip():
                        results.append({
                            "source": doc_name,
                            "page": i + 1,
                            "text": text.strip()
                        })
        except Exception as e:
            print(f"[ExtractionService] PyPDF2 error on {doc_name}: {e}")
            
        return results

    @staticmethod
    def extract_from_docx(docx_path: str) -> List[Dict[str, Any]]:
        import docx
        doc_obj = docx.Document(docx_path)
        doc_name = Path(docx_path).name
        results = []
        
        current_section = "General"
        # Extract paragraphs
        for p in doc_obj.paragraphs:
            text = p.text.strip()
            if not text:
                continue
            if p.style.name.startswith("Heading"):
                current_section = text
            else:
                results.append({
                    "source": doc_name,
                    "section": current_section,
                    "type": "paragraph",
                    "text": text
                })
                
        # Extract tables
        for t_idx, table in enumerate(doc_obj.tables):
            headers = [cell.text.strip() for cell in table.rows[0].cells]
            for r_idx, row in enumerate(table.rows[1:]):
                row_vals = [cell.text.strip() for cell in row.cells]
                if len(row_vals) >= 2:
                    eng = row_vals[0]
                    bng = row_vals[1]
                    results.append({
                        "source": doc_name,
                        "section": current_section,
                        "type": "table_row",
                        "english_term": eng,
                        "bengali_term": bng,
                        "text": f"English Term: {eng} | Bengali: {bng}"
                    })
        return results

    @staticmethod
    def extract_from_csv(csv_path: str) -> List[Dict[str, Any]]:
        results = []
        doc_name = Path(csv_path).name
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r_idx, row in enumerate(reader):
                results.append({
                    "source": doc_name,
                    "row_idx": r_idx + 1,
                    "section": row.get("Section", "Table"),
                    "category_or_cancer": row.get("Category_or_Cancer", ""),
                    "term_or_subtype": row.get("Term_or_Subtype", ""),
                    "detail": row.get("Detail_or_Description", ""),
                    "guideline": row.get("Guideline_or_Action", ""),
                    "side_effects": row.get("SideEffects_or_Risks", ""),
                    "text": f"[{row.get('Category_or_Cancer','')}] {row.get('Term_or_Subtype','')}: {row.get('Detail_or_Description','')} | Guidelines: {row.get('Guideline_or_Action','')} | Risks/Side Effects: {row.get('SideEffects_or_Risks','')}"
                })
        return results

    @staticmethod
    def extract_from_json(json_path: str) -> Dict[str, Any]:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
