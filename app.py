"""
AI Resume Screening & Job Description Matching System
Streamlit front-end tying together resume parsing + NLP matching.
"""
import streamlit as st
from resume_parser import extract_text
from matcher import analyze

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🧠",
    layout="wide",
)

# ---------- Minimal styling ----------
st.markdown("""
<style>
    .big-score { font-size: 3rem; font-weight: 700; }
    .skill-pill {
        display: inline-block; padding: 4px 12px; margin: 3px;
        border-radius: 16px; font-size: 0.85rem;
    }
    .pill-match { background-color: #d1f5d3; color: #1a7431; }
    .pill-missing { background-color: #ffd9d9; color: #a10000; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Resume Screening & Job Description Matching")
st.caption("Upload a resume and a job description to get a match score, skill gap analysis, and recommendations.")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"], key="resume")
    resume_text_input = st.text_area(
        "...or paste resume text",
        height=200,
        placeholder="Paste resume content here if you'd rather not upload a file.",
    )

with col_right:
    st.subheader("📋 Job Description")
    jd_file = st.file_uploader("Upload job description", type=["pdf", "docx", "txt"], key="jd")
    jd_text_input = st.text_area(
        "...or paste job description text",
        height=200,
        placeholder="Paste the job description here if you'd rather not upload a file.",
    )

st.divider()
analyze_clicked = st.button("🔍 Analyze Match", type="primary", use_container_width=True)

if analyze_clicked:
    # Resolve resume text: uploaded file takes priority over pasted text
    try:
        if resume_file is not None:
            resume_text = extract_text(resume_file)
        elif resume_text_input.strip():
            resume_text = resume_text_input
        else:
            resume_text = None

        if jd_file is not None:
            jd_text = extract_text(jd_file)
        elif jd_text_input.strip():
            jd_text = jd_text_input
        else:
            jd_text = None
    except ValueError as e:
        st.error(str(e))
        st.stop()

    if not resume_text or not jd_text:
        st.warning("Please provide both a resume and a job description (upload a file or paste text) before analyzing.")
        st.stop()

    if not resume_text.strip() or not jd_text.strip():
        st.warning("One of the provided documents appears to be empty. Please check the file/text and try again.")
        st.stop()

    with st.spinner("Analyzing resume against job description..."):
        result = analyze(resume_text, jd_text)

    st.divider()
    st.header("Results")

    # --- Top-level metrics ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Overall Match Score", f"{result['match_score']}%")
    m2.metric("Skill Coverage", f"{result['skill_coverage']}%")
    m3.metric("Matched Skills", len(result["matching_skills"]))
    m4.metric("Missing Skills", len(result["missing_skills"]))

    st.progress(min(int(result["match_score"]), 100), text=f"Overall Match: {result['match_score']}%")

    st.divider()

    # --- Skills breakdown ---
    sc1, sc2 = st.columns(2)

    with sc1:
        st.subheader("✅ Matching Skills")
        if result["matching_skills"]:
            pills = "".join(f'<span class="skill-pill pill-match">{s}</span>' for s in result["matching_skills"])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.write("No overlapping skills detected.")

    with sc2:
        st.subheader("❌ Missing Skills")
        if result["missing_skills"]:
            pills = "".join(f'<span class="skill-pill pill-missing">{s}</span>' for s in result["missing_skills"])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.write("No missing skills — great coverage!")

    st.divider()

    # --- Full skill lists in expanders ---
    with st.expander("📄 All skills detected in resume"):
        st.write(", ".join(result["resume_skills"]) if result["resume_skills"] else "None detected.")

    with st.expander("📋 All skills required by job description"):
        st.write(", ".join(result["jd_skills"]) if result["jd_skills"] else "None detected.")

    st.divider()

    # --- Recommendations ---
    st.subheader("💡 Recommendations")
    for rec in result["recommendations"]:
        st.info(rec)

else:
    st.info("Upload or paste a resume and job description above, then click **Analyze Match** to get started.")

st.divider()
st.caption("Built with spaCy, TF-IDF, and Cosine Similarity · Streamlit interface")
