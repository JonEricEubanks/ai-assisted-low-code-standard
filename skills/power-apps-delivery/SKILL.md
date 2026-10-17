---
name: power-apps-delivery
description: Plan, implement, validate, and hand off a bounded Canvas app change using the approved Power Apps standard and authorized Canvas MCP capabilities.
---

# Power Apps Delivery

## Procedure

1. **Qualify.** Confirm the approved outcome, scope, owner, acceptance criteria, personas, data contract, and test identities. Record unknowns and who must resolve them. Stop if a missing security, data ownership, or production-access decision is required.
2. **Inspect.** For an existing app, inventory its version, screens, controls, formulas, data sources, connectors, dependencies, permissions, and known issues before proposing edits. Use only approved access and environments.
3. **Specify.** Complete the app specification required by `standards/power-apps.md`: journeys and exceptions, screens/states, phone/tablet/desktop responsive targets, repeated UI that must become components, Fluent design tokens, data/delegation constraints, and delivery/support details. Link requirements to acceptance and test IDs.
4. **Plan.** Produce a bounded edit plan and have the designated reviewer approve it before editing. Include:
   - app/environment/version and scope boundary
   - files/screens/controls/formulas/data sources to inspect or change
   - requirement, expected behavior, and test IDs for each change
   - dependencies, permission/data effects, delegation and responsive impact
   - backup/restore or rollback method, validation steps, and explicit exclusions
   - unresolved questions, risk, approver, and any production restriction
5. **Prepare.** Confirm the approved non-production environment and test identities. Preserve a recoverable baseline using the authorized platform procedure. Use synthetic test data; do not copy client-sensitive data into prompts, examples, screenshots, or logs.
6. **Edit.** Use only supported and authorized Canvas MCP capabilities for the approved plan. Centralize breakpoints and Fluent tokens; use AutoLayout, formula-driven dimensions, wrapping, and `AutoHeight`. Replace repeated headers, navigation, sidebars, footers, and shared status UI with Canvas components. Preview the proposed changes where supported and compare the result with the plan. Do not improvise scope, bypass approval, publish, or make production mutations.
   - Before component edits, assess execution and compile a minimal `ComponentDefinitions` definition plus `Control: Component` instance.
   - If the authoring service rejects component definitions or instances, preserve the exact diagnostics, stop that portion, and route it to Power Apps Studio or the approved component-library workflow. Do not silently duplicate controls or report the component work as complete.
7. **Check.** Compile/sync as supported, resolve every formula and App Checker error, and record warnings and dispositions. Run accessibility checks and the planned keyboard journey. Verify labels, gallery tab stops, focus order, contrast, and phone/tablet/desktop layouts at approved widths.
8. **Test.** Execute critical journeys for applicable personas, including validation, loading/empty/success/error states, denied permissions, write/duplicate behavior, connector failure/recovery, delegation, and representative synthetic volume. Check the data/service layer independently; a hidden control is not proof of authorization. Run critical regression tests.
9. **Review.** Compare actual changes and test results against the approved plan and acceptance criteria. Any failed, blocked, or review-needed result is explicit, linked to a defect or decision, and never represented as a pass. Obtain independent review and required approval before release.
10. **Hand off.** Provide app/version and dependency inventory, plan, validation evidence, screenshots cleared for the approved audience, defects/known limitations, release notes, support owner, rollback reference, and approval. Update relevant architecture and handoff records.

## Canvas MCP checklist

Complete for each bounded change. Stop and escalate instead of checking a box when approval, tool capability, or evidence is missing.

### Before editing

- [ ] Requirements, acceptance criteria, owner, personas, and test IDs are confirmed.
- [ ] Current app/version, environment, dependencies, permissions, and affected data sources are inventoried.
- [ ] Edit plan names the exact scope, expected changes, exclusions, risk, tests, and rollback method.
- [ ] Repeated app-shell controls and the component contracts that replace them are identified.
- [ ] Phone, tablet, and desktop breakpoints and expected layout behavior are explicit.
- [ ] Fluent palette, spacing, typography, and minimum touch-target tokens are defined.
- [ ] Required reviewer approval and authorized non-production environment are confirmed.
- [ ] Baseline is recoverable; test identities and synthetic data are approved.
- [ ] Planned Canvas MCP operations are supported and authorized; preview is available or its absence is recorded.

### After editing

- [ ] Actual changes match the approved plan; no out-of-scope or production change occurred.
- [ ] App sync/compile and App Checker results are recorded; remaining findings are dispositioned.
- [ ] Accessibility, keyboard journey, labels, focus, and required responsive targets are checked.
- [ ] Phone, tablet, and desktop layouts are tested with evidence; long text, galleries, forms, navigation, and action areas do not clip or overflow.
- [ ] Reusable component definitions and instances compile and pass contract tests, or the exact authoring diagnostic and Studio remediation owner are recorded.
- [ ] No duplicated header, navigation, sidebar, or footer controls remain without an approved temporary exception.
- [ ] Delegation and representative synthetic-volume results are recorded.
- [ ] Persona, data-layer permission, write/duplicate, error/recovery, and critical regression tests are recorded.
- [ ] Evidence, defects/known limitations, rollback reference, reviewer, and required release approval are complete.

## Required outputs

App specification; app/environment/version and dependency inventory; approved edit plan; component inventory and contracts; App Checker and accessibility results; phone/tablet/desktop evidence; test/evidence records; sanitized screenshots where approved; defect disposition and known limitations; release notes; rollback reference; named reviewer and required approval.

## ELM discovery questions

For an ELM-related app change, collect answers from authorized owners and evidence. Do not infer that an app, connector, list, flow, permission, or support arrangement exists. Record unanswered items as `Unknown`, the source checked, the decision owner, and the next action.

- What is the exact app identity, URL/ID, environment, version, and owner? Who can verify each?
- Which user outcomes, personas, roles, critical journeys, and acceptance criteria are in scope?
- What data sources, connectors, related flows/lists, identities, and solution dependencies does this app actually use?
- Who owns each data source, and what are its permissions, expected volume/growth, delegation behavior, and offline requirements?
- Which screens and controls support the in-scope journeys? What existing errors, accessibility issues, and responsive/device requirements are known?
- What test identities and synthetic data are approved, and how can app-level and data-layer permissions be independently verified?
- What environments and Canvas MCP operations are authorized? Which actions require preview, human approval, or are prohibited?
- What validation evidence, release approvals, support owner, recovery procedure, and rollback reference are required?

Do not include ELM client URLs, identifiers, records, credentials, or other sensitive details in a public-safe example or handoff proposal.
