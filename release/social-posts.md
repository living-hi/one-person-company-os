# Social Posts

## X / Short Post

I upgraded `one-person-company-os` to `v0.6.5`.

It now asks for founder direction first, then creates a real operating workspace that matches the founder language all the way down to visible file and directory names.

Not a prompt bundle. Not a mixed-language workspace with translated text on top.

## X / 中文短帖

我把 `one-person-company-os` 升级到 `v0.6.5`。

这一版补上了一个很关键的产品缺口：

- 中文用户拿到纯中文可见工作区
- 英文用户拿到纯英文可见工作区
- 机器状态隐藏到 `.opcos/state/current-state.json`

不再是“内容翻译了，但路径还是中英混合”。

## LinkedIn / Longer Post

`one-person-company-os` now closes a subtle but important trust gap.

The runtime had already become direction-first and bilingual, but the generated workspace still mixed Chinese and English visible paths and exposed internal state in the founder surface.

`v0.6.5` fixes that:

- founder-visible workspaces localize fully by language
- internal machine state moves to `.opcos/state/current-state.json`
- release validation now checks Chinese and English workspace separation directly

The result is a product that behaves more like a serious founder operating system and less like a translated wrapper around one filesystem layout.
