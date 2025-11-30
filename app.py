import streamlit as st
from analyzer.extract import extract_text
from analyzer.score import calculate_score
from analyzer.detect_sections import detect_sections
import json

# ----------------------
# Streamlit Page Setup
# ----------------------
st.set_page_config(
    page_title="AI Resume & Job Fit Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------
# Sidebar: Light/Dark Mode & Job Input
# ----------------------
st.sidebar.title("Settings & Job Search")

# Light/Dark mode toggle
mode = st.sidebar.radio("Select Theme", ["Light Mode", "Dark Mode"])
if mode == "Dark Mode":
    st.markdown(
        """
        <style>
        body { background-color: #0E1117; color: #FFFFFF; }
        .stProgress > div > div { background-color: #00ff00; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: #FFFFFF; color: #000000; }
        .stProgress > div > div { background-color: #00ff00; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Job position input
job_title = st.sidebar.text_input("Job Title / Position you're applying for", "")

# ----------------------
# Main Page
# ----------------------
st.title("📄 AI Resume & Job Fit Analyzer")
st.write("Upload your resume (PDF or DOCX) and check how well it matches your desired job.")

uploaded_file = st.file_uploader("Choose your resume", type=["pdf", "docx"])

# ----------------------
# Load keywords and job projects
# ----------------------
with open("analyzer/keywords.json") as f:
    all_keywords = json.load(f)

with open("analyzer/job_projects.json") as f:
    job_projects = json.load(f)  # Example: { "Cybersecurity": ["Project1", "Project2"], ... }

# ----------------------
# Process Resume
# ----------------------
if uploaded_file and job_title:
    text = extract_text(uploaded_file)

    # Section detection
    sections = detect_sections(text)
    st.header("✅ Sections Detected")
    for sec, present in sections.items():
        if present:
            st.success(f"{sec}: Present")
        else:
            st.error(f"{sec}: Missing")

    # Resume Score
    overall_score = calculate_score(text, all_keywords)
    st.header("🏆 Overall Resume Score")
    st.progress(overall_score / 100)
    st.write(f"Score: **{overall_score}/100**")

    # Job-fit Score
    job_keywords = job_projects.get(job_title, [])  # keywords for the job
    matched_keywords = [kw for kw in job_keywords if kw.lower() in text.lower()]
    job_fit_score = int((len(matched_keywords) / len(job_keywords)) * 100) if job_keywords else 0

    st.header(f"🎯 Job-Fit Score for '{job_title}'")
    st.progress(job_fit_score / 100)
    st.write(f"Job Fit: **{job_fit_score}%**")

    # Keywords Table
    st.header("🔑 Keyword Analysis")
    st.subheader("Found Keywords ✅")
    st.write(matched_keywords if matched_keywords else "None found")
    st.subheader("Missing Keywords ❌")
    missing_keywords = [kw for kw in job_keywords if kw not in matched_keywords]
    st.write(missing_keywords if missing_keywords else "None missing")

    # Recommendations & Projects
    st.header("💡 Recommendations & Projects")
    with st.expander("Click to see suggestions"):
        if job_fit_score < 50:
            st.write("- Consider adding more relevant skills and experiences.")
            st.write("- Suggested projects to improve your profile:")
            for p in missing_keywords:
                st.write(f"  • {p}")
        elif job_fit_score < 80:
            st.write("- Good job! Add a few more skills/projects for better fit.")
            for p in missing_keywords:
                st.write(f"  • {p}")
        else:
            st.write("Excellent fit! Your resume matches this role very well.")

    # Career Suggestions
    st.header("🚀 Possible Career Paths")
    st.write("Based on your skills and experience, you could consider applying to:")
    # Example: naive suggestion based on matched keywords
    suggested_jobs = []
    for job, keywords in job_projects.items():
        score = len([kw for kw in keywords if kw.lower() in text.lower()]) / max(1, len(keywords))
        if score > 0.5:
            suggested_jobs.append(job)
    st.write(suggested_jobs if suggested_jobs else "No strong matches found — consider adding more skills/projects.")

else:
    st.info("Please enter the job title and upload your resume to analyze.")
