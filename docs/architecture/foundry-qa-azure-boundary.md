# Foundry QA Azure Boundary

## Approved development scope

The Foundry QA development baseline is approved for non-production implementation within one dedicated Azure resource group.

| Setting | Approved value |
|---|---|
| Subscription | Microsoft Azure Sponsorship |
| Subscription ID | `b8f90e47-b8ee-45f1-9442-d3b4f8fd0695` |
| Tenant ID | `ce08ca1a-3a87-472b-affa-217b4d4793ce` |
| Resource group | `rg-mgp-foundry-qa-dev` |
| Region | `eastus2` |
| Environment | Development/non-production |
| Data boundary | Synthetic or explicitly approved non-production data |
| GitHub environment | `foundry-dev` |
| Workload identity | `id-mgp-foundry-qa-github` |

This approval is limited to the Foundry QA development workstream. It does not close unrelated program governance decisions or authorize production deployment.

## Enforced identity boundary

GitHub Actions authenticates through an Azure user-assigned managed identity and an OpenID Connect federated credential. The federated subject is:

```text
repo:JonEricEubanks/ai-assisted-low-code-standard:environment:foundry-dev
```

The identity has `Contributor` only at:

```text
/subscriptions/b8f90e47-b8ee-45f1-9442-d3b4f8fd0695/resourceGroups/rg-mgp-foundry-qa-dev
```

It has no approved subscription-, management-group-, or tenant-scoped role. Contributor does not authorize role assignments. Identity and access changes remain human-administered.

## Deployment contract

Every Azure workflow must:

1. Use the `foundry-dev` GitHub environment.
2. Authenticate with OIDC using environment variables rather than stored credentials.
3. Verify the active subscription ID before any write.
4. verify that the target resource group is exactly `rg-mgp-foundry-qa-dev`.
5. Use resource-group-scoped what-if or validation before deployment.
6. Deploy only after validation succeeds.
7. Retain the validation and deployment result as pull-request or workflow evidence.
8. Stop on missing configuration, permission errors, or scope mismatches.

The workflow must not silently select a default subscription or resource group.

## Prohibited actions

- Creating or selecting another resource group
- Subscription-, management-group-, or tenant-scoped deployment
- Creating role assignments or elevating the workload identity
- Adding Azure client secrets, publish profiles, access keys, or reusable tokens
- Production deployment or production mutation
- Uploading client, tenant, credential, or other unapproved sensitive data
- Enabling autonomous computer use before its separate threat-review gate

## Human-owned controls

A named human owner must approve:

- Identity or RBAC changes
- Model and deployment selection
- Network and data-boundary changes
- Budget and quota changes
- Release thresholds
- Any transition beyond development or shadow evaluation

Model-based QA remains supplemental. Deterministic checks and named human approval remain authoritative for release.
