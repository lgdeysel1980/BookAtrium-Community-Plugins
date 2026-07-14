# Contributing to the BookAtrium Community Plugins registry

Thank you for contributing catalogue entries. This repository ([`lgdeysel1980/BookAtrium-Community-Plugins`](https://github.com/lgdeysel1980/BookAtrium-Community-Plugins)) holds **curated metadata only**. It is not a plugin hosting service and not the BookAtrium application repository.

An empty live catalogue (`plugins/` with no JSON entries) is valid.

## Before you start

1. Read `policies/submission-policy.md`, `policies/security-policy.md`, `policies/removal-policy.md`, and `policies/publisher-guidelines.md`.
2. Build against **Plugin API 2.0** using **only** `BookAtrium.PluginContracts` **2.0.0**. Do not reference any other BookAtrium package. (Public NuGet publication of 2.0.0 may still be pending — do not invent a feed URL.)
3. Use the `bookatrium-plugin` CLI (`new` / `run` / `test` / `validate` / `pack` / `prepare-release`).
4. Publish an **immutable** GitHub Release asset ending in `.bookplugin` (not `/releases/latest/download/`). Legacy API 1.0/1.1 packages may use `.bookapp-plugin` or `.bookmetadata-plugin`.
5. Compute the SHA-256 and exact byte size of the release asset.

Opening an Issue does **not** list a plugin. Catalogue changes require a reviewed pull request that updates `plugins/*.json` and regenerates `generated/`.

## Fork and branch workflow

1. Fork the registry repository.
2. Create a branch from `main` (for example `add/com.example.my-plugin` or `update/com.example.my-plugin-1.2.0`).
3. Add or edit exactly the manifests you intend to change.
4. Regenerate the index locally.
5. Open a pull request using the PR template.

Prefer **one plugin per pull request**. Related update + deprecation pairs may share a PR when clearly documented.

## Manifest filename and layout

- Live catalogue entries live only in `plugins/{plugin-id}.json`.
- Use the stable plugin id as the filename (must match the JSON `id` field).
- One plugin per manifest file.
- Do **not** put live entries under `examples/`, `templates/`, or `samples/`.
- Do **not** hand-edit `generated/index.json` or `generated/index.json.gz` with different content than the generator produces — regenerate them.

Reserved plugin id prefixes (reject for third-party submissions):

- `bookatrium.*`
- `bookapplication.*` (legacy reserved)
- `builtin.*`

## Validation commands

From the registry repository root:

```bash
python scripts/validate_registry.py --plugins-dir plugins --schema schemas/community-plugin.schema.json
python scripts/generate_index.py --plugins-dir plugins --output-dir generated
python scripts/scan_public_export.py --root .
```

When working inside the private BookAtrium development tree before export, maintainers may also run `BookAtrium.PluginRegistryBuilder` with `--publication`. Public CI must remain self-contained and must not depend on private source.

## Generated index policy

Contributors must:

1. Edit `plugins/*.json` only for catalogue content
2. Regenerate `generated/index.json`
3. Regenerate `generated/index.json.gz`
4. Include those generated files in the pull request

CI regenerates independently and **fails** if committed generated files are stale. Ordering is deterministic. There is no CI auto-commit bot. Prefer squash merges.

## Pull request requirements

Use `.github/PULL_REQUEST_TEMPLATE.md` and fill every applicable section:

- Submission kind (new / update / deprecation / block / replacement)
- Plugin id, versions, release tag, immutable asset URL, SHA-256, size
- Plugin API (`2.0` for new submissions) and BookAtrium compatibility
- Platforms, licence, changelog
- Capability and network-host deltas for updates
- Rights and support confirmations
- Local validation commands and results

## Update submissions

For updates you must disclose:

- New or removed capabilities
- Added or removed network hosts
- Publisher or repository changes
- Plugin-type changes
- Native dependency changes
- Breaking configuration changes
- Removed platform support
- Security-sensitive behaviour changes
- Telemetry / privacy changes

A GitHub Release alone does **not** produce a catalogue update.

## Review expectations

- Maintainers may request changes, reject, or defer listings without explanation of private security criteria.
- Passing CI is necessary but not sufficient.
- Approval is discretionary and is **not** a safety guarantee.
- Maintainers may squash-merge.

## Support responsibilities

- You support your own plugin (via `supportUrl` / repository Issues).
- Registry Issues are for listing and catalogue metadata problems.
- Application bugs go to the public BookAtrium repository Issues — not here.
- Do not direct end users to private development repositories.

## Security-sensitive submissions

If your change addresses malware, compromise, or hash mismatch:

- Prefer coordinated private disclosure via GitHub Private Vulnerability Reporting on this repository
- Mark urgency clearly in the PR
- Provide exact URL, SHA-256, and recommended block/deprecation fields

## No automatic approval

- Issues do not auto-list plugins
- Releases do not auto-update the catalogue
- CI does not approve or merge PRs
- Maintainer discretion always applies
