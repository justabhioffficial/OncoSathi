# -*- coding: utf-8 -*-
"""
Verification of Section 14: TEST THE ACTUAL LIVE WORKFLOW
Runs all 16 verification steps against the active HTTP server at http://127.0.0.1:8000.
"""
import json
import urllib.request
import sys

BASE_URL = "http://127.0.0.1:8000"

def post_json(path, data):
    url = BASE_URL + path
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

print("======================================================================")
print("  ONCOSATHI AI — SECTION 14 LIVE WORKFLOW VERIFICATION SUITE")
print("======================================================================")

# Step 1 & 2: Ask "What is metastasis?"
print("\n[Step 1 & 2] Query: What is metastasis?")
res1 = post_json("/api/ask", {"question": "What is metastasis?", "target_language": "en", "level": "level_2"})
ans1 = res1.get("answer", "")
print("Answer snippet:", ans1[:120], "...")
assert "metasta" in ans1.lower()
assert "spread" in ans1.lower() or "travel" in ans1.lower()
print("[PASS] Output is directly about metastasis.")

# Step 3 & 4: Ask "What is chemotherapy?"
print("\n[Step 3 & 4] Query: What is chemotherapy?")
res2 = post_json("/api/ask", {"question": "What is chemotherapy?", "target_language": "en", "level": "level_2"})
ans2 = res2.get("answer", "")
print("Answer snippet:", ans2[:120], "...")
assert "chemotherapy" in ans2.lower()
assert "medicine" in ans2.lower() or "drug" in ans2.lower() or "systemic" in ans2.lower()
assert ans2 != ans1
print("[PASS] Output changed completely and is directly about chemotherapy.")

# Step 5 & 6: Ask "What is a biopsy?"
print("\n[Step 5 & 6] Query: What is a biopsy?")
res3 = post_json("/api/ask", {"question": "What is a biopsy?", "target_language": "en", "level": "level_2"})
ans3 = res3.get("answer", "")
print("Answer snippet:", ans3[:120], "...")
assert "biopsy" in ans3.lower()
assert "sample" in ans3.lower() or "tissue" in ans3.lower()
assert ans3 != ans2 and ans3 != ans1
print("[PASS] Output changed and is directly about biopsy.")

# Step 7 & 8: Ask "What are lymph nodes?"
print("\n[Step 7 & 8] Query: What are lymph nodes?")
res4 = post_json("/api/ask", {"question": "What are lymph nodes?", "target_language": "en", "level": "level_2"})
ans4 = res4.get("answer", "")
print("Answer snippet:", ans4[:120], "...")
assert "lymph" in ans4.lower()
assert "filter" in ans4.lower() or "immune" in ans4.lower() or "bean-shaped" in ans4.lower()
assert ans4 != ans3
print("[PASS] Output changed and is directly about lymph nodes.")

# Step 9 & 10: Ask metastasis again
print("\n[Step 9 & 10] Query: Repeat metastasis question")
res5 = post_json("/api/ask", {"question": "What does metastasis mean and how does cancer spread?", "target_language": "en", "level": "level_2"})
ans5 = res5.get("answer", "")
print("Answer snippet:", ans5[:120], "...")
assert "metasta" in ans5.lower()
assert ans5 != ans4  # Not the lymph nodes answer!
print("[PASS] Produces relevant metastasis answer, no stale state.")

# Step 11 & 12: Bengali output
print("\n[Step 11 & 12] Query: What is a biopsy? (in Bengali)")
res6 = post_json("/api/ask", {"question": "What is a biopsy?", "target_language": "bn", "level": "level_2"})
ans6 = res6.get("answer", "")
print("Bengali answer snippet:", ans6[:120], "...")
assert any('\u0980' <= c <= '\u09FF' for c in ans6)
assert "বায়োপসি" in ans6
print("[PASS] Authentic Bengali output generated with medical terminology in Bengali script.")

# Step 13 & 14: Submit long medical paragraph
print("\n[Step 13 & 14] Paragraph Simplification")
text_para = "Patient presented with a palpable, painless lump in the upper outer quadrant of the right breast. Core needle biopsy confirmed invasive ductal carcinoma. Histopathological examination shows Grade 2 malignancy with negative surgical margins."
res7 = post_json("/api/simplify", {"text": text_para, "target_language": "en", "level": "level_2"})
simp7 = res7.get("simplified_text", "")
print("Simplified snippet:", simp7[:140], "...")
assert len(simp7) > 100
assert "carcinoma" in simp7.lower() or "margins" in simp7.lower() or "grade 2" in simp7.lower()
print("[PASS] Medical paragraph was successfully simplified with clinical takeaways.")

# Step 15 & 16: Unsupported query
print("\n[Step 15 & 16] Unsupported query check")
res8 = post_json("/api/ask", {"question": "What is the capital of France?", "target_language": "en", "level": "level_2"})
ans8 = res8.get("answer", "")
print("Fallback response:", ans8[:120], "...")
assert "couldn't find enough reliable information" in ans8.lower() or "medical sources" in ans8.lower()
assert len(res8.get("sources", [])) == 0
print("[PASS] Safely rejected without fabricating citations or hallucinating facts.")

print("\n======================================================================")
print("  ALL 16 LIVE WORKFLOW VERIFICATION STEPS PASSED WITH 100% SUCCESS!")
print("======================================================================")
