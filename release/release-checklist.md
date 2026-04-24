# Release Checklist

## Positioning

- keep the primary audience as AI-native solo founders and independent builders
- keep the visible model as `promise -> buyer -> product -> delivery -> cash -> learning -> asset`
- present v1.0 as a visual operating cockpit
- do not reintroduce stage/round as the founder-visible product contract
- describe AI image generation as an optional creative layer only

## Repository

- verify `README.md`, `README.zh-CN.md`, and `SKILL.md` describe v1.0 consistently
- verify `agents/openai.yaml` matches the visual cockpit positioning
- run `python3 scripts/preflight_check.py --mode 创建公司`
- run `python3 scripts/ensure_python_runtime.py`
- run `python3 scripts/validate_release.py`
- confirm v1.0 state does not contain `stage_id` or `current_round`
- confirm Chinese and English workspaces generate localized cockpit entries
- confirm `视觉素材/` or `visual-kit/` includes `business-loop.svg`, `revenue-pipeline.svg`, and `ai-image-prompts.md`
- confirm `产物/` or `artifacts/` only contains numbered `.docx` formal deliverables
- confirm `.opcos/state/current-state.json` exists and visible `自动化/当前状态.json` does not
- confirm old round/stage scripts return deprecation guidance

## Proof Assets

- include one screenshot of the operating cockpit
- include one screenshot of the generated visual-kit directory
- include `SAMPLE-OUTPUTS.md` excerpts in the release post
- include `release/assets/repo-social-card.svg` as the repository social preview

## Post-Launch Loop

- collect founder reactions to the cockpit-first workflow
- track whether users understand the business loop faster than the old markdown-first version
- watch whether optional AI image prompts help users produce better launch collateral
