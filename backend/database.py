from pathlib import Path
import sqlite3
from typing import Any

DATABASE_PATH = Path(__file__).resolve().parent.parent / "database" / "jobs.sqlite3"


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                status TEXT NOT NULL,
                cover_letter TEXT,
                form_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def create_application(application: dict[str, Any]) -> int:
    import json

    initialize_database()
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            "INSERT INTO applications (job_title, company, status, cover_letter, form_data) VALUES (?, ?, ?, ?, ?)",
            (
                application["job_title"],
                application["company"],
                application.get("status", "pending_approval"),
                application.get("cover_letter", ""),
                json.dumps(application.get("form_data", {})),
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def list_applications() -> list[dict[str, Any]]:
    initialize_database()
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute("SELECT * FROM applications ORDER BY created_at DESC")]
