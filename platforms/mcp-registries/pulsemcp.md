# PulseMCP Submission

Package: One Person Company OS

Version: 1.0.3

Submission summary:

One Person Company OS exposes a workspace-scoped MCP server for solo founders building AI-native businesses. It helps create and update an operating cockpit, generate formal artifacts, and validate the release package.

Metadata:

- transport: stdio
- command: `python3 platforms/mcp-server/server.py`
- OCI package: `ghcr.io/living-hi/one-person-company-os-mcp:1.0.3`
- tools: `preflight_check`, `init_business`, `update_focus`, `generate_artifact_document`, `validate_release`
- repository package version: `1.0.3`

Safety note:

Normal use does not require unrelated credentials. Persistent files stay inside the founder-approved workspace. The package does not auto-install system dependencies.

Submission blocker:

PulseMCP manual/API submission access or downstream sync from the Official MCP Registry. The official registry entry is live, but PulseMCP listing evidence is not visible yet.

Published evidence:

PulseMCP listing URL or API record for this package.
