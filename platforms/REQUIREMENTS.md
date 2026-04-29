# Platform Requirements

Target adapter version: `1.0.2`

## Universal Requirements

- Keep founder approval as the write boundary.
- Do not request unrelated credentials.
- Do not auto-install system packages.
- Persist only inside the founder-approved workspace.
- Keep AI images optional and creative only; deterministic SVG/HTML carries exact operating data.
- First user-facing surface should explain: promise, buyer, product capability, delivery, cash, learning, asset.
- Do not mark a market `published` without a visible listing, version API, downloadable package, or review record.

## Mainstream Push List

| Channel | Required access | Execution model | Publication status rule |
| --- | --- | --- | --- |
| OpenClaw / ClawHub | ClawHub publisher access | local skill package | published only after API/download/scan verification |
| Claude Skills | Claude account with Skills upload/install access | local skill or prompt skill | published only after the skill is installed, uploaded, or shareable |
| OpenAI GPT Store | ChatGPT builder access; verified builder profile for public listing | prompt-only GPT or GPT Actions over HTTPS | published only after the GPT Store/share page is visible |
| MCP Registry | publisher namespace/auth | stdio MCP server package | published only after registry listing or API record is visible |
| Smithery | Smithery account/API key or hosted endpoint | MCP server package or hosted MCP endpoint | published only after Smithery listing is visible |
| Glama | GitHub repo submission or indexing flow | MCP server package indexed from repo | published only after Glama listing is visible |
| PulseMCP | manual/API submission access | MCP server package metadata | published only after PulseMCP listing is visible |
| Hermes Agent / agentskills.io | running Hermes instance or agentskills.io-compatible distribution access | Hermes skill plus MCP adapter | published only after install/listing evidence is captured |
| Dify Marketplace | Dify marketplace publisher account | Dify plugin package | published only after review/listing evidence is captured |
| GitHub Copilot Extensions | GitHub App, webhook backend, Marketplace publisher approval | hosted backend extension | keep `backend-needed` until public backend exists |
| Microsoft Copilot Studio / Commercial Marketplace | Microsoft tenant, Copilot Studio license, Teams/admin approval, marketplace publisher account | tenant agent plus optional Teams/Commercial Marketplace app | keep `tenant-needed` until tenant and publisher access exist |
| Poe Bots | Poe creator account | prompt bot | published only after public/shareable bot URL exists |
| Gemini Gems | Gemini account with Gems creation/sharing | prompt Gem | published only after share/public URL or account-visible record exists |

## Versioning

Use the repository release version for all adapters. For this batch:

- package version: `1.0.2`
- Git tag: `v1.0.2`
- canonical commit: see Git tag `v1.0.2`

If adapter-only files change without changing runtime behavior, bump the patch version before publishing to marketplaces that require immutable package versions.
