# User Story Specification

Use this public-safe specification for straightforward discovery outcomes. It supplements the Solution Brief and does not replace intake, risk/complexity scoring, or Tier 1 closure.

## Project information

- Project:
- Product Owner:
- Prepared by:
- Discovery date:
- Specification version:
- Status: Draft / Accepted for accuracy

## Source register

- **Source ID:** `SRC-##`
  - Title/type:
  - Date:
  - Provider/participants:
  - Classification:
  - Approved location/access:
  - Retention/disposal:
  - Locator method:

Only supported statements may be presented as confirmed. Cite a source ID and locator such as a transcript timestamp, paragraph, or note heading. Put unsupported or unclear content under Open Questions or Assumptions.

## Business need

### Problem

[Current problem, affected users, impact, and source citation.]

### Desired outcome

[Observable improvement and source citation. Do not invent metrics.]

## Users and scope

### Primary users

- [Role]: [goal] — Source:

### In scope

- [Included outcome] — Source:

### Out of scope

- [Excluded outcome] — Source:

## User stories

Keep IDs stable after issue. Never reuse a retired ID.

### US-001 — [Short title]

- **Source:** `SRC-##`, [timestamp/section/paragraph]
- **Priority:** [Only when explicitly stated; otherwise “Not stated”]
- **Story:** As a [role], I want [capability], so that [business value].

#### Acceptance criteria

##### US-001-AC-01 — [Scenario]

- **Source:** `SRC-##`, [locator]
- **Given** [starting condition]
- **When** [action or event]
- **Then** [observable result]

##### US-001-AC-02 — [Scenario]

- **Source:** `SRC-##`, [locator]
- **Given** [starting condition]
- **When** [action or event]
- **Then** [observable result]

#### Business rules

- [Approval, validation, calculation, deadline, permission, or status rule] — Source:

#### Required information

- [Information users enter, view, or receive] — Known source:

#### Dependencies and fixed constraints

- [Only sourced dependencies or constraints] — Source:

#### Status

Active / Deferred / Retired. If deferred or retired, record reason, approver, date, and replacement ID if any.

## Cross-cutting requirements

Record confirmed positions or identify the open-question owner:

- Data classification and approved AI boundary:
- Recording/transcript storage, access, retention, and disposal:
- Records/retention:
- External/public access:
- Volume, growth, concurrency, and attachments:
- Supported devices, connectivity, and offline behavior:
- Accessibility baseline and additional needs:
- Licensing and recurring-cost approval:
- Support owner, backup, monitoring, and escalation:
- Security/permissions:
- Integrations and source systems:

## Open questions

- **Question ID:** `Q-##`
  - Question:
  - Why it matters:
  - Owner:
  - Due:
  - Blocking/Tier:
  - Source:

## Assumptions

- **Assumption ID:** `ASM-##`
  - Assumption:
  - Confirmation owner:
  - Due:
  - Source/basis:

## Product Owner acceptance

Acceptance means the specification accurately reflects the sourced business need. It is **not** project-go, readiness, architecture, estimate, build, production-change, or release authorization.

- Name:
- Role:
- Date:
- Accepted version:
- Evidence/location:

## Intake handoff check

- [ ] Every client-specific statement has a source ID and locator, or is visibly an assumption/open question.
- [ ] Story and acceptance IDs are stable and unique.
- [ ] Each story contains a role, capability, and value.
- [ ] Acceptance criteria are observable and testable.
- [ ] Scope, rules, required information, dependencies, and unknowns are visible.
- [ ] Classification, records, external access, volume, devices, accessibility, licensing, and support are addressed.
- [ ] Active stories and criteria are mapped into `templates/solution-intake.md`.
- [ ] Complexity tier and risk class are assigned during intake.
- [ ] All Tier 1 questions are closed before a Ready disposition.
