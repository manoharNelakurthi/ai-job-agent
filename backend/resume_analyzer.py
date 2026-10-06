from typing import Any


def analyze_resume(resume: dict[str, Any]) -> dict[str, Any]:
    skills = resume.get("skills", [])
    sections = [key for key in ("experience", "education", "projects") if resume.get(key)]
    score = min(100, len(skills) * 7 + len(sections) * 12 + (10 if resume.get("email") else 0))
    suggestions = []
    if not resume.get("email"):
        suggestions.append("Add a professional email address.")
    if not resume.get("experience"):
        suggestions.append("Add measurable work experience or internship results.")
    if not resume.get("projects"):
        suggestions.append("Include projects that demonstrate your strongest skills.")
    if len(skills) < 5:
        suggestions.append("Mirror relevant keywords from target job descriptions.")
    return {"ats_score": score, "detected_skills": skills, "sections_found": sections, "suggestions": suggestions}
