#!/usr/bin/env python3
"""Create a dated weekly review file from the bundled template."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path


def monday_for(value: date) -> date:
    return value - timedelta(days=value.weekday())


def detect_company_name(company_dir: Path) -> str:
    charter_path = company_dir / "00-company-charter.md"
    if charter_path.is_file():
        first_line = charter_path.read_text(encoding="utf-8").splitlines()[0].strip()
        if first_line.startswith("# ") and first_line.endswith(" Company Charter"):
            return first_line[2:].removesuffix(" Company Charter")
    return company_dir.name.replace("-", " ").title()


def render_template(text: str, company_name: str, today: str, week_of: str) -> str:
    return (
        text.replace("{{COMPANY_NAME}}", company_name)
        .replace("{{DATE}}", today)
        .replace("{{WEEK_OF}}", week_of)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a dated weekly review file in a one-person-company workspace."
    )
    parser.add_argument("company_dir", help="Path to the company workspace created by init_company.py")
    parser.add_argument(
        "--week-of",
        help="Any ISO date within the desired review week (defaults to today)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    company_dir = Path(args.company_dir).expanduser().resolve()
    if not company_dir.is_dir():
        parser.error(f"company directory not found: {company_dir}")

    if args.week_of:
        selected_day = datetime.strptime(args.week_of, "%Y-%m-%d").date()
    else:
        selected_day = date.today()
    week_start = monday_for(selected_day).isoformat()
    today = date.today().isoformat()

    template_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "weekly-review-template.md"
    template = template_path.read_text(encoding="utf-8")
    company_name = detect_company_name(company_dir)

    reviews_dir = company_dir / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    output_path = reviews_dir / f"{week_start}-weekly-review.md"

    rendered = render_template(template, company_name, today, week_start)
    output_path.write_text(rendered, encoding="utf-8")

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
