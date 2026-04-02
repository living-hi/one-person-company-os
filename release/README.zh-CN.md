# One Person Company OS

One Person Company OS 现在是一套面向中文用户优先的一人公司操作系统。

它的核心不再是每周复盘，而是：

- 创建公司
- 启动回合
- 推进回合
- 触发时才校准
- 瓶颈变化时切阶段

## 它为什么不一样

- 中文优先的工作区和工作语言
- 用回合制推进代替按周管理
- 先用最小角色集，而不是一开始铺满角色
- 优先适配 OpenClaw 的本地执行链路

## 首次使用承诺

一次像样的首次调用，应该直接给你：

- 一份公司创建草案
- 3 到 5 个公司名称建议
- 当前建议阶段
- 最小角色体系
- 中文工作区方案
- 第一个可以立即推进的回合

## 本地工作流

```bash
python3 scripts/init_company.py "北辰实验室" --path ./workspace --product-name "北辰助手" --stage 构建期
python3 scripts/start_round.py ./workspace/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/validate_release.py
```

## 核心定位

把一个创始人升级成一间高效推进的一人公司。
