import streamlit as st
from analyzer.extract import extract_text
from analyzer.detect_sections import detect_sections
from analyzer.web_scraper import fetch_job_requirements
from analyzer.score import score_resume
from analyzer.analyzer import generate_suggestions_with_llm, generate_heuristic_suggestions
from analyzer.report_generator import build_text_report

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.markdown("<h1 style='text-align:center; color:#4CAF50;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- SIDEBAR --------------------
st.sidebar.header("Job & Options")
job_title = st.sidebar.text_input(
    "Preferred job title (e.g., cybersecurity analyst)", 
    value=st.session_state.get("job_title", "")
)
st.session_state["job_title"] = job_title

use_llm = st.sidebar.checkbox(
    "Use Groq LLM for polished suggestions (optional)", value=False
)

uploaded = st.sidebar.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf","docx"])
analyze_button = st.sidebar.button("Analyze Resume")

# -------------------- MAIN UI --------------------
if uploaded and job_title.strip() and analyze_button:
    st.info("Extracting resume text...")
    text = extract_text(uploaded)
    st.success("Text extracted. Running analysis...")

    sections_present, missing_sections = detect_sections(text)

    st.info("Fetching live job requirements from the web...")
    requirements = fetch_job_requirements(job_title)

    st.info("Scoring resume...")
    score, details = score_resume(text, requirements, sections_present)

    # -------------------- SCORE & SECTIONS --------------------
    st.subheader("📊 Resume Score")
    st.progress(score)
    st.write(f"**Score:** {score}/100")

    st.subheader("🔎 Detected Sections")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Present Sections:")
        st.write(sections_present)
    with col2:
        if missing_sections:
            st.warning("Missing Sections:")
            st.write(missing_sections)

    # -------------------- JOB REQUIREMENTS --------------------
    st.subheader("🔑 Top Requirements (from Web Scrape)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Skills:")
        st.write(requirements.get("skills", [])[:20])
    with col2:
        st.write("Tools:")
        st.write(requirements.get("tools", [])[:15])
    with col3:
        st.write("Certifications:")
        st.write(requirements.get("certifications", [])[:10])

    # -------------------- MATCHES --------------------
    st.subheader("✅ Matches Found in Resume")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Skills Matched:")
        st.write(details.get("matched_skills", []))
    with col2:
        st.write("Tools Matched:")
        st.write(details.get("matched_tools", []))
    with col3:
        st.write("Certifications Matched:")
        st.write(details.get("matched_certs", []))

    # -------------------- SUGGESTIONS --------------------
    st.subheader("📝 Suggestions")
    suggestions_text = ""
    if use_llm:
        try:
            suggestions_text = generate_suggestions_with_llm(text, job_title, requirements, details)
        except Exception:
            st.warning("LLM suggestion failed — using heuristic suggestions.")
            suggestions_text = generate_heuristic_suggestions(text, job_title, requirements, details)
    else:
        suggestions_text = generate_heuristic_suggestions(text, job_title, requirements, details)
    
    with st.expander("View Suggestions"):
        st.text(suggestions_text)

    # -------------------- DOWNLOAD REPORT --------------------
    report_text = build_text_report(job_title, score, requirements, details, suggestions_text)
    st.download_button(
        "Download Full Report", 
        data=report_text, 
        file_name="resume_analysis_report.txt", 
        mime="text/plain"
    )

    # -------------------- RESUME PREVIEW --------------------
    with st.expander("View Extracted Resume Text"):
        st.text(text)

else:
    st.info("Enter a job title, upload your resume, and click 'Analyze Resume' in the sidebar.")
    
# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Made with ❤️ by Jessica | <a href='https://github.com/jessicadodoo/ai-resume-app'>GitHub Repo</a></p>", 
    unsafe_allow_html=True
)
