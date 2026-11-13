# Common Delivery Lifecycle

## 1. Intake and qualification

Capture business outcome, users, scope, constraints, data sensitivity, urgency, owner, and success measures. Reject or re-scope work that lacks an accountable owner or testable outcome.

An approved discovery package may supplement, but never replace, the intake evidence. Product Owner acceptance confirms that a User Story Specification accurately represents the sourced business need; it does not authorize architecture, build, production change, or release.

**Exit:** approved intake brief, initial risk class, and any accepted discovery artifacts linked as attributed sources.

## 2. Discovery and requirements

Identify personas, journeys, functional and non-functional requirements, exceptions, accessibility, records, security, integrations, volume, support, and acceptance criteria.

When recorded or AI-assisted discovery is proposed, confirm participant notice/consent, approved recording and transcription handling, the approved AI boundary, data classification, and records/retention treatment before capture or processing. Attribute each derived requirement to a source and preserve stable story and acceptance-criterion IDs.

An accepted User Story Specification is handed into the Solution Brief through an explicit mapping of story and acceptance IDs; contradictions and missing intake controls remain open questions rather than being silently resolved.

**Exit:** requirements are testable, sources are attributed, unknowns are logged, and the accepted specification is mapped into the Solution Brief.

## 3. Architecture and data design

Decide system of record, component boundaries, data model, identities, permissions, environments, connectors, licensing, ALM, telemetry, error handling, recovery, retention, and rollback.

**Exit:** architecture decision and impact map approved.

## 4. Build planning

Decompose work into bounded changes. Map each task to requirements, tests, owner, dependencies, risk, and evidence.

**Exit:** approved plan and Definition of Ready.

## 5. Implementation

Use the applicable platform standards and skills. Make changes only in approved environments. Update source, documentation, tests, release notes, and evidence together.

**Exit:** builder self-review passes.

## 6. Independent QA

Run deterministic checks first, then functional, accessibility, visual, exploratory, permissions, recovery, performance, and regression testing as applicable.

Visual checks follow `visual-verification.md`: the agent that made a backend change opens the real rendered surface in the shared browser, captures it at each supported breakpoint, and inspects the capture before claiming completion.

**Exit:** critical tests pass and defects are dispositioned.

## 7. Release approval and deployment

Confirm solution version, dependencies, connection references, environment variables, permissions, rollback, communications, support, and evidence.

**Exit:** named approvers authorize release.

## 8. Handoff and support

Deliver inventory, architecture, runbook, support model, known issues, ownership, recovery, and regression pack. A successor performs representative tasks.

**Exit:** successor verification accepted.

## 9. Retrospective and standard update

Measure effort, rework, defects, outcomes, skill performance, manual intervention, and adoption. Promote reusable lessons into versioned standards.

**Exit:** metrics recorded and improvement backlog approved.

## Definition of Ready

- Named owner and approver
- Testable outcome and acceptance criteria
- Data classification and approved AI boundary
- Source attribution for discovery-derived requirements and stable story/acceptance IDs
- Recording, transcription, and participant-notice checks completed when applicable
- Complexity tier and risk class assigned
- All Tier 1 intake questions closed with attributed answers
- Architecture and impact understood
- Licensing, security, records, and accessibility considered
- Environment and test data ready
- Dependencies and rollback identified

## Definition of Done

- Acceptance criteria and critical regression pass
- No unresolved Sev 1/2 defects
- Security, accessibility, records, and licensing decisions retained
- Release and rollback evidence retained
- Runbook and handoff complete
- Successor can locate and use the artifacts
- Metrics and retrospective recorded
