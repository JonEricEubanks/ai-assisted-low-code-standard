# QA/QC Strategy

## Validation lanes

### 1. Deterministic

Run deterministic checks first. Their authoritative checks include schema, configuration, solution dependencies, App Checker, accessibility output, flow validation/preflight, API assertions, permissions, test data, and expected state. Use the platform interfaces in [`deterministic-checks.md`](deterministic-checks.md); unresolved or subjective results are `review-needed`, never inferred passes.

### 2. Functional

Happy path, validation, empty state, representative volume, duplicate, concurrency, permissions, connector failure, retry, recovery, approval outcomes, and rollback.

### 3. Browser automation

Use Playwright for stable journeys, navigation, forms, SharePoint pages, screenshots, responsive checks, and regression. Do not force brittle automation where the platform lacks stable selectors.

### 4. Vision

Review alignment, clipping, overlap, missing labels, blank states, responsive rendering, and differences from an approved baseline. Every uncertain result is `review-needed`.

### 5. Exploratory computer use

Run only in an allowlisted disposable non-production session with synthetic data, bounded actions, trace retention, and a kill switch.

### 6. Human approval

Required for business acceptance, permissions, accessibility judgment, sensitive data, records, production release, and standard exceptions.

Visual and computer-use evaluation may begin only after deterministic results and traceability are recorded. Follow the synthetic-data, publication-approval, and existing-media restrictions in [`screenshot-plan.md`](screenshot-plan.md).

## Severity

| Severity | Meaning |
|---|---|
| Sev 1 | Safety, security, records, irreversible data loss, or complete critical-service failure |
| Sev 2 | Critical journey unavailable, unauthorized access, material incorrect outcome, or no viable recovery |
| Sev 3 | Noncritical functional, accessibility, supportability, or performance issue with workaround |
| Sev 4 | Cosmetic or minor usability issue |

## Release threshold

- No open Sev 1 or Sev 2
- At least 95% critical regression pass (passed critical tests divided by all declared critical tests; an empty suite fails)
- 100% of destructive, security, and records-sensitive paths executed
- Explicitly review and record applicability of destructive, security, and records-sensitive paths
- Failed/blocked tests explicitly dispositioned
- Rollback and support evidence complete
- Named human approval recorded as approved

The deterministic gate calculation emits `release-ready` or `not-ready`, each criterion, and residual risks. A ready recommendation is not release authority; only the named human approver decides release. See [`deterministic-checks.md`](deterministic-checks.md#release-gate-and-residual-risk) and [`deterministic_qa.py`](deterministic_qa.py).
