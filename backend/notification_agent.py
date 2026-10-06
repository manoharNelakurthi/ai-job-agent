from typing import Any


def build_notification(email_result: dict[str, Any]) -> dict[str, Any]:
    category = email_result.get("category", "other")
    messages = {
        "interview": "Interview activity needs your attention.",
        "assessment": "A hiring assessment is waiting for review.",
        "offer": "You may have received an offer. Review the email carefully.",
        "rejection": "An application status changed.",
        "application_update": "An application received an update.",
    }
    return {"title": category.replace("_", " ").title(), "message": messages.get(category, "A recruiting email was received."), "requires_action": email_result.get("requires_action", False)}
