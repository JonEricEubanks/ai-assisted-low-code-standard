import json
import pathlib
import re
import unittest


WORKSTREAM = pathlib.Path(__file__).resolve().parent
SCENARIO_FILE = WORKSTREAM / "recovery-scenarios.json"
GUIDE_FILE = WORKSTREAM / "recovery-scenarios.md"
REQUIRED_SCENARIO_FIELDS = {
    "id",
    "family",
    "title",
    "requirements",
    "preconditions",
    "synthetic_inputs",
    "injected_condition",
    "expected_results",
    "observed_results",
    "duplicate_prevention_retry_recovery",
    "evidence_to_collect",
    "human_review_requirements",
}
REQUIRED_FAMILIES = {
    "happy_path",
    "invalid_missing_input",
    "duplicate_delivery",
    "concurrent_duplicate",
    "authentication_failure",
    "timeout_uncertain_completion",
    "throttling_bounded_retry",
    "exhausted_retries",
    "partial_failure_recovery",
    "approval_approve",
    "approval_reject",
    "approval_reassign",
    "approval_expire",
    "service_identity_continuity",
    "notification_failure",
    "correlation_safe_logging",
}
SECRET_OR_ENDPOINT = re.compile(
    r"https?://|(?:password|passwd|secret|access[_-]?token|api[_-]?key)\s*[:=]\s*"
    r"""["'][^"']+["']""",
    re.IGNORECASE,
)


class RecoveryScenarioPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(SCENARIO_FILE.read_text(encoding="utf-8"))
        cls.scenarios = cls.document["scenarios"]
        cls.guide = GUIDE_FILE.read_text(encoding="utf-8")

    def test_pack_declares_offline_unexecuted_status(self):
        pack = self.document["pack"]
        self.assertEqual(pack["source_status"], "fully_fictional_offline_reference")
        self.assertEqual(pack["execution_status"], "not_executed")
        self.assertIs(pack["platform_execution_claim"], False)
        self.assertIn("environment_specific_validation", pack["flow_actions_and_connector_semantics"])
        self.assertIn("not executed", self.guide.lower())

    def test_scenarios_have_stable_unique_ids_and_required_fields(self):
        ids = [scenario["id"] for scenario in self.scenarios]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            ids,
            [f"TST-FLOW-{number:03}" for number in range(1, len(ids) + 1)],
        )
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario["id"]):
                self.assertTrue(REQUIRED_SCENARIO_FIELDS.issubset(scenario))
                self.assertTrue(scenario["requirements"])
                self.assertTrue(all(
                    re.fullmatch(r"REQ-\d{3}", requirement)
                    for requirement in scenario["requirements"]
                ))
                for field in (
                    "preconditions",
                    "evidence_to_collect",
                    "human_review_requirements",
                ):
                    self.assertTrue(scenario[field], field)
                self.assertTrue(scenario["injected_condition"])

    def test_required_failure_recovery_and_approval_families_are_covered(self):
        families = {scenario["family"] for scenario in self.scenarios}
        self.assertTrue(REQUIRED_FAMILIES.issubset(families))

    def test_expected_and_observed_results_are_distinct(self):
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario["id"]):
                expected = scenario["expected_results"]
                observed = scenario["observed_results"]
                self.assertTrue(expected["state_transition"])
                self.assertTrue(expected["observable_behavior"])
                self.assertEqual(observed["status"], "not_observed")
                self.assertIn("no flow was run", observed["detail"].lower())

    def test_retry_replay_and_compensation_are_explicit(self):
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario["id"]):
                recovery = scenario["duplicate_prevention_retry_recovery"]
                self.assertTrue(recovery["duplicate_prevention"])
                self.assertTrue(recovery["automatic_retry"])
                self.assertTrue(recovery["human_authorized_replay"])
                self.assertTrue(recovery["compensating_action"])
        self.assertIn("try", self.guide.lower())
        self.assertIn("catch", self.guide.lower())
        self.assertIn("finally", self.guide.lower())
        self.assertIn("run-after", self.guide.lower())
        self.assertIn("exactly-once", self.guide.lower())

    def test_fixtures_contain_no_real_endpoints_or_secret_literals(self):
        serialized = json.dumps(self.document)
        self.assertNotRegex(serialized, SECRET_OR_ENDPOINT)
        self.assertNotIn("SYNTHETIC-DO-NOT-LOG", self.guide)

    def test_guide_documents_unknown_platform_semantics(self):
        for phrase in (
            "connector retry",
            "idempotency storage",
            "concurrency semantics",
            "environment-specific validation",
            "native run history",
            "unresolved platform-specific questions",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.guide.lower())


if __name__ == "__main__":
    unittest.main()
