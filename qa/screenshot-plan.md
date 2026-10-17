# Screenshot and Visual Evidence Plan

## Capture moments

### Baseline

- Current requirements and process
- Existing build inconsistencies
- Current QA and handoff state
- Repetitive manual steps

### Planning

- Goal scorecard
- Intake output
- Acceptance criteria
- Architecture and data diagrams
- Human/agent/MCP swimlane
- Risk and decision register

### Power Apps

- Screen specification and implemented screen
- App Checker before and after
- Accessibility before and after
- Delegation warning and correction
- Loading, empty, validation, error, desktop, and mobile states

### Power Automate

- Design and standardized scope structure
- Error handling, run-after, retry, and connection references
- Successful and intentionally failed runs
- Diagnostic output, notification, and recovery

### SharePoint

- Requirements-to-schema mapping
- Columns, indexes, views, formatting, content types, metadata, versioning, permissions, page wireframe, and final page

### QA and adoption

- Requirement-to-test traceability
- Playwright journey
- Vision finding
- Failed test, correction, rerun, and final pass
- Release report
- Another developer using the standard
- Training and feedback

## Capture log fields

Use `qa/screenshot-register.csv`. For every image, explain what it proves; a screenshot without a claim is decoration, not evidence.

## Public safety

- Prefer a demonstration tenant/site and synthetic data.
- Remove names, email addresses, tenant/environment IDs, internal URLs, connection IDs, client branding, tokens, headers, cookies, and unrelated tabs.
- Do not rely on redaction for inherently sensitive content; recreate the scenario safely.
- Retain publication approval and the source-to-public transformation record.

