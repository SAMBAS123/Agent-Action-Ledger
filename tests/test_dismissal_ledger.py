import unittest
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dismissal_ledger import DismissalLedger


class TestDismissalLedger(unittest.TestCase):
    def test_dismiss_and_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "dismissals.jsonl")
            ledger = DismissalLedger(path)

            ledger.dismiss("act-123", "fingerprint-abc", "already_done")
            self.assertTrue(ledger.is_dismissed("act-123", "fingerprint-abc"))

    def test_audit_trail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "dismissals.jsonl")
            ledger = DismissalLedger(path)

            d = ledger.dismiss("act-456", "fp-xyz", "bad_suggestion", dismissed_by="demo")
            self.assertEqual(d["reason"], "bad_suggestion")
            self.assertIn("dismissed_at", d)