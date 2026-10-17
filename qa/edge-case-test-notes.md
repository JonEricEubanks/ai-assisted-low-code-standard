# Offline Edge-Case Test Notes

These regressions use only synthetic repository fixtures and the Python standard
library. They do not access a tenant or establish live-app QA, security
assurance, release approval, or pilot completion.

## Contract coverage

`test_evidence_edge_cases.py` adds checks for required and unexpected evidence
fields; malformed run and defect identifiers; ISO timestamps with explicit
offsets and malformed/naive timestamps; artifact type, claim, reference, and
unexpected fields; invalid field types; and failed-record defect linkage.

The release-gate cases cover malformed input shapes and values, duplicate test
IDs, empty critical suites, blocked and review-needed critical outcomes, the
exact 95% threshold and nearest discrete rate below it, unreviewed
release-sensitive applicability, missing rollback or support evidence, and
missing, rejected, or deferred human approval. Assertions check criteria,
recommendations, and residual-risk details.

## Confirmed duplicate-ID defect

The duplicate critical-test-ID regression expects malformed release input with
the same `testId` twice to raise `ValueError` with a duplicate-ID message.
`evaluate_release_gate` currently accepts two identical passing entries,
calculates a 100% critical regression pass rate, and recommends
`release-ready`. The release gate does not check uniqueness before calculating
its criteria. The regression is intentionally retained without a skip or
expected-failure marker; the input validation defect remains a bounded follow-up
for the release-gate implementation.

No production validator, schema, fixture, existing test, or other repository
file was changed.
