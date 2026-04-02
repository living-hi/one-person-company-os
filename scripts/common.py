#!/usr/bin/env python3
"""Shared helpers for the One Person Company OS workspace scripts."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, TextIO


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = ROOT / "scripts"
TEMPLATE_DIR = ROOT / "assets" / "templates"
ROLE_DIR = ROOT / "agents" / "roles"
ORCHESTRATION_DIR = ROOT / "orchestration"
STATE_PATH_PARTS = ("自动化", "当前状态.json")
CORE_WORKSPACE_FILES = (
    "00-公司总览.md",
    "04-当前回合.md",
    "自动化/当前状态.json",
)
REQUIRED_SCRIPT_NAMES = (
    "init_company.py",
    "build_agent_brief.py",
    "generate_artifact_document.py",
    "start_round.py",
    "update_round.py",
    "calibrate_round.py",
    "transition_stage.py",
    "preflight_check.py",
    "ensure_python_runtime.py",
    "checkpoint_save.py",
    "validate_release.py",
)
MIN_SUPPORTED_PYTHON = (3, 7)
PYTHON_CANDIDATE_COMMANDS = (
    "python3.13",
    "python3.12",
    "python3.11",
    "python3.10",
    "python3.9",
    "python3.8",
    "python3.7",
    "python3",
    "python",
)

STEP_CATALOG = {
    1: {
        "system": "模式判定",
        "human": "先判断这次要进入哪个流程",
    },
    2: {
        "system": "preflight 与保存策略检查",
        "human": "先确认环境、保存条件和执行方式",
    },
    3: {
        "system": "草案 / 变更提议 / 当前状态装载",
        "human": "先装载现状，再准备草案或变更",
    },
    4: {
        "system": "执行与落盘",
        "human": "开始执行，并把结果写入工作区",
    },
    5: {
        "system": "验证与回报",
        "human": "核对结果、说明变化并给出回报",
    },
}

STEP_ALIASES = {
    "模式判定": 1,
    "环境检查": 2,
    "preflight 与保存策略检查": 2,
    "工作区检查": 3,
    "组装初始状态": 3,
    "加载当前状态": 3,
    "组装角色 Brief": 3,
    "草案 / 变更提议 / 当前状态装载": 3,
    "保存策略判定": 4,
    "执行与落盘": 4,
    "验证与回报": 5,
}

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
    slug = re.sub(r"[^\w]+", "-", value.strip().lower(), flags=re.UNICODE).strip("-_")
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


def bool_label(value: bool) -> str:
    return "是" if value else "否"


def bool_audit_label(value: bool) -> str:
    return "通过" if value else "未通过"


def joined_text(values: Iterable[str]) -> str:
    cleaned = [value for value in values if value]
    return "；".join(cleaned) if cleaned else "无"


def display_path(path: Path, root: Optional[Path] = None) -> str:
    if root is not None:
        try:
            return str(path.relative_to(root))
        except ValueError:
            pass
    return str(path)


def version_text(version: tuple[int, ...]) -> str:
    return ".".join(str(part) for part in version)


def python_compatibility_label(version: tuple[int, ...]) -> str:
    return f"Python {version_text(version)}"


def is_python_version_supported(version: tuple[int, ...]) -> bool:
    return version >= MIN_SUPPORTED_PYTHON


def probe_python(executable: str) -> Optional[dict[str, Any]]:
    command = [executable, "-c", "import json, sys; print(json.dumps({'executable': sys.executable, 'version': list(sys.version_info[:3])}, ensure_ascii=False))"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError, OSError):
        return None
    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        return None

    version = tuple(int(part) for part in payload.get("version", [])[:3])
    executable_path = str(payload.get("executable", executable))
    if len(version) < 3 or not executable_path:
        return None

    return {
        "executable": executable_path,
        "version": version,
        "supported": is_python_version_supported(version),
    }


def discover_python_runtimes() -> list[dict[str, Any]]:
    candidates = [sys.executable]
    candidates.extend(PYTHON_CANDIDATE_COMMANDS)

    runtimes: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        resolved = candidate
        if not os.path.isabs(candidate):
            located = shutil.which(candidate)
            if not located:
                continue
            resolved = located

        probe = probe_python(resolved)
        if not probe:
            continue

        executable = probe["executable"]
        if executable in seen:
            continue
        seen.add(executable)
        runtimes.append(probe)
    return runtimes


def choose_compatible_runtime(runtimes: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    current = os.path.realpath(sys.executable)
    compatible = [
        runtime
        for runtime in runtimes
        if runtime["supported"] and os.path.realpath(runtime["executable"]) != current
    ]
    if not compatible:
        return None
    compatible.sort(key=lambda runtime: runtime["version"], reverse=True)
    return compatible[0]


def build_agent_action(
    *,
    current_supported: bool,
    compatible_runtime: Optional[dict[str, Any]],
    writable: bool,
) -> str:
    if current_supported:
        return "优先在 OpenClaw 中继续执行当前脚本；若脚本失败，再由智能体切到手动落盘模式。"

    minimum = version_text(MIN_SUPPORTED_PYTHON)
    if compatible_runtime:
        return (
            "优先让 OpenClaw 智能体运行 `scripts/ensure_python_runtime.py --run-script <目标脚本>`，改用兼容解释器 "
            f"{compatible_runtime['executable']} ({python_compatibility_label(compatible_runtime['version'])}) 重跑脚本；"
            "若切换失败，再由智能体手动完成脚本任务。"
        )

    if writable:
        return (
            f"优先让 OpenClaw 智能体运行 `scripts/ensure_python_runtime.py --apply` 安装兼容解释器（目标 {minimum}+）；"
            "若当前环境不便安装，则由智能体直接完成脚本任务并手动落盘。"
        )

    return (
        f"优先让 OpenClaw 智能体在宿主环境运行 `scripts/ensure_python_runtime.py --apply` 安装兼容解释器（目标 {minimum}+）；"
        "若仍无法写文件，只能由智能体继续纯对话推进并明确未保存。"
    )


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


def workspace_core_paths(company_dir: Path) -> list[Path]:
    return [company_dir / relative for relative in CORE_WORKSPACE_FILES]


def ensure_workspace_dirs(company_dir: Path) -> None:
    for relative in [
        "",
        "角色智能体",
        "流程",
        "产物/内部工作稿",
        "产物/标准规范稿",
        "产物/可转DOCX稿",
        "产物/文档模板",
        "产物/产品",
        "产物/增长",
        "产物/运营",
        "记录/推进日志",
        "记录/决策记录",
        "记录/校准记录",
        "记录/检查点",
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


def preflight_status(company_dir: Optional[Path] = None) -> dict[str, Any]:
    current_version = tuple(sys.version_info[:3])
    current_supported = is_python_version_supported(current_version)
    runtimes = discover_python_runtimes()
    compatible_runtime = choose_compatible_runtime(runtimes)

    required_paths = [SCRIPT_DIR / name for name in REQUIRED_SCRIPT_NAMES]
    required_paths.extend(
        [
            TEMPLATE_DIR / "company-overview-template.md",
            TEMPLATE_DIR / "artifact-output-guide-template.md",
            TEMPLATE_DIR / "artifact-internal-draft-template.md",
            TEMPLATE_DIR / "artifact-standard-spec-template.md",
            TEMPLATE_DIR / "artifact-docx-ready-template.md",
            ORCHESTRATION_DIR / "stage-defaults.json",
            ORCHESTRATION_DIR / "handoff-schema.json",
        ]
    )
    missing = [display_path(path, ROOT) for path in required_paths if not path.exists()]
    installed = ROLE_DIR.is_dir() and not missing

    runtime_error = "无"
    runnable = False

    if company_dir is None:
        writable_target = ROOT
    elif company_dir.exists():
        writable_target = company_dir
    else:
        writable_target = company_dir.parent
    writable = writable_target.exists() and os.access(writable_target, os.W_OK)

    if not current_supported:
        minimum = version_text(MIN_SUPPORTED_PYTHON)
        if compatible_runtime:
            runtime_error = (
                f"当前解释器 {python_compatibility_label(current_version)} 不在兼容范围内；"
                f"可改用 {compatible_runtime['executable']} ({python_compatibility_label(compatible_runtime['version'])})。"
            )
        else:
            runtime_error = (
                f"当前解释器 {python_compatibility_label(current_version)} 不在兼容范围内；"
                f"未发现可直接切换的 Python {minimum}+。"
            )
    elif installed:
        try:
            load_stage_defaults()
            load_role_specs()
            render_template("company-overview-template.md", {"COMPANY_NAME": "预检"})
        except Exception as exc:
            runtime_error = f"{type(exc).__name__}: {exc}"
        else:
            runnable = True
    else:
        runtime_error = f"缺少文件: {joined_text(missing)}"

    workspace_created = bool(company_dir and company_dir.exists())
    persisted = bool(company_dir and all(path.is_file() for path in workspace_core_paths(company_dir)))

    if runnable and writable:
        recommended_mode = "模式 A：脚本执行"
    elif compatible_runtime and installed and writable:
        recommended_mode = "模式 A：脚本执行（切换兼容 Python）"
    elif writable:
        recommended_mode = "模式 B：手动落盘"
    else:
        recommended_mode = "模式 C：纯对话推进"

    if company_dir is None:
        unsaved_reason = "尚未指定目标工作区"
    elif not workspace_created:
        unsaved_reason = "目标工作区尚未创建"
    elif not persisted:
        unsaved_reason = "工作区已存在，但关键文件未全部落盘"
    else:
        unsaved_reason = "无"

    return {
        "installed": installed,
        "runnable": runnable,
        "python_supported": current_supported,
        "python_minimum": version_text(MIN_SUPPORTED_PYTHON),
        "current_python_version": version_text(current_version),
        "current_python_label": python_compatibility_label(current_version),
        "compatible_python_found": compatible_runtime is not None,
        "compatible_python_path": compatible_runtime["executable"] if compatible_runtime else "无",
        "compatible_python_version": version_text(compatible_runtime["version"]) if compatible_runtime else "无",
        "recovery_script": "scripts/ensure_python_runtime.py",
        "agent_action": build_agent_action(
            current_supported=current_supported,
            compatible_runtime=compatible_runtime,
            writable=writable,
        ),
        "workspace_created": workspace_created,
        "persisted": persisted,
        "writable": writable,
        "writable_target": str(writable_target),
        "python_path": sys.executable,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "recommended_mode": recommended_mode,
        "runtime_error": f"{runtime_error} 建议动作: {build_agent_action(current_supported=current_supported, compatible_runtime=compatible_runtime, writable=writable)}"
        if runtime_error != "无"
        else runtime_error,
        "missing_files": joined_text(missing),
        "unsaved_reason": unsaved_reason,
    }


def print_step(step: int, total: int, title: str, *, status: str = "已完成", stream: TextIO = sys.stdout) -> None:
    step_id = STEP_ALIASES.get(title, step)
    meta = STEP_CATALOG.get(step_id, {"human": title, "system": title})
    human_label = meta["human"]
    system_label = meta["system"]
    if title not in (human_label, system_label):
        status = f"{status}（{title}）"
    print(f"Step {step}/{total} {human_label} [{system_label}]: {status}", file=stream)


def print_block(title: str, items: list[tuple[str, str]], *, stream: TextIO = sys.stdout) -> None:
    print(f"{title}:", file=stream)
    for label, value in items:
        print(f"- {label}: {value}", file=stream)


def step_display(step_number: int, phase: str) -> str:
    step_id = STEP_ALIASES.get(phase, step_number)
    meta = STEP_CATALOG.get(step_id, {"human": phase, "system": phase})
    return f"Step {step_number}/5 {meta['human']} [{meta['system']}]"


def explain_save_status(
    *,
    saved: bool,
    save_path: str,
    filenames: str,
    save_details: str,
    unsaved_reason: str,
    persistence_mode: str,
) -> list[tuple[str, str]]:
    if saved:
        return [
            ("保存结论", "本次关键内容已经真实写入工作区，不只是停留在聊天里。"),
            ("你可以去哪里看", save_path),
            ("这次写入了什么", filenames),
            ("写入明细", save_details),
            ("当前保存方式", persistence_mode),
        ]

    save_next = {
        "模式 A：脚本执行": "先修复脚本执行问题，再重跑当前步骤。",
        "模式 A：脚本执行（切换兼容 Python）": "先切换到兼容 Python，再重跑当前步骤。",
        "模式 B：手动落盘": "当前适合直接手动写入 markdown/json 到工作区。",
        "模式 C：纯对话推进": "当前只能在对话里推进；如果要落盘，需要先确认创建或恢复写入能力。",
    }.get(persistence_mode, "先确认是否允许写文件，再决定脚本执行或手动落盘。")

    return [
        ("保存结论", "本次内容还没有真实写入工作区。"),
        ("为什么还没保存", unsaved_reason),
        ("现在内容在哪里", "当前内容只存在于本次输出或标准输出里。"),
        ("如果你要保存", save_next),
        ("当前保存方式", persistence_mode),
    ]


def explain_runtime_status(runtime: dict[str, Any]) -> list[tuple[str, str]]:
    if runtime["runnable"]:
        runtime_summary = "当前环境可以直接运行脚本，适合走模式 A。"
    elif runtime["compatible_python_found"]:
        runtime_summary = "当前解释器不理想，但已经找到可切换的兼容 Python。"
    elif runtime["writable"]:
        runtime_summary = "脚本暂时不稳，但当前环境还能直接写文件，适合走手动落盘。"
    else:
        runtime_summary = "当前环境既不适合直接跑脚本，也不适合直接写文件，只能先纯对话推进。"

    install_summary = "技能文件齐全，可以继续恢复运行。" if runtime["installed"] else "技能文件还不完整，先补齐缺失文件。"
    persistence_summary = "当前工作区已经具备核心落盘文件。" if runtime["persisted"] else runtime["unsaved_reason"]

    return [
        ("运行结论", runtime_summary),
        ("安装情况", install_summary),
        ("工作区情况", "目标工作区已存在。" if runtime["workspace_created"] else "目标工作区还没有创建。"),
        ("落盘情况", persistence_summary),
        ("Python 兼容", f"当前是 {runtime['current_python_label']}；兼容目标是 Python {runtime['python_minimum']}+。"),
        ("推荐动作", runtime["agent_action"]),
    ]


def build_round_dashboard(
    *,
    company_dir: Optional[Path],
    stage: str,
    round_name: str,
    role: str,
    artifact: str,
    next_action: str,
) -> list[tuple[str, str]]:
    if company_dir is not None:
        state_file = state_path(company_dir)
        if state_file.is_file():
            state = load_state(company_dir)
            current_round = state.get("current_round", {})
            return [
                ("当前阶段", state.get("stage_label", stage)),
                ("当前回合", current_round.get("name", round_name)),
                ("回合状态", current_round.get("status", "待定义")),
                ("当前负责角色", current_round.get("owner_role_name", role)),
                ("关键产物", current_round.get("artifact", artifact)),
                ("当前阻塞", current_round.get("blocker", "无")),
                ("下一步最短动作", current_round.get("next_action", next_action)),
                ("完成标准", current_round.get("success_criteria", "待定义")),
            ]

    return [
        ("当前阶段", stage),
        ("当前回合", round_name),
        ("回合状态", "待确认"),
        ("当前负责角色", role),
        ("关键产物", artifact),
        ("当前阻塞", "待确认"),
        ("下一步最短动作", next_action),
        ("完成标准", "待确认"),
    ]


def default_work_scope(artifact: str) -> list[str]:
    return [
        f"说明本次与 {artifact} 相关的关键结果。",
        "明确这次是否真正保存、保存到哪里。",
        "明确当前环境该继续脚本执行、手动落盘，还是只做对话推进。",
    ]


def default_non_scope(mode: str) -> list[str]:
    if mode == "创建公司":
        return ["不会在未确认前假装已经完成正式创建。"]
    return ["不会把未执行的动作说成已经完成。"]


def emit_runtime_report(
    *,
    mode: str,
    phase: str,
    stage: str,
    round_name: str,
    role: str,
    artifact: str,
    next_action: str,
    needs_confirmation: str,
    persistence_mode: str,
    company_dir: Optional[Path],
    saved_paths: list[Path],
    unsaved_reason: str = "无",
    work_scope: Optional[list[str]] = None,
    non_scope: Optional[list[str]] = None,
    changes: Optional[list[str]] = None,
    output_view: str = "both",
    step_number: int = 5,
    stream: TextIO = sys.stdout,
) -> None:
    runtime = preflight_status(company_dir)
    saved = bool(saved_paths) and all(path.exists() for path in saved_paths)
    save_path = str(company_dir) if company_dir is not None else "未指定"
    save_details = joined_text(display_path(path, company_dir) for path in saved_paths)
    filenames = joined_text(path.name for path in saved_paths)

    if not saved and unsaved_reason == "无":
        unsaved_reason = runtime["unsaved_reason"]
    work_scope = work_scope or default_work_scope(artifact)
    non_scope = non_scope or default_non_scope(mode)
    changes = changes or (
        [f"已更新或写入 {joined_text(path.name for path in saved_paths)}。"] if saved_paths else ["本次没有写入新文件。"]
    )
    step_label = step_display(step_number, phase)
    round_dashboard = build_round_dashboard(
        company_dir=company_dir,
        stage=stage,
        round_name=round_name,
        role=role,
        artifact=artifact,
        next_action=next_action,
    )
    save_explanation = explain_save_status(
        saved=saved,
        save_path=save_path,
        filenames=filenames,
        save_details=save_details,
        unsaved_reason=unsaved_reason,
        persistence_mode=persistence_mode,
    )
    runtime_explanation = explain_runtime_status(runtime)

    if output_view in ("both", "navigation"):
        print("用户导航版:", file=stream)
        print_block(
            "三层导航条",
            [
                ("阶段", stage),
                ("回合", round_name),
                ("本次 Step", step_label),
            ],
            stream=stream,
        )
        print_block(
            "本次范围",
            [
                ("本次会做", joined_text(work_scope)),
                ("本次不会做", joined_text(non_scope)),
            ],
            stream=stream,
        )
        print_block(
            "本次变化",
            [(f"变化 {index}", value) for index, value in enumerate(changes, start=1)],
            stream=stream,
        )
        print_block("回合仪表盘", round_dashboard, stream=stream)
        print_block("保存解释", save_explanation, stream=stream)
        print_block("运行解释", runtime_explanation, stream=stream)
        if output_view == "both":
            print("", file=stream)

    if output_view in ("both", "audit"):
        print("审计版:", file=stream)
        print_block(
            "状态栏",
            [
                ("当前模式", mode),
                ("当前步骤", step_label),
                ("当前阶段", stage),
                ("当前回合", round_name),
                ("当前角色", role),
                ("当前产物", artifact),
                ("当前保存模式", persistence_mode),
                ("下一步动作", next_action),
                ("是否需要确认", needs_confirmation),
            ],
            stream=stream,
        )
        print_block(
            "保存状态",
            [
                ("是否已保存", bool_label(saved)),
                ("保存路径", save_path),
                ("文件名", filenames),
                ("保存明细", save_details),
                ("未保存原因", "无" if saved else unsaved_reason),
            ],
            stream=stream,
        )
        print_block(
            "运行状态",
            [
                ("installed", bool_audit_label(runtime["installed"])),
                ("runnable", bool_audit_label(runtime["runnable"])),
                ("python_supported", bool_audit_label(runtime["python_supported"])),
                ("workspace_created", bool_audit_label(runtime["workspace_created"])),
                ("persisted", bool_audit_label(runtime["persisted"])),
                ("writable", bool_audit_label(runtime["writable"])),
                ("当前 Python", f"{runtime['python_path']} ({runtime['python_version']})"),
                ("兼容目标", f"Python {runtime['python_minimum']}+"),
                ("可切换解释器", "无" if not runtime["compatible_python_found"] else f"{runtime['compatible_python_path']} ({runtime['compatible_python_version']})"),
                ("恢复脚本", runtime["recovery_script"]),
                ("推荐模式", runtime["recommended_mode"]),
                ("智能体建议动作", runtime["agent_action"]),
                ("环境异常", runtime["runtime_error"]),
            ],
            stream=stream,
        )


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
    write_text(company_dir / "07-文档产物规范.md", render_template("artifact-output-guide-template.md", common_values))

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
    write_text(company_dir / "产物" / "文档模板" / "内部工作稿模板.md", render_template("artifact-internal-draft-template.md", common_values))
    write_text(company_dir / "产物" / "文档模板" / "标准规范稿模板.md", render_template("artifact-standard-spec-template.md", common_values))
    write_text(company_dir / "产物" / "文档模板" / "可转DOCX稿模板.md", render_template("artifact-docx-ready-template.md", common_values))
