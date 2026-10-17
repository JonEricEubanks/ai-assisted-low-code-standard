# Power Apps Delivery Standard

## Required design

- Define personas, journeys, screens, navigation, responsive behavior, and device targets.
- Inventory data sources, connectors, delegation limits, expected volume, and offline needs.
- Define component reuse, naming, state, error handling, telemetry, and accessibility.
- Use environment variables and connection references where supported.

## Build controls

- Prefer reusable components and consistent layout containers.
- Avoid nondelegable formulas on growing data sources without an approved bound.
- Provide loading, empty, validation, success, permission-denied, and error states.
- Do not hide authorization logic solely in the interface.
- Use clear control names and isolate non-obvious formulas.

## Required validation

- App Checker and formula errors
- Accessibility findings and keyboard journey
- Delegation and representative-volume behavior
- Persona and permission boundaries
- Submit/update/delete/duplicate behavior
- Connector failure and recovery
- Desktop, tablet, and mobile layouts as applicable
- Regression against every critical journey

## Evidence

App version, environment, test persona, requirement/test IDs, App Checker output, accessibility output, screenshots, defects, reviewer, approval, and rollback reference.

