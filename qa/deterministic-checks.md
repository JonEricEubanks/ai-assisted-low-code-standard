# Deterministic Check Interfaces

Deterministic checks are repeatable, machine-verifiable results. They run before visual review or exploratory computer use. A check that depends on subjective judgment must return `review-needed`, not a guessed pass.

## Common request and result

Each adapter receives the project, environment, exact solution version, run ID, requirement IDs, test ID, executor, approved test-data reference, and the platform-specific check configuration. It returns one result per check with:

| Field | Contract |
|---|---|
| checkId | Stable check identifier within the run |
| platform | `power-apps`, `power-automate`, `sharepoint`, or `integrated` |
| requirementId / testId | The requirement and test that this result evaluates |
| result | `pass`, `fail`, `blocked`, or `review-needed` |
| expected / actual | Assertion and observed output |
| startedAt / completedAt | ISO 8601 timestamps with offset |
| executor | Tool or accountable person |
| artifacts | Typed references and the claim each supports |
| defectId | Required for a failed result |

Each result becomes an evidence record conforming to [`evidence-schema.json`](evidence-schema.json). Preserve the source tool's raw output as an artifact; adapters may normalize fields, but must not turn missing, ambiguous, or inaccessible output into a pass.

## Platform interfaces

| Platform | Deterministic check inputs | Minimum check families |
|---|---|---|
| Power Apps | App/solution version, exported App Checker and accessibility outputs, formula assertions, persona, data-volume fixture | App Checker/formula errors; explicitly testable accessibility rules; delegation and representative-volume assertions; persona/permission checks; submit/update/delete/duplicate state; connector failure and recovery |
| Power Automate | Flow definition/version, preflight configuration, synthetic trigger/run inputs, logical connection references | Definition validation/preflight; trigger and input validation; duplicate/concurrency behavior; connector authentication, timeout, throttling and retry; partial failure/recovery; approval outcomes; service identity and support notification |
| SharePoint | List/library/page schema export, internal names, test persona, synthetic volume and permission fixtures | Schema/internal-name and required-field assertions; index/volume behavior; permission/inheritance results; retention/versioning configuration; list/library/page integration; search/navigation; backup/recovery/rollback checks |
| Integrated | Versioned dependency/configuration inventory, API contract, synthetic request/response, correlation ID | Dependency/configuration consistency; API assertions; cross-component state and permissions; failure propagation, retry/idempotency, recovery, and audit correlation |

An adapter records the platform tool and version, configuration/input reference, and raw-output reference. A human evaluates accessibility judgment, business acceptance, and any result marked `review-needed`; no adapter makes a release decision.

## Traceability vertical slice

The sanitized example in [`fixtures/deterministic-evidence.json`](fixtures/deterministic-evidence.json) demonstrates `REQ-008` → `TST-QA-001` → `EVD-QA-001`. The test runs the evidence-contract validator against a synthetic record and expects a valid result with all three stable IDs present. The evidence record links the validator's synthetic log reference and states the claim it proves. A failing assertion must instead produce `fail`, a linked defect ID, and the observed result; a blocked check stays blocked.

## Playwright journeys and traces

Use Playwright only for stable browser journeys, not as a substitute for platform-native deterministic checks.

- Pin the app/browser version, viewport, locale, timezone, and synthetic fixture for a journey.
- Prefer accessible role/name and label locators; use stable test IDs only where user-facing semantics are insufficient. Avoid positional selectors, arbitrary sleeps, and environment-specific text.
- Give each journey a stable `TST-<scope>-NNN` ID, explicit preconditions, deterministic setup/cleanup, expected assertions, and trace/evidence references.
- Record browser and Playwright versions, run ID, environment, solution version, and result. Retain traces on failure and when needed to substantiate a pass; redact or recreate before publication under the screenshot policy.
- Store traces in the approved evidence location with approved access and retention. Do not attach credentials, cookies, tokens, client data, or unapproved internal URLs to a trace.
- A flaky or selector-unstable journey is `blocked` until stabilized; do not retry until it passes and report only the successful attempt.

## Finding classifications

Keep outcome type separate from severity:

| Classification | Meaning | Required handling |
|---|---|---|
| Defect | Implemented behavior fails an accepted requirement or control | Record severity, evidence, disposition, and whether found pre-release or escaped; link the failed test |
| Missed requirement | An accepted requirement has no implementation, test, or passing evidence | Restore requirement-to-test traceability and disposition before release |
| Enhancement | Improvement outside the accepted requirement or current scope | Track separately; do not count as a defect or silently change acceptance criteria |

Use the severity scale in [`qa-strategy.md`](qa-strategy.md). Do not close a defect by relabeling it an enhancement; changes to accepted requirements require an explicit decision and updated traceability.

## Release gate and residual risk

`python qa/deterministic_qa.py` validates the evidence fixture and reports the release recommendation. Gate inputs use the same shape as [`fixtures/release-gate-input.json`](fixtures/release-gate-input.json). The evaluator recommends `release-ready` only when all criteria pass:

1. No open Sev 1 or Sev 2 findings.
2. Critical regression pass rate is at least 95% (`pass` count divided by all declared critical tests; an empty suite fails).
3. Every declared destructive, security, or records-sensitive path is executed. The project must explicitly review applicability; missing applicability review blocks the gate. An empty inventory passes this criterion only when the project records that none apply.
4. All failed and blocked tests are explicitly dispositioned.
5. Rollback and support evidence are complete.
6. A named human approver has recorded an `approved` decision.

The output always names human reviewers as the release authority and lists failed/blocked critical tests, incomplete sensitive paths, open findings, missing evidence, and unapproved human decisions as residual risks. A passing recommendation is evidence for the accountable human's release decision, never a substitute for it.

## Pilot handoff

For each pilot, provide the signed deterministic regression, requirement-to-test-to-evidence trace, separately classified findings, and failure, recovery, rollback, permission, accessibility, representative-volume, and successor-run regression evidence called for by [`evidence-gap-backlog.md`](../workstreams/evidence-gap-backlog.md). This QA output supports, but does not replace, the pilot exit gate in [`READINESS.md`](../workstreams/pilots/READINESS.md), which also requires retained evidence, metrics, and a retrospective-driven standard update.
