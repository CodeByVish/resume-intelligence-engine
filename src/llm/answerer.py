from typing import List, Dict


def generate_grounded_answer(query: str, retrieval_results: List[Dict], ranking_df=None) -> str:
    """
    Build a short recruiter-friendly answer using retrieved evidence.
    """
    if not retrieval_results:
        return "I could not find enough evidence in the uploaded resumes to answer that question confidently."

    top_item = retrieval_results[0]
    top_file = top_item.get("filename", "Unknown resume")
    top_name = top_item.get("candidate_name") or top_file

    answer_lines = [
        f"Top evidence suggests **{top_name}** is the strongest match for: {query}",
        "",
        "Why this candidate surfaced:",
    ]

    seen_files = set()
    for item in retrieval_results[:3]:
        filename = item.get("filename", "Unknown resume")
        candidate_name = item.get("candidate_name") or filename

        if filename in seen_files:
            continue
        seen_files.add(filename)

        chunk_text = item.get("chunk_text", "").strip()
        chunk_text = chunk_text[:280] + ("..." if len(chunk_text) > 280 else "")
        answer_lines.append(f"- **{candidate_name}** ({filename}): {chunk_text}")

    if ranking_df is not None and not ranking_df.empty:
        best_row = ranking_df.iloc[0]
        answer_lines.extend(
            [
                "",
                f"Ranking also supports this: **{best_row['filename']}** has the highest overall score at **{best_row['score']}%**.",
            ]
        )

    return "\n".join(answer_lines)
