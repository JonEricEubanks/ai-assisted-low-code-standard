from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_HEADERS = (
    "Measurement ID",
    "Project",
    "Activity",
    "Standard Version",
    "Developer",
    "Start Definition",
    "Stop Definition",
    "Baseline Minutes",
    "AI Assisted Minutes",
    "Human Review Minutes",
    "Rework Minutes",
    "Waiting Minutes",
    "Deployment Minutes",
    "Defects Sev1",
    "Defects Sev2",
    "Defects Sev3",
    "Defects Sev4",
    "Escaped Defects",
    "Critical Tests Planned",
    "Critical Tests Passed",
    "Documentation Completeness Percent",
    "Independent Assistance Minutes",
    "Sample Size",
    "Data Source",
    "Exclusions",
    "Actual or Estimate",
    "Notes",
)
GROUP_FIELDS = (
    "Project",
    "Activity",
    "Standard Version",
    "Start Definition",
    "Stop Definition",
)
DURATION_FIELDS = (
    "Baseline Minutes",
    "AI Assisted Minutes",
    "Human Review Minutes",
    "Rework Minutes",
    "Waiting Minutes",
    "Deployment Minutes",
    "Independent Assistance Minutes",
)
COUNT_FIELDS = (
    "Defects Sev1",
    "Defects Sev2",
    "Defects Sev3",
    "Defects Sev4",
    "Escaped Defects",
    "Critical Tests Planned",
    "Critical Tests Passed",
)
PERCENT_FIELDS = ("Documentation Completeness Percent",)


class InputError(Exception):
    def __init__(self, diagnostics: list[str]):
        self.diagnostics = diagnostics
        super().__init__("\n".join(diagnostics))


def _number(
    value: str,
    field: str,
    row_number: int,
    diagnostics: list[str],
    *,
    integer: bool = False,
    maximum: float | None = None,
) -> int | float | None:
    if not value:
        return None
    try:
        if integer:
            parsed: int | float = int(value)
        else:
            parsed = float(value)
            if not math.isfinite(parsed):
                raise ValueError
    except ValueError:
        expected = "a non-negative integer" if integer else "a finite number"
        diagnostics.append(f"Row {row_number}: {field} must be {expected}; got {value!r}.")
        return None

    if parsed < 0 or (maximum is not None and parsed > maximum):
        range_description = (
            f"between 0 and {maximum:g}" if maximum is not None else "non-negative"
        )
        diagnostics.append(
            f"Row {row_number}: {field} must be {range_description}; got {value!r}."
        )
        return None
    return parsed


def read_observations(input_path: Path) -> list[dict[str, Any]]:
    diagnostics: list[str] = []
    observations: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    try:
        with input_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            try:
                headers = next(reader)
            except StopIteration:
                return []

            duplicates = sorted({name for name in headers if headers.count(name) > 1})
            if duplicates:
                diagnostics.append(f"CSV header contains duplicate columns: {', '.join(duplicates)}.")
            missing_headers = [name for name in REQUIRED_HEADERS if name not in headers]
            if missing_headers:
                diagnostics.append(f"CSV is missing required headers: {', '.join(missing_headers)}.")
            if diagnostics:
                raise InputError(diagnostics)

            indices = {name: headers.index(name) for name in REQUIRED_HEADERS}
            for row_number, values in enumerate(reader, start=2):
                if not values:
                    continue
                if len(values) != len(headers):
                    diagnostics.append(
                        f"Row {row_number}: expected {len(headers)} columns, found {len(values)}; "
                        "check for malformed CSV quoting or row width."
                    )
                    continue

                row = {name: values[index].strip() for name, index in indices.items()}
                measurement_id = row["Measurement ID"]
                if not measurement_id:
                    diagnostics.append(f"Row {row_number}: Measurement ID is required.")
                elif measurement_id in seen_ids:
                    diagnostics.append(
                        f"Row {row_number}: duplicate Measurement ID {measurement_id!r}; "
                        "each observation must have a unique ID."
                    )
                else:
                    seen_ids.add(measurement_id)

                for field in GROUP_FIELDS:
                    if not row[field]:
                        diagnostics.append(f"Row {row_number}: {field} is required for comparison.")
                claim_class = row["Actual or Estimate"].casefold()
                if claim_class not in ("actual", "estimate"):
                    diagnostics.append(
                        f"Row {row_number}: Actual or Estimate must be 'Actual' or 'Estimate'; "
                        f"got {row['Actual or Estimate']!r}."
                    )
                if not row["Data Source"]:
                    diagnostics.append(f"Row {row_number}: Data Source is required.")

                sample_size = _number(
                    row["Sample Size"], "Sample Size", row_number, diagnostics, integer=True
                )
                if sample_size != 1:
                    diagnostics.append(
                        f"Row {row_number}: Sample Size must be 1 (one task observation per row); "
                        "split pre-aggregated data into individual observations."
                    )
                for field in DURATION_FIELDS:
                    row[field] = _number(row[field], field, row_number, diagnostics)
                for field in COUNT_FIELDS:
                    row[field] = _number(
                        row[field], field, row_number, diagnostics, integer=True
                    )
                for field in PERCENT_FIELDS:
                    row[field] = _number(
                        row[field], field, row_number, diagnostics, maximum=100
                    )

                planned = row["Critical Tests Planned"]
                passed = row["Critical Tests Passed"]
                if planned is not None and passed is not None and passed > planned:
                    diagnostics.append(
                        f"Row {row_number}: Critical Tests Passed ({passed}) cannot exceed "
                        f"Critical Tests Planned ({planned})."
                    )

                row["_row_number"] = row_number
                row["_claim_class"] = claim_class
                observations.append(row)
    except csv.Error as error:
        diagnostics.append(f"Malformed CSV near row {getattr(reader, 'line_num', '?')}: {error}.")
    except OSError as error:
        diagnostics.append(f"Cannot read input CSV {input_path}: {error}.")

    if diagnostics:
        raise InputError(diagnostics)
    return observations


def _summary(values: list[int | float]) -> dict[str, Any]:
    if not values:
        return {
            "status": "unknown",
            "observation_count": 0,
            "median": None,
            "minimum": None,
            "maximum": None,
        }
    return {
        "status": "available",
        "observation_count": len(values),
        "median": statistics.median(values),
        "minimum": min(values),
        "maximum": max(values),
    }


def _group_report(key: tuple[str, ...], rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = {
        field: _summary([row[field] for row in rows if row[field] is not None])
        for field in (*DURATION_FIELDS, *COUNT_FIELDS, *PERCENT_FIELDS)
    }
    paired_changes = [
        row["Baseline Minutes"] - row["AI Assisted Minutes"]
        for row in rows
        if row["Baseline Minutes"] is not None and row["AI Assisted Minutes"] is not None
    ]
    return {
        "comparison": {
            **dict(zip(GROUP_FIELDS, key[: len(GROUP_FIELDS)])),
            "claim_class": key[-1],
        },
        "sample_size": len(rows),
        "metrics": metrics,
        "paired_duration_change_minutes": _summary(paired_changes),
        "sources": sorted({row["Data Source"] for row in rows}),
        "exclusions": sorted({row["Exclusions"] for row in rows if row["Exclusions"]}),
        "limitations": [
            "Baseline Minutes and AI Assisted Minutes are paired per-task durations using the supplied start/stop definitions.",
            "Duration change is Baseline Minutes minus AI Assisted Minutes; positive values mean shorter assisted duration.",
            "Review, rework, waiting, deployment, and assistance are reported separately and are not added to either duration; components may overlap.",
            "Only pairs with both durations present contribute to duration change; missing values are unknown, not zero.",
            "This descriptive comparison does not establish causation or organization-wide improvement.",
            "The sample range is descriptive; no confidence interval or uncertainty estimate is calculated.",
        ],
    }


def analyze(observations: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in observations:
        key = (*(row[field] for field in GROUP_FIELDS), row["_claim_class"])
        grouped[key].append(row)

    sources = [row["Data Source"].casefold().startswith("synthetic:") for row in observations]
    if sources and all(sources):
        classification = "synthetic"
    elif any(sources):
        classification = "mixed"
    else:
        classification = "unclassified"

    groups = [_group_report(key, grouped[key]) for key in sorted(grouped)]
    has_paired_data = any(
        group["paired_duration_change_minutes"]["observation_count"] for group in groups
    )
    return {
        "schema_version": 1,
        "status": "reported" if has_paired_data else "insufficient_data",
        "dataset_classification": classification,
        "observation_count": len(observations),
        "group_count": len(groups),
        "groups": groups,
        "limitations": [
            "This report summarizes the supplied observations only and makes no causal or organization-wide claim.",
            "Actual and estimate observations are reported in separate groups.",
            "An empty input or absence of paired durations is insufficient data, not realized savings.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report descriptive baseline versus AI-assisted measurements from the metrics CSV contract."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input baseline-and-outcomes CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Path for machine-readable JSON output.")
    args = parser.parse_args(argv)

    if os.path.abspath(args.input) == os.path.abspath(args.output):
        print("Input and output paths must be different.", file=sys.stderr)
        return 2
    try:
        report = analyze(read_observations(args.input))
    except InputError as error:
        for diagnostic in error.diagnostics:
            print(diagnostic, file=sys.stderr)
        return 2

    try:
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(report, handle, indent=2, allow_nan=False)
            handle.write("\n")
    except OSError as error:
        print(f"Cannot write output JSON {args.output}: {error}.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
