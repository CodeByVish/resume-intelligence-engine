from typing import List, Dict

import numpy as np

from src.retrieval.chunker import chunk_text
from src.retrieval.embeddings import embed_query, embed_texts
from src.retrieval.vector_store import build_faiss_index


def build_resume_retrieval_index(resume_profiles: List[Dict]):
    """
    Turn a list of resume dicts into chunk-level searchable data.
    Returns a FAISS index plus metadata for each chunk.
    """
    all_chunks = []
    metadata = []

    for resume in resume_profiles:
        filename = resume["filename"]
        raw_text = resume["raw_text"]
        chunks = chunk_text(raw_text)

        candidate_name = (
            resume.get("profile", {})
            .get("basic_info", {})
            .get("name_guess", "Unknown")
        )

        for chunk_id, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata.append(
                {
                    "filename": filename,
                    "candidate_name": candidate_name,
                    "chunk_id": chunk_id,
                    "chunk_text": chunk,
                }
            )

    if not all_chunks:
        raise ValueError("No resume chunks available to index.")

    index, _ = build_faiss_index(all_chunks)
    return index, metadata


def retrieve_relevant_chunks(query: str, index, metadata, top_k: int = 5):
    """
    Retrieve the most relevant chunks for a given query.
    """
    if not query.strip():
        return []

    query_embedding = np.array([embed_query(query)], dtype="float32")
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        item = metadata[idx].copy()
        item["score"] = float(score)
        results.append(item)

    return results
