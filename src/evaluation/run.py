"""Fixed-weight synthetic ranking comparison: python -m src.evaluation.run."""
import hashlib
import json
import math
from pathlib import Path
from importlib.metadata import version

from src.scoring.skill_matcher_v2 import compute_match_score
from src.retrieval.embeddings import MODEL_NAME, MODEL_REVISION


def ndcg_at_k(labels, k=3):
    def dcg(values):
        return sum((2 ** grade - 1) / math.log2(i + 2) for i, grade in enumerate(values[:k]))
    ideal = dcg(sorted(labels, reverse=True))
    return dcg(labels) / ideal if ideal else 0.0


def main():
    root = Path(__file__).resolve().parents[2]
    source = root / "data/evaluation/benchmark.json"
    fixture = json.loads(source.read_text())
    methods = {"keyword": "keyword_score", "semantic": "semantic_score", "hybrid": "score"}
    results = []
    for job in fixture["jobs"]:
        scores = {r["id"]: compute_match_score(r["text"], job["text"], strict=True) for r in fixture["resumes"]}
        row = {"job": job["id"], "methods": {}}
        for method, field in methods.items():
            order = sorted(scores, key=lambda rid: (-scores[rid][field], rid))
            row["methods"][method] = {"ndcg_at_3": ndcg_at_k([job["relevance"][rid] for rid in order]), "ranking": order, "scores": [scores[rid][field] for rid in order]}
        results.append(row)
    means = {method: sum(r["methods"][method]["ndcg_at_3"] for r in results) / len(results) for method in methods}
    report = {"model": MODEL_NAME, "model_revision": MODEL_REVISION, "fixture_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "packages": {p: version(p) for p in ["sentence-transformers", "torch", "numpy"]}, "weights": {"semantic": 0.75, "keyword": 0.25}, "tie_break": "resume ID ascending", "mean_ndcg_at_3": means, "jobs": results}
    output = root / "docs/evaluation-results.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    lines = ["# Synthetic ranking evaluation", "", "12 fictional profiles × 6 job descriptions; 72 author-labeled pairs. Labels: 0 irrelevant, 1 partial fit, 2 strong fit. Fixed weights; no tuning. These labels and examples are a small sanity check, not independent evidence of real-world hiring quality.", "", "Run: `python -m src.evaluation.run`. Embedding failure stops the run. Ties use resume ID order.", "", "| Job | Keyword nDCG@3 | Semantic nDCG@3 | Hybrid nDCG@3 |", "| --- | ---: | ---: | ---: |"]
    for row in results:
        lines.append("| " + row["job"] + " | " + " | ".join(f"{row['methods'][m]['ndcg_at_3']:.3f}" for m in methods) + " |")
    lines.extend(["| **Mean** | " + " | ".join(f"**{means[m]:.3f}**" for m in methods) + " |", "", "## Inspectable failure probes", "", "The `stuffing` profile lists skills without hands-on evidence and has relevance 0 for every role. The `paraphrase` profile describes dense retrieval without naming the dictionary skills and has relevance 2 for the NLP search role.", ""])
    for row in results:
        if row["job"] in {"nlp_search", "backend_api"}:
            for rid in ["stuffing", "paraphrase"]:
                positions = ", ".join(f"{m}: #{row['methods'][m]['ranking'].index(rid)+1}" for m in methods)
                lines.append(f"- {row['job']} / {rid}: {positions}.")
    lines.extend(["", "Full rankings, scores, fixture hash and package versions: [JSON report](evaluation-results.json).", "", "Limitations: tiny author-created dataset; subjective labels; no human agreement study, uncertainty estimate, or held-out production data. Do not turn these results into an accuracy claim. Changing fixtures or weights requires a new evaluation and disclosure."])
    (root / "docs/evaluation.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(means, indent=2))


if __name__ == "__main__":
    main()
