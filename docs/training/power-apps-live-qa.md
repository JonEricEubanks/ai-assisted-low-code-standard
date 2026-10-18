# Power Apps Live QA Quick Start

Use this process to test a published Canvas app from the user's point of view and
produce evidence another developer can understand and repeat.

Live testing and edit-mode inspection are separate:

| Surface | Use it to verify |
|---|---|
| Published Player / play mode | Runtime navigation, visible state, validation, data behavior, permissions, responsive rendering, and recovery |
| Power Apps Studio / edit mode | Controls, formulas, data sources, App Checker, accessibility output, delegation warnings, and maintainability |

Do not claim runtime acceptance from Studio, YAML, compile output, or App Checker
alone. Do not claim formula or permission correctness from a live screenshot.

## Before the test

Collect these values before opening the app:

- Requirement and test IDs
- Exact app name, app ID, published solution/app version, and environment
- Test persona and expected permissions
- Approved synthetic test-data reference
- Supported desktop, tablet, and phone breakpoints
- Allowed mutations and cleanup owner
- Evidence classification, location, and retention

If the exact published version, persona, test data, or mutation permission is
unknown, continue only with a read-only smoke test and record the missing fact.

Close stale Player and Studio tabs. Use one authenticated Player tab for the test.
Reload it before capture so the evidence does not come from a stale session.

## Streamlined test loop

### 1. Confirm the target

Record the actual Player URL's environment and app IDs without copying the URL into
public evidence. Confirm the title and intended persona. Verify that the displayed
records are synthetic or otherwise approved for testing.

### 2. Run deterministic checks first

From the matching edit session, collect:

- App Checker output
- Accessibility output
- Compile/save status
- Known delegation warnings and disposition
- Data-source and connection-reference inventory

Do not edit the app during independent QA. If the edit session points to a
different app ID than the Player, stop and reconcile the target.

### 3. Check the initial live state

In Player, confirm:

- Shell, heading, navigation, metrics, search, filters, list, and empty/detail
  state render
- Counts agree with the visible synthetic fixture
- Interactive elements have meaningful accessible names
- No clipping, overlap, placeholder imagery, hidden error, or stuck loading state
- Console errors are separated into Microsoft platform noise and app-specific
  failures; uncertain ownership is `review-needed`

Capture the initial state and record what the capture proves.

### 4. Exercise read-only journeys

Use semantic accessible-role/name selectors where the browser surface supports
them. Test:

1. Refresh
2. Open each existing synthetic record
3. Return Home
4. Search for a known record, then a no-match value
5. Apply and clear each filter
6. Open Department work and Closeout without saving
7. Verify loading, empty, and detail states

Record expected and actual results after each step. Do not retry a failed or flaky
step until it passes and report only the successful attempt.

### 5. Exercise approved mutation journeys

Only when explicitly approved, test:

- Required-field validation without saving
- Create and submit a uniquely identified synthetic record
- Duplicate handling
- Update and status transition
- Connector failure and recovery
- Closeout, rollback, and cleanup

Record the created record ID and cleanup evidence. Never use a production resident,
employee, applicant, or client record.

### 6. Check supported breakpoints

Capture the published Player at:

- Desktop: 1366 CSS px wide
- Tablet: 820 CSS px wide
- Phone: 390 CSS px wide

Verify that the Player is reporting the intended app width. Power Apps Player can
scale an app inside its shell, so a resized outer browser is not automatically a
valid device test. Use a real device or approved maker-browser test when Player
scaling makes the result ambiguous.

### 7. Handle automation boundaries

Power Apps runs inside an embedded frame. If semantic clicks time out:

1. Resolve `iframe.player-app-frame` and locate controls through that frame's
   accessible roles and names; an outer-page locator does not search the app.
2. Do not silently switch to broad coordinate automation and call the result
   authoritative.
3. Capture the current state and browser/tool error.
4. Attempt one controlled reproduction after a clean reload.
5. If the app surface becomes blank or the interaction remains inaccessible,
   mark the journey `blocked`.
6. Hand the exact steps to a human tester in the authenticated Player.
7. Do not classify an app defect until the behavior reproduces through a supported
   manual or semantic interaction.

Authentication is never automated with a person's password or MFA. If a clean
automation context redirects to sign-in, use the approved authenticated shared
browser or stop.

## Evidence to retain

For every run, record:

- Environment, app ID, exact version, persona, and fixture
- Requirement, test, run, and evidence IDs
- Expected and actual result
- `pass`, `fail`, `blocked`, or `review-needed`
- Screenshot/trace/log reference and the claim it supports
- Defect ID for every failed result
- Independent reviewer, classification, and retention tag
- Untested areas and residual risks

Use `templates/test-case.md`, `qa/evidence-schema.md`, and
`qa/screenshot-register.csv`. A screenshot without a claim is not evidence.

## Completion rule

A live smoke test is not release approval. Release still requires deterministic
results, critical functional and permission paths, supported breakpoints, failure
and recovery evidence, rollback/support evidence, dispositions, and named human
approval.
