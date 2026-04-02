# Release Notes

## v0.3.3 - README Professionalization and Architecture Clarity

This patch release sharpens the public product surface.

The goal is simple: a founder should be able to open the README and understand in under a minute:

- what this system is
- what architecture it uses
- why it is more professional than a generic startup prompt
- how to install it in one line
- how to start it in one line

This release includes:

- a full rewrite of the main README information architecture
- a clearer architecture section for the system layers
- a stronger, more professional product definition
- one-line install and one-line start sections
- aligned release README, ClawHub listing, and agent metadata

## v0.3.2 - State Transparency and Runtime Recovery

This patch release makes the skill behave more like a real company operating system and less like an endless advisory prompt.

This release includes:

- fixed `Step 1/5 -> Step 5/5` execution reporting across preflight, workspace creation, round start, round update, calibration, checkpoint save, and stage transition
- explicit save reporting that states whether content was saved, where it was saved, which files were written, and why content remained chat-only
- a new `scripts/preflight_check.py` entry point for environment checks and mode selection
- a new `scripts/checkpoint_save.py` entry point for saving recoverable company checkpoints
- a new `scripts/ensure_python_runtime.py` entry point for Python runtime discovery, install planning, and interpreter switching
- updated runtime reporting that distinguishes `installed`, `runnable`, `python_supported`, `workspace_created`, and `persisted`
- a homepage rewrite and release-copy rewrite that target founders actively building AI-native solo companies

## v0.3.0 - Round-Based Solo Company OS

This release is a full V2 rewrite of the skill.

The product is no longer organized around weekly review and heavy startup documentation. It is now organized around:

- create the company
- start a round
- advance the round
- calibrate only when triggered
- transition stages when the bottleneck changes

This release includes:

- a rewritten `SKILL.md` centered on five clear user intents
- a Chinese-first workspace with Chinese file names and operating language by default
- a new `总控台` role and a smaller default starter role set
- new scripts for round start, round update, calibration, and stage transition
- rewritten references, templates, sample outputs, and release materials
- removal of the old weekly review flow, the legacy role/workflow references, and the previous bilingual SaaS example pack

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
