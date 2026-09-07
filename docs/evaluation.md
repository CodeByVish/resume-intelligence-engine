# Synthetic ranking evaluation

12 fictional profiles × 6 job descriptions; 72 author-labeled pairs. Labels: 0 irrelevant, 1 partial fit, 2 strong fit. Fixed weights; no tuning. These labels and examples are a small sanity check, not independent evidence of real-world hiring quality.

Run: `python -m src.evaluation.run`. Embedding failure stops the run. Ties use resume ID order.

| Job | Keyword nDCG@3 | Semantic nDCG@3 | Hybrid nDCG@3 |
| --- | ---: | ---: | ---: |
| nlp_search | 0.547 | 1.000 | 0.704 |
| ml_serving | 0.847 | 0.847 | 0.847 |
| data_platform | 0.700 | 1.000 | 0.879 |
| analytics_dashboard | 0.847 | 0.847 | 0.847 |
| backend_api | 0.847 | 1.000 | 0.879 |
| language_research | 0.907 | 1.000 | 0.907 |
| **Mean** | **0.783** | **0.949** | **0.844** |

## Inspectable failure probes

The `stuffing` profile lists skills without hands-on evidence and has relevance 0 for every role. The `paraphrase` profile describes dense retrieval without naming the dictionary skills and has relevance 2 for the NLP search role.

- nlp_search / stuffing: keyword: #2, semantic: #5, hybrid: #2.
- nlp_search / paraphrase: keyword: #9, semantic: #3, hybrid: #5.
- backend_api / stuffing: keyword: #2, semantic: #4, hybrid: #3.
- backend_api / paraphrase: keyword: #12, semantic: #12, hybrid: #12.

Full rankings, scores, fixture hash and package versions: [JSON report](evaluation-results.json).

Limitations: tiny author-created dataset; subjective labels; no human agreement study, uncertainty estimate, or held-out production data. Do not turn these results into an accuracy claim. Changing fixtures or weights requires a new evaluation and disclosure.
