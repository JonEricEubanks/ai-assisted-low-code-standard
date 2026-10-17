---
name: independent-qa
description: Execute risk-based independent QA and produce release evidence for low-code solutions.
---

# Independent QA

## Procedure

1. Verify requirements, architecture, risk class, build version, environment, and approved test-data boundary.
2. Build requirement-to-test traceability using `templates/test-case.md` and stable IDs.
3. Run and record deterministic platform checks first; validate evidence records and compute the release gate using `qa/deterministic_qa.py`.
4. Do not proceed to visual or exploratory computer-use evaluation until deterministic results and traceability are recorded.
5. Test functional, validation, permission, accessibility, volume, integration, failure, recovery, regression, and rollback paths.
6. Use Playwright only for stable browser journeys; retain traces under the approved evidence location, access, and retention rules.
7. Use vision review for layout and visual anomalies only; mark uncertain findings `review-needed`.
8. Use computer use only in an allowlisted disposable non-production session with synthetic data and a kill switch.
9. Record defects separately from enhancements and missed requirements.
10. Produce the gate recommendation, dispositions, and explicit residual risks for the named human release authority.

## Release rule

Vision and computer use are never release authorities. Critical deterministic results and accountable human approval are mandatory. Follow the capture and public-safety restrictions in `qa/screenshot-plan.md`; do not place client-sensitive data in repository fixtures.
