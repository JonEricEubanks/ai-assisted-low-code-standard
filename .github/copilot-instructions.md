# MGP Delivery Repository Instructions

Follow the governed lifecycle and workstream ownership rules in `AGENT_WORKFLOW.md` and `BRANCHING.md`. Never write directly to `main`; use one bounded branch and pull request per issue.

## Azure boundary for Foundry QA

All Azure work for the Foundry QA development workstream is restricted to:

- Subscription: `Microsoft Azure Sponsorship`
- Subscription ID: `b8f90e47-b8ee-45f1-9442-d3b4f8fd0695`
- Resource group: `rg-mgp-foundry-qa-dev`
- Region: `eastus2`
- GitHub environment: `foundry-dev`

Treat this as a hard boundary:

1. Create, update, query, or delete Foundry QA resources only inside `rg-mgp-foundry-qa-dev`.
2. Do not create another resource group, use another subscription, or deploy at subscription, management-group, or tenant scope.
3. Do not add role assignments, broaden identity permissions, create reusable credentials, or use a personal access token for Azure.
4. Use GitHub OIDC and the environment variables from `foundry-dev`; never add Azure client secrets or access keys.
5. Use resource-group-scoped deployments and fail before deployment if the active subscription or target resource group differs from the values above.
6. Use synthetic or explicitly approved non-production data only. Do not mutate production.
7. Infrastructure changes require a reviewed pull request and retained validation output.

The GitHub OIDC identity is intentionally limited to `Contributor` on this resource group. If a task requires broader access, stop and record the blocked requirement instead of changing the boundary.

See `docs/architecture/foundry-qa-azure-boundary.md` for the implementation and verification contract.
