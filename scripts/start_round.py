#!/usr/bin/env python3
"""Start a new round in an existing One Person Company OS workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import load_role_specs, load_state, now_string, render_workspace, round_id_now, save_state, write_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="启动一个新回合。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--round-name", required=True, help="回合名称")
    parser.add_argument("--goal", required=True, help="回合目标")
    parser.add_argument("--owner", default="control-tower", help="负责角色 id")
    parser.add_argument("--artifact", default="待定义", help="关键产物")
    parser.add_argument("--next-action", default="开始执行第一个最小动作", help="下一步最短动作")
    parser.add_argument("--success-criteria", default="关键产物完成并可判断下一步", help="完成标准")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    role_specs = load_role_specs()

    if args.owner not in role_specs:
        parser.error(f"unknown role id: {args.owner}")

    round_id = round_id_now()
    state["current_round"] = {
        "round_id": round_id,
        "name": args.round_name,
        "goal": args.goal,
        "status": "已拆解",
        "owner_role_id": args.owner,
        "owner_role_name": role_specs[args.owner]["display_name"],
        "artifact": args.artifact,
        "blocker": "无",
        "next_action": args.next_action,
        "success_criteria": args.success_criteria,
        "started_at": now_string(),
        "updated_at": now_string(),
    }
    state["current_bottleneck"] = args.goal
    save_state(company_dir, state)
    render_workspace(company_dir, state)

    record = write_record(
        company_dir,
        "推进日志",
        "启动回合",
        f"启动回合 {args.round_name}",
        [
            f"- 回合编号: {round_id}",
            f"- 回合目标: {args.goal}",
            f"- 负责角色: {role_specs[args.owner]['display_name']}",
            f"- 关键产物: {args.artifact}",
            f"- 下一步最短动作: {args.next_action}",
        ],
    )
    print(company_dir / "04-当前回合.md")
    print(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
