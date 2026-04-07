# GitHub Announcement

I upgraded `one-person-company-os` to `v0.6.5`.

The previous release fixed the direction-first contract and removed the leaked default vertical case.
This release fixes the next product mismatch: the runtime could already speak Chinese or English, but the generated workspace still mixed Chinese and English paths and exposed state in the founder-visible surface.

What changed:

- founder-visible workspaces now fully localize by language
- Chinese founders get Chinese root files and directories
- English founders get English root files and directories
- machine state moved to the hidden stable path `.opcos/state/current-state.json`
- validation now checks Chinese and English workspace separation explicitly

This matters because content localization alone was not enough.
If the workspace surface still mixed `销售/` with `product/`, or exposed `自动化/当前状态.json`, the product still felt unfinished and untrustworthy.

`v0.6.5` fixes that mismatch.
The package now creates a language-matched founder workspace instead of a mixed-language filesystem with translated text on top.
