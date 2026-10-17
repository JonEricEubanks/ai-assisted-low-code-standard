# QA and Validation Workstream Backlog

## Branches

- `feature/qa-validation`
- `feature/foundry-validation`

## Deterministic QA tasks

- [x] Formalize the evidence record as a machine-readable schema.
- [x] Create sanitized fixtures and validate evidence IDs, requirement IDs, test IDs, and result states.
- [x] Define platform-specific deterministic check interfaces.
- [x] Create the first vertical-slice requirement-to-test-to-evidence example.
- [x] Add stable Playwright journey conventions and trace retention guidance.
- [x] Define defect, enhancement, and missed-requirement classifications.
- [x] Define release-gate calculation and residual-risk output.

Deterministic QA is complete before visual or computer-use evaluation. The executable evidence and gate fixtures, check interfaces, traceability example, classification, and gate contract are in `qa/`; the screenshot policy remains governed by `qa/screenshot-plan.md`.

## Foundry tasks

- [ ] Obtain approved project, model, identity, network, budget, logging, and data-boundary decisions.
- [ ] Create a human-labeled visual evaluation set.
- [ ] Measure visual false positives and false negatives.
- [ ] Define the computer-use allowlist, disposable environment, kill switch, and forbidden actions.
- [ ] Compare computer-use findings with deterministic and human results.
- [ ] Complete threat review before any pilot.

## Definition of done

QA emits reproducible evidence and an explicit recommendation while human reviewers remain the only release authority.
