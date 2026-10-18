from __future__ import annotations

from typing import Any

from .dataset import (
    CATEGORIES,
    provenance_gaps,
    unresolved_adjudication_cases,
    validate_dataset,
)


def _ratios(counts: dict[str, int]) -> dict[str, float | None]:
    true_positive = counts["truePositive"]
    false_positive = counts["falsePositive"]
    true_negative = counts["trueNegative"]
    false_negative = counts["falseNegative"]

    def ratio(numerator: int, denominator: int) -> float | None:
        return numerator / denominator if denominator else None

    return {
        "precision": ratio(true_positive, true_positive + false_positive),
        "recall": ratio(true_positive, true_positive + false_negative),
        "falsePositiveRate": ratio(false_positive, false_positive + true_negative),
        "falseNegativeRate": ratio(false_negative, false_negative + true_positive),
    }


def _empty_counts() -> dict[str, int]:
    return {
        "truePositive": 0,
        "falsePositive": 0,
        "trueNegative": 0,
        "falseNegative": 0,
    }


def _count_case(
    counts: dict[str, int], actual: bool, predicted: bool
) -> None:
    if actual and predicted:
        counts["truePositive"] += 1
    elif not actual and predicted:
        counts["falsePositive"] += 1
    elif not actual and not predicted:
        counts["trueNegative"] += 1
    else:
        counts["falseNegative"] += 1


def evaluate_dataset(dataset: Any) -> dict[str, Any]:
    validation_errors = validate_dataset(dataset)
    gaps = provenance_gaps(dataset)
    unresolved = unresolved_adjudication_cases(dataset)
    cases = dataset.get("cases", []) if isinstance(dataset, dict) else []
    if not isinstance(cases, list):
        cases = []

    overall = _empty_counts()
    categories = {category: _empty_counts() for category in sorted(CATEGORIES)}
    evaluated_case_count = 0
    uncertain_count = 0
    prediction_count = 0
    high_impact_false_negatives: list[str] = []

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            continue
        adjudication = case.get("adjudication")
        prediction = case.get("modelPrediction")
        if not isinstance(prediction, dict):
            continue
        predicted = prediction.get("defectPresent")
        if (
            predicted is True
            or predicted is False
            or isinstance(predicted, str) and predicted == "uncertain"
        ):
            prediction_count += 1
        if predicted == "uncertain":
            uncertain_count += 1
        if (
            not isinstance(adjudication, dict)
            or adjudication.get("status") != "resolved"
            or not isinstance(adjudication.get("defectPresent"), bool)
            or not (
                predicted is True
                or predicted is False
                or isinstance(predicted, str) and predicted == "uncertain"
            )
        ):
            continue

        actual = adjudication["defectPresent"]
        actual_category = adjudication.get("category")
        predicted_category = prediction.get("category")
        if predicted in (True, False):
            evaluated_case_count += 1
            _count_case(overall, actual, predicted)
            for category, counts in categories.items():
                _count_case(
                    counts,
                    actual and actual_category == category,
                    predicted and predicted_category == category,
                )
        if actual and adjudication.get("impact") == "high" and predicted is False:
            case_id = case.get("caseId")
            high_impact_false_negatives.append(
                case_id if isinstance(case_id, str) else f"cases[{index}]"
            )

    case_count = len(cases)
    blockers = []
    if validation_errors:
        blockers.append("dataset validation failed")
    if gaps:
        blockers.append("provenance is incomplete")
    if unresolved:
        blockers.append("adjudication is unresolved")
    if high_impact_false_negatives:
        blockers.append("one or more high-impact defects were missed")

    return {
        "datasetId": dataset.get("datasetId") if isinstance(dataset, dict) else None,
        "caseCount": case_count,
        "evaluatedCaseCount": evaluated_case_count,
        "confusionCounts": overall,
        **_ratios(overall),
        "uncertainCount": uncertain_count,
        "uncertainRate": (
            uncertain_count / prediction_count if prediction_count else None
        ),
        "perCategory": {
            category: {
                "confusionCounts": counts,
                **_ratios(counts),
            }
            for category, counts in categories.items()
        },
        "highImpactFalseNegativeCaseIds": sorted(high_impact_false_negatives),
        "provenanceGaps": sorted(gaps),
        "unresolvedAdjudicationCaseIds": sorted(unresolved),
        "validationErrors": sorted(validation_errors),
        "disposition": "blocked" if blockers else "favorable",
        "dispositionBlockers": blockers,
    }
