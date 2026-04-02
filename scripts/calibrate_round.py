#!/usr/bin/env python3
"""Create a calibration record and update the current round."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    emit_runtime_report,
    load_role_specs,
    load_state,
    now_string,
    preflight_status,
    print_step,
    render_workspace,
    save_state,
    state_path,
    write_record,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="记录一次回合校准。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--reason", required=True, help="触发原因")
    parser.add_argument("--finding", default="待补充结论", help="校准结论")
    parser.add_argument("--next-action", required=True, help="校准后的下一步最短动作")
    parser.add_argument("--owner", help="校准后负责人角色 id")
    parser.add_argument("--needs-founder-approval", action="store_true", help="是否需要创始人拍板")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()

    print_step(1, 5, "模式判定")
    print_step(2, 5, "preflight 与保存策略检查")
    runtime = preflight_status(company_dir)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")

    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status="已完成（加载当前状态）")
    state = load_state(company_dir)
    role_specs = load_role_specs()
    current_round = state["current_round"]

    if args.owner:
        if args.owner not in role_specs:
            parser.error(f"unknown role id: {args.owner}")
        current_round["owner_role_id"] = args.owner
        current_round["owner_role_name"] = role_specs[args.owner]["display_name"]

    current_round["status"] = "待决策" if args.needs_founder_approval else "待校准"
    current_round["blocker"] = args.reason
    current_round["next_action"] = args.next_action
    current_round["updated_at"] = now_string()
    state["current_bottleneck"] = args.reason

    print_step(4, 5, "执行与落盘")
    save_state(company_dir, state)
    render_workspace(company_dir, state)

    record = write_record(
        company_dir,
        "校准记录",
        "校准",
        f"校准记录 {current_round['name']}",
        [
            f"- 回合编号: {current_round['round_id']}",
            f"- 触发原因: {args.reason}",
            f"- 当前结论: {args.finding}",
            f"- 调整后负责人: {current_round['owner_role_name']}",
            f"- 下一步最短动作: {args.next_action}",
            f"- 是否需要创始人确认: {'是' if args.needs_founder_approval else '否'}",
        ],
    )

    print_step(5, 5, "验证与回报")
    emit_runtime_report(
        mode="校准回合",
        phase="验证与回报",
        stage=state["stage_label"],
        round_name=current_round["name"],
        role=current_round["owner_role_name"],
        artifact=current_round["artifact"],
        next_action=args.next_action,
        needs_confirmation="是" if args.needs_founder_approval else "否",
        persistence_mode="模式 A：脚本执行",
        company_dir=company_dir,
        saved_paths=[
            company_dir / "04-当前回合.md",
            record,
            state_path(company_dir),
        ],
        work_scope=[
            "记录这次为什么进入校准。",
            "更新回合状态、负责人和下一步最短动作。",
            "把校准结论写入工作区，便于后续接力。",
        ],
        non_scope=[
            "不会用长篇空泛建议替代校准结论。",
            "不会省略是否需要创始人拍板。",
        ],
        changes=[
            f"已记录本次校准原因：{args.reason}。",
            f"已把下一步最短动作更新为 {args.next_action}。",
            f"当前是否需要创始人确认：{'是' if args.needs_founder_approval else '否'}。",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
