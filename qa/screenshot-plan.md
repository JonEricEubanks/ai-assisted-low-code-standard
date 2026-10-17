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

## Evaluation order

Complete deterministic checks and requirement-to-test-to-evidence traceability before visual or computer-use evaluation. Keep their outputs separate: visual uncertainty is `review-needed`, and computer-use results are exploratory only. Any screenshots or traces must follow the synthetic-data, publication-approval, and existing-media rules below.

## Public safety

- Prefer a demonstration tenant/site and synthetic data.
- Remove names, email addresses, tenant/environment IDs, internal URLs, connection IDs, client branding, tokens, headers, cookies, and unrelated tabs.
- Do not rely on redaction for inherently sensitive content; recreate the scenario safely.
- Retain publication approval and the source-to-public transformation record.

## Existing-media rule

Existing recordings, emails, meeting screenshots, application screens, flow definitions, inventories, and architecture walkthroughs are internal evidence candidates only. They are not public assets.

Do not publish media containing:

- tenant, environment, application, flow, resource, repository, channel, or group identifiers
- trigger URLs, webhook endpoints, tokens, authorization material, secrets, or service-principal details
- client, employee, applicant, resident, vendor, payment, invoice, signature, screening, or task-assignment data
- detailed finance, audit, records, retention, folder, payment, or external-integration architecture
- access weaknesses, missing permissions, temporary workarounds, unresolved defects, or client feedback
- staffing, handoff, performance, career, promotion, or unapproved rating information
- private code, exported packages, internal standards, training guides, or infrastructure details

Recreate public examples in a demonstration environment with synthetic data and an explicit publication approval.
