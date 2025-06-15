
import streamlit as st
import fitz  # PyMuPDF
import re
from scorer import score_resume, analyze_resume_sections
from keywords import DOMAIN_KEYWORDS

st.set_page_config(page_title="AI Resume Scorer", layout="centered")

st.markdown("""
    <style>
        .title {
            font-size: 2.5em;
            color: #2c3e50;
            font-weight: bold;
        }
        .subsection {
            background-color: #f9f9f9;
            padding: 1em;
            border-radius: 10px;
            margin-top: 10px;
            border-left: 5px solid #3498db;
        }
        .suggestion {
            color: #e74c3c;
            font-weight: 500;
        }
        .highlight {
            color: #e67e22;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📄 AI Resume Scorer</div>", unsafe_allow_html=True)

domain = st.selectbox("Select Domain", list(DOMAIN_KEYWORDS.keys()))

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    score, breakdown, suggestions, missing_keywords = score_resume(text, domain)
    section_feedback = analyze_resume_sections(text)

    st.markdown(f"<div class='subsection'><b>🔢 Total Score:</b> {score} / 10</div>", unsafe_allow_html=True)

    st.markdown("<div class='subsection'><b>🧩 Breakdown:</b>", unsafe_allow_html=True)
    for k, v in breakdown.items():
        st.markdown(f"- **{k}**: {v}")
    st.markdown("</div>", unsafe_allow_html=True)

    if missing_keywords:
        st.markdown("<div class='subsection'><b>🚫 Missing Important Keywords:</b>", unsafe_allow_html=True)
        for kw in missing_keywords:
            st.markdown(f"<span class='highlight'>• {kw}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if section_feedback:
        st.markdown("<div class='subsection'><b>🔍 Section Feedback:</b>", unsafe_allow_html=True)
        for fb in section_feedback:
            st.markdown(f"<span class='suggestion'>• {fb}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if suggestions:
        st.markdown("<div class='subsection'><b>💡 Suggestions:</b>", unsafe_allow_html=True)
        for s in suggestions:
            st.markdown(f"<span class='suggestion'>• {s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
