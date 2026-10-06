from typing import Any

from .cover_letter_generator import generate_cover_letter
from .database import create_application


def prepare_application(resume: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    return {
        "job_title": job.get("title", ""),
        "company": job.get("company", ""),
        "status": "pending_approval",
        "cover_letter": generate_cover_letter(resume, job),
        "form_data": {"name": resume.get("name", ""), "email": resume.get("email", ""), "phone": resume.get("phone", "")},
    }


def save_application(application: dict[str, Any]) -> int:
    return create_application(application)
