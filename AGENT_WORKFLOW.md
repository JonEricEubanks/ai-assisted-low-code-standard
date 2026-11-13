# Agent Workflow

## Standard operating flow

1. Read the program charter, repo architecture, and current branch status.
2. Confirm the current lifecycle stage and the approval that permits work at that stage.
3. For new requests, run solution intake before architecture:
   - triage the available CSM handoff
   - use the discovery script for unresolved stakeholder questions
   - retain source and participant attribution for recorded answers
   - generate the User Story Specification only from supported transcript content
   - separate confirmed facts, implied requirements, assumptions, and unknowns
   - obtain Product Owner acceptance of specification accuracy
   - complete complexity, risk, and readiness classification
4. Treat Product Owner specification acceptance as an input to readiness review, not as architecture, implementation, release, or production approval. Product Owner specification acceptance is not architecture, build, or release approval. Ready plus accountable developer approval opens architecture—not build or release.
5. Stop when recording, transcription, tenant access, or AI processing is outside the approved identity, consent, access, retention, or data boundary.
6. Pick the assigned workstream and branch.
7. Check the workstream README and scope definition.
8. Update only the assigned files.
9. Preserve stable requirement, story, acceptance-criterion, decision, task, test, and evidence IDs.
10. Validate local docs, links, JSON/CSV, and requirement traceability.
11. Create a short PR summary that states:
   - what changed
   - why it changed
   - what evidence was used
   - what remains open
12. Request review before merging to `main`.

## Required outputs for each workstream

Each workstream should produce:

- a clear scope definition
- a checklist or backlog for the work
- the relevant standards or templates it owns
- attributed discovery sources and approved specifications when applicable
- validation evidence
- a handoff note for downstream work

## Shared files and guardrails

The following files are shared and should be coordinated by the program owner or designated editor:

- `README.md`
- `requirements.md`
- `plan.md`
- `governance/*.md`

No agent should edit these without checking whether another branch already owns a related update.

## Goal

This repo should help multiple agents work in parallel without creating drift, duplication, or inconsistent standards.
