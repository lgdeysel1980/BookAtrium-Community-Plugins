## Submission kind

- [ ] New plugin
- [ ] Plugin update
- [ ] Deprecation
- [ ] Block
- [ ] Replacement / ownership follow-up

## Plugin identity

- **Plugin ID:**
- **Old version:** (N/A for new plugins)
- **New version:**
- **Release tag:**
- **Exact immutable asset URL:**
- **SHA-256:**
- **Package size (bytes):**
- **Plugin API version:** (`2.0`)
- **Package extension:** (`.bookplugin` for API 2.0)
- **App compatibility:** min ______ / max ______ (max optional)
- **Platforms:**
- **Licence (SPDX):**
- **Support URL:**

## Changelog

<!-- Summarise user-visible changes. -->

## Local validation

Commands run:

```bash
python scripts/validate_registry.py --plugins-dir plugins --schema schemas/community-plugin.schema.json
python scripts/generate_index.py --plugins-dir plugins --output-dir generated
python scripts/scan_public_export.py --root .
```

- **Validation result:** (pass/fail + notes)

## Rights confirmation

- [ ] I own or have permission to distribute this plugin and its dependencies
- [ ] Source repository is public
- [ ] Project references only `BookAtrium.PluginContracts` (no other BookAtrium package)
- [ ] Release asset is immutable (not `/releases/latest/download/`)
- [ ] Manifest matches the package
- [ ] No secrets, TLS bypass, hidden telemetry, undisclosed collection, DRM circumvention, or infringing content
- [ ] I accept support responsibility via the stated support URL
- [ ] I understand inclusion is discretionary and not a safety guarantee

## Update disclosures (required for updates)

Leave unchecked / write “none” only when truly not applicable.

- [ ] **New capabilities:**
- [ ] **Removed capabilities:**
- [ ] **Added network hosts:**
- [ ] **Removed network hosts:**
- [ ] **Publisher change:**
- [ ] **Repository transfer:**
- [ ] **Plugin-type change:**
- [ ] **Native dependency changes:**
- [ ] **Breaking configuration changes:**
- [ ] **Removed platform support:**
- [ ] **Security-sensitive changes:**
- [ ] **Telemetry / privacy changes:**

## Catalogue files

- [ ] `plugins/{id}.json` added or updated
- [ ] `generated/index.json` regenerated
- [ ] `generated/index.json.gz` regenerated
- [ ] Did **not** hand-author generated files with non-deterministic content
- [ ] `publisher.verified` is `false`
- [ ] Did **not** use reserved ids (`bookatrium.*`, `bookapplication.*`, `builtin.*`)
- [ ] Examples under `examples/` were not copied into live `plugins/` unless the package is a real public release

## Maintainer checklist

- [ ] Immutable URL verified
- [ ] SHA-256 / size verified against downloaded asset
- [ ] Plugin type + capabilities plausible
- [ ] Network hosts reviewed
- [ ] API 2.0 + `.bookplugin`
- [ ] Update disclosures reviewed (if applicable)
- [ ] Policy compliance (submission / security / removal)
- [ ] CI green
- [ ] Generated files fresh
- [ ] Decision: approve / request changes / reject
