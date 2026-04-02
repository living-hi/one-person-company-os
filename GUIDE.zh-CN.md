# One Person Company OS 通俗指南

这不是一个“帮你出几个点子”的提示词。

把它想成一套给独立开发者用的“公司操作系统”更准确：

- 你还是老板，负责拍板
- AI 不是假装创业导师，而是分角色帮你推进工作
- 每次输出尽量变成可复用文档，而不是聊完就散

## 它有什么作用

如果你一个人做 SaaS，最常见的问题不是不会写代码，而是：

- 今天做产品，明天写文案，后天改定价，事情很多但容易乱
- 想法很多，但没有固定流程把想法变成可执行文档
- 每次都从头跟 AI 解释背景，重复成本很高
- 中文市场和英文市场要兼顾时，容易做成两套割裂系统

这个技能解决的就是这些问题。它会把“一个人做公司”拆成几层：

- 阶段：你现在是在验证、开发、发布、运营还是增长
- 角色：产品、设计、工程、增长、客服、财务等分别负责什么
- 工作流：当前瓶颈该按什么顺序往下推
- 产物：每一步应该留下什么文档
- 节奏：每周怎么复盘，怎么继续推进

一句话说，它的目标不是帮你回答一个问题，而是帮你把业务长期跑顺。

## 最简单的用法

### 1. 直接调用技能

最适合第一次用。

```text
使用 $one-person-company-os 帮我搭建一个 solo SaaS 公司。
当前阶段是 Build，目标客户是中国的独立开发者。
请直接产出 company charter、ICP、offer sheet、PRD 和 weekly operating rhythm，全部用中文写。
```

你最好在提示里带上这几项：

- 当前阶段
- 你卖什么
- 目标客户是谁
- 当前最大瓶颈
- 这次希望拿到什么结果
- 时间、预算、风险限制
- 面向中文、英文还是双语市场

如果你没写全，这个技能也会先做工作假设，再继续往下产出。

### 2. 用本地脚本初始化一个公司工作区

最适合你想把输出真正沉淀到文件里。

```bash
python3 scripts/init_company.py "My Company" --path ./workspace --mode saas
```

它会生成一套基础目录和模板，比如：

- `00-company-charter.md`
- `01-icp-card.md`
- `02-offer-sheet.md`
- `03-prd.md`
- `launches/`
- `reviews/`
- `agent-briefs/`

你可以把这个目录理解成“你的公司硬盘”。

### 3. 给某个角色生成任务说明书

最适合你想把某一步明确交给某个 AI 角色时用。

```bash
python3 scripts/build_agent_brief.py \
  --stage Build \
  --role engineer-tech-lead \
  --language zh-CN \
  --company-name "My Company" \
  --objective "把 PRD 变成 implementation plan" \
  --current-bottleneck "范围已经确定，但交付路径仍不清晰" \
  --next-required-artifact "sprint-plan.md" \
  --input 03-prd.md
```

这个脚本会生成一份很像“岗位派单单”的 brief，告诉该角色：

- 你是谁
- 你负责什么
- 你拿到了哪些输入
- 你要产出什么
- 哪些事不能越权
- 做完要交给谁

### 4. 每周复盘

```bash
python3 scripts/weekly_review.py ./workspace/my-company --week-of 2026-03-30
```

它会帮你生成固定格式的周复盘文件，让你的业务不是“一阵一阵地冲”，而是形成节奏。

## 它是怎么工作的

可以把内部架构理解成 5 层。

### 第 1 层：行为规则层

`SKILL.md`

这是总指挥。它规定：

- 什么时候该用这个技能
- 怎么判断当前属于哪个阶段
- 默认该激活哪些角色
- 输出应该偏“文档产物”而不是空谈
- 哪些高风险动作必须让创始人审批

## 第 2 层：知识参考层

`references/`

这里放的是角色说明、生命周期模式、工作流、市场策略等参考资料。它像公司的“管理手册”。

AI 在生成产物时，不是临场瞎编，而是尽量按这些参考规则来组织输出。

## 第 3 层：机器可读角色层

`agents/roles/*.json`

这一层很关键。它把“产品经理、工程负责人、增长负责人”这些角色，写成结构化 JSON。

每个角色文件都会定义：

- 这个角色叫什么
- 主要使命是什么
- 默认适合什么阶段
- 它拥有什么职责
- 需要哪些输入
- 应该输出哪些产物
- 应该把结果交给谁
- 哪些事不能做
- 哪些动作需要审批

这意味着角色不是嘴上说说，而是机器真的能读懂并执行。

## 第 4 层：编排层

`orchestration/stage-defaults.json`
`orchestration/handoff-schema.json`

这一层解决两个问题：

第一，当前阶段默认应该上哪些角色。

比如 `Build` 阶段默认会偏向：

- founder-ceo
- chief-of-staff
- product-strategist
- engineer-tech-lead
- qa-reliability
- devops-sre

第二，角色之间怎么交接。

`handoff-schema.json` 规定交接时必须保留哪些字段，比如：

- 当前阶段
- 工作语言
- 目标
- 输入材料
- 需要的输出
- 约束条件
- 审批点
- 下一位接手者

这样做的核心价值是：上下文不会丢。

## 第 5 层：落地执行层

`scripts/*.py`

这里的脚本把前面的规则真正落到文件系统里：

- `init_company.py`：创建公司目录和模板
- `build_agent_brief.py`：根据阶段和角色生成 brief
- `weekly_review.py`：生成周复盘
- `validate_release.py`：做发布前检查

所以整套系统不是只停留在“提示词设计”，而是能产出真实文件、真实流程、真实交接。

## 为什么这种架构有用

如果不用这套架构，很多 AI 工作流会变成这样：

- 每次都重新解释背景
- 不同任务输出风格不一致
- 没有明确职责，AI 什么都说一点，但没人真正负责
- 做完一轮没有文档沉淀，下次还得重来

这套架构本质上是在解决 3 个问题：

### 1. 把“能力”拆成“职责”

不是问 AI 会不会，而是先规定谁该负责什么。

### 2. 把“聊天”变成“产物”

每一轮最好留下 charter、ICP、PRD、launch brief、weekly review 这类文档。

### 3. 把“一次回答”变成“持续经营”

今天做 Validate，后面进 Build、Launch、Operate、Grow，都还能沿着同一套公司内核运行。

## 你可以怎么理解它

用最通俗的话说：

- `SKILL.md` 是老板定的管理制度
- `references/` 是公司知识库
- `agents/roles/*.json` 是岗位说明书
- `orchestration/*.json` 是排班和交接规则
- `scripts/*.py` 是行政和执行工具
- `workspace/` 生成出来的目录，就是你的公司档案室

## 推荐使用姿势

如果你是第一次用，建议按这个顺序：

1. 先让技能帮你产出第一套 starter pack
2. 再用 `init_company.py` 建一个真实工作区
3. 把产出的关键文档填进工作区
4. 当你卡在某个环节时，用 `build_agent_brief.py` 给单个角色发任务
5. 每周用 `weekly_review.py` 固定复盘一次

这样它最像“公司操作系统”；如果只是偶尔问一句灵感，它的价值反而发挥不出来。
