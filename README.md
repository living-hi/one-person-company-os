# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

**One Person Company OS is a company operating system for AI-native solo founders.**

It is not a business-plan generator, not a generic startup copilot, and not an endless advisory prompt.
Its job is to give a solo founder a professional operating layer for:

- company definition
- role structure
- current round execution
- real workspace persistence
- calibration and checkpointing
- runtime recovery when the local environment is not ready

## One-Line Positioning

Turn one AI product idea into a runnable, persistent, state-aware solo company operating system.

## Who This Is For

- founders building an AI-native solo company
- operators with a product direction but no clear company structure yet
- people losing context across long chat threads and scattered notes
- users who want a real operating model instead of chat-only startup advice

## What Problem It Solves

The real problem is usually not lack of ideas.
It is lack of system.

Typical failure modes:

- too much output, unclear state
- useful artifacts, unclear persistence
- no single current round
- no standard operating structure
- scripts fail and the workflow collapses back into pure chat

One Person Company OS is designed to solve that category of problem.

## What You Get

On a serious first run, the system should produce:

- a company setup draft
- a one-line product definition
- 3 to 5 company name options
- a suggested stage
- target user and core problem
- a minimal org structure and starter role set
- a Chinese-first workspace plan
- the first round you can execute in 2 to 3 hours
- explicit founder approval items
- explicit save status and runtime status

After confirmation, it continues with:

- a persisted workspace
- current-round files
- role briefs
- calibration records
- checkpoint records

## System Architecture

This project is not just a bundle of documents.
It is a layered operating model:

```text
Founder
  ↓
Control Tower / Skill Protocol
  ↓
Round Engine
  ↓
Workspace Persistence Layer
  ↓
Runtime Recovery Layer
```

Layer responsibilities:

1. `Founder`
   - sets direction, approves high-risk actions, remains final decision-maker

2. `Control Tower / Skill Protocol`
   - handles mode selection, step progression, state reporting, and confirmation boundaries

3. `Round Engine`
   - handles stage, current round, blocker, artifact, and shortest next move

4. `Workspace Persistence Layer`
   - makes artifacts real by writing them into the workspace

5. `Runtime Recovery Layer`
   - handles preflight checks, Python compatibility, interpreter switching, install recovery, and OpenClaw takeover

## Standard Operating Model

Every real execution follows the same five-step state machine:

1. `Step 1/5` Mode selection
2. `Step 2/5` Preflight and persistence strategy check
3. `Step 3/5` Draft / proposed change / current state load
4. `Step 4/5` Execution and persistence
5. `Step 5/5` Verification and reporting

This is part of the product contract, not presentation fluff.

## Default Output Contract

Every major operation reports three groups of information.

### 1. Status

- current mode
- current step
- current stage
- current round
- current role
- current artifact
- persistence mode
- next action
- confirmation requirement

### 2. Save Status

- whether it was saved
- where it was saved
- which files were written
- why it was not saved

### 3. Runtime Status

- `installed`
- `runnable`
- `python_supported`
- `workspace_created`
- `persisted`

The goal is simple: users should not need to interrogate the system to understand what happened.

## Execution Modes

- `Mode A: Script execution`
  - use scripts when the environment is runnable
- `Mode B: Manual persistence`
  - write markdown/json directly when scripts are unavailable but the workspace is writable
- `Mode C: Chat-only progression`
  - use chat only when the system should not or cannot write files

Default downgrade path:

- prefer `Mode A -> Mode B`
- use `Mode C` only when writing is blocked or not yet approved

## Workspace Standard

```text
Company/
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

Core design rules:

- one company has one current state
- one stage has one dominant bottleneck
- one moment has one current round
- one round must have one artifact, one blocker, and one shortest next action

## Why It Is More Professional Than A Generic Prompt

- a formal operating protocol instead of free-form output
- explicit persistence boundaries instead of “said equals done”
- runtime recovery instead of silent failure
- round-based execution instead of vague weekly planning
- founder approval boundaries suitable for real business workflows

## One-Line Install

```bash
clawhub install one-person-company-os
```

## One-Line Start

```text
I am building an AI-native solo company. Use one-person-company-os, do Step 1/5 to Step 3/5 first, give me the company setup draft, and show the current persistence mode, save status, and runtime status before creation.
```

## Recommended Start Prompt

```text
I am building an AI-native solo company. Use one-person-company-os.
Do Step 1/5 to Step 3/5 first, give me the company setup draft,
and show the current persistence mode, save status, and runtime status before creation.
```

Common follow-up prompts:

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

## Python Compatibility And Recovery

- compatibility target: `Python 3.7+`
- the system runs preflight first
- if the current interpreter is incompatible, it first tries an existing compatible runtime
- if none exists locally, OpenClaw should try automatic installation
- if installation is not practical, the agent should finish the task manually and persist the output

Recovery entry points:

```bash
python3 scripts/ensure_python_runtime.py
python3 scripts/ensure_python_runtime.py --apply
python3 scripts/ensure_python_runtime.py --apply --run-script scripts/preflight_check.py -- --mode create-company
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
python3 scripts/ensure_python_runtime.py
python3 scripts/validate_release.py
```

## Operating Principles

- Chinese is the default for Chinese users across workspace, filenames, and operating language
- the founder remains the final approver for budget, launch, compliance, and customer-facing actions
- the system advances in rounds, not weekly reporting rituals
- the first round should be small enough to yield a clear result in 2 to 3 hours
