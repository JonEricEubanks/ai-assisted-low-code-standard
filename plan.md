# AI-Assisted Low-Code Standard Implementation Plan

## Summary

Operationalize the Copilot research package as a versioned delivery system with standards, reusable skills, agents, templates, QA evidence, pilots, adoption, metrics, portfolio proof, and a public-safe blog series. The approach standardizes the lifecycle first, encodes it as skills second, uses existing MCP tools third, and introduces specialized agents only where role separation adds measurable value.

## Technical Context

- Platforms: Microsoft Power Apps, Power Automate, SharePoint, Microsoft 365, Microsoft Foundry
- Tool layer: Canvas authoring MCP, Flow MCP, Playwright, approved Microsoft/Azure tools
- Artifact format: Markdown, CSV, JSON/YAML, Mermaid, retained Word source package
- Release authority: deterministic validation plus named human approval
- Initial pilots: Glencoe ELM and Glencoe Early Check
- Evidence boundary: approved repository, synthetic/non-production data, source citations, no inferred unknowns

## Constitution Check

- Accountable humans remain responsible for architecture, sensitive data, permissions, records, and release.
- Production mutation is not autonomous.
- Facts, assumptions, recommendations, and unknowns remain distinct.
- Least privilege and approved AI/data boundaries are mandatory.
- Every improvement must be measurable, versioned, and successor-ready.

## Applied Guidelines

- Prefer platform-native validation and MCP tools over custom duplication.
- Use risk-based testing, deterministic assertions, and explicit failure handling.
- Apply Power Platform ALM patterns: solutions, environment variables, connection references, dependency awareness, and rollback.
- Apply accessibility, secure development, records, and least-privilege practices throughout rather than as final checks.

## Implementation Steps and Tasks

### Phase 1: Program foundation

#### Plan 1.1 - Approve charter and evidence model (REQ-001, REQ-008, REQ-013)

- [ ] T001 [Plan:1.1] Review and approve `governance/goal-charter.md` with the manager and sponsor.
- [ ] T002 [P] [Plan:1.1] Confirm official rating thresholds in `governance/advanced-scorecard.md`.
- [ ] T003 [P] [Plan:1.1] Name all accountable roles and backups in `governance/operating-model.md`.
- [ ] T004 [Plan:1.1] Approve the evidence repository, classification, and retention fields in `qa/evidence-schema.md`.

#### Plan 1.2 - Preserve and normalize source material (REQ-014)

- [x] T005 [Plan:1.2] Preserve the Copilot ZIP contents under `source-material/copilot-package/`.
- [ ] T006 [Plan:1.2] Import `source-material/copilot-package/AI_Assisted_Low_Code_Standardization_Package/Source_Register/internal_evidence_register.csv` into the approved evidence index.
- [ ] T007 [Plan:1.2] Link every internal claim to a retrievable source and mark unsupported claims as open.

### Phase 2: Standard and control foundation

#### Plan 2.1 - Publish lifecycle and platform standards (REQ-002, REQ-003, REQ-013)

- [x] T008 [Plan:2.1] Publish `standards/common-delivery-lifecycle.md`.
- [x] T009 [P] [Plan:2.1] Publish `standards/power-apps.md`.
- [x] T010 [P] [Plan:2.1] Publish `standards/power-automate.md`.
- [x] T011 [P] [Plan:2.1] Publish `standards/sharepoint.md`.
- [x] T012 [P] [Plan:2.1] Publish `standards/integrated-solutions.md`.
- [ ] T013 [Plan:2.1] Obtain control-owner review for security, accessibility, records, licensing, support, and rollback requirements.

#### Plan 2.2 - Publish reusable templates (REQ-004, REQ-008, REQ-013)

- [x] T014 [P] [Plan:2.2] Publish `templates/solution-intake.md`.
- [x] T015 [P] [Plan:2.2] Publish `templates/architecture-decision.md`.
- [x] T016 [P] [Plan:2.2] Publish `templates/test-case.md`.
- [x] T017 [P] [Plan:2.2] Publish `templates/release-checklist.md`.
- [x] T018 [P] [Plan:2.2] Publish `templates/handoff-checklist.md`.

### Phase 3: Reusable skill and orchestration layer

#### Plan 3.1 - Publish core skills (REQ-004, REQ-005)

- [x] T019 [P] [Plan:3.1] Publish intake and architecture skills under `skills/solution-intake/` and `skills/architecture-and-impact/`.
- [x] T020 [P] [Plan:3.1] Publish platform skills under `skills/power-apps-delivery/`, `skills/power-automate-delivery/`, and `skills/sharepoint-delivery/`.
- [x] T021 [P] [Plan:3.1] Publish QA, handoff, and retrospective skills under `skills/`.
- [ ] T022 [Plan:3.1] Run controlled examples and version the first three skills after reviewer feedback.

#### Plan 3.2 - Configure role-based agents (REQ-004, REQ-005, REQ-007)

- [x] T023 [P] [Plan:3.2] Publish `agents/delivery-orchestrator.md`.
- [x] T024 [P] [Plan:3.2] Publish `agents/qa-reviewer.md`.
- [x] T025 [P] [Plan:3.2] Publish `agents/foundry-validation-architecture.md`.
- [ ] T026 [Plan:3.2] Approve the Foundry models, identities, data boundary, tool allowlist, budget, traces, and kill switch.

### Phase 4: QA and validation system

#### Plan 4.1 - Implement the evidence-first QA framework (REQ-006, REQ-008)

- [x] T027 [P] [Plan:4.1] Publish `qa/qa-strategy.md` and `qa/evidence-schema.md`.
- [x] T028 [P] [Plan:4.1] Publish `qa/screenshot-plan.md` and `qa/screenshot-register.csv`.
- [ ] T029 [Plan:4.1] Create synthetic personas, approved test data, and deterministic checks for the first vertical slice.
- [ ] T030 [Plan:4.1] Implement Playwright only for stable, approved journeys and retain traces/screenshots.

#### Plan 4.2 - Add vision and bounded computer use (REQ-006, REQ-007)

- [ ] T031 [Plan:4.2] Implement screenshot normalization and an approved visual baseline process.
- [ ] T032 [Plan:4.2] Evaluate vision output against human-labeled examples and document false positives/negatives.
- [ ] T033 [Plan:4.2] Pilot computer use in a disposable non-production environment or document the approved fallback.
- [ ] T034 [Plan:4.2] Complete threat review and end-to-end evidence-store smoke test.

### Phase 5: Pilot one - ELM

#### Plan 5.1 - Complete ELM evidence and execute the standard (REQ-009, REQ-010, REQ-011)

- [ ] T035 [Plan:5.1] Confirm ELM app URL/ID, owners, connections, lists, flows, permissions, retention, licensing, and support without inference.
- [ ] T036 [Plan:5.1] Baseline a representative ELM activity in `metrics/baseline-and-outcomes.csv`.
- [ ] T037 [Plan:5.1] Execute one approved ELM change using the lifecycle and skills.
- [ ] T038 [Plan:5.1] Run the ELM critical regression, recovery, rollback, and evidence pack.
- [ ] T039 [Plan:5.1] Conduct successor walkthrough and independent regression.
- [ ] T040 [Plan:5.1] Retrospect and publish standard/skill version updates.

### Phase 6: Pilot two - Glencoe Early Check

#### Plan 6.1 - Complete Early Check evidence and execute the standard (REQ-009, REQ-010, REQ-011)

- [ ] T041 [Plan:6.1] Confirm Forms URL, complete flow inventory, owners, connections, connector behavior, document metadata, records, licensing, and support.
- [ ] T042 [Plan:6.1] Baseline a representative Early Check activity in `metrics/baseline-and-outcomes.csv`.
- [ ] T043 [Plan:6.1] Execute an approved change covering approval, document, payment/completion, or connector behavior.
- [ ] T044 [Plan:6.1] Test wrong-department visibility, reject/reassign, duplicate, missing invoice, connector failure, PDF evidence, retention, permissions, accessibility, and rollback.
- [ ] T045 [Plan:6.1] Conduct successor walkthrough and independent regression.
- [ ] T046 [Plan:6.1] Retrospect and publish standard/skill version updates.

### Phase 7: Adoption, portfolio, and publication

#### Plan 7.1 - Demonstrate independent team adoption (REQ-010)

- [ ] T047 [Plan:7.1] Deliver role-based training on lifecycle, skills, platform standards, QA, and handoff.
- [ ] T048 [Plan:7.1] Run an independent developer challenge without author intervention.
- [ ] T049 [Plan:7.1] Record assistance required, unclear instructions, output consistency, defects, and participant feedback.

#### Plan 7.2 - Measure and communicate outcomes (REQ-011, REQ-012)

- [x] T050 [P] [Plan:7.2] Publish `portfolio/evidence-matrix.md`.
- [x] T051 [P] [Plan:7.2] Publish `blog/blog-series-plan.md` and `blog/work-log-template.md`.
- [x] T052 [P] [Plan:7.2] Publish `visuals/process-diagrams.md`.
- [ ] T053 [Plan:7.2] Calculate before/after medians with sample size, range, exclusions, rework, review, and defects.
- [ ] T054 [Plan:7.2] Create sanitized case studies for ELM and Early Check.
- [ ] T055 [Plan:7.2] Complete privacy, client, accessibility, and publication review for every blog asset.
- [ ] T056 [Plan:7.2] Present the evidence portfolio, residual risks, operating ownership, and Q1 backlog for sign-off.

## Project Structure

The root README links governance, standards, skills, agents, templates, QA, metrics, visuals, blog, portfolio, and immutable source material. New solution-specific evidence should be placed in approved project evidence locations and linked from this workspace rather than storing sensitive evidence in public artifacts.

## Requirement Mapping

| REQ ID | Description | Plan Items | Implementation Evidence |
|---|---|---|---|
| REQ-001 | Goal and scorecard | P1.1 | `governance/goal-charter.md`, `governance/advanced-scorecard.md` |
| REQ-002 | Common lifecycle | P2.1 | `standards/common-delivery-lifecycle.md` |
| REQ-003 | Platform standards | P2.1 | `standards/power-apps.md`, `standards/power-automate.md`, `standards/sharepoint.md`, `standards/integrated-solutions.md` |
| REQ-004 | Skills, instructions, templates, agents | P2.2, P3.1, P3.2 | `skills/`, `templates/`, `agents/` |
| REQ-005 | MCP as bounded tool layer | P3.1, P3.2 | Platform skills and orchestrator routing |
| REQ-006 | Multi-lane QA | P4.1, P4.2 | `qa/qa-strategy.md`, validation runs |
| REQ-007 | Safe Foundry validation | P3.2, P4.2 | `agents/foundry-validation-architecture.md`, threat review |
| REQ-008 | Traceability and screenshots | P1.1, P2.2, P4.1 | `qa/evidence-schema.md`, test and screenshot registers |
| REQ-009 | ELM and Early Check pilots | P5.1, P6.1 | Pilot inventories, regression packs, evidence |
| REQ-010 | Independent reuse | P5.1, P6.1, P7.1 | Successor observations, challenge results |
| REQ-011 | Measured improvement | P5.1, P6.1, P7.2 | `metrics/baseline-and-outcomes.csv`, analysis |
| REQ-012 | Portfolio and blog | P7.2 | `portfolio/`, `blog/`, sanitized case studies |
| REQ-013 | Governance and controls | P1.1, P2.1, P2.2 | Charter, standards, decisions, release evidence |
| REQ-014 | Preserve sources | P1.2 | `source-material/copilot-package/`, source register |

