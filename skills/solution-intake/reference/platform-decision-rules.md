# Platform Decision Rules

Each rule maps an observable requirement to a component choice. Never select a component without naming the requirement that forces it.

## Rule format

> **If** [requirement signal] **then** [component] **because** [reason] **unless** [exception].

---

## Intake form selection

**If** the request requires a public-facing or external intake form
**then** select the form tool from this table
**because** attachment support and external authentication differ by product.

| Audience | Attachments required | Tool |
|---|---|---|
| External (public) | Yes | Survey123 |
| External (public) | No | Microsoft Forms |
| Internal | Yes or No | Microsoft Forms |

**Unless** the client already runs a web form platform that must remain the public entry point — in which case record the integration contract (webhook, email parse, or export) as a Phase-1 risk and prefer replacing it with the table above.

## Data layer

**If** the solution tracks a business entity with a lifecycle and status
**then** a SharePoint list
**because** it provides versioning, permissions, views, and native Power Platform integration without additional licensing
**unless** the entity exceeds roughly 100,000 active items, requires complex relational integrity, requires row-level security at scale, or requires true transactional behavior — in which case escalate to Dataverse and record the licensing impact.

**If** the solution stores photos or documents as evidence
**then** a document library with content types and metadata
**because** libraries handle large binaries, versioning, and retention natively
**unless** the media volume per record is trivial and never referenced independently — in which case list attachments are acceptable.

**If** two entities relate as parent and child
**then** separate lists with a lookup, not a single flattened list
**because** flattening destroys reporting and history
**unless** the child has no independent lifecycle.

**If** the same reference values appear across multiple lists
**then** a single reference list
**because** choice columns drift and cannot be audited.

## Application layer

**If** work is performed on a tablet or phone in the field
**then** a canvas app
**because** it gives layout control, offline-capable patterns, camera access, and simplified task-focused screens
**unless** the work is purely record review — in which case a SharePoint view may be sufficient.

**If** work is primarily desk-based record management by trained staff
**then** evaluate SharePoint list views with formatting before building an app
**because** an app that duplicates a list view adds maintenance with no benefit
**unless** validation, multi-step logic, or cross-list orchestration is required.

**If** the solution has clearly separated personas with different tasks
**then** role-aware navigation within one app
**because** multiple apps multiply deployment, versioning, and handoff cost
**unless** the personas never overlap and have fundamentally different security postures.

**If** the audience is the general public or external parties
**then** stop and escalate
**because** external access changes licensing, security, and governance posture entirely.

## Automation layer

**If** something must happen when a record changes
**then** an automated cloud flow on the item trigger
**because** it is the native event model
**unless** the action must be user-initiated with confirmation — in which case an instant flow invoked from the app.

**If** something must happen on a date or cycle
**then** a scheduled cloud flow that queries for due conditions
**because** per-item delays are fragile across long durations and are lost on flow revision
**unless** the wait is under a few days and the volume is low.

**If** a person must approve, reject, or reassign
**then** an approval pattern with explicit reassignment, timeout, and escalation handling
**because** approvals that model only the happy path fail in production within weeks.

**If** a document must be produced for signature, mailing, or filing
**then** a document-generation step producing a stored, versioned artifact
**because** regenerating on demand loses the evidentiary snapshot.

**If** the flow writes to an external system
**then** isolate the call behind a single wrapper flow with retry, idempotency, and failure routing
**because** the integration contract must be independently testable and replaceable.

## Cross-cutting rules

**If** the request names two or more departments
**then** define the permission model before building anything
**because** cross-department visibility is the requirement most often assumed and least often specified.

**If** the output supports enforcement, adjudication, finance, or personnel action
**then** treat it as records-bearing and require a records decision
**because** the retention obligation attaches to the content regardless of where it is stored.

**If** the solution replaces institutional knowledge held by individuals
**then** a documented handoff package is a deliverable, not an afterthought
**because** continuity is the stated business outcome in these requests.

**If** any required capability needs a premium connector
**then** surface the license cost at intake
**because** discovering it at release converts a technical choice into a budget escalation.

## Default shape by complexity tier

| Tier | Typical shape |
|---|---|
| S | One list, one automated flow, SharePoint views |
| M | 2-4 lists, one canvas app, 2-4 flows, one library |
| L | Multi-entity model, role-aware canvas app, scheduled + event flows, document library with content types, reporting views |
| XL | Phase it. Deliver the data model and one persona journey first. |

The default shape is a starting hypothesis, not a design. It is replaced by the architecture decision record.

## Prohibited at intake

- Naming a component without naming the requirement
- Choosing Dataverse without recording the licensing impact
- Promising offline capability without confirming device management and data volume
- Assuming an existing identity group exists without verification
- Designing the screens — intake defines what, architecture defines how
