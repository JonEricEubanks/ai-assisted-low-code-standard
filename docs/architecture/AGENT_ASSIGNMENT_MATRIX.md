# Agent Assignment Matrix

## Assignment principles

- Each agent receives one bounded workstream and one branch.
- Shared governance files are owned by the program orchestrator.
- Agents communicate dependencies through issues and PRs, not direct cross-branch edits.
- A workstream agent may propose a shared-file change in its handoff notes; the orchestrator applies it.

## Workstream assignments

| Agent role | Branch | Owned paths | Initial objective | Depends on |
|---|---|---|---|---|
| Program orchestrator | `feature/governance-control` | `governance/`, root plans, `.github/` | Confirm charter, owners, rubric, controls, and gate status | Manager and control owners |
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

Platform branches may proceed in parallel after they consume the same approved governance baseline.

## Handoff contract

Every agent must report:

- issue and branch
- scope completed
- exact paths changed
- validation performed
- evidence used
- assumptions and unknowns
- downstream dependencies
- proposed shared-file changes
- risks requiring human decision
