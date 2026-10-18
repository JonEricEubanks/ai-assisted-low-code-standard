# MGP AI-Assisted Delivery Instructions

This repository defines the governed MGP delivery lifecycle for Power Apps, Power Automate, SharePoint, Microsoft 365, and integrated low-code solutions.

Follow the governed lifecycle and workstream ownership rules in `AGENT_WORKFLOW.md` and `BRANCHING.md`. Never write directly to `main`; use one bounded branch and pull request per issue.

## Required lifecycle

1. Start new requests with `solution-intake`.
2. Do not begin architecture or implementation until intake has a `Ready` disposition and the accountable developer approves the baseline.
3. Run `architecture-and-impact` before implementation.
4. Use the applicable platform delivery skill for approved build work.
5. Run `independent-qa` before recommending release.
6. Require named human approval for release.
7. Complete `documentation-handoff` before closure.

## Non-negotiable controls

- Treat missing facts as unknowns; never silently infer them.
- Keep confirmed facts, implied requirements, assumptions, and unknowns distinct.
- Preserve requirement, decision, task, test, evidence, defect, risk, and approval traceability.
- Never autonomously mutate production, change access, delete content, make retention decisions, or communicate externally.
- Do not expose secrets, client-sensitive data, or tenant content in repository files or chat output.
- Use approved authenticated tools for SharePoint and tenant access. A pasted URL is not proof that a tool can access it.
- Stop and explain the missing capability when an approved SharePoint/Microsoft 365 connection is unavailable.
- Prefer deterministic platform output over model judgment.
- Before Azure work, invoke `azure-resource-boundary` and follow `skills/azure-resource-boundary/SKILL.md`. Require an explicitly approved workload resource group in Microsoft Azure Sponsorship; never infer a sandbox from CLI defaults or an Owner login. Preserve any stricter workload-specific Azure boundary.

## Sources of truth

- Lifecycle: `standards/common-delivery-lifecycle.md`
- Intake: `standards/intake-and-triage.md`
- Orchestration: `agents/delivery-orchestrator.md`
- Procedures: `skills/*/SKILL.md`
- Platform decision rules: `skills/solution-intake/reference/platform-decision-rules.md`
- Templates: `templates/`
- QA and release evidence: `qa/`

Do not replace these governed sources with duplicated ad hoc instructions.

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
