#!/usr/bin/env python3
"""Scan a public registry export for secrets, private paths, and unresolved placeholders.

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".py",
    ".ps1",
    ".cs",
    ".csproj",
    ".props",
    ".targets",
    ".xml",
    ".config",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
}

BINARY_SUFFIXES = {".gz", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".pfx", ".snk", ".pem", ".key"}

# Matches high-risk material. Safe owner/public repo names are allowed below.
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("github_token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}", re.I)),
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.I)),
    ("api_key_assignment", re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")),
    ("password_assignment", re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{4,}")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("connection_string", re.compile(r"(?i)(Server|Data Source)=[^;]+;.*(Password|Pwd)=")),
    ("smtp_password", re.compile(r"(?i)smtp.*(password|pwd)\s*[:=]")),
    ("windows_abs_path", re.compile(r"(?i)[A-Z]:\\(?:Users|VS Projects|Program Files)\\[^\s\"']+")),
    ("appdata_expanded", re.compile(r"(?i)C:\\Users\\[^\\]+\\AppData\\")),
    ("private_dev_repo_url", re.compile(r"github\.com/lgdeysel1980/BookAtrium-Development", re.I)),
    ("bookapplication_branding", re.compile(r"\bBookApplication\b")),
    ("bookapplication_lower", re.compile(r"\bbookapplication\b")),
    ("bookapplication_env_active", re.compile(r"\bbookapplication_repo_path\b", re.I)),
    ("bookapplication_example_host", re.compile(r"bookapplication\.example", re.I)),
    ("temp_audit_dir", re.compile(r"BookAtrium-Phase3X-Audit", re.I)),
    ("nuget_credentials", re.compile(r"(?i)nuget.*(password|apikey|cleartextpassword)")),
    ("user_secrets", re.compile(r"(?i)usersecretsid\s*[:=]")),
    ("pluginsdk_package", re.compile(r"BookAtrium\.PluginSdk")),
]

# Mojibake literals encoded as escapes so this file does not contain the bad sequences.
# Built from UTF-8 of typographic punctuation mis-decoded as Windows-1252 / latin-1.
_MOJIBAKE = {
    "mojibake_emdash": "\u00e2\u20ac\u201d",
    "mojibake_rsquo": "\u00e2\u20ac\u2122",
    "mojibake_arrow": "\u00e2\u2020\u2019",
    "mojibake_ldquo": "\u00e2\u20ac\u0153",
    "mojibake_rdquo_c1": "\u00e2\u20ac\u009d",
    "mojibake_rdquo_replace": "\u00e2\u20ac\ufffd",
    "mojibake_ellipsis": "\u00e2\u20ac\u00a6",
    "mojibake_A_tilde": "\u00c3",
    "mojibake_replacement": "\ufffd",
}

CONTENT_POLICY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("api_1_1_preferred", re.compile(r"(?i)API\s*\*?\*?1\.1\*?\*?\s+preferred")),
    ("prefer_1_1", re.compile(r"(?i)Prefer\s+1\.1\b")),
    ("prefer_backtick_1_1", re.compile(r"(?i)prefer\s+`1\.1`")),
    ("plugin_api_1_1_preferred", re.compile(r"(?i)Plugin\s+API\s+\*?\*?1\.1\*?\*?\s+preferred")),
    *[
        (label, re.compile(re.escape(sequence)))
        for label, sequence in _MOJIBAKE.items()
    ],
]

PLACEHOLDER_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("curly_owner", re.compile(r"\{owner\}")),
    ("curly_repository", re.compile(r"\{repository\}")),
    ("your_github_username", re.compile(r"YOUR_GITHUB_USERNAME")),
    ("example_developer", re.compile(r"\bExampleDeveloper\b")),
    ("example_com", re.compile(r"(?<![/\w])example\.com(?![/\w])", re.I)),
    ("replace_me", re.compile(r"\bREPLACE_ME\b")),
    ("todo_security", re.compile(r"TODO_SECURITY_CONTACT")),
    ("todo_license", re.compile(r"TODO_LICENSE")),
]

# Paths under which ExampleDeveloper / example.com placeholders are allowed.
EXAMPLE_DIRS = {"examples", "templates"}

SAFE_ALLOWLIST_SNIPPETS = (
    "lgdeysel1980",
    "lgdeysel1980/BookAtrium",
    "lgdeysel1980/BookAtrium-Community-Plugins",
    "BOOKAPPLICATION_COMMUNITY_PLUGIN_REGISTRY_URL",  # explicit legacy env docs only; still flagged unless allowed file
)

FORBIDDEN_FILENAMES = {
    ".env",
    "appsettings.Development.json",
    "secrets.json",
}

FORBIDDEN_SUFFIXES = {".pfx", ".snk", ".pem", ".key"}


def is_example_path(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = {p.lower() for p in rel.parts[:-1]}
    return bool(parts & EXAMPLE_DIRS)


def should_scan_text(path: Path) -> bool:
    if path.name.startswith(".") and path.suffix == "":
        return path.name in {".gitignore", ".gitattributes", ".editorconfig"}
    if path.suffix.lower() in BINARY_SUFFIXES:
        return False
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
        "LICENSE",
        "LICENCE",
        "Dockerfile",
        "Makefile",
    }:
        return True
    # untitled / extensionless markdown-ish
    return path.suffix == "" and path.stat().st_size < 512_000


def scan_file(path: Path, root: Path, allow_legacy_env_docs: bool) -> list[str]:
    findings: list[str] = []
    name_lower = path.name.lower()
    if name_lower in {n.lower() for n in FORBIDDEN_FILENAMES} or path.suffix.lower() in FORBIDDEN_SUFFIXES:
        findings.append(f"{path.relative_to(root)}: forbidden secret/credential file type")
        return findings

    if not should_scan_text(path):
        return findings

    # The scanner documents the patterns it rejects; do not flag itself.
    if path.name == "scan_public_export.py":
        return findings

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as ex:
        findings.append(f"{path.relative_to(root)}: cannot read ({ex})")
        return findings

    example = is_example_path(path, root)
    rel = str(path.relative_to(root)).replace("\\", "/")

    # Documentation may mention reserved prefixes like bookapplication.* without branding the product.
    text_for_brand = re.sub(r"(?i)bookapplication\.\*", "", text)
    text_for_brand = re.sub(r"BOOKAPPLICATION_COMMUNITY_PLUGIN_REGISTRY_URL", "", text_for_brand)
    text_for_brand = re.sub(r"BookApplication-Community-Plugins", "", text_for_brand)
    # Validator reserved-prefix tuples are documentation, not branding.
    if path.name == "validate_registry.py":
        text_for_brand = re.sub(r'["\']bookapplication\.["\']?', "", text_for_brand)
        text_for_brand = re.sub(r"bookapplication\.\*", "", text_for_brand, flags=re.I)

    text_for_secrets = text
    if path.name == "validate_registry.py":
        # Validator rejects this string; do not flag the detector itself.
        text_for_secrets = text_for_secrets.replace("BookAtrium.PluginSdk", "")

    for label, pattern in SECRET_PATTERNS:
        sample = text_for_brand if label.startswith("bookapplication") else text_for_secrets
        if label == "bookapplication_env_active" and pattern.search(text):
            findings.append(f"{rel}: matched {label}")
            continue
        if pattern.search(sample):
            findings.append(f"{rel}: matched {label}")

    for label, pattern in CONTENT_POLICY_PATTERNS:
        if pattern.search(text):
            findings.append(f"{rel}: matched {label}")

    if not example:
        # Instructional path templates should use <id> not {id} in published docs.
        scan_text = re.sub(
            r"(?i)do not (?:leave|use|invent).*?(?:TODO_SECURITY_CONTACT|TODO_LICENSE|REPLACE_ME).*",
            "",
            text,
        )
        # Allow error-message templates in validators that mention ExampleDeveloper as a rejected value.
        if path.name == "validate_registry.py":
            scan_text = re.sub(r"ExampleDeveloper", "", scan_text)
            scan_text = re.sub(r"\{owner\}", "", scan_text)
            scan_text = re.sub(r"\{repo\}", "", scan_text)
        for label, pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(scan_text):
                findings.append(f"{rel}: unresolved placeholder ({label})")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan public registry export for secrets/placeholders")
    parser.add_argument("--root", required=True, help="Root of the exported registry tree")
    parser.add_argument(
        "--allow-legacy-env-docs",
        action="store_true",
        help="Permit documented legacy BOOKAPPLICATION_* environment variable names in specific docs",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 2

    findings: list[str] = []
    skip_dirs = {".git", "bin", "obj", ".vs", "node_modules", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        findings.extend(scan_file(path, root, args.allow_legacy_env_docs))

    if findings:
        print("error: public export scan found high-risk or placeholder content:", file=sys.stderr)
        for item in findings:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(f"::notice::scan_public_export.py OK ({root})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
