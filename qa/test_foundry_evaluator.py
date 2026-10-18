from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from qa.foundry.evaluator import VisualEvaluator
from qa.foundry.models import (
    ApprovedBaseline,
    ArtifactReference,
    DeterministicResult,
    ModelDeploymentVersion,
    Observation,
    PromptSkillVersion,
    ProviderResponse,
    Screenshot,
    VisualDisposition,
    VisualEvaluationRequest,
    VisualRubric,
)


QA = Path(__file__).resolve().parent


def _request_from_fixture() -> VisualEvaluationRequest:
    data = json.loads(
        (QA / "fixtures" / "foundry-evaluator-request.json").read_text(
            encoding="utf-8"
        )
    )
    return VisualEvaluationRequest(
        screenshot=Screenshot(
            artifact=ArtifactReference(**data["screenshot"]["artifact"]),
            viewport=data["screenshot"]["viewport"],
        ),
        baseline=ApprovedBaseline(
            artifact=ArtifactReference(**data["baseline"]["artifact"]),
            version=data["baseline"]["version"],
            approved=data["baseline"]["approved"],
        ),
        rubric=VisualRubric(
            version=data["rubric"]["version"],
            criteria=tuple(data["rubric"]["criteria"]),
        ),
        model=ModelDeploymentVersion(**data["model"]),
        prompt_skill=PromptSkillVersion(**data["prompt_skill"]),
        deterministic_result=DeterministicResult(data["deterministic_result"]),
    )


def _response_from_fixture() -> ProviderResponse:
    data = json.loads(
        (QA / "fixtures" / "foundry-evaluator-response.json").read_text(
            encoding="utf-8"
        )
    )
    return ProviderResponse(
        observations=tuple(Observation(**item) for item in data["observations"]),
        raw_output=ArtifactReference(**data["raw_output"]),
    )


class FakeProvider:
    def __init__(self, response: Any) -> None:
        self.response = response
        self.calls = 0

    def evaluate(self, request: VisualEvaluationRequest) -> Any:
        self.calls += 1
        return self.response


class VisualEvaluatorTests(unittest.TestCase):
    def test_cloud_and_local_providers_have_identical_adapter_behavior(self) -> None:
        request = _request_from_fixture()
        cloud = FakeProvider(_response_from_fixture())
        local = FakeProvider(_response_from_fixture())

        cloud_result = VisualEvaluator(cloud).evaluate(request)
        local_result = VisualEvaluator(local).evaluate(request)

        self.assertEqual(cloud_result, local_result)
        self.assertEqual(cloud_result.disposition, VisualDisposition.NO_VISUAL_FINDINGS)
        self.assertEqual(cloud.calls, 1)
        self.assertEqual(local.calls, 1)
        self.assertEqual(cloud_result.artifacts[-1].artifact_type, "evaluator-output")
        self.assertFalse(hasattr(cloud_result, "release_decision"))

    def test_uncertain_observation_requires_review(self) -> None:
        request = _request_from_fixture()
        uncertain = json.loads(
            (QA / "fixtures" / "foundry-evaluator-uncertain.json").read_text(
                encoding="utf-8"
            )
        )
        response = _response_from_fixture()
        response = replace(
            response,
            observations=(Observation(**uncertain), response.observations[1]),
        )

        result = VisualEvaluator(FakeProvider(response)).evaluate(request)

        self.assertEqual(result.disposition, VisualDisposition.REVIEW_NEEDED)
        self.assertIn("uncertain", result.review_reasons[0])

    def test_missing_screenshot_provenance_skips_provider(self) -> None:
        request = _request_from_fixture()
        screenshot = replace(
            request.screenshot,
            artifact=replace(request.screenshot.artifact, provenance=""),
        )
        request = replace(request, screenshot=screenshot)
        provider = FakeProvider(_response_from_fixture())

        result = VisualEvaluator(provider).evaluate(request)

        self.assertEqual(result.disposition, VisualDisposition.REVIEW_NEEDED)
        self.assertEqual(provider.calls, 0)
        self.assertIn("screenshot provenance", result.review_reasons[0])

    def test_deterministic_failure_cannot_be_overridden_by_no_findings(self) -> None:
        request = replace(
            _request_from_fixture(),
            deterministic_result=DeterministicResult.FAIL,
        )

        result = VisualEvaluator(FakeProvider(_response_from_fixture())).evaluate(
            request
        )

        self.assertEqual(result.disposition, VisualDisposition.REVIEW_NEEDED)
        self.assertEqual(result.deterministic_result, DeterministicResult.FAIL)
        self.assertTrue(
            any("cannot override" in reason for reason in result.review_reasons)
        )

    def test_conflicting_observations_require_review(self) -> None:
        request = _request_from_fixture()
        response = _response_from_fixture()
        response = replace(
            response,
            observations=(
                response.observations[0],
                replace(response.observations[0], finding=True),
                response.observations[1],
            ),
        )

        result = VisualEvaluator(FakeProvider(response)).evaluate(request)

        self.assertEqual(result.disposition, VisualDisposition.REVIEW_NEEDED)
        self.assertTrue(
            any("conflicting observations" in reason for reason in result.review_reasons)
        )

    def test_visual_finding_conflicting_with_deterministic_pass_requires_review(self) -> None:
        request = _request_from_fixture()
        response = _response_from_fixture()
        response = replace(
            response,
            observations=(
                replace(response.observations[0], finding=True),
                response.observations[1],
            ),
        )

        result = VisualEvaluator(FakeProvider(response)).evaluate(request)

        self.assertEqual(result.disposition, VisualDisposition.REVIEW_NEEDED)
        self.assertTrue(
            any("conflicts with deterministic pass" in reason for reason in result.review_reasons)
        )

    def test_unsupported_criterion_requires_review(self) -> None:
        request = _request_from_fixture()
        response = _response_from_fixture()
        response = replace(
            response,
            observations=(
                replace(response.observations[0], criterion="accessibility"),
                response.observations[1],
            ),
        )

        result = VisualEvaluator(FakeProvider(response)).evaluate(request)

        self.assertEqual(result.disposition, VisualDisposition.REVIEW_NEEDED)
        self.assertTrue(
            any("unsupported visual criterion" in reason for reason in result.review_reasons)
        )


if __name__ == "__main__":
    unittest.main()
