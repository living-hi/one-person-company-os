#!/usr/bin/env python3
"""Ensure a compatible Python runtime exists for One Person Company OS scripts."""

from __future__ import annotations

import argparse
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from common import (
    MIN_SUPPORTED_PYTHON,
    build_agent_action,
    choose_compatible_runtime,
    discover_python_runtimes,
    is_python_version_supported,
    print_block,
    print_step,
    python_compatibility_label,
    version_text,
)

def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def parse_os_release(path: Path = Path("/etc/os-release")) -> dict[str, str]:
    if not path.is_file():
        return {}

    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        result[key] = value.strip().strip('"')
    return result


def python_package_name(target_version: str, style: str) -> str:
    major, minor = target_version.split(".", 1)
    if style == "apt":
        return "python{}.{}".format(major, minor)
    if style == "dnf":
        return "python{}.{}".format(major, minor)
    if style == "choco":
        return "python{}{}".format(major, minor)
    return "python3"


def build_install_plan(
    *,
    target_version: str,
    system_name: Optional[str] = None,
    os_release: Optional[dict[str, str]] = None,
    available_commands: Optional[set[str]] = None,
) -> dict[str, Any]:
    system_name = (system_name or platform.system()).lower()
    os_release = os_release or parse_os_release()
    available_commands = available_commands or set()
    distro = os_release.get("ID", "").lower()
    distro_like = os_release.get("ID_LIKE", "").lower()

    plan = {
        "supported": False,
        "platform": system_name,
        "installer": "无",
        "title": "未找到自动安装方案",
        "commands": [],
        "notes": ["当前环境未识别到可直接执行的 Python 安装方案。"],
    }

    if system_name == "darwin":
        if "brew" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": "macOS",
                    "installer": "Homebrew",
                    "title": "通过 Homebrew 安装兼容 Python",
                    "commands": [["brew", "install", "python@{}".format(target_version)]],
                    "notes": ["安装完成后可用 `python{}` 重跑脚本。".format(target_version)],
                }
            )
        else:
            plan["notes"].append("缺少 Homebrew，需先安装 brew。")
        return plan

    if system_name == "windows":
        winget_id = "Python.Python.{}".format(target_version)
        if "winget" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": "Windows",
                    "installer": "winget",
                    "title": "通过 winget 安装兼容 Python",
                    "commands": [["winget", "install", "-e", "--id", winget_id]],
                    "notes": ["安装完成后优先使用 `py -{}.{}` 或新安装的 python 可执行文件。".format(*target_version.split("."))],
                }
            )
        elif "choco" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": "Windows",
                    "installer": "Chocolatey",
                    "title": "通过 Chocolatey 安装兼容 Python",
                    "commands": [["choco", "install", python_package_name(target_version, "choco"), "-y"]],
                    "notes": ["安装完成后重新打开终端，确保 PATH 生效。"],
                }
            )
        else:
            plan["notes"].append("缺少 winget 或 Chocolatey，需由 OpenClaw 智能体接管。")
        return plan

    if system_name == "linux":
        linux_id = "{} {}".format(distro, distro_like).strip()
        if ("ubuntu" in linux_id or "debian" in linux_id) and "apt-get" in available_commands:
            package = python_package_name(target_version, "apt")
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Debian/Ubuntu"),
                    "installer": "apt-get",
                    "title": "通过 apt-get 安装兼容 Python",
                    "commands": [
                        ["sudo", "apt-get", "update"],
                        ["sudo", "apt-get", "install", "-y", package, "{}-venv".format(package)],
                    ],
                    "notes": ["如果源里缺少该版本，可由 OpenClaw 智能体切回手动落盘。"],
                }
            )
            return plan

        if ("fedora" in linux_id or "rhel" in linux_id or "centos" in linux_id) and ("dnf" in available_commands or "yum" in available_commands):
            package = python_package_name(target_version, "dnf")
            installer = "dnf" if "dnf" in available_commands else "yum"
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Fedora/RHEL"),
                    "installer": installer,
                    "title": "通过 {} 安装兼容 Python".format(installer),
                    "commands": [["sudo", installer, "install", "-y", package]],
                    "notes": ["安装完成后让 OpenClaw 智能体重新探测解释器。"],
                }
            )
            return plan

        if ("alpine" in linux_id) and "apk" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Alpine"),
                    "installer": "apk",
                    "title": "通过 apk 安装兼容 Python",
                    "commands": [["sudo", "apk", "add", "python3", "py3-pip"]],
                    "notes": ["Alpine 会安装系统默认 Python 3。"],
                }
            )
            return plan

        if "pacman" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Arch Linux"),
                    "installer": "pacman",
                    "title": "通过 pacman 安装兼容 Python",
                    "commands": [["sudo", "pacman", "-Sy", "--noconfirm", "python"]],
                    "notes": ["Arch 默认提供当前 Python 3。"],
                }
            )
            return plan

        plan["platform"] = os_release.get("PRETTY_NAME", "Linux")
        plan["notes"].append("缺少已支持的包管理器，需由 OpenClaw 智能体接管。")
        return plan

    return plan


def available_command_names() -> set[str]:
    names = set()
    for command in ["brew", "apt-get", "dnf", "yum", "apk", "pacman", "winget", "choco"]:
        if shutil.which(command):
            names.add(command)
    return names


def execute_commands(commands: list[list[str]]) -> None:
    for command in commands:
        subprocess.run(command, check=True)


def run_script_with_runtime(runtime_path: str, script_path: str, script_args: list[str]) -> int:
    completed = subprocess.run([runtime_path, script_path, *script_args])
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="为 One Person Company OS 选择或安装兼容 Python。")
    parser.add_argument("--target-version", default="3.11", help="希望安装的 Python 次版本，例如 3.11")
    parser.add_argument("--apply", action="store_true", help="执行安装或直接运行目标脚本")
    parser.add_argument("--run-script", help="可选，指定一个目标脚本；如果有兼容解释器则直接用它运行")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="传给目标脚本的参数，前面可加 --")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print_step(1, 5, "检测当前 Python")
    current_version = tuple(sys.version_info[:3])
    current_supported = is_python_version_supported(current_version)
    runtimes = discover_python_runtimes()
    compatible_runtime = choose_compatible_runtime(runtimes)

    print_step(2, 5, "生成安装方案")
    install_plan = build_install_plan(
        target_version=args.target_version,
        available_commands=available_command_names(),
    )

    print_step(3, 5, "判定恢复路径")
    if current_supported:
        resolution = "当前 Python 已兼容，可直接继续"
        chosen_runtime = sys.executable
    elif compatible_runtime:
        resolution = "发现可切换的兼容解释器"
        chosen_runtime = compatible_runtime["executable"]
    elif install_plan["supported"]:
        resolution = "需要先安装兼容 Python"
        chosen_runtime = "安装完成后重新探测"
    else:
        resolution = "无法自动安装，需由 OpenClaw 智能体直接接管"
        chosen_runtime = "无"

    run_args = list(args.script_args)
    if run_args and run_args[0] == "--":
        run_args = run_args[1:]

    print_step(4, 5, "执行恢复动作", status="执行中" if args.apply else "已规划")
    return_code = 0
    action_summary = "未执行，仅输出计划"
    if args.apply:
        if current_supported and args.run_script:
            return_code = run_script_with_runtime(sys.executable, args.run_script, run_args)
            action_summary = "已用当前兼容 Python 运行目标脚本"
        elif compatible_runtime and args.run_script:
            return_code = run_script_with_runtime(compatible_runtime["executable"], args.run_script, run_args)
            action_summary = "已用兼容 Python 运行目标脚本"
        elif install_plan["supported"]:
            execute_commands(install_plan["commands"])
            action_summary = "已执行安装命令，请重新运行 preflight 或目标脚本"
        else:
            action_summary = "当前环境无法自动安装，请让 OpenClaw 智能体接管"

    print_step(5, 5, "验证与回报")
    print_block(
        "Python 兼容状态",
        [
            ("当前解释器", "{} ({})".format(sys.executable, python_compatibility_label(current_version))),
            ("兼容目标", "Python {}+".format(version_text(MIN_SUPPORTED_PYTHON))),
            ("当前是否兼容", "是" if current_supported else "否"),
            (
                "可切换解释器",
                "无"
                if not compatible_runtime
                else "{} ({})".format(
                    compatible_runtime["executable"],
                    python_compatibility_label(compatible_runtime["version"]),
                ),
            ),
            ("恢复结论", resolution),
            ("恢复动作", build_agent_action(current_supported=current_supported, compatible_runtime=compatible_runtime, writable=True)),
        ],
    )
    print_block(
        "安装方案",
        [
            ("平台", install_plan["platform"]),
            ("安装器", install_plan["installer"]),
            ("是否支持自动安装", "是" if install_plan["supported"] else "否"),
            ("推荐标题", install_plan["title"]),
            ("命令", "；".join(shell_join(command) for command in install_plan["commands"]) if install_plan["commands"] else "无"),
            ("备注", "；".join(install_plan["notes"]) if install_plan["notes"] else "无"),
        ],
    )
    print_block(
        "执行结果",
        [
            ("目标脚本", args.run_script or "无"),
            ("选用解释器", chosen_runtime),
            ("apply", "是" if args.apply else "否"),
            ("结果", action_summary),
            ("退出码", str(return_code)),
        ],
    )
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
