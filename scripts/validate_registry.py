#!/usr/bin/env python3
"""Lightweight registry validation for standalone public CI (no private monorepo required).

Validates:
  - plugins/*.json structural rules mirroring BookAtrium.Core CommunityPluginRegistryValidator
  - Unique plugin ids / package fileNames / downloadUrls
  - Immutable GitHub release download URL shape
  - SHA-256 hex length
  - pluginType / capability enum names
    - pluginApiVersion 2.0 only
    - Package extension .bookplugin only
  - Reserved id prefixes: bookatrium.*, bookapplication.*, builtin.*

Exit codes: 0 success, 1 validation failure, 2 usage/environment error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLUGIN_TYPES = {
    "ConversionInput",
    "ConversionOutput",
    "DeviceInterface",
    "MetadataReader",
    "MetadataSource",
    "MetadataWriter",
    "Store",
}

CAPABILITIES = {
    "NetworkAccess",
    "PluginSettingsStorage",
    "TemporaryFileAccess",
    "ReadBookMetadata",
    "WriteBookMetadata",
    "ReadInputFormat",
    "ProduceOutputFormat",
    "DetectDevice",
    "TransferToDevice",
    "StoreSearch",
    "CoverDownload",
    "MetadataLookup",
}

PLATFORMS = {"windows-x64", "windows-x86", "windows-arm64", "windows", "any"}
ALLOWED_API = {"2.0"}
API2_PACKAGE_SUFFIX = ".bookplugin"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
ID_RE = re.compile(r"^[a-z0-9]([a-z0-9.\-]{0,126}[a-z0-9])?$")
RELEASE_URL_RE = re.compile(
    r"^https://github\.com/[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9._\-]+/releases/download/[^/]+/[^/?#]+$"
)
REPO_URL_RE = re.compile(
    r"^https://github\.com/[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?/[A-Za-z0-9._\-]+/?$"
)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
WIN_ABS_PATH_RE = re.compile(r"(?i)[A-Za-z]:\\")
MAX_PACKAGE_BYTES = 40 * 1024 * 1024
MIN_PACKAGE_BYTES = 1
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
RESERVED_PREFIXES = ("bookatrium.", "bookapplication.", "builtin.")


def fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)


def iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from iter_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_strings(nested)


def validate_entry(
    path: Path,
    data: dict,
    seen_ids: set[str],
    seen_files: set[str],
    seen_urls: set[str],
    publication: bool,
) -> list[str]:
    errors: list[str] = []
    prefix = path.name

    comment = str(data.get("_comment") or "")
    if "EXAMPLE ONLY" in comment.upper() and publication:
        errors.append(f"{prefix}: EXAMPLE ONLY entries are not allowed in live plugins/")

    for text in iter_strings(data):
        if "BookAtrium.PluginSdk" in text:
            errors.append(f"{prefix}: BookAtrium.PluginSdk must not appear in registry entries")
            break
    for text in iter_strings(data):
        if "BookAtrium-Development" in text or WIN_ABS_PATH_RE.search(text):
            errors.append(f"{prefix}: private path / development-tree content is not allowed")
            break

    plugin_id = data.get("id")
    if not isinstance(plugin_id, str) or not ID_RE.match(plugin_id):
        errors.append(f"{prefix}: invalid id")
    elif plugin_id.startswith(RESERVED_PREFIXES):
        errors.append(f"{prefix}: reserved id prefix")
    elif plugin_id in seen_ids:
        errors.append(f"{prefix}: duplicate id '{plugin_id}'")
    else:
        seen_ids.add(plugin_id)

    if data.get("pluginType") not in PLUGIN_TYPES:
        errors.append(f"{prefix}: unknown pluginType '{data.get('pluginType')}'")

    publisher = data.get("publisher") or {}
    if publisher.get("verified") is True:
        errors.append(f"{prefix}: publisher.verified must be false")

    github_login = str(publisher.get("githubLogin") or "")
    if publication and github_login.lower() in {"exampledeveloper", "yourgithublogin"}:
        errors.append(f"{prefix}: placeholder publisher githubLogin is not allowed for publication")

    if not REPO_URL_RE.match(str(data.get("repositoryUrl") or "")):
        errors.append(f"{prefix}: repositoryUrl must be https://github.com/{{owner}}/{{repo}}")
    elif publication and "ExampleDeveloper" in str(data.get("repositoryUrl")):
        errors.append(f"{prefix}: placeholder repositoryUrl is not allowed for publication")

    version = str(data.get("version") or "")
    if not SEMVER_RE.match(version):
        errors.append(f"{prefix}: version must be semantic (e.g. 1.2.3)")

    api = str(data.get("pluginApiVersion") or "")
    if api not in ALLOWED_API:
        errors.append(f"{prefix}: pluginApiVersion must be 2.0")

    package = data.get("package") or {}
    download_url = str(package.get("downloadUrl") or "")
    if "/releases/latest/" in download_url or not RELEASE_URL_RE.match(download_url):
        errors.append(f"{prefix}: package.downloadUrl must be an immutable GitHub Releases asset URL")
    elif publication and "ExampleDeveloper" in download_url:
        errors.append(f"{prefix}: placeholder downloadUrl is not allowed for publication")

    file_name = str(package.get("fileName") or "")
    if not file_name or "/" in file_name or "\\" in file_name or ".." in file_name:
        errors.append(f"{prefix}: invalid package.fileName")
    elif not file_name.endswith(API2_PACKAGE_SUFFIX):
        errors.append(f"{prefix}: package.fileName must end with .bookplugin")
    elif file_name in seen_files:
        errors.append(f"{prefix}: duplicate package.fileName '{file_name}'")
    else:
        seen_files.add(file_name)

    if download_url in seen_urls:
        errors.append(f"{prefix}: duplicate package.downloadUrl")
    else:
        seen_urls.add(download_url)

    sha = str(package.get("sha256") or "")
    if not SHA256_RE.match(sha):
        errors.append(f"{prefix}: package.sha256 must be 64 hex characters")
    elif publication and sha.lower() == EMPTY_SHA256:
        errors.append(f"{prefix}: empty-file SHA-256 is not allowed for publication")

    size = package.get("sizeBytes")
    if not isinstance(size, int) or size < MIN_PACKAGE_BYTES or size > MAX_PACKAGE_BYTES:
        errors.append(f"{prefix}: package.sizeBytes must be between 1 and 40 MiB")

    platforms = data.get("supportedPlatforms")
    if not isinstance(platforms, list) or not platforms:
        errors.append(f"{prefix}: supportedPlatforms required")
    else:
        for p in platforms:
            if p not in PLATFORMS:
                errors.append(f"{prefix}: unknown platform '{p}'")

    caps = data.get("capabilities")
    if not isinstance(caps, list):
        errors.append(f"{prefix}: capabilities must be an array")
    else:
        for c in caps:
            if c not in CAPABILITIES:
                errors.append(f"{prefix}: unknown capability '{c}'")

    hosts = data.get("networkHosts")
    if not isinstance(hosts, list):
        errors.append(f"{prefix}: networkHosts must be an array")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate community plugin registry entries")
    parser.add_argument("--plugins-dir", required=True)
    parser.add_argument("--schema", default=None, help="Optional schema path (informational)")
    parser.add_argument(
        "--publication",
        action="store_true",
        help="Reject EXAMPLE/placeholder live catalogue entries",
    )
    args = parser.parse_args()

    plugins_dir = Path(args.plugins_dir)
    if not plugins_dir.is_dir():
        fail(f"plugins directory not found: {plugins_dir}")
        return 2

    files = sorted(plugins_dir.glob("*.json"), key=lambda p: p.name)
    print(f"::notice::validate_registry.py checking {len(files)} file(s)")

    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    seen_urls: set[str] = set()
    all_errors: list[str] = []

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as ex:
            all_errors.append(f"{path.name}: {ex}")
            continue
        if not isinstance(data, dict):
            all_errors.append(f"{path.name}: expected JSON object")
            continue
        all_errors.extend(
            validate_entry(path, data, seen_ids, seen_files, seen_urls, args.publication)
        )

    if all_errors:
        for err in all_errors:
            fail(err)
        return 1

    print(f"::notice::validate_registry.py OK ({len(files)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
