# SharePoint Workstream Backlog

## Branch and scope

- Branch: `feature/sharepoint-standard`
- Scope: SharePoint lists, libraries, metadata, pages, permissions, records, integrations, and delivery validation.
- Use this backlog to produce design and validation artifacts; it does not authorize production changes.
- Workstream guidance: [SharePoint Delivery Standard](../../standards/sharepoint.md) and [SharePoint Delivery skill](../../skills/sharepoint-delivery/SKILL.md).

## Synthetic design example

Use this example to exercise the backlog. It is fictional and illustrative only; values are not approved for deployment.

**Scenario:** a fictional department tracks equipment-loan requests and publishes an internal guide. Use only fabricated records such as `REQ-0001`, “Sample Laptop,” and “North Office.” Do not add real tenant or client names, URLs, people, records, or credentials.

### List schema: `EquipmentRequests`

| Display name | Internal name | Type | Required/default and validation | Index / expected scale |
| --- | --- | --- | --- | --- |
| Request ID | `RequestId` | Single line of text | Required; synthetic format `REQ-0001`; unique values enabled if supported by the approved design | Indexed; about 8,000 items in year one, 20,000 over three years |
| Item | `ItemName` | Single line of text | Required; non-empty | No index unless a demonstrated query needs it |
| Requester | `Requester` | Person | Required; one person | Indexed only if requester filtering is an accepted primary view |
| Office | `Office` | Choice | Required; controlled values such as `North Office`, `South Office` | Indexed if paired with status in a high-volume query |
| Status | `Status` | Choice | Required; default `Submitted`; values `Submitted`, `Approved`, `Declined`, `Issued`, `Returned` | Indexed; primary operational filter |
| Needed by | `NeededBy` | Date only | Required; must be today or later at submission | No index unless a date-filtered view is approved |
| Notes | `Notes` | Multiple lines of text | Optional; plain text; no sensitive data | Not indexed |

Create indexes only for fields used by selective, supported views; test combined filters and sorts against representative volume before release. Confirm platform threshold behavior and any tenant-specific limits with the SharePoint Service Owner. Do not treat the illustrative counts as capacity approval.

### Library and page examples

- **Library:** `EquipmentGuides`, with content type `Equipment Guide` and required `Title`, `GuideCategory` (choice), `Owner` (person), and `ReviewDate` (date) metadata. Synthetic sample: “Sample Laptop Setup.” Start with folders disabled unless an approved use case requires them. Specify major/minor versioning, draft visibility, check-out, approval, templates, search, archive, and migration decisions before provisioning.
- **Page:** `Equipment Help`, an internal modern page for request instructions and equipment guides. Assign a page owner, audience, review cadence, approved web parts, navigation placement, publishing approver, analytics need, and retirement path. Verify heading structure, link purpose, alt text, contrast, keyboard access, narrow-screen layout, and page load behavior.
- These are examples to refine during design, not a recommendation to deploy the named assets.

## Ready-to-assign backlog

For each item, record an owner, target, status, links to its design/evidence, and open decisions. Keep items open until their acceptance checks and required approvals are recorded.

- [ ] **List and library schemas:** Produce a data dictionary covering display and internal names, types, required/default values, validation, uniqueness, relationships, ownership, expected volume and growth, indexes, views, and threshold behavior. Include a synthetic list and library row set based on the example above. **Accept when** names are stable and reviewed, volume and query assumptions are testable, and required metadata and validation are explicit.
- [ ] **Data-model decisions:** Record lookup versus copied text, choice versus managed metadata, content type boundaries, folder policy, versioning, and attachment policy. State rationale, impacts on search and automation, and migration consequences for each choice. **Accept when** each decision has an accountable Business Data Owner and SharePoint Service Owner review; no relationship or attachment behavior is left implicit.
- [ ] **Permissions and inheritance:** Draw a role-to-permission matrix for owners, editors, contributors, readers, and service identities; identify inheritance boundaries, sharing settings, and any proposed unique scopes. **Approval point:** the Business Data Owner approves business access; the Information Security Owner approves sensitive access and unique-permission exceptions; the SharePoint Service Owner reviews inheritance and manageability. **Accept when** least privilege is demonstrated, every exception has a reason and review date, and unauthorized access is tested.
- [ ] **Records and information protection:** Document sensitivity classification, retention trigger and duration, record declaration, legal hold dependency, archive location, disposition method, and audit evidence. Mark unknown policy as unresolved rather than choosing a duration. **Approval point:** the Records Manager approves retention, record, archive, and disposition decisions; the Information Security Owner approves classification and handling. **Accept when** approval evidence and operational ownership are recorded before content is created or migrated.
- [ ] **Modern-page design and review:** Create page inventory and checklist for audience, purpose, owner, template, web parts, navigation, publishing, analytics, and review cadence. **Approval point:** the Business Data Owner approves content and audience; the Accessibility Reviewer signs off on accessibility; the SharePoint Service Owner approves navigation and publishing configuration. **Accept when** responsive, accessibility, link, publishing, and ownership checks pass with evidence.
- [ ] **App and flow integration contracts:** Inventory consuming apps, flows, forms, pages, and connectors. Specify stable internal names, operation, identity/connection owner, fields read or written, validation, failure/retry behavior, concurrency, volume, and change notification. Example: a synthetic request-submission flow creates `EquipmentRequests` with `Status=Submitted`; it must not approve or delete requests. **Approval point:** the Integration Owner and Business Data Owner approve the contract; the Information Security Owner reviews identities and data access. **Accept when** consumers are tested against the agreed contract and a breaking-change procedure is documented.
- [ ] **Provisioning, change, and rollback:** Prepare a non-production provisioning checklist, schema/configuration diff, test evidence, backup or recovery approach, rollback trigger, rollback owner, and communications plan. Include list/library/page changes, permissions, versioning, automation, and migration where relevant. **Approval point:** the Change Approver authorizes production change after the SharePoint Service Owner, Business Data Owner, and affected approval roles sign off. **Accept when** rollback is executable and tested in a representative environment; production execution remains separately authorized.

## Required validation evidence

- Schema and internal-name review; validation and required-field tests; relationship and content-type tests.
- Representative-volume and indexed-view tests, including likely filters, sorting, combined queries, pagination, and threshold behavior.
- Permission matrix, inheritance review, and positive/negative access tests.
- Recorded versioning, attachment, sensitivity, retention, archive, and disposition decisions with approval evidence.
- App/flow contract tests for successful writes, invalid input, permission failures, retries, duplicate submissions, and schema-change handling.
- Page publishing, navigation, search, accessibility, and responsive review evidence.
- Recovery and rollback rehearsal, change record, and downstream handoff (data dictionary, inventory, runbook, evidence).

## Definition of done

Another developer can design and validate a list, library, or page without hidden integration, permission, scale, accessibility, or records risks. Each backlog item has an owner and evidence; open policy or tenant-specific questions are explicit; approvals are attributable to the named roles above and are not implied by this example.

## Assumptions and unresolved decisions

- The synthetic scenario and volumes are for planning and test design only; confirm real workload, platform limits, tenant configuration, and query patterns with the relevant owners.
- No retention duration, sensitivity label, production permission, or unique-permission exception is prescribed here. Resolve these through the named approval points and applicable governance policy.
- Workstream task owners and target dates are not assigned; the workstream owner must assign them before execution.
