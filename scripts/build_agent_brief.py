#!/usr/bin/env python3
"""Build one or more role-agent briefs from the One Person Company OS manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "agent-brief"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build role-agent briefs from the one-person-company-os role manifests."
    )
    parser.add_argument(
        "--stage",
        choices=["Validate", "Build", "Launch", "Operate", "Grow"],
        required=True,
        help="Primary company stage for this work packet",
    )
    parser.add_argument(
        "--role",
        help="Single role id to emit, such as product-strategist or engineer-tech-lead",
    )
    parser.add_argument(
        "--all-stage-roles",
        action="store_true",
        help="Emit briefs for the default role set of the stage",
    )
    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="When used with --all-stage-roles, also include optional stage roles",
    )
    parser.add_argument(
        "--language",
        default="same-as-user",
        help="Working language to encode in the brief, such as zh-CN, en, or bilingual",
    )
    parser.add_argument("--company-name", default="Unnamed Company", help="Company name for the brief")
    parser.add_argument("--objective", default="Clarify and advance the next company milestone", help="Task objective")
    parser.add_argument(
        "--current-bottleneck",
        default="Not specified",
        help="Current bottleneck or problem this role should address",
    )
    parser.add_argument(
        "--next-required-artifact",
        default="Not specified",
        help="Main artifact expected after this role finishes",
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Extra input artifact or context. Repeat for multiple values.",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Override or extend required outputs. Repeat for multiple values.",
    )
    parser.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Hard constraint to include in the brief. Repeat for multiple values.",
    )
    parser.add_argument(
        "--approval-gate",
        action="append",
        default=[],
        help="Additional approval gate. Repeat for multiple values.",
    )
    parser.add_argument(
        "--pending-approval",
        action="append",
        default=[],
        help="Pending approval that the next role should be aware of. Repeat for multiple values.",
    )
    parser.add_argument(
        "--output-format",
        choices=["markdown", "json"],
        default="markdown",
        help="Brief output format",
    )
    parser.add_argument(
        "--output-dir",
        help="Write generated briefs to this directory. When omitted, single-role output is printed to stdout.",
    )
    return parser


def resolve_paths() -> tuple[Path, Path, Path]:
    root = Path(__file__).resolve().parent.parent
    roles_dir = root / "agents" / "roles"
    orchestration_dir = root / "orchestration"
    return root, roles_dir, orchestration_dir


def load_role_specs(roles_dir: Path) -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for path in sorted(roles_dir.glob("*.json")):
        spec = load_json(path)
        specs[spec["role_id"]] = spec
    return specs


def role_ids_for_stage(
    stage: str,
    stage_defaults: dict[str, Any],
    include_optional: bool,
) -> list[str]:
    role_ids = list(stage_defaults["stage_defaults"][stage])
    if include_optional:
        role_ids.extend(stage_defaults["stage_optional_roles"].get(stage, []))
    seen: set[str] = set()
    ordered: list[str] = []
    for role_id in role_ids:
        if role_id not in seen:
            ordered.append(role_id)
            seen.add(role_id)
    return ordered


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def build_packet(
    role_spec: dict[str, Any],
    *,
    stage: str,
    company_name: str,
    language: str,
    objective: str,
    current_bottleneck: str,
    next_required_artifact: str,
    extra_inputs: list[str],
    extra_artifacts: list[str],
    constraints: list[str],
    extra_approval_gates: list[str],
    pending_approvals: list[str],
) -> dict[str, Any]:
    required_outputs = unique(role_spec["outputs_required"] + extra_artifacts)
    approval_gates = unique(role_spec["approval_required_for"] + extra_approval_gates)
    return {
        "stage": stage,
        "working_language": language,
        "company_name": company_name,
        "role_id": role_spec["role_id"],
        "role_display_name": role_spec["display_name"],
        "objective": objective,
        "mission": role_spec["mission"],
        "owns": role_spec["owns"],
        "inputs": unique(role_spec["inputs_required"] + extra_inputs),
        "required_outputs": required_outputs,
        "constraints": constraints or ["Respect the founder as final decision-maker."],
        "approval_gates": approval_gates,
        "handoff_targets": role_spec["handoff_to"],
        "guardrails": role_spec["do_not_do"],
        "continuation_context": {
            "stage": stage,
            "current_bottleneck": current_bottleneck,
            "next_required_artifact": next_required_artifact,
            "pending_approvals": pending_approvals,
            "recommended_next_owner": role_spec["handoff_to"][0] if role_spec["handoff_to"] else "founder-ceo"
        }
    }


def format_markdown(packet: dict[str, Any], handoff_schema: dict[str, Any]) -> str:
    lines = [
        f"# Agent Brief: {packet['role_display_name']}",
        "",
        "## Session Frame",
        f"- Stage: {packet['stage']}",
        f"- Working language: {packet['working_language']}",
        f"- Company: {packet['company_name']}",
        f"- Objective: {packet['objective']}",
        "",
        "## Role Contract",
        f"- Role id: {packet['role_id']}",
        f"- Mission: {packet['mission']}",
        "",
        "## Ownership",
    ]
    lines.extend(f"- {item}" for item in packet["owns"])
    lines.extend([
        "",
        "## Inputs",
    ])
    lines.extend(f"- {item}" for item in packet["inputs"])
    lines.extend([
        "",
        "## Required Outputs",
    ])
    lines.extend(f"- {item}" for item in packet["required_outputs"])
    lines.extend([
        "",
        "## Constraints",
    ])
    lines.extend(f"- {item}" for item in packet["constraints"])
    lines.extend([
        "",
        "## Approval Gates",
    ])
    lines.extend(f"- {item}" for item in packet["approval_gates"])
    lines.extend([
        "",
        "## Handoff Targets",
    ])
    lines.extend(f"- {item}" for item in packet["handoff_targets"])
    lines.extend([
        "",
        "## Guardrails",
    ])
    lines.extend(f"- {item}" for item in packet["guardrails"])
    lines.extend([
        "",
        "## Continuation Context",
        f"- Current bottleneck: {packet['continuation_context']['current_bottleneck']}",
        f"- Next required artifact: {packet['continuation_context']['next_required_artifact']}",
        f"- Recommended next owner: {packet['continuation_context']['recommended_next_owner']}",
        "",
        "## Pending Approvals",
    ])
    pending = packet["continuation_context"]["pending_approvals"] or ["None recorded"]
    lines.extend(f"- {item}" for item in pending)
    lines.extend([
        "",
        "## Handoff Schema",
        f"- Required fields: {', '.join(handoff_schema['required_fields'])}",
    ])
    return "\n".join(lines) + "\n"


def write_packet(
    packet: dict[str, Any],
    *,
    output_format: str,
    output_dir: Path | None,
    handoff_schema: dict[str, Any],
) -> None:
    if output_format == "json":
        rendered = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
        suffix = ".json"
    else:
        rendered = format_markdown(packet, handoff_schema)
        suffix = ".md"

    if output_dir is None:
        print(rendered, end="")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{slugify(packet['role_id'])}{suffix}"
    path.write_text(rendered, encoding="utf-8")
    print(path)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.role and not args.all_stage_roles:
        parser.error("use --role for one brief or --all-stage-roles for the stage default set")

    _, roles_dir, orchestration_dir = resolve_paths()
    role_specs = load_role_specs(roles_dir)
    stage_defaults = load_json(orchestration_dir / "stage-defaults.json")
    handoff_schema = load_json(orchestration_dir / "handoff-schema.json")

    if args.role:
        role_ids = [args.role]
    else:
        role_ids = role_ids_for_stage(args.stage, stage_defaults, args.include_optional)

    missing = [role_id for role_id in role_ids if role_id not in role_specs]
    if missing:
        parser.error(f"unknown role ids: {', '.join(missing)}")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    if output_dir is None and len(role_ids) > 1:
        parser.error("multiple briefs require --output-dir")

    for role_id in role_ids:
        packet = build_packet(
            role_specs[role_id],
            stage=args.stage,
            company_name=args.company_name,
            language=args.language,
            objective=args.objective,
            current_bottleneck=args.current_bottleneck,
            next_required_artifact=args.next_required_artifact,
            extra_inputs=args.input,
            extra_artifacts=args.artifact,
            constraints=args.constraint,
            extra_approval_gates=args.approval_gate,
            pending_approvals=args.pending_approval,
        )
        write_packet(
            packet,
            output_format=args.output_format,
            output_dir=output_dir,
            handoff_schema=handoff_schema,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
