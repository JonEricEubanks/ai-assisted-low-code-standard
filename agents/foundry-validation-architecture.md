# Foundry Validation Architecture

## Modules

1. Planner/test-orchestrator: converts approved requirements into bounded test assignments.
2. Deterministic runner: executes API, schema, policy, solution, and supported UI assertions.
3. Playwright runner: handles stable SharePoint, Microsoft 365, and web journeys.
4. Vision reviewer: evaluates screenshots for layout, clipping, inconsistency, and apparent accessibility issues.
5. Computer-use explorer: performs allowlisted exploratory testing in a disposable non-production session.
6. Result normalizer: returns the evidence schema defined in `qa/evidence-schema.md`.
7. Human release reviewer: owns disposition and release recommendation.

## Security boundary

- Approved Foundry project and models only
- Synthetic or approved non-production data
- Managed identity or approved secret store
- Tool allowlist and least privilege
- Network and environment isolation
- Trace and artifact classification
- Consumption budget and kill switch
- No production mutation

## Implementation order

Build evidence schema and deterministic checks first, Playwright second, vision third, and bounded computer use last.

