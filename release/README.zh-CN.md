# One Person Company OS

One Person Company OS 把“一个 AI 产品想法”，推进成一套真实可运行的一人公司经营闭环：

- 定义价值承诺
- 把 MVP 推到可演示、可上线、可售卖
- 管理线索、成交、交付与回款
- 沉淀 SOP、模板、自动化和代码资产

安装：

```bash
clawhub install one-person-company-os
```

推荐启动提示：

```text
我正在围绕一个 AI 产品创建一人公司，请调用 one-person-company-os。不要先给我商业计划书模板。先主动问我一句创业想法；如果我还没想好，就给我 3 到 4 个方向让我选。等我们确认可卖承诺、第一批买家和核心问题后，再创建工作区、告诉我当前主瓶颈，并把真实文件改出来。
```

工作区现在会生成和语言一致的第一层主文件。

中文创始人会看到：

- `00-经营总盘.md`
- `02-价值承诺与报价.md`
- `03-机会与成交管道.md`
- `04-产品与上线状态.md`
- `05-客户交付与回款.md`

英文创始人会看到对应的英文文件名：

- `00-operating-dashboard.md`
- `02-value-promise-and-pricing.md`
- `03-opportunity-and-revenue-pipeline.md`
- `04-product-and-launch-status.md`
- `05-delivery-and-cash-collection.md`

这一版已经支持：

- v3 经营闭环状态模型
- 产品开发与上线推进
- 成交、交付、回款、资产沉淀入口
- 对创始人可见的中英文工作区完全分离，内部机器状态隐藏在 `.opcos/state/current-state.json`
- 旧阶段/回合脚本兼容
- 最终命名的编号化 DOCX 正式交付
