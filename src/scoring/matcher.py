"""Compatibility import: all callers use the same active matcher."""
from src.scoring.skill_matcher_v2 import compute_match_score, extract_skill_terms

__all__ = ["compute_match_score", "extract_skill_terms"]
