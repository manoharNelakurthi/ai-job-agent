import shutil
import sys
from pathlib import Path
from typing import Any

if not __package__:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    __package__ = "backend"

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .application_agent import prepare_application, save_application
from .database import initialize_database, list_applications
from .email_agent import classify_email
from .job_matcher import rank_jobs
from .job_search import refresh_jobs, search_jobs
from .notification_agent import build_notification
from .resume_analyzer import analyze_resume
from .resume_parser import parse_resume

try:
    from .gmail_agent import complete_authorization, fetch_updates, get_authorization_url
except Exception:  # pragma: no cover - Gmail is optional for app startup
    complete_authorization = None
    fetch_updates = None
    get_authorization_url = None

ROOT = Path(__file__).resolve().parent.parent
UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(exist_ok=True)

app = FastAPI(title="AI Job Agent", version="0.1.0")


class JobSearchRequest(BaseModel):
    query: str = ""
    location: str = ""
    resume: dict[str, Any]


class ApplicationRequest(BaseModel):
    resume: dict[str, Any]
    job: dict[str, Any]


class EmailRequest(BaseModel):
    subject: str
    body: str


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, Any]:
    if Path(file.filename or "").suffix.lower() not in {".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Upload a PDF or DOCX resume")
    destination = UPLOADS / Path(file.filename or "resume").name
    with destination.open("wb") as output:
        shutil.copyfileobj(file.file, output)
    parsed = parse_resume(destination)
    return {"resume": parsed, "analysis": analyze_resume(parsed)}


@app.post("/jobs/search")
def jobs_search(request: JobSearchRequest) -> dict[str, Any]:
    jobs = search_jobs(request.query, request.location)
    return {"jobs": rank_jobs(request.resume, jobs)}


@app.get("/jobs/refresh")
def jobs_refresh() -> dict[str, Any]:
    return {"jobs": refresh_jobs()}


@app.post("/applications/prepare")
def application_prepare(request: ApplicationRequest) -> dict[str, Any]:
    return {"application": prepare_application(request.resume, request.job)}


@app.post("/applications")
def application_create(request: dict[str, Any]) -> dict[str, Any]:
    return {"id": save_application(request), "status": "pending_approval"}


@app.get("/applications")
def applications_list() -> dict[str, Any]:
    return {"applications": list_applications()}


@app.post("/email/classify")
def email_classify(request: EmailRequest) -> dict[str, Any]:
    result = classify_email(request.subject, request.body)
    return {"classification": result, "notification": build_notification(result)}


@app.get("/gmail/login")
def gmail_login() -> RedirectResponse:
    if get_authorization_url is None:
        raise HTTPException(status_code=503, detail="Gmail integration is disabled. Install/google-auth packages and configure credentials.")
    try:
        return RedirectResponse(get_authorization_url())
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.get("/gmail/callback")
def gmail_callback(code: str, state: str | None = None) -> RedirectResponse:
    if complete_authorization is None:
        raise HTTPException(status_code=503, detail="Gmail integration is disabled.")
    try:
        complete_authorization(code, state)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RedirectResponse("/")


@app.get("/gmail/updates")
def gmail_updates() -> dict[str, Any]:
    if fetch_updates is None:
        raise HTTPException(status_code=503, detail="Gmail integration is disabled.")
    try:
        return {"updates": fetch_updates()}
    except PermissionError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


frontend_dir = ROOT / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
