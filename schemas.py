"""Lightweight schema helpers using only stdlib."""

from datetime import datetime
from typing import Any, Dict, List, Optional


def is_valid_action(action: Dict[str, Any]) -> bool:
    """Basic validation for an action dict."""
    required = ["action_type", "subject_key", "owner"]
    return all(k in action and action[k] for k in required)


def normalize_action(action: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize messy agent output into a clean action record."""
    return {
        "action_type": str(action.get("action_type", "unknown")).strip().lower(),
        "subject_key": str(action.get("subject_key", action.get("name", ""))).strip(),
        "owner": str(action.get("owner", "unknown")).strip(),
        "due_date": action.get("due_date") or action.get("due", ""),
        "reason": str(action.get("reason", action.get("notes", ""))).strip(),
        "confidence": float(action.get("confidence", 0.5)),
        "status": str(action.get("status", "open")).strip().lower(),
        "source_refs": action.get("source_refs", []),
        "created_at": action.get("created_at", datetime.utcnow().isoformat()),
    }