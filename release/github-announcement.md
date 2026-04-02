# GitHub Announcement

I upgraded `one-person-company-os` again.

The previous release made the project easier to understand.
This release makes it easier to actually operate.

The main gap was interaction quality during real use:

- users could still lose track of the current stage, round, and step
- save and runtime fields were technically correct, but not always easy to interpret quickly
- important outputs still leaned too much on chat formatting instead of standard document forms

This release fixes that.

This release includes:

- a three-layer navigation bar: stage, round, current step
- dual-labeled steps with natural-language guidance plus system labels
- `用户导航版` and `审计版` output modes
- `本次会做 / 不会做`, `本次变化`, and `回合仪表盘`
- clearer save explanations and runtime explanations
- a new artifact document generator
- three standard artifact forms:
  - internal draft
  - standard spec
  - DOCX-ready draft
