from typing import Any


# Provider adapters can be added here without changing matching or application logic.
def search_jobs(query: str, location: str = "") -> list[dict[str, Any]]:
    sample_jobs = [
        {"id": "demo-1", "title": "Python Backend Engineer", "company": "Northstar Labs", "location": "Remote", "skills": ["python", "fastapi", "sql"]},
        {"id": "demo-2", "title": "Full Stack Developer", "company": "Cedar Systems", "location": "New York", "skills": ["javascript", "react", "sql"]},
        {"id": "demo-3", "title": "Cloud Software Engineer", "company": "Blue Harbor", "location": "Remote", "skills": ["python", "docker", "azure"]},
    ]
    terms = query.lower().split()
    return [job for job in sample_jobs if not terms or any(term in job["title"].lower() for term in terms)]
