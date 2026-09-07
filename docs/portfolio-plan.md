# Portfolio scope and interview notes

## Completed scope

- A local Streamlit app for single or batch PDF matching and evidence search.
- A small runtime dependency list, verified Python 3.11 installation, and recorded test environment.
- Shared scorer, boundary-aware aliases, and explicit embedding-failure behavior.
- Ten tests plus a GitHub Actions workflow.
- A fixed synthetic ranking comparison across keyword, semantic, and hybrid methods.
- A real UI GIF embedded in the README, with an automated capture script.

## A 60-second walkthrough

1. Select the three fictional samples or upload their PDFs.
2. Use the default NLP job description and click Compare resumes.
3. Explain Alice's skill coverage and compare the component scores.
4. Search for semantic search pipelines and inspect the source excerpt.
5. Show the evaluation table: semantic-only beat the hybrid on this fixture.

## Interview outline

- **Problem:** keyword matching misses paraphrases; embedding similarity may overlook explicit requirements.
- **Design:** inspect semantic and skill signals separately, combine them with fixed weights, and retrieve source evidence.
- **Evaluation:** 12 profiles, 6 roles, 72 synthetic labels. Use nDCG@3 to reward placing highly relevant candidates at the top. Compare to both component baselines.
- **Finding:** semantic-only scored 0.949, hybrid 0.844, keyword-only 0.783. The hand-chosen hybrid was not best; keyword stuffing exposed a weakness.
- **Tradeoffs:** simple parsing, a limited dictionary, model input truncation, and subjective synthetic labels limit the claims.
- **Next experiment:** gather independent relevance labels and reserve separate development/test roles before choosing a scoring method or tuning weights.

## Scope boundary

This is a portfolio prototype, not a finished hiring platform. Agents, fine-tuning, authentication, cloud infrastructure, and an LLM chatbot are outside this version. The existing pipeline and evaluation are sufficient for a focused demonstration.

## Resume bullet

Built an explainable resume-matching application using MiniLM embeddings, hybrid skill scoring, and FAISS evidence retrieval; compared three ranking methods on 72 synthetic resume–job pairs and documented keyword-stuffing failure cases.
