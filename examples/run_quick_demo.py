#!/usr/bin/env python3
"""Quick demo script to extract profiles from PDF resumes and score them against a job description.

Usage:
    python -m examples.run_quick_demo --pdf resume1.pdf resume2.pdf --jd "Data scientist with NLP and Python experience"

This script is lightweight and uses the library internals to demonstrate core functionality.
"""
import argparse
from typing import List

from src.parsing.pdf_parser import extract_text_from_pdf
from src.parsing.profile_parser import build_resume_profile
from src.scoring.skill_matcher_v2 import compute_match_score


def process_pdf(path: str) -> dict:
    text = extract_text_from_pdf(path)
    profile = build_resume_profile(text)
    return {"filename": path, "raw_text": text, "profile": profile}


def score_resumes(resume_paths: List[str], job_description: str):
    results = []
    for p in resume_paths:
        try:
            item = process_pdf(p)
            score = compute_match_score(item["raw_text"], job_description)
            results.append({"filename": p, "score": score, "profile": item["profile"]})
        except Exception as e:
            results.append({"filename": p, "error": str(e)})

    for result in results:
        if "error" in result:
            print(f"Failed to process {result['filename']}: {result['error']}")

    # Sort by combined score
    scored = [r for r in results if r.get("score")]
    scored = sorted(scored, key=lambda r: r["score"]["score"], reverse=True)

    for r in scored:
        print("---")
        print(f"File: {r['filename']}")
        print(f"Score: {r['score']['score']}% (semantic: {r['score']['semantic_score']}%, keyword: {r['score']['keyword_score']}%)")
        if r["score"].get("warning"):
            print(r["score"]["warning"])
        basic = r["profile"]["basic_info"]
        print(f"Name guess: {basic.get('name_guess')}")
        print(f"Top skills: {', '.join(r['profile'].get('skills', [])[:10]) or 'None'}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", nargs="+", required=True, help="Path(s) to resume PDF files")
    parser.add_argument("--jd", required=True, help="Job description text")
    args = parser.parse_args()

    score_resumes(args.pdf, args.jd)


if __name__ == "__main__":
    main()
