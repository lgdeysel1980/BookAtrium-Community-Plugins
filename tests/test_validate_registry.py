from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_registry as vr  # noqa: E402


def _base_entry() -> dict:
    return {
        "id": "com.acme.testplugin",
        "name": "Test Plugin",
        "publisher": {"name": "Acme", "githubLogin": "acmeplugins", "verified": False},
        "pluginType": "Store",
        "version": "1.2.3",
        "minimumAppVersion": "1.0.0",
        "pluginApiVersion": "2.0",
        "supportedPlatforms": ["windows"],
        "repositoryUrl": "https://github.com/acmeplugins/test-plugin",
        "supportUrl": "https://github.com/acmeplugins/test-plugin/issues",
        "documentationUrl": "https://github.com/acmeplugins/test-plugin#readme",
        "license": {"spdxId": "MIT", "url": "https://github.com/acmeplugins/test-plugin/blob/main/LICENSE"},
        "package": {
            "downloadUrl": "https://github.com/acmeplugins/test-plugin/releases/download/v1.2.3/Test.Plugin-1.2.3.bookplugin",
            "fileName": "Test.Plugin-1.2.3.bookplugin",
            "sizeBytes": 12345,
            "sha256": "a" * 64,
        },
        "capabilities": ["StoreSearch"],
        "networkHosts": ["acmebooks.org"],
        "tags": ["acme"],
        "uninstallPluginIds": [],
        "blockedVersions": [],
    }


class ValidateRegistryApi2Tests(unittest.TestCase):
    def _validate(self, data: dict) -> list[str]:
        return vr.validate_entry(
            Path("plugins/com.acme.testplugin.json"),
            data,
            set(),
            set(),
            set(),
            publication=True,
        )

    def test_rejects_legacy_api_1_0(self) -> None:
        data = _base_entry()
        data["pluginApiVersion"] = "1.0"
        errors = self._validate(data)
        self.assertTrue(any("pluginApiVersion must be 2.0" in e for e in errors), errors)

    def test_rejects_bookapp_plugin_suffix(self) -> None:
        data = _base_entry()
        data["package"]["fileName"] = "Test.Plugin-1.2.3.bookapp-plugin"
        errors = self._validate(data)
        self.assertTrue(any("package.fileName must end with .bookplugin" in e for e in errors), errors)

    def test_rejects_bookmetadata_plugin_suffix(self) -> None:
        data = _base_entry()
        data["package"]["fileName"] = "Test.Plugin-1.2.3.bookmetadata-plugin"
        errors = self._validate(data)
        self.assertTrue(any("package.fileName must end with .bookplugin" in e for e in errors), errors)

    def test_accepts_api2_bookplugin(self) -> None:
        data = _base_entry()
        errors = self._validate(copy.deepcopy(data))
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
