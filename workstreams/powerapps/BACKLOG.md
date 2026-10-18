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

## Elevated UI/UX refinement (2026-10-17, after pilot review)

Driver: v2 was functional and responsive but visually below the two internal reference apps (Team Onboarding / ELM; Early Check Request). Their DOM was inspected in the shared browser and the design language codified.

- [x] `skills/power-apps-delivery/references/design-system.md` created: principles, `App.Formulas` token set, screen skeleton, 11-component catalog with contracts, 8 signature patterns with YAML, motion/feedback, accessibility, Elevated-UI acceptance checklist (§8), reference-evidence plan.
- [x] Skill procedure updated — Specify step requires a per-screen pattern map; Edit step orders tokens → components → screens; Check step runs the §8 checklist against screenshots; both checklists and Required outputs extended.
- [x] `standards/power-apps.md` — Design quality bar added under Responsive and accessible UI; tier-matrix acceptance now includes §8.
- [x] Toast captured from the Early Check "Fluent 2 Toast" component — real YAML stored at `skills/power-apps-delivery/references/toast-component.pa.yaml` (Action `SendToast`, variable-height gallery, per-row timer, progress/time options, cap 4) → design-system §5.9 with contract, App.OnStart setup, instance, call sites, intent table; made the **default notification surface** in the standard's Error/notification pattern (`Notify()` demoted to debug only).
- [ ] Capture sanitized reference screenshots (desktop/tablet/phone × home, detail, form w/ validation, empty state) for both reference apps into `visuals/power-apps/reference/` (T0xx — needs the Studio tab shared).
- [x] Re-apply the design system to FOIA App v2 → **YAML complete and compile-clean** (`pilots/flossmoor-foia/canvas-app-v3/`, plan at `canvas-app-v3-plan.md`): tokens + OnStart, 4 new components (`cmpToast`, `cmpMetricTile`, `cmpEmptyState`, `cmpPhoneNav`), 3 retokenised components, all 5 screens (accent-bar rows, section cards, stepper, master-detail, 18 `SendToast` call sites, zero user-facing `Notify()`). 0 errors; 172 pre-existing delegation warnings; App Checker 1 pre-existing unused variable.
- [ ] **Blocked — live sync.** Pushes to v2 landed in a headless session (unsaveable); pushes to a fresh "FOIA App v3" were echoed back unchanged by the server even after an MCP restart and fresh Studio tab. Rules 16–20 added to `standards/power-apps.md`. Next: retry probe on a fresh day/session; if still failing, Studio-side route (paste screen YAML into Studio; recreate components via Studio import) or packaged-app import.
- [x] **Live and published in FOIA App v3** (`4d206985-b66f-4f93-91fd-746b098cc7bd`). Root cause of the earlier sync failures: zombie coauthoring sessions from multiple Studio tabs; fixed with one fresh tab + new-control probe (rules 21–22). Full 16-file sync applied; Studio needed one reload. Visual QA at desktop found and fixed: tile overflow (rule 23), 0-height captions/filters (rule 24), invalid `DocumentSearch` icon ×7 (rule 25). Desktop Home, master-detail, and NewRequest verified by screenshot.
- [x] Added the missing request-to-department workflow: when a request has no active assignments, the detail action now opens an **Assign department** modal; staff select an unassigned active department, and the host creates a `New` assignment inheriting the request working due date before opening Department Work. The Assignments tab also supports adding more departments and explains the empty state. Compiles with zero errors; App Checker retains one pre-existing unused-variable performance note.
- [x] Elevated the Request Details pane from a flat field grid to a Fluent record view: raised record header, semantic section bands, compact three-column desktop grid, narrative/stage-note cards, and distinct extension-review treatment. Corrected padding-aware AutoLayout widths and title baseline clipping; compiled with zero errors, visually verified in Studio, saved, and published.
- [x] Refined the Request Details pane for common laptop canvases: replaced `App.Width`-only decisions with component-width breakpoints, prevented fixed header actions/status from overflowing, introduced pane-aware compact actions, and used a mixed-density requester/logistics grid. Verified without clipping at 1332×749 and 1280×720, compiled with zero errors, saved, and published.
- [x] Completed all Request Details tabs and whole-page visual QA: Assignments now has an elevated heading/action surface and designed empty state; Activity was moved out of the hidden modal hierarchy and rebuilt as an ordered, scrollable five-event timeline. Removed UTF-8 artifacts, verified Summary/Assignments/Activity in the 1280×720 whole-page context, compiled with zero errors, saved, and published.
- [ ] Revalidate the published assignment modal and SharePoint write in Player after the refreshed session completes its connection/consent load. Also open: phone/tablet Player tiers and end-to-end toast coverage.
- [x] Icon catalog (181 names) scraped from Studio → `skills/power-apps-delivery/references/icon-catalog.md`, wired into the skill's Check step.
- [ ] Capture §8 evidence at three tiers once the app renders.
- [ ] Power Automate intake flow (Microsoft Forms internal / Survey123 external-with-attachments → FOIA Pilot Requests) as a parallel agent task under `power-automate-delivery`.

## PR handoff

- **Shared-file proposal (not applied):** Ask the program owner to update `plan.md` so REQ-003 and REQ-009 explicitly point to this Power Apps standard, delivery skill, and backlog as workstream outputs. Keep ELM inventory, execution, and evidence tasks open until an authorized owner supplies the missing facts and approvals.
- **Governance:** No governance files were changed; no governance change is required to complete this workstream documentation.
- **Unresolved assumptions:** ELM app identity, owner, environment, version, data sources, connector behavior, permissions, licensing, test identities, representative volume, Canvas MCP capabilities/authorization, and release/rollback process remain to be confirmed by authorized owners. This documentation does not claim an ELM pilot was executed.
