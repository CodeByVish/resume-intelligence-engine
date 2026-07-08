import os
import json
import tempfile

import streamlit as st

from src.parsing.pdf_parser import extract_text_from_pdf
from src.parsing.profile_parser import build_resume_profile
from src.scoring.batch_ranker import rank_resumes
from src.scoring.skill_matcher_v2 import compute_match_score, VERSION as MATCHER_VERSION


def render_list(title, items):
    st.markdown(f"### {title}")
    if not items:
        st.caption(f"No {title.lower()} detected.")
        return
    for item in items:
        st.markdown(f"- {item}")


st.set_page_config(
    page_title="AI Resume Copilot",
    page_icon="✨",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #F1E4F3 0%, #F4BBD3 100%);
        }

        html, body, .stApp, p, span, div, label {
            color: #3D3D3D !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero-card {
            background: rgba(255, 255, 255, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 28px;
            padding: 2rem;
            box-shadow: 0 12px 35px rgba(254, 93, 159, 0.14);
        }

        .metric-card {
            background: white;
            border-radius: 22px;
            padding: 1rem 1.2rem;
            border: 1px solid #D6D2D2;
            box-shadow: 0 10px 25px rgba(214, 210, 210, 0.25);
        }

        .soft-text {
            color: #7A3E66;
        }

        h1, h2, h3 {
            color: #7A3E66;
        }

        div[data-testid="stFileUploader"] {
            background: white;
            border-radius: 20px;
            padding: 1rem;
            border: 1px solid #D6D2D2;
            box-shadow: 0 8px 20px rgba(214, 210, 210, 0.18);
        }

        div[data-testid="stTextArea"] textarea {
            background: white !important;
            border-radius: 16px !important;
            border: 1px solid #D6D2D2 !important;
        }

        .stButton > button {
            background: linear-gradient(90deg, #F686BD, #FE5D9F);
            color: white;
            border: none;
            border-radius: 999px;
            padding: 0.6rem 1.1rem;
            font-weight: 600;
        }

        .stButton > button:hover {
            opacity: 0.9;
            border: none;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1>AI Resume Copilot ✨</h1>
        <p class="soft-text">
            Upload a resume, extract a structured profile, and build toward RAG-based resume matching and ranking.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="metric-card">
            <h3>1</h3>
            <p>Upload resume PDF</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="metric-card">
            <h3>2</h3>
            <p>Extract structured profile</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="metric-card">
            <h3>3</h3>
            <p>Score against job descriptions</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.subheader("Upload a resume PDF")
uploaded_files = st.file_uploader(
    "Choose one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

job_description = st.text_area(
    "Paste a job description here",
    height=220,
    placeholder="Paste the job description recruiters would use for matching...",
)
st.caption(f"Matcher version: {MATCHER_VERSION}")

if uploaded_files:
    resume_profiles = []

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        try:
            raw_text = extract_text_from_pdf(temp_path)
            profile = build_resume_profile(raw_text)

            resume_profiles.append(
                {
                    "filename": uploaded_file.name,
                    "raw_text": raw_text,
                    "profile": profile,
                }
            )

        except Exception as e:
            st.error(f"Failed to extract {uploaded_file.name}: {e}")
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass

    if resume_profiles:
        st.success(f"Extracted {len(resume_profiles)} resume(s) successfully.")

        if len(resume_profiles) == 1:
            profile = resume_profiles[0]["profile"]
            raw_text = resume_profiles[0]["raw_text"]

            tab1, tab2, tab3 = st.tabs(["Extracted Text", "Structured Profile", "Raw JSON"])

            with tab1:
                st.text_area("Resume text", raw_text, height=500)

            with tab2:
                basic = profile["basic_info"]

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("### Basic Info")
                    st.write(f"**Name guess:** {basic['name_guess']}")
                    st.write(f"**Email:** {basic['email'] or 'Not found'}")
                    st.write(f"**Phone:** {basic['phone'] or 'Not found'}")
                with c2:
                    st.markdown("### Links")
                    st.write(f"**LinkedIn:** {basic['linkedin'] or 'Not found'}")
                    st.write(f"**GitHub:** {basic['github'] or 'Not found'}")

                st.markdown("### Sections Found")
                st.write(", ".join(profile["sections"].keys()))

                render_list("Skills", profile["skills"])
                render_list("Experience", profile["experience"])
                render_list("Education", profile["education"])
                render_list("Projects", profile["projects"])
                render_list("Certifications", profile["certifications"])

            with tab3:
                st.json(profile)

        if st.button("Score Against Job Description"):
            if not job_description.strip():
                st.warning("Please paste a job description first.")
            else:
                if len(resume_profiles) == 1:
                    result = compute_match_score(resume_profiles[0]["raw_text"], job_description)

                    score = result.get("score", 0.0)
                    semantic_score = result.get("semantic_score", score)
                    keyword_score = result.get("keyword_score", 0.0)
                    matched_terms = result.get("matched_terms", [])
                    missing_terms = result.get("missing_terms", [])

                    st.markdown("## Match Score")
                    st.metric("Resume match", f"{score}%")

                    st.caption(
                        f"Semantic score: {semantic_score}% | Keyword score: {keyword_score}%"
                    )

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("### Overlapping terms")
                        if matched_terms:
                            for term in matched_terms:
                                st.markdown(f"- {term}")
                        else:
                            st.caption("No obvious overlap found.")
                    with col_b:
                        st.markdown("### Missing terms")
                        if missing_terms:
                            for term in missing_terms:
                                st.markdown(f"- {term}")
                        else:
                            st.caption("No major missing terms found.")

                else:
                    df = rank_resumes(resume_profiles, job_description)

                    st.markdown("## Ranked Candidates")

                    display_df = df[
                        [
                            "filename",
                            "score",
                            "semantic_score",
                            "keyword_score",
                            "matched_terms",
                            "missing_terms",
                        ]
                    ]

                    st.dataframe(display_df, use_container_width=True, hide_index=True)

                    st.markdown("### Top 3 Candidates")

                    top_n = df.head(3)
                    if not top_n.empty:
                        cols = st.columns(len(top_n))
                        for idx, (_, row) in enumerate(top_n.iterrows()):
                            with cols[idx]:
                                st.markdown(
                                    f"""
                                    <div class="metric-card">
                                        <h3>#{idx + 1}</h3>
                                        <p><strong>{row['filename']}</strong></p>
                                        <p><strong>Score:</strong> {row['score']}%</p>
                                        <p><strong>Semantic:</strong> {row['semantic_score']}%</p>
                                        <p><strong>Keyword:</strong> {row['keyword_score']}%</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                st.progress(min(float(row["score"]) / 100.0, 1.0))
                                st.caption(f"Matched terms: {row['matched_terms'] or 'None'}")
                                st.caption(f"Missing terms: {row['missing_terms'] or 'None'}")
else:
    st.info("Upload one or more PDFs to see parsed resumes here.")
