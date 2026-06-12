"""Dismissal Ledger - allows suppression of actions without deleting history."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class DismissalLedger:
    def __init__(self, ledger_path: str):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> List[Dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        lines = self.ledger_path.read_text().strip().splitlines()
        return [json.loads(line) for line in lines if line.strip()]

    def _save(self, rows: List[Dict[str, Any]]):
        with self.ledger_path.open("w") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")

    def dismiss(
        self,
        action_id: str,
        fingerprint: str,
        reason: str,
        dismissed_by: str = "operator",
        expires_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record a dismissal for an action."""
        dismissal = {
            "action_id": action_id,
            "fingerprint": fingerprint,
            "reason": reason,
            "dismissed_by": dismissed_by,
            "dismissed_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at,
        }
        existing = self._load()
        existing.append(dismissal)
        self._save(existing)
        return dismissal

    def is_dismissed(self, action_id: str, fingerprint: str) -> bool:
        """Check if an action should be suppressed."""
        for d in self._load():
            if d["action_id"] == action_id or d["fingerprint"] == fingerprint:
                if not d.get("expires_at"):
                    return True
                # TODO: add expiration logic if needed
                return True
        return False

    def get_dismissals(self) -> List[Dict[str, Any]]:
        return self._load()