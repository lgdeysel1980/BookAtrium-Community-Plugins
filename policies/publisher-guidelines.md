# Publisher guidelines

Practical standards for developers who want a plugin listed in the BookAtrium Community Plugins registry.

## Repository naming and visibility

- Keep plugin **source** in a **public** GitHub repository you control.
- Use a clear repository name (for example `BookAtrium-MyPlugin` or `myplugin-bookatrium`).
- Do not imply official BookAtrium or PractiCore ownership unless you are an authorised maintainer of those projects.
- Document build and test steps in the repository README.

## README expectations

Your plugin README should include:

- What the plugin does
- Supported BookAtrium / Plugin API versions
- Licence
- Install notes (Community Plugins listing vs local `.bookapp-plugin` install)
- Configuration summary
- Privacy / network behaviour
- Support contact (`supportUrl` or Issues)

## Licence

- Dual-publish a clear OSS or other licence in the plugin repository.
- Declare the same licence in the registry entry (`license` / SPDX + URL fields as required by schema).
- Ensure dependencies permit redistribution in your `.bookapp-plugin` package.
- The registry’s MIT licence covers registry repository content and validation scripts only; it does **not** relicense your plugin.

## Changelog

- Keep human-readable release notes per GitHub Release.
- Link `changelogUrl` when available.
- Call out breaking changes, new capabilities, and new network hosts.

## Releases

- Publish **immutable** GitHub Releases with fixed tags (`v1.2.3`).
- Attach the exact `.bookapp-plugin` asset used by the registry entry.
- Never use `/releases/latest/download/` in registry metadata.
- Do not replace assets on an existing tag after the registry lists that URL; cut a new version instead.

## Semantic versioning

- Use SemVer for plugin versions.
- Breaking behaviour or capability removals → major bump when practical.
- Keep the registry `version` identical to the package manifest version.

## Stable plugin ID

- Choose a reverse-DNS id you will not abandon (`com.yourorg.feature`).
- Keep the id stable forever across updates.
- Do not use reserved prefixes: `bookatrium.*`, `bookapplication.*`, `builtin.*`.
- Do not impersonate other publishers’ namespaces.

## Contracts and packaging

1. Reference **`BookAtrium.PluginContracts`** only (no host UI stacks).
2. Implement a supported plugin type interface for Plugin API **1.1** (or a host-supported API).
3. Produce packages with **`BookAtrium.PluginPackager`**.
4. Validate the package with host install locally before submitting.
5. Compute **SHA-256** of the exact release asset bytes.
6. Record exact **sizeBytes**.

## Capabilities and network hosts

- Declare only capabilities your plugin actually uses.
- When declaring network access, list every outbound host the plugin needs.
- Do not omit hosts and then contact them at runtime.
- For **Store** plugins, comply with retailer terms and user expectations around purchases/accounts.
- For **Metadata Source** plugins, comply with website/API terms; **do not** undisclosed scrape in violation of terms or robots rules.

## Configuration, logging, and privacy

- Prefer settings schemas over hidden side channels.
- Do not collect personal data without disclosure.
- Do not include hidden telemetry.
- Do not disable TLS validation.
- Do not ship credentials, API keys, or private certificates inside packages.
- Log responsibly; avoid secrets in logs.

## Support

- Provide a working `supportUrl`.
- Support your users for plugin-specific failures.
- Point BookAtrium application bugs to https://github.com/lgdeysel1980/BookAtrium/issues.
- Point listing problems to the registry Issues (once published).
- Do not tell users to contact private development repositories.

## Deprecation

- When retiring a plugin, open a registry PR marking it deprecated and naming a replacement when possible.
- Keep critical security fixes available or clearly blocked.

## Ownership transfer

If the GitHub repository or publisher identity changes:

1. Open a registry Issue or PR of type **ownership transfer**
2. Prove control of both old and new homes when requested
3. Update `publisher`, `repositoryUrl`, and support links
4. Disclose the transfer clearly in the PR template

## Security response

- Monitor your repository’s security advisories.
- If a listed release is compromised, cut a fixed version **and** request a registry block of bad versions immediately via Private Vulnerability Reporting / urgent PR.
- Cooperate with registry maintainers on disclosure timing.

## Store and metadata-source extras

### Store plugins

- Honour retailer developer/API terms.
- Do not facilitate unauthorised downloading of paid content.
- Be transparent about authentication and purchase redirects.

### Metadata Source plugins

- Document the upstream APIs or sites you query.
- Respect rate limits and terms of use.
- No undisclosed scraping policy violations.

## Submission quick path

1. Public repo + contracts + tests
2. Package + immutable Release
3. SHA-256 + size
4. `plugins/{id}.json` PR (+ regenerated index)
5. Pass CI; wait for review

See also: `submission-policy.md`, root `CONTRIBUTING.md`, and `templates/submission-checklist.md`.
