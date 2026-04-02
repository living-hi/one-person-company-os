# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

给正在创立 AI 一人公司的创始人：你不是缺建议，你缺一个真正能把公司从想法推到执行的系统。

One Person Company OS 不是泛泛的创业 prompt。它会把一句产品想法收敛成一套可持续推进的 company OS：先出创建草案，再在你确认后创建中文工作区、最小角色体系、当前回合、记录文件和后续校准路径。

## 如果你正处在这种状态

- 有一个 AI 产品方向，但还没有形成清晰公司骨架
- 想快速启动一人公司，不想把时间耗在零碎管理上
- 内容都堆在聊天记录里，过两天就不知道当前阶段和下一步是什么
- 经常输出很多策略，但没有 checkpoint、没有真实落盘、没有持续执行节奏
- 想要一个更像操作系统的流程，而不是一个会不断说话的顾问

这个技能就是为这种用户设计的。

## 它的核心承诺

- 先把模糊想法变成“可确认的公司创建草案”
- 再把草案变成“真实落盘的中文工作区”
- 再把工作区变成“只有一个当前回合、一个当前瓶颈、一个下一步最短动作”的执行系统
- 在阻塞、偏航、关键产物完成或准备切阶段时，才进入校准
- 脚本环境出问题时，不会只报错停住，而会优先恢复、安装或由 OpenClaw 智能体接管

## 第一次使用你会得到什么

- 产品一句话定义
- 3 到 5 个公司名称建议
- 当前建议阶段
- 目标用户与核心问题
- 最小组织架构和首批激活角色
- 中文工作区结构
- 第一个 2 到 3 小时内可推进的回合
- 待创始人确认事项

## 为什么它更像 Company OS，而不是普通 Prompt

- 有固定 `Step 1/5` 到 `Step 5/5` 的状态机
- 有固定的 `状态栏 / 保存状态 / 运行状态`
- 有真实落盘，而不是只存在于对话里
- 有 preflight 检查，不把“已安装”误说成“可运行”
- 有 `模式 A / 模式 B / 模式 C` 降级策略
- 有 Python 兼容恢复链路，优先适配 OpenClaw

## 直接这样开始

```text
我想围绕一个 AI 产品创建一间一人公司，请帮我调用 one-person-company-os。
先做 Step 1/5 到 Step 3/5，给我公司创建草案，并明确当前保存模式、保存状态和运行状态；我确认后再正式创建。
```

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

## 真实执行时你会看到什么

所有执行都遵循固定的 5 步状态机：

1. `Step 1/5` 模式判定
2. `Step 2/5` preflight 与保存策略检查
3. `Step 3/5` 草案 / 变更提议 / 当前状态装载
4. `Step 4/5` 执行与落盘
5. `Step 5/5` 验证与回报

每次关键产出后，默认输出：

- `状态栏`
  - 当前模式、当前步骤、当前阶段、当前回合、当前角色、当前产物、当前保存模式、下一步动作、是否需要确认
- `保存状态`
  - 是否已保存、保存路径、文件名、未保存原因
- `运行状态`
  - `installed`、`runnable`、`python_supported`、`workspace_created`、`persisted`

## 三种执行模式

- `模式 A：脚本执行`
  - 环境可运行，直接走 `scripts/*.py`
- `模式 B：手动落盘`
  - 脚本不可用，但仍可直接把 markdown/json 写进工作区
- `模式 C：纯对话推进`
  - 当前不能写文件，或用户尚未确认正式创建

脚本失败时，默认优先从 A 降级到 B，而不是直接退回纯聊天。

## Python 不兼容时怎么恢复

- 兼容目标：`Python 3.7+`
- preflight 会检查当前解释器、可切换解释器、恢复脚本和推荐动作
- 如果当前版本不适配，优先让 `OpenClaw` 智能体切换到本机已有兼容 Python
- 如果本机没有兼容解释器，再由 `OpenClaw` 智能体尝试自动安装
- 如果不适合安装，则由智能体直接完成脚本任务并手动落盘

恢复入口：

```bash
python3 scripts/ensure_python_runtime.py
python3 scripts/ensure_python_runtime.py --apply
python3 scripts/ensure_python_runtime.py --apply --run-script scripts/preflight_check.py -- --mode 创建公司
```

## 确认后会创建什么

工作区围绕“公司当前状态”和“当前回合”组织：

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

## 快速自检

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/validate_release.py
```

## 使用原则

- 中文用户默认全部用中文，包括工作区、文件名和日常用语。
- 创始人始终保留预算、上线、合规、客户触达等最终拍板权。
- 系统以“回合”推进，而不是把周报当主循环。
- 第一个回合应该足够小，能在 2 到 3 小时内推进出明确结果。
