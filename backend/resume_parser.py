from pathlib import Path
import re
from typing import Any


def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        return "\n".join(page.extract_text() or "" for page in PdfReader(file_path).pages)
    if suffix == ".docx":
        from docx import Document

        return "\n".join(paragraph.text for paragraph in Document(file_path).paragraphs)
    raise ValueError("Only PDF and DOCX resumes are supported")


def parse_resume(file_path: Path) -> dict[str, Any]:
    text = extract_text(file_path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone_match = re.search(r"(?:\+?\d[\d ()-]{7,}\d)", text)
    sections = _extract_sections(lines)
    return {
        "name": lines[0] if lines else "",
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "skills": _find_skills(text),
        "experience": sections.get("experience", []),
        "education": sections.get("education", []),
        "projects": sections.get("projects", []),
        "raw_text": text,
    }


def _extract_sections(lines: list[str]) -> dict[str, list[str]]:
    headings = {"experience", "work experience", "education", "projects"}
    sections: dict[str, list[str]] = {}
    current = "summary"
    sections[current] = []
    for line in lines:
        normalized = line.lower().rstrip(":")
        if normalized in headings:
            current = normalized.split()[0]
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)
    return sections


def _find_skills(text: str) -> list[str]:
    known_skills = ["python", "javascript", "typescript", "java", "sql", "react", "fastapi", "aws", "azure", "docker", "git", "machine learning"]
    lowered = text.lower()
    return [skill for skill in known_skills if skill in lowered]
