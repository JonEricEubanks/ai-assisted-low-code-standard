# Pilot Readiness

## Pilot C: Flossmoor FOIA (live, new build) — ACTIVE

Purpose: run the full standard from intake forward on a genuinely new client request, with no dependency on reconstructing undocumented facts. First pilot to produce realized (not reconstructed) evidence.

Status 2026-10-17: intake complete; data layer provisioned; Canvas app v2 (Tablet-type, adaptive three-tier) published to dev with desktop and phone tiers verified; Survey123 intake flow fully designed, not yet deployed. Tracked as Phase 5A in `plan.md`; working folder `pilots/flossmoor-foia/`.

Entry gate status:

- accountable owner and approver — client FOIA officer identified in transcript; MGP owner = pilot lead; formal backup **open**
- entry points and component inventory — complete (`sharepoint-schema.md`, `datasource-schema.md`, v2 YAML)
- data classification and test-data boundary — synthetic only in Community Essentials; approved
- baseline activity and measurement rules — defined in `metrics/baseline-and-outcomes.csv` schema; **actuals not yet recorded** (T071)
- rollback and support ownership — v1 retained as rollback reference until v2 acceptance; support owner **open**

Required outputs remaining: real-device tier evidence (T064), end-to-end CRUD journey (T065), flow deployment and test (T068–T070), effort actuals (T071), second-developer change (T072), retrospective (T073).

## Pilot A: reusable product-family reconstruction (ELM) — BLOCKED

Purpose: prove that a repeated solution family can be reconstructed into one governed baseline plus implementation-specific delta records.

Required outputs:

- product-family component and dependency baseline
- implementation delta template
- persona regression pack
- owner and backup matrix
- connection and service-identity inventory
- security, records, licensing, monitoring, and support decisions
- deployment, rollback, and recovery runbook
- observed independent-developer change
- before/after measurements

## Pilot B: integration-governance reconstruction (Early Check) — BLOCKED

Purpose: prove that a multi-stage workflow with approvals, documents, finance/records processing, and an external integration can be made successor-ready.

Required outputs:

- complete trigger and flow inventory
- secret-safe integration contract
- sanitized data-flow diagram
- persona-based end-to-end regression
- duplicate, reassignment, rejection, missing-document, authentication-failure, retry, and recovery tests
- approval and audit-evidence validation
- security, licensing, records, and support sign-off
- observed independent-developer change
- before/after measurements

## Entry gate

Neither reconstruction pilot (A, B) starts implementation until:

- accountable owner and approver are named
- reliable entry points and component inventories exist
- data classification and test-data boundary are approved
- baseline activity and measurement rules are defined
- rollback and support ownership are identified

## Exit gate

The pilot is complete only after deterministic QA, named human approval, successor verification, retained evidence, metrics, and a retrospective-driven standard update.
