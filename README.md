# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

One Person Company OS is a Chinese-first operating system for AI-native solo companies.

It is no longer centered on weekly reviews or heavy startup documents. The core loop is now:

- create the company
- start a round
- advance the round
- calibrate only when triggered
- transition stages when the bottleneck changes

## What It Solves

This skill helps one founder run like a company without drowning in management overhead.

It does that by combining:

- a Chinese-first workspace
- a minimal role system
- round-based execution
- trigger-based calibration
- OpenClaw-friendly local scripts and agent briefs

## Main Entry Prompts

```text
我想创建一间一人公司，请帮我调用 one-person-company-os。
主要是打造一个 AI 产品，请你开始。
```

```text
帮我启动当前阶段的第一个推进回合。
```

```text
我卡住了，帮我进入校准回合。
```

```text
帮我判断现在是否应该切换阶段。
```

## Core Modes

- `创建公司`
- `启动回合`
- `推进回合`
- `校准回合`
- `切换阶段`

## Workspace Outcome

The V2 workspace is centered on the current company state and the current round:

```text
公司名/
  00-公司总览.md
  01-产品定位.md
  02-当前阶段.md
  03-组织架构.md
  04-当前回合.md
  05-推进规则.md
  06-触发器与校准规则.md
  角色智能体/
  流程/
  产物/
  记录/
  自动化/
```

## Local Scripts

- `scripts/init_company.py`
- `scripts/build_agent_brief.py`
- `scripts/start_round.py`
- `scripts/update_round.py`
- `scripts/calibrate_round.py`
- `scripts/transition_stage.py`
- `scripts/validate_release.py`

## References

- `references/bootstrap-playbook.md`
- `references/round-execution-playbook.md`
- `references/calibration-playbook.md`
- `references/stage-transition-playbook.md`
- `references/openclaw-runtime.md`
- `references/chinese-workspace-conventions.md`

## Validation

Run:

```bash
python3 scripts/validate_release.py
```

## Notes

- Chinese is the default for Chinese users, including workspace names and daily operating terms.
- The founder remains the final approver for budget, launch, compliance, and customer-facing actions.
- Weekly review is no longer the main loop. Time-based review is only a fallback.
