# Live-platform handoff

This pack is a synthetic, offline reference only. It contains no executed cloud-flow result, live definition, tenant action, or production evidence. A future platform agent must not treat expected results as observed results.

## Mapping and evidence collection

1. Obtain the approved flow, environment, version, owner, connection references, trigger/input contract, downstream effects, and approval boundaries. Resolve the platform-specific questions below with the accountable owner before testing.
2. Map each applicable `TST-FLOW-NNN` case to the approved flow's trigger and actions. Record the intended action/state correspondence and any non-applicable case; do not infer an unobserved behavior from this pack.
3. Use only an approved non-production environment and synthetic data. Confirm authorization, backup/rollback readiness, identity, and connector configuration before executing any case. Do not use this reference pack as a deployment artifact or contact a tenant based on its example values.
4. For each authorized run, retain the native run history and action/repetition results, flow/version and environment, timestamps, synthetic input reference, correlation and idempotency references, retry outcomes, final downstream/reconciled state, and recovery or compensation decision. Preserve sanitized source evidence in the approved evidence location.
5. Keep expected behavior and actual observed behavior as separate evidence fields. Record blocked, failed, ambiguous, and unexecuted results as such. A missing or ambiguous native result is not a pass.
6. Capture named human reviewer/approver, authorization for replay or compensation, outcome of the review, and remaining risks. Do not automatically replay an uncertain write or perform destructive compensation.

## Unresolved platform-specific questions

Resolve these in context; this document makes no assumptions:

- Which approved flow, environment, version, owner, and support owner are in scope?
- What trigger and input contract apply, and which downstream effects can commit independently?
- Which connectors/actions are used, and what are their actual authentication, timeout, throttling, retry, and response semantics?
- What native or external storage provides idempotency, and does its actual operation provide the atomicity needed for concurrent claims?
- What concurrency limits, ordering guarantees, and overlap behavior are configured and validated for the specific flow?
- How are uncertain write outcomes queried or reconciled before replay?
- Which actions are safe to retry, which require human-authorized replay, and which compensations are destructive or require separate approval?
- What `Try`/`Catch`/`Finally` scope structure and run-after statuses does the flow use, including notification and logging failures?
- Which service identity and connection references are approved; how are least privilege, owner continuity, successor access, and licensing verified?
- What approval connector and policy govern approve, reject, reassign, expiry, stale decisions, and resubmission?
- Which native run-history fields, correlation propagation, log sinks, redaction, access controls, and retention rules are available?
- What approved evidence repository, retention tag, reviewer, and release gate apply?

Record each answer with its accountable source and validation evidence. Until resolved, mark the relevant scenario blocked or not applicable only after explicit human review.
