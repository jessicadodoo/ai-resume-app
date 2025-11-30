def detect_sections(text):
    text_lower = text.lower()
    sections = ["education", "skills", "projects", "experience", "certifications", "contact"]
    sections_present = []
    missing_sections = []

    for sec in sections:
        if sec in text_lower:
            sections_present.append(sec)
        else:
            missing_sections.append(sec)

    return sections_present, missing_sections
