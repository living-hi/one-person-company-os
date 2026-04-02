#!/usr/bin/env python3
"""Run a runtime preflight check for One Person Company OS."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="检查 One Person Company OS 的运行环境与保存状态。")
    parser.add_argument("--mode", default="创建公司", help="当前准备执行的模式标签")
    parser.add_argument("--company-dir", help="可选，公司工作区目录")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve() if args.company_dir else None

    print_step(1, 5, "模式判定")
    print_step(2, 5, "preflight 与保存策略检查")
    status = preflight_status(company_dir)
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status="已完成（读取当前工作区）")
    print_step(4, 5, "执行与落盘", status="跳过（本次只做预检与策略判定）")

    stage = "未确认"
    round_name = "未确认"
    role = "总控台"
    next_action = "环境可运行后再执行正式创建或更新"
    if company_dir and status["workspace_created"] and status["persisted"]:
        state = load_state(company_dir)
        stage = state.get("stage_label", stage)
        round_name = state.get("current_round", {}).get("name", round_name)
        role = state.get("current_round", {}).get("owner_role_name", role)
        next_action = state.get("current_round", {}).get("next_action", next_action)

    if status["recommended_mode"] == "模式 A：脚本执行（切换兼容 Python）":
        next_action = "优先让 OpenClaw 智能体切换到兼容 Python 后重跑脚本"
    elif status["recommended_mode"] == "模式 B：手动落盘" and not status["python_supported"] and status["writable"]:
        next_action = "优先让 OpenClaw 智能体运行 scripts/ensure_python_runtime.py --apply；若恢复失败，再切到手动落盘"
    elif status["recommended_mode"] == "模式 B：手动落盘":
        next_action = "跳过脚本执行，直接手动写入 markdown/json 到工作区"
    if status["recommended_mode"] == "模式 C：纯对话推进":
        next_action = "先解释当前内容未保存，再等待用户确认或修复环境"

    print_step(5, 5, "验证与回报")
    emit_runtime_report(
        mode=args.mode,
        phase="验证与回报",
        stage=stage,
        round_name=round_name,
        role=role,
        artifact="运行环境检查结果",
        next_action=next_action,
        needs_confirmation="否",
        persistence_mode=status["recommended_mode"],
        company_dir=company_dir,
        saved_paths=[],
        unsaved_reason="本次仅执行预检，没有新增落盘",
        work_scope=[
            "检查当前环境能不能直接运行脚本。",
            "判断现在该走脚本执行、手动落盘还是纯对话推进。",
            "把保存状态和恢复动作翻译成用户可理解的话。",
        ],
        non_scope=[
            "不会在这一步创建新公司文件。",
            "不会把预检结果冒充成正式执行结果。",
        ],
        changes=[
            f"已确认当前推荐执行模式为 {status['recommended_mode']}。",
            "本次没有写入新文件，只更新了对环境与保存策略的判断。",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
