# Power Apps Delivery Standard

This standard applies to Canvas app planning, bounded changes, validation, and handoff. Treat missing app, data, environment, and ownership facts as unknowns; do not fill gaps with assumptions.

## App specification

Record the following before implementation. Link each acceptance criterion to a requirement and test ID.

| Area | Required specification |
|---|---|
| Outcome and people | Business outcome, named owner, personas, roles, and permission boundaries |
| Journeys | Start and end conditions, primary and exception paths, expected results, and acceptance criteria |
| Screens | Screen purpose, navigation, controls, empty/loading/error/success states, and accessibility labels |
| Responsive targets | Supported device classes, orientation, minimum usable viewport, and layout behavior |
| Data and integrations | Source of truth, connectors, operations, identity, permissions, expected volume/growth, delegation constraints, and offline requirement |
| Delivery | App/environment/version, dependencies, licensing, telemetry, support owner, and rollback reference |

An unknown or unapproved item is listed with an owner and the decision needed. Do not begin a change that depends on an unresolved security, data ownership, or production-access decision.

## Power Fx and component patterns

Use semantic names and one consistent naming scheme. The prefixes below are the standard for this workstream; add a clear purpose after the prefix and avoid default names such as `Button1`.

| Artifact | Prefix | Example |
|---|---|---|
| Screen / container | `scr` / `cnt` | `scrRequestDetails`, `cntRequestHeader` |
| Label / button / input | `lbl` / `btn` / `txt` | `lblRequestStatus`, `btnSaveRequest`, `txtRequestTitle` |
| Combo box / gallery / form | `cmb` / `gal` / `frm` | `cmbOwner`, `galRequests`, `frmRequest` |
| Icon / component | `ico` / `cmp` | `icoRefresh`, `cmpStatusBadge` |
| Context / global variable | `loc` / `gbl` | `locIsSaving`, `gblCurrentUser` |
| Collection | `col` | `colVisibleRequests` |

Names must communicate purpose, not implementation order. Keep formulas short enough to review; extract repeated or non-obvious logic into a named formula, component, or documented behavior where supported.

| Pattern | Inputs | Constraints | Outputs | Validation |
|---|---|---|---|---|
| Screen state | Explicit navigation parameters and state owned by the screen | Keep transient state local; use app-wide state only when multiple screens need it; initialize and reset deliberately | Predictable screen and control properties | Navigate in and out repeatedly; verify no stale selection or unintended state |
| Data operation | Validated form values, target source, and operation | Check required fields and permissions before writing; do not rely on UI visibility as authorization | Confirmed saved result or surfaced failure | Test valid, invalid, duplicate, denied, and failed-connector cases |
| Error and notification | Operation result, safe user-facing message, and diagnostic context | Never expose secrets or raw sensitive data; do not report success after failure; preserve recoverable user input | Accessible progress, success, or error feedback | Force success and failure paths; confirm feedback, retry behavior, and retained input |
| Reusable component | Declared input properties, output/event properties, and accessibility name | No undocumented dependencies on global state; use only when reuse or consistency justifies the boundary | Consistent reusable UI or behavior | Test component inputs, outputs, keyboard access, and each consuming screen |

Use app-level state only for values genuinely shared across screens. Prefer declarative control properties over duplicating state. A component must expose its contract and must not silently perform writes or bypass the parent screen's permission and error handling.

## Responsive and accessible UI

- Desktop, tablet, and phone are the default supported device classes unless the approved specification explicitly narrows the target. Record the approved minimum widths and orientation.
- Use phone `< 600`, tablet `600-1199`, and desktop `>= 1200` as the default breakpoint contract. Centralize breakpoint, spacing, color, typography, and minimum-touch-target values as app named formulas rather than repeating literals.
- Use AutoLayout containers, `Parent.Width`/`Parent.Height`, `FillPortions`, `LayoutMinWidth`, `LayoutWrap`, `Min`, `Max`, and breakpoint formulas. Fixed coordinates or viewport-sized widths require a documented exception.
- Phone layouts are single-column with touch targets of at least 44 pixels. Tablet layouts wrap or use bounded two-column groups. Desktop layouts may use multi-column content and persistent navigation.
- Set text controls to `AutoHeight` when content can wrap or vary. Give AutoLayout children a small, intentional `LayoutMinHeight`; do not clip long labels, localized text, validation messages, or record content.
- Build shared headers, navigation, sidebars, footers, status treatments, and other repeated shell elements as Canvas components with explicit input/output/event contracts. Do not copy the same shell controls across screens without a documented tool or platform limitation.
- Prefer modern Fluent controls, Segoe UI, neutral surfaces, accessible semantic colors, and consistent spacing/type tokens. Color is never the only status cue.
- Keep navigation, labels, focus order, keyboard operation, contrast, and non-color status cues usable at each supported size.
- Every actionable control has a clear accessible name and purpose; do not use placeholder text as the only label.
- Record accessibility findings and disposition. A clean automated check does not replace keyboard and assistive-technology review where required.

### Reusable component contract

For every shared Canvas component, record:

- purpose and consuming screens
- input, output, and event properties with types and defaults
- app-scope dependencies and whether they are justified
- width, height, and breakpoint behavior
- accessible name, focus behavior, and keyboard interaction
- independent component test plus one test on every consuming device class

Before source-based component editing, run the authoring service's execution assessment and compile a minimal component definition and instance. If the service rejects `ComponentDefinitions` or `Control: Component`, stop the component edit and record the exact diagnostic. Use Power Apps Studio or an approved component library workflow; do not replace the requested component with duplicated controls and claim compliance.

## Data and delegation review

For each data-bound screen and operation, record the source/connector, query or formula, expected and growth volume, delegation warnings or limits, and the behavior if the source is unavailable.

1. Review delegation indicators and the connector's supported delegation behavior for every filter, sort, search, and aggregate used on a growing source.
2. Do not treat a client row limit or a small development dataset as evidence of correctness. If an operation is nondelegable, either redesign it, establish and approve a safe bounded dataset, or block the change.
3. Test with representative synthetic volume and records placed beyond any client-side retrieval limit. Compare displayed/search results with the expected source results.
4. Use available monitoring/diagnostics to inspect requests and failures. Record the tested volume, environment, result, and any approved bound.
5. Recheck the review when the connector, formula, schema, or expected scale changes.

## Required user states

Every applicable journey defines and tests these states. Examples use generic wording and synthetic values only; adapt them to the approved journey and verify the behavior before release.

| State | Example user-facing copy | Behavior and acceptance evidence |
|---|---|---|
| Loading | “Loading items…” | Indicate work in progress and prevent conflicting repeat submission where appropriate. A slow response shows progress; controls recover afterward. |
| Empty | “No items match these filters.” | Explain no matching items and provide a permitted next action. No-results and a genuinely empty source are distinguishable from failure. |
| Validation | “Enter a title before saving.” | Identify the invalid or missing field and retain correctable input. Invalid input cannot submit; focus/announcement makes the issue findable. |
| Permission denied | “You don’t have access to this action. Contact your app owner.” | Explain the unavailable action without revealing protected data. A denied persona cannot read or change data through the app; verify data-layer controls separately. |
| Error | “We couldn’t complete that action. Check its status before trying again or contact support.” | Give a safe, actionable message and retry/recovery path where appropriate. A forced connector/service failure is not success-shaped; handle input and diagnostics safely. |
| Success | “Changes saved.” | Confirm the completed action and resulting state. A successful operation is reflected once; repeat action does not create unintended duplicates. |

## Build controls

- Backend changes are made through the authoring service (Canvas MCP, YAML sync/compile) or approved CLI; visual acceptance is made by viewing the live app in the shared browser per `standards/visual-verification.md`. Both halves are required for every bounded change.
- Use reusable Canvas components for repeated app-shell and cross-screen UI. Prefer an approved component library when reuse spans multiple apps. Instances use `Control: CanvasComponent` with `ComponentName`.

### Canvas MCP sync rules (verified 2026-10-17 on the Flossmoor FOIA pilot)

These were discovered by inspecting the rendered DOM after a compile-clean sync produced black, default-sized controls. They are mandatory until the authoring service changes.

1. **Never reparent an existing control through sync.** The sync merges a same-named control onto its existing instance; if its parent changed, the instance is corrupted (renders at template defaults with a black fill, all layout properties blank, children positioned absolutely). Property-only updates to an existing control under the same parent are safe.
2. **Structural rebuilds use a two-sync wipe-and-recreate.** First sync the screens with no children (keep `App`, `_EditorState`, and `ComponentDefinitions`), confirm the server returns zero controls, then sync the full YAML. Every control is then created fresh.
3. **A freshly created parent requires freshly created descendants.** If a parent is recreated, every descendant must also be new; otherwise the descendants are reparented and corrupted (rule 1).
4. **Canvas component instances are not allowed inside a Gallery template.** Use a native control (e.g. `ModernBadge`) with the same mapping inside galleries.
5. **Event custom properties require `Default: =false`.** `PropertyKind: Event` without a `Default` fails compile.
6. **Do not put `App.Width` behind a named formula for breakpoints.** `IsPhone = App.Width < 600` in `App.Formulas` is evaluated once and does not re-evaluate on resize or rotation. Inline `App.Width < BreakpointPhone` in control formulas; keep only literal tokens (`BreakpointPhone = 600`) as named formulas.
7. **`ModernBadge` enums:** `BadgeIntent` has `Neutral`, not `Subtle`; `Size` is a number; `Content` is not readable as an output.
8. **Studio device emulator does not drive `App.Width`.** Phone/tablet emulation scales the canvas but `App.Width` does not follow. Verify breakpoints by resizing the real browser viewport (Browser preview mode) or in the published Player.
9. **After a large sync, hard-reload Studio.** The designer's render order and property pane can lag the server document; the server YAML (`sync_canvas` into a clean folder) is authoritative.
- Reject duplicated headers, navigation, sidebars, or footers unless a recorded authoring limitation blocks component creation and a named owner accepts the temporary exception.
- Use AutoLayout and formula-driven sizing for all supported device classes. Review every fixed width, height, X, and Y value for necessity.
- Prefer Fluent modern controls and shared design tokens; avoid per-screen color, spacing, and type literals.
- Avoid nondelegable formulas on growing data sources without an explicitly approved and tested bound.
- Keep authorization in the data/service layer; the interface may improve usability but is not an authorization control.
- Validate before writes, surface connector failures, and define duplicate, retry, and recovery behavior.
- Use environment variables and connection references where supported by the app's solution and environment.
- Make edits only in the approved environment and within the approved bounded plan. Do not publish or mutate production without explicit approval.

## Required validation and evidence

Run and retain results for applicable checks:

- App Checker findings and formula errors, including disposition of remaining findings
- Accessibility output plus the planned keyboard journey and its result
- Phone, tablet, and desktop screenshots or assessment results at the approved widths, including navigation, long text, forms, galleries, and action areas
- Component-definition compile evidence, component contract tests, and consuming-screen tests; if blocked, retain the exact service diagnostic and Studio remediation owner
- Evidence that repeated shell controls were replaced by components, or the approved temporary exception
- Delegation review and representative-volume results
- Critical persona journeys and both app-level and data-layer permission boundaries
- Submit/update/delete and duplicate behavior, connector failure, and recovery
- Each required responsive target and critical regression journey

Evidence identifies the app version, environment, test persona, requirement and test IDs, timestamp, executor, expected and actual results, result status, artifacts, defects, independent reviewer, approval where required, and rollback reference. Use the repository evidence schema; store only approved evidence in its approved location. Examples in this standard and skill must remain synthetic and contain no client identifiers, URLs, or data.

## Handoff

Provide the approved app specification, bounded edit plan, app/version and dependency inventory, validation evidence, defect disposition, known limitations, support/owner details, rollback reference, and named reviewer/approval. A successor must be able to locate the artifacts and repeat a representative critical test.
