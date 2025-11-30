import streamlit as st
from analyzer.extract import extract_text
from analyzer.detect_sections import detect_sections
from analyzer.score import score_resume
import json



st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")

# Load keywords
with open("analyzer/keywords.json") as f:
    keywords = json.load(f)

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.success("Resume uploaded successfully!")

    # Extract text
    text = extract_text(uploaded_file)

    # Detect sections
    sections_present, missing_sections = detect_sections(text)

    # Score resume
    score, keyword_matches = score_resume(text, keywords)

    # Display score
    st.subheader("📊 Resume Score")
    st.progress(score)
    st.write(f"**Score:** {score}/100")

    # Display missing sections
    if missing_sections:
        st.subheader("⚠ Missing Sections")
        st.write(missing_sections)
    else:
        st.success("All key sections are present!")

    # Display keyword matches
    st.subheader("🔑 Keyword Analysis")
    st.write("Keywords found:")
    st.write(keyword_matches)

    # Suggestions
    st.subheader("📝 Suggestions")
    if "projects" in missing_sections:
        st.write("- Add a Projects section with at least 2 examples.")
    if "skills" in missing_sections:
        st.write("- Add a Skills section with technical and soft skills.")
    if "experience" in missing_sections:
        st.write("- Include measurable achievements in Experience section.")
    if score < 80:
        st.write("- Consider adding keywords relevant to the job description.")
    st.write("- Keep resume concise and clear for readability.")
