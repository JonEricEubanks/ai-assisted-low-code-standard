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
Optional: meeting notes, email threads, existing solution inventory, prior work for the same client.

## Prohibited actions

- Inferring an unstated fact and presenting it as confirmed
- Treating an unchecked checkbox as a negative answer
- Producing an effort estimate from the form alone
- Designing screens, columns, or flow steps
- Marking a request Ready while a Tier 1 question is open
- Touching any production environment

## Procedure

### 1. Parse into four buckets

Read every section including narrative free text. Place each statement into exactly one bucket: **confirmed fact**, **implied requirement**, **assumption**, or **unknown**.

Narrative success-criteria text usually contains more real requirements than the structured sections. Mine it line by line.

### 2. Detect silent gaps

Flag each default-state or absent field as an unanswered question rather than a negative answer. Apply the silent-gap list in `standards/intake-and-triage.md`.

Challenge any "Constraints: None" on records-bearing, regulated, financial, or public-sector work.

### 3. Score

Apply `reference/complexity-and-risk-scoring.md`. Produce complexity tier, risk class, records-bearing flag, and external-exposure flag.

### 4. Recommend platform shape

Apply `reference/platform-decision-rules.md`. For each component, record the requirement that forces it. Components without a forcing requirement are removed.

### 5. Derive acceptance criteria

Convert every narrative success criterion into a testable acceptance criterion or an explicitly deferred item with a reason. Nothing disappears silently.

Format: persona + action + observable outcome + condition.

### 6. Build the question set

Apply `reference/question-bank.md`. Select Tier 1 questions only for round one. Cap at eight. Route each to a named role.

### 7. Assign disposition

Ready, Discovery, or Re-scope, with the reason stated.

### 8. Write the brief

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

## Quality bar

The output passes when a developer who has never spoken to the client can read the brief and state what to build, what is unknown, what is risky, and what must be answered before starting.

## Next skill

`architecture-and-impact` once the disposition is Ready.

## Reference

- `reference/complexity-and-risk-scoring.md`
- `reference/platform-decision-rules.md`
- `reference/question-bank.md`
- `examples/worked-example-inspection-workflow.md`
