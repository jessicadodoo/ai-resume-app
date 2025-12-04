# analyzer/report_generator.py
from datetime import datetime

def build_text_report(job_title, score, requirements, details, suggestions_text):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    rep = []
    rep.append("===== Resume Analysis Report =====")
    rep.append(f"Job Title analyzed: {job_title}")
    rep.append(f"Date: {now}")
    rep.append(f"\nOverall Score: {score}/100\n")
    rep.append("=== Requirements considered ===")
    rep.append(f"Top skills considered: {', '.join(requirements.get('skills', [])[:25])}")
    if requirements.get("tools"):
        rep.append(f"Tools considered: {', '.join(requirements.get('tools', [])[:25])}")
    if requirements.get("certifications"):
        rep.append(f"Certifications considered: {', '.join(requirements.get('certifications', [])[:25])}")
    rep.append("\n=== Matches found ===")
    rep.append(f"Matched skills: {', '.join(details.get('matched_skills', [])) or 'None'}")
    rep.append(f"Matched tools: {', '.join(details.get('matched_tools', [])) or 'None'}")
    rep.append(f"Matched certs: {', '.join(details.get('matched_certs', [])) or 'None'}")
    rep.append(f"\nMissing sections: {', '.join(details.get('missing_sections', [])) or 'None'}")
    rep.append("\n=== Suggestions ===")
    rep.append(suggestions_text)
    rep.append("\n===================================")
    return "\n".join(rep)
