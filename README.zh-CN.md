# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

**One Person Company OS 是一套面向 AI Native Solo Founder 的公司运行系统。**

它不是商业计划书生成器，不是泛创业顾问，也不是一串只会持续输出建议的 prompt。
它的职责是把一人公司的 **定义、决策、角色、回合、文件、校准、恢复** 收敛到同一套可执行操作层里，让创始人始终知道：

- 现在处于哪个阶段
- 当前只有哪个回合在推进
- 关键产物是否已经落盘
- 下一步最短动作是什么
- 如果本地环境有问题，系统应该如何恢复

## 一句话定位

把一个 AI 产品想法，升级成一套可持续推进、可真实落盘、可恢复运行的一人公司操作系统。

## 适用对象

这个项目主要服务以下用户：

- 正在创立 AI 一人公司或 AI 原生微型团队的创始人
- 已有产品方向，但缺少专业、稳定、可持续推进的公司运行结构的人
- 不想把上下文散落在长聊天、临时笔记和碎片文档里的人
- 希望系统像标准 operating layer 一样工作，而不是像普通顾问对话一样漂浮的人

## 它解决的不是“内容不够”，而是“系统不存在”

大多数创业 prompt 的问题不是不会说，而是不会运行。

常见真实问题：

- 说了很多，但不知道当前系统状态
- 生成了很多内容，但不知道是否已经保存
- 文件和回合没有统一模型
- 脚本一旦跑不了，就退回纯聊天
- 过几天回来，不知道当前阶段、阻塞和下一步动作

One Person Company OS 的目标不是再多给一点建议，而是提供一层真正的 **Company Operating Layer**。

## 你会得到什么

首次像样的调用，应该直接产出这些标准件：

- 公司创建草案
- 产品一句话定义
- 3 到 5 个公司名称建议
- 当前建议阶段
- 目标用户与核心问题
- 最小组织架构与首批激活角色
- 中文工作区结构
- 第一个 2 到 3 小时内可推进的执行回合
- 待创始人确认事项
- 当前保存状态与运行状态

确认后，系统会继续给你：

- 真实落盘的中文工作区
- 当前回合文件
- 角色 brief
- 推进记录
- 校准记录
- 检查点记录

## 系统架构

这个项目的核心架构不是“多文档集合”，而是一个分层运行模型：

```text
创始人
  ↓
总控台 / Skill Protocol
  ↓
Round Engine
  ↓
Workspace Persistence Layer
  ↓
Runtime Recovery Layer
```

各层职责：

1. `创始人`
   - 提供方向、确认关键事项、保留最终决策权

2. `总控台 / Skill Protocol`
   - 负责模式判定、步骤推进、状态输出、确认边界

3. `Round Engine`
   - 负责当前阶段、当前回合、当前阻塞、下一步最短动作

4. `Workspace Persistence Layer`
   - 负责把关键产物真实写入工作区，而不是只存在于聊天中

5. `Runtime Recovery Layer`
   - 负责 preflight、Python 兼容检查、解释器切换、安装恢复和 OpenClaw 接管

## 标准运行模型

所有真实执行都遵循固定的五步状态机：

1. `Step 1/5` 模式判定
2. `Step 2/5` preflight 与保存策略检查
3. `Step 3/5` 草案 / 变更提议 / 当前状态装载
4. `Step 4/5` 执行与落盘
5. `Step 5/5` 验证与回报

这不是展示层装饰，而是交付协议的一部分。

## 默认输出协议

每次关键执行后，系统固定输出三组信息：

### 1. 状态栏

- 当前模式
- 当前步骤
- 当前阶段
- 当前回合
- 当前角色
- 当前产物
- 当前保存模式
- 下一步动作
- 是否需要确认

### 2. 保存状态

- 是否已保存
- 保存路径
- 文件名
- 未保存原因

### 3. 运行状态

- `installed`
- `runnable`
- `python_supported`
- `workspace_created`
- `persisted`

这意味着用户不需要靠追问来判断系统到底进行到哪一步。

## 三种执行模式

- `模式 A：脚本执行`
  - 环境可运行，直接使用脚本完成工作区与状态变更
- `模式 B：手动落盘`
  - 脚本不稳定或暂时不可用，但仍可以直接写入 markdown/json
- `模式 C：纯对话推进`
  - 当前不能写文件，或用户尚未确认正式创建

默认降级路径：

- 优先从 `模式 A` 降到 `模式 B`
- 只有在不能写文件或不应写文件时才进入 `模式 C`

## 工作区标准结构

```text
公司名/
  00-公司总览.md
  01-产品定位.md
  02-当前阶段.md
  03-组织架构.md
  04-当前回合.md
  05-推进规则.md
  06-触发器与校准规则.md
  角色智能体/
  流程/
  产物/
  记录/
  自动化/
```

核心设计原则：

- 一个公司只有一个当前状态
- 一个阶段只看一个当前瓶颈
- 一个时点只推进一个当前回合
- 一个回合必须有明确产物、阻塞和下一步动作

## 为什么它比普通 Prompt 更专业

- 有标准运行协议，而不是即兴输出
- 有明确持久化边界，而不是“说了等于做了”
- 有运行时恢复层，而不是脚本失败就中断
- 有回合制推进模型，而不是泛化周报心智
- 有创始人确认边界，适合真实业务环境

## 一句话安装

```bash
clawhub install one-person-company-os
```

## 一句话启动

```text
我正在创立一间 AI 一人公司，请帮我调用 one-person-company-os。先做 Step 1/5 到 Step 3/5，给我公司创建草案，并明确当前保存模式、保存状态和运行状态；我确认后再正式创建。
```

## 推荐启动方式

```text
我正在创立一间 AI 一人公司，请帮我调用 one-person-company-os。
先做 Step 1/5 到 Step 3/5，给我公司创建草案，并明确当前保存模式、保存状态和运行状态；
我确认后再正式创建。
```

后续常用入口：

```text
帮我启动当前阶段的第一个推进回合。
```

```text
继续推进当前回合，告诉我现在最短路径怎么走。
```

```text
我卡住了，进入校准回合。
```

```text
帮我判断现在是否应该切换阶段。
```

## Python 兼容与恢复

- 兼容目标：`Python 3.7+`
- 系统会先做 preflight
- 如果当前解释器不兼容，优先切换到本机已有兼容解释器
- 如果本机没有兼容解释器，优先由 OpenClaw 自动安装
- 如果当前环境不适合安装，则由智能体直接接管脚本任务并手动落盘

恢复入口：

```bash
python3 scripts/ensure_python_runtime.py
python3 scripts/ensure_python_runtime.py --apply
python3 scripts/ensure_python_runtime.py --apply --run-script scripts/preflight_check.py -- --mode 创建公司
```

## 本地脚本

- `scripts/preflight_check.py`
- `scripts/ensure_python_runtime.py`
- `scripts/init_company.py`
- `scripts/build_agent_brief.py`
- `scripts/start_round.py`
- `scripts/update_round.py`
- `scripts/calibrate_round.py`
- `scripts/checkpoint_save.py`
- `scripts/transition_stage.py`
- `scripts/validate_release.py`

## 交付校验

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/validate_release.py
```

## 使用原则

- 中文用户默认使用中文工作区、中文文件名、中文流程与中文输出
- 创始人保留预算、上线、合规、客户触达等最终拍板权
- 系统以“回合”推进，不以“周报”推进
- 第一个回合应足够小，能在 2 到 3 小时内产生明确结果
