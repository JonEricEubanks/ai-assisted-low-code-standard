from __future__ import annotations

import copy
import unittest

from scripts.run_foundry_shadow_eval import APPROVED_SCOPE, normalize_shadow_run


class ShadowEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = {
            "records": [
                {
                    "testId": "TST-QA-001",
                    "result": "pass",
                    "actual": "Tenant content must not be returned.",
                    "artifacts": [{"type": "screenshot", "reference": "private.png"}],
                },
                {"testId": "TST-QA-002", "result": "review-needed"},
            ]
        }

    def test_normalizes_results_and_preserves_review_needed(self) -> None:
        summary = normalize_shadow_run(self.fixture, APPROVED_SCOPE)

        self.assertEqual(summary["mode"], "shadow")
        self.assertEqual(summary["overallResult"], "review-needed")
        self.assertEqual(
            summary["resultCounts"],
            {"pass": 1, "fail": 0, "blocked": 0, "review-needed": 1},
        )
        self.assertEqual(
            summary["evaluations"],
            [
                {"testId": "TST-QA-001", "result": "pass"},
                {"testId": "TST-QA-002", "result": "review-needed"},
            ],
        )
        self.assertEqual(summary["releaseAuthorization"], "not-authorized")

    def test_summary_omits_untrusted_fixture_content(self) -> None:
        summary = normalize_shadow_run(self.fixture, APPROVED_SCOPE)
        serialized = str(summary)

        self.assertNotIn("Tenant content", serialized)
        self.assertNotIn("private.png", serialized)
        self.assertNotIn("release-ready", serialized)

    def test_wrong_or_missing_scope_fails_closed(self) -> None:
        for key, value in (
            ("subscriptionId", "wrong-subscription"),
            ("resourceGroup", "wrong-resource-group"),
            ("region", "westus"),
            ("region", None),
        ):
            with self.subTest(key=key, value=value):
                scope = copy.deepcopy(APPROVED_SCOPE)
                if value is None:
                    scope.pop(key)
                else:
                    scope[key] = value
                with self.assertRaisesRegex(ValueError, "approved Foundry QA scope"):
                    normalize_shadow_run(self.fixture, scope)

    def test_malformed_or_duplicate_results_are_rejected(self) -> None:
        malformed_fixtures = [
            {"records": []},
            {"records": [{"testId": "bad", "result": "pass"}]},
            {"records": [{"testId": "TST-QA-001", "result": "unknown"}]},
            {
                "records": [
                    {"testId": "TST-QA-001", "result": "pass"},
                    {"testId": "TST-QA-001", "result": "fail"},
                ]
            },
        ]
        for fixture in malformed_fixtures:
            with self.subTest(fixture=fixture):
                with self.assertRaises(ValueError):
                    normalize_shadow_run(fixture, APPROVED_SCOPE)

    def test_blocked_results_require_review(self) -> None:
        summary = normalize_shadow_run(
            {"records": [{"testId": "TST-QA-001", "result": "blocked"}]},
            APPROVED_SCOPE,
        )

        self.assertEqual(summary["overallResult"], "review-needed")


if __name__ == "__main__":
    unittest.main()
