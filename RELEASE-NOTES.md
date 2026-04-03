# Release Notes

## v0.5.6 - Founder Intake And Placeholder Deliverable Control

`v0.5.5` improved the storefront hook.

`v0.5.6` improves the actual founder experience and artifact discipline during real use.

The gap was no longer positioning alone.
It was that first-run interaction still asked too much of the founder, and the workspace still did not make pending vs completed deliverables obvious enough.

This release adds:

- proactive founder intake from a one-line idea, with 3 to 4 suggested directions when the founder is still undecided
- a new `10-创始人启动卡.md` so the workspace itself teaches the founder how to reply with low effort
- a new `11-交付状态总览.md` so users can immediately see which DOCX files are pending and which are complete
- placeholder starter deliverables marked with `[待生成]` and automatic promotion to `[已生成]` when a formal artifact is generated
- review-path and improvement reminders in every runtime report
- stricter validation against legacy unnumbered artifact folders and outdated deliverable naming

The product now behaves more like a serious control board:

- lighter founder input at the start
- clearer output visibility during execution
- stronger formal-deliverable discipline throughout the workspace lifecycle

## v0.5.5 - Outcome-Driven Storefront Hook

This patch release makes the ClawHub storefront more compelling.

The previous summary was cleaner, but still mostly descriptive.
This version shifts the opening line to an outcome:

- start from one AI product idea
- end with a run-ready solo company

This release updates:

- the `SKILL.md` public summary
- the ClawHub listing short description

No runtime behavior changes are included in this patch.

## v0.5.4 - ClawHub Summary Compression

This patch release shortens the public storefront summary.

The product surface was already in the right order, with English first and Chinese second.
The remaining issue was card-level length: the English sentence still took too much room, so the Chinese half was cut off too early in ClawHub previews.

This release fixes that by:

- replacing the long storefront summary with a shorter English hook
- keeping the same Chinese value proposition in a more compact form
- aligning the ClawHub listing short description with the new compressed summary

## v0.5.3 - English-First Storefront Polish

This patch release improves the public-facing storefront for both GitHub and ClawHub.

The runtime and generated materials were already bilingual.
The remaining weak point was presentation:

- the English README still showed too many raw Chinese workspace paths without enough English framing
- the public `SKILL.md` still read like an internal Chinese-first spec instead of a storefront that English users could scan quickly
- ClawHub-facing copy still exposed Chinese before English in places where English readers were likely to bounce

This release closes that gap by:

- rewriting the GitHub English README sections that describe canonical workspace files
- turning `SKILL.md` into an English-first bilingual storefront while preserving the same operating rules
- reordering ClawHub listing copy and prompts so English users see an immediately understandable product surface

## v0.5.2 - Bilingual Listing Metadata Polish

This patch release fixes the remaining public-surface mismatch after the bilingual runtime upgrade.

The runtime, generated documents, GitHub README, and release materials were already bilingual.
The remaining weak point was the live ClawHub listing summary, which still rendered as Chinese-only metadata.

This release closes that gap by:

- updating `SKILL.md` frontmatter to use a concise Chinese-plus-English description
- making the latest ClawHub listing readable to both Chinese and English users before they even open the repository
- keeping the runtime and packaging behavior unchanged so the patch is safe to ship immediately

## v0.5.1 - Bilingual Runtime And Document Upgrade

This release upgrades `one-person-company-os` from “Chinese-friendly” to “actually bilingual in production use.”

The remaining gap was not core workflow design.
It was language continuity across the real product surface:

- English founders could read the README but still hit Chinese-only runtime output
- generated role briefs and formal deliverables did not fully follow English execution
- public release copy still leaned too hard on a Chinese-only framing

This release closes that gap by adding:

- language-aware runtime reports across the main workflow scripts
- English role localization and English generated workspace content
- English DOCX artifact content generation
- release validation that now checks the English path as well as the Chinese path
- updated GitHub, ClawHub, guide, and release materials for both Chinese and English founders

## v0.5.0 - Numbered DOCX Deliverables and Post-Launch Ops Pack

This release upgrades `one-person-company-os` from “deliverable-aware” to “actually deliverable under audit.”

The remaining gaps were practical:

- artifacts still produced too many markdown-like forms instead of one formal output
- software or non-software runs could look “busy” without leaving clear real deliverables
- launch-stage work could miss deployment or production materials because the default role/output set was too light

This release closes those gaps by adding:

- numbered `.docx` outputs only inside `产物/`
- a built-in DOCX writer so the workspace can generate formal deliverables without extra tooling
- starter deliverable packs for actual outputs, software/code evidence, and non-software deliverables
- automatic deployment, rollback, monitoring, and production materials for launch and later stages
- explicit stage-role and deliverable matrices so users can see which roles and outputs must exist at each stage
- default launch-stage activation of `运维保障` and `用户运营`
- updated validation so release checks now assert numbered DOCX artifacts and launch-stage ops materials

## v0.4.0 - Navigation UX and Deliverable Document System

This minor release upgrades the product from “state-aware skill” to “navigable and deliverable operating system.”

The main problem was no longer content quality.
It was that founders could still lose orientation inside a long run, and key artifacts still depended too much on ad hoc chat formatting.

This release closes that gap by adding:

- a three-layer navigation bar with `阶段 / 回合 / 本次 Step`
- dual-labeled steps with natural-language intent plus system step names
- a split output contract with `用户导航版` and `审计版`
- explicit `本次会做 / 不会做`, `本次变化`, and `回合仪表盘` sections
- user-readable save explanations and runtime explanations instead of terse raw fields alone
- a new `scripts/generate_artifact_document.py` entry point for artifact generation
- three standard artifact forms:
  - `内部工作稿`
  - `标准规范稿`
  - `可转 DOCX 稿`
- built-in workspace templates and a document-output guide so deliverables can be persisted in a standard format
- updated README, release listing copy, and sample outputs to match the upgraded interaction model

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
