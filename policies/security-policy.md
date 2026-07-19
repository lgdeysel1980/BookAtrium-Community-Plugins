# Security policy (registry operations)

Operational security policy for the BookAtrium Community Plugins catalogue ([`lgdeysel1980/BookAtrium-Community-Plugins`](https://github.com/lgdeysel1980/BookAtrium-Community-Plugins)). Companion to root `SECURITY.md`.

## Trust boundaries

| Layer | Trust statement |
|-------|-----------------|
| Catalogue metadata | Curated by registry maintainers; still human-reviewed, not formally certified |
| Release assets | Hosted by the publisher on GitHub Releases; integrity checked by SHA-256 + size |
| Installed plugins | Third-party .NET code with host privileges after explicit user trust confirmation |
| Host behaviour | Downloads immutable URLs only; no GitHub search; no arbitrary registry URLs for normal users |

Catalogue inclusion is **not** a sandbox, signature programme, or safety warranty.

## Reporting channels

### Preferred channel

**GitHub Private Vulnerability Reporting** on `lgdeysel1980/BookAtrium-Community-Plugins`.

Do not invent a public security email. Do not leave unresolved security-contact placeholders.

### What to report privately

- Registry security reports (poisoned metadata, CI bypasses, secret leaks in this repo)
- Vulnerable plugin reports that affect users via the catalogue
- Compromised developer accounts for listed publishers
- Compromised or replaced release assets
- Hash mismatches between catalogue and downloaded bytes
- Malicious update packages referenced by a new listing
- Repository takeover / unexpected transfer of a listed plugin repo

## Incident classes and maintainer actions

| Incident | Typical actions |
|----------|-----------------|
| Hash mismatch / tampered asset | Block version or whole plugin; regenerate index; warn users to disable |
| Malicious update listing | Revert/block entry; private disclosure; public advisory when safe |
| Compromised publisher account | Block listings; contact publisher via alternate channel when possible |
| Repository takeover | Block; require ownership-transfer PR evidence before unblock |
| Broken metadata only | Fix via PR or temporary block if installs fail dangerously |
| Secret leaked in registry repo | Rotate credentials if any; purge history if needed; private report |

## Emergency blocking

Maintainers may immediately:

1. Set `blocked: true` with `blockSeverity` and `blockReason`
2. Populate `blockedVersions` for surgical blocks
3. Set `safeReplacementVersion` or `replacementPluginId` when known
4. Merge an emergency PR to `main` (owner override allowed under branch policy)
5. Communicate severity through BookAtrium release notes / public Issues when appropriate

### Installed-plugin warnings

Hosts may surface block/deprecation metadata on refresh. Users should disable or remove affected plugins. Maintainers should write clear `blockReason` text suitable for display.

### Disable-required handling

When severity is high, prefer catalogue fields that signal “disable now” semantics understood by the host, rather than relying only on prose in Issues.

### No remote deletion

The registry **cannot** and **must not** remotely delete files from user machines. Blocking stops discovery / install / update pathways; uninstall remains a local user action.

## Disclosure coordination

1. Acknowledge private report
2. Reproduce or verify asset hashes / URLs
3. Prepare blocking or corrective catalogue commit
4. Notify publisher when doing so does not increase risk
5. Publish limited public guidance after mitigation
6. Keep exploit detail private until risk is reduced

## Related user support (non-security)

Route non-security support correctly:

- App bugs → https://github.com/lgdeysel1980/BookAtrium/issues
- Plugin behaviour → publisher `supportUrl`
- Listing metadata (non-urgent) → https://github.com/lgdeysel1980/BookAtrium-Community-Plugins/issues

Do not expose private development repositories as a support contact.

## Limits and package constraints

- Maximum package size: **40 MiB**
- HTTPS immutable GitHub Releases URLs only
- Required package extension: `.bookplugin` (Plugin API 2.0)
- Declared `networkHosts` should match real outbound needs
- No certificate-validation bypasses in plugins
- No hidden telemetry without disclosure
