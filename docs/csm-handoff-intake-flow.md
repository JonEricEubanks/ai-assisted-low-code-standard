# CSM Handoff to Developer Intake Flow

## Purpose

Define how a CSM handoff becomes an approved, traceable developer work package without requiring developers to manually reconstruct requirements or download disconnected copies of project files.

## Operating flow

1. **CSM prepares the SharePoint project folder**
   - Project charter
   - Approved scope and exclusions
   - User stories
   - Business owner and sponsor
   - Known constraints, dependencies, and target dates
   - Existing solution or environment references, when applicable

2. **Developer opens the Developer Delivery Guide**
   - Selects **Review the CSM handoff**
   - Opens **Start Solution Intake**
   - Confirms VS Code, GitHub Copilot Chat, the MGP Delivery agent, and approved tenant tools are available
   - Copies the approved SharePoint project folder link

3. **Developer launches the intake agent**
   - Opens this repository as the active VS Code workspace
   - Selects **MGP Delivery** from the Copilot Chat agent picker
   - Uses the generated intake prompt with the SharePoint folder link
   - The agent reads accessible handoff materials through the approved Microsoft 365 integration
   - The agent reports a setup or permission blocker when it cannot list and read the folder
   - The agent does not infer missing facts or silently broaden scope

4. **Intake agent normalizes the handoff**
   - Produces a completed solution intake
   - Assigns requirement and acceptance-criteria identifiers
   - Separates facts, assumptions, and unknowns
   - Identifies data, access, integration, licensing, records, accessibility, and support concerns
   - Recommends a platform and risk class
   - Determines whether the work targets an existing solution or a new build

5. **Developer and accountable owner review**
   - Resolve or assign missing decisions
   - Confirm the implementation boundary
   - Approve the next lifecycle gate

6. **Delivery workspace is prepared**
   - Existing solution: provide the approved environment/repository retrieval path
   - New solution: create the standard project workspace and implementation plan
   - Create or link the delivery work item

## What the portal does

The static training portal:

- explains the handoff path
- provides the one-time readiness checklist
- validates the SharePoint URL format in the browser
- generates the governed Copilot Chat intake prompt
- links to standards, templates, and playbooks

The portal does **not** authenticate to SharePoint, submit the URL, start Copilot Chat, or directly download or export a Power Platform solution. The URL stays in the browser until the developer copies the prompt into Copilot Chat.

## What requires integration

For the MGP Delivery agent to review tenant content, the developer's Copilot environment needs an approved authenticated integration such as:

- a Copilot or agent experience with an approved SharePoint/Microsoft 365 connector
- Microsoft Graph or a bounded SharePoint connector
- a Power Automate flow that accepts a folder URL and starts the intake workflow

The integration must respect the developer's permissions. It must not expose folders or files the developer cannot already access.

## Implemented first experience

The repository now provides:

1. Project instructions under `.github/copilot-instructions.md`.
2. A selectable agent under `.github/agents/mgp-delivery.agent.md`.
3. Discoverable lifecycle skills under `.github/skills/`.
4. A local readiness checker at `scripts/Test-DeveloperSetup.ps1`.
5. A guided Start Solution Intake page that validates the URL format and generates the prompt.
6. A mandatory human approval gate before architecture or implementation.

The repository does not provide or configure the tenant connection because authentication, consent, permissions, and approved server selection are organization-controlled.

Do not implement direct solution download until the intake result establishes:

- whether an existing solution actually exists
- which environment or repository is authoritative
- whether the developer is authorized to retrieve it
- whether the solution should be exported as managed or unmanaged
- which dependencies and connection references are required
