"""Local resume matching demo. Run with: python -m streamlit run app.py."""
from pathlib import Path
from base64 import b64encode
from html import escape

import streamlit as st

from src.retrieval.retriever import build_resume_retrieval_index, retrieve_relevant_chunks
from src.services.resume_service import process_multiple_uploaded_resumes
from src.services.ranking_service import rank_resume_batch

st.set_page_config(page_title="AI Resume Copilot", page_icon="✦", layout="wide")
def load_styles():
    assets = Path(__file__).parent / "assets"
    faces = []
    for family, weight, filename in [
        ("Cormorant Garamond", 500, "cormorant-garamond-500.ttf"),
        ("Inter", 400, "inter-400.ttf"),
        ("Inter", 600, "inter-600.ttf"),
    ]:
        data = b64encode((assets / "fonts" / filename).read_bytes()).decode()
        faces.append(f"@font-face {{font-family: '{family}'; font-weight: {weight}; font-style: normal; font-display: swap; src: url(data:font/ttf;base64,{data}) format('truetype');}}")
    return "<style>" + "\n".join(faces) + (assets / "style.css").read_text() + "</style>"


st.markdown(load_styles(), unsafe_allow_html=True)
st.markdown("""
<div class="topline"><div class="wordmark"><span class="brand-star">✳</span> AI RESUME COPILOT</div><span class="top-note">A thoughtful approach to finding the right fit</span></div>
<div class="hero"><span class="eyebrow">A little clarity for your next chapter</span>
<h1>Find the fit.<br><em>See the potential.</em></h1>
<p>Compare candidate resumes against your open role, explore relevant experience,<br class="desktop-break"> and build a more informed shortlist.</p></div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.15], gap="large")
with left, st.container(border=True, key="resume_panel"):
    st.markdown('<div class="step-label">01 / THE PEOPLE</div>', unsafe_allow_html=True)
    st.subheader("Your resumes")
    st.caption("One for your own next step. A few to find your next teammate.")
    uploaded = st.file_uploader("Add your resume PDFs", type=["pdf"], accept_multiple_files=True)
    use_samples = st.checkbox("Try three fictional sample resumes", value=False)
    st.caption("Just exploring? The samples are a lovely place to start.")
with right, st.container(border=True, key="role_panel"):
    st.markdown('<div class="step-label">02 / THE OPPORTUNITY</div>', unsafe_allow_html=True)
    st.subheader("The role in mind")
    st.caption("Add the skills and experience that matter for this role.")
    jd = st.text_area("Job description", value="NLP engineer with Python, natural language processing, and vector search skills.", height=128)
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
    st.markdown('<div class="step-label" style="margin-top:24px">03 / THE POSSIBILITIES</div>', unsafe_allow_html=True)
    st.subheader("Your matches")
    for warning in df["warning"].dropna().unique():
        st.warning(warning)
    a, b, c = st.columns(3)
    a.metric("Resumes compared", len(df))
    b.metric("Top relevance score", f"{df.iloc[0]['score']:.1f} / 100")
    c.metric("Scoring", "Keyword fallback" if (df["mode"] == "keyword_fallback").any() else "Hybrid")
    c.caption("75% semantic similarity + 25% skill coverage")
    st.caption("Relevance scores support review; they are not hiring probabilities. Missing skills mean no recognized mention was found.")
    names = {p["filename"]: p.get("profile", {}).get("basic_info", {}).get("name_guess", p["filename"]) for p in profiles}
    for start in range(0, len(df), 3):
        columns = st.columns(min(3, len(df) - start))
        for offset, (_, row) in enumerate(df.iloc[start:start + 3].iterrows()):
            position = start + offset + 1
            def chips(value, missing=False):
                terms = [term.strip() for term in str(value or "").split(",") if term.strip()]
                if not terms:
                    return '<span class="no-skills">' + ("No missing mentions" if missing else "No recognized overlap") + '</span>'
                return "".join(f'<span class="chip {"missing" if missing else ""}">{escape(term)}</span>' for term in terms)
            semantic = "Unavailable" if row["mode"] == "keyword_fallback" else f"{row['semantic_score']:.1f}"
            with columns[offset]:
                st.markdown(f"""
<div class="candidate {'featured' if position == 1 else ''}">
<div class="candidate-top"><span>Match {position:02d}</span><span>{'Highest relevance' if position == 1 else 'At a glance'}</span></div>
<h3>{escape(str(names[row['filename']]))}</h3><div class="filename">{escape(row['filename'])}</div>
<div class="score">{row['score']:.1f} <small>/ 100 relevance</small></div>
<div class="score-track"><span style="width:{max(0, min(100, row['score']))}%"></span></div>
<div class="components">Semantic {semantic} &nbsp; · &nbsp; Skill coverage {row['keyword_score']:.0f}%</div>
<div class="skill-title">MATCHED SKILLS</div>{chips(row['matched_terms'])}
<div class="skill-title">MISSING MENTIONS</div>{chips(row['missing_terms'], True)}
</div>""", unsafe_allow_html=True)
    st.write("")
    tabs = st.tabs(["Evidence search", "Parsed profiles", "Compare all scores"])
    with tabs[0]:
        query = st.text_input("Search resume evidence", value="semantic search pipelines", placeholder="A skill, project, or responsibility")
        st.caption("Look beyond the score. Find the projects, skills, and experience in their own words.")
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
    with tabs[2]:
        st.dataframe(df[["filename", "score", "semantic_score", "keyword_score", "matched_terms", "missing_terms"]].rename(columns={
            "filename": "Resume", "score": "Relevance", "semantic_score": "Semantic", "keyword_score": "Skill coverage", "matched_terms": "Matched skills", "missing_terms": "Missing mentions"
        }), hide_index=True, use_container_width=True)
else:
    st.markdown('<div class="empty-state"><span class="empty-icon">✧</span><div><strong>Your next match starts here.</strong><p>Add a resume or try the samples, then select Compare resumes. We’ll take it from there.</p></div></div>', unsafe_allow_html=True)
st.markdown('<div class="footer"><span>Made for thoughtful decisions. The final call is always yours.</span><span>Resume matching &amp; evidence search · Local demo</span></div>', unsafe_allow_html=True)
