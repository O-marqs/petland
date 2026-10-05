"""Shared public-source/archive guards; report paths, never secret values."""

import hashlib
import re
import subprocess
from pathlib import Path, PurePosixPath

PRIVATE_PARTS = {
    ".git",
    ".local",
    ".tools",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "dist",
    "coverage",
    "htmlcov",
    "playwright-report",
    "test-results",
}
PRIVATE_SUFFIXES = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".dump",
    ".backup",
    ".bak",
    ".pgdump",
    ".plbackup",
    ".log",
    ".tsbuildinfo",
    ".pyc",
    ".pyo",
}
SECRET_PATTERNS = [
    re.compile(rb"-----BEGIN (?:RSA |DSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{80,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
]
# Concrete Windows user homes, including JSON-escaped separators. Templates and
# shared system homes are allowed; API URLs containing /users/ are unrelated.
LOCAL_USER_PATH = re.compile(
    rb"(?i)[a-z]:[\\/]+(?:Users|Documents and Settings)[\\/]+"
    rb"(?![<%{]|Public[\\/]|Default[\\/]|All Users[\\/])"
    rb"[^\\/\r\n\t\x00\"'`<>%{}]+[\\/]+"
)
SQL_DUMP_HEADER = re.compile(rb"(?m)^-- (?:PostgreSQL database dump|MySQL dump)\b")
# Fingerprints only: block reintroduction of the three exposed legacy literals
# without publishing their values in this guard or its diagnostics.
LEGACY_CREDENTIAL_SHA256 = frozenset(
    {
        "aa3eab8414727da7bd74fb57f76ee5e1b1cb3ff3b09efc24c1ff1e82a2b95074",
        "5061453026f4d55be44fca373d896f79c0feb1deac14425e3a6751e50f1b8c9c",
        "4441b9946f595223b09e9a4e87b31347bfd5fb0f4bad2e790947b33e2f5a974e",
    }
)
# These values are word tokens; exact fingerprints also catch bare env values
# and credentials in URLs without applying entropy heuristics to normal text.
CREDENTIAL_TOKEN = re.compile(rb"\b([A-Za-z0-9_]{8,128})\b")


def check_public_path(name: str) -> None:
    path = PurePosixPath(name)
    parts = tuple(part.casefold() for part in path.parts)
    if (
        not name
        or "\\" in name
        or ":" in name
        or any(ord(char) < 32 for char in name)
        or path.is_absolute()
        or ".." in parts
        or PRIVATE_PARTS.intersection(parts)
        or any(part.startswith(".local-") for part in parts)
        or any(part.startswith(".env") and part != ".env.example" for part in parts)
        or path.suffix.casefold() in PRIVATE_SUFFIXES
        or path.name.casefold()
        in {
            ".coverage",
            "thumbs.db",
            ".ds_store",
            "id_rsa",
            "id_ed25519",
            ".pgpass",
            ".netrc",
        }
        or name.casefold().endswith((".sql.gz", ".sql.zip", ".sql.bz2", ".sql.xz", ".sql.zst"))
    ):
        raise ValueError(f"Private or unsafe public path: {name}")


def check_public_file(name: str, content: bytes) -> None:
    check_public_path(name)
    if any(pattern.search(content) for pattern in SECRET_PATTERNS):
        raise ValueError(f"Possible secret in {name} (value withheld)")
    if any(
        hashlib.sha256(match[1]).hexdigest() in LEGACY_CREDENTIAL_SHA256
        for match in CREDENTIAL_TOKEN.finditer(content)
    ):
        raise ValueError(f"Known exposed legacy credential in {name} (value withheld)")
    if content.startswith((b"SQLite format 3\0", b"PGDMP")) or SQL_DUMP_HEADER.search(content):
        raise ValueError(f"Database or dump in {name} (content withheld)")


def check_current_file(name: str, content: bytes) -> None:
    """Current-source privacy policy; historical releases retain harmless paths."""
    check_public_file(name, content)
    if LOCAL_USER_PATH.search(content):
        raise ValueError(f"Personal local path in {name} (value withheld)")


def check_current_repository(root: Path) -> int:
    """Inspect tracked and unignored new files, never print sensitive contents."""
    names = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root,
        )
        .decode()
        .split("\0")
    )
    errors = []
    checked = 0
    for name in sorted(set(filter(None, names))):
        path = root / name
        if not path.is_file():
            continue
        checked += 1
        try:
            check_current_file(name, path.read_bytes())
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        raise ValueError("\n".join(errors))
    return checked


def main() -> None:
    try:
        count = check_current_repository(Path(__file__).resolve().parents[1])
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
    print(f"Active source scan passed: {count} files. This is not a historical credential audit.")


if __name__ == "__main__":
    main()
