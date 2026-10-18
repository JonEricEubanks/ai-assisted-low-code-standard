from __future__ import annotations

import re
from collections import defaultdict
from typing import Any


CASE_ID = re.compile(r"^FDE-CASE-[0-9]{3}$")
REQUIREMENT_ID = re.compile(r"^REQ-([A-Z0-9]+-)?[0-9]{3}$")
TEST_ID = re.compile(r"^TST-[A-Z0-9]+-[0-9]{3}$")
CATEGORIES = {"accessibility", "content", "layout", "state", "text"}
SPLITS = {"development", "held-out"}
IMPACTS = {"high", "low", "medium", "none"}

PROVENANCE_FIELDS = (
    "caseId",
    "requirementId",
    "testId",
    "solutionVersion",
    "environment",
    "journeyId",
    "scenarioId",
    "split",
    "viewport",
    "state",
    "baselineReference",
    "classification",
    "retentionTag",
)


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_label(value: Any, category: Any) -> bool:
    if not (
        value is True
        or value is False
        or isinstance(value, str) and value == "uncertain"
    ):
        return False
    if value is True:
        return isinstance(category, str) and category in CATEGORIES
    return category is None


def _normalized_group(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def validate_dataset(dataset: Any) -> list[str]:
    if not isinstance(dataset, dict):
        return ["dataset must be an object"]

    errors: list[str] = []
    if not _non_empty_string(dataset.get("datasetId")):
        errors.append("datasetId is required")
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["cases must be a non-empty array"]

    seen_case_ids: set[str] = set()
    split_groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in PROVENANCE_FIELDS:
            if field not in case:
                errors.append(f"{prefix}.{field} is required")
        case_id = case.get("caseId")
        if case_id is not None:
            if not isinstance(case_id, str) or not CASE_ID.fullmatch(case_id):
                errors.append(f"{prefix}.caseId has an invalid identifier")
            elif case_id in seen_case_ids:
                errors.append(f"{prefix}.caseId is duplicated")
            else:
                seen_case_ids.add(case_id)

        for field, pattern in (
            ("requirementId", REQUIREMENT_ID),
            ("testId", TEST_ID),
        ):
            value = case.get(field)
            if value is not None and (
                not isinstance(value, str) or not pattern.fullmatch(value)
            ):
                errors.append(f"{prefix}.{field} has an invalid identifier")

        for field in (
            "solutionVersion",
            "environment",
            "journeyId",
            "scenarioId",
            "state",
            "baselineReference",
            "classification",
            "retentionTag",
        ):
            if field in case and not _non_empty_string(case[field]):
                errors.append(f"{prefix}.{field} must be a non-empty string")

        split = case.get("split")
        if split is not None and (
            not isinstance(split, str) or split not in SPLITS
        ):
            errors.append(f"{prefix}.split must be development or held-out")

        viewport = case.get("viewport")
        if (
            not isinstance(viewport, dict)
            or set(viewport) != {"width", "height"}
            or any(
                isinstance(viewport.get(dimension), bool)
                or not isinstance(viewport.get(dimension), int)
                or viewport[dimension] <= 0
                for dimension in ("width", "height")
            )
        ):
            errors.append(f"{prefix}.viewport must have positive integer width and height")

        journey = case.get("journeyId")
        scenario = case.get("scenarioId")
        if _non_empty_string(journey) and _non_empty_string(split):
            group = _normalized_group(journey)
            if group:
                split_groups[("journey", group)].add(split)
        if _non_empty_string(scenario) and _non_empty_string(split):
            group = _normalized_group(scenario)
            if group:
                split_groups[("scenario", group)].add(split)

        labels = case.get("labels")
        if not isinstance(labels, list) or len(labels) != 2:
            errors.append(f"{prefix}.labels must contain exactly two independent labels")
        else:
            annotators: set[str] = set()
            for label_index, label in enumerate(labels):
                label_prefix = f"{prefix}.labels[{label_index}]"
                if not isinstance(label, dict):
                    errors.append(f"{label_prefix} must be an object")
                    continue
                annotator = label.get("annotatorId")
                if not _non_empty_string(annotator):
                    errors.append(f"{label_prefix}.annotatorId is required")
                elif annotator in annotators:
                    errors.append(f"{prefix}.labels must have two independent annotators")
                else:
                    annotators.add(annotator)
                if not _valid_label(label.get("defectPresent"), label.get("category")):
                    errors.append(f"{label_prefix} has an invalid classification")

        adjudication = case.get("adjudication")
        if not isinstance(adjudication, dict):
            errors.append(f"{prefix}.adjudication must be an object")
        else:
            status = adjudication.get("status")
            if not isinstance(status, str) or status not in {"resolved", "unresolved"}:
                errors.append(f"{prefix}.adjudication.status is invalid")
            adjudicator = adjudication.get("adjudicatorId")
            if not _non_empty_string(adjudicator):
                errors.append(f"{prefix}.adjudication.adjudicatorId is required")
            elif isinstance(labels, list) and any(
                isinstance(label, dict)
                and label.get("annotatorId") == adjudicator
                for label in labels
            ):
                errors.append(
                    f"{prefix}.adjudication.adjudicatorId must differ from annotators"
                )
            defect_present = adjudication.get("defectPresent")
            category = adjudication.get("category")
            impact = adjudication.get("impact")
            if status == "resolved":
                if not isinstance(defect_present, bool):
                    errors.append(f"{prefix}.adjudication.defectPresent must be boolean")
                elif not _valid_label(defect_present, category):
                    errors.append(f"{prefix}.adjudication has an invalid classification")
                if not isinstance(impact, str) or impact not in IMPACTS or (
                    defect_present is False and impact != "none"
                ) or (defect_present is True and impact == "none"):
                    errors.append(f"{prefix}.adjudication.impact is invalid")
            elif status == "unresolved" and (
                defect_present is not None
                or category is not None
                or not isinstance(impact, str)
                or impact not in IMPACTS
            ):
                errors.append(f"{prefix}.unresolved adjudication must not assert a class")

        prediction = case.get("modelPrediction")
        if not isinstance(prediction, dict) or not _valid_label(
            prediction.get("defectPresent"), prediction.get("category")
        ):
            errors.append(f"{prefix}.modelPrediction has an invalid classification")

    for (kind, group), splits in sorted(split_groups.items()):
        if len(splits) > 1:
            errors.append(f"near-duplicate {kind} group {group} crosses dataset splits")
    return errors


def unresolved_adjudication_cases(dataset: Any) -> list[str]:
    if not isinstance(dataset, dict) or not isinstance(dataset.get("cases"), list):
        return []
    unresolved = []
    for index, case in enumerate(dataset["cases"]):
        if not isinstance(case, dict):
            continue
        adjudication = case.get("adjudication")
        if not isinstance(adjudication, dict) or adjudication.get("status") != "resolved":
            case_id = case.get("caseId")
            unresolved.append(
                case_id if isinstance(case_id, str) else f"cases[{index}]"
            )
    return unresolved


def provenance_gaps(dataset: Any) -> list[str]:
    if not isinstance(dataset, dict):
        return ["dataset must be an object"]
    gaps = []
    if not _non_empty_string(dataset.get("datasetId")):
        gaps.append("datasetId is missing or empty")
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases:
        return gaps + ["cases are missing or empty"]
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            gaps.append(f"cases[{index}] is not an object")
            continue
        missing = [
            field
            for field in PROVENANCE_FIELDS
            if field not in case
            or (
                field != "viewport"
                and not _non_empty_string(case.get(field))
            )
        ]
        if missing:
            case_ref = case.get("caseId", f"cases[{index}]")
            gaps.extend(f"{case_ref}.{field} is missing or empty" for field in missing)
        adjudication = case.get("adjudication")
        if not isinstance(adjudication, dict) or not _non_empty_string(
            adjudication.get("adjudicatorId")
        ):
            gaps.append(
                f"{case.get('caseId', f'cases[{index}]')}.adjudication.adjudicatorId is missing or empty"
            )
        if not isinstance(case.get("caseId"), str) or not CASE_ID.fullmatch(
            case["caseId"]
        ):
            gaps.append(f"{case.get('caseId', f'cases[{index}]')}.caseId is invalid")
        if not isinstance(case.get("requirementId"), str) or not REQUIREMENT_ID.fullmatch(
            case["requirementId"]
        ):
            gaps.append(f"{case.get('caseId', f'cases[{index}]')}.requirementId is invalid")
        if not isinstance(case.get("testId"), str) or not TEST_ID.fullmatch(
            case["testId"]
        ):
            gaps.append(f"{case.get('caseId', f'cases[{index}]')}.testId is invalid")
        split = case.get("split")
        if not isinstance(split, str) or split not in SPLITS:
            gaps.append(f"{case.get('caseId', f'cases[{index}]')}.split is invalid")
        viewport = case.get("viewport")
        if (
            not isinstance(viewport, dict)
            or set(viewport) != {"width", "height"}
            or any(
                isinstance(viewport.get(dimension), bool)
                or not isinstance(viewport.get(dimension), int)
                or viewport[dimension] <= 0
                for dimension in ("width", "height")
            )
        ):
            gaps.append(f"{case.get('caseId', f'cases[{index}]')}.viewport is invalid")
    return gaps
