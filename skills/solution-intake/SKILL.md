---
name: solution-intake
description: Triage a submitted project scope intake form into a developer-ready Solution Brief, a bounded clarification set, and a readiness disposition, without inferring unknown facts.
---

# Solution Intake

Converts a CSM-submitted Project Scope Intake Form into a developer-ready Solution Brief.

Governed by `standards/intake-and-triage.md`.

## When to use

A new client request has arrived as a scope form, meeting summary, or email thread, and someone needs to know what is actually being asked for and whether it can be built.

## Inputs

Required: the scope form or request narrative.
Optional: an approved discovery package, attributed transcript or notes, email threads, existing solution inventory, and prior work for the same client.

When discovery artifacts are supplied, use the public-safe repository templates:

- `../../templates/discovery-script.md`
- `../../templates/discovery-to-user-story-prompt.md`
- `../../templates/user-story-specification.md`

Treat the package as supplemental evidence. Product Owner acceptance confirms specification accuracy only; it does not authorize architecture, build, production change, or release.

## Prohibited actions

- Inferring an unstated fact and presenting it as confirmed
- Treating an unchecked checkbox as a negative answer
- Producing an effort estimate from the form alone
- Designing screens, columns, or flow steps
- Marking a request Ready while a Tier 1 question is open
- Marking a request Ready without a complexity tier and risk class
- Treating Product Owner specification acceptance as approval for a later lifecycle gate
- Generating or retaining a client-specific statement without source attribution
- Sending recordings or transcripts through AI before recording, classification, records, access, retention, and approved-AI-boundary checks
- Touching any production environment

## Procedure

### 1. Register and qualify sources

Assign each source a stable `SRC-##` ID. Record title/type, date, provider or participants, locator method, data classification, access boundary, retention status, and whether it is inside the approved AI boundary.

If recording or transcription is planned, first confirm the approved platform, participant notice/consent, storage and access, records/retention treatment, and permitted AI processing. If a check is unresolved, use approved non-recorded notes or stop; never treat inaccessible or unapproved content as reviewed.

### 2. Parse into four buckets

Read every section including narrative free text. Place each statement into exactly one bucket: **confirmed fact**, **implied requirement**, **assumption**, or **unknown**.

Narrative success-criteria text usually contains more real requirements than the structured sections. Mine it line by line.

### 3. Detect silent gaps

Flag each default-state or absent field as an unanswered question rather than a negative answer. Apply the silent-gap list in `standards/intake-and-triage.md`.

Challenge any "Constraints: None" on records-bearing, regulated, financial, or public-sector work.

Explicitly establish data classification, records/retention, external access, volume/concurrency, devices/connectivity/offline use, accessibility, licensing/cost ownership, support/escalation, and the recording/transcription/AI boundary.

### 4. Incorporate an accepted User Story Specification

If the discovery package includes a Product Owner-accepted specification:

1. Preserve its accepted version and source register.
2. Keep stable story IDs (`US-###`) and acceptance IDs (`US-###-AC-##`); do not renumber or reuse retired IDs.
3. Map every story and criterion into the Solution Brief.
4. Transfer facts, rules, constraints, assumptions, and questions without changing their evidence status.
5. Record contradictions or missing intake controls as open questions.

Product Owner acceptance is evidence of specification accuracy, not readiness or authorization for architecture, build, production change, or release.

### 5. Score

Apply `reference/complexity-and-risk-scoring.md`. Produce complexity tier, risk class, records-bearing flag, and external-exposure flag.

### 6. Recommend platform shape

Apply `reference/platform-decision-rules.md`. For each component, record the requirement that forces it. Components without a forcing requirement are removed.

### 7. Derive acceptance criteria

Convert every narrative success criterion into a testable acceptance criterion or an explicitly deferred item with a reason. Nothing disappears silently.

Format: persona + action + observable outcome + condition. Preserve or assign stable IDs and cite `SRC-##` plus a section, timestamp, or paragraph locator where available.

### 8. Build the question set

Apply `reference/question-bank.md`. Select Tier 1 questions only for round one. Cap at eight. Route each to a named role.

### 9. Assign disposition

Ready, Discovery, or Re-scope, with the reason stated. Ready requires both assigned risk/complexity and closure of every Tier 1 question.

### 10. Write the brief

Populate `templates/solution-intake.md` and produce the outputs below.

## Stop conditions

Stop and escalate rather than proceeding when:

- No accountable business owner exists
- The request requires external or public access
- The request replaces a system of record
- Sensitive data has no approved handling boundary
- The requested timeline is incompatible with the risk class
- The form requests production changes outside normal approval

## Outputs

1. **Triage Record** — four buckets, silent gaps, scores
2. **Solution Brief** — completed intake template
3. **Acceptance criteria table** — with deferrals and reasons
4. **Recommended platform shape** — with forcing requirement per component
5. **Tier 1 question set** — routed to roles, capped at eight
6. **Disposition** — Ready, Discovery, or Re-scope with reason
7. **Risk register seed** — initial risks with owners
8. **Source register and traceability map** — source IDs/locators mapped to stable story and acceptance IDs
9. **Discovery governance record** — recording/transcription, approved AI boundary, classification, access, and retention checks
10. **Specification acceptance record** — Product Owner accuracy acceptance kept distinct from readiness and later approvals

## Quality bar

The output passes when a developer who has never spoken to the client can read the brief and state what to build, what is unknown, what is risky, and what must be answered before starting.

## Next skill

`architecture-and-impact` once the disposition is Ready.

## Reference

- `reference/complexity-and-risk-scoring.md`
- `reference/platform-decision-rules.md`
- `reference/question-bank.md`
- `examples/worked-example-inspection-workflow.md`
