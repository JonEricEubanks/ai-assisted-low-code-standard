from __future__ import annotations

import csv
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def require_files() -> None:
    required = [
        "README.md",
        "requirements.md",
        "plan.md",
        "BRANCHING.md",
        "CONTRIBUTING.md",
        "AGENT_WORKFLOW.md",
        "governance/power-desk-delivery-charter.md",
        "governance/delivery-quality-scorecard.md",
        "standards/common-delivery-lifecycle.md",
        "qa/qa-strategy.md",
        "qa/evidence-schema.md",
        "blog/blog-series-plan.md",
        "portfolio/operational-evidence-matrix.md",
        "checkpoints/spec-to-plan.yaml",
        "checkpoints/plan-to-tasks.yaml",
    ]
    for relative_path in required:
        if not (ROOT / relative_path).is_file():
            ERRORS.append(f"Missing required file: {relative_path}")


def validate_skills() -> None:
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(skills) < 8:
        ERRORS.append(f"Expected at least 8 skills, found {len(skills)}")

    header = re.compile(r"^---\nname: .+\ndescription: .+\n---\n")
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        if not header.match(text):
            ERRORS.append(f"Invalid skill frontmatter: {skill.relative_to(ROOT)}")


def validate_csv() -> None:
    csv_files = [
        "qa/screenshot-register.csv",
        "metrics/baseline-and-outcomes.csv",
    ]
    for relative_path in csv_files:
        with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows or len(rows[0]) < 10:
            ERRORS.append(f"Invalid CSV header: {relative_path}")


def validate_requirements() -> None:
    requirement_text = (ROOT / "requirements.md").read_text(encoding="utf-8")
    plan_text = (ROOT / "plan.md").read_text(encoding="utf-8")
    requirements = set(re.findall(r"REQ-\d{3}", requirement_text))
    mapped = set(re.findall(r"REQ-\d{3}", plan_text))
    missing = requirements - mapped
    if missing:
        ERRORS.append(f"Requirements absent from plan: {', '.join(sorted(missing))}")


def validate_links() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown_file in ROOT.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if target and not (markdown_file.parent / target).resolve().exists():
                ERRORS.append(
                    f"Broken link: {markdown_file.relative_to(ROOT)} -> {target}"
                )


def validate_json() -> None:
    for json_file in ROOT.rglob("*.json"):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            ERRORS.append(f"Invalid JSON {json_file.relative_to(ROOT)}: {error}")


def main() -> int:
    require_files()
    validate_skills()
    validate_csv()
    validate_requirements()
    validate_links()
    validate_json()

    if ERRORS:
        print("VALIDATION FAILED")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
