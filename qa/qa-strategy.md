# QA/QC Strategy

## Validation lanes

### 1. Deterministic

Authoritative checks: schema, configuration, solution dependencies, App Checker, accessibility output, flow validation/preflight, API assertions, permissions, test data, and expected state.

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

## Severity

| Severity | Meaning |
|---|---|
| Sev 1 | Safety, security, records, irreversible data loss, or complete critical-service failure |
| Sev 2 | Critical journey unavailable, unauthorized access, material incorrect outcome, or no viable recovery |
| Sev 3 | Noncritical functional, accessibility, supportability, or performance issue with workaround |
| Sev 4 | Cosmetic or minor usability issue |

## Release threshold

- No open Sev 1 or Sev 2
- At least 95% critical regression pass
- 100% of destructive, security, and records-sensitive paths executed
- Failed/blocked tests explicitly dispositioned
- Rollback and support evidence complete
- Named human approval

