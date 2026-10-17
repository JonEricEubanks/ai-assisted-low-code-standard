# Power Apps Workstream Backlog

## Branch

`feature/powerapps-standard`

## Initial tasks

- [x] Define the app specification fields for personas, journeys, screens, states, data contracts, and responsive targets in `standards/power-apps.md`.
- [x] Define Power Fx naming, state, error/notification, and reusable component patterns with inputs, constraints, outputs, and validation in `standards/power-apps.md`.
- [x] Define delegation and representative-volume review procedures in `standards/power-apps.md`.
- [x] Define App Checker, accessibility, keyboard, and evidence acceptance in `standards/power-apps.md`.
- [x] Add generic, synthetic acceptance examples for loading, empty, validation, permission-denied, error, and success states in `standards/power-apps.md`.
- [x] Build an approval-gated Canvas MCP edit-plan and validation workflow in `skills/power-apps-delivery/SKILL.md`.
- [x] Define ELM discovery questions that record unknowns rather than inferring app, data, permission, or ownership facts in `skills/power-apps-delivery/SKILL.md`.

## Validation

- `python scripts/validate_repo.py` — passed; includes skill frontmatter and Markdown link validation.
- `git diff --check` — passed.
- Reviewed the Power Fx/component pattern table for inputs, constraints, outputs, and validation; reviewed state examples and ELM questions for synthetic content and explicit unknowns.
- Changes are standards and procedure documentation only; no production mutation or client-sensitive example/data is included.

## Definition of done

Another developer can use the standard and skill to plan, build, self-review, and hand off one bounded Canvas app change.

## PR handoff

- **Shared-file proposal (not applied):** Ask the program owner to update `plan.md` so REQ-003 and REQ-009 explicitly point to this Power Apps standard, delivery skill, and backlog as workstream outputs. Keep ELM inventory, execution, and evidence tasks open until an authorized owner supplies the missing facts and approvals.
- **Governance:** No governance files were changed; no governance change is required to complete this workstream documentation.
- **Unresolved assumptions:** ELM app identity, owner, environment, version, data sources, connector behavior, permissions, licensing, test identities, representative volume, Canvas MCP capabilities/authorization, and release/rollback process remain to be confirmed by authorized owners. This documentation does not claim an ELM pilot was executed.
