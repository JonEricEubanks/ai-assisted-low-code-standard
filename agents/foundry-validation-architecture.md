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

## Visual validation boundary

- Run vision review only against screenshots from an identified, approved non-production test run and an approved baseline.
- Keep deterministic assertions authoritative for functional, data, permission, accessibility, and release-gate outcomes. Vision findings are supplemental observations; they cannot pass a failed check, clear a defect, or authorize release.
- Limit observations to the visual criteria in `qa/qa-strategy.md`. A screenshot cannot establish semantic accessibility, correct data, or authorization.
- Return uncertain, conflicting, or out-of-scope observations as `review-needed` for an independent human reviewer. Do not silently omit them.
- Keep the vision path read-only. Computer-use exploration is a separate later capability and must not be enabled by visual review.
- Normalize each run into the QA evidence record. Record model/deployment and skill version, screenshot and baseline references, test context, reviewer, classification, and retention tag. Any additional visual-finding fields remain proposed until the deterministic evidence contract is approved.

## Evaluation gate

Use the synthetic, human-labeled protocol in `workstreams/qa/foundry-visual-evaluation.md` before considering a pilot. Do not claim evaluation results or mark Foundry backlog tasks complete until the evidence contract is stable, the required control approvals are recorded, and an approved evaluation set has been reviewed. A future pilot also requires threat review and the security boundary above.
