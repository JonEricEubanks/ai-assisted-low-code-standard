from __future__ import annotations

from .models import (
    ApprovedBaseline,
    ArtifactReference,
    DeterministicResult,
    ModelDeploymentVersion,
    Observation,
    PromptSkillVersion,
    ProviderResponse,
    Screenshot,
    VisualCriterion,
    VisualDisposition,
    VisualEvaluationRequest,
    VisualEvaluationResult,
    VisualInferenceProvider,
    VisualRubric,
)


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _artifact_is_provenanced(artifact: object, expected_type: str) -> bool:
    if not isinstance(artifact, ArtifactReference):
        return False
    return all(
        _nonempty_string(value)
        for value in (
            artifact.reference,
            artifact.claim,
            artifact.provenance,
        )
    ) and artifact.artifact_type == expected_type


class VisualEvaluator:
    """Read-only visual evaluator; its output has no release authority."""

    def __init__(self, provider: VisualInferenceProvider) -> None:
        self._provider = provider

    def evaluate(self, request: VisualEvaluationRequest) -> VisualEvaluationResult:
        reasons = self._request_review_reasons(request)
        if reasons:
            return self._result(
                request,
                VisualDisposition.REVIEW_NEEDED,
                (),
                (),
                reasons,
            )

        try:
            response = self._provider.evaluate(request)
        except Exception:
            return self._result(
                request,
                VisualDisposition.REVIEW_NEEDED,
                (),
                (),
                ("provider evaluation failed",),
            )

        if not isinstance(response, ProviderResponse):
            return self._result(
                request,
                VisualDisposition.REVIEW_NEEDED,
                (),
                (),
                ("provider returned an unsupported response",),
            )

        artifacts = (request.screenshot.artifact, request.baseline.artifact)
        if _artifact_is_provenanced(response.raw_output, "evaluator-output"):
            artifacts += (response.raw_output,)
        else:
            reasons.append("raw evaluator output is missing a valid artifact reference")

        reasons.extend(self._observation_review_reasons(request, response))
        if request.deterministic_result is not DeterministicResult.PASS:
            reasons.append(
                "deterministic result is not pass; visual evaluation cannot override it"
            )
        elif any(observation.finding for observation in response.observations):
            reasons.append("visual finding conflicts with deterministic pass")

        disposition = (
            VisualDisposition.REVIEW_NEEDED
            if reasons
            else VisualDisposition.NO_VISUAL_FINDINGS
        )

        return self._result(
            request,
            disposition,
            response.observations,
            artifacts,
            tuple(reasons),
        )

    @staticmethod
    def _request_review_reasons(request: VisualEvaluationRequest) -> list[str]:
        reasons: list[str] = []
        if not isinstance(request.screenshot, Screenshot) or not (
            _artifact_is_provenanced(request.screenshot.artifact, "screenshot")
        ):
            reasons.append("screenshot provenance is missing or invalid")
        if (
            not isinstance(request.screenshot, Screenshot)
            or not _nonempty_string(request.screenshot.viewport)
        ):
            reasons.append("screenshot viewport is missing")
        if (
            not isinstance(request.baseline, ApprovedBaseline)
            or not _artifact_is_provenanced(
                request.baseline.artifact, "screenshot"
            )
            or not _nonempty_string(request.baseline.version)
            or request.baseline.approved is not True
        ):
            reasons.append("approved baseline provenance is missing or invalid")
        if (
            not isinstance(request.rubric, VisualRubric)
            or not _nonempty_string(request.rubric.version)
            or not isinstance(request.rubric.criteria, tuple)
            or not request.rubric.criteria
            or any(
                not isinstance(criterion, str)
                for criterion in request.rubric.criteria
            )
            or any(
                criterion not in {item.value for item in VisualCriterion}
                for criterion in request.rubric.criteria
                if isinstance(criterion, str)
            )
            or (
                isinstance(request.rubric.criteria, tuple)
                and all(
                    isinstance(criterion, str)
                    for criterion in request.rubric.criteria
                )
                and len(set(request.rubric.criteria)) != len(request.rubric.criteria)
            )
        ):
            reasons.append("rubric is missing, duplicated, or includes unsupported criteria")
        if (
            not isinstance(request.model, ModelDeploymentVersion)
            or not isinstance(request.prompt_skill, PromptSkillVersion)
            or not all(
                _nonempty_string(value)
                for value in (
                    request.model.provider,
                    request.model.model,
                    request.model.deployment_version,
                    request.prompt_skill.prompt_version,
                    request.prompt_skill.skill_version,
                )
            )
        ):
            reasons.append("model, deployment, prompt, or skill provenance is missing")
        if not isinstance(request.deterministic_result, DeterministicResult):
            reasons.append("deterministic result is missing or unsupported")
        return reasons

    @staticmethod
    def _observation_review_reasons(
        request: VisualEvaluationRequest, response: ProviderResponse
    ) -> list[str]:
        reasons: list[str] = []
        if not isinstance(response.observations, tuple) or not response.observations:
            return ["provider observations are missing or malformed"]

        criteria = set(request.rubric.criteria)
        seen: dict[str, bool | None] = {}
        for observation in response.observations:
            if not isinstance(observation, Observation):
                reasons.append("provider returned a malformed observation")
                continue
            if (
                not isinstance(observation.criterion, str)
                or observation.criterion not in criteria
            ):
                reasons.append("provider returned an unsupported visual criterion")
                continue
            if observation.criterion in seen:
                if seen[observation.criterion] != observation.finding:
                    reasons.append("provider returned conflicting observations")
                else:
                    reasons.append("provider returned duplicate observations")
            seen[observation.criterion] = observation.finding
            if (
                not isinstance(observation.uncertainty, bool)
                or observation.uncertainty
                or (
                    observation.finding is not None
                    and not isinstance(observation.finding, bool)
                )
                or observation.finding is None
                or (
                    observation.confidence is not None
                    and (
                        isinstance(observation.confidence, bool)
                        or not isinstance(observation.confidence, (int, float))
                        or not 0 <= observation.confidence <= 1
                    )
                )
            ):
                reasons.append("provider observation is uncertain or invalid")

        if criteria - seen.keys():
            reasons.append("provider omitted one or more rubric criteria")
        return reasons

    @staticmethod
    def _result(
        request: VisualEvaluationRequest,
        disposition: VisualDisposition,
        observations: tuple[Observation, ...],
        artifacts: tuple[ArtifactReference, ...],
        reasons: tuple[str, ...] | list[str],
    ) -> VisualEvaluationResult:
        return VisualEvaluationResult(
            disposition=disposition,
            observations=observations,
            deterministic_result=request.deterministic_result,
            artifacts=artifacts,
            review_reasons=tuple(reasons),
        )
