# MCP Registry Submission

Package: One Person Company OS

Version: 1.0.3

Server:

- transport: stdio
- OCI package: `ghcr.io/living-hi/one-person-company-os-mcp:1.0.3`
- metadata: `platforms/mcp-server/server.json`

Description:

One Person Company OS gives MCP clients a local execution layer for a solo founder's operating cockpit. It supports workspace preflight checks, business initialization, focus updates, artifact generation, and release validation.

Submission requirement:

- GitHub Actions OIDC publisher
- public repository URL
- GHCR OCI package with `io.modelcontextprotocol.server.name` ownership label
- package metadata from `server.json`
- safety statement that all persistent writes stay inside the founder-approved workspace

Published evidence:

- Official MCP Registry API returns `io.github.living-hi/one-person-company-os`.
- `publishedAt=2026-05-06T02:52:00Z`.
- GitHub Actions run `25413862092` completed successfully.
