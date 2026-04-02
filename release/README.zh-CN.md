# One Person Company OS

给正在创立 AI 一人公司的创始人：这不是一个会不断给建议的 prompt，而是一套真正能落盘、能推进、能恢复的一人公司操作系统。

One Person Company OS 会先给你公司创建草案；你确认后，再创建中文工作区、最小角色体系、当前回合和后续校准路径。

它最适合这些情况：

- 有一个 AI 产品方向，但还没有形成清晰的一人公司骨架
- 内容都散落在对话里，缺少当前阶段、当前回合和下一步动作
- 想让系统真实落盘，而不是过几天就丢上下文
- 希望脚本跑不起来时，OpenClaw 也能继续接管

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
