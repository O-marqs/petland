"""Scanner behavior, using synthetic values generated only in memory."""

import importlib.util
import hashlib
from pathlib import Path
import secrets
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("snapshot_guard", Path(__file__).resolve().parents[1] / "scripts/check_legacy_snapshot.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class SnapshotHygieneTests(unittest.TestCase):
    def test_example_configuration_is_allowed(self):
        self.assertEqual(guard.findings(".env.example", b"MYSQL_PASSWORD=change-me\nMYSQL_HOST=localhost\n"), [])

    def test_retired_literal_detected_by_hash_without_disclosing_it(self):
        value = secrets.token_hex(24).encode()
        with patch.dict(guard.RETIRED, {hashlib.sha256(value).hexdigest(): "RETIRED_TEST_CREDENTIAL"}):
            labels = guard.findings("config.py", b"CONFIG=" + value)
            self.assertEqual(labels, ["RETIRED_TEST_CREDENTIAL"])

    def test_private_key_and_access_token_detected(self):
        for content in [b"-----BEGIN " + b"PRIVATE KEY-----", b"ghp_" + b"A" * 36]:
            self.assertEqual(guard.findings("config.txt", content), ["POSSIBLE_SECRET"])

    def test_generated_and_private_artifacts_blocked(self):
        for path in [".venv/Lib/a.py", "models/__pycache__/a.pyc", ".env", "db.sqlite", "backup.dump", "server.key"]:
            self.assertIn("PRIVATE_OR_GENERATED_ARTIFACT", guard.findings(path, b""))

    def test_personal_paths_and_ambiguous_fixture_mail_blocked(self):
        personal_path = b"C:" + b"\\Users\\demo\\repo\\app.py"
        self.assertEqual(guard.findings("notes.md", personal_path), ["PERSONAL_LOCAL_PATH"])
        personal_mail = b"demo@" + b"gmail.com"
        self.assertEqual(guard.findings("Tests/example.side", personal_mail), ["AMBIGUOUS_FIXTURE_EMAIL"])
        self.assertEqual(guard.findings("Tests/example.side", b"demo-cliente@example.com"), [])


if __name__ == "__main__":
    unittest.main()
