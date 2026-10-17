# Branching and Parallel Agent Operating Model

## Core rule

One branch = one workstream.
One workstream = one owner.
One PR = one approval gate.

## Protected default branch

- `main` is the protected branch.
- No agent writes directly to `main`.
- `main` represents the approved standard, not the working draft.

## Branch naming

Use this naming pattern:

- `feature/powerapps-standard`
- `feature/powerautomate-standard`
- `feature/sharepoint-standard`
- `feature/qa-validation`
- `feature/foundry-validation`
- `feature/portfolio-blog`
- `feature/metrics-evidence`
- `feature/governance-control`
- `fix/issue-###`

## Workstream ownership map

| Workstream | Owner | Main files |
|---|---|---|
| powerapps | Power Apps lead | `standards/power-apps.md`, `workstreams/powerapps/` |
| powerautomate | Automation lead | `standards/power-automate.md`, `workstreams/powerautomate/` |
| sharepoint | SharePoint lead | `standards/sharepoint.md`, `workstreams/sharepoint/` |
| qa | QA lead | `qa/`, `workstreams/qa/` |
| portfolio | Portfolio lead | `portfolio/`, `blog/`, `workstreams/portfolio/` |
| config/governance | Program owner | `governance/`, `README.md`, `plan.md` |

See `docs/architecture/AGENT_ASSIGNMENT_MATRIX.md` for complete role and dependency assignments.

## Merge rules

- Branches may only merge into `main` via PR.
- Every PR needs review by either the program owner or designated workstream owner.
- PRs must include evidence of validation and a short summary of changes.
- Merge only if there are no conflicting changes in the same file.
- Merge only if requirements and traceability remain consistent.

## Conflict prevention

- Do not let multiple agents edit the same file in parallel.
- Shared files like `README.md`, `plan.md`, `requirements.md`, and governance files must be edited by the orchestrator or designated owner only.
- Workstreams own separate directories or clearly scoped files.
- If a file is shared across multiple workstreams, assign one owner and require a handoff.

## Handoff procedure

When one workstream depends on another:

1. Open a PR in the upstream branch.
2. Mark the downstream branch as waiting on that work.
3. The downstream branch must point to the approved merged version.
4. Do not merge partial dependencies silently.

## Recovery procedure

If an agent branch gets stale or conflicting:

1. Rebase or cherry-pick from `main`.
2. Resolve conflicts in the owning file only.
3. Re-run validation.
4. Recreate a clean PR.

## PR template requirement

Each PR should contain:

- Workstream name
- Scope and file list
- Validation performed
- Evidence references
- Risks and open unknowns
- What is ready for downstream handoff
