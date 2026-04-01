#!/usr/bin/env python3
"""Scaffold a one-person-company workspace from bundled templates."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


TEMPLATE_MAP = {
    "00-company-charter.md": "company-charter-template.md",
    "01-icp-card.md": "icp-card-template.md",
    "02-offer-sheet.md": "offer-sheet-template.md",
    "03-prd.md": "prd-template.md",
    "launches/00-launch-brief.md": "launch-brief-template.md",
    "reviews/weekly-review-template.md": "weekly-review-template.md",
    "decisions/decision-log-entry-template.md": "decision-log-entry-template.md",
    "roles/role-card-template.md": "role-card-template.md",
    "metrics/dashboard-outline.md": "dashboard-outline-template.md",
}

MODE_HINTS = {
    "generic": "- Add the business model details that matter most for this company.",
    "saas": "- Clarify the product wedge, activation path, pricing model, and retention mechanic.",
    "service": "- Clarify the service package, delivery scope, fulfillment method, and cash collection rhythm.",
    "content": "- Clarify the audience, content engine, distribution channels, and monetization path.",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "company"


def render_template(text: str, company_name: str, mode: str, today: str) -> str:
    return (
        text.replace("{{COMPANY_NAME}}", company_name)
        .replace("{{DATE}}", today)
        .replace("{{MODE}}", mode)
        .replace("{{MODE_HINTS}}", MODE_HINTS[mode])
        .replace("{{WEEK_OF}}", today)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold a one-person-company workspace from bundled templates."
    )
    parser.add_argument("company_name", help="Human-readable company name")
    parser.add_argument("--path", required=True, help="Directory where the company workspace will be created")
    parser.add_argument(
        "--mode",
        choices=sorted(MODE_HINTS),
        default="generic",
        help="Business model flavor used to tailor the starter notes",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing company directory",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    company_dir = root / slugify(args.company_name)

    if company_dir.exists() and not args.force:
        parser.error(f"target already exists: {company_dir}")

    template_dir = Path(__file__).resolve().parent.parent / "assets" / "templates"
    if not template_dir.is_dir():
        parser.error(f"template directory not found: {template_dir}")

    today = date.today().isoformat()
    directories = [
        company_dir,
        company_dir / "roles",
        company_dir / "workflows",
        company_dir / "launches",
        company_dir / "reviews",
        company_dir / "decisions",
        company_dir / "metrics",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    created_files: list[Path] = []
    for output_name, template_name in TEMPLATE_MAP.items():
        template_path = template_dir / template_name
        output_path = company_dir / output_name
        rendered = render_template(
            template_path.read_text(encoding="utf-8"),
            company_name=args.company_name,
            mode=args.mode,
            today=today,
        )
        output_path.write_text(rendered, encoding="utf-8")
        created_files.append(output_path)

    print(f"Created company workspace: {company_dir}")
    for path in created_files:
        print(path.relative_to(company_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
