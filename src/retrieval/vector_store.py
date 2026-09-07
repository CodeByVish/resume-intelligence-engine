from typing import List, Tuple

import faiss
import numpy as np

from src.retrieval.embeddings import embed_texts


def build_faiss_index(chunks: List[str]) -> Tuple[faiss.IndexFlatIP, List[str]]:
    """
    Build a FAISS cosine-similarity index using normalized embeddings.
    """
    if not chunks:
        raise ValueError("No chunks provided to build the FAISS index.")

    embeddings = embed_texts(chunks)
    embeddings = np.array(embeddings, dtype="float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, chunks
