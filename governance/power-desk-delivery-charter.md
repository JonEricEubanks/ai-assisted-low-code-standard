# Power Desk Delivery Charter

## Purpose

Provide new hires and current Power Desk developers with one governed, reusable delivery system for Power Apps, Power Automate, SharePoint lists, modern pages, document libraries, and related Microsoft 365 components.

## Business outcome

Appropriately scoped solutions are delivered consistently without depending on one developer's undocumented knowledge. Developers can enter the process at the stage they need, follow the same controls, and leave traceable work for the next owner.

## In scope

- Intake, discovery, architecture, implementation, QA, release, handoff, and retrospective
- Power Apps Canvas apps
- Power Automate cloud flows
- SharePoint lists, libraries, and modern pages
- Reusable prompts, skills, agent instructions, templates, and patterns
- Deterministic, visual, exploratory, accessibility, and human validation
- ALM, security, records, licensing, support, and rollback decisions
- New-hire onboarding and continued developer enablement

## Out of scope

- Autonomous production deployment or security changes
- Replacement of platform-native validation
- Full automation of every Microsoft 365 surface
- Unverified claims about quality or efficiency
- Publishing client-sensitive implementation details

## Non-negotiables

1. One accountable human owner exists for every solution and release.
2. Requirements and impact analysis precede implementation.
3. Unknown facts are logged, not inferred.
4. Least privilege and approved data boundaries apply.
5. Deterministic checks and human approval remain release authorities.
6. Records, licensing, rollback, and support decisions are documented.
7. Every requirement maps to acceptance criteria, a test, and retained evidence.
8. Handoff enables another developer to support the solution.
9. Discovery statements retain source attribution and remain separated as confirmed facts, implied requirements, assumptions, or unknowns.
10. Requirement, story, and acceptance-criterion IDs remain stable from discovery through handoff.
11. Recording, transcription, and AI use during discovery require explicit approval for the applicable participants, content, and data boundary.
12. Unresolved blockers remain visible and prevent readiness approval when they affect architecture or delivery.

## Discovery-to-architecture control

The governed sequence is:

`Qualification/intake -> discovery artifacts -> Product Owner specification-accuracy validation -> developer/agent governed triage -> accountable readiness approval -> architecture`

The Product Owner validates that the discovery specification accurately represents the intended need. That acceptance does not approve architecture, authorize build, or approve release. Governed triage and accountable readiness approval remain mandatory before architecture.

## Delivery gates

| Gate | Exit criteria |
|---|---|
| Discovery specification validated | Sources are attributed; confirmed facts, implied requirements, assumptions, and unknowns are separated; stable requirement, story, and acceptance-criterion IDs are assigned; unresolved blockers are recorded; recording, transcription, and AI boundaries are approved; and the Product Owner confirms specification accuracy |
| Intake ready | Developer/agent triage is complete; scope, owners, requirements, unknowns, blockers, risk, and platform recommendation are reviewed; and the accountable readiness approver accepts the baseline |
| Architecture approved | Data, integration, security, licensing, support, impact, and rollback decisions accepted |
| Build complete | Approved design implemented with traceability and no unauthorized production changes |
| QA complete | Required functional, deterministic, accessibility, permission, recovery, and regression evidence accepted |
| Release approved | Readiness, approvals, rollback, support, and release evidence complete |
| Handoff accepted | Documentation, ownership, support context, and successor walkthrough accepted |

## Ownership

- Power Desk leadership owns this charter and the approved delivery boundaries.
- Product Owners validate discovery specification accuracy without granting architecture, build, or release approval.
- Developers or agents complete governed triage after specification validation.
- The designated readiness approver authorizes progression from a `Ready` triage baseline to architecture.
- Solution owners approve scope, architecture, release, and material risk decisions.
- Developers follow the lifecycle and retain required evidence.
- Independent reviewers validate the solution against approved requirements.
- Successors confirm that handoff materials are usable.
