from typing import Any


def generate_cover_letter(resume: dict[str, Any], job: dict[str, Any]) -> str:
    name = resume.get("name") or "Candidate"
    skills = ", ".join(resume.get("skills", [])[:5]) or "relevant technical skills"
    return (
        f"Dear {job.get('company', 'Hiring Team')} team,\n\n"
        f"I am excited to apply for the {job.get('title', 'role')} position. "
        f"My background includes {skills}, and I would welcome the opportunity to contribute to your team.\n\n"
        f"Thank you for your consideration.\n\nSincerely,\n{name}"
    )
