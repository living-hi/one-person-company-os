# Claude Code Runtime Notes

Use this file when the host is Claude Code or another terminal agent runtime that does not natively consume OpenClaw `SKILL.md`.

## Purpose

Treat this repository as a role-aware operating system for a solo SaaS founder.

The core behavior lives in:
- `SKILL.md`
- `agents/roles/*.json`
- `orchestration/stage-defaults.json`
- `orchestration/handoff-schema.json`
- `scripts/build_agent_brief.py`

## Default Working Rules

- Treat the human user as the founder and final decision-maker.
- Produce artifacts, not just advice.
- Activate only the minimum role set needed for the current bottleneck.
- Mirror the user's working language by default.
- If the user asks in Chinese, draft the operating materials in Chinese unless asked otherwise.
- If the user asks in English, draft the operating materials in English unless asked otherwise.
- Do not claim a delegated agent ran unless the host actually launched one.

## Runtime Flow

1. Infer or confirm the primary stage:
   `Validate`, `Build`, `Launch`, `Operate`, or `Grow`
2. Read `orchestration/stage-defaults.json` to identify the default role set for that stage.
3. Narrow the activated roles to the smallest set needed for the task.
4. Read the matching files in `agents/roles/` for machine-readable role contracts.
5. When delegation is supported, generate a role brief with `scripts/build_agent_brief.py` before assigning work.
6. Keep handoffs consistent with `orchestration/handoff-schema.json`.
7. End with a reusable artifact pack and continuation context.

## When To Delegate

Delegate only when the host actually supports sub-agents and delegation will materially improve execution.

Good delegation candidates:
- Product scope definition
- Architecture planning
- Launch copy drafting
- Weekly review synthesis
- Funnel or metric diagnosis

Do not delegate:
- Founder approvals
- Legal certainty
- Production actions without explicit approval
- Any action the host cannot actually execute

## Output Contract

Prefer this response structure:

```md
## Session Frame
- Stage:
- Working language:
- Bottleneck:
- Success criterion:

## Activated Roles
- role:
  owner:
  output:

## Artifact Pack
- artifact:

## Approval Gates
- gate:

## Next Actions
- action:
```

When delegation is used, append a short continuation context that the next role can consume without rebuilding context.
