# BookAtrium Community Plugins registry

Curated catalogue metadata for third-party BookAtrium plugins.

Live public repository: [`lgdeysel1980/BookAtrium-Community-Plugins`](https://github.com/lgdeysel1980/BookAtrium-Community-Plugins).

## What this registry is

- A **curated** list of plugin metadata entries (`plugins/*.json`)
- A machine-readable generated index (`generated/index.json` and `generated/index.json.gz`)
- A review process for **new listings**, **updates**, **deprecations**, and **blocks**
- Documentation and policies for publishers and maintainers

An empty `plugins/` directory (zero plugins) is valid. BookAtrium hosts fetch the official generated index over HTTPS:

```text
https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json
```

Compressed sibling:

```text
https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json.gz
```

## What this registry is not

- Not a plugin binary host — developers publish packages on **their own** GitHub Releases
- Not a source-code host for plugins — developers keep public source in **their own** repositories
- Not a support desk for third-party plugin behaviour
- Not an automatic GitHub crawler — BookAtrium does **not** search or scrape GitHub for plugins
- Not automatic approval of every release — a Release alone never updates this catalogue
- Not a security certification — inclusion is **not** a safety, quality, or endorsement guarantee
- Not the BookAtrium application repository
- Not a place to file BookAtrium product bugs

## Trust model (read carefully)

Registry entries are **metadata only**. Installing a community plugin downloads a `.bookplugin` package (legacy listings may use `.bookapp-plugin`) and loads .NET assemblies that run with the **same privileges** as BookAtrium. Users must explicitly confirm trust before install/update. Publishers remain responsible for their code, licences, and support.

## Live catalogue vs examples

| Path | Meaning |
|------|---------|
| `plugins/*.json` | **Live** curated entries included in the generated index |
| `examples/` | **EXAMPLE ONLY — NOT INCLUDED IN THE LIVE CATALOGUE** |
| `templates/` | Example shape + submission checklist helpers |

Fake or placeholder packages must never land in `plugins/`. Zero live plugins is a valid catalogue state.

## Supported plugin types

Catalogue entries must use one of these BookAtrium plugin types. **Plugin API 2.0** is canonical for new submissions (API 1.0 / 1.1 remain accepted for legacy packages).

| Type | API 2.0 base class | Typical use |
|------|--------------------|-------------|
| `ConversionInput` | `InputConverterPlugin` | Import / convert into library formats |
| `ConversionOutput` | `OutputConverterPlugin` | Export / convert to other formats |
| `DeviceInterface` | `DevicePlugin` | Device sync / device-specific features |
| `MetadataReader` | `MetadataReaderPlugin` | Read metadata from files |
| `MetadataSource` | `MetadataSourcePlugin` | Look up metadata from external sources |
| `MetadataWriter` | `MetadataWriterPlugin` | Write metadata to files |
| `Store` | `StorePlugin` | Store / retailer search and purchase flows |

Authoring helpers include `PluginInfo`, `PluginContext`, `PluginTestContext`, `NetworkHosts`, and the `PluginSetting` attribute. Capabilities and network hosts must be declared accurately for the chosen type.

## Reserved plugin id prefixes

Third-party plugins must **not** use:

- `bookatrium.*`
- `bookapplication.*`
- `builtin.*`

Use a stable reverse-DNS id you control (for example `com.yourorg.plugin-name`).

## How to submit a new plugin

1. Reference **only** `BookAtrium.PluginContracts` **2.0.0** (PackageReference; public NuGet publication pending — do not invent a feed URL). Do not reference any other BookAtrium package.
2. Scaffold and develop with the `bookatrium-plugin` CLI (`new`, `run`, `test`, `validate`, `pack`, `prepare-release`).
3. Implement an API 2.0 base class (`StorePlugin`, `MetadataSourcePlugin`, etc.).
4. Pack a **`.bookplugin`** asset and publish an **immutable** GitHub Release URL of the form:

   ```text
   https://github.com/<owner>/<repo>/releases/download/{tag}/{asset}.bookplugin
   ```

   Rejected: `/releases/latest/download/…`
5. Record SHA-256 (64 hex) and exact `sizeBytes`.
6. Open a submission Issue with `.github/ISSUE_TEMPLATE/submit-plugin.yml` (optional coordination).
7. Open a pull request adding `plugins/<id>.json`, regenerating `generated/`, and completing the PR template.
8. Pass CI validation. Await maintainer review.

**Opening an Issue does not list the plugin.** Inclusion is discretionary and may be rejected.

See `CONTRIBUTING.md`, `policies/submission-policy.md`, and `policies/publisher-guidelines.md`.

## How to update a listed plugin

1. Bump the semantic version; build and test (`bookatrium-plugin test` / `validate`).
2. Publish a **new** immutable tagged Release asset (never reuse mutable “latest” URLs).
3. Compute the new SHA-256 and size.
4. Update `plugins/<id>.json` — keep `id` stable.
5. Disclose capability, network-host, publisher, repository, type, telemetry, and breaking changes in the PR.
6. Regenerate the index; open a PR; pass CI; await review.

A GitHub Release by itself does **not** produce a BookAtrium update.

## Blocked and deprecated plugins

Maintainers may:

- Deprecate an entry and suggest `replacementPluginId`
- Block specific versions (`blockedVersions`) or the whole plugin (`blocked`)
- Record severity and human-readable reasons for hosts to surface

Blocking affects catalogue discovery and remote install/update. BookAtrium does **not** remotely delete installed plugin files. Users disable or remove local plugins themselves. Details: `policies/removal-policy.md`.

## Official first-party plugins

First-party BookAtrium plugins are published through the **official** plugin registry, not this community catalogue. When a plugin moves to the official catalogue, its community source entry is removed and a short migration note is kept under `docs/migrations/`. Existing installs continue to match by permanent plugin ID.

See for example: [`docs/migrations/amazon-us-kindle-store.md`](docs/migrations/amazon-us-kindle-store.md).

## Support routing

Please file issues in the right place. **Do not** use private development repositories as a public support contact.

### Application problems → BookAtrium

https://github.com/lgdeysel1980/BookAtrium/issues

Use for BookAtrium bugs, installer problems, application crashes, Community Plugins **window** bugs, and core plugin-host problems.

### Plugin-specific problems → the plugin publisher

Use the plugin’s `supportUrl` (and their public repository Issues).

Use for plugin output quality, retailer/API changes, metadata quality, device-specific plugin failures, and conversion plugin behaviour.

### Registry / listing problems → this repository

https://github.com/lgdeysel1980/BookAtrium-Community-Plugins/issues

Use for listing errors, broken registry metadata, missing release assets referenced by an entry, publisher changes, deprecation, removal requests, and compromised listings.

### Security

Use **GitHub Private Vulnerability Reporting** on this registry repository. See `SECURITY.md`. Do not open public Issues for active compromise or exploit details.

This registry must **not** become the support desk for every third-party plugin.

## Security overview

- Hosts download only immutable GitHub Releases assets, verify size and SHA-256, then validate the package locally.
- Users confirm trust before install/update.
- Report registry integrity problems via Private Vulnerability Reporting (`SECURITY.md`, `policies/security-policy.md`).

## Licence

The registry repository content and validation scripts are MIT licensed.

Plugin source code and binaries remain under each publisher's declared licence.
Listing a plugin does not transfer ownership to BookAtrium.
BookAtrium is not the publisher or support provider for third-party plugins.
The MIT licence applies only to material contained in the registry repository.

See `LICENSE` for the full MIT text.

## Building and validating locally

```bash
python scripts/validate_registry.py --plugins-dir plugins --schema schemas/community-plugin.schema.json
python scripts/generate_index.py --plugins-dir plugins --output-dir generated
python scripts/scan_public_export.py --root .
```

Public CI (`.github/workflows/validate-and-build-index.yml`) uses these self-contained scripts. It does not clone private development sources.

## Links

| Resource | URL |
|----------|-----|
| BookAtrium public repository | https://github.com/lgdeysel1980/BookAtrium |
| BookAtrium releases | https://github.com/lgdeysel1980/BookAtrium/releases |
| BookAtrium issues | https://github.com/lgdeysel1980/BookAtrium/issues |
| Community Plugins registry | https://github.com/lgdeysel1980/BookAtrium-Community-Plugins |
| Catalogue index (JSON) | https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json |
| Catalogue index (gzip) | https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json.gz |
| Developer guide | BookAtrium `docs/plugins/sdk-2/` (Plugin API 2.0) |

## Policies

- `policies/submission-policy.md`
- `policies/security-policy.md`
- `policies/removal-policy.md`
- `policies/publisher-guidelines.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
