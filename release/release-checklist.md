# Release Checklist

## Positioning

- keep the primary audience as AI-native solo founders and independent builders
- keep the primary mental model as `创建公司 -> 启动回合 -> 推进回合 -> 校准 -> 切阶段`
- avoid reintroducing week-based positioning as the main loop

## Repository

- verify `README.md`, `README.zh-CN.md`, and `SKILL.md` describe the same product
- verify `agents/openai.yaml` matches the current positioning
- run `python3 scripts/validate_release.py`
- confirm the Chinese-first workspace scripts still pass

## Proof Assets

- include one screenshot of the generated Chinese workspace
- include one screenshot of `00-公司总览.md`
- include one screenshot of `04-当前回合.md`
- include `SAMPLE-OUTPUTS.md` excerpts in the release post

## Post-Launch Loop

- collect founder reactions to the new round-based workflow
- watch which first prompt users actually copy
- track whether users understand `总控台` quickly
- tighten the setup draft if users still ask too many clarifying questions
