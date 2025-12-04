# app.py
import streamlit as st
from analyzer.extract import extract_text
from analyzer.detect_sections import detect_sections
from analyzer.web_scraper import fetch_job_requirements
from analyzer.score import score_resume
from analyzer.analyzer import generate_suggestions_with_llm, generate_heuristic_suggestions
from analyzer.report_generator import build_text_report
import os

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer — job-title driven (web-backed)")

# Sidebar inputs
st.sidebar.header("Job & Options")
job_title = st.sidebar.text_input("Preferred job title (e.g., cybersecurity analyst)", value=st.session_state.get("job_title",""))
st.session_state["job_title"] = job_title

use_llm = st.sidebar.checkbox("Use Groq LLM for polished suggestions (optional)", value=False)

uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf","docx"])

if uploaded and job_title.strip():
    st.info("Extracting resume text...")
    text = extract_text(uploaded)
    st.success("Text extracted. Running analysis...")

    sections_present, missing_sections = detect_sections(text)

    st.info("Fetching live job requirements from the web...")
    requirements = fetch_job_requirements(job_title)

    st.info("Scoring resume...")
    score, details = score_resume(text, requirements, sections_present)

    st.subheader("📊 Score")
    st.progress(score)
    st.write(f"**Score:** {score}/100")

    st.subheader("🔎 Detected sections")
    st.write(sections_present)
    if missing_sections:
        st.warning(f"Missing: {missing_sections}")

    st.subheader("🔑 Top requirements (from web scrape)")
    st.write("Skills:", requirements.get("skills", [])[:20])
    st.write("Tools:", requirements.get("tools", [])[:15])
    st.write("Certifications:", requirements.get("certifications", [])[:10])

    st.subheader("✅ Matches found in resume")
    st.write("Skills matched:", details.get("matched_skills", []))
    st.write("Tools matched:", details.get("matched_tools", []))
    st.write("Certifications matched:", details.get("matched_certs", []))

    # Suggestions: try LLM if asked and key present, otherwise fallback
    suggestions_text = ""
    if use_llm:
        try:
            suggestions_text = generate_suggestions_with_llm(text, job_title, requirements, details)
        except Exception as e:
            st.warning("LLM suggestion failed — falling back to heuristic suggestions.")
            suggestions_text = generate_heuristic_suggestions(text, job_title, requirements, details)
    else:
        suggestions_text = generate_heuristic_suggestions(text, job_title, requirements, details)

    st.subheader("📝 Suggestions")
    st.text(suggestions_text)

    # Build and provide downloadable report
    report_text = build_text_report(job_title, score, requirements, details, suggestions_text)
    st.download_button("Download full report", data=report_text, file_name="resume_analysis_report.txt", mime="text/plain")

else:
    st.info("Enter a job title in the sidebar and upload your resume to start.")
