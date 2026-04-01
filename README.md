# One Person Company

One Person Company is an AI-native operating system for solo founders.

Its primary use case is helping a solo SaaS founder run like a real company by producing concrete operating artifacts, assigning role ownership, and maintaining a lightweight weekly rhythm.

This repository contains the actual skill package: the publishable `SKILL.md`, supporting references, reusable templates, helper scripts, and example assets.

## Core Promise

Turn one founder into a functioning AI-native company.

## Best Fit

- solo SaaS founders
- indie hackers shipping paid software
- independent developers turning a product into a business
- founder-led micro-teams

## First-Run Outcome

A strong first run should produce a starter operating pack such as:

- company charter
- ICP card
- offer sheet
- MVP scope or PRD
- weekly operating rhythm

## Language Behavior

- if the user works in Chinese, the skill should output Chinese materials by default
- if the user works in English, the skill should output English materials by default
- bilingual output should happen only when explicitly requested
- shared company logic can stay in one working language while market-facing materials are localized separately

## Quick Start

Use prompts like these:

```text
使用 $one-person-company 帮我搭建一个 solo SaaS 公司。请直接产出 company charter、ICP、offer sheet、MVP scope 和 weekly operating rhythm，全部用中文写。
```

```text
Use $one-person-company to set up my solo SaaS company. I want a charter, ICP, offer sheet, MVP scope, and weekly operating rhythm.
```

```text
Use $one-person-company. We are in Build mode for a B2B AI SaaS. Produce a PRD, sprint plan, architecture note, and release checklist.
```

```text
Use $one-person-company. We are in Launch mode. Produce a launch brief, landing page outline, onboarding outline, FAQ, and a 2-week launch checklist.
```

```text
Use $one-person-company to run my weekly review. Summarize wins, losses, metrics, blockers, and the next 5 actions for this week.
```

## What The Skill Contains

- `SKILL.md`: the skill behavior and operating rules
- `LICENSE`: MIT license for the repository
- `CHANGELOG.md`: release history
- `RELEASE-NOTES.md`: first public release summary
- `PUBLISHING.md`: standalone GitHub publishing steps
- `SECURITY.md`: responsible-use and disclosure notes
- `references/`: role cards, lifecycle modes, market guidance, workflows, and artifact templates
- `assets/templates/`: reusable starter document templates
- `assets/examples/`: sample outputs for a bilingual global SaaS scenario
- `scripts/init_company.py`: starter workspace scaffolding
- `scripts/weekly_review.py`: recurring weekly review generation
- `agents/openai.yaml`: display metadata for compatible agent surfaces

## Example Workspace

The helper scripts are designed to produce a company workspace like this:

```text
my-company/
  00-company-charter.md
  01-icp-card.md
  02-offer-sheet.md
  03-prd.md
  launches/
    00-launch-brief.md
  reviews/
    weekly-review-template.md
    2026-03-30-weekly-review.md
  decisions/
    decision-log-entry-template.md
  roles/
    role-card-template.md
  metrics/
    dashboard-outline.md
```

## Local File Workflow

Initialize a starter company workspace:

```bash
python3 scripts/init_company.py "My Company" --path ./workspace --mode saas
```

Create a weekly review:

```bash
python3 scripts/weekly_review.py ./workspace/my-company --week-of 2026-03-30
```

## Why It Is Different

- not generic startup advice
- not prompt cosplay
- not limited to one function
- designed for recurring execution instead of one-off setup
- built for Chinese and English market execution without splitting the company core

## Trust Boundary

This skill should draft first and require explicit founder approval before:

- production deployment
- live pricing changes
- legal or compliance claims
- destructive data actions
- budget spend
- customer communication at scale

## Repository Guide

- See `assets/examples/global-saas-cn-en/` for sample outputs
- See `SAMPLE-OUTPUTS.md` for marketing-ready excerpts
- See `scripts/` for local workspace helpers
- See `references/` when extending the skill or reviewing role and workflow behavior
- See `PUBLISHING.md` for the standalone GitHub repo flow
