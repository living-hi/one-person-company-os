#!/usr/bin/env python3
"""Shared helpers for the One Person Company OS workspace scripts."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, TextIO
from xml.sax.saxutils import escape


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
ARTIFACT_ROOT = "产物"
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

STAGE_REQUIRED_OUTPUTS = {
    "validate": [
        "用户问题证据、访谈纪要、付费或预约信号等真实验证材料。",
        "至少一份可直接继续使用的正式交付文档，而不是只有聊天摘要。",
    ],
    "build": [
        "实际软件或实际非软件交付物必须至少有一项真实落盘。",
        "如果做软件，必须能看到代码、配置、脚本、接口或自动化资产中的至少一类产出。",
        "如果做非软件产品，必须能看到服务方案、培训材料、研究成果、销售资料或执行清单中的至少一类产出。",
        "必须同步保留测试或验收记录。",
    ],
    "launch": [
        "必须同时看到对外可交付物和上线资料，不能只有发布文案。",
        "必须包含部署清单、回滚方案、生产观测/告警安排。",
        "必须包含上线公告、反馈回收路径和首轮支持安排。",
    ],
    "operate": [
        "必须持续更新生产运行资料、事故复盘和用户反馈处理记录。",
        "部署与生产类资料不能在产品上线后消失，必须继续维护。",
    ],
    "grow": [
        "必须把增长实验、收入/成本复盘和运行稳定性资料一起保留。",
        "增长动作不能脱离真实交付和生产运行状态单独存在。",
    ],
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


def safe_document_name(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", value).strip()
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "未命名文档"


def numbered_name(index: int, title: str, suffix: str) -> str:
    return f"{index:02d}-{safe_document_name(title)}{suffix}"


def next_numbered_index(directory: Path) -> int:
    max_index = 0
    if directory.is_dir():
        for path in directory.iterdir():
            match = re.match(r"^(\d{2})-", path.name)
            if match:
                max_index = max(max_index, int(match.group(1)))
    return max_index + 1


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


def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def docx_content_types_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""


def docx_root_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


def docx_document_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


def docx_styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:sz w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="34"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
</w:styles>
"""


def docx_app_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>One Person Company OS</Application>
</Properties>
"""


def docx_core_xml(title: str) -> str:
    created = iso_now()
    escaped = escape(title)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{escaped}</dc:title>
  <dc:creator>One Person Company OS</dc:creator>
  <cp:lastModifiedBy>One Person Company OS</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>
</cp:coreProperties>
"""


def docx_paragraph_xml(text: str, style: Optional[str] = None) -> str:
    escaped_text = escape(text)
    paragraph_style = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    return (
        "<w:p>"
        f"{paragraph_style}"
        "<w:r><w:t xml:space=\"preserve\">"
        f"{escaped_text}"
        "</w:t></w:r>"
        "</w:p>"
    )


def markdown_to_docx_xml(markdown_text: str) -> str:
    paragraphs: list[str] = []
    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            paragraphs.append("<w:p/>")
            continue
        style = None
        text = line
        if line.startswith("# "):
            style = "Heading1"
            text = line[2:]
        elif line.startswith("## "):
            style = "Heading2"
            text = line[3:]
        elif line.startswith("### "):
            style = "Heading3"
            text = line[4:]
        elif line.startswith("- "):
            text = f"• {line[2:]}"
        paragraphs.append(docx_paragraph_xml(text, style))

    body = "".join(paragraphs) or "<w:p/>"
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
        "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
        "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
        "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
        "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
        "xmlns:wne=\"http://schemas.microsoft.com/office/2006/wordml\" "
        "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
        "mc:Ignorable=\"w14 wp14\">"
        f"<w:body>{body}"
        "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
        "</w:body></w:document>"
    )


def write_docx(path: Path, markdown_text: str, *, title: Optional[str] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc_title = title or path.stem
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", docx_content_types_xml())
        archive.writestr("_rels/.rels", docx_root_rels_xml())
        archive.writestr("docProps/app.xml", docx_app_xml())
        archive.writestr("docProps/core.xml", docx_core_xml(doc_title))
        archive.writestr("word/_rels/document.xml.rels", docx_document_rels_xml())
        archive.writestr("word/styles.xml", docx_styles_xml())
        archive.writestr("word/document.xml", markdown_to_docx_xml(markdown_text))


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
        "产物/00-交付模板",
        "产物/01-实际交付",
        "产物/02-软件与代码",
        "产物/03-非软件与业务",
        "产物/04-部署与生产",
        "产物/05-上线与增长",
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
            TEMPLATE_DIR / "artifact-docx-ready-template.md",
            TEMPLATE_DIR / "artifact-delivery-index-template.md",
            TEMPLATE_DIR / "artifact-software-delivery-template.md",
            TEMPLATE_DIR / "artifact-non-software-delivery-template.md",
            TEMPLATE_DIR / "artifact-quality-template.md",
            TEMPLATE_DIR / "artifact-deployment-template.md",
            TEMPLATE_DIR / "artifact-production-template.md",
            TEMPLATE_DIR / "artifact-launch-feedback-template.md",
            TEMPLATE_DIR / "artifact-validate-evidence-template.md",
            TEMPLATE_DIR / "artifact-growth-template.md",
            TEMPLATE_DIR / "stage-role-deliverable-matrix-template.md",
            TEMPLATE_DIR / "current-stage-deliverable-template.md",
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


def build_matrix_values(role_specs: dict[str, dict[str, Any]]) -> dict[str, str]:
    defaults = load_stage_defaults()
    values: dict[str, str] = {}
    for stage_id in STAGE_CONFIG:
        stage_upper = stage_id.upper()
        stage_roles = role_display_names(defaults["stage_defaults"][stage_id], role_specs)
        optional_roles = role_display_names(defaults["stage_optional_roles"].get(stage_id, []), role_specs)
        values[f"{stage_upper}_DEFAULT_ROLES"] = format_list(stage_roles)
        values[f"{stage_upper}_OPTIONAL_ROLES"] = format_list(optional_roles)
        values[f"{stage_upper}_REQUIRED_OUTPUTS"] = format_list(STAGE_REQUIRED_OUTPUTS[stage_id])
    return values


def stage_artifact_specs(stage_id: str) -> list[dict[str, str]]:
    common_specs = [
        {
            "subdir": "00-交付模板",
            "filename": "01-正式交付文档模板.docx",
            "template": "artifact-docx-ready-template.md",
        },
        {
            "subdir": "01-实际交付",
            "filename": "01-实际产出总表.docx",
            "template": "artifact-delivery-index-template.md",
        },
        {
            "subdir": "02-软件与代码",
            "filename": "01-代码与功能交付清单.docx",
            "template": "artifact-software-delivery-template.md",
        },
        {
            "subdir": "03-非软件与业务",
            "filename": "01-非软件交付清单.docx",
            "template": "artifact-non-software-delivery-template.md",
        },
    ]
    stage_specific = {
        "validate": [
            {
                "subdir": "01-实际交付",
                "filename": "02-问题与用户证据包.docx",
                "template": "artifact-validate-evidence-template.md",
            },
        ],
        "build": [
            {
                "subdir": "02-软件与代码",
                "filename": "02-测试与验收记录.docx",
                "template": "artifact-quality-template.md",
            },
        ],
        "launch": [
            {
                "subdir": "02-软件与代码",
                "filename": "02-测试与验收记录.docx",
                "template": "artifact-quality-template.md",
            },
            {
                "subdir": "04-部署与生产",
                "filename": "01-部署与回滚清单.docx",
                "template": "artifact-deployment-template.md",
            },
            {
                "subdir": "04-部署与生产",
                "filename": "02-生产观测与告警清单.docx",
                "template": "artifact-production-template.md",
            },
            {
                "subdir": "05-上线与增长",
                "filename": "01-上线公告与反馈回收清单.docx",
                "template": "artifact-launch-feedback-template.md",
            },
        ],
        "operate": [
            {
                "subdir": "04-部署与生产",
                "filename": "01-部署与回滚清单.docx",
                "template": "artifact-deployment-template.md",
            },
            {
                "subdir": "04-部署与生产",
                "filename": "02-生产观测与告警清单.docx",
                "template": "artifact-production-template.md",
            },
            {
                "subdir": "04-部署与生产",
                "filename": "03-事故响应与复盘记录.docx",
                "template": "artifact-production-template.md",
            },
            {
                "subdir": "05-上线与增长",
                "filename": "01-上线公告与反馈回收清单.docx",
                "template": "artifact-launch-feedback-template.md",
            },
        ],
        "grow": [
            {
                "subdir": "04-部署与生产",
                "filename": "01-部署与回滚清单.docx",
                "template": "artifact-deployment-template.md",
            },
            {
                "subdir": "04-部署与生产",
                "filename": "02-生产观测与告警清单.docx",
                "template": "artifact-production-template.md",
            },
            {
                "subdir": "05-上线与增长",
                "filename": "01-增长实验与经营复盘.docx",
                "template": "artifact-growth-template.md",
            },
        ],
    }
    return common_specs + stage_specific.get(stage_id, [])


def artifact_template_values(common_values: dict[str, str], state: dict[str, Any]) -> dict[str, str]:
    current_round = state.get("current_round", {})
    current_stage = state["stage_id"]
    return {
        **common_values,
        "ARTIFACT_TITLE": "正式交付文档模板",
        "ARTIFACT_TYPE": "正式交付文档",
        "ARTIFACT_OWNER": current_round.get("owner_role_name", "总控台"),
        "ARTIFACT_OBJECTIVE": current_round.get("goal", "记录一个可真正交付的实际产出"),
        "ARTIFACT_SUMMARY": "这是一份正式交付文档模板。交付时必须写清真实产出、证据、责任人和下一步动作。",
        "ARTIFACT_SCOPE_IN": format_list([
            "实际软件产出或实际非软件产出",
            "验收证据与责任人",
            "与当前阶段匹配的部署/生产资料",
        ]),
        "ARTIFACT_SCOPE_OUT": format_list([
            "只有聊天记录、没有文件或链接的伪交付",
            "缺少证据路径的空泛总结",
        ]),
        "ARTIFACT_DELIVERABLES": format_list(STAGE_REQUIRED_OUTPUTS[current_stage]),
        "ARTIFACT_CHANGES": format_list([
            "文件名使用两位序号开头。",
            "产物目录默认只落 DOCX。",
            "上线后自动要求部署与生产资料。",
        ]),
        "ARTIFACT_DECISIONS": format_list([
            "关键产物统一进入正式交付文档路径。",
            "软件和非软件产出都必须可被审计。",
        ]),
        "ARTIFACT_RISKS": format_list([
            "没有真实文件、代码、配置、材料或证据时，不应视为完成交付。",
        ]),
        "ARTIFACT_NEXT_ACTION": current_round.get("next_action", "补齐本轮真实交付与证据。"),
    }


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
        "CURRENT_STAGE_REQUIRED_OUTPUTS": format_list(STAGE_REQUIRED_OUTPUTS[stage_id]),
        "ACTIVE_ROLE_LIST": format_list(active_display),
        "AVAILABLE_ROLE_LIST": format_list(available_display),
        "ACTIVE_ROLE_INLINE": "、".join(active_display) or "无",
    }
    matrix_values = build_matrix_values(role_specs)

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
    write_text(
        company_dir / "08-阶段角色与交付矩阵.md",
        render_template("stage-role-deliverable-matrix-template.md", {**common_values, **matrix_values}),
    )
    write_text(
        company_dir / "09-当前阶段交付要求.md",
        render_template("current-stage-deliverable-template.md", common_values),
    )

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

    docx_values = artifact_template_values(common_values, state)
    for spec in stage_artifact_specs(stage_id):
        rendered = render_template(spec["template"], docx_values)
        filename = spec["filename"]
        title = filename[:-5] if filename.endswith(".docx") else filename
        write_docx(company_dir / ARTIFACT_ROOT / spec["subdir"] / filename, rendered, title=title)
