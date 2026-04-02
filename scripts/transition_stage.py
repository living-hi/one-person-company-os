#!/usr/bin/env python3
"""Transition the company to another stage."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    default_role_ids_for_stage,
    load_role_specs,
    load_state,
    normalize_stage,
    now_string,
    render_workspace,
    save_state,
    stage_label,
    write_record,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="切换公司阶段。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--stage", required=True, help="新阶段")
    parser.add_argument("--reason", required=True, help="切换原因")
    parser.add_argument("--first-round-name", default="", help="新阶段首个回合名称")
    parser.add_argument("--first-round-goal", default="", help="新阶段首个回合目标")
    parser.add_argument("--first-round-owner", default="control-tower", help="新阶段首个回合负责人")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    role_specs = load_role_specs()
    new_stage_id = normalize_stage(args.stage)

    state["stage_id"] = new_stage_id
    state["stage_label"] = stage_label(new_stage_id)
    state["active_roles"] = default_role_ids_for_stage(new_stage_id)
    state["current_bottleneck"] = args.reason

    if args.first_round_name or args.first_round_goal:
        owner = args.first_round_owner
        if owner not in role_specs:
            parser.error(f"unknown role id: {owner}")
        state["current_round"] = {
            "round_id": f"{state['stage_label']}-首回合",
            "name": args.first_round_name or "新阶段首回合",
            "goal": args.first_round_goal or "待定义",
            "status": "已拆解",
            "owner_role_id": owner,
            "owner_role_name": role_specs[owner]["display_name"],
            "artifact": "待定义",
            "blocker": "无",
            "next_action": "启动新阶段的第一个最小动作",
            "success_criteria": "首个新阶段产物完成",
            "started_at": now_string(),
            "updated_at": now_string(),
        }
    else:
        state["current_round"]["status"] = "待定义"
        state["current_round"]["updated_at"] = now_string()

    save_state(company_dir, state)
    render_workspace(company_dir, state)

    record = write_record(
        company_dir,
        "决策记录",
        "阶段切换",
        f"阶段切换到 {state['stage_label']}",
        [
            f"- 新阶段: {state['stage_label']}",
            f"- 切换原因: {args.reason}",
            f"- 默认激活角色: {'、'.join(spec['display_name'] for role_id, spec in role_specs.items() if role_id in state['active_roles'])}",
        ],
    )
    print(company_dir / "02-当前阶段.md")
    print(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
