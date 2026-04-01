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


def validate_workspace_scripts() -> None:
    with tempfile.TemporaryDirectory(prefix="opc-validate-") as tmp_dir:
        workspace = Path(tmp_dir)

        init = run(str(SCRIPTS_DIR / "init_company.py"), "Acme Solo", "--path", str(workspace), "--mode", "saas")
        print(init.stdout.strip())

        company_dir = workspace / "acme-solo"
        assert_exists(company_dir / "00-company-charter.md")
        assert_exists(company_dir / "reviews" / "weekly-review-template.md")

        weekly = run(
            str(SCRIPTS_DIR / "weekly_review.py"),
            str(company_dir),
            "--week-of",
            "2026-03-30",
        )
        print(weekly.stdout.strip())
        assert_exists(company_dir / "reviews" / "2026-03-30-weekly-review.md")

        single_brief = run(
            str(SCRIPTS_DIR / "build_agent_brief.py"),
            "--stage",
            "Build",
            "--role",
            "engineer-tech-lead",
            "--language",
            "en",
            "--company-name",
            "Acme Solo",
            "--objective",
            "Turn the PRD into an implementation plan",
            "--current-bottleneck",
            "Scope is defined but delivery is still ambiguous",
            "--next-required-artifact",
            "sprint-plan.md",
            "--input",
            "03-prd.md",
            "--output-format",
            "json",
        )
        packet = json.loads(single_brief.stdout)
        if packet["role_id"] != "engineer-tech-lead":
            raise ValueError("unexpected role id in single brief validation")
        if packet["stage"] != "Build":
            raise ValueError("unexpected stage in single brief validation")

        output_dir = company_dir / "agent-briefs"
        stage_briefs = run(
            str(SCRIPTS_DIR / "build_agent_brief.py"),
            "--stage",
            "Launch",
            "--all-stage-roles",
            "--language",
            "en",
            "--company-name",
            "Acme Solo",
            "--objective",
            "Prepare the launch pack",
            "--current-bottleneck",
            "Messaging is not synchronized with onboarding",
            "--next-required-artifact",
            "launch-brief.md",
            "--output-dir",
            str(output_dir),
        )
        print(stage_briefs.stdout.strip())
        assert_exists(output_dir / "founder-ceo.md")
        assert_exists(output_dir / "growth-sales.md")


def validate_svg_assets() -> None:
    for path in sorted(RELEASE_ASSETS_DIR.glob("*.svg")):
        ET.parse(path)
        print(f"OK {path.relative_to(ROOT)}")


def main() -> int:
    validate_workspace_scripts()
    validate_svg_assets()
    print("Release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
