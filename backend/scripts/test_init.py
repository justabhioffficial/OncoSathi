# -*- coding: utf-8 -*-
import os, sys, json
import docx
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

base_dir = r'C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi'
src_dir = os.path.join(base_dir, 'backend', 'data', 'source_documents')
os.makedirs(src_dir, exist_ok=True)
print('Directory confirmed:', src_dir)
