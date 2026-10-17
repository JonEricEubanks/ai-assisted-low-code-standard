# AI-Assisted Low-Code Delivery Standard

This workspace operationalizes the Q4 2026 goal to create a governed, reusable AI-assisted delivery system for Power Apps, Power Automate, SharePoint, and related Microsoft 365 solutions.

## Start here

1. Read [the goal charter](governance/goal-charter.md).
2. Review [the implementation plan](plan.md).
3. Use [the common delivery lifecycle](standards/common-delivery-lifecycle.md).
4. Select the applicable platform standard under `standards/`.
5. Invoke the applicable procedure under `skills/`.
6. Use the templates under `templates/`.
7. Capture validation and portfolio proof using `qa/`, `metrics/`, and `portfolio/`.
8. For parallel work, follow [the branching model](BRANCHING.md) and [agent assignment matrix](docs/architecture/AGENT_ASSIGNMENT_MATRIX.md).

## Operating principle

- Instructions define universal constraints.
- Skills define repeatable procedures.
- MCP tools perform bounded platform actions.
- Agents coordinate roles and decisions.
- Deterministic tests and accountable people authorize release.

No agent may autonomously mutate production, change access, delete content, make retention decisions, or communicate externally.

## Repository map

| Area | Purpose |
|---|---|
| `governance/` | Goal, scorecard, roles, controls, and decisions |
| `standards/` | Common and platform-specific delivery standards |
| `skills/` | Reusable agent procedures |
| `agents/` | Orchestrator and reviewer instructions |
| `templates/` | Immediately reusable delivery artifacts |
| `qa/` | QA strategy, evidence schema, and screenshot process |
| `blog/` | Public-safe documentation plan |
| `portfolio/` | Promotion evidence and case-study structure |
| `metrics/` | Baseline and outcome measurement |
| `visuals/` | Editable Mermaid diagram sources |
| `source-material/` | Original Copilot package retained unchanged |

## Collaboration

- [Repository architecture](docs/architecture/REPO_ARCHITECTURE.md)
- [Branching and merge model](BRANCHING.md)
- [Agent workflow](AGENT_WORKFLOW.md)
- [Agent assignment matrix](docs/architecture/AGENT_ASSIGNMENT_MATRIX.md)
- [Scaling guide](docs/architecture/SCALING_GUIDE.md)
- [Contribution rules](CONTRIBUTING.md)
- [Repository controls and hosting limitation](governance/repository-controls.md)

Internal source material is intentionally excluded from GitHub. Store it locally or in an approved MGP evidence repository and reference it by evidence ID.

## Initial pilots

- Glencoe ELM
- Glencoe Early Check

Unknown URLs, owners, connections, licensing decisions, retention decisions, and technical details must be recorded as open items rather than inferred.
