#!/usr/bin/env python3
"""Update the current round state."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import load_role_specs, load_state, now_string, render_workspace, save_state, write_record


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
    print(company_dir / "04-当前回合.md")
    print(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
