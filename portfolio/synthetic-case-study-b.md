# Case Study B: Fictional Community Event Check-In

> Synthetic demonstration scenario. This is not a description of a pilot, client, organization, or deployed solution. All names, records, and outcomes are fictional.

## Problem and prior process

A fictional community group uses a paper tally to estimate attendance at a public workshop. The group wants a simple, accessible way to count check-ins and view an aggregate total.

## Constraints and assumptions

The example uses anonymous, synthetic check-in records and a disposable demonstration environment. It does not collect names, contact details, eligibility, health information, or other personal data. No real deployment or client process is represented.

## Design and decisions

Use a minimal check-in control and an aggregate count. A human host handles exceptions. Do not add identity, payment, records-retention, or external-system integrations to this example.

## Delivery and validation

Define keyboard and screen-reader expectations before implementation. Test empty, valid, duplicate, and unavailable states with synthetic fixtures. A synthetic QA finding identifies that the count is not announced after check-in; the correction adds an accessible status announcement and is retested.

## Outcomes and evidence

No pilot result or realized benefit is claimed. The aggregate counter is a design demonstration only. Any future impact claim requires an approved measurement method and source.

## Reuse and lessons

Independent reuse and successor support remain validation questions. Keep the data model intentionally minimal and test accessible feedback as part of the acceptance criteria.

## Visuals

See [`synthetic-visuals.md`](synthetic-visuals.md), which contains synthetic process, architecture, QA, adoption, and outcome diagrams with alt text and captions.
