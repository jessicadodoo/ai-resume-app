# analyzer/detect_sections.py
def detect_sections(text):
    """
    Detects main resume sections: experience, skills, projects, education.
    Returns (sections_present, missing_sections).
    """
    text_lower = text.lower()
    sections = ["experience", "work experience", "employment", "skills", "projects", "education", "certifications"]
    sections_present = []
    for sec in sections:
        if sec in text_lower:
            sections_present.append(sec)
    # For user-friendly output, normalize primary types
    present_primary = []
    for primary in ["experience", "skills", "projects", "education", "certifications"]:
        if any(primary in s for s in sections_present):
            present_primary.append(primary)
    missing = [p for p in ["experience", "skills", "projects", "education", "certifications"] if p not in present_primary]
    return present_primary, missing
