# Submission policy

Final policy for curated entries in the BookAtrium Community Plugins registry (`lgdeysel1980/BookAtrium-Community-Plugins` when published).

This policy applies to Issues, pull requests, and maintainer decisions that add or change live catalogue metadata under `plugins/`.

## Purpose

The registry lists **reviewed metadata** pointing at immutable GitHub Release packages. It does not host plugin binaries, does not crawl GitHub, and does not automatically approve releases.

## Acceptance requirements

A submission may be considered only when all of the following are true:

1. **Public source code** â€” the pluginâ€™s source repository is publicly reachable over HTTPS.
2. **Stable plugin ID** â€” lowercase reverse-DNS style id that remains stable across versions.
3. **Supported plugin type** â€” one of: `ConversionInput`, `ConversionOutput`, `DeviceInterface`, `MetadataReader`, `MetadataSource`, `MetadataWriter`, `Store`.
4. **Plugin API** â€” declares Plugin API **1.1** or another API version the current BookAtrium host explicitly supports.
5. **Semantic version** â€” valid SemVer for the listed package.
6. **Immutable release tag** â€” fixed Git tag; no floating channels.
7. **Immutable GitHub Release asset URL** of the form:

   ```text
   https://github.com/<owner>/<repo>/releases/download/{tag}/{asset}
   ```

8. **Valid BookAtrium plugin package** â€” `.bookapp-plugin` produced for BookAtrium / `BookAtrium.PluginContracts`.
9. **SHA-256** â€” 64 hexadecimal characters matching the asset bytes.
10. **Declared package size** â€” exact `sizeBytes` within host limits (maximum 40 MiB).
11. **Declared licence** â€” SPDX identifier and licence URL where applicable.
12. **Support URL** â€” working public support location (Issues URL or documented support page).
13. **Accurate description** â€” not misleading about features, ownership, or affiliation.
14. **Declared capabilities** â€” exact capability names allowed for the plugin type.
15. **Declared network hosts** â€” complete list of outbound hosts when network access is required.
16. **Manifest match** â€” registry entry fields match the package manifest (`id`, version, type, API, capabilities, platforms, bounds).

## Hard prohibitions

Submissions must **not** include or facilitate:

- Malware, droppers, or credential theft
- Hidden telemetry or data collection without clear disclosure
- Disabling or bypassing TLS / certificate validation
- DRM circumvention or piracy tooling
- Pirated, stolen, or otherwise infringing bundled content
- Misleading branding or impersonation of **BookAtrium** or **PractiCore**
- Unsupported or invented plugin types
- Mutable download URLs (`/releases/latest/download/` or equivalent)
- Hidden executable payloads unrelated to the declared plugin
- Secret material (tokens, keys, passwords, private certificates)
- Reserved plugin id prefixes: `bookatrium.*`, `bookapplication.*`, `builtin.*`
- Placeholder / example-only packaging in the live `plugins/` directory
- Hand-edited generated index content that disagrees with regeneration

`publisher.verified` must remain `false` until an official cryptographic publisher-verification programme exists.

## Process

1. Optional: open a submission Issue using the registry Issue form.
2. Required: open a pull request adding or updating `plugins/<id>.json`.
3. Regenerate `generated/index.json` and `generated/index.json.gz`.
4. Pass CI validation and secret/placeholder scans.
5. Maintainer review (discretionary).

**Opening an Issue never lists a plugin automatically.**

## Maintainer discretion

- **Inclusion is discretionary.** Maintainers may reject, defer, or request changes for any reason consistent with safety and quality of the catalogue.
- **Listings may be rejected** even when CI passes.
- **Listings may be deprecated or removed** later under the removal policy.
- **Approval is not a safety guarantee.** Review checks metadata integrity and policy fit; it does not sandbox plugins or cryptographically attest publishers.
- **The publisher remains responsible** for code quality, legal compliance, user support, and security response for their plugin.

## Updates

Update PRs must keep the same plugin `id`, point at a new immutable asset, and disclose material changes (capabilities, network hosts, publisher, repository, type, native dependencies, configuration breaks, platform removals, telemetry, security-sensitive behaviour). See `CONTRIBUTING.md` and the pull-request template.

## Appeals

Publishers may open a registry Issue requesting reconsideration of a rejection, deprecation, or block. Maintainers are not obliged to reverse a decision. Emergency security blocks take priority over appeals.
