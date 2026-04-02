# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

One Person Company OS 现在是一套面向中文用户优先的一人公司操作系统。

它不再以“每周复盘”或一堆重型创业文档为中心，而是改成了更适合 AI 智能体时代的主循环：

- 创建公司
- 启动回合
- 推进回合
- 触发时才校准
- 瓶颈变化时切换阶段

## 它解决什么问题

它要解决的不是“给你一点创业建议”，而是让一个创始人在不增加管理负担的情况下，像一家公司那样推进。

核心做法是：

- 中文优先的工作区
- 最小角色体系
- 回合制推进
- 触发式校准
- 适配 OpenClaw 的本地脚本和角色 brief

## 主入口

可以直接这样调用：

```text
我想创建一间一人公司，请帮我调用 one-person-company-os。
主要是打造一个 AI 产品，请你开始。
```

```text
帮我启动当前阶段的第一个推进回合。
```

```text
继续推进当前回合，告诉我现在最短路径怎么走。
```

```text
我卡住了，帮我进入校准回合。
```

```text
帮我判断现在是否应该切换阶段。
```

## 核心模式

- `创建公司`
- `启动回合`
- `推进回合`
- `校准回合`
- `切换阶段`

## 工作区结果

V2 工作区围绕“公司当前状态”和“当前回合”组织：

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

- `scripts/init_company.py`
- `scripts/build_agent_brief.py`
- `scripts/start_round.py`
- `scripts/update_round.py`
- `scripts/calibrate_round.py`
- `scripts/transition_stage.py`
- `scripts/validate_release.py`

## 参考资料

- `references/bootstrap-playbook.md`
- `references/round-execution-playbook.md`
- `references/calibration-playbook.md`
- `references/stage-transition-playbook.md`
- `references/openclaw-runtime.md`
- `references/chinese-workspace-conventions.md`

## 校验

运行：

```bash
python3 scripts/validate_release.py
```

## 使用原则

- 中文用户默认全部用中文，包括工作区和日常用语。
- 创始人始终保留预算、上线、合规、客户触达等最终拍板权。
- 周复盘不再是主循环，只作为兜底的战略复核。
