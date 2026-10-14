import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import safestride


class SafeStrideTests(unittest.TestCase):
    def test_valid_coordinates(self):
        self.assertEqual(safestride.validate_coordinates(12.5, 80.2), (12.5, 80.2))

    def test_rejects_invalid_latitude(self):
        with self.assertRaises(ValueError):
            safestride.validate_coordinates(91, 80)

    def test_rejects_invalid_longitude(self):
        with self.assertRaises(ValueError):
            safestride.validate_coordinates(12, 181)

    def test_rejects_non_numeric_coordinates(self):
        with self.assertRaises(ValueError):
            safestride.validate_coordinates("north", "east")

    def test_alert_has_expected_fields(self):
        alert = safestride.create_sos_alert(12.5, 80.2, "Test Contact")
        self.assertEqual(alert["event_type"], "SOS")
        self.assertEqual(alert["status"], "SIMULATED")
        self.assertEqual(alert["contact_label"], "Test Contact")
        self.assertEqual(alert["indicators"]["buzzer"], "SIMULATED_ON")

    def test_save_alert_creates_json_file(self):
        alert = safestride.create_sos_alert(12.5, 80.2)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "alerts.json"
            saved = safestride.save_alert(alert, target)
            self.assertTrue(saved.exists())
            self.assertIn('"event_type": "SOS"', saved.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
