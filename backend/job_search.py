from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
JOBS_PATH = ROOT / "database" / "jobs.json"


def _default_jobs() -> list[dict[str, Any]]:
    return [
        {"id": "demo-1", "title": "Python Backend Engineer", "company": "Northstar Labs", "location": "Remote", "skills": ["python", "fastapi", "sql", "postgresql"]},
        {"id": "demo-2", "title": "Full Stack Developer", "company": "Cedar Systems", "location": "New York", "skills": ["javascript", "react", "sql", "nodejs"]},
        {"id": "demo-3", "title": "Cloud Software Engineer", "company": "Blue Harbor", "location": "Remote", "skills": ["python", "docker", "azure", "aws"]},
        {"id": "demo-4", "title": "Data Engineer", "company": "Atlas Analytics", "location": "Austin", "skills": ["python", "sql", "spark", "etl"]},
        {"id": "demo-5", "title": "ML Engineer", "company": "VisionForge", "location": "Remote", "skills": ["python", "machine learning", "pytorch", "model deployment"]},
        {"id": "demo-6", "title": "DevOps Engineer", "company": "Nimbus Cloud", "location": "Chicago", "skills": ["docker", "kubernetes", "aws", "linux"]},
        {"id": "demo-7", "title": "Frontend Engineer", "company": "Pixel Harbor", "location": "Remote", "skills": ["javascript", "react", "typescript", "css"]},
        {"id": "demo-8", "title": "Backend Engineer", "company": "SummitIQ", "location": "Boston", "skills": ["python", "django", "rest api", "redis"]},
        {"id": "demo-9", "title": "Security Engineer", "company": "Horizon Secure", "location": "San Francisco", "skills": ["python", "cybersecurity", "aws", "security tools"]},
        {"id": "demo-10", "title": "Platform Engineer", "company": "HarborOne", "location": "Remote", "skills": ["kubernetes", "terraform", "aws", "linux"]},
    ]


def _load_jobs() -> list[dict[str, Any]]:
    if JOBS_PATH.exists():
        try:
            jobs = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
            if isinstance(jobs, list) and jobs:
                return jobs
        except (json.JSONDecodeError, OSError):
            pass
    return _default_jobs()


# Provider adapters can be added here without changing matching or application logic.
def search_jobs(query: str, location: str = "") -> list[dict[str, Any]]:
    jobs = _load_jobs()
    query_terms = [term.lower() for term in query.split() if term]
    location_filter = location.strip().lower()

    filtered_jobs = jobs
    if location_filter:
        filtered_jobs = [
            job for job in filtered_jobs
            if location_filter in (job.get("location", "") or "").lower()
        ]

    if query_terms:
        filtered_jobs = [
            job for job in filtered_jobs
            if any(term in (job.get("title", "") or "").lower()
                   for term in query_terms)
               or any(term in " ".join(job.get("skills", [])).lower()
                      for term in query_terms)
        ]

    return filtered_jobs


def refresh_jobs() -> list[dict[str, Any]]:
    """Return the latest jobs list, allowing the project to refresh its dataset."""
    return _load_jobs()
