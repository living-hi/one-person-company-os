# One Person Company OS

One Person Company OS helps a solo founder run a solo SaaS like a real company.

Instead of giving you a pile of prompts, it gives you a practical operating layer: role ownership, stage-aware workflows, reusable artifacts, weekly review rhythm, and clear approval boundaries.

The first run should produce real working documents such as a company charter, ICP card, offer sheet, MVP scope, launch brief, or weekly review. It is built for global execution, with Chinese and English treated as first-class markets.

## Best Fit

- solo SaaS founders
- indie hackers shipping paid products
- independent developers turning a product into a business
- founder-led micro-teams that still operate like one decision-maker

## What You Get Fast

- a clear company setup instead of vague founder advice
- stage-aware execution for `Validate`, `Build`, `Launch`, `Operate`, and `Grow`
- reusable artifacts like PRDs, ICP cards, launch briefs, dashboards, and weekly reviews
- explicit AI roles with ownership and handoffs
- bilingual execution logic for Chinese and English markets without forking the whole business

## Language Behavior

- if you prompt in Chinese, the skill should draft the materials in Chinese by default
- if you prompt in English, the skill should draft the materials in English by default
- bilingual output should only happen when you ask for it explicitly
- shared strategy and market-facing materials can use different languages when needed

## Quick Start

Use these prompts directly:

```text
使用 $one-person-company-os 帮我搭建一个 solo SaaS 公司。请直接产出 company charter、ICP、offer sheet、MVP scope 和 weekly operating rhythm，全部用中文写。
```

```text
Use $one-person-company-os to set up my solo SaaS company. I want a charter, ICP, offer sheet, MVP scope, and weekly operating rhythm.
```

```text
Use $one-person-company-os as my Chief of Staff and Product Strategist. We are in Validate mode. Produce an ICP card, offer sheet, pricing hypothesis, and validation plan.
```

```text
Use $one-person-company-os. We are in Build mode for a B2B AI SaaS. Produce a PRD, sprint plan, architecture note, and release checklist.
```

```text
Use $one-person-company-os. We are in Launch mode. Produce a launch brief, landing page outline, onboarding outline, FAQ, and a 2-week launch checklist.
```

```text
Use $one-person-company-os to run my weekly review. Summarize wins, losses, metrics, blockers, and the next 5 actions for this week.
```

## What Makes It Different

- not generic startup advice
- not roleplay prompt theater
- not a single-function skill limited to only product or only sales
- not "translate the English page into Chinese" disguised as global strategy

This skill is designed to hold one shared company core while localizing the go-to-market layer where markets actually differ:

- positioning
- landing pages
- channel strategy
- sales scripts
- support surfaces
- market assumptions

## Included

- publishable `SKILL.md`
- role references across founder, chief of staff, product, design, engineering, QA, DevOps, growth, support, finance, legal, data, content, and community
- workflow references for idea to MVP, build to launch, launch motion, lead to close, feedback loops, and weekly rhythm
- reusable document templates
- setup and weekly review scripts
- a sample global bilingual SaaS example pack

## Local File Workflow

The skill ships with two helper scripts:

- `scripts/init_company.py` scaffolds a starter company workspace from the templates
- `scripts/weekly_review.py` creates a dated weekly review file

Example:

```bash
python3 scripts/init_company.py "My Company" --path ./workspace --mode saas
python3 scripts/weekly_review.py ./workspace/my-company --week-of 2026-03-30
```

## Trust Boundary

This skill is meant to draft and coordinate work, not silently take risky actions.

It should require explicit founder approval before:

- production deployment
- live pricing changes
- legal or compliance claims
- spending budget
- deleting or backfilling live data
- sending customer-facing communication at scale

## Positioning

Turn one founder into a functioning AI-native company.
