import os
import tempfile
from typing import List, Dict

from src.parsing.pdf_parser import extract_text_from_pdf
from src.parsing.profile_parser import build_resume_profile


def process_uploaded_resume(uploaded_file) -> Dict:
    """
    Takes a Streamlit uploaded file, extracts text, and builds a structured profile.
    """
    uploaded_file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        raw_text = extract_text_from_pdf(temp_path)
        if not raw_text.strip():
            raise ValueError("No readable text found. Use a text-based PDF; OCR is not supported.")
        profile = build_resume_profile(raw_text)

        return {
            "filename": uploaded_file.name,
            "raw_text": raw_text,
            "profile": profile,
        }
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def process_multiple_uploaded_resumes(uploaded_files) -> List[Dict]:
    """
    Process a list of uploaded PDF files.
    """
    resume_profiles = []

    for uploaded_file in uploaded_files:
        try:
            resume_profiles.append(process_uploaded_resume(uploaded_file))
        except Exception as e:
            resume_profiles.append(
                {
                    "filename": uploaded_file.name,
                    "raw_text": "",
                    "profile": {},
                    "error": str(e),
                }
            )

    return resume_profiles
