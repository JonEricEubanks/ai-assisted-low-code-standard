# Synthetic failure and recovery scenario pack

This is a fully fictional, offline reference pack for Power Automate delivery (REQ-003, REQ-006, and REQ-008). The cases are specifications, not executed cloud-flow tests: the catalog marks every observation as `not_observed`, and no tenant or live endpoint was contacted. The inputs, identifiers, results, and evidence references are synthetic. Intended behavior is recorded separately from observed behavior; there are no observed platform results.

The machine-readable catalog is [`recovery-scenarios.json`](recovery-scenarios.json). Validate its internal consistency with:

```sh
python -m unittest discover -s workstreams/powerautomate -p 'test_*.py' -v
```

## Scenario coverage

| Test ID | Scenario |
| --- | --- |
| TST-FLOW-001 | Happy path |
| TST-FLOW-002 | Invalid or missing input |
| TST-FLOW-003 | Duplicate delivery |
| TST-FLOW-004 | Concurrent duplicate processing |
| TST-FLOW-005 | Authentication failure |
| TST-FLOW-006 | Timeout with uncertain downstream completion |
| TST-FLOW-007 | 429/throttling with bounded retry |
| TST-FLOW-008 | Exhausted retries |
| TST-FLOW-009 | Partial failure and explicit recovery |
| TST-FLOW-010–013 | Approval, rejection, reassignment, and expiry |
| TST-FLOW-014 | Service-identity continuity |
| TST-FLOW-015 | Notification failure |
| TST-FLOW-016 | Correlation-safe logging |

## Design notes and limits

- Group actions into `Try`, `Catch`, and `Finally` scopes. Configure explicit run-after behavior: `Catch` handles the relevant failure, timeout, and skipped statuses; `Finally` records required completion/observability details after applicable success and failure paths. Preserve the original business failure if Catch, logging, or notification also fails.
- Automatic retry means only a finite, configured retry of an operation known to be safe to repeat. Human-authorized replay is a separate recovery decision made after checking prior side effects and remote state. A compensating action is a separately reviewed business operation; it must not be destructive or run automatically without explicit authorization.
- Never blindly replay a write whose timeout leaves its downstream completion uncertain. Do not claim exactly-once delivery: actual duplicate prevention depends on the validated flow design and storage/concurrency primitives.
- A failed operation, rejected/expired approval, or failed notification cannot be represented as successful business completion. Observability failure must not overwrite the original outcome.
- Flow actions, run-after behavior, connector retry support and response semantics, idempotency storage, atomicity, and concurrency behavior all require environment-specific validation. This pack invents no connector guarantees and is not a deployable flow definition.
- Evidence listed in a scenario describes what a future live validation should collect. Native run history, action details, retry behavior, timestamps, and correlation values do not exist for this offline pack.

## Synthetic-source status and assumptions

All fixture values are fictional labels and test values. The examples assume a request can be correlated with a stable business/idempotency key and that an accountable owner can review uncertain outcomes. These are design prompts, not claims about a particular connector, tenant, flow configuration, licensing, connector SLA, storage primitive, or approval feature. Unknowns must be resolved by the platform owner before a live test or replay.

## Handoff

See [`handoff.md`](handoff.md) for mapping these cases to an approved flow, collecting native evidence, and unresolved platform-specific questions.
