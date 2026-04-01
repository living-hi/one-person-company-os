# Agent Runtime Guide

This repository supports role-aware execution across terminal agent hosts such as Codex, Claude Code, and compatible OpenClaw runtimes.

## Core Files

- `SKILL.md`: primary OpenClaw and Codex-facing skill behavior
- `agents/openai.yaml`: OpenClaw-compatible UI metadata
- `agents/roles/*.json`: machine-readable role contracts
- `orchestration/stage-defaults.json`: default role activation by stage
- `orchestration/handoff-schema.json`: required handoff fields
- `scripts/build_agent_brief.py`: generate role packets for delegated work

## Stage Model

Use one primary stage per session:
- `Validate`
- `Build`
- `Launch`
- `Operate`
- `Grow`

Secondary stages are allowed only when they materially change the required outputs.

## Role Activation Rules

- Activate the smallest role set that can move the bottleneck.
- Keep one owner per output.
- Reuse the same role ids from `agents/roles/*.json`.
- If the host does not support sub-agents, simulate the role workflow in one response.

## Handoff Contract

Every role handoff should preserve:
- stage
- working language
- objective
- company name
- inputs
- required outputs
- constraints
- approval gates
- handoff targets
- continuation context

Use `orchestration/handoff-schema.json` as the source of truth.

## Brief Generation

Single role:

```bash
python3 scripts/build_agent_brief.py --stage Build --role engineer-tech-lead --language zh-CN --company-name "My Company" --objective "Turn the PRD into an implementation plan" --current-bottleneck "Scope is defined but delivery is still ambiguous" --next-required-artifact "sprint-plan.md" --input 03-prd.md
```

Stage default role set:

```bash
python3 scripts/build_agent_brief.py --stage Launch --all-stage-roles --language en --company-name "My Company" --objective "Prepare the launch pack" --current-bottleneck "Messaging is not synchronized with onboarding" --next-required-artifact "launch-brief.md" --output-dir ./workspace/my-company/agent-briefs
```

## Language Rules

- Chinese prompt in: Chinese artifact drafts out by default
- English prompt in: English artifact drafts out by default
- Bilingual output only when explicitly requested
- Preserve names, URLs, legal entities, and code identifiers in original form when translation would reduce accuracy
