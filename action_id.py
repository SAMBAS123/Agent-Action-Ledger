"""Generate stable, deterministic action IDs."""

import hashlib
import json
import re
from typing import Any, Dict


def _clean(s: str) -> str:
    """Make a string safe and readable for action IDs."""
    s = re.sub(r"[^a-zA-Z0-9_-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-").lower()
    return s[:20]


def _stable_fingerprint(data: Dict[str, Any]) -> str:
    """Create a deterministic fingerprint from core identity fields only."""
    key_fields = ["action_type", "subject_key", "owner", "due_date"]
    stable = {k: data.get(k, "") for k in key_fields}
    serialized = json.dumps(stable, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()[:16]


def generate_action_id(action: Dict[str, Any]) -> str:
    """Generate a clean, human-readable + stable action ID."""
    action_type = _clean(action.get("action_type", "act"))
    subject = _clean(action.get("subject_key", "unknown"))
    owner = _clean(action.get("owner", "unk"))

    fingerprint = _stable_fingerprint(action)

    return f"{action_type}-{subject}-{owner}-{fingerprint}"


def get_fingerprint(action: Dict[str, Any]) -> str:
    """Return only the fingerprint for suppression matching."""
    return _stable_fingerprint(action)