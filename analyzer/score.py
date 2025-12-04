# analyzer/score.py
import math

def score_resume(resume_text, requirements, sections_present):
    """
    requirements: dict with lists: 'skills', 'tools', 'certifications'
    sections_present: list of present primary sections
    Returns (score_percent, details dict)
    """
    resume_lower = resume_text.lower()
    skills = requirements.get("skills", [])
    tools = requirements.get("tools", [])
    certs = requirements.get("certifications", [])

    match_skills = [s for s in skills if s.lower() in resume_lower]
    match_tools = [t for t in tools if t.lower() in resume_lower]
    match_certs = [c for c in certs if c.lower() in resume_lower]

    # Percent coverage (weighted)
    w_skills = 0.6
    w_tools = 0.25
    w_certs = 0.15

    # avoid division by zero
    skill_pct = (len(match_skills) / len(skills)) if skills else 0
    tool_pct = (len(match_tools) / len(tools)) if tools else 0
    cert_pct = (len(match_certs) / len(certs)) if certs else 0

    base_score = w_skills*skill_pct + w_tools*tool_pct + w_certs*cert_pct
    base_percent = int(base_score * 100)

    # Section bonus/penalty
    missing_sections = [s for s in ["experience", "skills", "projects", "education"] if s not in sections_present]
    section_penalty = max(0, len(missing_sections)) * 5  # -5 per missing section
    final_percent = max(0, base_percent - section_penalty)

    # small floor if some matches found
    if final_percent == 0 and (match_skills or match_tools or match_certs):
        final_percent = max(10, min(30, base_percent))

    details = {
        "matched_skills": match_skills,
        "matched_tools": match_tools,
        "matched_certs": match_certs,
        "skill_count": len(skills),
        "tool_count": len(tools),
        "cert_count": len(certs),
        "missing_sections": missing_sections
    }
    return final_percent, details
