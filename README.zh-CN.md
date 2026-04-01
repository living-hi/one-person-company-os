# One Person Company

[English](./README.md) | [简体中文](./README.zh-CN.md)

One Person Company 帮一个 solo founder 把 solo SaaS 经营得像一家真正的公司。

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

## 仓库包含什么

- `SKILL.md`：技能行为和操作规则
- `LICENSE`：MIT 许可证
- `CHANGELOG.md`：版本变更记录
- `RELEASE-NOTES.md`：首个公开版本说明
- `PUBLISHING.md`：独立发布到 GitHub 的步骤
- `SECURITY.md`：安全与责任边界说明
- `references/`：角色卡、生命周期模式、市场说明、工作流和产物模板
- `assets/templates/`：可复用模板
- `assets/examples/`：全球双语 SaaS 示例输出
- `scripts/init_company.py`：初始化公司工作区
- `scripts/weekly_review.py`：生成每周复盘
- `agents/openai.yaml`：兼容 agent 界面的展示元信息

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
- `scripts/`：本地辅助脚本
- `references/`：扩展技能时用的参考资料
- `PUBLISHING.md`：独立 GitHub 仓库发布流程
