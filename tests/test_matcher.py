import pytest
from src.scoring import skill_matcher_v2 as matcher


def test_hybrid_weights_and_missing_skills(monkeypatch):
    monkeypatch.setattr(matcher, "semantic_similarity", lambda *args: 0.8)
    result = matcher.compute_match_score("Python", "Python and SQL")
    assert result["score"] == 72.5
    assert result["semantic_score"] == 80
    assert result["keyword_score"] == 50
    assert result["matched_terms"] == ["python"]
    assert result["missing_terms"] == ["sql"]
    assert result["mode"] == "hybrid"


def test_aliases_and_word_boundaries():
    assert matcher.extract_skill_terms("natural language processing; PostgreSQL; sklearn") == ["nlp", "scikit-learn", "sql"]
    assert matcher.extract_skill_terms("rapid paragraph draws") == []


def test_empty_input_never_loads_model(monkeypatch):
    def fail(*args):
        raise AssertionError("Must not load model")
    monkeypatch.setattr(matcher, "semantic_similarity", fail)
    assert matcher.compute_match_score("", "Python")["mode"] == "empty"


def test_model_failure_is_explicit_and_evaluation_fails(monkeypatch):
    def fail(*args):
        raise OSError("model unavailable")
    monkeypatch.setattr(matcher, "semantic_similarity", fail)
    result = matcher.compute_match_score("Python", "Python and SQL")
    assert result["score"] == 50
    assert result["semantic_score"] is None
    assert result["mode"] == "keyword_fallback"
    assert result["warning"]
    with pytest.raises(RuntimeError, match="evaluation stopped"):
        matcher.compute_match_score("Python", "Python", strict=True)
