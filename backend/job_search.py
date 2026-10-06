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
        {"id": "demo-11", "title": "Python Developer", "company": "StackForge", "location": "Remote", "skills": ["python", "flask", "api", "redis"]},
        {"id": "demo-12", "title": "Senior Software Engineer", "company": "LumaWorks", "location": "Seattle", "skills": ["python", "java", "microservices", "design"]},
        {"id": "demo-13", "title": "AI Engineer", "company": "Signal Harbor", "location": "Remote", "skills": ["python", "machine learning", "llm", "prompt engineering"]},
        {"id": "demo-14", "title": "Site Reliability Engineer", "company": "Cloud Thread", "location": "Denver", "skills": ["linux", "kubernetes", "aws", "monitoring"]},
        {"id": "demo-15", "title": "Automation Engineer", "company": "Fjord Systems", "location": "Remote", "skills": ["python", "automation", "bash", "ci cd"]},
        {"id": "demo-16", "title": "Product Engineer", "company": "Verve Labs", "location": "Remote", "skills": ["javascript", "typescript", "react", "product development"]},
        {"id": "demo-17", "title": "Data Scientist", "company": "BrightPath AI", "location": "Remote", "skills": ["python", "statistics", "machine learning", "sql"]},
        {"id": "demo-18", "title": "Infrastructure Engineer", "company": "PeakForge", "location": "Los Angeles", "skills": ["aws", "terraform", "docker", "linux"]},
        {"id": "demo-19", "title": "Frontend Developer", "company": "Aster Labs", "location": "New York", "skills": ["javascript", "react", "css", "ui design"]},
        {"id": "demo-20", "title": "Software Engineer", "company": "Northwind", "location": "Remote", "skills": ["python", "java", "microservices", "database"]},
    ]


def _load_jobs() -> list[dict[str, Any]]:
    JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if JOBS_PATH.exists():
        try:
            payload = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
            jobs = payload.get("jobs", payload) if isinstance(payload, dict) else payload
            if isinstance(jobs, list) and jobs:
                return jobs
        except (json.JSONDecodeError, OSError):
            pass

    default_jobs = _default_jobs()
    JOBS_PATH.write_text(json.dumps({"jobs": default_jobs}, indent=2), encoding="utf-8")
    return default_jobs


def search_jobs(query: str, location: str = "") -> list[dict[str, Any]]:
    jobs = _load_jobs()
    terms = [term.lower() for term in query.split() if term]
    location_filter = (location or "").strip().lower()

    filtered_jobs = jobs
    if location_filter:
        filtered_jobs = [
            job for job in filtered_jobs
            if location_filter in (job.get("location", "") or "").lower()
        ]

    if terms:
        filtered_jobs = [
            job for job in filtered_jobs
            if any(term in (job.get("title", "") or "").lower() for term in terms)
            or any(term in " ".join(job.get("skills", [])).lower() for term in terms)
        ]

    return filtered_jobs


def refresh_jobs() -> list[dict[str, Any]]:
    return _load_jobs()
