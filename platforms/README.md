# Platform Adapters

This directory contains distribution adapters for One Person Company OS v1.0.

The canonical package remains the repository root:

- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- `agents/`

Adapters in this directory translate that canonical package into platform-specific surfaces.

## Adapter Types

- `claude-skill/`: Claude Skills compatible package notes.
- `mcp-server/`: local stdio MCP server that exposes core workspace tools.
- `hermes-agent/`: Hermes Agent skill and MCP configuration.
- `openai-gpt/`: Custom GPT instructions and optional Actions schema.
- `dify-plugin/`: Dify plugin submission draft.
- `poe-bot/`: Poe bot prompt package.
- `gemini-gem/`: Gemini Gem instruction package.
- `github-copilot-extension/`: GitHub Copilot Extension manifest draft.
- `microsoft-copilot-studio/`: Microsoft Copilot Studio agent draft.

## Publishing Rule

Do not mark a platform as published unless one of these is true:

- the CLI/API returned a successful publish response
- the platform page or version API shows the target version
- the downloadable package contains the target files

If a platform requires a browser session, account approval, paid plan, API key, or organization admin approval, keep it marked as `ready-to-submit`.
