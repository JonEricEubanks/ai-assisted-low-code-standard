# AI-Assisted Low-Code Delivery Standard

This workspace provides the Power Desk with a governed, reusable AI-assisted delivery system for Power Apps, Power Automate, SharePoint, and related Microsoft 365 solutions. It is designed for new-hire onboarding and day-to-day use by current developers.

## Start here

For a new CSM handoff:

1. Install VS Code and Git. Ask IT to install Azure CLI when administrator rights are required.
2. Clone this repository, open it as the active VS Code workspace, and install the extensions listed in `.vscode/extensions.json`.
3. Run `.\scripts\Test-DeveloperSetup.ps1`.
4. Open GitHub Copilot Chat and select **MGP Delivery**.
5. Provide the approved SharePoint project-folder URL.
6. Complete initial intake triage and identify the questions that require stakeholder discovery.
7. Use the governed discovery script with an approved recording/transcription tool and data boundary.
8. Generate a draft User Story Specification from the attributed transcript; do not invent missing facts.
9. Have the Product Owner confirm that the specification accurately captures the need, scope, stories, and acceptance criteria.
10. Complete developer triage, risk classification, and the readiness decision.
11. Obtain explicit approval before architecture or implementation.

The repository includes a standard discovery-to-user-story workflow:

- [Discovery Script](templates/discovery-script.md)
- [Discovery-to-User-Story Prompt](templates/discovery-to-user-story-prompt.md)
- [User Story Specification](templates/user-story-specification.md)
- [Solution Intake](templates/solution-intake.md)

The workflow converts stakeholder conversations into a reviewed specification while preserving source attribution, assumptions, dependencies, and open questions. Product Owner acceptance confirms specification accuracy; it does not authorize architecture, implementation, release, or production changes. Product Owner specification acceptance is not architecture, build, or release approval. Ready plus accountable developer approval opens architecture—not build or release.

The active Copilot customizations are under `.github/agents/`, `.github/skills/`, and `.github/copilot-instructions.md`. The governed source procedures remain under `agents/` and `skills/`.

### What each person provides

- **This repository provides:** the MGP Delivery agent, instructions, skills, prompts, standards, templates, and the setup checker.
- **The developer installs:** the extensions recommended in `.vscode/extensions.json` — GitHub Copilot Chat and Microsoft Power Platform Tools.
- **IT or the device administrator installs when required:** Azure CLI. The installer may require local administrator rights.
- **IT or the platform owner provisions:** the approved SharePoint/Microsoft 365 MCP connection, authentication, tenant consent, and permissions. Request access through the standard IT service channel.
- **The CSM provides:** the authorized SharePoint project-folder link and complete handoff documents.

Do not download arbitrary MCP servers or store tenant credentials in this repository. A SharePoint URL only identifies the CSM handoff; the selected MCP tool must already be authenticated and authorized before intake can begin.

For repository orientation:

1. Read [the Power Desk delivery charter](governance/power-desk-delivery-charter.md).
2. Review [the implementation plan](plan.md).
3. Use [the common delivery lifecycle](standards/common-delivery-lifecycle.md).
4. Select the applicable platform standard under `standards/`.
5. Capture validation and operational evidence using `qa/`, `metrics/`, and `portfolio/`.
6. For parallel work, follow [the branching model](BRANCHING.md) and [agent assignment matrix](docs/architecture/AGENT_ASSIGNMENT_MATRIX.md).

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
| `templates/` | Reusable discovery, intake, architecture, and handoff artifacts |
| `qa/` | QA strategy, evidence schema, and screenshot process |
| `blog/` | Public-safe documentation plan |
| `portfolio/` | Operational evidence and reusable case-study structure |
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
- [Sanitized evidence boundary](governance/evidence-boundary.md)
- [Evidence gap backlog](workstreams/evidence-gap-backlog.md)
- [Skill priority register](skills/PRIORITY_REGISTER.md)
- [Pilot readiness gates](workstreams/pilots/READINESS.md)

Internal source material is intentionally excluded from GitHub. Store it locally or in an approved MGP evidence repository and reference it by evidence ID.

## Local repository explorer

The repository includes a local-only explorer at [docs/admin/index.html](docs/admin/index.html). It provides a searchable, categorized quick view of skills, instructions, agents, standards, templates, QA, governance, architecture, and training resources. Select a resource to switch between a readable preview and its Markdown source.

The explorer's **Edit with Copilot** and **Suggest a change** actions create a governed, file-specific prompt for GitHub Copilot Chat. They do not overwrite repository files from the browser. Copy the generated prompt, return to VS Code with **MGP Delivery** selected, and paste it into Copilot Chat. Owner prompts request a bounded local edit; contributor prompts preserve the feature-branch and pull-request workflow.

Run `.\scripts\Build-AdminCatalog.ps1` after adding or removing repository resources so the explorer catalog stays current. The explorer reads the repository source directly and does not provide an in-browser editing surface. Changes still go through VS Code, a branch, validation, and pull-request review.

## Initial pilots

- Glencoe ELM
- Glencoe Early Check

Unknown URLs, owners, connections, licensing decisions, retention decisions, and technical details must be recorded as open items rather than inferred.
