# Foundry QA development infrastructure

`main.bicep` is a resource-group-scoped foundation for a future Foundry account,
project, and optional diagnostics. All resources are disabled by default.
Names are parameters; the boundary validator fixes the only permitted
subscription, resource group, location, and GitHub environment.

Do not deploy this template. Resource deployment is blocked until the choices
below are approved. `deployFoundation` and `diagnosticsEnabled` default to
`false`; local authentication is disabled. No model deployments, role
assignments, or budget resources are defined. A budget is intentionally omitted
because it requires a broader scope than this resource-group-only contract.

## Decisions still required

- Model and deployment selection, including model-specific quota and capacity.
- Network access design and the corresponding public/private connectivity.
- Regional quota and service availability for the selected model and SKU.
- Budget amount, alert thresholds, and the human owner for subscription-level
  budget controls.
- A same-resource-group Log Analytics workspace and approved diagnostic
  retention/cost policy before enabling diagnostics.

Do not supply placeholder values to enable resources. Keep both deployment
switches off until the decisions and approvals are recorded.

## Boundary validation

Run `python scripts/validate_foundry_boundary.py` from the repository root.
The validator checks `boundary.json` and the Bicep source before any Azure
operation. Update neither the approved scope nor the authentication/RBAC
contract in this workstream.
