# Agent Workflow

## Standard operating flow

1. Read the program charter, repo architecture, and current branch status.
2. Pick the assigned workstream and branch.
3. Check the workstream README and scope definition.
4. Update only the assigned files.
5. Validate local docs, links, JSON/CSV, and requirement traceability.
6. Create a short PR summary that states:
   - what changed
   - why it changed
   - what evidence was used
   - what remains open
7. Request review before merging to `main`.

## Required outputs for each workstream

Each workstream should produce:

- a clear scope definition
- a checklist or backlog for the work
- the relevant standards or templates it owns
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
