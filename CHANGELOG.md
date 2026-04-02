# Changelog

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
