# One Person Company OS

这不是泛创业 prompt，而是一套面向 AI 一人公司的 **状态驱动 operating system**。

One Person Company OS 用来统一四类关键对象：

- 公司定义
- 角色结构
- 当前回合
- 文件与运行状态

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
我正在创立一间 AI 一人公司，请帮我调用 one-person-company-os。先做 Step 1/5 到 Step 3/5，给我公司创建草案，并明确当前保存模式、保存状态和运行状态；我确认后再正式创建。
```

## 它会给你什么

- 公司创建草案
- 3 到 5 个公司名称建议
- 当前建议阶段
- 最小组织架构和首批角色
- 中文工作区结构
- 第一个可执行回合
- 状态透明、保存透明、运行透明的执行过程

## 它为什么更像 Company OS

- 固定 `Step 1/5 -> Step 5/5`
- 固定 `状态栏 / 保存状态 / 运行状态`
- 固定 `模式 A / 模式 B / 模式 C`
- 固定 preflight 与 Python 恢复入口

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

## 本地工作流

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/init_company.py "北辰实验室" --path ./workspace --product-name "北辰助手" --stage 构建期
python3 scripts/start_round.py ./workspace/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/checkpoint_save.py ./workspace/北辰实验室 --reason "准备结束当前会话"
python3 scripts/validate_release.py
```

## 核心定位

把一个正在创立 AI 一人公司的创始人，升级成一套可持续推进的 company OS。
