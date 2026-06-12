import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from action_id import generate_action_id, get_fingerprint


class TestActionID(unittest.TestCase):
    def test_stable_id(self):
        action1 = {"action_type": "collection", "subject_key": "Martinez", "owner": "Caitlin"}
        action2 = {"action_type": "collection", "subject_key": "Martinez", "owner": "Caitlin", "notes": "extra"}

        id1 = generate_action_id(action1)
        id2 = generate_action_id(action2)

        self.assertEqual(id1, id2)

    def test_fingerprint_changes_with_key_fields(self):
        a1 = {"action_type": "collection", "subject_key": "Martinez", "owner": "Caitlin"}
        a2 = {"action_type": "follow_up", "subject_key": "Martinez", "owner": "Caitlin"}

        self.assertNotEqual(get_fingerprint(a1), get_fingerprint(a2))