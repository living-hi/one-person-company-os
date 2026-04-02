#!/usr/bin/env python3
"""Update the current round state."""

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
    parser = argparse.ArgumentParser(description="更新当前回合。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--status", choices=["待定义", "已拆解", "执行中", "待校准", "待决策", "已完成"], help="新状态")
    parser.add_argument("--owner", help="新负责角色 id")
    parser.add_argument("--artifact", help="关键产物")
    parser.add_argument("--blocker", help="当前阻塞")
    parser.add_argument("--next-action", help="下一步最短动作")
    parser.add_argument("--success-criteria", help="完成标准")
    parser.add_argument("--note", default="", help="更新说明")
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
    if args.status:
        current_round["status"] = args.status
    if args.artifact:
        current_round["artifact"] = args.artifact
    if args.blocker is not None:
        current_round["blocker"] = args.blocker
    if args.next_action:
        current_round["next_action"] = args.next_action
    if args.success_criteria:
        current_round["success_criteria"] = args.success_criteria

    current_round["updated_at"] = now_string()
    if args.blocker:
        state["current_bottleneck"] = args.blocker

    print_step(4, 5, "执行与落盘")
    save_state(company_dir, state)
    render_workspace(company_dir, state)

    lines = [
        f"- 回合编号: {current_round['round_id']}",
        f"- 当前状态: {current_round['status']}",
        f"- 负责角色: {current_round['owner_role_name']}",
        f"- 当前阻塞: {current_round['blocker']}",
        f"- 下一步最短动作: {current_round['next_action']}",
    ]
    if args.note:
        lines.append(f"- 更新说明: {args.note}")
    record = write_record(company_dir, "推进日志", "回合更新", f"回合更新 {current_round['name']}", lines)

    print_step(5, 5, "验证与回报")
    emit_runtime_report(
        mode="推进回合",
        phase="验证与回报",
        stage=state["stage_label"],
        round_name=current_round["name"],
        role=current_round["owner_role_name"],
        artifact=current_round["artifact"],
        next_action=current_round["next_action"],
        needs_confirmation="是" if current_round["status"] == "待决策" else "否",
        persistence_mode="模式 A：脚本执行",
        company_dir=company_dir,
        saved_paths=[
            company_dir / "04-当前回合.md",
            record,
            state_path(company_dir),
        ],
        work_scope=[
            "更新当前回合的状态、负责人、阻塞或下一步动作。",
            "把回合变化真实写回工作区。",
            "明确这次更新后是否需要创始人确认。",
        ],
        non_scope=[
            "不会重建整套公司设计。",
            "不会把旧状态留在工作区里不更新。",
        ],
        changes=[
            f"已把当前回合状态更新为 {current_round['status']}。",
            f"当前阻塞为 {current_round['blocker']}。",
            f"下一步最短动作已更新为 {current_round['next_action']}。",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
