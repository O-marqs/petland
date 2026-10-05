"""Exercise real archive rejection boundaries without application/database state."""

import hashlib
import json
import subprocess
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from release import validate, validate_policy, verify
from repository_hygiene import (
    check_current_file,
    check_current_repository,
    check_public_file,
    check_public_path,
)


class PublicArchiveTests(unittest.TestCase):
    def archive(self, folder, entries, *, manifest_commit="a" * 40, zip_commit="a" * 40):
        archive = folder / "candidate.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(archive, "w") as file:
                file.comment = zip_commit.encode()
                for name, data in entries:
                    file.writestr(name, data)
        manifest = {
            "archive": archive.name,
            "commit": manifest_commit,
            "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "files": {name: hashlib.sha256(data).hexdigest() for name, data in entries},
        }
        (folder / "manifest.json").write_text(json.dumps(manifest))
        return archive

    def test_private_paths_and_cross_platform_traversal_are_refused(self):
        for name in [
            "../dump.txt",
            "C:/dump.txt",
            r"folder\dump.txt",
            ".ENV",
            ".local/fixture.json",
            "public/private.key",
            "database.sqlite3",
            "backup.sql.gz",
            "apps/web/dist/index.html",
            ".local-audit.json",
            "test-results/trace.zip",
            "certificates/server.pem",
        ]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                check_public_path(name)

    def test_public_configuration_and_source_are_allowed(self):
        check_public_file(".env.example", b"POSTGRES_PASSWORD=GENERATE_MIGRATOR_PASSWORD")
        check_public_file("apps/api/migrations/versions/0007_product_operations.py", b"# DDL")
        check_public_file("docs/architecture/diagrams/containers.svg", b"<svg/>")

    def test_secret_detection_does_not_disclose_the_value(self):
        secret = b"ghp_" + b"A" * 40
        with self.assertRaises(ValueError) as error:
            check_public_file("innocent.txt", secret)
        self.assertIn("innocent.txt", str(error.exception))
        self.assertNotIn(secret.decode(), str(error.exception))

    def test_zip_commit_must_match_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.archive(folder, [("README.md", b"public")], zip_commit="b" * 40)
            with self.assertRaisesRegex(ValueError, "Archive commit disagrees"):
                verify(folder)

    def test_manifest_archive_path_is_checked_before_reading(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "manifest.json").write_text(json.dumps({"archive": r"..\private.zip"}))
            with self.assertRaises(ValueError):
                verify(folder)

    def test_duplicate_zip_entries_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.archive(folder, [("README.md", b"first"), ("README.md", b"last")])
            with self.assertRaisesRegex(ValueError, "Duplicate candidate"):
                verify(folder)

    def test_secret_in_zip_is_refused_even_with_matching_checksums(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            secret = b"-----BEGIN " + b"PRIVATE KEY-----\nsynthetic rejected payload"
            self.archive(folder, [("innocent.txt", secret)])
            with self.assertRaisesRegex(ValueError, "Possible secret in innocent.txt"):
                verify(folder)

    def test_changed_zip_cannot_pass_the_original_checksum(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            archive = self.archive(folder, [("README.md", b"public")])
            with archive.open("ab") as file:
                file.write(b"tampered")
            with self.assertRaisesRegex(ValueError, "Candidate archive checksum mismatch"):
                verify(folder)


class CurrentPrivacyTests(unittest.TestCase):
    def local_path(self):
        # Construct the fixture so the test source remains publishable.
        return b"C:" + b"\\Users\\PrivatePerson\\Documents\\petland"

    def test_concrete_user_homes_are_refused_with_redacted_errors(self):
        path = self.local_path()
        for data in [
            path,
            path.replace(b"\\", b"/"),
            path.replace(b"\\", b"\\\\"),
            path.replace(b"PrivatePerson", b"Private Person"),
        ]:
            with self.subTest(data=data), self.assertRaises(ValueError) as error:
                check_current_file("docs/setup.md", data)
            self.assertNotIn("PrivatePerson", str(error.exception))
            self.assertIn("docs/setup.md", str(error.exception))

    def test_neutral_templates_system_homes_and_api_urls_are_allowed(self):
        for data in [
            b"%USERPROFILE%\\Documents\\GitHub",
            b"<workspace>/petland",
            b"C:" + b"\\Users\\<user>\\Documents",
            b"C:" + b"\\Users\\Public\\Documents",
            b"https://localhost/api/v1/management/users/",
            b"demo-admin@example.com; Endereco ficticio de demonstracao",
        ]:
            with self.subTest(data=data):
                check_current_file("docs/setup.md", data)

    def test_historical_archive_can_retain_a_path_but_current_cannot(self):
        check_public_file("docs/evidence.md", self.local_path())
        with self.assertRaises(ValueError):
            check_current_file("docs/evidence.md", self.local_path())

    def test_encrypted_private_keys_and_fine_grained_tokens_always_refused(self):
        secrets = [
            b"-----BEGIN " + b"ENCRYPTED PRIVATE KEY-----",
            b"github_pat_" + b"A" * 82,
        ]
        for guard in [check_public_file, check_current_file]:
            for secret in secrets:
                with (
                    self.subTest(guard=guard.__name__),
                    self.assertRaises(ValueError) as error,
                ):
                    guard("innocent.txt", secret)
                self.assertNotIn(secret.decode(), str(error.exception))

    def test_disguised_databases_and_dumps_are_refused_but_ddl_is_allowed(self):
        for content in [
            b"SQLite format 3\0" + b"payload",
            b"PGDMP" + b"payload",
            b"-- PostgreSQL " + b"database dump\nCREATE TABLE pets();",
            b"-- MySQL " + b"dump 10.13\nINSERT INTO pets VALUES (1);",
        ]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                check_public_file("data.txt", content)
        check_current_file("migration.sql", b"CREATE TABLE pets (id UUID PRIMARY KEY);")

    def test_private_backup_and_credential_filenames_are_refused(self):
        for name in [
            "data.bak",
            "data.pgdump",
            "backup.sql.xz",
            "id_rsa",
            ".pgpass",
            ".netrc",
        ]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                check_public_path(name)

    def test_known_exposed_literals_are_blocked_by_fingerprint_without_disclosure(self):
        synthetic = b"synthetic_fingerprint_test"
        fingerprints = {hashlib.sha256(synthetic).hexdigest()}
        with patch("repository_hygiene.LEGACY_CREDENTIAL_SHA256", fingerprints):
            for guard in [check_public_file, check_current_file]:
                for data in [
                    b"secret = '" + synthetic + b"'",
                    b"PASSWORD=" + synthetic,
                    b"postgresql://demo:" + synthetic + b"@localhost/demo",
                ]:
                    with (
                        self.subTest(guard=guard.__name__),
                        self.assertRaises(ValueError) as error,
                    ):
                        guard("config.py", data)
                    self.assertNotIn(synthetic.decode(), str(error.exception))

    def test_repository_scans_new_and_forced_tracked_files_but_ignores_runtime(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".env\n")
            (root / ".env").write_bytes(b"ghp_" + b"A" * 40)
            (root / "README.md").write_bytes(b"public")
            self.assertEqual(check_current_repository(root), 2)
            (root / "new.md").write_bytes(self.local_path())
            with self.assertRaisesRegex(ValueError, "Personal local path in new.md"):
                check_current_repository(root)
            (root / "new.md").unlink()
            subprocess.run(["git", "add", "-f", ".env"], cwd=root, check=True)
            with self.assertRaisesRegex(ValueError, "Private or unsafe public path: .env"):
                check_current_repository(root)


class PortfolioPolicyTests(unittest.TestCase):
    def metadata(self):
        return json.loads(
            (Path(__file__).resolve().parents[1] / "docs/release/candidate.json").read_text()
        )

    def test_stable_portfolio_delegates_publication_to_github(self):
        candidate = self.metadata()
        validate_policy(candidate)
        self.assertIsNone(candidate["stable_release_published"])

    def test_cannot_claim_publication_before_external_receipt(self):
        candidate = self.metadata()
        candidate["stable_release_published"] = True
        with self.assertRaisesRegex(ValueError, "external GitHub receipt"):
            validate_policy(candidate)

    def test_cannot_grant_commercial_production(self):
        candidate = self.metadata()
        candidate["production_ready"] = True
        with self.assertRaisesRegex(ValueError, "production readiness"):
            validate_policy(candidate)

    def test_historical_rc_policy_still_supported(self):
        candidate = self.metadata()
        candidate.update(
            version="3.0.0-rc.1",
            python_version="3.0.0rc1",
            status="candidate_for_review",
            stable_release_published=False,
        )
        validate_policy(candidate)

    def test_historical_media_cannot_be_redated_as_stable(self):
        root = Path(__file__).resolve().parents[1]

        def read(name):
            data = (root / name).read_bytes()
            if name == "docs/case/media/capture.json":
                capture = json.loads(data)
                capture["version"] = "3.0.0"
                return json.dumps(capture).encode()
            return data

        with self.assertRaisesRegex(ValueError, "recording evidence"):
            validate(read)


if __name__ == "__main__":
    unittest.main()
