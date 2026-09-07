from functools import lru_cache



MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"


@lru_cache(maxsize=1)
def get_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME, revision=MODEL_REVISION)


def embed_texts(texts):
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True)


def embed_query(query: str):
    model = get_embedding_model()
    return model.encode([query], normalize_embeddings=True)[0]
