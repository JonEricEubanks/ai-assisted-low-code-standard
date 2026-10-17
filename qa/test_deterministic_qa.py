from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from deterministic_qa import evaluate_release_gate, validate_evidence_record


QA = Path(__file__).resolve().parent


class EvidenceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads(
            (QA / "fixtures" / "deterministic-evidence.json").read_text(
                encoding="utf-8"
            )
        )
        cls.record = fixture["records"][0]

    def test_sanitized_fixture_is_valid(self) -> None:
        self.assertEqual(validate_evidence_record(self.record), [])

    def test_rejects_invalid_traceability_ids_and_result(self) -> None:
        record = copy.deepcopy(self.record)
        record.update(
            evidenceId="bad-evidence",
            requirementId="bad-requirement",
            testId="bad-test",
            result="unknown",
        )
        errors = validate_evidence_record(record)
        self.assertTrue(any("evidenceId" in error for error in errors))
        self.assertTrue(any("requirementId" in error for error in errors))
        self.assertTrue(any("testId" in error for error in errors))
        self.assertTrue(any("result" in error for error in errors))

    def test_failed_record_requires_a_defect_id(self) -> None:
        record = copy.deepcopy(self.record)
        record["result"] = "fail"
        self.assertIn(
            "defectId is required when result is fail",
            validate_evidence_record(record),
        )


class ReleaseGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inputs = json.loads(
            (QA / "fixtures" / "release-gate-input.json").read_text(
                encoding="utf-8"
            )
        )

    def test_fixture_recommends_release_only_after_all_gates_pass(self) -> None:
        report = evaluate_release_gate(self.inputs)
        self.assertEqual(report["recommendation"], "release-ready")
        self.assertEqual(report["criteria"]["criticalRegressionPassRate"], 1.0)
        self.assertEqual(report["residualRisks"], [])

    def test_95_percent_boundary_passes_and_below_boundary_fails(self) -> None:
        inputs = copy.deepcopy(self.inputs)
        inputs["criticalTests"] = [
            {"testId": f"TST-QA-{index:03d}", "result": "pass"}
            for index in range(1, 20)
        ] + [{"testId": "TST-QA-020", "result": "fail"}]
        report = evaluate_release_gate(inputs)
        self.assertEqual(report["criteria"]["criticalRegressionPassRate"], 0.95)
        self.assertEqual(report["recommendation"], "release-ready")

        inputs["criticalTests"].append(
            {"testId": "TST-QA-021", "result": "fail"}
        )
        report = evaluate_release_gate(inputs)
        self.assertEqual(report["recommendation"], "not-ready")

    def test_open_sev2_and_unexecuted_sensitive_path_block_release(self) -> None:
        inputs = copy.deepcopy(self.inputs)
        inputs["openFindings"] = [
            {
                "findingId": "DEF-QA-001",
                "severity": "Sev 2",
                "status": "open",
                "description": "Synthetic open finding.",
            }
        ]
        inputs["releaseSensitiveTests"][0]["executed"] = False
        report = evaluate_release_gate(inputs)
        self.assertEqual(report["recommendation"], "not-ready")
        self.assertFalse(report["criteria"]["noOpenSev1OrSev2"])
        self.assertFalse(report["criteria"]["releaseSensitivePathsExecuted"])
        self.assertGreaterEqual(len(report["residualRisks"]), 2)

    def test_empty_test_sets_do_not_pass_vacuously(self) -> None:
        inputs = copy.deepcopy(self.inputs)
        inputs["criticalTests"] = []
        inputs["releaseSensitiveTests"] = []
        report = evaluate_release_gate(inputs)
        self.assertEqual(report["recommendation"], "not-ready")
        self.assertEqual(report["criteria"]["criticalRegressionPassRate"], 0)
        self.assertFalse(report["criteria"]["releaseSensitivePathsExecuted"])


if __name__ == "__main__":
    unittest.main()
