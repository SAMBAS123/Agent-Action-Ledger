import unittest
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from action_ledger import ActionLedger


class TestActionLedger(unittest.TestCase):
    def test_add_and_retrieve(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "ledger.jsonl")
            ledger = ActionLedger(path)

            action = {"action_type": "collection", "subject_key": "Test", "owner": "Sam"}
            row = ledger.add_action(action)

            self.assertIn("action_id", row)
            self.assertEqual(len(ledger.get_all()), 1)

    def test_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "ledger.jsonl")
            ledger = ActionLedger(path)

            a1 = {"action_type": "collection", "subject_key": "Dup", "owner": "Sam"}
            a2 = {"action_type": "collection", "subject_key": "Dup", "owner": "Sam", "extra": "noise"}

            ledger.add_action(a1)
            ledger.add_action(a2)

            self.assertEqual(len(ledger.get_all()), 1)