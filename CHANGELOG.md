# Changelog

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
