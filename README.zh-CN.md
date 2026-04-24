# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

**One Person Company OS v1.0 是面向 AI 一人创始人的可视化经营驾驶舱。**

它不是商业计划书生成器，不是阶段/回合项目管理器，也不是模板包。
它帮助一个创始人持续看住真实经营闭环：

`价值承诺 -> 买家 -> 产品能力 -> 交付 -> 回款 -> 学习 -> 资产`

## v1.0 改了什么

v1.0 是一次断代架构发布。

- 状态文件升级为 v1.0 经营闭环模型，不再写入旧 `stage_id` 或 `current_round`
- 下载后优先打开的是经营驾驶舱 HTML，不再只是 markdown 包装页
- 每个工作区自动生成经营闭环图和成交管道图
- AI 图片能力作为可选创作层，用于封面、发布帖和宣发视觉，不承载精确经营数据
- 旧阶段/回合命令保留为废弃提示，不再生成旧语义

## 工作区模型

生成后的工作区仍然分三层：

- Markdown：可持续编辑的经营底稿
- HTML：下载后优先查看的本地阅读层，以经营驾驶舱为入口
- DOCX：`产物/` 或 `artifacts/` 下的编号正式交付件

中文工作区会包含：

- `阅读版/00-经营驾驶舱.html`
- `视觉素材/business-loop.svg`
- `视觉素材/revenue-pipeline.svg`
- `视觉素材/ai-image-prompts.md`

英文工作区会包含：

- `reading/00-operating-cockpit.html`
- `visual-kit/business-loop.svg`
- `visual-kit/revenue-pipeline.svg`
- `visual-kit/ai-image-prompts.md`

机器状态仍固定隐藏在 `.opcos/state/current-state.json`。

## 运行要求与安全边界

- 脚本模式需要本机已有 `Python 3.7+`
- `scripts/ensure_python_runtime.py` 只输出兼容性与手动安装建议
- marketplace 版不会自动安装系统级依赖
- 所有生成文件只写入创始人批准的工作区
- 正常使用不需要 API key 或无关凭据
- AI 图片是可选创作层，不是核心运行依赖

## 本地命令

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/init_business.py "北辰实验室" --path ./workspace --product-name "北辰助手" --target-user "独立开发者" --core-problem "还没有一个真正能持续推进产品和成交的一人公司系统" --product-pitch "一个帮助独立开发者把产品做出来并卖出去的一人公司控制系统" --confirmed
python3 scripts/validate_release.py
```

## 一行安装

```bash
clawhub install one-person-company-os
```

## 一行启动

```text
我正在创建一个 AI 一人公司，请调用 one-person-company-os v1.0。不要先给我商业计划书模板。先帮我确认可卖承诺、第一批买家和核心问题；确认后在我批准的本地目录创建工作区，用经营驾驶舱作为入口，直观展示当前瓶颈，并且只把批准后的文件保存到这个工作区内。
```

## 校验

```bash
python3 scripts/validate_release.py
```

它会校验 v1.0 状态、双语工作区、经营驾驶舱、视觉素材、DOCX-only 产物目录、废弃阶段/回合命令和公开发布物料。
