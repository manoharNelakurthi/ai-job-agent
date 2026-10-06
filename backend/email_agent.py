import re
from typing import Any


def classify_email(subject: str, body: str) -> dict[str, Any]:
    text = f"{subject} {body}".lower()
    categories = {
        "interview": ["interview", "schedule a call", "next round"],
        "assessment": ["assessment", "coding challenge", "take-home"],
        "rejection": ["unfortunately", "not moving forward", "rejected"],
        "offer": ["offer", "compensation package", "welcome to the team"],
        "application_update": ["application", "status update", "received your application"],
    }
    for category, keywords in categories.items():
        if any(re.search(rf"\b{re.escape(keyword)}\b", text) for keyword in keywords):
            return {"category": category, "requires_action": category in {"interview", "assessment", "offer"}}
    return {"category": "other", "requires_action": False}
