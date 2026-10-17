# Power Automate Workstream Backlog

## Branch

`feature/powerautomate-standard`

## Initial tasks

- [ ] Define trigger, input, output, identity, and downstream-effect specification.
- [ ] Create standard try/catch/finally scope and run-after patterns.
- [ ] Define idempotency, duplicate prevention, concurrency, retry, timeout, and pagination guidance.
- [ ] Define correlation, telemetry, alert, support, and recovery evidence.
- [ ] Create failure-path and approval-path test templates.
- [ ] Build a Flow MCP preview, backup, validation, preflight, smoke-test, and publish checklist.
- [ ] Define Early Check discovery questions for the unknown flow inventory and connector behavior.

## Validation

- Failure cannot produce a success-shaped result.
- Destructive actions require explicit approval.
- Tests cover duplicates, concurrency, connector failure, partial failure, and recovery.

## Definition of done

Another developer can safely design, validate, diagnose, and hand off one bounded cloud-flow change.
