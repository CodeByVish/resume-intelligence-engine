from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest
from src.services import ranking_service


def test_samples_rank_and_results_survive_evidence_input(monkeypatch):
    def rank(profiles, jd):
        return pd.DataFrame([{
            "filename": p["filename"], "score": 75.0,
            "semantic_score": 70.0, "keyword_score": 90.0,
            "matched_terms": "python", "missing_terms": "sql",
            "mode": "hybrid", "warning": None,
        } for p in profiles])
    monkeypatch.setattr(ranking_service, "rank_resume_batch", rank)
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=15).run()
    assert not app.exception
    app.checkbox[0].check().run()
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value == "3"
    app.text_input[0].set_value("Python pipelines").run()
    assert app.metric[0].value == "3"
    app.text_area[0].set_value("Different role").run()
    assert len(app.metric) == 0
