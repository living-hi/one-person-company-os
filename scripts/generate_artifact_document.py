#!/usr/bin/env python3
"""Generate standard artifact documents for One Person Company OS."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    emit_runtime_report,
    load_state,
    preflight_status,
    print_step,
    render_template,
    slugify,
    stage_label,
    write_record,
    write_text,
)


FORM_CONFIG = {
    "internal": {
        "label": "内部工作稿",
        "template": "artifact-internal-draft-template.md",
        "subdir": "产物/内部工作稿",
        "suffix": "内部工作稿",
    },
    "spec": {
        "label": "标准规范稿",
        "template": "artifact-standard-spec-template.md",
        "subdir": "产物/标准规范稿",
        "suffix": "标准规范稿",
    },
    "docx": {
        "label": "可转 DOCX 稿",
        "template": "artifact-docx-ready-template.md",
        "subdir": "产物/可转DOCX稿",
        "suffix": "可转DOCX稿",
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成关键产物的内部工作稿、标准规范稿和可转 DOCX 稿。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--title", required=True, help="产物标题")
    parser.add_argument("--artifact-type", default="关键产物", help="产物类型")
    parser.add_argument("--form", choices=["internal", "spec", "docx", "all"], default="all", help="输出稿型")
    parser.add_argument("--summary", default="待补充本次产物摘要", help="产物摘要")
    parser.add_argument("--objective", default="", help="本次产物目标，默认读取当前回合目标")
    parser.add_argument("--owner-role", default="", help="负责人，默认读取当前回合负责人")
    parser.add_argument("--scope-in", action="append", default=[], help="本次纳入范围，可重复")
    parser.add_argument("--scope-out", action="append", default=[], help="本次不纳入范围，可重复")
    parser.add_argument("--deliverable", action="append", default=[], help="交付物，可重复")
    parser.add_argument("--change", action="append", default=[], help="本次变化，可重复")
    parser.add_argument("--decision", action="append", default=[], help="关键决策，可重复")
    parser.add_argument("--risk", action="append", default=[], help="风险与待确认事项，可重复")
    parser.add_argument("--next-action", default="", help="下一步动作，默认读取当前回合")
    parser.add_argument("--output-dir", help="可选，自定义输出目录")
    return parser


def to_bullets(items: list[str], fallback: str) -> str:
    values = [item for item in items if item]
    if not values:
        values = [fallback]
    return "\n".join(f"- {item}" for item in values)


def selected_forms(form: str) -> list[str]:
    if form == "all":
        return ["internal", "spec", "docx"]
    return [form]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()

    print_step(1, 5, "模式判定")
    print_step(2, 5, "preflight 与保存策略检查")
    runtime = preflight_status(company_dir)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")

    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status="已完成（装载当前状态与文档参数）")
    state = load_state(company_dir)
    current_round = state["current_round"]
    forms = selected_forms(args.form)
    owner_role = args.owner_role or current_round.get("owner_role_name", "待指定")
    objective = args.objective or current_round.get("goal", "待定义")
    next_action = args.next_action or current_round.get("next_action", "待定义")
    artifact_slug = slugify(args.title)

    values = {
        "COMPANY_NAME": state["company_name"],
        "PRODUCT_NAME": state["product_name"],
        "STAGE_LABEL": stage_label(state["stage_id"]),
        "CURRENT_ROUND_NAME": current_round.get("name", "待定义"),
        "ROUND_GOAL": current_round.get("goal", "待定义"),
        "ROUND_STATUS": current_round.get("status", "待定义"),
        "ARTIFACT_TITLE": args.title,
        "ARTIFACT_TYPE": args.artifact_type,
        "ARTIFACT_OWNER": owner_role,
        "ARTIFACT_OBJECTIVE": objective,
        "ARTIFACT_SUMMARY": args.summary,
        "ARTIFACT_SCOPE_IN": to_bullets(args.scope_in, "待补充本次纳入范围"),
        "ARTIFACT_SCOPE_OUT": to_bullets(args.scope_out, "待补充本次不纳入范围"),
        "ARTIFACT_DELIVERABLES": to_bullets(args.deliverable, "待补充交付物"),
        "ARTIFACT_CHANGES": to_bullets(args.change, "待补充本次变化"),
        "ARTIFACT_DECISIONS": to_bullets(args.decision, "待补充关键决策"),
        "ARTIFACT_RISKS": to_bullets(args.risk, "待补充风险与待确认事项"),
        "ARTIFACT_NEXT_ACTION": next_action,
    }

    print_step(4, 5, "执行与落盘")
    saved_paths: list[Path] = []
    base_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else company_dir
    for form in forms:
        config = FORM_CONFIG[form]
        rendered = render_template(config["template"], values)
        output_path = base_dir / config["subdir"] / f"{artifact_slug}-{config['suffix']}.md"
        write_text(output_path, rendered)
        saved_paths.append(output_path)

    record = write_record(
        company_dir,
        "推进日志",
        "文档产物",
        f"生成文档产物 {args.title}",
        [
            f"- 产物标题: {args.title}",
            f"- 产物类型: {args.artifact_type}",
            f"- 稿型: {'、'.join(FORM_CONFIG[form]['label'] for form in forms)}",
            f"- 当前阶段: {stage_label(state['stage_id'])}",
            f"- 当前回合: {current_round.get('name', '待定义')}",
            f"- 负责人: {owner_role}",
            f"- 下一步最短动作: {next_action}",
        ],
    )
    saved_paths.append(record)

    print_step(5, 5, "验证与回报")
    emit_runtime_report(
        mode="生成关键产物文档",
        phase="验证与回报",
        stage=stage_label(state["stage_id"]),
        round_name=current_round.get("name", "待定义"),
        role=owner_role,
        artifact=f"{args.title} 文档包",
        next_action=next_action,
        needs_confirmation="否",
        persistence_mode="模式 A：脚本执行",
        company_dir=company_dir,
        saved_paths=saved_paths,
        work_scope=[
            "为关键产物生成内部工作稿、标准规范稿和可转 DOCX 稿。",
            "把本次变化、边界、交付物和风险整理成标准结构。",
            "将文档真实落盘到工作区，便于继续编辑或转 DOCX。",
        ],
        non_scope=[
            "不会只给一段聊天内容而不形成文件。",
            "不会混淆内部工作稿、标准规范稿和可转 DOCX 稿的用途。",
        ],
        changes=[
            f"已生成 {len(forms)} 种稿型：{'、'.join(FORM_CONFIG[form]['label'] for form in forms)}。",
            "已把产物摘要、范围、交付物、决策、风险和下一步动作写入标准模板。",
            "已新增一条文档产物生成记录，便于审计和回看。",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
