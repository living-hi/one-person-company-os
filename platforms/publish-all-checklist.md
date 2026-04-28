# Publish-All Checklist

## Before Any Publish

- Run `python3 scripts/validate_release.py`.
- Run `python3 scripts/validate_platforms.py`.
- Confirm `git status --short` is clean or only contains intended changes.
- Confirm `README.md`, `README.zh-CN.md`, and `SKILL.md` match the target version.

## Directly Automatable

- GitHub push and tags.
- ClawHub publish and download verification.
- Local MCP adapter smoke test.

## Requires Account Or Browser Approval

- Claude Skills upload/install.
- OpenAI GPT Store creation and public listing.
- Smithery / Glama / PulseMCP submissions.
- Dify Marketplace plugin submission.
- Poe bot creation.
- Gemini Gem sharing.
- GitHub Copilot Extension marketplace listing.
- Microsoft Copilot Studio and Teams/Commercial Marketplace publishing.

## Evidence To Capture

- public listing URL
- version number
- package hash or download URL
- key file check
- security scan result
- rejection reason if any
