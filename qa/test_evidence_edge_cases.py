from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from deterministic_qa import evaluate_release_gate, validate_evidence_record


QA = Path(__file__).resolve().parent


class EvidenceEdgeCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads(
            (QA / "fixtures" / "deterministic-evidence.json").read_text(
                encoding="utf-8"
            )
        )
        cls.record = fixture["records"][0]

    def test_required_and_unexpected_fields(self) -> None:
        record = copy.deepcopy(self.record)
        del record["runId"]
        del record["retentionTag"]
        record["unexpected"] = "not permitted"

        errors = validate_evidence_record(record)
        self.assertIn("runId is required", errors)
        self.assertIn("retentionTag is required", errors)
        self.assertIn("unexpected is not allowed", errors)

    def test_malformed_run_and_defect_identifiers(self) -> None:
        record = copy.deepcopy(self.record)
        record["runId"] = "RUN-QA-1"
        record["result"] = "fail"
        record["defectId"] = "DEF-QA-1"

        errors = validate_evidence_record(record)
        self.assertIn("runId has an invalid identifier", errors)
        self.assertIn("defectId has an invalid identifier", errors)

    def test_timestamp_requires_iso_datetime_with_timezone(self) -> None:
        record = copy.deepcopy(self.record)
        record["timestamp"] = "2026-10-17T12:00:00+05:30"
        self.assertEqual(validate_evidence_record(record), [])

        record["timestamp"] = "2026-10-17T12:00:00"
        self.assertIn(
            "timestamp must include a UTC or explicit offset",
            validate_evidence_record(record),
        )
        record["timestamp"] = "not-a-date"
        self.assertIn(
            "timestamp must be an ISO 8601 date-time",
            validate_evidence_record(record),
        )

    def test_artifact_type_claim_reference_and_fields_are_validated(self) -> None:
        bad_artifacts = [
            (
                {"type": "document", "reference": "synthetic://artifact", "claim": "supports"},
                "artifacts[0].type is invalid",
            ),
            (
                {"type": "log", "reference": "synthetic://artifact", "claim": ""},
                "artifacts[0].claim is required",
            ),
            (
                {"type": "log", "reference": 7, "claim": "supports"},
                "artifacts[0].reference is required",
            ),
            (
                {
                    "type": "log",
                    "reference": "synthetic://artifact",
                    "claim": "supports",
                    "source": "unexpected",
                },
                "artifacts[0] has an unexpected field",
            ),
        ]
        for artifact, expected_error in bad_artifacts:
            with self.subTest(artifact=artifact):
                record = copy.deepcopy(self.record)
                record["artifacts"] = [artifact]
                self.assertIn(expected_error, validate_evidence_record(record))

    def test_invalid_evidence_field_types_are_rejected(self) -> None:
        record = copy.deepcopy(self.record)
        record["project"] = ["not", "a", "string"]
        record["result"] = True
        record["artifacts"] = "not-an-array"

        errors = validate_evidence_record(record)
        self.assertIn("project must be a non-empty string", errors)
        self.assertIn(
            "result must be pass, fail, blocked, or review-needed", errors
        )
        self.assertIn("artifacts must be a non-empty array", errors)

    def test_failed_evidence_requires_a_well_formed_defect_link(self) -> None:
        record = copy.deepcopy(self.record)
        record.update(result="fail", defectId="DEF-QA-002")
        self.assertEqual(validate_evidence_record(record), [])

        record.pop("defectId")
        self.assertIn(
            "defectId is required when result is fail",
            validate_evidence_record(record),
        )


class ReleaseGateEdgeCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(
            (QA / "fixtures" / "release-gate-input.json").read_text(
                encoding="utf-8"
            )
        )

    def test_malformed_release_inputs_raise_value_error(self) -> None:
        malformed_inputs = [
            (None, "release gate input must be an object"),
            ({"criticalTests": "not-an-array"}, "criticalTests and releaseSensitiveTests must be arrays"),
            ({"releaseSensitiveTests": {}}, "criticalTests and releaseSensitiveTests must be arrays"),
            ({"openFindings": None}, "openFindings must be an array"),
            (
                {"criticalTests": [{"testId": "bad", "result": "pass"}]},
                "criticalTests[0] has an invalid test ID or result",
            ),
            (
                {
                    "releaseSensitiveTests": [
                        {
                            "testId": "TST-QA-001",
                            "category": "unknown",
                            "executed": True,
                            "result": "pass",
                        }
                    ]
                },
                "releaseSensitiveTests[0] has an invalid ID, category, execution state, or result",
            ),
            (
                {"openFindings": [{"severity": "Sev 1", "status": "pending"}]},
                "openFindings[0] has an invalid severity or status",
            ),
        ]
        for malformed, expected_error in malformed_inputs:
            with self.subTest(malformed=malformed):
                inputs = (
                    malformed
                    if malformed is None
                    else {**copy.deepcopy(self.fixture), **malformed}
                )
                with self.assertRaises(ValueError) as error:
                    evaluate_release_gate(inputs)
                self.assertEqual(str(error.exception), expected_error)

    def test_duplicate_critical_test_ids_are_rejected(self) -> None:
        inputs = copy.deepcopy(self.fixture)
        inputs["criticalTests"] = [
            {"testId": "TST-QA-001", "result": "pass"},
            {"testId": "TST-QA-001", "result": "pass"},
        ]

        with self.assertRaisesRegex(ValueError, "duplicate testId"):
            evaluate_release_gate(inputs)

    def test_exact_95_percent_passes_and_immediately_below_fails(self) -> None:
        inputs = copy.deepcopy(self.fixture)
        inputs["criticalTests"] = [
            {"testId": f"TST-QA-{index:03d}", "result": "pass"}
            for index in range(1, 20)
        ] + [{"testId": "TST-QA-020", "result": "fail"}]

        at_threshold = evaluate_release_gate(inputs)
        self.assertEqual(at_threshold["criteria"]["criticalRegressionPassRate"], 0.95)
        self.assertTrue(at_threshold["criteria"]["criticalRegressionAtLeast95Percent"])
        self.assertEqual(at_threshold["recommendation"], "release-ready")
        self.assertEqual(
            at_threshold["residualRisks"],
            [
                {
                    "testId": "TST-QA-020",
                    "result": "fail",
                    "description": "Critical regression did not pass.",
                }
            ],
        )

        inputs["criticalTests"] = [
            {"testId": f"TST-QA-{index:03d}", "result": "pass"}
            for index in range(1, 19)
        ] + [{"testId": "TST-QA-019", "result": "fail"}]
        below_threshold = evaluate_release_gate(inputs)
        self.assertEqual(
            below_threshold["criteria"]["criticalRegressionPassRate"], 18 / 19
        )
        self.assertFalse(
            below_threshold["criteria"]["criticalRegressionAtLeast95Percent"]
        )
        self.assertEqual(below_threshold["recommendation"], "not-ready")
        self.assertEqual(
            below_threshold["residualRisks"],
            [
                {
                    "testId": "TST-QA-019",
                    "result": "fail",
                    "description": "Critical regression did not pass.",
                }
            ],
        )

    def test_blocked_and_review_needed_critical_tests_remain_risks(self) -> None:
        for result in ("blocked", "review-needed"):
            with self.subTest(result=result):
                inputs = copy.deepcopy(self.fixture)
                inputs["criticalTests"] = [
                    {"testId": "TST-QA-003", "result": result}
                ]

                report = evaluate_release_gate(inputs)
                self.assertEqual(report["recommendation"], "not-ready")
                self.assertFalse(
                    report["criteria"]["criticalRegressionAtLeast95Percent"]
                )
                self.assertEqual(
                    report["residualRisks"],
                    [
                        {
                            "testId": "TST-QA-003",
                            "result": result,
                            "description": "Critical regression did not pass.",
                        }
                    ],
                )

    def test_unreviewed_release_sensitive_applicability_blocks_release(self) -> None:
        inputs = copy.deepcopy(self.fixture)
        inputs["releaseSensitiveApplicabilityReviewed"] = False

        report = evaluate_release_gate(inputs)
        self.assertEqual(report["recommendation"], "not-ready")
        self.assertFalse(report["criteria"]["releaseSensitiveApplicabilityReviewed"])
        self.assertFalse(report["criteria"]["releaseSensitivePathsExecuted"])
        self.assertIn(
            {
                "description": "Applicability of release-sensitive paths was not reviewed."
            },
            report["residualRisks"],
        )

    def test_missing_rollback_or_support_evidence_blocks_release(self) -> None:
        for field, criterion, risk in (
            (
                "rollbackEvidence",
                "rollbackEvidenceComplete",
                "Rollback evidence is incomplete.",
            ),
            (
                "supportEvidence",
                "supportEvidenceComplete",
                "Support evidence is incomplete.",
            ),
        ):
            with self.subTest(field=field):
                inputs = copy.deepcopy(self.fixture)
                inputs[field] = False

                report = evaluate_release_gate(inputs)
                self.assertEqual(report["recommendation"], "not-ready")
                self.assertFalse(report["criteria"][criterion])
                self.assertIn({"description": risk}, report["residualRisks"])

    def test_missing_rejected_or_deferred_human_approval_blocks_release(self) -> None:
        approval_cases = [
            ("missing", None),
            ("rejected", {"approver": "Synthetic Approver", "decision": "rejected"}),
            ("deferred", {"approver": "Synthetic Approver", "decision": "deferred"}),
        ]
        for label, approval in approval_cases:
            with self.subTest(approval=label):
                inputs = copy.deepcopy(self.fixture)
                if approval is None:
                    inputs.pop("humanApproval")
                else:
                    inputs["humanApproval"] = approval

                report = evaluate_release_gate(inputs)
                self.assertEqual(report["recommendation"], "not-ready")
                self.assertFalse(report["criteria"]["namedHumanApprovalRecorded"])
                self.assertIn(
                    {
                        "description": "Named human release approval is missing or not approved."
                    },
                    report["residualRisks"],
                )

    def test_empty_critical_suite_is_not_ready_and_is_reported_as_a_risk(self) -> None:
        inputs = copy.deepcopy(self.fixture)
        inputs["criticalTests"] = []

        report = evaluate_release_gate(inputs)
        self.assertEqual(report["recommendation"], "not-ready")
        self.assertEqual(report["criteria"]["criticalRegressionPassRate"], 0)
        self.assertFalse(report["criteria"]["criticalRegressionAtLeast95Percent"])
        self.assertIn(
            {"description": "No critical regression tests were declared."},
            report["residualRisks"],
        )


if __name__ == "__main__":
    unittest.main()
