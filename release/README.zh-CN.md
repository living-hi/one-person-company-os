# One Person Company

One Person Company 帮一个 solo founder 把 solo SaaS 经营得像一家真正的公司。

它不是一堆 Prompt，也不是泛泛的创业建议，而是一层可执行的公司操作系统：角色分工、阶段化工作流、可复用文档、周复盘节奏，以及清晰的审批边界。

第一次使用时，它应该直接产出真实工作文档，比如 company charter、ICP card、offer sheet、MVP scope、launch brief 或 weekly review。它面向全球执行设计，把中文和英文市场都当作一级市场。

## 最适合谁

- solo SaaS founder
- 正在做付费产品的独立开发者
- 想把“一个产品”升级成“一个业务”的 indie hacker
- 仍然以创始人为核心决策者的微型团队

## 你能很快得到什么

- 不是空泛建议，而是一套清晰的公司起步方案
- `Validate`、`Build`、`Launch`、`Operate`、`Grow` 五阶段执行方式
- PRD、ICP、Launch Brief、Dashboard、Weekly Review 等真实产物
- 明确的 AI 角色分工和交接关系
- 同一套公司内核下的中英双市场执行逻辑

## 语言行为

- 用户用中文调用时，默认输出中文材料
- 用户用英文调用时，默认输出英文材料
- 只有用户明确要求时，才默认同时输出中英文双语版本
- 共享战略文档和面向市场的材料，可以在需要时采用不同语言

## 快速开始

直接这样调用：

```text
使用 $one-person-company 帮我搭建一个 solo SaaS 公司。请直接产出 company charter、ICP、offer sheet、MVP scope 和 weekly operating rhythm，全部用中文写。
```

```text
使用 $one-person-company，当前处于 Validate 阶段。请产出 ICP card、offer sheet、pricing hypothesis 和 validation plan，全部用中文写。
```

```text
使用 $one-person-company。我们正在做一个 B2B AI SaaS 的 Build 阶段，请产出 PRD、sprint plan、architecture note 和 release checklist，全部用中文写。
```

```text
使用 $one-person-company。我们现在处于 Launch 阶段，请产出 launch brief、landing page outline、onboarding outline、FAQ 和两周 launch checklist，全部用中文写。
```

```text
使用 $one-person-company 帮我做本周 weekly review，请总结 wins、losses、metrics、blockers 和本周接下来 5 个动作，全部用中文写。
```

## 它和普通创业技能的区别

- 不是创业鸡汤
- 不是角色扮演 Prompt 包
- 不是只覆盖产品或只覆盖销售的单点技能
- 不是把英文文案翻译成中文就叫全球化

它的设计原则是：

- 一套共享的 company core
- 一套共享的 product truth
- 按市场本地化执行面

需要本地化的通常是：

- positioning
- landing page
- 渠道策略
- sales script
- support FAQ
- 市场假设

## 技能里包含什么

- 可发布的 `SKILL.md`
- founder、chief of staff、product、design、engineering、QA、DevOps、growth、support、finance、legal、data、content、community 等角色参考
- 从 idea 到 MVP、从 build 到 launch、从 lead 到 close、从反馈到迭代、到 weekly rhythm 的工作流参考
- 一组可复用模板
- 初始化公司和生成周复盘的脚本
- 一个全球双语 SaaS 示例包

## 本地文件工作流

技能自带两个脚本：

- `scripts/init_company.py` 用模板初始化公司目录
- `scripts/weekly_review.py` 生成某周的 weekly review

示例：

```bash
python3 scripts/init_company.py "My Company" --path ./workspace --mode saas
python3 scripts/weekly_review.py ./workspace/my-company --week-of 2026-03-30
```

## 信任边界

这个技能适合先出草稿、先搭系统、先组织执行，不适合默认替你做高风险动作。

以下事情应当要求创始人明确确认：

- 生产环境部署
- 修改线上定价
- 法务或合规表述
- 花预算
- 删除或回填线上数据
- 大规模自动发送面向客户的内容

## 核心定位

把一个创始人升级成一家公司。
