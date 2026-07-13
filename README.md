# BookAtrium Community Plugins registry

Curated catalogue metadata for third-party BookAtrium plugins.

> **Publication status:** This tree is the **template / export source** for the intended public repository [`lgdeysel1980/BookAtrium-Community-Plugins`](https://github.com/lgdeysel1980/BookAtrium-Community-Plugins). That GitHub repository is **not claimed to be live yet**. Until it is created, pushed, and serving raw index files, BookAtrium hosts may see an empty or unreachable catalogue depending on configuration.

## What this registry is

- A **curated** list of plugin metadata entries (`plugins/*.json`)
- A machine-readable generated index (`generated/index.json` and `generated/index.json.gz`)
- A review process for **new listings**, **updates**, **deprecations**, and **blocks**
- Documentation and policies for publishers and maintainers

BookAtrium fetches the official generated index over HTTPS. The intended production endpoint (once the public repo exists on branch `main`) is:

```text
https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json
```

Optional compressed sibling:

```text
https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json.gz
```

## What this registry is not

- Not a plugin binary host â€” developers publish packages on **their own** GitHub Releases
- Not a source-code host for plugins â€” developers keep public source in **their own** repositories
- Not a support desk for third-party plugin behaviour
- Not an automatic GitHub crawler â€” BookAtrium does **not** search or scrape GitHub for plugins
- Not automatic approval of every release â€” a Release alone never updates this catalogue
- Not a security certification â€” inclusion is **not** a safety, quality, or endorsement guarantee
- Not the BookAtrium application repository
- Not a place to file BookAtrium product bugs

## Trust model (read carefully)

Registry entries are **metadata only**. Installing a community plugin downloads a `.bookapp-plugin` package and loads .NET assemblies that run with the **same privileges** as BookAtrium. Users must explicitly confirm trust before install/update. Publishers remain responsible for their code, licences, and support.

## Live catalogue vs examples

| Path | Meaning |
|------|---------|
| `plugins/*.json` | **Live** curated entries included in the generated index |
| `examples/` | **EXAMPLE ONLY â€” NOT INCLUDED IN THE LIVE CATALOGUE** |
| `templates/` | Example shape + submission checklist helpers |

The initial publication intends an **empty** live `plugins/` directory and a valid empty generated index. Fake or placeholder packages must never land in `plugins/`.

## Supported plugin types

Catalogue entries must use one of these BookAtrium plugin types (Plugin API **1.1**):

| Type | Typical use |
|------|-------------|
| `ConversionInput` | Import / convert into library formats |
| `ConversionOutput` | Export / convert to other formats |
| `DeviceInterface` | Device sync / device-specific features |
| `MetadataReader` | Read metadata from files |
| `MetadataSource` | Look up metadata from external sources |
| `MetadataWriter` | Write metadata to files |
| `Store` | Store / retailer search and purchase flows |

Capabilities and network hosts must be declared accurately for the chosen type.

## Reserved plugin id prefixes

Third-party plugins must **not** use:

- `bookatrium.*`
- `bookapplication.*`
- `builtin.*`

Use a stable reverse-DNS id you control (for example `com.yourorg.plugin-name`).

## How to submit a new plugin

1. Implement against `BookAtrium.PluginContracts` (API 1.1 preferred).
2. Test locally in BookAtrium.
3. Package with `BookAtrium.PluginPackager` (`.bookapp-plugin`).
4. Publish an **immutable** GitHub Release asset URL of the form:

   ```text
   https://github.com/<owner>/<repo>/releases/download/{tag}/{asset}.bookapp-plugin
   ```

   Rejected: `/releases/latest/download/â€¦`
5. Record SHA-256 (64 hex) and exact `sizeBytes`.
6. Open a submission Issue with `.github/ISSUE_TEMPLATE/submit-plugin.yml` (optional coordination).
7. Open a pull request adding `plugins/<id>.json`, regenerating `generated/`, and completing the PR template.
8. Pass CI validation. Await maintainer review.

**Opening an Issue does not list the plugin.** Inclusion is discretionary and may be rejected.

See `CONTRIBUTING.md`, `policies/submission-policy.md`, and `policies/publisher-guidelines.md`.

## How to update a listed plugin

1. Bump the semantic version; build and test.
2. Publish a **new** immutable tagged Release asset (never reuse mutable â€œlatestâ€ URLs).
3. Compute the new SHA-256 and size.
4. Update `plugins/<id>.json` â€” keep `id` stable.
5. Disclose capability, network-host, publisher, repository, type, telemetry, and breaking changes in the PR.
6. Regenerate the index; open a PR; pass CI; await review.

A GitHub Release by itself does **not** produce a BookAtrium update.

## Blocked and deprecated plugins

Maintainers may:

- Deprecate an entry and suggest `replacementPluginId`
- Block specific versions (`blockedVersions`) or the whole plugin (`blocked`)
- Record severity and human-readable reasons for hosts to surface

Blocking affects catalogue discovery and remote install/update. BookAtrium does **not** remotely delete installed plugin files. Users disable or remove local plugins themselves. Details: `policies/removal-policy.md`.

## Support routing

Please file issues in the right place. **Do not** use private development repositories as a public support contact.

### Application problems â†’ BookAtrium

https://github.com/lgdeysel1980/BookAtrium/issues

Use for BookAtrium bugs, installer problems, application crashes, Community Plugins **window** bugs, and core plugin-host problems.

### Plugin-specific problems â†’ the plugin publisher

Use the pluginâ€™s `supportUrl` (and their public repository Issues).

Use for plugin output quality, retailer/API changes, metadata quality, device-specific plugin failures, and conversion plugin behaviour.

### Registry / listing problems â†’ this repository (once published)

https://github.com/lgdeysel1980/BookAtrium-Community-Plugins/issues

Use for listing errors, broken registry metadata, missing release assets referenced by an entry, publisher changes, deprecation, removal requests, and compromised listings.

### Security

Use **GitHub Private Vulnerability Reporting** on this registry repository once it exists and the feature is enabled. See `SECURITY.md`. Do not open public Issues for active compromise or exploit details.

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
| Intended registry repository | https://github.com/lgdeysel1980/BookAtrium-Community-Plugins |
| Developer guide (in BookAtrium docs) | See BookAtrium `docs/plugins/developer-guide.md` once published with the app |

## Policies

- `policies/submission-policy.md`
- `policies/security-policy.md`
- `policies/removal-policy.md`
- `policies/publisher-guidelines.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
