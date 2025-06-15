
from keywords import DOMAIN_KEYWORDS

def score_resume(text, domain):
    keywords = DOMAIN_KEYWORDS[domain]
    text_lower = text.lower()

    matched = [kw for kw in keywords if kw.lower() in text_lower]
    missing = [kw for kw in keywords if kw.lower() not in text_lower]

    keyword_score = min(10, round((len(matched) / len(keywords)) * 10))

    structure_score = 7 if "experience" in text_lower and "education" in text_lower else 4
    edu_score = 7 if "certification" in text_lower or "degree" in text_lower else 5
    exp_score = 5 if "intern" in text_lower or "worked" in text_lower else 3
    impact_score = 8 if any(word in text_lower for word in ["led", "improved", "managed", "increased"]) else 5

    breakdown = {
        "Keywords": keyword_score,
        "Structure & Format": structure_score,
        "Edu & Cert": edu_score,
        "Experience": exp_score,
        "Impact Language": impact_score,
    }

    total_score = round(sum(breakdown.values()) / 5)

    suggestions = []
    if keyword_score < 6:
        suggestions.append(f"Add more domain-specific keywords.")
    if structure_score < 6:
        suggestions.append("Include sections like Education and Experience.")
    if edu_score < 6:
        suggestions.append("Highlight certifications or degrees.")
    if exp_score < 4:
        suggestions.append("Mention relevant experience or internships.")
    if impact_score < 6:
        suggestions.append("Use more action and impact-oriented language.")

    return total_score, breakdown, suggestions, missing

def analyze_resume_sections(text):
    feedback = []
    text_lower = text.lower()

    if "education" not in text_lower:
        feedback.append("Education section not clearly mentioned.")
    if "experience" not in text_lower:
        feedback.append("Experience section seems missing.")
    if "skills" not in text_lower:
        feedback.append("Consider adding a 'Skills' section.")
    if "projects" not in text_lower:
        feedback.append("Highlighting key projects can improve impact.")
    return feedback
