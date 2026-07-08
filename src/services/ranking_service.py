from src.scoring.skill_matcher_v2 import compute_match_score
from src.scoring.batch_ranker import rank_resumes


def score_single_resume(raw_text: str, job_description: str):
    return compute_match_score(raw_text, job_description)


def rank_resume_batch(resume_profiles, job_description):
    return rank_resumes(resume_profiles, job_description)
