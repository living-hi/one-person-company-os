#!/usr/bin/env python3
"""Persist a checkpoint for the current company workspace state."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, now_string, preflight_status, print_step, render_workspace, save_state, state_path, write_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="把当前公司状态保存为一个检查点。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--reason", required=True, help="为什么要保存这个检查点")
    parser.add_argument("--artifact", help="当前关键产物，默认读取当前回合")
    parser.add_argument("--next-action", help="下一步最短动作，默认读取当前回合")
    parser.add_argument("--note", default="", help="补充说明")
    parser.add_argument("--needs-founder-approval", action="store_true", help="是否需要创始人确认")
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
    current_round = state["current_round"]
    artifact = args.artifact or current_round.get("artifact", "待定义")
    next_action = args.next_action or current_round.get("next_action", "待定义")

    state["last_checkpoint"] = {
        "saved_at": now_string(),
        "reason": args.reason,
        "artifact": artifact,
        "next_action": next_action,
        "needs_founder_approval": args.needs_founder_approval,
        "note": args.note,
    }

    print_step(4, 5, "执行与落盘")
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    lines = [
        f"- 保存时间: {state['last_checkpoint']['saved_at']}",
        f"- 当前阶段: {state['stage_label']}",
        f"- 当前回合: {current_round['name']}",
        f"- 当前状态: {current_round['status']}",
        f"- 当前关键产物: {artifact}",
        f"- 当前阻塞: {current_round['blocker']}",
        f"- 下一步最短动作: {next_action}",
        f"- 保存原因: {args.reason}",
        f"- 是否需要创始人确认: {'是' if args.needs_founder_approval else '否'}",
    ]
    if args.note:
        lines.append(f"- 备注: {args.note}")
    checkpoint = write_record(company_dir, "检查点", "检查点", f"检查点 {current_round['name']}", lines)

    print_step(5, 5, "验证与回报")
    emit_runtime_report(
        mode="保存检查点",
        phase="验证与回报",
        stage=state["stage_label"],
        round_name=current_round["name"],
        role=current_round["owner_role_name"],
        artifact=artifact,
        next_action=next_action,
        needs_confirmation="是" if args.needs_founder_approval else "否",
        persistence_mode="模式 A：脚本执行",
        company_dir=company_dir,
        saved_paths=[
            checkpoint,
            company_dir / "04-当前回合.md",
            state_path(company_dir),
        ],
        work_scope=[
            "把当前阶段、当前回合和下一步动作保存成一个可恢复检查点。",
            "把检查点理由与备注写入记录文件。",
            "确认这次检查点是否需要创始人进一步拍板。",
        ],
        non_scope=[
            "不会只在聊天里说已保存而不落盘。",
            "不会丢失当前回合的关键上下文。",
        ],
        changes=[
            f"已保存新的检查点，原因是：{args.reason}。",
            f"检查点覆盖当前关键产物：{artifact}。",
            f"下一步最短动作记录为：{next_action}。",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
