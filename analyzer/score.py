def score_resume(text, keywords):
    text_lower = text.lower()
    score = 0
    keyword_matches = []

    # Section-based scoring
    sections = ["education", "skills", "projects", "experience"]
    for sec in sections:
        if sec in text_lower:
            score += 20  # each section 20 points

    # Keyword scoring
    total_keywords = len(keywords)
    found_keywords = 0
    for kw in keywords:
        if kw.lower() in text_lower:
            found_keywords += 1
            keyword_matches.append(kw)

    if total_keywords > 0:
        score += int((found_keywords / total_keywords) * 40)  # max 40 points

    # Cap score at 100
    if score > 100:
        score = 100

    return score, keyword_matches
