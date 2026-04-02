#!/usr/bin/env python3
"""Build role-agent briefs for One Person Company OS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import (
    load_json,
    load_role_specs,
    load_stage_defaults,
    normalize_stage,
    role_display_names,
    role_spec,
    stage_label,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成一个或多个角色智能体 brief。")
    parser.add_argument("--stage", required=True, help="阶段，如 构建期 或 build")
    parser.add_argument("--role", help="单个角色 id")
    parser.add_argument("--all-default-roles", action="store_true", help="输出该阶段的默认角色集")
    parser.add_argument("--include-optional", action="store_true", help="同时包含阶段可选角色")
    parser.add_argument("--language", default="zh-CN", help="工作语言")
    parser.add_argument("--company-name", default="未命名公司", help="公司名称")
    parser.add_argument("--objective", default="推进当前阶段的关键回合", help="当前目标")
    parser.add_argument("--current-round", default="当前回合待定义", help="当前回合名称")
    parser.add_argument("--round-goal", default="待定义", help="当前回合目标")
    parser.add_argument("--current-bottleneck", default="待确认", help="当前瓶颈")
    parser.add_argument("--trigger-reason", default="无", help="触发原因")
    parser.add_argument("--next-shortest-action", default="待确认", help="下一步最短动作")
    parser.add_argument("--input", action="append", default=[], help="补充输入，可重复")
    parser.add_argument("--artifact", action="append", default=[], help="补充输出，可重复")
    parser.add_argument("--constraint", action="append", default=[], help="补充约束，可重复")
    parser.add_argument("--approval-gate", action="append", default=[], help="补充审批点，可重复")
    parser.add_argument("--pending-approval", action="append", default=[], help="待创始人确认事项")
    parser.add_argument("--output-format", choices=["markdown", "json"], default="markdown", help="输出格式")
    parser.add_argument("--output-dir", help="批量写入的目录")
    return parser


def unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def role_ids_for_stage(stage_id: str, include_optional: bool) -> list[str]:
    defaults = load_stage_defaults()
    role_ids = list(defaults["stage_defaults"][stage_id])
    if include_optional:
        role_ids.extend(defaults["stage_optional_roles"].get(stage_id, []))
    return unique(role_ids)


def build_packet(
    spec: dict[str, Any],
    *,
    stage_id: str,
    role_specs: dict[str, dict[str, Any]],
    company_name: str,
    language: str,
    objective: str,
    current_round: str,
    round_goal: str,
    current_bottleneck: str,
    trigger_reason: str,
    next_shortest_action: str,
    extra_inputs: list[str],
    extra_artifacts: list[str],
    constraints: list[str],
    extra_approval_gates: list[str],
    pending_approvals: list[str],
) -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "stage_label": stage_label(stage_id),
        "working_language": language,
        "company_name": company_name,
        "role_id": spec["role_id"],
        "role_display_name": spec["display_name"],
        "objective": objective,
        "current_round": current_round,
        "round_goal": round_goal,
        "mission": spec["mission"],
        "owns": spec["owns"],
        "inputs": unique(spec["inputs_required"] + extra_inputs),
        "required_outputs": unique(spec["outputs_required"] + extra_artifacts),
        "constraints": constraints or ["尊重创始人是最终决策者。"],
        "approval_gates": unique(spec["approval_required_for"] + extra_approval_gates),
        "handoff_targets": role_display_names(spec["handoff_to"], role_specs),
        "guardrails": spec["do_not_do"],
        "continuation_context": {
            "round_id": current_round,
            "round_status": "待确认",
            "current_bottleneck": current_bottleneck,
            "trigger_reason": trigger_reason,
            "next_shortest_action": next_shortest_action,
            "pending_approvals": pending_approvals,
            "recommended_next_owner": role_display_names(spec["handoff_to"][:1], role_specs)[0]
            if spec["handoff_to"]
            else "创始人",
        },
    }


def format_markdown(packet: dict[str, Any], schema: dict[str, Any]) -> str:
    lines = [
        f"# 角色 Brief: {packet['role_display_name']}",
        "",
        "## 会话框架",
        f"- 阶段: {packet['stage_label']}",
        f"- 工作语言: {packet['working_language']}",
        f"- 公司: {packet['company_name']}",
        f"- 当前回合: {packet['current_round']}",
        f"- 回合目标: {packet['round_goal']}",
        f"- 当前目标: {packet['objective']}",
        "",
        "## 角色使命",
        f"- 角色 ID: {packet['role_id']}",
        f"- 使命: {packet['mission']}",
        "",
        "## 负责范围",
    ]
    lines.extend(f"- {item}" for item in packet["owns"])
    lines.extend(["", "## 输入"])
    lines.extend(f"- {item}" for item in packet["inputs"])
    lines.extend(["", "## 输出"])
    lines.extend(f"- {item}" for item in packet["required_outputs"])
    lines.extend(["", "## 约束"])
    lines.extend(f"- {item}" for item in packet["constraints"])
    lines.extend(["", "## 审批点"])
    lines.extend(f"- {item}" for item in packet["approval_gates"])
    lines.extend(["", "## 默认交接对象"])
    lines.extend(f"- {item}" for item in packet["handoff_targets"])
    lines.extend(["", "## 不该做的事"])
    lines.extend(f"- {item}" for item in packet["guardrails"])
    lines.extend(
        [
            "",
            "## 延续上下文",
            f"- 当前瓶颈: {packet['continuation_context']['current_bottleneck']}",
            f"- 触发原因: {packet['continuation_context']['trigger_reason']}",
            f"- 下一步最短动作: {packet['continuation_context']['next_shortest_action']}",
            f"- 推荐下一负责人: {packet['continuation_context']['recommended_next_owner']}",
            "",
            "## 待确认事项",
        ]
    )
    pending = packet["continuation_context"]["pending_approvals"] or ["无"]
    lines.extend(f"- {item}" for item in pending)
    lines.extend(["", "## Schema", f"- 必填字段: {', '.join(schema['required_fields'])}"])
    return "\n".join(lines) + "\n"


def write_packet(packet: dict[str, Any], output_format: str, output_dir: Path | None, schema: dict[str, Any]) -> None:
    if output_format == "json":
        rendered = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
        suffix = ".json"
    else:
        rendered = format_markdown(packet, schema)
        suffix = ".md"

    if output_dir is None:
        print(rendered, end="")
        return

    filename = packet["role_display_name"] + suffix
    write_text(output_dir / filename, rendered)
    print(output_dir / filename)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.role and not args.all_default_roles:
        parser.error("use --role or --all-default-roles")

    stage_id = normalize_stage(args.stage)
    role_specs = load_role_specs()
    schema = load_json(Path(__file__).resolve().parent.parent / "orchestration" / "handoff-schema.json")

    if args.role:
        role_ids = [args.role]
    else:
        role_ids = role_ids_for_stage(stage_id, args.include_optional)

    missing = [role_id for role_id in role_ids if role_id not in role_specs]
    if missing:
        parser.error(f"unknown role ids: {', '.join(missing)}")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    if output_dir is None and len(role_ids) > 1:
        parser.error("multiple briefs require --output-dir")

    for role_id in role_ids:
        packet = build_packet(
            role_spec(role_id, role_specs),
            stage_id=stage_id,
            role_specs=role_specs,
            company_name=args.company_name,
            language=args.language,
            objective=args.objective,
            current_round=args.current_round,
            round_goal=args.round_goal,
            current_bottleneck=args.current_bottleneck,
            trigger_reason=args.trigger_reason,
            next_shortest_action=args.next_shortest_action,
            extra_inputs=args.input,
            extra_artifacts=args.artifact,
            constraints=args.constraint,
            extra_approval_gates=args.approval_gate,
            pending_approvals=args.pending_approval,
        )
        write_packet(packet, args.output_format, output_dir, schema)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
