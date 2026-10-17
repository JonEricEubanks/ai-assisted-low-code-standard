# QA and Validation Workstream Backlog

## Branches

- `feature/qa-validation`
- `feature/foundry-validation`

## Deterministic QA tasks

- [ ] Formalize the evidence record as a machine-readable schema.
- [ ] Create sanitized fixtures and validate evidence IDs, requirement IDs, test IDs, and result states.
- [ ] Define platform-specific deterministic check interfaces.
- [ ] Create the first vertical-slice requirement-to-test-to-evidence example.
- [ ] Add stable Playwright journey conventions and trace retention guidance.
- [ ] Define defect, enhancement, and missed-requirement classifications.
- [ ] Define release-gate calculation and residual-risk output.

## Foundry tasks

- [ ] Obtain approved project, model, identity, network, budget, logging, and data-boundary decisions.
- [ ] Create a human-labeled visual evaluation set.
- [ ] Measure visual false positives and false negatives.
- [ ] Define the computer-use allowlist, disposable environment, kill switch, and forbidden actions.
- [ ] Compare computer-use findings with deterministic and human results.
- [ ] Complete threat review before any pilot.

## Definition of done

QA emits reproducible evidence and an explicit recommendation while human reviewers remain the only release authority.
