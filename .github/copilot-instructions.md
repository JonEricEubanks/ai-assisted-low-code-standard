# MGP AI-Assisted Delivery Instructions

This repository defines the governed MGP delivery lifecycle for Power Apps, Power Automate, SharePoint, Microsoft 365, and integrated low-code solutions.

## Required lifecycle

1. Start new requests with qualification and `solution-intake`.
2. When discovery is required, produce the approved discovery artifacts within the authorized recording, transcription, and AI-use boundary.
3. Require the Product Owner to validate specification accuracy before the developer/agent completes governed triage.
4. Do not begin architecture or implementation until triage has a `Ready` disposition and the accountable readiness approver approves the baseline.
5. Treat Product Owner specification acceptance only as confirmation of specification accuracy; it is not architecture, build, or release approval. Product Owner specification acceptance is not architecture, build, or release approval. Ready plus accountable developer approval opens architecture—not build or release.
6. Run `architecture-and-impact` before implementation.
7. Use the applicable platform delivery skill for approved build work.
8. Run `independent-qa` before recommending release.
9. Require named human approval for release.
10. Complete `documentation-handoff` before closure.

## Non-negotiable controls

- Treat missing facts as unknowns; never silently infer them.
- Keep confirmed facts, implied requirements, assumptions, and unknowns distinct.
- Attribute discovery statements to their sources and preserve source precedence or conflicts.
- Preserve stable requirement, story, acceptance-criterion, decision, task, test, evidence, defect, risk, and approval traceability.
- Surface unresolved blockers explicitly; never advance a blocking item as resolved without evidence.
- Record, transcribe, or use AI on discovery content only within explicitly approved boundaries.
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
