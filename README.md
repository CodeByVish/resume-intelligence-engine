# 🚀 Resume Intelligence Platform

An end-to-end AI Engineering project that transforms unstructured resumes into an intelligent, searchable knowledge base using NLP, semantic retrieval, vector search, and Retrieval-Augmented Generation (RAG).

<p align="center">
  <strong>NLP</strong> •
  <strong>Semantic Search</strong> •
  <strong>Vector Databases</strong> •
  <strong>RAG</strong> •
  <strong>Streamlit</strong> •
  <strong>LangChain</strong> •
  <strong>FAISS</strong>
</p>

---

## 🌸 Overview

Recruiters spend hours manually reviewing resumes, comparing applicants, identifying skill gaps, and deciding who deserves an interview.

Traditional Applicant Tracking Systems (ATS) mostly rely on keyword matching, often missing highly qualified candidates simply because they use different wording.

**Resume Intelligence Platform** approaches the problem differently.

Instead of treating resumes as plain text documents, it converts them into structured knowledge that can be searched, ranked, retrieved, and queried using modern AI techniques.

The project combines classical NLP with semantic embeddings, vector search, and Retrieval-Augmented Generation (RAG) to create an explainable AI assistant for recruiters.

---

## 🎬 Demo

### 📹 Demo GIF

Replace this section with a GIF of the Streamlit application once complete.

---

## 📸 Screenshots

### Home Dashboard

Insert screenshot here.

### Resume Parsing

Insert screenshot here.

### Semantic Matching

Insert screenshot here.

### Candidate Ranking

Insert screenshot here after batch ranking is implemented.

### RAG Chat Assistant

Insert screenshot after implementation.

---

## ✨ Features

### Document Intelligence

- PDF resume parsing
- Automatic resume section detection
- Contact information extraction
- Structured candidate profiles
- Resume normalization

### Semantic Candidate Matching

- Resume ↔ job description matching
- Embedding-based similarity
- Skill-aware matching
- Explainable match scores
- Missing skill detection

### AI & Retrieval

- Dense vector embeddings
- FAISS vector database
- Resume chunking
- Semantic resume search
- Retrieval-Augmented Generation (RAG)

### Recruiter Experience

- Candidate ranking
- Multi-resume upload
- Resume comparison
- Interview question generation
- AI recruiter assistant

---

## 🧠 AI Pipeline

```text
                        Resume PDFs
                              │
                              ▼
                  Document Parsing Pipeline
                              │
                              ▼
                 Structured Resume Profiles
                              │
                              ▼
                 Skill Extraction + NLP
                              │
                              ▼
                  Embedding Generation
                              │
                              ▼
                     FAISS Vector Store
                              │
                              ▼
              Semantic Resume Retrieval
                              │
                              ▼
             Retrieval-Augmented Generation
                              │
                              ▼
                Recruiter AI Assistant
```

---

## ⚙ Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python |
| Frontend | Streamlit |
| Document Parsing | PyMuPDF |
| NLP | spaCy |
| Embeddings | Sentence Transformers |
| Similarity | scikit-learn |
| Vector Search | FAISS |
| RAG Framework | LangChain |
| Agent Workflow | LangGraph |
| Data Processing | pandas, NumPy |

---

## 📂 Project Structure

```text
resume-intelligence-engine/
│
├── app.py
│
├── src/
│   ├── parsing/
│   ├── scoring/
│   ├── retrieval/
│   ├── llm/
│   ├── evaluation/
│   └── utils/
│
├── data/
│
├── notebooks/
│
├── docs/
│
└── README.md
```

---

## 🚀 Running Locally

Clone the repository:

```bash
git clone https://github.com/CodeByVish/resume-intelligence-engine.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## 📊 Example Workflow

```text
Upload Resume(s)
       ↓
Parse Resume
       ↓
Extract Skills & Experience
       ↓
Generate Embeddings
       ↓
Compare Against Job Description
       ↓
Rank Candidates
       ↓
Retrieve Supporting Evidence
       ↓
Ask AI Questions
       ↓
Generate Interview Questions
```

---

## 🎯 Engineering Highlights

This repository demonstrates practical AI Engineering concepts including:

- NLP pipelines
- Information extraction
- Semantic search
- Dense vector embeddings
- Vector databases
- Retrieval-Augmented Generation (RAG)
- Explainable AI
- Streamlit application development
- Modular Python architecture

---

## 🔮 Future Enhancements

- Fine-tuned resume skill extraction
- ATS compatibility analysis
- Resume quality scoring
- Multi-agent recruiter workflow
- Recruiter analytics dashboard
- Cloud deployment

---

## 🤝 Contributing

Contributions, discussions, and ideas are always welcome.

---

## ⭐ If you enjoyed this project...

Consider giving it a ⭐ on GitHub!
