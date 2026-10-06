# AI Job Agent

A modular resume-to-job-application workflow.

## Run

```powershell
cd ai-job-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn backend.app:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API.

The current implementation uses deterministic local parsing, demo job data, SQLite, and generated cover letters. External AI, job-board, Gmail, Outlook, and browser-automation adapters can be added behind the existing module boundaries. Applications are saved as `pending_approval`; automatic submission is intentionally not performed.

## Connect Gmail

1. In Google Cloud Console, create an OAuth client for a **Web application** and add `http://127.0.0.1:8000/gmail/callback` as an authorized redirect URI.
2. Download the client JSON as `credentials.json` into this project directory.
3. Restart the server and open the app at `http://127.0.0.1:8000/`.
4. Click **Connect Gmail** and approve the read-only Gmail permission.

The app searches the last 30 days for recruiting messages and classifies interview, assessment, offer, rejection, and application updates. It stores the OAuth token locally in `database/gmail-token.json`; do not commit that file.
