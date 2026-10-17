# Evidence Schema

Every validation artifact must be traceable through these fields. The machine-readable contract is [`evidence-schema.json`](evidence-schema.json); the standard-library validator checks evidence IDs, requirement IDs, test IDs, timestamps, result states, required fields, and failure-to-defect linkage.

| Field | Required | Description |
|---|---|---|
| evidenceId | Yes | Stable ID such as `EVD-PA-014` |
| runId | Yes | Validation execution ID |
| project | Yes | Pilot or solution |
| environment | Yes | Non-production/production environment name |
| solutionVersion | Yes | Exact app/flow/solution version |
| requirementId | Yes | Requirement being demonstrated |
| testId | Yes | Test case |
| executor | Yes | Person, script, skill, or agent |
| modelSkillVersion | If AI used | Model/deployment and skill version |
| persona | If applicable | Test identity/role |
| timestamp | Yes | ISO 8601 date-time with UTC or explicit offset |
| result | Yes | `pass`, `fail`, `blocked`, or `review-needed` |
| expected | Yes | Expected result |
| actual | Yes | Observed result |
| artifacts | Yes | One or more typed references with the claim each artifact supports |
| defectId | If failed | Linked defect |
| reviewer | Yes | Named independent reviewer |
| approval | For release | Named approver and `approved`, `rejected`, or `deferred` decision |
| classification | Yes | Evidence sensitivity, using the approved project taxonomy |
| retentionTag | Yes | Approved retention category |

Evidence IDs use `EVD-<scope>-NNN`, run IDs use `RUN-<scope>-NNN`, requirement IDs use `REQ-NNN` or `REQ-<scope>-NNN`, test IDs use `TST-<scope>-NNN`, and defect IDs use `DEF-<scope>-NNN`. A failed record must include a defect ID. `blocked` and `review-needed` are not passes and must remain visible in the release report.

Run the sanitized example and release-gate fixture from the repository root:

```sh
python qa/deterministic_qa.py
python -m unittest discover -s qa -p 'test_*.py' -v
```

For a project run, pass approved evidence and gate-input JSON with `--evidence` and `--gate`. Do not place client-sensitive data in repository fixtures or use these fixtures as a substitute for the approved evidence location, classification, access, or retention controls.

## Filename convention

`YYYY-MM-DD_phase_platform_subject_state.ext`

Store unedited internal evidence in the approved repository. Publish only recreated or sanitized evidence approved for external use. Follow the capture, public-safety, and existing-media rules in [`screenshot-plan.md`](screenshot-plan.md).
