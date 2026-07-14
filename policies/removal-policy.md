# Removal, deprecation, and blocking policy

This policy governs how live catalogue entries are deprecated, blocked, replaced, or removed from the BookAtrium Community Plugins registry ([`lgdeysel1980/BookAtrium-Community-Plugins`](https://github.com/lgdeysel1980/BookAtrium-Community-Plugins)).

An empty catalogue after removals is valid.

## Principles

1. Prefer **blocking** or **deprecation metadata** over silent hard deletion when users may already have the plugin installed.
2. Prefer **version-specific blocks** when only some releases are unsafe.
3. Prefer a documented **replacement plugin** when a rename or successor exists.
4. Never claim remote deletion of files on user disks.
5. Security emergencies outrank courtesy notice periods.

## Grounds for action

Maintainers may deprecate, block, or remove entries for:

| Ground | Typical tool |
|--------|----------------|
| Deprecation / rename | `deprecated` + `replacementPluginId` |
| Version-specific defect or vulnerability | `blockedVersions` |
| Whole-plugin compromise or abandonment | `blocked: true` |
| Security compromise | Block + security process |
| Malware | Immediate whole-plugin block |
| Repository takeover | Block pending ownership verification |
| Broken or missing release asset | Block or remove until fixed |
| Package / hash / size mismatch | Block version; fix or remove |
| Licence violation | Deprecate/remove; legal review |
| Copyright / DMCA-style complaint | Temporary block pending review |
| Severe incompatibility with current BookAtrium | Deprecate or block versions |
| Repeated policy violation | Removal after warnings when practical |
| Publisher-requested removal | Confirm identity, then deprecate/remove |
| Emergency owner override | Direct `main` fix under branch policy |

## Deprecation

Use deprecation when a plugin should stop receiving new installs but is not necessarily malicious:

- Mark the entry deprecated
- Provide `replacementPluginId` when available
- Keep historical versions visible for update/disable messaging when useful
- Document rationale in the PR

## Version-specific blocking

When only certain versions are unsafe:

- Add those versions to `blockedVersions`
- Leave safe versions installable if still appropriate
- Provide `safeReplacementVersion` when a patched release exists

## Whole-plugin blocking

When the plugin as a whole is unsafe, abandoned in a dangerous state, or repeatedly abusive:

- Set `blocked: true`
- Set `blockSeverity` and a clear `blockReason`
- Regenerate and publish the index promptly

## Replacement plugin

When ownership, naming, or architecture changes:

- Keep old id deprecated with `replacementPluginId`
- Do not reuse a different product’s id without an ownership-transfer process
- Document repository URL and publisher changes in the PR

## Publisher-requested removal

Publishers may request removal via registry Issue or PR:

1. Maintainer verifies the requester controls the listed publisher/repository
2. Prefer deprecation + replacement when users are mid-migration
3. Hard-delete `plugins/{id}.json` only when necessary
4. Regenerate the index via the normal PR/CI path

## Appeal / review path

- Open a registry Issue describing the action and requested remedy
- Provide evidence (fixed release, new hash, ownership proof)
- Security blocks may remain until maintainers are satisfied
- Appeals do not entitle automatic reinstatement

## Emergency owner override

Repository owners may push an emergency catalogue fix when:

- Delay would leave users exposed
- CI or review workflows are unavailable
- A compromised listing must be blocked immediately

Document the override in a follow-up PR or Issue when practical. Branch protection may temporarily be bypassed by owners; restore normal process after.

## User impact and local control

| Catalogue action | Host effect | Local plugin files |
|------------------|-------------|--------------------|
| Deprecate | Warn; may discourage new installs | Remain until user removes |
| Block version | Refuse install/update of that version | User should disable/uninstall |
| Block plugin | Hide / refuse remote install/update | User should disable/uninstall |
| Hard-delete entry | Disappears from catalogue | Still local until user removes |

Hosts may recommend disable. **No remote file deletion** is performed by the registry.

## Process checklist for maintainers

1. Confirm ground and severity
2. Prefer smallest effective action (version block vs whole-plugin block)
3. Update `plugins/{id}.json` (or delete if hard-removing)
4. Regenerate `generated/index.json` and `.gz`
5. Pass CI
6. Merge to `main`
7. Communicate via registry Issue / BookAtrium notes when user-visible
8. Coordinate private disclosure for active compromises (`SECURITY.md`)
