from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class VisualCriterion(str, Enum):
    ALIGNMENT = "alignment"
    CLIPPING = "clipping"
    OVERLAP = "overlap"
    MISSING_LABELS = "missing-labels"
    BLANK_STATES = "blank-states"
    RESPONSIVE_RENDERING = "responsive-rendering"
    BASELINE_DIFFERENCE = "baseline-difference"


class DeterministicResult(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    BLOCKED = "blocked"
    REVIEW_NEEDED = "review-needed"


class VisualDisposition(str, Enum):
    NO_VISUAL_FINDINGS = "no-visual-findings"
    REVIEW_NEEDED = "review-needed"


@dataclass(frozen=True)
class ArtifactReference:
    artifact_type: str
    reference: str
    claim: str
    provenance: str


@dataclass(frozen=True)
class Screenshot:
    artifact: ArtifactReference
    viewport: str


@dataclass(frozen=True)
class ApprovedBaseline:
    artifact: ArtifactReference
    version: str
    approved: bool


@dataclass(frozen=True)
class VisualRubric:
    version: str
    criteria: tuple[str, ...]


@dataclass(frozen=True)
class ModelDeploymentVersion:
    provider: str
    model: str
    deployment_version: str


@dataclass(frozen=True)
class PromptSkillVersion:
    prompt_version: str
    skill_version: str


@dataclass(frozen=True)
class VisualEvaluationRequest:
    screenshot: Screenshot
    baseline: ApprovedBaseline
    rubric: VisualRubric
    model: ModelDeploymentVersion
    prompt_skill: PromptSkillVersion
    deterministic_result: DeterministicResult


@dataclass(frozen=True)
class Observation:
    criterion: str
    finding: bool | None
    uncertainty: bool = False
    region: str | None = None
    confidence: float | None = None
    rationale: str = ""


@dataclass(frozen=True)
class ProviderResponse:
    observations: tuple[Observation, ...]
    raw_output: ArtifactReference


@dataclass(frozen=True)
class VisualEvaluationResult:
    disposition: VisualDisposition
    observations: tuple[Observation, ...]
    deterministic_result: DeterministicResult
    artifacts: tuple[ArtifactReference, ...]
    review_reasons: tuple[str, ...]


class VisualInferenceProvider(Protocol):
    def evaluate(self, request: VisualEvaluationRequest) -> ProviderResponse:
        """Return visual-only observations and a reference to the raw output."""
