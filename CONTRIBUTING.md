# Contributing

This repository is a standards and delivery operating system for AI-assisted Microsoft 365 and Power Platform delivery.

## Contribution model

- Work in a feature branch for your assigned workstream.
- Keep changes within the designated scope.
- Preserve versioned standards, evidence, and traceability.
- Never change production access, retention, or data-handling rules without governance approval.

## Required before merge

- The branch is based on the latest `main`.
- The change has a clear owner.
- The change is traceable to a requirement or backlog item.
- The relevant validation passes.
- The change does not break the repo architecture or standards.

## Workstream directories

- `standards/` for lifecycle and platform standards
- `skills/` for reusable procedures
- `agents/` for orchestration and QA guidance
- `templates/` for reusable deliverables
- `qa/` for validation and evidence plans
- `portfolio/` for proof and case studies
- `blog/` for public-safe content
- `metrics/` for measured outcomes
- `workstreams/` for branch-owned workstream artifacts

## Agent etiquette

- Do not edit another agent's branch without explicit assignment.
- Do not merge to `main` without review.
- If a standard changes, update the relevant artifacts and downstream templates together.
- If you discover an unknown, do not infer; document it.
