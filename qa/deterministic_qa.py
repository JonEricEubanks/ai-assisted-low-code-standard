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
SEVERITIES = {"Sev 1", "Sev 2", "Sev 3", "Sev 4"}
FINDING_STATUSES = {"open", "closed"}


def validate_evidence_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]

    errors: list[str] = []
    allowed = {
        "evidenceId",
        "runId",
        "project",
        "environment",
        "solutionVersion",
        "requirementId",
        "testId",
        "executor",
        "modelSkillVersion",
        "persona",
        "timestamp",
        "result",
        "expected",
        "actual",
        "artifacts",
        "defectId",
        "reviewer",
        "approval",
        "classification",
        "retentionTag",
    }
    for field in sorted(record.keys() - allowed):
        errors.append(f"{field} is not allowed")
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
    if result is not None and (
        not isinstance(result, str) or result not in RESULTS
    ):
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
            parsed_timestamp = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
            if parsed_timestamp.tzinfo is None:
                errors.append("timestamp must include a UTC or explicit offset")
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
            if artifact.keys() - {"type", "reference", "claim"}:
                errors.append(f"artifacts[{index}] has an unexpected field")
            if not isinstance(artifact.get("type"), str) or artifact.get("type") not in {
                "log",
                "screenshot",
                "video",
                "trace",
                "export",
            }:
                errors.append(f"artifacts[{index}].type is invalid")

    for field in ("modelSkillVersion", "persona"):
        if field in record and (
            not isinstance(record[field], str) or not record[field].strip()
        ):
            errors.append(f"{field} must be a non-empty string")
    if "approval" in record:
        approval = record["approval"]
        if (
            not isinstance(approval, dict)
            or set(approval) != {"approver", "decision"}
            or not isinstance(approval.get("approver"), str)
            or not approval["approver"].strip()
            or not isinstance(approval.get("decision"), str)
            or approval.get("decision") not in {"approved", "rejected", "deferred"}
        ):
            errors.append("approval must include a named approver and valid decision")

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
    for index, test in enumerate(critical_tests):
        if (
            not isinstance(test, dict)
            or not isinstance(test.get("testId"), str)
            or not TEST_ID.fullmatch(test["testId"])
            or not isinstance(test.get("result"), str)
            or test["result"] not in RESULTS
        ):
            raise ValueError(f"criticalTests[{index}] has an invalid test ID or result")
    for index, test in enumerate(sensitive_tests):
        if (
            not isinstance(test, dict)
            or not isinstance(test.get("testId"), str)
            or not TEST_ID.fullmatch(test["testId"])
            or not isinstance(test.get("category"), str)
            or test["category"] not in RELEASE_SENSITIVE_CATEGORIES
            or not isinstance(test.get("executed"), bool)
            or not isinstance(test.get("result"), str)
            or test["result"] not in RESULTS
        ):
            raise ValueError(
                f"releaseSensitiveTests[{index}] has an invalid ID, category, execution state, or result"
            )
    for index, finding in enumerate(open_findings):
        if (
            not isinstance(finding, dict)
            or not isinstance(finding.get("severity"), str)
            or finding["severity"] not in SEVERITIES
            or not isinstance(finding.get("status"), str)
            or finding["status"] not in FINDING_STATUSES
        ):
            raise ValueError(f"openFindings[{index}] has an invalid severity or status")
    if not isinstance(inputs.get("releaseSensitiveApplicabilityReviewed"), bool):
        raise ValueError("releaseSensitiveApplicabilityReviewed must be a boolean")
    if not isinstance(inputs.get("allFailedAndBlockedDispositioned"), bool):
        raise ValueError("allFailedAndBlockedDispositioned must be a boolean")
    if not isinstance(inputs.get("rollbackEvidence"), bool):
        raise ValueError("rollbackEvidence must be a boolean")
    if not isinstance(inputs.get("supportEvidence"), bool):
        raise ValueError("supportEvidence must be a boolean")

    critical_pass_rate = (
        sum(test.get("result") == "pass" for test in critical_tests)
        / len(critical_tests)
        if critical_tests
        else 0.0
    )
    critical_pass = bool(critical_tests) and critical_pass_rate >= 0.95
    applicability_reviewed = inputs["releaseSensitiveApplicabilityReviewed"]
    sensitive_coverage = applicability_reviewed and all(
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
        "releaseSensitiveApplicabilityReviewed": applicability_reviewed,
        "releaseSensitivePathsExecuted": sensitive_coverage,
        "failedAndBlockedTestsDispositioned": inputs["allFailedAndBlockedDispositioned"],
        "rollbackEvidenceComplete": inputs["rollbackEvidence"],
        "supportEvidenceComplete": inputs["supportEvidence"],
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
    if not inputs["allFailedAndBlockedDispositioned"]:
        residual_risks.append(
            {"description": "Failed or blocked tests lack explicit disposition."}
        )
    if not inputs["rollbackEvidence"]:
        residual_risks.append({"description": "Rollback evidence is incomplete."})
    if not inputs["supportEvidence"]:
        residual_risks.append({"description": "Support evidence is incomplete."})
    if not human_approval_recorded:
        residual_risks.append(
            {"description": "Named human release approval is missing or not approved."}
        )
    if not applicability_reviewed:
        residual_risks.append(
            {
                "description": "Applicability of release-sensitive paths was not reviewed."
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
