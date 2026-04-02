#!/usr/bin/env python3
"""Run local release validation for One Person Company OS."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
RELEASE_ASSETS_DIR = ROOT / "release" / "assets"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def assert_exists(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"expected file not found: {path}")


def assert_contains(text: str, *snippets: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            raise AssertionError(f"expected snippet not found: {snippet}")


def validate_python_compatibility_logic() -> None:
    from common import build_agent_action, is_python_version_supported
    from ensure_python_runtime import build_install_plan

    if not is_python_version_supported((3, 7, 0)):
        raise AssertionError("Python 3.7 should be supported")
    if is_python_version_supported((3, 6, 15)):
        raise AssertionError("Python 3.6 should not be supported")

    switch_action = build_agent_action(
        current_supported=False,
        compatible_runtime={"executable": "/opt/python3.11/bin/python3.11", "version": (3, 11, 9)},
        writable=True,
    )
    assert_contains(switch_action, "OpenClaw", "/opt/python3.11/bin/python3.11", "重跑脚本")

    install_action = build_agent_action(
        current_supported=False,
        compatible_runtime=None,
        writable=True,
    )
    assert_contains(install_action, "OpenClaw", "安装兼容解释器", "手动落盘")

    mac_plan = build_install_plan(
        target_version="3.11",
        system_name="darwin",
        available_commands={"brew"},
    )
    if not mac_plan["supported"] or mac_plan["installer"] != "Homebrew":
        raise AssertionError("expected Homebrew install plan for macOS")

    apt_plan = build_install_plan(
        target_version="3.11",
        system_name="linux",
        os_release={"ID": "ubuntu", "PRETTY_NAME": "Ubuntu 24.04"},
        available_commands={"apt-get"},
    )
    if not apt_plan["supported"] or apt_plan["installer"] != "apt-get":
        raise AssertionError("expected apt-get install plan for Ubuntu")

    win_plan = build_install_plan(
        target_version="3.11",
        system_name="windows",
        available_commands={"winget"},
    )
    if not win_plan["supported"] or win_plan["installer"] != "winget":
        raise AssertionError("expected winget install plan for Windows")


def validate_workspace_scripts() -> None:
    with tempfile.TemporaryDirectory(prefix="opc-validate-") as tmp_dir:
        workspace = Path(tmp_dir)

        ensure_runtime = run(str(SCRIPTS_DIR / "ensure_python_runtime.py"))
        assert_contains(ensure_runtime.stdout, "Step 5/5 验证与回报", "Python 兼容状态", "安装方案", "执行结果")
        print(ensure_runtime.stdout.strip())

        preflight = run(
            str(SCRIPTS_DIR / "preflight_check.py"),
            "--mode",
            "创建公司",
            "--company-dir",
            str(workspace / "北辰实验室"),
        )
        assert_contains(
            preflight.stdout,
            "Step 5/5 验证与回报",
            "保存状态:",
            "运行状态:",
            "模式 A：脚本执行",
            "python_supported",
            "兼容目标",
            "恢复脚本",
            "智能体建议动作",
        )
        print(preflight.stdout.strip())

        init = run(
            str(SCRIPTS_DIR / "init_company.py"),
            "北辰实验室",
            "--path",
            str(workspace),
            "--product-name",
            "北辰助手",
            "--stage",
            "构建期",
            "--target-user",
            "独立开发者",
            "--core-problem",
            "缺少持续推进的一人公司系统",
            "--product-pitch",
            "一个帮助独立开发者持续推进业务的总控台",
        )
        assert_contains(init.stdout, "Step 5/5 验证与回报", "保存状态:", "运行状态:", "文件名:")
        print(init.stdout.strip())

        company_dir = workspace / "北辰实验室"
        assert_exists(company_dir / "00-公司总览.md")
        assert_exists(company_dir / "04-当前回合.md")
        assert_exists(company_dir / "角色智能体" / "角色清单.md")
        assert_exists(company_dir / "自动化" / "当前状态.json")

        start = run(
            str(SCRIPTS_DIR / "start_round.py"),
            str(company_dir),
            "--round-name",
            "完成首页首屏",
            "--goal",
            "完成首页首屏结构与注册入口",
            "--owner",
            "product-strategist",
            "--artifact",
            "产物/产品/首页首屏草稿.md",
            "--next-action",
            "先确定首屏价值主张",
        )
        assert_contains(start.stdout, "Step 5/5 验证与回报", "启动回合", "保存状态:")
        print(start.stdout.strip())

        update = run(
            str(SCRIPTS_DIR / "update_round.py"),
            str(company_dir),
            "--status",
            "执行中",
            "--blocker",
            "首屏信息层级仍不稳定",
            "--next-action",
            "重写首屏主标题与副标题",
            "--note",
            "进入执行阶段",
        )
        assert_contains(update.stdout, "Step 5/5 验证与回报", "推进回合", "运行状态:")
        print(update.stdout.strip())

        calibrate = run(
            str(SCRIPTS_DIR / "calibrate_round.py"),
            str(company_dir),
            "--reason",
            "30 分钟内无法确定首屏价值主张",
            "--finding",
            "需要产品负责人先收敛目标用户表达",
            "--next-action",
            "把目标用户缩小到做 AI SaaS 的独立开发者",
        )
        assert_contains(calibrate.stdout, "Step 5/5 验证与回报", "校准回合", "保存状态:")
        print(calibrate.stdout.strip())

        checkpoint = run(
            str(SCRIPTS_DIR / "checkpoint_save.py"),
            str(company_dir),
            "--reason",
            "准备结束当前会话，保存一次可恢复检查点",
            "--note",
            "验证 checkpoint save 能力",
        )
        assert_contains(checkpoint.stdout, "Step 5/5 验证与回报", "保存检查点", "记录/检查点")
        print(checkpoint.stdout.strip())

        transition = run(
            str(SCRIPTS_DIR / "transition_stage.py"),
            str(company_dir),
            "--stage",
            "上线期",
            "--reason",
            "关键功能与首屏已经具备对外测试条件",
            "--first-round-name",
            "准备首轮外部测试",
            "--first-round-goal",
            "整理测试入口、反馈表单和告知文案",
            "--first-round-owner",
            "growth-sales",
        )
        assert_contains(transition.stdout, "Step 5/5 验证与回报", "切换阶段", "保存状态:")
        print(transition.stdout.strip())

        single_brief = run(
            str(SCRIPTS_DIR / "build_agent_brief.py"),
            "--stage",
            "构建期",
            "--role",
            "engineer-tech-lead",
            "--company-name",
            "北辰实验室",
            "--objective",
            "把首屏需求落实成可交付路径",
            "--current-round",
            "完成首页首屏",
            "--round-goal",
            "完成首页首屏结构与注册入口",
            "--current-bottleneck",
            "前端结构还未收敛",
            "--next-shortest-action",
            "先拆出首屏组件和 CTA 路径",
            "--output-format",
            "json",
        )
        packet = json.loads(single_brief.stdout)
        if packet["role_id"] != "engineer-tech-lead":
            raise ValueError("unexpected role id in single brief validation")
        if packet["stage_id"] != "build":
            raise ValueError("unexpected stage in single brief validation")
        assert_contains(
            single_brief.stderr,
            "Step 5/5 验证与回报",
            "模式 C：纯对话推进",
            "当前内容仅输出到标准输出，未指定 --output-dir",
        )

        output_dir = company_dir / "角色智能体"
        stage_briefs = run(
            str(SCRIPTS_DIR / "build_agent_brief.py"),
            "--stage",
            "上线期",
            "--all-default-roles",
            "--company-name",
            "北辰实验室",
            "--objective",
            "启动上线期的第一个回合",
            "--current-round",
            "准备首轮外部测试",
            "--round-goal",
            "整理测试入口、反馈表单和告知文案",
            "--current-bottleneck",
            "反馈入口还没打通",
            "--next-shortest-action",
            "先确认首轮测试表单字段",
            "--output-dir",
            str(output_dir),
        )
        assert_contains(stage_briefs.stdout, "总控台.md", "增长负责人.md")
        assert_contains(stage_briefs.stderr, "Step 5/5 验证与回报", "模式 A：脚本执行", "保存状态:")
        print(stage_briefs.stdout.strip())
        assert_exists(output_dir / "总控台.md")
        assert_exists(output_dir / "增长负责人.md")
        assert_exists(next((company_dir / "记录" / "检查点").glob("*-检查点.md")))


def validate_svg_assets() -> None:
    for path in sorted(RELEASE_ASSETS_DIR.glob("*.svg")):
        ET.parse(path)
        print(f"OK {path.relative_to(ROOT)}")


def main() -> int:
    validate_python_compatibility_logic()
    validate_workspace_scripts()
    validate_svg_assets()
    print("Release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
