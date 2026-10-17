from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import analyze_outcomes


METRICS_DIR = Path(__file__).resolve().parent
FIXTURE = METRICS_DIR / "fixtures" / "synthetic-outcomes.csv"
SCRIPT = METRICS_DIR / "analyze_outcomes.py"


class AnalyzeOutcomesTests(unittest.TestCase):
    def load_fixture(self) -> dict:
        with FIXTURE.open(encoding="utf-8", newline="") as handle:
            return next(csv.DictReader(handle))

    def write_csv(self, path: Path, rows: list[dict], headers: list[str] | None = None) -> None:
        headers = headers or list(analyze_outcomes.REQUIRED_HEADERS)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(
                {field: row[field] for field in headers if field in row} for row in rows
            )

    def analyze_rows(self, rows: list[dict]) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            self.write_csv(input_path, rows)
            return analyze_outcomes.analyze(analyze_outcomes.read_observations(input_path))

    def test_actual_estimate_incompatible_groups_and_known_arithmetic(self) -> None:
        report = analyze_outcomes.analyze(analyze_outcomes.read_observations(FIXTURE))
        self.assertEqual("synthetic", report["dataset_classification"])
        self.assertEqual("reported", report["status"])
        self.assertEqual(5, report["observation_count"])
        self.assertEqual(3, report["group_count"])

        build_actual = next(
            group
            for group in report["groups"]
            if group["comparison"]["Activity"] == "Build task"
            and group["comparison"]["claim_class"] == "actual"
        )
        self.assertEqual(3, build_actual["sample_size"])
        self.assertEqual(
            {"status": "available", "observation_count": 3, "median": 100.0, "minimum": 80.0, "maximum": 120.0},
            build_actual["metrics"]["Baseline Minutes"],
        )
        self.assertEqual(
            {"status": "available", "observation_count": 3, "median": 20.0, "minimum": -20.0, "maximum": 30.0},
            build_actual["paired_duration_change_minutes"],
        )
        self.assertEqual("estimate", next(
            group["comparison"]["claim_class"]
            for group in report["groups"]
            if group["comparison"]["Activity"] == "Build task"
            and group["comparison"]["claim_class"] == "estimate"
        ))
        self.assertEqual(
            {"status": "available", "observation_count": 3, "median": 10.0, "minimum": 0.0, "maximum": 20.0},
            build_actual["metrics"]["Human Review Minutes"],
        )
        self.assertEqual(["synthetic: invented fixture"], build_actual["sources"])

    def test_missing_is_unknown_and_zero_is_observed(self) -> None:
        row = self.load_fixture()
        row["Baseline Minutes"] = ""
        row["AI Assisted Minutes"] = "0"
        row["Human Review Minutes"] = "0"
        report = self.analyze_rows([row])
        group = report["groups"][0]
        self.assertEqual("unknown", group["metrics"]["Baseline Minutes"]["status"])
        self.assertIsNone(group["metrics"]["Baseline Minutes"]["median"])
        self.assertEqual(0.0, group["metrics"]["AI Assisted Minutes"]["median"])
        self.assertEqual(0.0, group["metrics"]["Human Review Minutes"]["median"])
        self.assertEqual("unknown", group["paired_duration_change_minutes"]["status"])
        self.assertEqual("insufficient_data", report["status"])

    def test_zero_baseline_has_change_but_no_percent_improvement(self) -> None:
        row = self.load_fixture()
        row["Baseline Minutes"] = "0"
        row["AI Assisted Minutes"] = "5"
        group = self.analyze_rows([row])["groups"][0]
        self.assertEqual(-5.0, group["paired_duration_change_minutes"]["median"])
        self.assertNotIn("percent_improvement", group)

    def test_empty_and_header_only_inputs_are_insufficient_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_path = Path(temp_dir) / "empty.csv"
            empty_path.write_text("", encoding="utf-8")
            report = analyze_outcomes.analyze(analyze_outcomes.read_observations(empty_path))
            self.assertEqual("insufficient_data", report["status"])
            self.assertEqual(0, report["observation_count"])

            header_path = Path(temp_dir) / "header.csv"
            self.write_csv(header_path, [])
            report = analyze_outcomes.analyze(analyze_outcomes.read_observations(header_path))
            self.assertEqual("insufficient_data", report["status"])
            self.assertEqual([], report["groups"])

    def test_invalid_numeric_data_and_sample_size_are_rejected(self) -> None:
        invalid_cases = (
            ("Baseline Minutes", "-1", "non-negative"),
            ("AI Assisted Minutes", "nan", "finite number"),
            ("Documentation Completeness Percent", "101", "between 0 and 100"),
            ("Defects Sev1", "1.5", "non-negative integer"),
            ("Sample Size", "2", "Sample Size must be 1"),
            ("Critical Tests Planned", "1", "cannot exceed"),
        )
        for field, value, expected_message in invalid_cases:
            with self.subTest(field=field):
                row = self.load_fixture()
                row[field] = value
                with tempfile.TemporaryDirectory() as temp_dir:
                    input_path = Path(temp_dir) / "invalid.csv"
                    self.write_csv(input_path, [row])
                    with self.assertRaises(analyze_outcomes.InputError) as raised:
                        analyze_outcomes.read_observations(input_path)
                    self.assertIn(expected_message, str(raised.exception))

    def test_duplicate_ids_and_malformed_row_are_rejected(self) -> None:
        row = self.load_fixture()
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "duplicates.csv"
            self.write_csv(input_path, [row, row])
            with self.assertRaisesRegex(analyze_outcomes.InputError, "duplicate Measurement ID"):
                analyze_outcomes.read_observations(input_path)

            input_path.write_text(",".join(analyze_outcomes.REQUIRED_HEADERS) + "\nshort,row\n", encoding="utf-8")
            with self.assertRaisesRegex(analyze_outcomes.InputError, "expected 27 columns"):
                analyze_outcomes.read_observations(input_path)

    def test_missing_required_header_is_rejected(self) -> None:
        row = self.load_fixture()
        headers = [header for header in analyze_outcomes.REQUIRED_HEADERS if header != "Project"]
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "missing.csv"
            self.write_csv(input_path, [row], headers)
            with self.assertRaisesRegex(analyze_outcomes.InputError, "missing required headers: Project"):
                analyze_outcomes.read_observations(input_path)

    def test_cli_writes_json_and_invalid_input_exits_without_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "fixture.csv"
            output_path = Path(temp_dir) / "report.json"
            input_path.write_bytes(FIXTURE.read_bytes())
            success = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, success.returncode, success.stderr)
            self.assertEqual("synthetic", json.loads(output_path.read_text())["dataset_classification"])

            bad_path = Path(temp_dir) / "bad.csv"
            row = self.load_fixture()
            row["Sample Size"] = "5"
            self.write_csv(bad_path, [row])
            output_path.unlink()
            failure = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(bad_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, failure.returncode)
            self.assertIn("Sample Size must be 1", failure.stderr)
            self.assertFalse(output_path.exists())

    def test_cli_requires_explicit_paths(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("--input", result.stderr)
        self.assertIn("--output", result.stderr)


if __name__ == "__main__":
    unittest.main()
