# Discovery-to-User-Story Prompt

Use this public-safe prompt only after the recording/transcription, data-classification, records/retention, access, and approved-AI-boundary checks in `templates/discovery-script.md` are complete. Do not submit unapproved or client-sensitive content.

## Inputs

- Project name: `[PROJECT NAME]`
- Approved transcript or note source IDs: `[SRC-##]`
- Optional existing specification version: `[VERSION OR NONE]`

## Prompt

Act as a business analyst. Create a concise draft User Story Specification for `[PROJECT NAME]` using **only** the supplied approved discovery sources.

Source-only rules:

1. Do not invent or infer requirements, decisions, priorities, metrics, business rules, technical details, classifications, approvals, or source locators.
2. Cite every client-specific statement with its supplied stable source ID and the most precise available locator (timestamp, section, paragraph, or note heading).
3. If information is missing or unclear, put it under Open Questions with an owner only when the source names one.
4. If a statement appears likely but is not confirmed, put it under Assumptions and mark it “Confirm with Product Owner.”
5. Preserve existing story and acceptance IDs. For new items, assign the next unused `US-###` and `US-###-AC-##` IDs. Never reuse or renumber retired IDs.
6. Combine duplicate sourced statements without losing meaning and cite every supporting source.
7. Do not expose content that the supplied boundary instructions mark for exclusion or redaction.

Use the structure in `templates/user-story-specification.md`:

- Project information
- Source register
- Business need: problem and desired outcome
- Primary users, in scope, and out of scope
- One story per distinct user outcome
  - Stable story ID and short title
  - Priority only if explicitly stated
  - “As a [role], I want [capability], so that [business value].”
  - Stable acceptance IDs using Given / When / Then
  - Business rules
  - Required information and known source
  - Dependencies and fixed constraints
- Cross-cutting requirements
- Open Questions
- Assumptions
- Product Owner accuracy-acceptance block
- Intake handoff check

For cross-cutting requirements, report only sourced facts for data classification and approved AI boundary, recording/transcript handling, records/retention, external access, volume/concurrency, devices/connectivity/offline use, accessibility, licensing/cost ownership, support/escalation, security/permissions, and integrations. Missing positions belong under Open Questions and may prevent Ready.

Do not create architecture, data models, screen layouts, field specifications, connector choices, integrations, estimates, technical tasks, or release plans unless a source explicitly states a fixed constraint. Record such statements as sourced constraints, not as design decisions.

Before responding, verify:

- Every client-specific statement has a supplied source ID and valid locator.
- Every story identifies a role, capability, and value.
- Every acceptance criterion is observable and testable.
- Missing or conflicting information is visible.
- The draft does not claim Ready.
- Product Owner acceptance is described only as confirmation of specification accuracy, not authorization for architecture, build, production change, or release.

Return only the completed Markdown specification. Do not reproduce source transcripts or client-sensitive passages.
Use concise headings, bullets, and numbered IDs; do not use tables in the generated specification.

## Human review

The generated document is a draft. The Product Owner and technical team review source fidelity, story boundaries, acceptance criteria, controls, and open questions. Intake then assigns complexity and risk, closes Tier 1 questions, and issues the readiness disposition.
