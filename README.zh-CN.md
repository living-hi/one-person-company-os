# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

One Person Company OS 帮一个 solo founder 把 solo SaaS 经营得像一家真正的公司。

它不是一堆 Prompt，也不是泛泛的创业建议，而是一层可执行的公司操作系统：角色分工、阶段化工作流、可复用文档、周复盘节奏，以及清晰的审批边界。

这个仓库包含技能本体：可发布的 `SKILL.md`、参考资料、模板、辅助脚本和示例资产。

## 核心承诺

把一个创始人升级成一家公司。

## 最适合谁

- solo SaaS founder
- 正在做付费软件的 indie hacker
- 想把“一个产品”升级成“一个业务”的独立开发者
- 仍然以创始人为核心决策者的微型团队

## 首次使用会得到什么

一次像样的首轮调用，应该直接产出一套 starter operating pack，例如：

- company charter
- ICP card
- offer sheet
- MVP scope 或 PRD
- weekly operating rhythm

## 语言行为

- 用户用中文调用时，默认输出中文材料
- 用户用英文调用时，默认输出英文材料
- 只有用户明确要求时，才输出双语版本
- 共享战略文档和面向市场的材料，可以按需要采用不同语言

## 快速开始

可以直接这样调用：

```text
使用 $one-person-company-os 帮我搭建一个 solo SaaS 公司。请直接产出 company charter、ICP、offer sheet、MVP scope 和 weekly operating rhythm，全部用中文写。
```

```text
Use $one-person-company-os to set up my solo SaaS company. I want a charter, ICP, offer sheet, MVP scope, and weekly operating rhythm.
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

## 仓库包含什么

- `SKILL.md`：技能行为和操作规则
- `CLAUDE.md`：给 Claude Code 一类终端智能体看的运行入口
- `AGENTS.md`：宿主无关的 role-agent 编排说明
- `LICENSE`：MIT 许可证
- `CHANGELOG.md`：版本变更记录
- `RELEASE-NOTES.md`：首个公开版本说明
- `PUBLISHING.md`：独立发布到 GitHub 的步骤
- `SECURITY.md`：安全与责任边界说明
- `references/`：角色卡、生命周期模式、市场说明、工作流和产物模板
- `orchestration/`：给 role agent 用的阶段默认激活规则和 handoff schema
- `assets/templates/`：可复用模板
- `assets/examples/`：全球双语 SaaS 示例输出
- `release/`：GitHub、ClawHub 和社媒发布材料
- `scripts/init_company.py`：初始化公司工作区
- `scripts/build_agent_brief.py`：生成可直接下发给角色 agent 的 brief
- `scripts/weekly_review.py`：生成每周复盘
- `agents/openai.yaml`：兼容 agent 界面的展示元信息
- `agents/roles/`：给兼容 agent runtime 使用的机器可读角色定义

## 示例工作区

辅助脚本会生成类似这样的公司目录：

```text
my-company/
  00-company-charter.md
  01-icp-card.md
  02-offer-sheet.md
  03-prd.md
  launches/
    00-launch-brief.md
  agent-briefs/
  handoffs/
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

## 本地文件工作流

初始化一个 starter company workspace：

```bash
python3 scripts/init_company.py "My Company" --path ./workspace --mode saas
```

生成某周 weekly review：

```bash
python3 scripts/weekly_review.py ./workspace/my-company --week-of 2026-03-30
```

生成某个角色的 agent brief：

```bash
python3 scripts/build_agent_brief.py --stage Build --role engineer-tech-lead --language zh-CN --company-name "My Company" --objective "把 PRD 变成 implementation plan" --current-bottleneck "范围已经确定，但交付路径仍不清晰" --next-required-artifact "sprint-plan.md" --input 03-prd.md
```

批量生成某个阶段的默认角色 brief：

```bash
python3 scripts/build_agent_brief.py --stage Launch --all-stage-roles --language en --company-name "My Company" --objective "Prepare the launch pack" --current-bottleneck "Messaging is not synchronized with onboarding" --next-required-artifact "launch-brief.md" --output-dir ./workspace/my-company/agent-briefs
```

在本地运行仓库自带的发布验证：

```bash
python3 scripts/validate_release.py
```

## 它为什么不一样

- 不是创业鸡汤
- 不是 prompt cosplay
- 不是只解决一个职能的单点工具
- 面向持续经营，而不是只做第一天的 setup
- 支持中英文市场执行，而不是把公司内核拆成两套系统

## 信任边界

这个技能默认应该先出草稿，而不是静默替创始人做高风险动作。

以下动作应当要求创始人明确确认：

- 生产环境部署
- 修改线上定价
- 法务或合规表述
- 删除或回填线上数据
- 花预算
- 大规模发送面向客户的内容

## 仓库导航

- `assets/examples/global-saas-cn-en/`：示例输出
- `SAMPLE-OUTPUTS.md`：可直接用于营销展示的片段
- `release/`：ClawHub 上架文案、社媒文案和发布视觉素材
- `scripts/`：本地辅助脚本
- 发布前运行 `python3 scripts/validate_release.py`
- `references/`：扩展技能时用的参考资料
- `CLAUDE.md`：从 Claude Code 使用仓库时先看这里
- `AGENTS.md`：适配其他 agent 宿主时先看这里
- `PUBLISHING.md`：独立 GitHub 仓库发布流程
