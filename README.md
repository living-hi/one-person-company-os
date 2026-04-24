# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

**One Person Company OS v1.0 is a visual operating cockpit for AI-native solo founders.**

It is not a business-plan generator, not a stage tracker, and not a template pack.
It helps one founder keep the real company loop visible:

`promise -> buyer -> product capability -> delivery -> cash -> learning -> asset`

## What Changed In v1.0

v1.0 is a breaking architecture release.

- the state file is now a v1.0 business-loop model, without legacy `stage_id` or `current_round` fields
- the download-first HTML entry is now an operating cockpit, not a markdown wrapper
- every workspace gets deterministic SVG visuals for the business loop and revenue pipeline
- AI image generation is treated as an optional creative layer for covers, launch posts, and visual storytelling
- old round/stage commands now print deprecation guidance instead of creating old semantics

## Workspace Model

Generated workspaces keep three output layers:

- editable markdown work surfaces
- localized HTML reading pages led by the operating cockpit
- numbered DOCX files under `artifacts/` or `产物/` for formal deliverables

Chinese founders get:

- `阅读版/00-经营驾驶舱.html`
- `视觉素材/business-loop.svg`
- `视觉素材/revenue-pipeline.svg`
- `视觉素材/ai-image-prompts.md`

English founders get:

- `reading/00-operating-cockpit.html`
- `visual-kit/business-loop.svg`
- `visual-kit/revenue-pipeline.svg`
- `visual-kit/ai-image-prompts.md`

The hidden machine state stays at `.opcos/state/current-state.json`.

## Runtime Requirements And Safety Boundary

- script mode expects an existing local `Python 3.7+`
- `scripts/ensure_python_runtime.py` prints compatibility and manual install guidance only
- the marketplace build does not auto-install system packages
- generated files stay inside the founder-approved workspace directory
- normal use does not require API keys or unrelated credentials
- AI images are optional creative assets, not a required runtime dependency

## Local Commands

```bash
python3 scripts/preflight_check.py --mode create-company
python3 scripts/ensure_python_runtime.py
python3 scripts/init_business.py "North Star Lab" --path ./workspace --product-name "North Star Assistant" --target-user "independent builders" --core-problem "they need one visible loop for product, revenue, delivery, and cash" --product-pitch "a visual operating cockpit for one-person AI companies" --language en-US --confirmed
python3 scripts/validate_release.py
```

## One-Line Install

```bash
clawhub install one-person-company-os
```

## One-Line Start

```text
I am building a one-person AI company. Use one-person-company-os v1.0. Do not give me a business-plan template. First help me confirm the sellable promise, first buyer, and core problem. Then create the approved local workspace, open with the operating cockpit, show the current bottleneck visually, and save only approved files inside that workspace.
```

## Validation

Run:

```bash
python3 scripts/validate_release.py
```

It validates v1.0 state, localized workspaces, the operating cockpit, visual assets, DOCX-only artifact directories, deprecated round/stage commands, and public release materials.
