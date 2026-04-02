# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

For founders building an AI-native solo company: this is not another startup advice prompt. It is an operating system for turning one product idea into a company draft, a real workspace, a current round, and a repeatable execution loop.

## Built For This Founder Situation

- you have an AI product direction but no clear company structure yet
- your strategy lives in chats and gets lost after a few days
- you want momentum without creating management overhead for yourself
- you need one current stage, one current round, one blocker, and one shortest next move
- you want a system that saves work, reports state, and survives environment issues

## Core Promise

- turn a vague idea into a founder-reviewable company setup draft
- turn that draft into a real Chinese-first workspace after confirmation
- keep the company moving through rounds instead of vague weekly planning
- calibrate only when triggered by blockers, drift, completed outputs, or stage transitions
- recover from Python/runtime issues instead of silently dropping back to pure chat

## What You Get On The First Run

- a one-line product definition
- 3 to 5 company name options
- a suggested current stage
- target user and core problem
- a minimal org structure and first active roles
- a Chinese workspace plan
- the first round you can actually execute
- explicit founder approval items

## Why This Feels More Like A Company OS

- fixed `Step 1/5` to `Step 5/5` execution flow
- fixed `Status / Save / Runtime` reporting
- real persistence instead of chat-only output
- preflight checks that distinguish installed from runnable
- fallback modes for script execution, manual persistence, and chat-only operation
- Python recovery flow that prefers OpenClaw-managed execution

## Start With These Prompts

```text
Use one-person-company-os to help me create a one-person company around an AI product.
Do Step 1/5 to Step 3/5 first, give me the company setup draft, and show the current persistence mode, save status, and runtime status. I will confirm before creation.
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

## What Execution Looks Like

Every real run follows the same five-step state machine:

1. `Step 1/5` Mode selection
2. `Step 2/5` Preflight and persistence strategy check
3. `Step 3/5` Draft / proposed change / current state load
4. `Step 4/5` Execution and persistence
5. `Step 5/5` Verification and reporting

Every major output also includes:

- `Status`
  - current mode, step, stage, round, role, artifact, persistence mode, next action, confirmation need
- `Save Status`
  - whether it was saved, where it was saved, file names, and why it was not saved
- `Runtime Status`
  - `installed`, `runnable`, `python_supported`, `workspace_created`, `persisted`

## Python Recovery

- compatibility target: `Python 3.7+`
- preflight detects the current interpreter, alternative compatible runtimes, and the recovery script
- if the current version is incompatible, OpenClaw should first switch to an existing compatible interpreter
- if no compatible runtime exists locally, OpenClaw should try automatic installation
- if installation is not practical, the agent should finish the script task manually and persist the results

Recovery entry points:

```bash
python3 scripts/ensure_python_runtime.py
python3 scripts/ensure_python_runtime.py --apply
python3 scripts/ensure_python_runtime.py --apply --run-script scripts/preflight_check.py -- --mode create-company
```

## Workspace After Confirmation

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

- `scripts/preflight_check.py`
- `scripts/ensure_python_runtime.py`
- `scripts/init_company.py`
- `scripts/build_agent_brief.py`
- `scripts/start_round.py`
- `scripts/update_round.py`
- `scripts/calibrate_round.py`
- `scripts/checkpoint_save.py`
- `scripts/transition_stage.py`
- `scripts/validate_release.py`

## Validation

```bash
python3 scripts/preflight_check.py --mode create-company
python3 scripts/validate_release.py
```

## Notes

- Chinese is the default for Chinese users, including workspace names and operating language.
- The founder remains the final approver for budget, launch, compliance, and customer-facing actions.
- The system advances in rounds, not in weekly reporting rituals.
