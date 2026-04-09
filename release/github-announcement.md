# GitHub Announcement

I upgraded `one-person-company-os` to `v0.6.6`.

The previous release fixed the language-localized workspace surface.
This release fixes the next trust mismatch: the public marketplace surface still left too much ambiguity around host-environment changes and write boundaries.

What changed:

- `scripts/ensure_python_runtime.py` now stays in compatibility-guidance mode and does not auto-install system packages
- persisted artifact output paths are constrained to stay inside the approved company workspace
- `agents/openai.yaml` now disables implicit invocation for this higher-authority skill
- README, SKILL, release README, listing copy, publishing notes, and validation all now describe the same safety boundary

This matters because platform trust is not only about whether code is malicious.
It is also about whether the package makes its requirements and authority explicit before users run it.

`v0.6.6` makes that contract explicit and enforceable.
