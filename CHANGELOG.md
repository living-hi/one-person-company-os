# Changelog

## v0.5.0 - 2026-04-03

- replaced the old three-form artifact model with numbered `.docx` deliverables inside `产物/`
- added real DOCX generation in `scripts/common.py` and upgraded `scripts/generate_artifact_document.py` to emit numbered files only
- added workspace starter deliverables for actual output tracking, software/code evidence, non-software deliverables, and post-launch deployment/production materials
- added `08-阶段角色与交付矩阵.md` and `09-当前阶段交付要求.md` so role activation and required outputs are explicit
- promoted `devops-sre` and `customer-success` into the default launch-stage role set to ensure上线后资料不缺位
- upgraded release validation to assert numbered DOCX artifacts, launch-stage ops docs, and the expanded launch role pack
- added language-aware runtime reports, role briefs, and generated documents so Chinese prompts produce Chinese materials and English prompts produce English materials
- updated README, ClawHub copy, and release docs to position the project as bilingual rather than Chinese-only

## v0.4.0 - 2026-04-03

- upgraded the interaction contract from plain step reporting to a two-view output system with `用户导航版` and `审计版`
- added a three-layer navigation bar across the workflow so every major operation now surfaces `阶段 / 回合 / 本次 Step`
- changed `Step 1/5 -> Step 5/5` from system-only labels to dual labels with natural-language intent plus system step names
- added explicit `本次会做 / 不会做`, `本次变化`, and `回合仪表盘` sections to the runtime report layer
- replaced terse save/runtime reporting with user-readable save explanations and runtime explanations
- added `scripts/generate_artifact_document.py` to generate standard artifact outputs
- added three standard artifact forms: `内部工作稿`, `标准规范稿`, and `可转 DOCX 稿`
- added workspace artifact templates and `07-文档产物规范.md` so document delivery is built into the workspace instead of left to ad hoc chat output
- updated README, release copy, sample outputs, and agent metadata to reflect the new navigation and document model

## v0.3.3 - 2026-04-02

- rewrote the repository README to explain the product as a professional, state-driven company operating system instead of a generic prompt
- added explicit architecture framing so users can immediately understand the system layers and operating model
- added one-line install and one-line start entry points for faster onboarding
- aligned release READMEs, ClawHub listing copy, and agent metadata with the sharper positioning

## v0.3.2 - 2026-04-02

- added fixed `Step 1/5 -> Step 5/5` progress reporting plus default `状态栏 / 保存状态 / 运行状态` output across the workflow
- made persistence explicit by reporting whether artifacts were saved, where they were saved, and why they were not saved
- introduced `scripts/preflight_check.py` for environment checks and clearer separation between `installed`, `runnable`, `workspace_created`, and `persisted`
- introduced `scripts/checkpoint_save.py` for explicit checkpoint persistence during live company operation
- introduced `scripts/ensure_python_runtime.py` to detect compatible runtimes, generate install plans, and let OpenClaw recover from Python incompatibility
- widened helper-script compatibility to older Python environments by removing newer union syntax from runtime-critical paths
- rewrote the main README and release-facing copy to target founders actively building AI-native solo companies instead of generic startup readers

## v0.3.0 - 2026-04-02

- rebuilt the skill around `创建公司 -> 启动回合 -> 推进回合 -> 校准 -> 切阶段`
- made Chinese-first workspace names, file names, role names, and operating language the default for Chinese users
- replaced week-based operating rhythm with round-based execution and trigger-based calibration
- introduced `总控台` as the central coordinating role and reduced the default starter role set
- rewrote the repository references, templates, examples, and release materials to match the V2 product shape
- added new scripts for starting rounds, updating rounds, calibrating rounds, and transitioning stages
- removed the old weekly review script, old role/workflow references, and the legacy bilingual SaaS example pack

## v0.2.1 - 2026-04-01

- added a single-command release validator that checks workspace scripts, agent-brief generation, and release SVG assets
- updated GitHub Actions to run the shared release validator instead of duplicated inline checks
- documented the validation step in the README, publishing guide, PR template, and release checklist
- ignored local Codex metadata and tmp-validation outputs from Git status

## v0.2.0 - 2026-04-01

- narrowed the primary positioning to solo SaaS founders while keeping broader one-person business support
- added quick-start prompts to the skill itself
- emphasized first-run artifact creation instead of theory-heavy responses
- strengthened trust-boundary and approval language
- aligned packaging copy across skill metadata, GitHub materials, and ClawHub listing
- added repository README for direct GitHub publishing
- added Chinese repository README and bilingual navigation
- added in-repo release materials for GitHub, ClawHub, and social launch
- added GitHub validation workflow and contribution templates

## v0.1.0 - 2026-04-01

- initial publishable skill package
- role references across company functions
- lifecycle and workflow references
- reusable templates
- company initialization and weekly review scripts
- global bilingual SaaS example pack
