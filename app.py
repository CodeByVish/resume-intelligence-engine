"""Local resume matching demo. Run with: python -m streamlit run app.py."""
from pathlib import Path

import streamlit as st

from src.retrieval.retriever import build_resume_retrieval_index, retrieve_relevant_chunks
from src.services.resume_service import process_multiple_uploaded_resumes
from src.services.ranking_service import rank_resume_batch

st.set_page_config(page_title="AI Resume Copilot", page_icon="✦", layout="wide")
st.markdown("""
<style>
.stApp { background: #f7f8fc; }
.block-container { max-width: 1200px; padding-top: 2.5rem; }
h1, h2, h3 { color: #172240; }
.hero { padding: 28px 32px; border-radius: 20px; background: #172240; margin-bottom: 24px; }
.hero h1 { color: white; margin: 8px 0; }
.hero p { color: #d7dff4; margin-bottom: 0; }
.eyebrow { color: #bdb4ff; font-size: 12px; letter-spacing: 2px; font-weight: 700; }
[data-testid="stMetric"] { background: white; padding: 16px; border-radius: 12px; border: 1px solid #e4e8f0; }
</style>
<div class="hero"><span class="eyebrow">SEMANTIC MATCHING · EVIDENCE SEARCH</span>
<h1>AI Resume Copilot</h1><p>Compare resumes to a role. See the skills. Inspect the evidence.</p></div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.15], gap="large")
with left:
    st.subheader("1. Add resumes")
    uploaded = st.file_uploader("Upload one or more resume PDFs", type=["pdf"], accept_multiple_files=True)
    use_samples = st.checkbox("Try three fictional sample resumes", value=False)
    st.caption("Use one resume to check your own fit, or several to compare candidates.")
with right:
    st.subheader("2. Describe the role")
    jd = st.text_area("Job description", value="NLP engineer with Python, natural language processing, and vector search skills.", height=140)
    run = st.button("Compare resumes", type="primary", use_container_width=True)

# Include input bytes in the signature so results never outlive their inputs.
inputs = [(file.name, file.getvalue()) for file in uploaded or []]
if use_samples and not inputs:
    sample_dir = Path(__file__).parent / "examples" / "samples"
    inputs = [(p.name, p.read_bytes()) for p in sorted(sample_dir.glob("*.pdf"))]
    if not inputs:
        st.info("Generate samples with: python -m examples.generate_samples")
signature = (tuple(inputs), jd)
if st.session_state.get("signature") != signature:
    st.session_state.pop("ranked", None)
    st.session_state.pop("profiles", None)
    st.session_state.pop("retrieval", None)
    st.session_state["signature"] = signature

if run:
    if not inputs:
        st.warning("Upload a PDF or select the fictional samples first.")
    elif not jd.strip():
        st.warning("Enter a job description first.")
    else:
        from io import BytesIO
        files = []
        for name, data in inputs:
            file = BytesIO(data)
            file.name = name
            files.append(file)
        with st.spinner("Parsing resumes and comparing with the role…"):
            processed = process_multiple_uploaded_resumes(files)
            for item in processed:
                if item.get("error"):
                    st.error(f"{item['filename']}: {item['error']}")
            profiles = [item for item in processed if item.get("raw_text")]
            if profiles:
                st.session_state["profiles"] = profiles
                st.session_state["ranked"] = rank_resume_batch(profiles, jd)

if "ranked" in st.session_state:
    df = st.session_state["ranked"]
    profiles = st.session_state["profiles"]
    st.subheader("3. Review the matches")
    for warning in df["warning"].dropna().unique():
        st.warning(warning)
    a, b, c = st.columns(3)
    a.metric("Resumes compared", len(df))
    b.metric("Top relevance score", f"{df.iloc[0]['score']:.1f} / 100")
    c.metric("Scoring", "Keyword fallback" if (df["mode"] == "keyword_fallback").any() else "Hybrid")
    c.caption("75% semantic similarity + 25% skill coverage")
    st.caption("Relevance scores support review; they are not hiring probabilities. Missing skills mean no recognized mention was found.")
    st.dataframe(df[["filename", "score", "semantic_score", "keyword_score", "matched_terms", "missing_terms"]].rename(columns={
        "filename": "Resume", "score": "Relevance", "semantic_score": "Semantic", "keyword_score": "Skill coverage", "matched_terms": "Matched skills", "missing_terms": "Missing skills"
    }), hide_index=True, use_container_width=True)
    tabs = st.tabs(["Evidence search", "Parsed profiles"])
    with tabs[0]:
        query = st.text_input("Search resume evidence", value="semantic search pipelines", placeholder="A skill, project, or responsibility")
        st.caption("Returns source excerpts using vector similarity. No generated answers.")
        if st.button("Find evidence"):
            if not query.strip():
                st.warning("Enter a search phrase first.")
            else:
                try:
                    with st.spinner("Searching resume excerpts…"):
                        if "retrieval" not in st.session_state:
                            st.session_state["retrieval"] = build_resume_retrieval_index(profiles)
                        index, metadata = st.session_state["retrieval"]
                        results = retrieve_relevant_chunks(query, index, metadata, top_k=3)
                    for item in results:
                        with st.expander(f"{item['filename']} · similarity {item['score']:.3f}", expanded=True):
                            st.text(item["chunk_text"])
                except Exception:
                    st.error("Evidence search is unavailable. Check that the embedding model can load and try again.")
    with tabs[1]:
        for item in profiles:
            with st.expander(item["filename"]):
                st.json(item["profile"])
else:
    st.info("Start with fictional samples or upload your PDFs, then choose Compare resumes.")
st.divider()
st.caption("Portfolio prototype · MiniLM embeddings · FAISS retrieval · Rule-based skill extraction")
