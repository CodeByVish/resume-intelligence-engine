# Resume Intelligence Engine

An AI-powered Resume Intelligence Platform for semantic candidate search, intelligent resume parsing, recruiter decision support, and Retrieval-Augmented Generation (RAG).

<p align="center">

🚀 NLP • RAG • LLMs • Semantic Search • Vector Databases • Streamlit • LangChain • FAISS

</p>

## 🌸 Overview

Recruiters often spend hours manually reviewing resumes and comparing candidates against job descriptions.

This project aims to automate that workflow by combining modern NLP techniques with semantic search and Retrieval-Augmented Generation (RAG).

Instead of simply extracting text from resumes, the platform understands candidate profiles, evaluates job fit, ranks applicants, and provides explainable AI-assisted recommendations.

## ✨ Features

### Current

✅ Resume PDF Parsing

✅ Structured Resume Extraction

✅ Contact Information Detection

✅ Resume Section Detection

- Experience
- Skills
- Education
- Projects
- Certifications

✅ Semantic Resume ↔ Job Description Matching

✅ Skill-aware Matching Engine

✅ Interactive Streamlit Dashboard

### Coming Soon

🔄 Multi-resume Batch Processing

🔄 Candidate Ranking Dashboard

🔄 FAISS Vector Database

🔄 Resume Chunking

🔄 Retrieval-Augmented Generation (RAG)

🔄 Recruiter AI Assistant

🔄 Interview Question Generation

🔄 Skill Gap Analysis

🔄 Candidate Comparison

🔄 Recruiter Analytics Dashboard

## 🏗 System Architecture

```text
                        PDF Resume
                             │
                             ▼
                   Document Parsing Layer
                             │
                             ▼
                 Structured Resume Profile
                             │
                             ▼
             Semantic Matching Engine
                             │
                             ▼
              Candidate Scoring Pipeline
                             │
                             ▼
                  Recruiter Dashboard
                             │
                             ▼
          (Upcoming)
        Embeddings → FAISS → RAG → LLM
```

## 🛠 Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python |
| Frontend | Streamlit |
| Resume Parsing | PyMuPDF |
| NLP | spaCy |
| Semantic Matching | Sentence Transformers |
| ML | scikit-learn |
| Vector Search | FAISS (Upcoming) |
| LLM Framework | LangChain (Upcoming) |
| Agent Framework | LangGraph (Upcoming) |

## 📸 Screenshots

### Dashboard

(Insert Streamlit Home Page Screenshot Here)

### Resume Parsing

(Insert Resume Parsing Screenshot Here)

### Semantic Matching

(Insert Resume Match Screenshot Here)

### Candidate Ranking

(Coming Soon)

## 🧠 Why this project?

Most resume screening tools rely heavily on keyword matching.

This project moves beyond keyword search by introducing semantic similarity, structured resume understanding, and Retrieval-Augmented Generation to help recruiters make faster and more informed hiring decisions.

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

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/resume-intelligence-engine.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## 🎯 Roadmap

### Phase 1 ✅

- Resume Parsing
- Structured Extraction
- Skill-aware Matching

### Phase 2 🚧

- Multi Resume Upload
- Candidate Ranking
- Recruiter Dashboard

### Phase 3

- Embedding Generation
- FAISS Vector Search
- Resume Retrieval

### Phase 4

- Retrieval-Augmented Generation (RAG)
- LangChain Integration
- Recruiter AI Assistant

### Phase 5

- LangGraph Agent Workflow
- Candidate Comparison
- Analytics Dashboard

## 📈 Future Improvements

- OCR for scanned resumes
- Fine-tuned skill extraction
- ATS compatibility scoring
- Resume recommendations
- Recruiter PDF reports
- Cloud deployment

## 🤝 Contributing

Contributions, feature requests, and discussions are always welcome.

## ⭐ If you found this project interesting...

Please consider starring the repository.
