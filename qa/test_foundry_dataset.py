from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from foundry.dataset import validate_dataset
from foundry.metrics import evaluate_dataset


QA = Path(__file__).resolve().parent


class FoundryDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(
            (QA / "fixtures" / "foundry-dataset-synthetic.json").read_text(
                encoding="utf-8"
            )
        )

    def test_synthetic_fixture_is_valid_and_metrics_are_checkable(self) -> None:
        self.assertEqual(validate_dataset(self.fixture), [])
        report = evaluate_dataset(self.fixture)

        self.assertEqual(
            report["confusionCounts"],
            {
                "truePositive": 1,
                "falsePositive": 1,
                "trueNegative": 1,
                "falseNegative": 1,
            },
        )
        self.assertEqual(report["precision"], 0.5)
        self.assertEqual(report["recall"], 0.5)
        self.assertEqual(report["falsePositiveRate"], 0.5)
        self.assertEqual(report["falseNegativeRate"], 0.5)
        self.assertEqual(report["uncertainCount"], 1)
        self.assertEqual(report["uncertainRate"], 0.2)
        self.assertEqual(
            report["perCategory"]["layout"]["confusionCounts"]["truePositive"], 1
        )
        self.assertEqual(report["disposition"], "blocked")
        self.assertEqual(report["highImpactFalseNegativeCaseIds"], ["FDE-CASE-004"])

    def test_required_references_context_and_independent_labels_are_validated(self) -> None:
        dataset = copy.deepcopy(self.fixture)
        case = dataset["cases"][0]
        case.update(caseId="not-stable", requirementId="bad", testId="bad")
        case["viewport"]["width"] = True
        case["environment"] = ""
        case["state"] = ""
        case["baselineReference"] = ""
        case["classification"] = ""
        case["retentionTag"] = ""
        case["labels"][1]["annotatorId"] = case["labels"][0]["annotatorId"]

        errors = validate_dataset(dataset)
        self.assertIn("cases[0].caseId has an invalid identifier", errors)
        self.assertIn("cases[0].requirementId has an invalid identifier", errors)
        self.assertIn("cases[0].testId has an invalid identifier", errors)
        self.assertIn("cases[0].viewport must have positive integer width and height", errors)
        self.assertIn("cases[0].labels must have two independent annotators", errors)
        for field in (
            "environment",
            "state",
            "baselineReference",
            "classification",
            "retentionTag",
        ):
            self.assertIn(
                f"cases[0].{field} must be a non-empty string",
                errors,
            )

    def test_near_duplicate_journey_or_scenario_cannot_cross_splits(self) -> None:
        dataset = copy.deepcopy(self.fixture)
        dataset["cases"][1]["journeyId"] = "jny.checkout"

        errors = validate_dataset(dataset)
        self.assertIn(
            "near-duplicate journey group jnycheckout crosses dataset splits",
            errors,
        )

    def test_unresolved_adjudication_blocks_favorable_disposition(self) -> None:
        dataset = copy.deepcopy(self.fixture)
        dataset["cases"][0]["adjudication"] = {
            "status": "unresolved",
            "adjudicatorId": "Synthetic-Adjudicator-1",
            "defectPresent": None,
            "category": None,
            "impact": "none",
        }

        report = evaluate_dataset(dataset)
        self.assertEqual(report["disposition"], "blocked")
        self.assertEqual(report["unresolvedAdjudicationCaseIds"], ["FDE-CASE-001"])
        self.assertIn("adjudication is unresolved", report["dispositionBlockers"])

    def test_missing_provenance_blocks_favorable_disposition(self) -> None:
        dataset = copy.deepcopy(self.fixture)
        del dataset["cases"][0]["baselineReference"]

        report = evaluate_dataset(dataset)
        self.assertEqual(report["disposition"], "blocked")
        self.assertTrue(
            any("FDE-CASE-001.baselineReference" in gap for gap in report["provenanceGaps"])
        )

    def test_uncertain_only_predictions_have_explicit_empty_denominators(self) -> None:
        dataset = copy.deepcopy(self.fixture)
        dataset["cases"] = [dataset["cases"][0]]
        dataset["cases"][0]["modelPrediction"] = {
            "defectPresent": "uncertain",
            "category": None,
        }
        dataset["cases"][0]["adjudication"]["impact"] = "low"

        report = evaluate_dataset(dataset)
        self.assertEqual(report["confusionCounts"]["truePositive"], 0)
        self.assertIsNone(report["precision"])
        self.assertIsNone(report["recall"])
        self.assertIsNone(report["falsePositiveRate"])
        self.assertIsNone(report["falseNegativeRate"])
        self.assertEqual(report["uncertainCount"], 1)
        self.assertEqual(report["uncertainRate"], 1.0)

    def test_high_impact_false_negative_blocks_favorable_disposition(self) -> None:
        dataset = copy.deepcopy(self.fixture)
        dataset["cases"][0]["modelPrediction"] = {
            "defectPresent": False,
            "category": None,
        }

        report = evaluate_dataset(dataset)
        self.assertEqual(
            report["highImpactFalseNegativeCaseIds"], ["FDE-CASE-001", "FDE-CASE-004"]
        )
        self.assertEqual(report["disposition"], "blocked")
        self.assertIn(
            "one or more high-impact defects were missed",
            report["dispositionBlockers"],
        )


if __name__ == "__main__":
    unittest.main()
