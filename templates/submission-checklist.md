# Plugin submission checklist

- [ ] Id is stable, lowercase, and not reserved (`bookatrium.*` / `bookapplication.*` / `builtin.*`)
- [ ] `pluginApiVersion` is `"2.0"`
- [ ] Project references **only** `BookAtrium.PluginContracts` 2.0.0 (no other BookAtrium package)
- [ ] Implemented via API 2.0 bases (`StorePlugin`, `MetadataSourcePlugin`, `MetadataReaderPlugin`, `MetadataWriterPlugin`, `InputConverterPlugin`, `OutputConverterPlugin`, or `DevicePlugin`)
- [ ] Validated with `bookatrium-plugin` (`validate` / `test` / `pack` / `prepare-release` as applicable)
- [ ] `pluginType` is an exact registry enum name
- [ ] `capabilities` use exact capability names allowed for that type
- [ ] `publisher.verified` is `false`
- [ ] `repositoryUrl` is `https://github.com/OWNER/REPO` with real owner/repo filled in
- [ ] `package.downloadUrl` is an immutable Releases download URL (not `/latest/`)
- [ ] `package.fileName` ends in `.bookplugin`
- [ ] `package.fileName` matches the asset name in the URL
- [ ] `package.sha256` is hex (64 chars) of the asset bytes
- [ ] `package.sizeBytes` matches the asset size (1 … 40 MiB)
- [ ] Licence SPDX id is set
- [ ] Entry file is named `plugins/{id}.json`
- [ ] I have read `policies/submission-policy.md`, `security-policy.md`, and `removal-policy.md`
