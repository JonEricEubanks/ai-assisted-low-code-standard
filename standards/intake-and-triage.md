# Intake and Triage Standard

Version 1.0 — provisional pending program owner approval.

## Purpose

Convert a CSM-submitted Project Scope Intake Form, supplemented where available by an approved discovery package, into a developer-ready Solution Brief, or return it with a bounded list of blocking questions.

This standard exists because the submitted scope form is written by a client-facing role for a client audience. It is a sales and alignment artifact. It is not a build specification. The gap between those two documents is where estimates fail, rework happens, and handoff debt is created.

## Scope boundary

| Stage | Owner | Produces |
|---|---|---|
| Scope capture | CSM | Project Scope Intake Form sections 1-3 |
| Discovery | Facilitator + stakeholders | Attributed transcript/notes and draft User Story Specification |
| Specification accuracy review | Product Owner | Accepted User Story Specification |
| Triage | Developer / agent | Triage Record |
| Clarification | Developer + CSM + client | Answered question set |
| Solution brief | Developer / agent | Developer-ready Solution Brief |
| Readiness decision | SDM / program owner | Ready, Discovery, or Re-scope |

The developer does not negotiate commercial terms. The CSM does not define technical architecture. Triage is the controlled translation layer between them.

Product Owner acceptance of a User Story Specification confirms that the sourced business need was captured accurately. It is not approval to perform architecture, estimate or build, change production, or release. Those decisions remain at their governed lifecycle gates.

## Core principle

**An intake form is never rejected for being incomplete. It is triaged into one of three dispositions.**

| Disposition | Meaning | Next action |
|---|---|---|
| Ready | All blocking facts are confirmed and the outcome is testable | Proceed to architecture |
| Discovery | Direction is sound but blocking facts are missing | Run a scoped discovery session |
| Re-scope | The request as written cannot be delivered within the stated boundary | Return to CSM with options |

Most forms land in Discovery. That is the expected and healthy result, not a failure.

## Discovery package as intake evidence

The repository-native discovery package consists of:

- `templates/discovery-script.md` — facilitation guide
- `templates/discovery-to-user-story-prompt.md` — source-only draft-generation instruction
- `templates/user-story-specification.md` — Product Owner accuracy-review artifact

The package supplements the Project Scope Intake Form. It does not waive intake scoring, Tier 1 closure, platform decision discipline, or readiness approval.

Before recording, transcription, or AI-assisted processing:

1. Confirm the meeting platform and features are approved.
2. Record participant notice/consent and any restriction on recording or reuse.
3. State the data classification and whether client-sensitive, personal, regulated, or records-bearing content may enter the approved AI boundary.
4. Identify the owner, storage location, access boundary, retention schedule, and disposal rule for recordings, transcripts, notes, prompts, and generated drafts.
5. If any check is unresolved, use approved non-recorded notes or pause capture; do not upload the content to an AI service.

Every transcript, note set, or other discovery source receives a stable source ID such as `SRC-01`, with title/type, date, author or participants, location, classification, and access/retention status. Every derived story and acceptance criterion cites one or more source IDs and, where available, a section, timestamp, or paragraph locator. Unattributed content is an assumption or open question, never a confirmed requirement.

Story IDs (`US-001`, `US-002`) and acceptance IDs (`US-001-AC-01`) remain stable after Product Owner review. Retired IDs are marked retired and not reused. This preserves traceability into architecture, tasks, tests, evidence, and change control.

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
- No accessibility needs or organizational baseline
- No licensing or recurring-cost owner
- No named support owner, backup, or escalation route
- No external-user or public-access position
- No approved recording, transcription, AI, or transcript-retention boundary when discovery capture is proposed

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

Acceptance criteria are written in the form: *persona + action + observable outcome + condition.* Assign stable story and acceptance IDs, and cite the source ID and locator for each criterion.

## Stage 6 — Hand off the accepted specification

When a Product Owner has accepted the User Story Specification for accuracy:

1. Preserve the accepted version and its source register.
2. Map every active story ID and acceptance ID into the Solution Brief.
3. Transfer confirmed facts, business rules, required information, constraints, assumptions, and open questions without changing their evidence status.
4. Reconcile the specification against intake controls for data classification, records/retention, external access, volume, devices/offline use, accessibility, licensing, support, security, and integrations.
5. Log contradictions and uncovered controls as questions; do not infer answers or silently expand scope.
6. Record Product Owner acceptance separately from the readiness decision and all later approvals.

The Solution Brief remains the handoff artifact into architecture.

## Stage 7 — Produce the readiness decision

Complete the Solution Brief and assign the disposition. The brief is the handoff artifact into architecture.

A request may not be marked Ready while any blocking question remains open. Blocking questions are defined in the question bank as Tier 1. Ready also requires an assigned complexity tier and risk class. Product Owner specification acceptance cannot substitute for either requirement.

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
                    │ Stage 7 Readiness decision ──┼───────────────────────┤──► Ready
                    │                              │                       │    Discovery
                    │                              │                       │    Re-scope
```

## Definition of Ready for architecture

Inherits the Definition of Ready in `common-delivery-lifecycle.md`, plus:

- Every narrative success criterion is mapped or explicitly deferred
- Every accepted discovery story and acceptance criterion is mapped by stable ID or explicitly retired/deferred with reason
- Every discovery-derived requirement has source attribution
- Complexity tier and risk class are assigned
- All Tier 1 questions are answered
- A named business owner exists who is not the developer
- Records and retention position is stated, even if the answer is "not a record"
- Data classification is stated, even if the answer is "public"
- Recording/transcription and approved AI-boundary checks are complete or recorded as not applicable
- External access, volume, supported devices/offline use, accessibility, licensing, and support positions are stated

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Estimating from the form alone | The form describes outcomes, not surface area |
| Treating unchecked boxes as "no" | Converts unasked questions into false facts |
| Starting the build during discovery | Creates unreviewed scope that nobody approved |
| Treating Product Owner specification acceptance as project approval | Bypasses architecture, build, release, and named-approver gates |
| Generating requirements without source locators | Turns model output into unattributed scope |
| Uploading a transcript before boundary checks | May violate consent, classification, records, or AI-use controls |
| Accepting a platform name as a deliverable | Defers the real decision to implementation |
| Sending more than a focused question set at once | Produces no answers at all |
| Carrying "Constraints: None" forward unchallenged | Hides records, security, and licensing obligations |

## Related

- `standards/common-delivery-lifecycle.md`
- `skills/solution-intake/SKILL.md`
- `templates/solution-intake.md`
