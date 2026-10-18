# Repository Architecture

## Purpose

This repository is designed to support parallel AI and developer work without creating unmaintainable drift. It is structured so each workstream owns a bounded domain and merges into a single source of truth.

## Top-level structure

```text
.
├── README.md
├── requirements.md
├── plan.md
├── AGENT_WORKFLOW.md
├── BRANCHING.md
├── CONTRIBUTING.md
├── .gitignore
├── governance/
│   ├── power-desk-delivery-charter.md
│   ├── delivery-quality-scorecard.md
│   └── operating-model.md
├── standards/
│   ├── common-delivery-lifecycle.md
│   ├── power-apps.md
│   ├── power-automate.md
│   ├── sharepoint.md
│   └── integrated-solutions.md
├── skills/
│   ├── solution-intake/
│   ├── architecture-and-impact/
│   ├── power-apps-delivery/
│   ├── power-automate-delivery/
│   ├── sharepoint-delivery/
│   ├── independent-qa/
│   ├── documentation-handoff/
│   └── retrospective-pattern-extraction/
├── agents/
│   ├── delivery-orchestrator.md
│   ├── qa-reviewer.md
│   └── foundry-validation-architecture.md
├── templates/
│   ├── solution-intake.md
│   ├── architecture-decision.md
│   ├── test-case.md
│   ├── release-checklist.md
│   └── handoff-checklist.md
├── qa/
│   ├── qa-strategy.md
│   ├── evidence-schema.md
│   ├── screenshot-plan.md
│   ├── screenshot-register.csv
│   └── ...
├── metrics/
│   └── baseline-and-outcomes.csv
├── portfolio/
│   └── operational-evidence-matrix.md
├── blog/
│   ├── blog-series-plan.md
│   ├── work-log-template.md
│   └── ...
├── workstreams/
│   ├── powerapps/
│   ├── powerautomate/
│   ├── sharepoint/
│   ├── qa/
│   └── portfolio/
├── docs/
│   └── architecture/
│       └── REPO_ARCHITECTURE.md
├── source-material/
│   └── copilot-package/
├── checkpoints/
│   ├── spec-to-plan.yaml
│   └── plan-to-tasks.yaml
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
└── .gitignore
```

## Design principles

1. One source of truth: `main` is the canonical program baseline.
2. Parallel worktracks: each workstream owns an explicit directory and branch.
3. Reasoned handoffs: dependencies are communicated, not assumed.
4. Evidence-first: every change includes validation and traceability.
5. Human approval: no automated deployment or production change without a named person.
6. Future-proofing: add new workstreams as bounded areas rather than expanding the shared root files.

## Recommended agent ownership

- Program owner: shared governance and cross-cutting change control
- Power Apps workstream: standards and templates for app backlogs and UX patterns
- Power Automate workstream: flow design, telemetry, failure-handling, recovery patterns
- SharePoint workstream: list/library/page governance and information architecture
- QA/workflow validation: test harness, evidence schema, screenshot capture, Playwright/Foundry validation
- Evidence/blog workstream: operational evidence, metrics, public-safe articles, and reusable case studies

## Merge workflow

The repo is designed for this flow:

- Agent branch is created from `main`
- Agent works within a workstream folder
- Validation occurs locally and in CI if later added
- Agent opens PR
- Owner reviews and approves if criteria are met
- Merge into `main`
- Downstream workstreams rebase or update from `main`

This preserves governance while still allowing parallel execution.

## Future-proofing

As the team grows, this structure can expand by adding:

- `deployment/` for environment and release packaging
- `security/` for DLP, policy, and records controls
- `playbooks/` for onboarding and standard operating procedures
- `templates/automation/` for reusable prompter and pipeline assets
- `examples/` for sanitized client scenarios

Do not let these be added as ad hoc root folders. Keep them under owned workstreams or domain areas.
