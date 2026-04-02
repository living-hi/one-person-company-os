# One Person Company OS

This is not a generic startup prompt. It is a **navigable, persistent, deliverable company operating system** for founders actively building an AI-native solo company.

It unifies four critical objects into one operating layer:

- company definition
- role structure
- current round
- file and runtime state
- artifact documents

## One-Line Install

```bash
clawhub install one-person-company-os
```

## One-Line Start

```text
I am building an AI-native solo company. Use one-person-company-os, do Step 1/5 to Step 3/5 first, give me the company setup draft, and show the three-layer navigation bar, user-navigation view, audit view, save explanation, and runtime explanation before creation.
```

## Best For Founders Who

- have an AI product direction but no clear company structure yet
- keep losing state across long chat threads
- want real persistence instead of advisory-only output
- need one current round, one blocker, and one shortest next move
- want OpenClaw to recover when local scripts or Python versions get in the way

## What You Get

- a company setup draft
- 3 to 5 company name options
- a suggested stage
- a minimal org structure and first active roles
- a Chinese workspace plan
- the first executable round
- a three-layer navigation model
- user-navigation and audit views
- explicit state, save, and runtime explanations
- numbered DOCX deliverables with software/non-software evidence and post-launch deployment materials

## Why It Feels Like A Company OS

- fixed `Step 1/5 -> Step 5/5` execution flow
- fixed `Stage / Round / Current Step` navigation
- split user-navigation and audit reporting
- explicit persistence instead of chat-only output
- preflight checks plus Python recovery
- fallback modes for execution, manual persistence, and chat-only operation
- standard document templates for deliverable output

## Architecture

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

## Local Workflow

```bash
python3 scripts/preflight_check.py --mode create-company
python3 scripts/ensure_python_runtime.py
python3 scripts/init_company.py "北辰实验室" --path ./workspace --product-name "北辰助手" --stage 构建期
python3 scripts/start_round.py ./workspace/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/generate_artifact_document.py ./workspace/北辰实验室 --title "Homepage Hero Spec" --category software
python3 scripts/checkpoint_save.py ./workspace/北辰实验室 --reason "end of current session"
python3 scripts/validate_release.py
```

## Core Positioning

Turn a founder into a fast-moving AI-native solo company operating system.
