# Security policy

This document is intended for the future public repository `lgdeysel1980/BookAtrium-Community-Plugins`. That repository is **not yet published**. When it is, enable **GitHub Private Vulnerability Reporting** before treating this channel as live.

## How to report a vulnerability

**Do not open a public issue for security-sensitive reports.**

Security reports for this registry should use **GitHub Private Vulnerability Reporting** for the `lgdeysel1980/BookAtrium-Community-Plugins` repository once it exists and that feature is enabled.

Use Private Vulnerability Reporting for:

- Suspected malicious or compromised catalogue entries
- Hash mismatches or tampered release assets referenced by the registry
- Compromised publisher accounts or repository takeovers affecting listed plugins
- Malicious update paths discovered through the catalogue
- Secrets accidentally committed to this registry repository
- CI or indexing defects that could cause unsafe installs

If Private Vulnerability Reporting is not yet enabled, repository maintainers must enable it before first public release. Until then, do not invent an email address or leave an unresolved security-contact placeholder.

## What is in scope

| In scope | Out of scope |
|----------|--------------|
| Registry metadata accuracy and integrity | Everyday plugin usage questions |
| Catalogue listing that points at unsafe assets | Feature requests for BookAtrium |
| Compromised / replaced GitHub Release assets for listed plugins | Support for third-party retailer APIs |
| Registry CI defects that accept invalid / mutable URLs | Product bugs unrelated to the catalogue |
| Integrity of committed `generated/index.json` | Private development repository access |

## Plugin security reports

Community plugins are third-party .NET packages. Installing a plugin executes code with the same privileges as BookAtrium. Catalogue inclusion is curated metadata review — **not** a sandbox, notarisation, or cryptographic publisher signature.

When reporting a vulnerable or malicious **plugin**:

1. Prefer GitHub Private Vulnerability Reporting on this registry if the listing is the distribution path.
2. Also notify the plugin publisher via their `supportUrl` / repository Security tab when safe.
3. Include plugin id, version, release asset URL, SHA-256, and observed behaviour.

## Compromised assets and accounts

Report immediately if you believe any of the following occurred:

- A listed release asset was replaced or poisoned
- A publisher GitHub account was taken over
- A plugin repository was transferred to an untrusted party without registry notice
- A new “update” package does not match the declared SHA-256
- An entry uses a mutable `/releases/latest/download/` URL

Maintainers may mark versions or whole plugins as blocked, deprecate entries, or remove listings. See `policies/security-policy.md` and `policies/removal-policy.md`.

## Emergency blocking

Maintainers may:

- Set `blocked: true` with `blockSeverity` and `blockReason`
- Add specific versions to `blockedVersions`
- Point users at `safeReplacementVersion` or `replacementPluginId`
- Force a catalogue refresh path for subsequent client fetches

**Hosts do not remotely delete files from a user’s machine.** Blocking and deprecation affect discovery, install, and update behaviour. Users disable or uninstall local plugins themselves.

## Disclosure coordination

- Prefer coordinated disclosure when a patch or blocked listing can ship quickly.
- Maintainers may publish public advisories after mitigation when appropriate.
- Do not disclose exploit details in public Issues while a blocking update is in progress.

## Maintainer response (target)

Once the public repository is live and Private Vulnerability Reporting is enabled, maintainers aim to:

1. Acknowledge receipt
2. Triage severity (listing integrity vs installed-plugin impact)
3. Block or remove unsafe catalogue references when needed
4. Coordinate with the publisher when contact is safe
5. Document user guidance (disable / update / replacement)

Response times depend on severity and maintainer availability. This policy is not an SLA.

## Related policies

- `policies/security-policy.md` — detailed registry security process
- `policies/removal-policy.md` — deprecation, blocking, removal
- `policies/submission-policy.md` — what submissions must not contain
