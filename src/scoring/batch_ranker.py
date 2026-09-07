from typing import List, Dict

import pandas as pd

from src.scoring.skill_matcher_v2 import compute_match_score


def rank_resumes(resume_profiles: List[Dict], job_description: str) -> pd.DataFrame:
    rows = []

    for profile in resume_profiles:
        raw_text = profile["raw_text"]
        filename = profile["filename"]

        result = compute_match_score(raw_text, job_description)

        rows.append(
            {
                "filename": filename,
                "mode": result["mode"],
                "warning": result["warning"],
                "score": result.get("score", 0.0),
                "semantic_score": result.get("semantic_score", 0.0),
                "keyword_score": result.get("keyword_score", 0.0),
                "matched_terms": ", ".join(result.get("matched_terms", [])),
                "missing_terms": ", ".join(result.get("missing_terms", [])),
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

    return df
