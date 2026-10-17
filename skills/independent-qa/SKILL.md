---
name: independent-qa
description: Execute risk-based independent QA and produce release evidence for low-code solutions.
---

# Independent QA

## Procedure

1. Verify requirements, architecture, risk class, build version, environment, and test data.
2. Build requirement-to-test traceability using `templates/test-case.md`.
3. Run deterministic checks before visual or exploratory testing.
4. Test functional, validation, permission, accessibility, volume, integration, failure, recovery, regression, and rollback paths.
5. Use Playwright for stable browser journeys and screenshots.
6. Use vision review for layout and visual anomalies only; mark uncertain findings for human review.
7. Use computer use only in an allowlisted disposable non-production session.
8. Record defects separately from enhancements and missed requirements.
9. Produce a release recommendation with explicit residual risk.

## Release rule

Vision and computer use are never release authorities. Critical deterministic results and accountable human approval are mandatory.

