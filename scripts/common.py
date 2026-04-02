#!/usr/bin/env python3
"""Shared helpers for the One Person Company OS workspace scripts."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "assets" / "templates"
ROLE_DIR = ROOT / "agents" / "roles"
ORCHESTRATION_DIR = ROOT / "orchestration"
STATE_PATH_PARTS = ("自动化", "当前状态.json")

STAGE_CONFIG = {
    "validate": {
        "label": "验证期",
        "goal": "确认问题、目标用户和愿意付费的信号。",
        "exit_criteria": "至少拿到足够明确的用户反馈与继续构建的理由。",
        "next_requirements": "问题定义稳定、目标用户清晰、第一版范围可收敛。",
        "risks": ["把假设当事实", "在没有证据前过早开发"],
    },
    "build": {
        "label": "构建期",
        "goal": "把核心产品路径做出来，并形成最小可交付结果。",
        "exit_criteria": "关键流程可跑通，具备最小验证或上线条件。",
        "next_requirements": "关键功能可用、质量边界清晰、上线准备就绪。",
        "risks": ["范围失控", "技术债堆积", "没有明确验收标准"],
    },
    "launch": {
        "label": "上线期",
        "goal": "把产品带到目标用户面前，并建立最小反馈闭环。",
        "exit_criteria": "产品已对外可访问，渠道和反馈路径跑通。",
        "next_requirements": "上线链路稳定、反馈可回收、关键问题有处理路径。",
        "risks": ["信息不一致", "上线无回滚", "渠道铺太多"],
    },
    "operate": {
        "label": "运营期",
        "goal": "维持产品稳定运行，并持续处理反馈与问题。",
        "exit_criteria": "关键问题处理机制稳定，指标和反馈进入可持续节奏。",
        "next_requirements": "留存和稳定性基本可控，优化方向明确。",
        "risks": ["问题积压", "缺少优先级", "数据无法解释"],
    },
    "grow": {
        "label": "增长期",
        "goal": "围绕获客、转化、留存和收益持续放大有效动作。",
        "exit_criteria": "有清晰的增长杠杆与投入产出判断。",
        "next_requirements": "实验机制可持续，财务边界清晰。",
        "risks": ["过早铺渠道", "用噪音替代有效增长", "忽视现金流"],
    },
}

STAGE_ALIASES = {
    "validate": "validate",
    "validation": "validate",
    "验证": "validate",
    "验证期": "validate",
    "build": "build",
    "构建": "build",
    "构建期": "build",
    "launch": "launch",
    "上线": "launch",
    "上线期": "launch",
    "operate": "operate",
    "运营": "operate",
    "运营期": "operate",
    "grow": "grow",
    "增长": "grow",
    "增长期": "grow",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def safe_workspace_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", value).strip()
    return cleaned or "未命名公司"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "record"


def normalize_stage(value: str) -> str:
    key = value.strip().lower()
    if key not in STAGE_ALIASES:
        raise ValueError(f"unknown stage: {value}")
    return STAGE_ALIASES[key]


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def round_id_now() -> str:
    return datetime.now().strftime("R%Y%m%d%H%M")


def format_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- 无"


def render_template(template_name: str, values: dict[str, str]) -> str:
    template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def load_role_specs() -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for path in sorted(ROLE_DIR.glob("*.json")):
        spec = load_json(path)
        specs[spec["role_id"]] = spec
    return specs


def load_stage_defaults() -> dict[str, Any]:
    return load_json(ORCHESTRATION_DIR / "stage-defaults.json")


def default_role_ids_for_stage(stage_id: str) -> list[str]:
    return list(load_stage_defaults()["stage_defaults"][stage_id])


def stage_label(stage_id: str) -> str:
    return STAGE_CONFIG[stage_id]["label"]


def state_path(company_dir: Path) -> Path:
    return company_dir.joinpath(*STATE_PATH_PARTS)


def ensure_workspace_dirs(company_dir: Path) -> None:
    for relative in [
        "",
        "角色智能体",
        "流程",
        "产物/产品",
        "产物/增长",
        "产物/运营",
        "记录/推进日志",
        "记录/决策记录",
        "记录/校准记录",
        "自动化",
    ]:
        (company_dir / relative).mkdir(parents=True, exist_ok=True)


def save_state(company_dir: Path, state: dict[str, Any]) -> None:
    ensure_workspace_dirs(company_dir)
    write_text(state_path(company_dir), json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def load_state(company_dir: Path) -> dict[str, Any]:
    return load_json(state_path(company_dir))


def role_display_names(role_ids: list[str], role_specs: dict[str, dict[str, Any]]) -> list[str]:
    return [role_specs[role_id]["display_name"] for role_id in role_ids if role_id in role_specs]


def role_spec(role_id: str, role_specs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if role_id not in role_specs:
        raise ValueError(f"unknown role id: {role_id}")
    return role_specs[role_id]


def write_record(company_dir: Path, subdir: str, suffix: str, title: str, lines: list[str]) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = company_dir / "记录" / subdir / f"{timestamp}-{suffix}.md"
    content = "\n".join([f"# {title}", "", *lines]) + "\n"
    write_text(path, content)
    return path


def render_workspace(company_dir: Path, state: dict[str, Any]) -> None:
    role_specs = load_role_specs()
    ensure_workspace_dirs(company_dir)

    stage_id = state["stage_id"]
    stage = STAGE_CONFIG[stage_id]
    active_roles = state.get("active_roles") or default_role_ids_for_stage(stage_id)
    active_display = role_display_names(active_roles, role_specs)
    available_display = [
        spec["display_name"]
        for role_id, spec in sorted(role_specs.items())
        if role_id not in active_roles
    ]
    current_round = state.get("current_round", {})

    round_name = current_round.get("name", "未启动")
    round_owner = current_round.get("owner_role_name", "待指定")
    round_next_action = current_round.get("next_action", "待定义")

    common_values = {
        "COMPANY_NAME": state["company_name"],
        "PRODUCT_NAME": state["product_name"],
        "STAGE_LABEL": stage["label"],
        "UPDATED_AT": now_string(),
        "COMPANY_GOAL": state["company_goal"],
        "CURRENT_BOTTLENECK": state["current_bottleneck"],
        "CURRENT_ROUND_NAME": round_name,
        "CURRENT_NEXT_ACTION": round_next_action,
        "TARGET_USER": state["target_user"],
        "CORE_PROBLEM": state["core_problem"],
        "PRODUCT_PITCH": state["product_pitch"],
        "STAGE_GOAL": stage["goal"],
        "STAGE_EXIT_CRITERIA": stage["exit_criteria"],
        "NEXT_STAGE_REQUIREMENTS": stage["next_requirements"],
        "STAGE_RISKS": format_list(stage["risks"]),
        "ACTIVE_ROLE_LIST": format_list(active_display),
        "AVAILABLE_ROLE_LIST": format_list(available_display),
        "ACTIVE_ROLE_INLINE": "、".join(active_display) or "无",
    }

    write_text(company_dir / "00-公司总览.md", render_template("company-overview-template.md", common_values))
    write_text(company_dir / "01-产品定位.md", render_template("product-positioning-template.md", common_values))
    write_text(company_dir / "02-当前阶段.md", render_template("current-stage-template.md", common_values))
    write_text(company_dir / "03-组织架构.md", render_template("organization-template.md", common_values))

    round_values = dict(common_values)
    round_values.update(
        {
            "ROUND_ID": current_round.get("round_id", "未启动"),
            "ROUND_NAME": round_name,
            "ROUND_STATUS": current_round.get("status", "待定义"),
            "ROUND_OWNER": round_owner,
            "ROUND_GOAL": current_round.get("goal", "待定义"),
            "ROUND_ARTIFACT": current_round.get("artifact", "待定义"),
            "ROUND_BLOCKER": current_round.get("blocker", "无"),
            "ROUND_NEXT_ACTION": round_next_action,
            "ROUND_SUCCESS_CRITERIA": current_round.get("success_criteria", "待定义"),
            "ROUND_STARTED_AT": current_round.get("started_at", "未启动"),
            "ROUND_UPDATED_AT": current_round.get("updated_at", "未启动"),
        }
    )
    write_text(company_dir / "04-当前回合.md", render_template("current-round-template.md", round_values))
    write_text(company_dir / "05-推进规则.md", render_template("execution-rules-template.md", common_values))
    write_text(company_dir / "06-触发器与校准规则.md", render_template("calibration-rules-template.md", common_values))

    write_text(company_dir / "角色智能体" / "角色清单.md", render_template("role-index-template.md", common_values))
    for role_id in active_roles:
        spec = role_spec(role_id, role_specs)
        role_values = {
            "ROLE_NAME": spec["display_name"],
            "ROLE_MISSION": spec["mission"],
            "ROLE_OWNS": format_list(spec["owns"]),
            "ROLE_INPUTS": format_list(spec["inputs_required"]),
            "ROLE_OUTPUTS": format_list(spec["outputs_required"]),
            "ROLE_GUARDRAILS": format_list(spec["do_not_do"]),
            "ROLE_APPROVALS": format_list(spec["approval_required_for"]),
            "ROLE_HANDOFFS": format_list(role_display_names(spec["handoff_to"], role_specs)),
        }
        filename = spec.get("workspace_filename", spec["display_name"])
        write_text(company_dir / "角色智能体" / f"{filename}.md", render_template("role-brief-template.md", role_values))

    write_text(company_dir / "流程" / "创建公司流程.md", render_template("bootstrap-flow-template.md", common_values))
    write_text(company_dir / "流程" / "推进回合流程.md", render_template("round-flow-template.md", common_values))
    write_text(company_dir / "流程" / "校准回合流程.md", render_template("calibration-flow-template.md", common_values))
    write_text(company_dir / "流程" / "阶段切换流程.md", render_template("stage-flow-template.md", common_values))
    write_text(company_dir / "自动化" / "提醒规则.md", render_template("reminder-rules-template.md", common_values))
    write_text(company_dir / "自动化" / "定时任务定义.md", render_template("scheduler-spec-template.md", common_values))
