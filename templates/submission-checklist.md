# Plugin submission checklist

- [ ] Id is stable, lowercase, and not reserved (`bookatrium.*` / `bookapplication.*` / `builtin.*`)
- [ ] `pluginType` is an exact Phase 3U enum name
- [ ] `capabilities` use exact Phase 3U capability names allowed for that type
- [ ] `publisher.verified` is `false`
- [ ] `repositoryUrl` is `https://github.com/{owner}/{repo}` (filled with real owner/repo — never leave braces)
- [ ] `package.downloadUrl` is an immutable Releases download URL (not `/latest/`)
- [ ] `package.fileName` matches the asset name in the URL
- [ ] `package.sha256` is lowercase/uppercase hex (64 chars) of the asset bytes
- [ ] `package.sizeBytes` matches the asset size (1 … 40 MiB)
- [ ] Licence SPDX id is set
- [ ] Entry file is named `plugins/{id}.json`
- [ ] I have read `policies/submission-policy.md`, `security-policy.md`, and `removal-policy.md`
