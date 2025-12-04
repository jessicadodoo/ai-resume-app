# analyzer/analyzer.py
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_suggestions_with_llm(resume_text, job_title, requirements, details):
    """
    If GROQ_API_KEY is available, call Groq LLM to create human-like suggestions.
    This function shows the prompt structure — you'll need Groq client installed and set up.
    If there is no API key or call fails, raise an exception so caller can fallback.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("No Groq API key configured")

    # Lazy import to avoid hard dependency if not used
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
You are an expert career advisor. The user wants to become a {job_title}.
Resume text:
{resume_text[:5000]}

Detected requirements:
Skills: {requirements.get('skills')[:20]}
Tools: {requirements.get('tools')[:20]}
Certifications: {requirements.get('certifications')[:20]}

Detected matches: {details}

Produce:
1) Short strengths (3 bullets)
2) Missing skills/tools/certifications (3 bullets)
3) Concrete next steps and suggested resources (3 bullets)
Keep it concise.
"""
    response = client.chat.completions.create(
        messages=[{"role":"user","content":prompt}],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content

def generate_heuristic_suggestions(resume_text, job_title, requirements, details):
    """
    Generate simple but useful suggestions when LLM is not available.
    """
    suggestions = []
    if details["matched_skills"]:
        suggestions.append(f"Strengths: {', '.join(details['matched_skills'][:5])}")
    else:
        suggestions.append("Strengths: None of the top-listed role skills were detected in your resume.")

    missing = []
    if requirements.get("skills"):
        missing_skills = [s for s in requirements["skills"] if s not in details["matched_skills"]]
        missing += missing_skills[:6]
    if requirements.get("tools"):
        missing_tools = [t for t in requirements["tools"] if t not in details["matched_tools"]]
        missing += missing_tools[:4]
    if requirements.get("certifications"):
        missing += requirements.get("certifications", [])[:3]

    if missing:
        suggestions.append("Missing / Weak: " + ", ".join(missing[:8]))
    else:
        suggestions.append("No major missing skills detected among the top scraped items.")

    # Actionable next steps
    suggestions.append("Next steps: 1) Add project examples that show hands-on work; 2) Take short courses for missing tools (e.g., SIEM); 3) Mention measurable results (percentages, numbers).")

    return "\n".join(suggestions)
