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

- lightweight founder intake from a single-sentence idea
- 3 to 4 startup directions when the founder is still undecided
- a company setup draft
- a one-line product definition
- 3 to 5 company name options
- a suggested stage
- target user and core problem
- a minimal org structure and starter role set
- a language-aware workspace plan
- the first round you can execute in 2 to 3 hours
- explicit founder approval items
- explicit save status and runtime status

After confirmation, it continues with:

- a persisted workspace
- current-round files
- role briefs
- calibration records
- checkpoint records
- English content and runtime reports for English prompts
- Chinese content and runtime reports for Chinese prompts

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

1. `Step 1/5 Decide which flow this run should enter [Mode selection]`
2. `Step 2/5 Confirm environment, persistence conditions, and execution path [Preflight and persistence strategy check]`
3. `Step 3/5 Load current state, then prepare the draft or proposed change [Draft / proposed change / current state load]`
4. `Step 4/5 Execute and write the result into the workspace [Execution and persistence]`
5. `Step 5/5 Verify the result, explain changes, and report back [Verification and reporting]`

This is part of the product contract, not presentation fluff.

## Default Output Contract

Every major operation now reports two views.

### 1. User Navigation View

- three-layer navigation bar
  - stage
  - round
  - current step
- what this run will do / will not do
- what changed this time
- round dashboard
- save explanation
- runtime explanation

### 2. Audit View

- status
- save status
- runtime status

This means users can read the system at a glance without losing the deeper technical audit trail.

## Three-Layer Navigation And Round Dashboard

The navigation model is now explicit:

- `Stage`
  - shows whether the company is in validation, build, launch, operate, or grow
- `Round`
  - shows the single current round being advanced
- `Current Step`
  - shows whether this output is selecting mode, checking preflight, loading state, writing files, or reporting

The round dashboard always surfaces:

- current stage
- current round
- round status
- current owner
- current artifact
- current blocker
- shortest next action
- completion criteria

## Numbered DOCX Deliverables

Key artifacts no longer exist as loose markdown drafts.

The default contract is now:

- every formal artifact inside the canonical `产物/` (`Artifacts`) directory is a numbered `.docx`
- software work must leave real code, config, script, interface, or automation evidence
- non-software work must leave real deliverables instead of chat-only summaries
- launch and post-launch stages must include deployment and production materials

For English users, the content and runtime output switch to English, but the on-disk canonical filenames stay stable for automation.

After workspace initialization, the system creates three clear file groups.

### Root Navigation Files

- artifact output spec: `07-文档产物规范.md`
- stage-role deliverable matrix: `08-阶段角色与交付矩阵.md`
- current-stage delivery requirements: `09-当前阶段交付要求.md`
- founder start card: `10-创始人启动卡.md`
- deliverable status overview: `11-交付状态总览.md`

### Formal Deliverable Starter Files

- formal deliverable template: `产物/00-交付模板/01-[待生成]正式交付文档模板.docx`
- actual deliverables index: `产物/01-实际交付/01-[待生成]实际产出总表.docx`

### Stage-Dependent Operational Files

- when the stage requires it, the workspace also auto-adds the matching starter docs under `产物/04-部署与生产/` and `产物/05-上线与增长/`

Starter deliverables land as `[待生成]` placeholder DOCX files so the founder can see the full formal output plan immediately. Once a deliverable is formally produced, it switches to `[已生成]`.

To generate artifact documents directly:

```bash
python3 scripts/generate_artifact_document.py <company-workspace-dir> --title "Artifact Title" --category software
```

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
  core overview docs
  role agents/
  process guides/
  artifacts/
  records/
  automation/
```

Canonical root files on disk remain:

- company overview: `00-公司总览.md`
- product positioning: `01-产品定位.md`
- current stage: `02-当前阶段.md`
- org structure: `03-组织架构.md`
- current round: `04-当前回合.md`
- execution rules: `05-推进规则.md`
- trigger and calibration rules: `06-触发器与校准规则.md`
- artifact output spec: `07-文档产物规范.md`
- stage-role deliverable matrix: `08-阶段角色与交付矩阵.md`
- current-stage delivery requirements: `09-当前阶段交付要求.md`

Core design rules:

- one company has one current state
- one stage has one dominant bottleneck
- one moment has one current round
- one round must have one artifact, one blocker, and one shortest next action
- every meaningful reply should say where to review the latest output and how to tighten it further

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
I am building an AI-native solo company. Use one-person-company-os. Do not make me fill a big form first. Ask for the idea in one sentence, or give me 3 to 4 directions to pick from. Then do Step 1/5 to Step 3/5, give me the company setup draft, and tell me whether anything is saved plus which path I should open next.
```

## Recommended Start Prompt

```text
I am building an AI-native solo company. Use one-person-company-os.
Do not make me fill a lot of fields first. Ask for the idea in one sentence, or give me 3 to 4 directions to choose from.
Then do Step 1/5 to Step 3/5, give me the company setup draft,
and tell me whether anything is saved plus which path I should open next.
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
- `scripts/generate_artifact_document.py`
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

- Chinese prompts produce Chinese runtime reports and Chinese generated materials by default
- English prompts produce English runtime reports and English generated materials by default
- the repository keeps a stable canonical workspace structure for automation compatibility, while user-facing content follows the active language
- the founder remains the final approver for budget, launch, compliance, and customer-facing actions
- the system advances in rounds, not weekly reporting rituals
- the first round should be small enough to yield a clear result in 2 to 3 hours
