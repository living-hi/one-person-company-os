# One Person Company OS

这不是泛创业 prompt，而是一套面向 AI 一人公司的 **可导航、可落盘、可交付、按快循环运行的 operating system**。

One Person Company OS 用来统一四类关键对象：

- 公司定义
- 角色结构
- 当前回合
- 文件与运行状态
- 文档产物

适合：

- 正在创立 AI 一人公司的创始人
- 需要一个比“聊天建议”更专业的执行层的人
- 希望系统能落盘、能推进、能恢复的人

## 一句话安装

```bash
clawhub install one-person-company-os
```

## 一句话启动

```text
我正在创立一间 AI 一人公司，请帮我调用 one-person-company-os。先别让我填很多表，先主动问我一句创业想法；如果我没想好，就给我 3 到 4 个方向建议让我选。默认按 AI 时代的一人公司快循环来：快速验证需求，快速做 MVP，小范围上线，收反馈再迭代。然后做 Step 1/5 到 Step 3/5，给我公司创建草案，并告诉我当前内容有没有保存、我接下来该看哪个路径。
```

## 它会给你什么

- 公司创建草案
- 一句话创始人输入入口
- 如果没想清楚，也能直接选创业方向
- 3 到 5 个公司名称建议
- 当前主瓶颈阶段
- 最小组织架构和首批角色
- 按用户语言输出的工作区与资料方案
- 第一个可执行回合
- 三层导航条与回合仪表盘
- 用户导航版与审计版双视图输出
- 状态透明、保存透明、运行透明的执行过程
- 直接按最终文件名落盘的正式 DOCX 交付，以及软件/非软件/部署生产证据链
- `12-AI时代快循环.md`，让工作区内直接解释这套方法

## 语言行为

- 中文输入 -> 默认输出中文运行过程和中文资料
- 英文输入 -> 默认输出英文运行过程和英文资料
- 仓库内部路径保持稳定，避免自动化和发布链路因语言切换而失稳

## 它为什么更像 Company OS

- 固定 `Step 1/5 -> Step 5/5`
- 固定 `阶段 / 回合 / 本次 Step`
- 固定 `用户导航版 / 审计版`
- 固定 `模式 A / 模式 B / 模式 C`
- 固定 preflight 与 Python 恢复入口
- 固定交付物地图、交付目录总览与 DOCX 导向输出
- 固定 AI 时代快循环说明，并把阶段降级为主瓶颈标签

## 核心架构

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

## AI 时代默认流程

- 先收窄一个痛点和一个付费用户
- 快速验证需求
- 先做最小可上线 MVP
- 小范围上线
- 用反馈、指标和生产现实持续修产品
- 产品价值和留存稳定后，再放大增长

## 本地工作流

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/init_company.py "北辰实验室" --path ./workspace --product-name "北辰助手" --stage 构建期
python3 scripts/start_round.py ./workspace/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/generate_artifact_document.py ./workspace/北辰实验室 --title "首页首屏规范" --category software
python3 scripts/checkpoint_save.py ./workspace/北辰实验室 --reason "准备结束当前会话"
python3 scripts/validate_release.py
```

## 核心定位

把一个正在创立 AI 一人公司的创始人，升级成一套可持续推进的 company OS。
