# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

One Person Company OS 是一套面向中文用户优先的一人公司总控台。

从一句产品想法开始，它会先帮你产出公司创建草案；你确认后，再创建中文工作区、最小角色智能体和首个推进回合。

它的主循环是：

- 创建公司
- 启动回合
- 推进回合
- 触发时才校准
- 瓶颈变化时切换阶段

## 它帮你做到什么

- 把一个模糊想法整理成可执行的一人公司骨架
- 明确当前阶段、当前回合、当前阻塞和下一步最短动作
- 用最小角色体系持续推进，而不是把时间耗在管理上
- 只在卡住、偏航、完成关键产物或准备切阶段时才校准

## 首次使用你会得到什么

- 产品一句话定义
- 3 到 5 个公司名称建议
- 当前建议阶段
- 最小组织架构和首批激活角色
- 中文工作区结构
- 第一个可立即推进的回合
- 待创始人确认事项

## 直接这样调用

```text
我想围绕一个 AI 产品创建一间一人公司，请帮我调用 one-person-company-os。
先给我公司创建草案；我确认后，再创建中文工作区、角色智能体和首个推进回合。
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

## 确认后会创建什么

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
