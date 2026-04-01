# Release Notes

## v0.2.1 - Release Validation and Publishing Cleanup

This patch release tightens the publishing surface without changing the core positioning of the skill.

This release includes:

- a single-command `scripts/validate_release.py` check for workspace setup, weekly review generation, role-agent brief generation, and release SVG parsing
- a GitHub Actions workflow that reuses the same release validator locally and in CI
- README, publishing, and release-checklist updates so the validation step is part of the default release flow
- `.gitignore` updates for local Codex metadata and tmp-validation output

## v0.2.0 - First Public Release

One Person Company OS is an AI-native operating system for solo founders, with solo SaaS founders as the primary use case.

This release includes:

- a publishable `SKILL.md` with quick-start prompts and explicit language behavior
- role references across founder, product, engineering, QA, DevOps, growth, support, finance, legal, data, content, and community
- workflow references for validation, build, launch, operating rhythm, and feedback loops
- reusable templates for company charter, ICP, offer sheet, PRD, launch brief, dashboard outline, and weekly review
- helper scripts for company setup and recurring weekly reviews
- example outputs for a bilingual global SaaS scenario
- GitHub, ClawHub, and social launch materials

Key behavior:

- strong first-run bias toward artifact creation
- draft-first trust boundary for high-risk actions
- Chinese prompt in -> Chinese output by default
- English prompt in -> English output by default
- bilingual output only when requested
