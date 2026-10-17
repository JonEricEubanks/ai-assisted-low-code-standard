# Complexity and Risk Scoring

Complexity and risk are scored independently. A small solution can carry high risk, and a large solution can carry low risk. Collapsing them into one number is the most common estimating error.

## Complexity scoring

Score each dimension 0-3. Sum to get the tier.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Entities | 1 | 2-3 | 4-6 | 7+ |
| Personas | 1 | 2 | 3-4 | 5+ |
| Departments or orgs | 1 | 2 | 3 | 4+ |
| Process stages | Single step | 2-3 | 4-6 | 7+ with branching |
| Device surface | Desktop only | Desktop + tablet | Field/mobile primary | Offline required |
| Integrations | None | 1 M365 service | 2-3 M365 services | External system |
| Media handling | None | Attachments | Photos with rules | Photos + generated documents |
| Scheduling | None | Simple reminder | Recurring cycle | Cycle + escalation |
| Reporting | None | Basic views | Dashboard | Cross-entity analytics |
| Migration | None | Small seed | Historical records | Legacy system cutover |

| Total | Tier | Typical shape |
|---|---|---|
| 0-6 | S | One list plus a basic flow |
| 7-13 | M | Multiple lists, one app, several flows |
| 14-21 | L | Multi-entity app, role separation, scheduled automation, documents |
| 22+ | XL | Multi-department platform; split into phases before estimating |

**XL requests are not estimated as a single unit.** They are decomposed into phases, and only phase one is estimated.

## Risk scoring

Risk is assessed by trigger, not by score. Any single trigger sets the class.

### High risk — any one of these

- Output is an official record, or feeds legal, court, adjudication, or enforcement action
- Financial transaction, payment, or invoice handling
- Personal, health, or employment-sensitive data
- Public-records, FOIA, or legal-hold exposure
- External-party or public-facing access
- Replaces a system of record
- Failure causes a compliance or statutory deadline to be missed

### Moderate risk — any one of these

- Crosses departmental ownership boundaries
- Drives notifications that people act on operationally
- Stores photos or documents used as evidence
- Requires a premium connector or paid license
- Has a hard external deadline
- Involves a service account or shared identity

### Low risk

- Internal, single-department, non-records, no external exposure, no financial impact

## What risk class controls

| Risk class | Required before build | Required before release |
|---|---|---|
| Low | Named owner, acceptance criteria | Owner acceptance |
| Moderate | Owner, permission model, retention position, support route | QA evidence, owner acceptance |
| High | All of the above plus records decision, security review, rollback plan, named approver | Full traceability matrix, signed approval, rollback evidence, successor handoff |

High-risk work may not proceed on an unstated records position. "We did not consider it" is not a position.

## Honest statement of use

These thresholds are a provisional calibration instrument, not a measured model. They are intentionally coarse. Their value is forcing the conversation to happen at intake rather than at QA.

Record the actual outcome against the predicted tier in `metrics/baseline-and-outcomes.csv`. Recalibrate the bands once real data exists. Until then, do not present a tier as an effort estimate.
