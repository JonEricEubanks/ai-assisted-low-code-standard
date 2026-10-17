# Integrated Solution Standard

Use this standard whenever a solution spans more than one app, flow, list, library, page, form, custom connector, or external service.

## Required contracts

- Identify the system of record for every business entity.
- Define data ownership, identifiers, schemas, inputs, outputs, and error semantics.
- Map app-to-flow, flow-to-SharePoint, connector, approval, document, and notification boundaries.
- Record identities, connections, permissions, environment variables, solution dependencies, and licenses.
- Define failure boundaries, replay/idempotency, recovery, rollback, monitoring, and support.

## Change-impact map

Every change must list:

- Components changed
- Upstream and downstream dependencies
- Data/schema effects
- Security and records effects
- Regression tests
- Deployment order
- Rollback order
- Owners and approvers

## Release rule

An integrated solution cannot release when a critical dependency is unknown, an integration failure has no observable signal, or a successor cannot identify the responsible owner and recovery procedure.

