#!/usr/bin/env python3
"""Create a calibration record and update the current round."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import load_role_specs, load_state, now_string, render_workspace, save_state, write_record


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
    print(company_dir / "04-当前回合.md")
    print(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
