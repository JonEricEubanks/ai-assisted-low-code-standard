# Agent Assignment Matrix

## Assignment principles

- Each agent receives one bounded workstream and one branch.
- Shared governance files are owned by the program orchestrator.
- Agents communicate dependencies through issues and PRs, not direct cross-branch edits.
- A workstream agent may propose a shared-file change in its handoff notes; the orchestrator applies it.
- Before architecture, routing follows qualification/intake, approved discovery artifacts, Product Owner specification-accuracy validation, developer/agent governed triage, and accountable readiness approval.
- Product Owner specification acceptance is not architecture, build, or release approval.

## Workstream assignments

| Agent role | Branch | Owned paths | Initial objective | Depends on |
|---|---|---|---|---|
| Program orchestrator | `feature/governance-control` | `governance/`, root plans, `.github/` | Confirm charter, owners, discovery controls, accountable readiness, rubric, and gate status | Manager and control owners |
| Discovery facilitator | Assigned discovery branch | Approved discovery artifacts | Capture source-attributed discovery within approved recording, transcription, and AI boundaries; separate facts, implied requirements, assumptions, unknowns, and blockers; assign stable requirement, story, and acceptance-criterion IDs | Qualified intake and discovery approvals |
| Product Owner | Approval record; no implementation ownership | Discovery specification validation | Validate that the specification accurately reflects the intended need without approving architecture, build, or release | Completed discovery artifacts |
| Triage developer / agent | Assigned intake branch | Triage record and solution brief | Complete governed triage, preserve stable IDs and unresolved blockers, and propose the readiness disposition | Product Owner specification-accuracy validation |
| Accountable readiness approver | Approval record; no implementation ownership | Readiness decision | Approve or reject progression of a `Ready` triage baseline to architecture | Completed governed triage |
| Power Apps specialist | `feature/powerapps-standard` | Power Apps standard, skill, workstream | Build reusable design, formula, accessibility, and QA patterns | Governance baseline |
| Power Automate specialist | `feature/powerautomate-standard` | Flow standard, skill, workstream | Build lifecycle, resilience, telemetry, and recovery patterns | Governance baseline |
| SharePoint specialist | `feature/sharepoint-standard` | SharePoint standard, skill, workstream | Build list, library, page, permissions, and records patterns | Governance baseline |
| QA automation specialist | `feature/qa-validation` | `qa/`, QA skill, QA workstream | Implement evidence schema and deterministic vertical slice | Platform test cases |
| Foundry validation specialist | `feature/foundry-validation` | Foundry architecture and QA extensions | Design vision/computer-use evaluation after deterministic QA | QA baseline and approvals |
| Metrics analyst | `feature/metrics-evidence` | `metrics/`, analysis outputs | Define baseline, sample, calculations, and reporting | Pilot task definitions |
| Portfolio/blog specialist | `feature/portfolio-blog` | `portfolio/`, `blog/` | Create public-safe case-study and publication system | Sanitized pilot evidence |

## Merge order

1. Governance and controls
2. Platform workstreams in parallel
3. QA deterministic foundation
4. Metrics baseline
5. Foundry visual and computer-use evaluation
6. Portfolio and blog publication

Platform branches may proceed in parallel after they consume the same approved governance baseline. No platform workstream begins architecture or implementation from Product Owner specification acceptance alone.

## Handoff contract

Every agent must report:

- issue and branch
- scope completed
- exact paths changed
- validation performed
- evidence used with source attribution
- confirmed facts, implied requirements, assumptions, and unknowns kept separate
- stable requirement, story, and acceptance-criterion IDs
- unresolved blockers
- approved recording, transcription, and AI-use boundary when discovery occurred
- downstream dependencies
- proposed shared-file changes
- risks requiring human decision
