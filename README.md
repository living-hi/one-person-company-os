# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

One Person Company OS is a Chinese-first control tower for AI-native solo companies.

Start with one product idea. The skill first produces a company setup draft, then after founder confirmation it creates the workspace, core role briefs, and the first execution round.

The core loop is:

- create the company
- start a round
- advance the round
- calibrate only when triggered
- transition stages when the bottleneck changes

## What It Helps You Do

- turn a vague idea into an executable solo-company setup
- keep one clear current stage, current round, current blocker, and shortest next move
- move with a minimal role system instead of management overhead
- calibrate only when blocked, drifting, finishing key outputs, or preparing a stage transition

## What You Get On The First Run

- a one-line product definition
- 3 to 5 company name options
- a suggested current stage
- a minimal org structure and first active roles
- a Chinese workspace plan
- the first executable round
- explicit founder approval items

## Start With These Prompts

```text
Use one-person-company-os to help me create a one-person company around an AI product.
Start with a company setup draft. After I confirm it, create the workspace, role briefs, and first round.
```

```text
Start the first execution round for the current stage.
```

```text
Continue the current round and tell me the shortest path forward.
```

```text
I am blocked. Enter a calibration round.
```

```text
Tell me whether I should transition to the next stage now.
```

## Core Modes

- `创建公司`
- `启动回合`
- `推进回合`
- `校准回合`
- `切换阶段`

## What Gets Created After Confirmation

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
