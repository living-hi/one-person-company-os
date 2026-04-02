# One Person Company OS

One Person Company OS is now a Chinese-first operating system for AI-native solo companies.

The new product shape is simple:

- create the company
- start a round
- advance the round
- calibrate only when triggered
- transition stages when the bottleneck changes

## What Makes It Different

- Chinese-first workspace and operating language
- round-based execution instead of week-based management
- minimal role activation instead of role overload
- OpenClaw-first local workflow

## First-Run Promise

The first serious run should produce:

- a company setup draft
- company name options
- a suggested stage
- a minimal role system
- a Chinese workspace plan
- the first executable round

## Local Workflow

```bash
python3 scripts/init_company.py "北辰实验室" --path ./workspace --product-name "北辰助手" --stage 构建期
python3 scripts/start_round.py ./workspace/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/validate_release.py
```

## Core Positioning

Turn one founder into a fast-moving AI-native solo company.
