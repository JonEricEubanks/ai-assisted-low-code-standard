# CSM Handoff to Developer Intake Flow

## Purpose

Define how a qualified opportunity becomes an approved, traceable discovery package and then a developer-ready Solution Brief without requiring developers to manually reconstruct requirements or download disconnected copies of project files.

## Operating flow

1. **CSM qualifies the opportunity**
   - Confirms the opportunity is qualified and identifies the Product Owner and primary stakeholders
   - Defines the discovery objective and expected deliverables
   - Does not begin solution design or promise implementation

2. **Facilitator conducts discovery**
   - Uses the approved discovery script to capture the problem, desired outcome, users, scope, user outcomes, business rules, required information, constraints, assumptions, and open questions
   - Focuses on business needs and observable acceptance criteria rather than screens or technical design
   - Uses recording and transcription only when the meeting tool, consent and organizational policy, participant access, retention handling, and AI processing boundary are all approved
   - Produces an attributed transcript that preserves who said what; uncertain or unattributed statements remain open questions

3. **Copilot produces a bounded draft**
   - Uses the approved transcript and prompt within the approved AI boundary
   - Creates one story per distinct user outcome with testable acceptance criteria
   - Uses only transcript-supported statements
   - Places missing information under open questions and likely-but-unconfirmed statements under assumptions
   - Does not invent architecture, fields, integrations, priorities, metrics, or technical tasks

4. **Humans refine and accept the specification**
   - The facilitator and relevant stakeholders correct attribution, remove unsupported statements, resolve duplication, and make acceptance criteria observable
   - The Product Owner reviews the problem, outcome, users, scope, stories, acceptance criteria, business rules, required information, assumptions, and open questions
   - Product Owner acceptance confirms that the specification accurately captures the need
   - Product Owner acceptance is not authorization to build, release, publish, change access, or make a production change

5. **CSM prepares the SharePoint project folder**
   - Project charter
   - Approved scope and exclusions
   - Product Owner-accepted User Story Specification
   - Attributed transcript or approved transcript reference, with access and retention applied
   - Business owner and sponsor
   - Known constraints, dependencies, and target dates
   - Existing solution or environment references, when applicable

6. **Developer opens the Developer Delivery Guide**
   - Selects **Review the CSM handoff**
   - Opens **Start Solution Intake**
   - Confirms VS Code, GitHub Copilot Chat, the MGP Delivery agent, and approved tenant tools are available
   - Copies the approved SharePoint project folder link

7. **Developer launches the intake agent**
   - Opens this repository as the active VS Code workspace
   - Selects **MGP Delivery** from the Copilot Chat agent picker
   - Uses the generated intake prompt with the SharePoint folder link
   - The agent reads accessible handoff materials through the approved Microsoft 365 integration
   - The agent reports a setup or permission blocker when it cannot list and read the folder
   - The agent does not infer missing facts or silently broaden scope

8. **Intake agent normalizes the handoff**
   - Produces a completed solution intake
   - Assigns requirement and acceptance-criteria identifiers
   - Separates facts, assumptions, and unknowns
   - Identifies data, access, integration, licensing, records, accessibility, and support concerns
   - Recommends a platform and risk class
   - Determines whether the work targets an existing solution or a new build

9. **Developer and accountable owner review**
   - Resolve or assign missing decisions
   - Confirm the implementation boundary
   - Assign **Ready**, **Discovery**, or **Re-scope**
   - When the disposition is **Ready**, obtain accountable developer approval to proceed to architecture
   - Do not treat specification acceptance or intake readiness as build or release approval

10. **Architecture and impact assessment begins**
   - Starts only after a **Ready** intake disposition and accountable developer approval
   - Defines architecture, data ownership, security, licensing, records, support, recovery, integration, and regression decisions
   - Requires its own approval before implementation

11. **Delivery workspace is prepared**
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
- teaches the sequence from qualification through discovery, specification acceptance, intake readiness, and architecture

The portal does **not** record or transcribe discovery sessions, authenticate to SharePoint, submit the URL, start Copilot Chat, or directly download or export a Power Platform solution. The URL stays in the browser until the developer copies the prompt into Copilot Chat.

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

## Practical learning example

Use a fictional request with no client or tenant facts:

1. An approved attributed transcript states: **Request owner:** “A requester needs to submit the required information and see whether anything is missing.”
2. Copilot drafts: “As a requester, I want missing required information identified so that I can correct the request before submission.”
3. A human reviewer confirms the attribution and rewrites the acceptance criterion as observable behavior: “Given a required value is absent, when the requester attempts submission, then the request is not submitted and the missing value is identified.”
4. The Product Owner accepts the specification as an accurate statement of need.
5. Developer triage still records data source, permissions, records and retention, volume, support, and other unknowns before assigning readiness.
6. Architecture begins only after the intake is **Ready** and the accountable developer approves that gate.

The repository does not provide or configure the tenant connection because authentication, consent, permissions, and approved server selection are organization-controlled.

Do not implement direct solution download until the intake result establishes:

- whether an existing solution actually exists
- which environment or repository is authoritative
- whether the developer is authorized to retrieve it
- whether the solution should be exported as managed or unmanaged
- which dependencies and connection references are required
