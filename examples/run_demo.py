#!/usr/bin/env python3
"""Demo of the Agent Action Ledger Kit."""

import json
import tempfile
import sys
from pathlib import Path

# Allow running directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from action_ledger import ActionLedger
from dismissal_ledger import DismissalLedger


def main():
    base = Path(__file__).parent
    messy_path = base / "messy_agent_output.json"

    with tempfile.TemporaryDirectory() as tmp:
        action_ledger_path = Path(tmp) / "action_ledger.jsonl"
        dismissal_ledger_path = Path(tmp) / "dismissal_ledger.jsonl"

        action_ledger = ActionLedger(str(action_ledger_path))
        dismissal_ledger = DismissalLedger(str(dismissal_ledger_path))

        messy_actions = json.loads(messy_path.read_text())

        print("=== BEFORE: Raw messy agent output ===")
        for a in messy_actions:
            print(f"  - {a.get('name')} | {a.get('notes')}")

        print("\n=== Processing actions ===")
        for messy in messy_actions:
            row = action_ledger.add_action(messy)
            print(f"  Normalized → {row['action_id']}")

        first = action_ledger.get_all()[0]
        dismissal_ledger.dismiss(
            action_id=first["action_id"],
            fingerprint=first["fingerprint"],
            reason="already_contacted",
            dismissed_by="demo",
        )
        print(f"\n=== Dismissed: {first['action_id']} ===")

        print("\n=== AFTER: Re-processing same input ===")
        for messy in messy_actions:
            row = action_ledger.add_action(messy)
            if dismissal_ledger.is_dismissed(row["action_id"], row["fingerprint"]):
                print(f"  SUPPRESSED: {row['action_id']}")
            else:
                print(f"  Would act on: {row['action_id']}")

        print("\n=== Summary ===")
        print(f"Total actions in ledger: {len(action_ledger.get_all())}")
        print(f"Total dismissals: {len(dismissal_ledger.get_dismissals())}")


if __name__ == "__main__":
    main()