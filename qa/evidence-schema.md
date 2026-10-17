# Evidence Schema

Every validation artifact must be traceable through these fields.

| Field | Required | Description |
|---|---|---|
| evidenceId | Yes | Stable ID such as EVD-PA-014 |
| runId | Yes | Validation execution ID |
| project | Yes | Pilot or solution |
| environment | Yes | Non-production/production environment name |
| solutionVersion | Yes | Exact app/flow/solution version |
| requirementId | Yes | Requirement being demonstrated |
| testId | Yes | Test case |
| executor | Yes | Person, script, skill, or agent |
| modelSkillVersion | If AI used | Model/deployment and skill version |
| persona | If applicable | Test identity/role |
| timestamp | Yes | ISO 8601 timestamp |
| result | Yes | pass, fail, blocked, or review-needed |
| expected | Yes | Expected result |
| actual | Yes | Observed result |
| artifacts | Yes | Logs, screenshots, video, traces, or exported output |
| defectId | If failed | Linked defect |
| reviewer | Yes | Named independent reviewer |
| approval | For release | Named approver and decision |
| classification | Yes | Evidence sensitivity |
| retentionTag | Yes | Approved retention category |

## Filename convention

`YYYY-MM-DD_phase_platform_subject_state.ext`

Store unedited internal evidence in the approved repository. Publish only recreated or sanitized evidence approved for external use.

