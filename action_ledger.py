"""Action Ledger - writes and reads structured actions with stable IDs."""

import json
from pathlib import Path
from typing import Any, Dict, List

from action_id import generate_action_id, get_fingerprint
from schemas import normalize_action


class ActionLedger:
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

    def add_action(self, messy_action: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize, generate ID, and append to ledger."""
        normalized = normalize_action(messy_action)
        action_id = generate_action_id(normalized)
        fingerprint = get_fingerprint(normalized)

        row = {
            "action_id": action_id,
            "fingerprint": fingerprint,
            **normalized,
        }

        existing = self._load()
        # Avoid exact duplicates
        if not any(r["action_id"] == action_id for r in existing):
            existing.append(row)
            self._save(existing)
        return row

    def get_all(self) -> List[Dict[str, Any]]:
        return self._load()

    def find_by_id(self, action_id: str) -> Dict[str, Any] | None:
        for row in self._load():
            if row["action_id"] == action_id:
                return row
        return None