# Power Automate Delivery Standard

## Required design

- Define trigger, inputs, outputs, owner, connection identity, and downstream effects.
- Decide idempotency, concurrency, retries, timeouts, pagination, throttling, and duplicate prevention.
- Group work into try/catch/finally-style scopes with explicit run-after behavior.
- Define operational logging, correlation ID, alerting, recovery, and support.

## Build controls

- Use descriptive trigger, scope, action, variable, and compose names.
- Keep secrets out of definitions, logs, and notifications.
- Use environment variables and connection references for deployable assets.
- Minimize nested loops and repeated connector calls.
- Make destructive actions explicit and independently approved.
- Ensure failures cannot be reported as successful outcomes.

## Required validation

- Definition validation and preflight
- Happy path and validation failure
- Duplicate trigger and concurrent execution
- Connector authentication, timeout, throttling, and retry
- Partial failure and compensating/recovery behavior
- Approval approve/reject/reassign/expire paths
- Permission and service-account continuity
- Monitoring and support notification
- Visual verification of the flow designer and a representative run detail in the shared browser per `visual-verification.md`; a passing preflight is not acceptance

## Evidence

Flow version, connections by logical name, trigger sample, test IDs, run IDs, action results, retry behavior, failure notification, recovery result, reviewer, and approval.

