from io import BytesIO
import numpy as np
import fitz
from src.services.resume_service import process_multiple_uploaded_resumes
from src.retrieval import vector_store, retriever


def test_pdf_upload_can_be_processed_again():
    with fitz.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 72), "Test Person\nSkills\nPython")
        upload = BytesIO(doc.tobytes())
    upload.name = "fictional.pdf"
    for _ in range(2):
        result = process_multiple_uploaded_resumes([upload])[0]
        assert result["profile"]["skills"] == ["Python"]


def test_bad_pdf_returns_visible_error():
    upload = BytesIO(b"invalid pdf")
    upload.name = "invalid.pdf"
    assert process_multiple_uploaded_resumes([upload])[0]["error"]


def test_faiss_evidence_has_correct_source(monkeypatch):
    monkeypatch.setattr(vector_store, "embed_texts", lambda texts: np.array([[1, 0], [0, 1]], dtype="float32"))
    monkeypatch.setattr(retriever, "embed_query", lambda query: np.array([0, 1], dtype="float32"))
    profiles = [{"filename": "a.pdf", "raw_text": "Python"}, {"filename": "b.pdf", "raw_text": "SQL"}]
    index, metadata = retriever.build_resume_retrieval_index(profiles)
    results = retriever.retrieve_relevant_chunks("SQL", index, metadata, top_k=5)
    assert len(results) == 2
    assert results[0]["filename"] == "b.pdf"
    assert results[0]["chunk_text"] == "SQL"
    assert retriever.retrieve_relevant_chunks(" ", index, metadata) == []
