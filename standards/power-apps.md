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

- Prefer responsive containers and relative sizing over fixed coordinates. State the supported viewport and test every required device class.
- Keep navigation, labels, focus order, keyboard operation, contrast, and non-color status cues usable at each supported size.
- Every actionable control has a clear accessible name and purpose; do not use placeholder text as the only label.
- Record accessibility findings and disposition. A clean automated check does not replace keyboard and assistive-technology review where required.

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

- Use reusable components and consistent layout containers when they improve reuse or consistency.
- Avoid nondelegable formulas on growing data sources without an explicitly approved and tested bound.
- Keep authorization in the data/service layer; the interface may improve usability but is not an authorization control.
- Validate before writes, surface connector failures, and define duplicate, retry, and recovery behavior.
- Use environment variables and connection references where supported by the app's solution and environment.
- Make edits only in the approved environment and within the approved bounded plan. Do not publish or mutate production without explicit approval.

## Required validation and evidence

Run and retain results for applicable checks:

- App Checker findings and formula errors, including disposition of remaining findings
- Accessibility output plus the planned keyboard journey and its result
- Delegation review and representative-volume results
- Critical persona journeys and both app-level and data-layer permission boundaries
- Submit/update/delete and duplicate behavior, connector failure, and recovery
- Each required responsive target and critical regression journey

Evidence identifies the app version, environment, test persona, requirement and test IDs, timestamp, executor, expected and actual results, result status, artifacts, defects, independent reviewer, approval where required, and rollback reference. Use the repository evidence schema; store only approved evidence in its approved location. Examples in this standard and skill must remain synthetic and contain no client identifiers, URLs, or data.

## Handoff

Provide the approved app specification, bounded edit plan, app/version and dependency inventory, validation evidence, defect disposition, known limitations, support/owner details, rollback reference, and named reviewer/approval. A successor must be able to locate the artifacts and repeat a representative critical test.
