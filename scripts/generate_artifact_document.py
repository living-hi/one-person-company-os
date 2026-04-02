#!/usr/bin/env python3
"""Generate numbered DOCX artifact documents for One Person Company OS."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    emit_runtime_report,
    load_state,
    next_numbered_index,
    numbered_name,
    preflight_status,
    print_step,
    render_template,
    stage_label,
    write_docx,
    write_record,
)


CATEGORY_DIRS = {
    "delivery": "产物/01-实际交付",
    "software": "产物/02-软件与代码",
    "business": "产物/03-非软件与业务",
    "ops": "产物/04-部署与生产",
    "growth": "产物/05-上线与增长",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成带序号的正式 DOCX 产物。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--title", required=True, help="产物标题")
    parser.add_argument("--artifact-type", default="关键产物", help="产物类型")
    parser.add_argument(
        "--category",
        choices=["auto", "delivery", "software", "business", "ops", "growth"],
        default="auto",
        help="产物目录分类",
    )
    parser.add_argument("--summary", default="待补充本次产物摘要", help="产物摘要")
    parser.add_argument("--objective", default="", help="本次产物目标，默认读取当前回合目标")
    parser.add_argument("--owner-role", default="", help="负责人，默认读取当前回合负责人")
    parser.add_argument("--scope-in", action="append", default=[], help="本次纳入范围，可重复")
    parser.add_argument("--scope-out", action="append", default=[], help="本次不纳入范围，可重复")
    parser.add_argument("--deliverable", action="append", default=[], help="交付物，可重复")
    parser.add_argument("--software-output", action="append", default=[], help="软件/代码产出，可重复")
    parser.add_argument("--non-software-output", action="append", default=[], help="非软件产出，可重复")
    parser.add_argument("--evidence", action="append", default=[], help="证据或路径，可重复")
    parser.add_argument("--deployment-item", action="append", default=[], help="部署资料项，可重复")
    parser.add_argument("--production-item", action="append", default=[], help="生产/运维资料项，可重复")
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


def resolve_category(requested: str, artifact_type: str, state: dict[str, object]) -> str:
    if requested != "auto":
        return requested

    stage_id = state["stage_id"]
    artifact_key = artifact_type.lower()
    if any(token in artifact_type for token in ("部署", "生产", "回滚", "运维")) or any(
        token in artifact_key for token in ("deploy", "ops", "production")
    ):
        return "ops"
    if any(token in artifact_type for token in ("代码", "软件", "工程", "测试")) or any(
        token in artifact_key for token in ("software", "code", "engineering", "qa")
    ):
        return "software"
    if stage_id in {"launch", "grow"} and any(token in artifact_type for token in ("增长", "上线", "转化")):
        return "growth"
    if any(token in artifact_type for token in ("方案", "培训", "咨询", "销售", "运营", "研究", "材料")):
        return "business"
    return "delivery"


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
    owner_role = args.owner_role or current_round.get("owner_role_name", "待指定")
    objective = args.objective or current_round.get("goal", "待定义")
    next_action = args.next_action or current_round.get("next_action", "待定义")
    category = resolve_category(args.category, args.artifact_type, state)

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
        "ARTIFACT_SOFTWARE_OUTPUTS": to_bullets(args.software_output, "如为软件产品，请补齐代码、脚本、接口、配置或自动化产出"),
        "ARTIFACT_NON_SOFTWARE_OUTPUTS": to_bullets(
            args.non_software_output,
            "如为非软件产品，请补齐方案、培训材料、研究成果、销售材料或执行清单",
        ),
        "ARTIFACT_EVIDENCE": to_bullets(args.evidence, "待补充文件路径、仓库地址、演示链接或其他验收证据"),
        "ARTIFACT_DEPLOYMENT_ITEMS": to_bullets(
            args.deployment_item,
            "如已进入上线/运营，请补齐部署目标、发布窗口、回滚方案与配置变更",
        ),
        "ARTIFACT_PRODUCTION_ITEMS": to_bullets(
            args.production_item,
            "如已进入上线/运营，请补齐监控、告警、值守、事故响应和生产观察项",
        ),
        "ARTIFACT_CHANGES": to_bullets(args.change, "待补充本次变化"),
        "ARTIFACT_DECISIONS": to_bullets(args.decision, "待补充关键决策"),
        "ARTIFACT_RISKS": to_bullets(args.risk, "待补充风险与待确认事项"),
        "ARTIFACT_NEXT_ACTION": next_action,
    }

    print_step(4, 5, "执行与落盘")
    base_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else company_dir
    output_dir = base_dir / CATEGORY_DIRS[category]
    filename = numbered_name(next_numbered_index(output_dir), args.title, ".docx")
    output_path = output_dir / filename
    rendered = render_template("artifact-docx-ready-template.md", values)
    write_docx(output_path, rendered, title=args.title)

    record = write_record(
        company_dir,
        "推进日志",
        "文档产物",
        f"生成正式交付文档 {args.title}",
        [
            f"- 产物标题: {args.title}",
            f"- 产物类型: {args.artifact_type}",
            f"- 输出分类: {category}",
            f"- 当前阶段: {stage_label(state['stage_id'])}",
            f"- 当前回合: {current_round.get('name', '待定义')}",
            f"- 负责人: {owner_role}",
            f"- 实际文件: {output_path.name}",
            f"- 下一步最短动作: {next_action}",
        ],
    )

    print_step(5, 5, "验证与回报")
    emit_runtime_report(
        mode="生成正式交付文档",
        phase="验证与回报",
        stage=stage_label(state["stage_id"]),
        round_name=current_round.get("name", "待定义"),
        role=owner_role,
        artifact=f"{args.title} DOCX",
        next_action=next_action,
        needs_confirmation="否",
        persistence_mode="模式 A：脚本执行",
        company_dir=company_dir,
        saved_paths=[output_path, record],
        work_scope=[
            "为关键产物生成带序号的正式 DOCX 文件。",
            "把软件产出、非软件产出、证据以及部署/生产资料写成可交付格式。",
            "将文档真实落盘到工作区，不再只生成 Markdown 草稿。",
        ],
        non_scope=[
            "不会在产物目录里再生成未编号的 Markdown 文件。",
            "不会把缺少实际证据的内容说成已经完成交付。",
        ],
        changes=[
            f"已生成编号化 DOCX：{output_path.name}。",
            "已把实际软件/非软件产出、证据、部署与生产资料纳入正式结构。",
            "已新增一条文档产物生成记录，便于审计和回看。",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
