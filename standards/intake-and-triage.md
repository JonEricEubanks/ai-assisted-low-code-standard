# Intake and Triage Standard

Version 1.0 — provisional pending program owner approval.

## Purpose

Convert a CSM-submitted Project Scope Intake Form into a developer-ready Solution Brief, or return it with a bounded list of blocking questions.

This standard exists because the submitted scope form is written by a client-facing role for a client audience. It is a sales and alignment artifact. It is not a build specification. The gap between those two documents is where estimates fail, rework happens, and handoff debt is created.

## Scope boundary

| Stage | Owner | Produces |
|---|---|---|
| Scope capture | CSM | Project Scope Intake Form sections 1-3 |
| Triage | Developer / agent | Triage Record |
| Clarification | Developer + CSM + client | Answered question set |
| Solution brief | Developer / agent | Developer-ready Solution Brief |
| Readiness decision | SDM / program owner | Ready, Discovery, or Re-scope |

The developer does not negotiate commercial terms. The CSM does not define technical architecture. Triage is the controlled translation layer between them.

## Core principle

**An intake form is never rejected for being incomplete. It is triaged into one of three dispositions.**

| Disposition | Meaning | Next action |
|---|---|---|
| Ready | All blocking facts are confirmed and the outcome is testable | Proceed to architecture |
| Discovery | Direction is sound but blocking facts are missing | Run a scoped discovery session |
| Re-scope | The request as written cannot be delivered within the stated boundary | Return to CSM with options |

Most forms land in Discovery. That is the expected and healthy result, not a failure.

## Stage 1 — Parse

Read the form and extract every statement into one of four buckets. Do not blend them.

| Bucket | Definition |
|---|---|
| Confirmed fact | Explicitly stated in the form or a cited source |
| Implied requirement | Strongly suggested by the narrative but never stated as a requirement |
| Assumption | Something the developer would otherwise fill in silently |
| Unknown | Required to build, and not answerable from the form |

The non-negotiable Power Desk rule applies here: **unknown facts are logged, not inferred.**

Pay particular attention to narrative success-criteria text. Client narratives routinely contain requirements that never appear in the checkbox sections. The narrative is usually the richest part of the form and the least structured.

## Stage 2 — Detect silent gaps

Checkbox sections left at their default state are the single most common source of downstream failure. An unchecked box is not a "no." It is an unanswered question.

Treat each of the following as a silent gap until explicitly confirmed:

- No target completion date
- No objective category selected
- No estimated hours
- No risk category selected
- Constraints stated as "None"
- Deliverable described only as a platform name
- No named business owner distinct from the requester
- No statement of record ownership or retention
- No statement of who may see or edit data
- No volume, no device, and no offline expectation

"Constraints: None" deserves specific scrutiny. For public-sector, regulated, or records-bearing work, there are always constraints. The absence means nobody asked.

## Stage 3 — Classify

Score the request using `skills/solution-intake/reference/complexity-and-risk-scoring.md`. Produce:

- Complexity tier: S, M, L, or XL
- Risk class: Low, Moderate, High
- Records-bearing: yes or no
- External-party exposure: yes or no

Complexity drives effort and sequencing. Risk drives approval depth. They are independent — a small solution can carry high risk.

## Stage 4 — Recommend platform shape

Apply `skills/solution-intake/reference/platform-decision-rules.md`. Produce a recommended component shape and, critically, the reason each component was chosen. The reason is what survives into the architecture decision record.

Never recommend a platform component without naming the requirement that forces it.

## Stage 5 — Write acceptance criteria

Every success-criteria bullet in the narrative must become either:

- a testable acceptance criterion, or
- an explicitly deferred item with a recorded reason

No bullet may silently disappear. This is the traceability root. The Power Desk delivery charter requires every acceptance criterion to map to test evidence, and that mapping begins here, at intake, not at QA.

Acceptance criteria are written in the form: *persona + action + observable outcome + condition.*

## Stage 6 — Produce the readiness decision

Complete the Solution Brief and assign the disposition. The brief is the handoff artifact into architecture.

A request may not be marked Ready while any blocking question remains open. Blocking questions are defined in the question bank as Tier 1.

## Swimlane

```
CSM                 │ Developer / Agent            │ Client                │ SDM / Program Owner
────────────────────┼──────────────────────────────┼───────────────────────┼────────────────────
Submit scope form   │                              │                       │
                    │ Stage 1 Parse                │                       │
                    │ Stage 2 Detect silent gaps   │                       │
                    │ Stage 3 Classify             │                       │
                    │ Stage 4 Platform shape       │                       │
                    │ Stage 5 Acceptance criteria  │                       │
                    │ Produce Triage Record        │                       │
                    │         │                    │                       │
                    │         ├─ Tier 1 gaps? ──── │ ──► Clarification     │
Relay questions ◄───┤         │                    │     session           │
                    │         │                    │     Answers ──────────┤
                    │ Update brief ◄───────────────┤                       │
                    │         │                    │                       │
                    │ Stage 6 Readiness decision ──┼───────────────────────┤──► Ready
                    │                              │                       │    Discovery
                    │                              │                       │    Re-scope
```

## Definition of Ready for architecture

Inherits the Definition of Ready in `common-delivery-lifecycle.md`, plus:

- Every narrative success criterion is mapped or explicitly deferred
- Complexity tier and risk class are assigned
- All Tier 1 questions are answered
- A named business owner exists who is not the developer
- Records and retention position is stated, even if the answer is "not a record"
- Data classification is stated, even if the answer is "public"

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Estimating from the form alone | The form describes outcomes, not surface area |
| Treating unchecked boxes as "no" | Converts unasked questions into false facts |
| Starting the build during discovery | Creates unreviewed scope that nobody approved |
| Accepting a platform name as a deliverable | Defers the real decision to implementation |
| Sending more than a focused question set at once | Produces no answers at all |
| Carrying "Constraints: None" forward unchallenged | Hides records, security, and licensing obligations |

## Related

- `standards/common-delivery-lifecycle.md`
- `skills/solution-intake/SKILL.md`
- `templates/solution-intake.md`
