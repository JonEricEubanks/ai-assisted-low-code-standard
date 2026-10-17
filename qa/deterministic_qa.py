from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EVIDENCE_FIXTURE = ROOT / "fixtures" / "deterministic-evidence.json"
GATE_FIXTURE = ROOT / "fixtures" / "release-gate-input.json"
RESULTS = {"pass", "fail", "blocked", "review-needed"}
EVIDENCE_ID = re.compile(r"^EVD-[A-Z0-9]+-[0-9]{3}$")
RUN_ID = re.compile(r"^RUN-[A-Z0-9]+-[0-9]{3}$")
REQUIREMENT_ID = re.compile(r"^REQ-([A-Z0-9]+-)?[0-9]{3}$")
TEST_ID = re.compile(r"^TST-[A-Z0-9]+-[0-9]{3}$")
DEFECT_ID = re.compile(r"^DEF-[A-Z0-9]+-[0-9]{3}$")
RELEASE_SENSITIVE_CATEGORIES = {"destructive", "security", "records-sensitive"}


def validate_evidence_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]

    errors: list[str] = []
    required = {
        "evidenceId",
        "runId",
        "project",
        "environment",
        "solutionVersion",
        "requirementId",
        "testId",
        "executor",
        "timestamp",
        "result",
        "expected",
        "actual",
        "artifacts",
        "reviewer",
        "classification",
        "retentionTag",
    }
    for field in sorted(required - record.keys()):
        errors.append(f"{field} is required")

    for field, pattern in (
        ("evidenceId", EVIDENCE_ID),
        ("runId", RUN_ID),
        ("requirementId", REQUIREMENT_ID),
        ("testId", TEST_ID),
    ):
        value = record.get(field)
        if value is not None and (
            not isinstance(value, str) or not pattern.fullmatch(value)
        ):
            errors.append(f"{field} has an invalid identifier")

    result = record.get("result")
    if result is not None and result not in RESULTS:
        errors.append("result must be pass, fail, blocked, or review-needed")

    defect_id = record.get("defectId")
    if defect_id is not None and (
        not isinstance(defect_id, str) or not DEFECT_ID.fullmatch(defect_id)
    ):
        errors.append("defectId has an invalid identifier")
    if result == "fail" and not defect_id:
        errors.append("defectId is required when result is fail")

    timestamp = record.get("timestamp")
    if timestamp is not None:
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except (AttributeError, TypeError, ValueError):
            errors.append("timestamp must be an ISO 8601 date-time")

    artifacts = record.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty array")
    else:
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"artifacts[{index}] must be an object")
                continue
            for field in ("type", "reference", "claim"):
                if not isinstance(artifact.get(field), str) or not artifact[field]:
                    errors.append(f"artifacts[{index}].{field} is required")
            if artifact.get("type") not in {
                "log",
                "screenshot",
                "video",
                "trace",
                "export",
            }:
                errors.append(f"artifacts[{index}].type is invalid")

    for field in (
        "project",
        "environment",
        "solutionVersion",
        "executor",
        "expected",
        "actual",
        "reviewer",
        "classification",
        "retentionTag",
    ):
        if field in record and (
            not isinstance(record[field], str) or not record[field].strip()
        ):
            errors.append(f"{field} must be a non-empty string")

    return errors


def evaluate_release_gate(inputs: Any) -> dict[str, Any]:
    if not isinstance(inputs, dict):
        raise ValueError("release gate input must be an object")

    critical_tests = inputs.get("criticalTests", [])
    sensitive_tests = inputs.get("releaseSensitiveTests", [])
    open_findings = inputs.get("openFindings", [])
    if not isinstance(critical_tests, list) or not isinstance(sensitive_tests, list):
        raise ValueError("criticalTests and releaseSensitiveTests must be arrays")
    if not isinstance(open_findings, list):
        raise ValueError("openFindings must be an array")

    critical_pass_rate = (
        sum(test.get("result") == "pass" for test in critical_tests)
        / len(critical_tests)
        if critical_tests
        else 0.0
    )
    critical_pass = bool(critical_tests) and critical_pass_rate >= 0.95
    sensitive_coverage = bool(sensitive_tests) and all(
        test.get("executed") is True for test in sensitive_tests
    )
    no_critical_findings = not any(
        finding.get("status") == "open"
        and finding.get("severity") in {"Sev 1", "Sev 2"}
        for finding in open_findings
    )
    approval = inputs.get("humanApproval", {})
    human_approval_recorded = (
        isinstance(approval, dict)
        and isinstance(approval.get("approver"), str)
        and bool(approval["approver"].strip())
        and approval.get("decision") == "approved"
    )
    criteria = {
        "noOpenSev1OrSev2": no_critical_findings,
        "criticalRegressionAtLeast95Percent": critical_pass,
        "criticalRegressionPassRate": critical_pass_rate,
        "releaseSensitivePathsExecuted": sensitive_coverage,
        "failedAndBlockedTestsDispositioned": (
            inputs.get("allFailedAndBlockedDispositioned") is True
        ),
        "rollbackEvidenceComplete": inputs.get("rollbackEvidence") is True,
        "supportEvidenceComplete": inputs.get("supportEvidence") is True,
        "namedHumanApprovalRecorded": human_approval_recorded,
    }

    residual_risks = []
    for test in critical_tests:
        if test.get("result") != "pass":
            residual_risks.append(
                {
                    "testId": test.get("testId"),
                    "result": test.get("result", "missing"),
                    "description": "Critical regression did not pass.",
                }
            )
    for test in sensitive_tests:
        if test.get("executed") is not True or test.get("result") != "pass":
            residual_risks.append(
                {
                    "testId": test.get("testId"),
                    "result": test.get("result", "not-executed"),
                    "description": "Release-sensitive path is incomplete or did not pass.",
                }
            )
    for finding in open_findings:
        if finding.get("status") == "open":
            residual_risks.append(
                {
                    "findingId": finding.get("findingId"),
                    "severity": finding.get("severity"),
                    "description": finding.get("description", "Open finding."),
                }
            )
    if inputs.get("allFailedAndBlockedDispositioned") is not True:
        residual_risks.append(
            {"description": "Failed or blocked tests lack explicit disposition."}
        )
    if inputs.get("rollbackEvidence") is not True:
        residual_risks.append({"description": "Rollback evidence is incomplete."})
    if inputs.get("supportEvidence") is not True:
        residual_risks.append({"description": "Support evidence is incomplete."})
    if not human_approval_recorded:
        residual_risks.append(
            {"description": "Named human release approval is missing or not approved."}
        )
    if not sensitive_tests:
        residual_risks.append(
            {
                "description": (
                    "No destructive, security, or records-sensitive paths were declared."
                )
            }
        )
    if not critical_tests:
        residual_risks.append(
            {"description": "No critical regression tests were declared."}
        )

    ready = all(
        value
        for key, value in criteria.items()
        if key != "criticalRegressionPassRate"
    )
    return {
        "recommendation": "release-ready" if ready else "not-ready",
        "humanReleaseAuthority": "Human reviewers remain the release authority.",
        "criteria": criteria,
        "residualRisks": residual_risks,
    }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate evidence and calculate the deterministic release gate."
    )
    parser.add_argument("--evidence", type=Path, default=EVIDENCE_FIXTURE)
    parser.add_argument("--gate", type=Path, default=GATE_FIXTURE)
    args = parser.parse_args()

    try:
        evidence = _read_json(args.evidence)
        gate_inputs = _read_json(args.gate)
    except (OSError, json.JSONDecodeError) as error:
        print(f"VALIDATION FAILED: {error}", file=sys.stderr)
        return 1

    records = evidence.get("records") if isinstance(evidence, dict) else None
    if not isinstance(records, list) or not records:
        print("VALIDATION FAILED: records must be a non-empty array", file=sys.stderr)
        return 1

    errors = [
        f"records[{index}]: {error}"
        for index, record in enumerate(records)
        for error in validate_evidence_record(record)
    ]
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    try:
        release_gate = evaluate_release_gate(gate_inputs)
    except ValueError as error:
        print(f"VALIDATION FAILED: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "evidenceRecordsValidated": len(records),
                "releaseGate": release_gate,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
