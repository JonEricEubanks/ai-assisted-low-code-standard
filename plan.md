# AI-Assisted Low-Code Standard Implementation Plan

## Summary

Operationalize the Copilot research package as a versioned Power Desk delivery system with standards, reusable skills, agents, templates, QA evidence, pilots, developer onboarding, metrics, operational evidence, and public-safe training content. The approach standardizes the lifecycle first, encodes it as skills second, uses existing MCP tools third, and introduces specialized agents only where role separation adds measurable value.

## Discovery Workflow Update Plan

The new discovery package (Discovery Script, User Story Specification, and Copilot translation prompt) is a strong operational improvement for discovery and user-story capture, but it must be integrated into the existing governance lifecycle rather than treated as a replacement for architecture, intake, QA, or release approval.

### Rollout objective

Align the repo around a single discovery-to-delivery workflow:

1. CSM package and intake brief establish scope and unknowns.
2. Discovery captures business problem, users, outcomes, constraints, and open questions.
3. User Story Specification and acceptance criteria are reviewed by the Product Owner.
4. Intake triage and risk classification determine whether the request is Ready, Discovery, or Re-scope.
5. Architecture and implementation only begin after formal approval.
6. QA, release, and handoff remain governed by the same evidence and approval model.

### Workstreams to update in one batch

- Repo overview and onboarding: `README.md`, `AGENT_WORKFLOW.md`, `docs/start/*`, `docs/architecture/*`
- Governance and lifecycle standards: `standards/common-delivery-lifecycle.md`, `standards/intake-and-triage.md`, `skills/solution-intake/*`, `templates/solution-intake.md`
- Agent behavior: `agents/delivery-orchestrator.md`, `.github/agents/mgp-delivery.agent.md`, `.github/copilot-instructions.md`
- Training and public-facing content: `docs/training/*`, `blog/*`, `docs/index.html`, `portfolio/*` where appropriate
- GitHub tracking: create a coordinated update issue and a single review PR for the documentation batch

### Delivery sequence and status

#### Phase A — Governance alignment
- [x] Confirm the discovery package is treated as a discovery artifact, not a release decision.
- [x] Update the intake standard to explicitly differentiate Product Owner specification acceptance from architecture readiness.
- [x] Update the solution intake template and question bank to capture records, retention, volume, owner, approval path, data classification, and approved recording/AI boundaries.
- [x] Confirm that all statements, open questions, and assumptions remain traceable to an attributed source.

#### Phase B — Repository updates
- [x] Update `README.md` to describe the new discovery flow as the default intake path.
- [x] Update `AGENT_WORKFLOW.md` to route work through discovery before architecture.
- [x] Publish repository-native discovery script, transcript-to-story prompt, and User Story Specification templates.
- [x] Refresh `skills/solution-intake/SKILL.md` and the intake reference material to include the new discovery package and Product Owner validation gate.
- [x] Update `templates/solution-intake.md` and the supporting standards to require a governance review before Ready is assigned.

#### Phase C — Training and enablement
- [x] Update onboarding, training materials, and workshop docs to teach the new discovery script and user-story workflow.
- [x] Update blog and public-safe materials to describe the governed discovery flow and the approval gates that follow it.
- [x] Add examples showing how a discovery transcript becomes a user story specification and then enters the lifecycle.

#### Phase D — GitHub tracking and review
- [x] Create repo-level issue `#34` covering the documentation and standards alignment batch.
- [ ] Open a single PR branch for the cross-document update and keep the scope limited to documentation and workflow alignment.
- [ ] Require review from the program owner, developer representative, and training/enablement owner before merge.

### Change owners

- Program owner: lifecycle, readiness gate, and strategic approval
- Developer/architect: standards, intake, risk classification, and architecture readiness
- Repo editor: README, repo map, cross-link cleanup, and documentation consistency
- Training owner: docs/training and blog updates
- GitHub/ops: issue, PR, and branch tracking

### Acceptance criteria for the rollout

- The repo clearly states that discovery and user-story capture are upstream of architecture and build.
- The workflow preserves explicit human approval at each gate.
- The repo distinguishes confirmed facts, assumptions, unknowns, and open questions.
- Transcript-derived statements retain source and participant attribution, and recording/transcription stays within the approved consent, access, retention, and AI boundary.
- Training materials explain both the discovery script and the governance gates that follow it.
- The README and operating guidance reflect the same lifecycle sequence.

## Technical Context

- Platforms: Microsoft Power Apps, Power Automate, SharePoint, Microsoft 365, Microsoft Foundry
- Tool layer: Canvas authoring MCP, Flow MCP, Playwright, approved Microsoft/Azure tools
- Artifact format: Markdown, CSV, JSON/YAML, Mermaid, retained Word source package
- Release authority: deterministic validation plus named human approval
- Initial pilots: Glencoe ELM and Glencoe Early Check (reconstruction; blocked on owner/ID confirmation)
- Live pilot: Flossmoor FOIA (new build; executing now — see Phase 5A)
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

- [ ] T001 [Plan:1.1] Review and approve `governance/power-desk-delivery-charter.md` with Power Desk leadership.
- [ ] T002 [P] [Plan:1.1] Confirm operational quality thresholds in `governance/delivery-quality-scorecard.md`.
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

#### Plan 2.3 - Integrate governed discovery (REQ-015)

- [x] T018A [P] [Plan:2.3] Publish the discovery script, transcript-to-story prompt, and User Story Specification templates.
- [x] T018B [Plan:2.3] Align intake, lifecycle, agent, and training guidance with Product Owner specification acceptance and the separate readiness decision.
- [x] T018C [Plan:2.3] Validate cross-document links, terminology, source attribution, recording/AI-boundary controls, negative approval cases, and desktop/mobile training-page smoke paths.

### Phase 3: Reusable skill and orchestration layer

#### Plan 3.1 - Publish core skills (REQ-004, REQ-005)

- [x] T019 [P] [Plan:3.1] Publish intake and architecture skills under `skills/solution-intake/` and `skills/architecture-and-impact/`.
- [x] T020 [P] [Plan:3.1] Publish platform skills under `skills/power-apps-delivery/`, `skills/power-automate-delivery/`, and `skills/sharepoint-delivery/`.
- [x] T021 [P] [Plan:3.1] Publish QA, handoff, and retrospective skills under `skills/`.
- [x] T022 [Plan:3.1] Run controlled examples and version the first three skills after reviewer feedback. *(Intake, Power Apps delivery, and Power Automate delivery each ran on the Flossmoor pilot; see Phase 5A. Reviewer sign-off pending.)*

#### Plan 3.2 - Configure role-based agents (REQ-004, REQ-005, REQ-007)

- [x] T023 [P] [Plan:3.2] Publish `agents/delivery-orchestrator.md`.
- [x] T024 [P] [Plan:3.2] Publish `agents/qa-reviewer.md`.
- [x] T025 [P] [Plan:3.2] Publish `agents/foundry-validation-architecture.md`.
- [ ] T026 [Plan:3.2] Approve the Foundry models, identities, data boundary, tool allowlist, budget, traces, and kill switch.

### Phase 4: QA and validation system

#### Plan 4.1 - Implement the evidence-first QA framework (REQ-006, REQ-008)

- [x] T027 [P] [Plan:4.1] Publish `qa/qa-strategy.md` and `qa/evidence-schema.md`.
- [x] T028 [P] [Plan:4.1] Publish `qa/screenshot-plan.md` and `qa/screenshot-register.csv`.
- [x] T029 [Plan:4.1] Create synthetic personas, approved test data, and deterministic checks for the first vertical slice. *(QA workstream PR #10; Flossmoor pilot runs on synthetic data in Community Essentials.)*
- [x] T030 [Plan:4.1] Implement Playwright only for stable, approved journeys and retain traces/screenshots. *(Visual verification loop via shared browser, `standards/visual-verification.md`; evidence under `pilots/flossmoor-foia/evidence/visual/`.)*

#### Plan 4.2 - Add vision and bounded computer use (REQ-006, REQ-007)

- [ ] T031 [Plan:4.2] Implement screenshot normalization and an approved visual baseline process.
- [ ] T032 [Plan:4.2] Evaluate vision output against human-labeled examples and document false positives/negatives.
- [ ] T033 [Plan:4.2] Pilot computer use in a disposable non-production environment or document the approved fallback.
- [ ] T034 [Plan:4.2] Complete threat review and end-to-end evidence-store smoke test.

### Phase 5: Pilot one - ELM

#### Plan 5.1 - Complete ELM evidence and execute the standard (REQ-009, REQ-010, REQ-011)

- [ ] T035 [Plan:5.1] Confirm ELM app URL/ID, owners, connections, lists, flows, permissions, retention, licensing, and support without inference. *(Blocked: Pilot Gap Closure found app ID and owners not recorded; see `workstreams/evidence-gap-backlog.md`.)*
- [ ] T036 [Plan:5.1] Baseline a representative ELM activity in `metrics/baseline-and-outcomes.csv`.
- [ ] T037 [Plan:5.1] Execute one approved ELM change using the lifecycle and skills.
- [ ] T038 [Plan:5.1] Run the ELM critical regression, recovery, rollback, and evidence pack.
- [ ] T039 [Plan:5.1] Conduct successor walkthrough and independent regression.
- [ ] T040 [Plan:5.1] Retrospect and publish standard/skill version updates.

### Phase 5A: Live pilot - Flossmoor FOIA (new build)

Added 2026-10-17. ELM and Early Check are reconstruction pilots blocked on human confirmations; Flossmoor is a new client request that lets the standard run from intake forward with no dependency on missing facts. All work is in the Community Essentials dev environment on synthetic data. Branch `feature/flossmoor-foia-pilot`.

#### Plan 5A.1 - Intake and data layer (REQ-002, REQ-003, REQ-004)

- [x] T057 [Plan:5A.1] Run the intake skill on the real scope form, meeting transcript, and public website; record facts, implied requirements, unknowns, and routing decisions. *(`pilots/flossmoor-foia/`, intake standard v1.)*
- [x] T058 [Plan:5A.1] Design and provision the SharePoint data layer (Requests, Assignments, Departments, Records) with stable internal names. *(`sharepoint-schema.md`, `scripts/provision-flossmoor-foia-pilot.ps1`; provisioned manually after Graph write scope was denied.)*
- [x] T059 [Plan:5A.1] Extract the live connected schema from the saved app package for builders to use. *(`datasource-schema.md`.)*

#### Plan 5A.2 - Canvas app (REQ-003, REQ-004, REQ-005, REQ-006, REQ-008)

- [x] T060 [Plan:5A.2] Build v1 with components, Fluent tokens, AutoLayout; discover and record the Canvas MCP sync rules through visual verification. *(App `afe38862`; 15 sync rules in `standards/power-apps.md`.)*
- [x] T061 [Plan:5A.2] Fix silent save failure (required `OverallStatus`, `IfError` on all writes); publish and confirm a row lands.
- [x] T062 [Plan:5A.2] Diagnose Phone app type as the root cause of unreadable wide-screen and non-firing phone layouts; codify Tablet-type prerequisite and the adaptive layout tier matrix.
- [x] T063 [Plan:5A.2] Rebuild as v2 Tablet-type with `cmpRequestDetailPane`, desktop master-detail, stat strip, distribution bar, phone bottom nav; publish to dev. *(App `6ea0c73b`; desktop and phone tiers verified in `evidence/visual/`.)*
- [ ] T064 [Plan:5A.2] Confirm phone and tablet tiers on a real device or maker browser at 100% zoom; capture evidence; run App Checker and accessibility on v2.
- [ ] T065 [Plan:5A.2] End-to-end CRUD journey in v2 Player: create request → confirm due date → assignment save/complete → closeout; record results against the test plan.
- [ ] T066 [Plan:5A.2] Delete v1 (`afe38862`) after v2 acceptance; record rollback reference.

#### Plan 5A.3 - Public intake flow (REQ-003, REQ-004, REQ-005)

- [x] T067 [Plan:5A.3] Design the Survey123 → Power Automate → SharePoint intake flow: XLSForm schema, 47-action definition, routing, suggest-and-confirm due date, idempotency, attachments, receipts, error paths, 18-case test plan. *(`pilots/flossmoor-foia/flows/intake/`.)*
- [ ] T068 [Plan:5A.3] Build the Survey123 survey from `survey123-schema.md`; share publicly in the dev ArcGIS org.
- [ ] T069 [Plan:5A.3] Deploy the flow (MCP after `PA_TENANT_ID` restart, or maker portal per README); bind connection references; run PF-01…05 and TC-01…18.
- [ ] T070 [Plan:5A.3] Visual verification of designer and one run detail per `standards/visual-verification.md`.

#### Plan 5A.4 - Pilot close (REQ-009, REQ-010, REQ-011)

- [ ] T071 [Plan:5A.4] Record actual effort by phase in `metrics/baseline-and-outcomes.csv` (AI generation, review, rework, waiting, deployment) — this is the first realized measurement.
- [ ] T072 [Plan:5A.4] Second developer completes one bounded change in v2 using only the standard and skill; record assistance required.
- [ ] T073 [Plan:5A.4] Retrospective: promote rules from `evidence/STANDARD-CHANGE-CAPTURE.md` into versioned standard/skill releases; close the pilot with a sanitized case study.

### Phase 6: Pilot two - Glencoe Early Check

#### Plan 6.1 - Complete Early Check evidence and execute the standard (REQ-009, REQ-010, REQ-011)

- [ ] T041 [Plan:6.1] Confirm Forms URL, complete flow inventory, owners, connections, connector behavior, document metadata, records, licensing, and support.
- [ ] T042 [Plan:6.1] Baseline a representative Early Check activity in `metrics/baseline-and-outcomes.csv`.
- [ ] T043 [Plan:6.1] Execute an approved change covering approval, document, payment/completion, or connector behavior.
- [ ] T044 [Plan:6.1] Test wrong-department visibility, reject/reassign, duplicate, missing invoice, connector failure, PDF evidence, retention, permissions, accessibility, and rollback.
- [ ] T045 [Plan:6.1] Conduct successor walkthrough and independent regression.
- [ ] T046 [Plan:6.1] Retrospect and publish standard/skill version updates.

### Phase 7: Developer adoption, evidence, and publication

#### Plan 7.1 - Demonstrate independent team adoption (REQ-010)

- [ ] T047 [Plan:7.1] Deliver role-based training on lifecycle, skills, platform standards, QA, and handoff.
- [ ] T048 [Plan:7.1] Run an independent developer challenge without relying on the original developer.
- [ ] T049 [Plan:7.1] Record assistance required, unclear instructions, output consistency, defects, and participant feedback.

#### Plan 7.2 - Measure and communicate outcomes (REQ-011, REQ-012)

- [x] T050 [P] [Plan:7.2] Publish `portfolio/operational-evidence-matrix.md`.
- [x] T051 [P] [Plan:7.2] Publish `blog/blog-series-plan.md` and `blog/work-log-template.md`.
- [x] T052 [P] [Plan:7.2] Publish `visuals/process-diagrams.md`.
- [ ] T053 [Plan:7.2] Calculate before/after medians with sample size, range, exclusions, rework, review, and defects.
- [ ] T054 [Plan:7.2] Create sanitized case studies for ELM and Early Check.
- [ ] T055 [Plan:7.2] Complete privacy, client, accessibility, and publication review for every blog asset.
- [ ] T056 [Plan:7.2] Present operational evidence, residual risks, operating ownership, and the improvement backlog for sign-off.

## Project Structure

The root README links governance, standards, skills, agents, templates, QA, metrics, visuals, blog, portfolio, and immutable source material. New solution-specific evidence should be placed in approved project evidence locations and linked from this workspace rather than storing sensitive evidence in public artifacts.

## Requirement Mapping

| REQ ID | Description | Plan Items | Implementation Evidence |
|---|---|---|---|
| REQ-001 | Delivery charter and quality scorecard | P1.1 | `governance/power-desk-delivery-charter.md`, `governance/delivery-quality-scorecard.md` |
| REQ-002 | Common lifecycle | P2.1 | `standards/common-delivery-lifecycle.md` |
| REQ-003 | Platform standards | P2.1, P5A.2, P5A.3 | `standards/power-apps.md`, `standards/power-automate.md`, `standards/sharepoint.md`, `standards/integrated-solutions.md`, `standards/visual-verification.md`, `standards/intake-and-triage.md` |
| REQ-004 | Skills, instructions, templates, agents | P2.2, P3.1, P3.2, P5A.1 | `skills/`, `templates/`, `agents/` |
| REQ-005 | MCP as bounded tool layer | P3.1, P3.2, P5A.2, P5A.3 | Platform skills, orchestrator routing, Canvas MCP sync rules |
| REQ-006 | Multi-lane QA | P4.1, P4.2, P5A.2 | `qa/qa-strategy.md`, `standards/visual-verification.md`, validation runs |
| REQ-007 | Safe Foundry validation | P3.2, P4.2 | `agents/foundry-validation-architecture.md`, threat review |
| REQ-008 | Traceability and screenshots | P1.1, P2.2, P4.1, P5A.2 | `qa/evidence-schema.md`, test and screenshot registers, `pilots/flossmoor-foia/evidence/` |
| REQ-009 | ELM and Early Check pilots; Flossmoor live pilot | P5.1, P6.1, P5A | Pilot inventories, regression packs, evidence |
| REQ-010 | Independent reuse | P5.1, P6.1, P5A.4, P7.1 | Successor observations, challenge results |
| REQ-011 | Measured improvement | P5.1, P6.1, P5A.4, P7.2 | `metrics/baseline-and-outcomes.csv`, analysis |
| REQ-012 | Portfolio and blog | P7.2 | `portfolio/`, `blog/`, sanitized case studies |
| REQ-013 | Governance and controls | P1.1, P2.1, P2.2 | Charter, standards, decisions, release evidence |
| REQ-014 | Preserve sources | P1.2 | `source-material/copilot-package/`, source register |
