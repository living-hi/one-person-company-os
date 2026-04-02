# One Person Company OS

One Person Company OS is a Chinese-first control tower for AI-native solo companies.

Start with one product idea. It first gives you a company setup draft, then after founder confirmation it creates the workspace, core role briefs, and the first execution round.

The product loop is simple:

- create the company
- start a round
- advance the round
- calibrate only when triggered
- transition stages when the bottleneck changes

## What It Helps You Do

- turn an idea into an executable solo-company setup
- keep one clear current stage, current round, current blocker, and shortest next move
- move with a minimal role system instead of management overhead
- calibrate only when blocked, drifting, finishing key outputs, or preparing a stage transition

## First-Run Promise

The first serious run should produce:

- a company setup draft
- 3 to 5 company name options
- a suggested stage
- a minimal org structure and first active roles
- a Chinese workspace plan
- the first executable round
- explicit founder approval items

## Local Workflow

```bash
python3 scripts/init_company.py "北辰实验室" --path ./workspace --product-name "北辰助手" --stage 构建期
python3 scripts/start_round.py ./workspace/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/validate_release.py
```

## Core Positioning

Turn one founder into a fast-moving AI-native solo company.
