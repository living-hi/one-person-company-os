# Platform Requirements

## Universal Requirements

- Keep founder approval as the write boundary.
- Do not request unrelated credentials.
- Do not auto-install system packages.
- Persist only inside the founder-approved workspace.
- Keep AI images optional and creative only; deterministic SVG/HTML carries exact operating data.
- First user-facing surface should explain: promise, buyer, product, delivery, cash, learning, asset.

## Account Or Credential Requirements

| Platform | Required Access |
| --- | --- |
| Claude Skills | Claude account with Skills upload/install access |
| OpenAI GPT Store | ChatGPT builder access; verified builder profile for public listing |
| MCP Registry | namespace/publisher auth for official registry |
| Smithery | Smithery account/API key or hosted endpoint |
| Glama | GitHub repo submission or indexing flow |
| PulseMCP | manual/API submission access |
| Hermes Agent | running Hermes instance or agentskills.io-compatible distribution flow |
| Dify Marketplace | Dify marketplace publisher account |
| Poe | Poe creator account |
| Gemini Gems | Gemini account with Gems creation/sharing |
| GitHub Copilot Extensions | GitHub App, webhook backend, Marketplace publisher approval |
| Microsoft Copilot Studio | Microsoft tenant, Copilot Studio license, Teams/Commercial Marketplace approval |

## Versioning

Use the repository release version for all adapters. For this batch:

- package version: `1.0.2`
- Git tag: `v1.0.2`
- canonical commit: see Git tag `v1.0.2`

If adapter-only files change without changing runtime behavior, bump patch version before publishing to marketplaces that require immutable versions.
