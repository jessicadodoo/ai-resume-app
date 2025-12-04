# analyzer/web_scraper.py
import requests
from bs4 import BeautifulSoup
from collections import Counter
import time
import string

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/142.0.0.0 Safari/537.36"
}

# A small fallback bank used only if scraping fails or returns nothing
FALLBACK_BANK = {
    "cybersecurity": ["network security","incident response","siem","threat detection","penetration testing","linux","firewalls","python","vulnerability assessment","wireshark","forensics","risk assessment"],
    "data scientist": ["python","machine learning","sql","data analysis","pandas","numpy","statistics","modeling","visualization","feature engineering"],
    "software engineer": ["python","java","git","api","react","algorithms","data structures","testing"],
}

def _text_to_keywords(raw_text, top_n=25):
    translator = str.maketrans("", "", string.punctuation)
    tokens = [w.translate(translator) for w in raw_text.lower().split()]
    tokens = [t for t in tokens if len(t) > 3 and not t.isnumeric()]
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_n)]

def fetch_job_requirements(job_title, limit=10):
    """
    Scrape Indeed for job listings for the given title and return a dict:
    {'skills': [...], 'tools': [...], 'certifications': [...]}
    This is heuristic: we extract top terms from job snippets and titles.
    If scraping fails or returns nothing, fallback to curated keywords.
    """
    job_title_q = job_title.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={job_title_q}&limit={limit}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        time.sleep(0.5)  # polite pause
        if resp.status_code != 200:
            raise RuntimeError(f"Non-200 status: {resp.status_code}")
        soup = BeautifulSoup(resp.text, "html.parser")

        texts = []
        # job titles
        for t in soup.find_all(attrs={"class": "jobTitle"}):
            texts.append(t.get_text(separator=" ").strip())
        # job snippets/descriptions
        for s in soup.find_all("div", class_="job-snippet"):
            texts.append(s.get_text(separator=" ").strip())

        combined = " ".join(texts)
        keywords = _text_to_keywords(combined, top_n=40)
        # Heuristic split: first half as skills, next as tools/certs (simple)
        half = max(8, len(keywords)//2)
        skills = keywords[:half]
        tools = keywords[half:half+10]
        certs = [w for w in keywords if "cert" in w or "security+" in w.lower()]  # quick cert detection
        # If nothing found, fallback
        if not skills:
            raise RuntimeError("No keywords parsed")
        return {"skills": skills, "tools": tools, "certifications": certs}
    except Exception:
        # fallback to curated bank or simple tokenization of job_title
        jt = job_title.lower()
        for k in FALLBACK_BANK:
            if k in jt:
                return {"skills": FALLBACK_BANK[k], "tools": [], "certifications": []}
        # generic fallback
        generic = job_title.split()[:3]
        return {"skills": generic, "tools": [], "certifications": []}
