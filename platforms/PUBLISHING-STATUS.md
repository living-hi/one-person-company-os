# Publishing Status

Updated: 2026-04-28

| Platform | Status | Version | Evidence | Blocker |
| --- | --- | --- | --- | --- |
| ClawHub / OpenClaw | published | 1.0.2 | ClawHub API latest is `1.0.2`; download package verified | none |
| GitHub | published | v1.0.2 | `main` and tag `v1.0.2` point to the release commit | none |
| Claude Skills | ready-to-submit | 1.0.2 | `platforms/claude-skill/` generated | requires Claude account upload/install flow |
| Hermes Agent | ready-to-submit | 1.0.2 | `platforms/hermes-agent/` and MCP config generated | requires Hermes instance or agentskills.io submission flow |
| MCP Registry | ready-to-submit | 1.0.2 | `platforms/mcp-server/server.py` and `server.json` generated | official registry requires publisher auth and final package namespace |
| Smithery | ready-to-submit | 1.0.2 | MCP server package generated | requires Smithery account/API key or hosted endpoint |
| Glama | ready-to-submit | 1.0.2 | MCP server package generated | requires GitHub indexing/submission action |
| PulseMCP | ready-to-submit | 1.0.2 | MCP server package generated | requires manual/API submission |
| OpenAI GPT Store | ready-to-submit | 1.0.2 | `platforms/openai-gpt/` generated | requires ChatGPT builder account; Actions require hosted HTTPS API |
| Dify Marketplace | ready-to-submit | 1.0.2 | `platforms/dify-plugin/` generated | requires Dify marketplace account and packaging review |
| Poe Bots | ready-to-submit | 1.0.2 | `platforms/poe-bot/` generated | requires Poe creator account |
| Gemini Gems | ready-to-submit | 1.0.2 | `platforms/gemini-gem/` generated | requires Gemini account share/publish flow |
| GitHub Copilot Extensions | backend-needed | 1.0.2 | manifest draft generated | requires GitHub App, public backend, Marketplace listing |
| Microsoft Copilot Studio | tenant-needed | 1.0.2 | agent instructions and Teams manifest draft generated | requires Microsoft tenant, Copilot Studio, admin approval |

## Notes

- The MCP adapter is the highest-leverage adapter because Hermes, Claude Desktop, Cursor, VS Code, Codex-style clients, and registry sites can consume it.
- OpenAI GPT Store, Poe, and Gemini Gems should be treated as guided assistant versions unless they are connected to the MCP/API backend.
- Enterprise marketplaces require admin-owned accounts; do not claim publication until the platform shows the public listing.
