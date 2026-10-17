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

## Applied on the Flossmoor pilot (2026-10-17)

- [x] Standard and skill exercised end-to-end on a new Tablet-type app (`pilots/flossmoor-foia/canvas-app-v2/`).
- [x] Responsive requirement hardened: Tablet app-type prerequisite, inlined `App.Width` checks, adaptive layout tier matrix (phone bottom nav → tablet rail → desktop master-detail).
- [x] Component requirement proven: four components incl. `cmpRequestDetailPane` reused across screens; verified instance syntax recorded.
- [x] Visual verification loop added and used; found black-box corruption, placeholder images, button wrapping, silent save failure — none visible to compile or App Checker.
- [x] Fifteen Canvas MCP sync/platform rules recorded in `standards/power-apps.md`.
- [x] Write-path rules added: required columns set/defaulted and gated; every write in `IfError`.
- [ ] Reviewer sign-off on the updated standard (T022).
- [ ] Second-developer bounded change on v2 (T072) — the Definition of done test.

Trace of every request to its rule: `pilots/flossmoor-foia/evidence/STANDARD-CHANGE-CAPTURE.md`.

## PR handoff

- **Shared-file proposal (not applied):** Ask the program owner to update `plan.md` so REQ-003 and REQ-009 explicitly point to this Power Apps standard, delivery skill, and backlog as workstream outputs. Keep ELM inventory, execution, and evidence tasks open until an authorized owner supplies the missing facts and approvals.
- **Governance:** No governance files were changed; no governance change is required to complete this workstream documentation.
- **Unresolved assumptions:** ELM app identity, owner, environment, version, data sources, connector behavior, permissions, licensing, test identities, representative volume, Canvas MCP capabilities/authorization, and release/rollback process remain to be confirmed by authorized owners. This documentation does not claim an ELM pilot was executed.
