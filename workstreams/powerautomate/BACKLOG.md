# Power Automate Workstream Backlog

## Branch

`feature/powerautomate-standard`

## Delivery procedure

Complete these checks for each bounded cloud-flow change before implementation:

- Record the flow/environment, business outcome, trigger and trigger conditions, input/output contract, accountable owner, connection identities, dependencies, downstream effects, and approver. Mark unknowns for discovery; do not infer them.
- Define a stable idempotency key and duplicate handling. Set an appropriate concurrency limit and explain its effect on ordering and throughput. Identify pagination, throttling, timeout, and retry limits.
- Group related actions into named `Try`, `Catch`, and `Finally` scopes. Configure `Catch` to run after the relevant `Try` failure, timeout, or skip statuses. Configure `Finally` to run after success and failure statuses as applicable. Preserve the original failure status and details; logging or notification in `Catch` must never turn a failed business operation into a successful outcome.
- Define actionable alerts, correlation ID propagation, support owner, safe replay criteria, compensating actions, rollback, and a recovery decision-maker. Never retry a non-idempotent action until its prior outcome is known.
- Keep credentials, tokens, personal/client data, and sensitive payloads out of flow definitions, test fixtures, logs, and notifications. Use synthetic test data and approved connection references/environment variables.
- Require named approval before destructive actions, production mutation, or publishing. Stop when target environment, owner, permissions, backup, or approval is unclear.

## Failure handling

For each failure mode, document the affected action and repetition, detection signal, impact, retryability, owner, response, and evidence to retain.

| Failure mode | Required handling |
| --- | --- |
| Invalid input or definition | Reject before side effects; return a clear failure and safe diagnostic reference. Correct the input/definition and rerun validation. |
| Authentication, permission, or connection failure | Stop dependent work; do not retry indefinitely or switch identities silently. Notify the connection owner, restore approved access, then validate and replay only after checking for prior side effects. |
| Throttling, transient connector error, or timeout | Apply bounded exponential retry only for safe/idempotent operations. After exhaustion, record the correlation/run ID and action; check the remote outcome before replaying a timed-out write. |
| Duplicate trigger or concurrent run | Use the idempotency key and concurrency policy to prevent duplicate effects. Quarantine or reconcile ambiguous runs; do not assume that a second run is harmless. |
| Partial completion or downstream failure | Stop unsafe downstream actions, retain completed-action evidence, and run the documented compensation or manual recovery. Mark the business operation failed/partial until reconciled. |
| Catch, notification, or logging failure | Preserve the original failure and raise a separate observability/support alert where possible. Do not claim success because error reporting failed or succeeded. |
| Approval rejected, reassigned, or expired | Do not perform the gated action. Record the terminal approval outcome and route to the named owner for resubmission or closure. |

Do not place secrets or full sensitive payloads in error messages. Include only a concise failure category, safe diagnostic context, correlation/run ID, owner, and next action.

## Recovery procedure

1. Pause or disable further triggering only when authorized and when doing so is safer than continued processing. Notify the owner/support contact and record the time and reason.
2. Preserve the failed run and action/repetition details, correlation ID, timestamps, flow version, environment, and sanitized connector response. Identify completed and uncertain side effects before retrying.
3. Classify the fault as configuration/definition, identity/permission, transient service, invalid input, duplicate/concurrency, or partial side effect. Assign an owner and decide whether to correct, retry, compensate, reconcile manually, or roll back.
4. Obtain required approval for changes, destructive compensation, replay, or rollback. Verify idempotency and remote state before replaying any write whose outcome is uncertain.
5. Validate the fix in a non-production environment with synthetic data, then run the relevant recovery and regression tests. Resume or republish only after the named approver authorizes it.
6. Confirm downstream state, alert/support outcome, and that queued or in-flight events are accounted for. Record the recovery result, remaining risk, reviewer, and follow-up action; update the runbook if the procedure changed.

If safe replay or compensation cannot be established, leave the flow paused when authorized, escalate to the accountable owner, and document the unresolved state rather than guessing.

## Validation checklist

Record a test ID, environment, flow version, synthetic input, expected/actual result, run ID, action results, status, executor, reviewer, and evidence for each applicable case. Do not use production data for test fixtures.

| Case | Acceptance evidence |
| --- | --- |
| Definition and preflight | Definition is valid; required connections, references, variables, permissions, and trigger configuration resolve in the target environment. |
| Happy path and invalid input | Valid input produces the specified outcome; invalid input is rejected before side effects and is not reported as success. |
| Duplicate trigger and concurrency | Repeated and overlapping events do not create duplicate effects or violate ordering/limits. |
| Authentication, permission, timeout, throttling, and retry | Each failure is detected; retries are bounded and safe; exhausted or ambiguous writes remain failed pending reconciliation. |
| Partial failure and recovery | Completed effects are identified; compensation/reconciliation is approved and verified; final status does not conceal the failure. |
| Approval | Approve, reject, reassign, and expire paths enforce the gate and produce the expected notification and terminal state. |
| Monitoring and support | Correlation ID reaches logs/alerts; the right owner receives a useful, sanitized notification; notification failure does not mask the flow failure. |
| Service continuity and permissions | Required connection identity, least-privilege access, owner continuity, and successor support access are verified. |

Do not publish when a required test fails, a critical result is ambiguous, or an unresolved defect could cause unauthorized or duplicate effects. Document exclusions and obtain approval for accepted residual risk.

## Flow MCP procedure

Use only an approved Flow MCP server and tools available in the current environment; do not assume a tool name or capability that is not exposed. Confirm the MCP identity, tenant/environment, target flow, access level, and whether each operation is read-only or mutating before invoking it. If these cannot be verified, stop and use the documented manual process.

1. **Inspect (read-only):** retrieve flow metadata/version, trigger and connections by logical name, dependencies, recent failure summaries, and available run details. Limit inspection to the approved target and avoid exporting sensitive payloads.
2. **Plan and preview:** prepare a bounded change plan and inspect the MCP preview/diff. Confirm every affected action, connection reference, environment variable, permission, and downstream effect. Request review before mutation.
3. **Back up:** create or verify a restorable backup/export of the current flow before updates. Store it only in the approved location with appropriate access; do not include client-sensitive data or secrets in the workstream evidence.
4. **Validate and preflight:** run available definition validation and deployment preflight without publishing. Resolve validation errors and verify target environment, dependencies, connections, permissions, and rollback readiness.
5. **Smoke test:** execute only in an approved non-production environment with synthetic data. Capture run IDs and sanitized action outcomes; run the applicable failure, duplicate, concurrency, approval, and recovery cases from the validation checklist.
6. **Publish (mutating):** publish only after explicit named approval for the exact flow/version/environment. Reconfirm the preview, backup, preflight, and target immediately before the operation. Never use MCP to bypass approval or environment controls.
7. **Verify and hand off:** read back the published version and status, run an approved post-publish smoke check, confirm monitoring/support ownership, and record release and rollback evidence. If an operation returns an ambiguous result, inspect state before repeating it.

If MCP access is unavailable, insufficiently scoped, or returns an unexpected result, do not improvise a mutation. Record the limitation and use an approved manual procedure with the same preview, backup, validation, approval, and evidence gates.

## Evidence and definition of done

Retain the flow/environment and version, connection logical names, trigger/input contract, test IDs and synthetic-data note, run IDs and sanitized action results, retry/failure/recovery evidence, approval and reviewer, backup/rollback reference, support owner, and known limitations. Exclude secrets and client-sensitive values.

The work is done when another developer can use the standard and this procedure to safely design, validate, diagnose, recover, publish with approval, and hand off one bounded cloud-flow change. Record unresolved discovery items (including unknown flow inventory, connector behavior, licensing, and environment-specific MCP capabilities) with an owner and resolution path instead of assuming answers.
