from typing import List


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    """
    Simple character-based chunking for resume text.
    Good enough for an MVP and easy to reason about.
    """
    text = (text or "").strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks
