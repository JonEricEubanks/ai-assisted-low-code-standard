---
name: azure-resource-boundary
description: "Use when: doing any Azure work, using Azure CLI, Azure MCP, SDKs, REST, azd, Bicep, or Terraform; creating a resource group or subscription boundary; or turning on Azure guardrails. Covers Foundry, OCR, Document Intelligence, storage, and other workloads in Microsoft Azure Sponsorship. Require an explicitly approved resource group per workload and verify the executing identity before writes."
---

# Azure Resource Boundary

Version: 1.0.0. Installed workflow; independent second-developer validation is pending.

## Purpose

Establish and verify one workload-specific Azure boundary before passing control to
a service skill. Invoke this skill before Azure work, not instead of the Foundry,
OCR, storage, deployment, or other service-specific procedure.

A skill is not an Azure security control. It cannot remove permissions from an
Owner session, constrain an MCP connection by changing CLI defaults, or sandbox
arbitrary commands. Azure RBAC enforces the permissions of the identity actually
executing each request. A preflight is a point-in-time check, not a persistent lock.

## Subscription policy

For this installation, the permitted subscription is:

- Name: Microsoft Azure Sponsorship
- ID: `b8f90e47-b8ee-45f1-9442-d3b4f8fd0695`
- Tenant: `ce08ca1a-3a87-472b-affa-217b4d4793ce`

Do not silently change this policy for another project. A different subscription
requires explicit human approval and a separately reviewed policy configuration.
Never infer authorization from a subscription name or the current CLI default.

## Required inputs

Obtain and record:

- Workload name, purpose, environment, accountable owner, and approval reference
- Exact approved resource-group name and Azure resource ID
- Approved resource locations and any service-specific exceptions
- Permitted operations and explicitly prohibited operations
- Executing identity and authentication channel for CLI, MCP, SDK, or workflow
- Data classification, approved inputs, evidence destination, and retention
- Cost limits, model/service choices, network requirements, and rollback approach

Unknown values stay unknown. Planning may continue with clearly labeled unknowns;
resource writes must wait for the relevant approvals.

Each workload needs an explicitly approved group. The Foundry QA group
`rg-mgp-foundry-qa-dev` is a workload-specific example, NOT a default for OCR or
unrelated work. Do not reuse, create, rename, or select a group without approval.

## Procedure

### 1. Resolve the boundary

Read the project's existing boundary record and applicable instructions first.
Preserve stricter project controls. Ask for missing workload, group, location,
identity, or approval decisions before implementation.

If the user says "turn guardrails on", run this procedure and report the verified
state. Do not interpret that phrase as permission to create identities, assign
roles, alter policies, enable public access, or deploy chargeable resources.

### 2. Verify context without mutation

Use approved authenticated tools. For Azure CLI, start with read-only commands:

```powershell
az account show --subscription b8f90e47-b8ee-45f1-9442-d3b4f8fd0695 --output json
```

Compare the returned subscription ID, tenant ID, state, and executing identity
with the approved record. Check native exit codes explicitly; a failed command
must not be followed by a write.

After substituting the approved group, inspect that group using the explicit
subscription. Inspect relevant existing resources, inherited role assignments,
group-scoped roles, group memberships, and data-plane access as needed.
Do not treat a direct-role listing as proof that no broader access exists.
If effective permissions cannot be established, report enforcement as unverified.

For MCP, verify that tool's own identity and subscription context. CLI login,
`az account set`, and environment variables do not prove MCP uses the same identity.
For SDKs, resolve the actual selected credential; do not assume a credential chain
uses the intended managed identity.

### 3. Separate bootstrap from workload access

If the group or workload identity does not exist, present a bounded bootstrap
plan for approval. Include exact names, location, role, scope, trust subject,
cost implications, and rollback. Only an explicitly approved human-administered
bootstrap may create a group, identity, federation, or role assignment.

Use a distinct workload identity with the least privileges needed. Prefer
service-specific roles over Contributor when practical. Scope management access
to the approved group or narrower resource. Approve data-plane permissions
separately; a management role is not proof of authorized OCR, storage, or model
data access.

For GitHub, prefer OIDC with a narrowly bound repository and environment subject.
Configure environment protection and branch restrictions where supported. Never
claim those protections exist without verifying them. Do not store client secrets,
publish profiles, account keys, or reusable personal tokens.

Do not change an Owner user's roles or log them out automatically. If the tool is
using Owner or another broadly privileged identity, report that it is NOT
RBAC-confined. Use the approved limited identity before routine workload writes;
request explicit bootstrap approval if elevated access is genuinely required.

### 4. Validate every operation

Before each write or delegated assignment:

1. Require the approved subscription, group, identity, and locations explicitly.
2. Validate every target and referenced resource ID, including existing resources,
   nested deployments, cross-group modules, storage destinations, and connections.
3. Reject subscription-, management-group-, and tenant-scoped workload deployments.
4. Review resource-group-scoped validation/what-if or the Terraform plan before
   apply. Check resolved parameters, provider aliases, and module scopes.
5. Stop on scope mismatch, missing inputs, permission errors, unexpected changes,
   unsupported geography, or unapproved data movement. Never use another group or
   region as a silent fallback.
6. Keep deletion, access changes, retention changes, public-network exposure, and
   production mutation behind their own explicit approvals.
7. Recheck context after authentication changes, tool changes, handoffs, or retries.

Subscription/provider registration and quota requests are separate privileged
operations. Report them as blockers instead of performing them implicitly.
Use explicit resource-group deployment commands rather than relying on defaults.
Require the same contract in Azure CLI, MCP, SDK/REST, Bicep, Terraform, and azd.

### 5. Delegate with the boundary

Give every agent the exact subscription, tenant, group, allowed locations,
approved operations, identity/channel, owned paths, and stop conditions.
Do not give agents an Owner credential or reusable secret.
Require a reviewed PR and validation evidence; do not let an agent grant itself
permissions or weaken this policy. A repository instruction alone is not a sandbox.

### 6. Verify and hand off

Retain sanitized checks, validation results, actual target resource IDs, role/trust
configuration, and unresolved risks in the approved evidence location.
Do not retain tokens, keys, sensitive document contents, or unapproved traces.
After bootstrap, verify access using the workload identity, not just the creator's
Owner account. Do not test isolation by attempting writes outside the boundary.

Hand off to the applicable service skill only after its prerequisites are met.
Cost alerts are not hard spending caps; document actual stop controls separately.

## Required status report

Always return:

| Field | Value |
|---|---|
| Workload / environment / approval | Named values or unknown |
| Subscription / tenant | Verified IDs or mismatch |
| Resource group / allowed locations | Explicit approved values |
| Execution channel / identity | CLI, MCP, SDK, or workflow and actual identity |
| Boundary state | `blocked`, `guidance-only`, `scope-verified`, or `rbac-verified` |
| Permitted operations | Explicit list |
| Validation evidence | Commands/tools, timestamps, results, and safe references |
| Remaining decisions | Unknowns, privileged bootstrap needs, and risks |

`scope-verified` means target context matches, NOT that permissions are restricted.
Use `rbac-verified` only when the executing identity, effective role scopes, relevant
data access, and authentication binding have been checked. State limitations.
If an input mismatches, use `blocked`; never announce a generic "guardrail enabled".
