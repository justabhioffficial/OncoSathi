# -*- coding: utf-8 -*-
"""
Query Differentiation Test Suite for OncoSathi AI.
Validates that different questions produce genuinely different, topic-specific,
accurate answers grounded in the 4 oncology reference sources, and that out-of-domain
queries safely trigger the fallback without hallucination.
"""
import unittest
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.services.retrieval_service import RetrievalService
from app.services.simplification_service import SimplificationService

class TestQueryDifferentiation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        retriever = RetrievalService()
        cls.service = SimplificationService(retriever)

    def test_query_a_metastasis(self):
        """Test A: What is metastasis?"""
        query = "What does metastasis mean and how does cancer spread from its original organ to lymph nodes or other parts of the body?"
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("metasta", answer)
        self.assertTrue("spread" in answer or "travel" in answer or "lymph" in answer)
        # Must NOT start with generic cancer preamble
        self.assertFalse(answer.startswith("cancer occurs when abnormal cells in the body multiply uncontrollably and form a growth"))
        # Must cite metastasis source
        doc_sources = [s.document_name for s in response.sources]
        self.assertTrue(any("glossary" in d.lower() or "table" in d.lower() or "terminology" in d.lower() for d in doc_sources))

    def test_query_b_lymph_nodes(self):
        """Test B: What are lymph nodes?"""
        query = "What are lymph nodes?"
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("lymph", answer)
        self.assertTrue("filter" in answer or "immune" in answer or "bean-shaped" in answer)
        self.assertNotIn("metasta", answer[:100])  # First 100 characters must focus on lymph nodes

    def test_query_c_chemotherapy(self):
        """Test C: What is chemotherapy?"""
        query = "What is chemotherapy?"
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("chemotherapy", answer)
        self.assertTrue("medicine" in answer or "drug" in answer or "systemic" in answer)
        self.assertTrue(answer.startswith("chemotherapy"))

    def test_query_d_biopsy(self):
        """Test D: What is a biopsy?"""
        query = "What is a biopsy?"
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("biopsy", answer)
        self.assertTrue("sample" in answer or "tissue" in answer or "microscope" in answer)
        self.assertTrue(answer.startswith("a biopsy") or answer.startswith("biopsy"))

    def test_query_e_benign_vs_malignant(self):
        """Test E: What is the difference between benign and malignant tumors?"""
        query = "What is the difference between benign and malignant tumors?"
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("benign", answer)
        self.assertIn("malignant", answer)
        self.assertTrue("non-cancerous" in answer or "not cancerous" in answer or "নির্দোষ" in answer)

    def test_query_f_cancer_staging(self):
        """Test F: Explain cancer staging in simple English."""
        query = "Explain cancer staging in simple English."
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("stag", answer)
        self.assertTrue("stage i" in answer or "tnm" in answer or "size" in answer or "spread" in answer)

    def test_query_g_breast_cancer(self):
        """Test G: Explain breast cancer in simple language."""
        query = "Explain breast cancer in simple language."
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer.lower()
        self.assertIn("breast", answer)
        self.assertTrue("lump" in answer or "ductal" in answer or "mammogram" in answer)

    def test_query_h_bengali_paragraph_simplification(self):
        """Test H: Paragraph simplification in Bengali."""
        text = "Patient presented with a palpable, painless lump in the upper outer quadrant of the right breast. Core needle biopsy confirmed invasive ductal carcinoma. Histopathological examination shows Grade 2 malignancy with negative surgical margins."
        response = self.service.simplify_text(text, target_language="bn", level="level_2")
        
        simplified = response.simplified_text
        self.assertTrue(any('\u0980' <= c <= '\u09FF' for c in simplified))
        self.assertEqual(response.target_language, "bn")
        self.assertGreaterEqual(len(response.key_points), 2)

    def test_query_i_out_of_domain_no_hallucination(self):
        """Test I: Out of domain question must trigger honest fallback without hallucinating sources."""
        query = "What is the capital of France?"
        response = self.service.answer_question(query, target_language="en", level="level_2")
        
        answer = response.answer
        self.assertTrue("couldn't find enough reliable information" in answer.lower() or "medical sources" in answer.lower())
        self.assertEqual(len(response.sources), 0)

    def test_queries_produce_distinct_answers(self):
        """Verify that clearly different questions do NOT produce identical answers."""
        ans_meta = self.service.answer_question("What is metastasis?", target_language="en", level="level_2").answer
        ans_chemo = self.service.answer_question("What is chemotherapy?", target_language="en", level="level_2").answer
        ans_biopsy = self.service.answer_question("What is a biopsy?", target_language="en", level="level_2").answer
        ans_lymph = self.service.answer_question("What are lymph nodes?", target_language="en", level="level_2").answer
        
        answers = [ans_meta, ans_chemo, ans_biopsy, ans_lymph]
        self.assertEqual(len(set(answers)), 4)

if __name__ == "__main__":
    unittest.main()
