#!/usr/bin/env python3
"""Initialize a Chinese-first One Person Company OS workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    default_role_ids_for_stage,
    normalize_stage,
    now_string,
    render_workspace,
    safe_workspace_name,
    save_state,
    stage_label,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="创建 One Person Company OS 中文工作区。")
    parser.add_argument("company_name", help="公司名称")
    parser.add_argument("--path", required=True, help="工作区父目录")
    parser.add_argument("--product-name", default="未命名产品", help="产品名称")
    parser.add_argument("--stage", default="验证期", help="当前阶段，如 验证期、构建期、上线期")
    parser.add_argument("--target-user", default="待确认用户", help="目标用户")
    parser.add_argument("--core-problem", default="待确认核心问题", help="核心问题")
    parser.add_argument("--product-pitch", default="待补充产品一句话定义", help="产品一句话定义")
    parser.add_argument("--company-goal", default="先完成当前阶段最关键的一个回合", help="当前主目标")
    parser.add_argument("--current-bottleneck", default="尚未定义首个回合", help="当前瓶颈")
    parser.add_argument("--force", action="store_true", help="允许写入已存在目录")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    stage_id = normalize_stage(args.stage)
    root = Path(args.path).expanduser().resolve()
    company_dir = root / safe_workspace_name(args.company_name)
    if company_dir.exists() and not args.force:
        parser.error(f"target already exists: {company_dir}")

    active_roles = default_role_ids_for_stage(stage_id)
    state = {
        "version": "2.0",
        "language": "zh-CN",
        "company_name": args.company_name,
        "product_name": args.product_name,
        "stage_id": stage_id,
        "stage_label": stage_label(stage_id),
        "target_user": args.target_user,
        "core_problem": args.core_problem,
        "product_pitch": args.product_pitch,
        "company_goal": args.company_goal,
        "current_bottleneck": args.current_bottleneck,
        "active_roles": active_roles,
        "current_round": {
            "round_id": "未启动",
            "name": "未启动",
            "goal": "待定义",
            "status": "待定义",
            "owner_role_id": active_roles[1] if len(active_roles) > 1 else active_roles[0],
            "owner_role_name": "总控台",
            "artifact": "待定义",
            "blocker": "无",
            "next_action": "先确认首个推进回合",
            "success_criteria": "首个回合被明确并进入已拆解",
            "started_at": now_string(),
            "updated_at": now_string(),
        },
    }

    save_state(company_dir, state)
    render_workspace(company_dir, state)

    print(f"Created company workspace: {company_dir}")
    print("00-公司总览.md")
    print("04-当前回合.md")
    print("角色智能体/角色清单.md")
    print("自动化/当前状态.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
