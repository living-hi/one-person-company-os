# Social Posts

## X / Short Post

I upgraded `one-person-company-os` to `v0.6.6`.

This patch hardens the marketplace safety boundary:

- no automatic system-package installation
- persisted writes stay inside the approved workspace
- public docs now match the real runtime contract

## X / 中文短帖

我把 `one-person-company-os` 升级到 `v0.6.6`。

这一版补的是公开发布面的安全边界：

- marketplace 版不再自动安装系统级依赖
- 持久化写入只留在确认过的工作区里
- README、SKILL、ClawHub listing 和真实运行契约终于对齐

不是只改文案，也不是只改代码，而是把公开面和真实行为一起收紧。

## LinkedIn / Longer Post

`one-person-company-os` now closes an important marketplace trust gap.

The package was already direction-first and language-localized, but the public surface still left too much ambiguity around host changes and write scope.

`v0.6.6` fixes that:

- `scripts/ensure_python_runtime.py` now stays in compatibility-guidance mode and does not auto-install system packages
- persisted write paths are tightened to the approved company workspace
- public docs, prompts, metadata, and release material now describe the same safety boundary the runtime actually follows

The result is a package that is easier to audit, easier to trust, and more likely to clear platform security review without diluting the core founder workflow.
