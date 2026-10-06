import base64
import json
import os
from email import message_from_bytes
from pathlib import Path
from typing import Any

from .email_agent import classify_email
from .notification_agent import build_notification

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
ROOT = Path(__file__).resolve().parent.parent
TOKEN_PATH = ROOT / "database" / "gmail-token.json"
_pending_state: str | None = None


def _credential_path() -> Path:
    configured = os.getenv("GMAIL_CREDENTIALS_FILE")
    if configured:
        path = Path(configured)
        if path.exists():
            return path
        raise FileNotFoundError(f"Gmail OAuth credentials were not found at {path}")

    fallback = ROOT / "credentials.json"
    if fallback.exists():
        return fallback
    raise FileNotFoundError("Gmail OAuth credentials were not found. Place credentials.json in the project root or set GMAIL_CREDENTIALS_FILE.")


def _client_config() -> dict[str, Any]:
    return json.loads(_credential_path().read_text(encoding="utf-8"))


def get_authorization_url() -> str:
    global _pending_state
    from google_auth_oauthlib.flow import Flow

    flow = Flow.from_client_config(_client_config(), scopes=SCOPES)
    flow.redirect_uri = os.getenv("GMAIL_REDIRECT_URI", "http://127.0.0.1:8000/gmail/callback")
    authorization_url, _pending_state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return authorization_url


def complete_authorization(code: str, state: str | None) -> None:
    global _pending_state
    if not state or state != _pending_state:
        raise ValueError("Invalid Gmail OAuth state. Please try the Connect Gmail flow again.")
    from google_auth_oauthlib.flow import Flow

    flow = Flow.from_client_config(_client_config(), scopes=SCOPES, state=state)
    flow.redirect_uri = os.getenv("GMAIL_REDIRECT_URI", "http://127.0.0.1:8000/gmail/callback")
    flow.fetch_token(code=code)
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(flow.credentials.to_json(), encoding="utf-8")
    _pending_state = None


def _gmail_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not TOKEN_PATH.exists():
        raise PermissionError("Gmail is not connected. Please log in with Connect Gmail first.")

    credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if credentials.expired and credentials.refresh_token:
        from google.auth.transport.requests import Request

        credentials.refresh(Request())
        TOKEN_PATH.write_text(credentials.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=credentials, cache_discovery=False)


def _message_text(payload: dict[str, Any]) -> str:
    data = payload.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    for part in payload.get("parts", []):
        text = _message_text(part)
        if text:
            return text
    return ""


def fetch_updates(limit: int = 10) -> list[dict[str, Any]]:
    service = _gmail_service()
    response = service.users().messages().list(userId="me", q="newer_than:30d (interview OR assessment OR offer OR application)", maxResults=limit).execute()
    updates = []
    for item in response.get("messages", []):
        message = service.users().messages().get(userId="me", id=item["id"], format="full").execute()
        headers = {header["name"].lower(): header["value"] for header in message.get("payload", {}).get("headers", [])}
        subject = headers.get("subject", "")
        body = _message_text(message.get("payload", {}))
        classification = classify_email(subject, body)
        updates.append({
            "id": item["id"],
            "from": headers.get("from", ""),
            "subject": subject,
            "date": headers.get("date", ""),
            "classification": classification,
            "notification": build_notification(classification),
        })
    return updates
