import re
from functools import lru_cache
from typing import Dict

import numpy as np
from sentence_transformers import SentenceTransformer

SKILL_ALIASES = {
    "python": ["python"],
    "streamlit": ["streamlit"],
    "sql": ["sql", "postgresql", "mysql", "sqlite"],
    "nlp": ["nlp", "natural language processing"],
    "document processing": ["document processing", "document parsing", "pdf parsing", "pdf processing"],
    "pandas": ["pandas"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "aws": ["aws", "amazon web services"],
    "fastapi": ["fastapi"],
    "rest api": ["rest api", "rest apis", "api", "apis"],
    "langchain": ["langchain"],
    "vector search": ["vector search", "embeddings", "retrieval", "rag"],
    "pdf": ["pdf", "pdfs"],
    "dashboard": ["dashboard", "dashboards"],
    "matching": ["matching", "match", "ranking", "rank"],
}

GENERIC_STOPWORDS = {
    "experience", "strong", "candidate", "ideal", "looking", "plus", "build", "built",
    "building", "work", "worked", "team", "teams", "resume", "job", "description",
    "tool", "tools", "project", "projects", "using", "use", "used", "responsible",
    "solution", "solutions", "years", "year", "present", "skills", "software",
    "engineer", "developer", "role", "have", "has", "will", "may", "can",
    "for", "with", "and", "or", "the", "a", "an"
}

WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#./-]{1,}")


@lru_cache(maxsize=1)
def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")


def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = text.replace("scikit learn", "scikit-learn")
    text = text.replace("rest apis", "rest api")
    text = re.sub(r"[\u2022•]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skill_terms(text: str):
    normalized = normalize_text(text)
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                found.append(canonical)
                break
    return sorted(set(found))


def extract_generic_tokens(text: str):
    tokens = WORD_RE.findall(normalize_text(text))
    cleaned = []
    for token in tokens:
        token = token.strip(".,;:()[]{}<>|/")
        if token in GENERIC_STOPWORDS:
            continue
        if len(token) <= 2:
            continue
        cleaned.append(token)
    return cleaned


def semantic_similarity(resume_text: str, job_description: str) -> float:
    model = get_embedder()
    vectors = model.encode([resume_text, job_description], normalize_embeddings=True)
    return float(np.dot(vectors[0], vectors[1]))


def compute_match_score(resume_text: str, job_description: str) -> Dict:
    resume_text = (resume_text or "").strip()
    job_description = (job_description or "").strip()

    if not resume_text or not job_description:
        return {
            "score": 0.0,
            "semantic_score": 0.0,
            "keyword_score": 0.0,
            "matched_terms": [],
            "missing_terms": [],
        }

    resume_skills = set(extract_skill_terms(resume_text))
    job_skills = set(extract_skill_terms(job_description))

    resume_tokens = set(extract_generic_tokens(resume_text))
    job_tokens = set(extract_generic_tokens(job_description))

    matched_terms = sorted(resume_skills & job_skills)
    missing_skill_terms = sorted(job_skills - resume_skills)

    matched_generic = sorted((resume_tokens & job_tokens) - set(GENERIC_STOPWORDS))
    keyword_score = len(matched_terms) / max(len(job_skills), 1)

    try:
        semantic_score = semantic_similarity(resume_text, job_description)
    except Exception:
        semantic_score = keyword_score

    combined_score = (0.75 * semantic_score) + (0.25 * keyword_score)

    return {
        "score": round(combined_score * 100, 2),
        "semantic_score": round(semantic_score * 100, 2),
        "keyword_score": round(keyword_score * 100, 2),
        "matched_terms": matched_terms[:20] if matched_terms else matched_generic[:20],
        "missing_terms": missing_skill_terms[:20],
    }
