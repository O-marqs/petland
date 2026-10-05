"""Scan the current public snapshot; never print matching values or scan history."""

import hashlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

RETIRED = {
    "aa3eab8414727da7bd74fb57f76ee5e1b1cb3ff3b09efc24c1ff1e82a2b95074": "LEGACY_SESSION_SECRET",
    "5061453026f4d55be44fca373d896f79c0feb1deac14425e3a6751e50f1b8c9c": "LEGACY_JWT_SECRET",
    "4441b9946f595223b09e9a4e87b31347bfd5fb0f4bad2e790947b33e2f5a974e": "LEGACY_MYSQL_PASSWORD",
}
GENERATED = {".venv", "venv", "env", "__pycache__", "node_modules", "dist", "build", "coverage", "htmlcov", ".pytest_cache", ".idea", ".vscode", ".audit"}
PRIVATE_SUFFIXES = {".pyc", ".pyo", ".db", ".sqlite", ".sqlite3", ".dump", ".backup", ".bak", ".log", ".key", ".pem", ".p12", ".pfx"}
SECRET_PATTERNS = [
    re.compile(rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{80,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
]
LOCAL_PATH = re.compile(rb"(?i)[a-z]:[\\/]+Users[\\/]+(?![<%{]|Public[\\/]|Default[\\/])[^\\/\r\n\t\x00\"'`<>%{}]+[\\/]+")
PERSONAL_EMAIL = re.compile(rb"[\w.+-]+@(?:gmail|hotmail|outlook)\.com", re.I)


def findings(name, content):
    path = PurePosixPath(name)
    labels = set()
    if GENERATED.intersection(path.parts) or path.suffix.lower() in PRIVATE_SUFFIXES or path.name in {".coverage", ".DS_Store", "Thumbs.db"} or (path.name.startswith(".env") and path.name != ".env.example"):
        labels.add("PRIVATE_OR_GENERATED_ARTIFACT")
    for token in re.finditer(rb"\b([A-Za-z0-9_]{8,128})\b", content):
        label = RETIRED.get(hashlib.sha256(token[1]).hexdigest())
        if label:
            labels.add(label)
    if any(pattern.search(content) for pattern in SECRET_PATTERNS):
        labels.add("POSSIBLE_SECRET")
    if LOCAL_PATH.search(content):
        labels.add("PERSONAL_LOCAL_PATH")
    if path.parts and path.parts[0].lower() == "tests" and PERSONAL_EMAIL.search(content):
        labels.add("AMBIGUOUS_FIXTURE_EMAIL")
    if re.search(rb"(?m)^-- (?:PostgreSQL database dump|MySQL dump)\b", content):
        labels.add("DATABASE_DUMP")
    return sorted(labels)


def main():
    root = Path(__file__).resolve().parents[1]
    # Index excludes staged deletions. Include nonignored additions during review.
    names = subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root).decode().split("\0")
    failures = []
    checked = 0
    for name in sorted(set(names) - {""}):
        path = root / name
        if not path.is_file():
            continue
        checked += 1
        for label in findings(name, path.read_bytes()):
            failures.append((name, label))
    for name, label in failures:
        print(f"BLOCKED: {name}: {label} (value withheld)")
    print(f"Checked {checked} current files; {len(failures)} findings. History intentionally excluded.")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
