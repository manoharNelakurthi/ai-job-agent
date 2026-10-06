from typing import Any


def score_job_match(resume: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    resume_skills = {skill.lower() for skill in resume.get("skills", [])}
    required_skills = {skill.lower() for skill in job.get("skills", [])}
    matched = sorted(resume_skills & required_skills)
    missing = sorted(required_skills - resume_skills)
    score = round((len(matched) / len(required_skills)) * 100) if required_skills else 0
    return {**job, "match_score": score, "matched_skills": matched, "missing_skills": missing}


def rank_jobs(resume: dict[str, Any], jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted((score_job_match(resume, job) for job in jobs), key=lambda job: job["match_score"], reverse=True)
