from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


APPROVED_SCOPE = {
    "subscriptionId": "b8f90e47-b8ee-45f1-9442-d3b4f8fd0695",
    "resourceGroup": "rg-mgp-foundry-qa-dev",
    "region": "eastus2",
}
TEST_ID = re.compile(r"^TST-[A-Z0-9]+-[0-9]{3}$")
RESULTS = ("pass", "fail", "blocked", "review-needed")


def normalize_shadow_run(fixture: Any, scope: Any) -> dict[str, Any]:
    if not isinstance(scope, dict) or scope != APPROVED_SCOPE:
        raise ValueError("scope does not match the approved Foundry QA scope")
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")

    records = fixture.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("fixture records must be a non-empty array")

    evaluations = []
    seen_test_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"records[{index}] must be an object")
        test_id = record.get("testId")
        result = record.get("result")
        if not isinstance(test_id, str) or not TEST_ID.fullmatch(test_id):
            raise ValueError(f"records[{index}].testId is invalid")
        if test_id in seen_test_ids:
            raise ValueError(f"records[{index}].testId is duplicated")
        if not isinstance(result, str) or result not in RESULTS:
            raise ValueError(f"records[{index}].result is invalid")
        seen_test_ids.add(test_id)
        evaluations.append({"testId": test_id, "result": result})

    counts = {result: 0 for result in RESULTS}
    for evaluation in evaluations:
        counts[evaluation["result"]] += 1

    if counts["review-needed"] or counts["blocked"]:
        overall_result = "review-needed"
    elif counts["fail"]:
        overall_result = "fail"
    else:
        overall_result = "pass"

    return {
        "schemaVersion": 1,
        "mode": "shadow",
        "scope": APPROVED_SCOPE.copy(),
        "overallResult": overall_result,
        "resultCounts": counts,
        "evaluations": evaluations,
        "releaseAuthorization": "not-authorized",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize local Foundry QA shadow-evaluation fixture data."
    )
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--subscription-id", required=True)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    scope = {
        "subscriptionId": args.subscription_id,
        "resourceGroup": args.resource_group,
        "region": args.region,
    }
    try:
        if scope != APPROVED_SCOPE:
            raise ValueError("scope does not match the approved Foundry QA scope")
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        summary = normalize_shadow_run(fixture, scope)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"SHADOW EVALUATION FAILED: {error}", file=sys.stderr)
        return 1

    serialized = json.dumps(summary, indent=2)
    if args.output:
        args.output.write_text(f"{serialized}\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    sys.exit(main())
