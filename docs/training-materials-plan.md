# Training Materials Build Plan

## Objective

Create a polished, developer-friendly Power Desk training portal that captures the full delivery lifecycle: governance, standards, skills, process, QA, operational evidence, and reusable delivery patterns. The final result should be easy to navigate, visually engaging, and publishable through GitHub Pages so new hires and current developers can self-serve the guidance they need.

## Target outcome

A GitHub Pages site that acts as the operating handbook for delivery teams, with:

- a compelling homepage and visual framing
- clear process journeys by workstream
- reusable training modules for each delivery process
- callouts to standards, templates, and operating rules
- examples of quality evidence and success patterns
- a simple search and navigation experience

## Recommended site approach

Use GitHub Pages with a lightweight static site stack:

- Option A: Jekyll theme with markdown-first content and custom styling
- Option B: plain HTML/CSS/JS for full visual control
- Option C: docs-as-code structure using markdown plus a custom site shell

Recommended default: Jekyll or a static site generator with custom theme overrides.
This gives the team a strong balance between maintainability, visual quality, and easy publishing from the repo.

## Content model

Organize the training portal around the repository's existing architecture:

1. Getting started
   - repository overview
   - operating principles
   - how to navigate the standards and skills library

2. Delivery lifecycle
   - opportunity qualification
   - discovery interview using the approved script
   - attributed transcript under approved consent, access, retention, and AI controls
   - Copilot-generated specification draft
   - human refinement and Product Owner specification acceptance
   - developer intake triage and readiness
   - architecture and impact assessment
   - governance and approval
   - build and implementation
   - QA and evidence
   - release and handoff

3. Platform playbooks
   - Power Apps
   - Power Automate
   - SharePoint
   - cross-platform delivery patterns

4. Operational playbooks
   - handoff and review
   - branch strategy
   - agent workflow and assignment matrix
   - release gates and evidence review

5. Operational evidence and improvement
   - success stories
   - metrics and reporting
   - case studies and examples
   - reusable demo materials

6. Reference library
   - skills
   - standards
   - templates
   - checklists
   - governance docs

## Proposed page structure

### Home page

Sections:

- hero message with value proposition
- key delivery outcomes
- quick links to standards, skills, and process docs
- "how to use this site" section
- feature cards for lifecycle, platform guidance, QA, and evidence

### Process pages

Each process page should include:

- purpose and when to use it
- step-by-step flow
- decision points
- roles and responsibilities
- artifacts produced
- quality checks
- examples and templates

### Skills pages

Each skill page should include:

- business problem solved
- trigger conditions
- required inputs
- steps and tool usage
- outputs and handoff materials
- common mistakes and guardrails

### Standards library

A visual index for:

- governance standards
- delivery lifecycle
- platform standards
- QA standards
- evidence schema and verification steps

## Visual design direction

The training portal should feel polished and premium, not like a plain documentation dump.

### Design principles

- clean, generous spacing
- strong hierarchy with clear headings and scannable sections
- high-contrast typography and readable layouts
- card-based navigation for process areas
- icons or simple illustrations for each major workstream
- white-first surfaces with MGP blue accents
- consistent section patterns across pages

### MGP brand system

Use the public brand signals from [mgpinc.com](https://mgpinc.com/):

- official MGP header logo
- primary blue `#007FE8`
- bright blue `#1C91F2`
- deep blue `#094363`
- slate `#46525E`
- white and near-white page surfaces
- Nunito Sans for headings and body copy
- Poppins for navigation
- restrained map, data, technology, and community imagery

Do not substitute branding from MGP Ingredients or another company with the MGP name.

### Suggested aesthetic

Borrow from modern documentation portals and product knowledge hubs:

- visual cards with soft shadows
- subtle gradients and accent colors
- left navigation for major sections
- topic tags and status badges
- screenshots or diagrams where relevant
- strong landing-page storytelling

## Content production plan

### Implemented training architecture

The first training layer now uses progressive disclosure:

1. **Homepage orientation** — explains the four-stage delivery route and provides a future 90-second video location.
2. **Task selection** — asks developers whether they need to start, build, or validate.
3. **Quick-start hub** — provides short task paths at `docs/training/index.html`.
4. **Authoritative detail** — links to the existing standards, skills, templates, and QA artifacts.

This lets an experienced developer open one artifact immediately while giving a new developer enough context to follow the full path.

### Video and onboarding layer

Add a lightweight video and walkthrough layer to the learning experience before expanding into deeper training modules.

- keep orientation videos short and task-based
- place the first video prominently on the homepage for visibility
- reserve a dedicated training section for screenshots and quick-start tour assets
- link each video to a specific task or process path so developers know what to do next

This keeps the portal easy to scan while still leaving room for richer learning assets as the program matures.

### Discovery-to-intake learning objective

After the quick start, a developer should be able to:

- explain the sequence **qualification → discovery interview → attributed transcript → Copilot draft → human refinement → Product Owner specification acceptance → developer triage/readiness → architecture**
- distinguish transcript-supported facts from assumptions, unknowns, and model-generated wording
- explain that recording and transcription require an approved tool, consent and policy compliance, controlled access and retention, and an approved AI processing boundary
- turn one attributed statement into a user story and observable acceptance criterion, then identify what remains for intake
- state that Product Owner specification acceptance confirms accuracy only; it does not authorize build or release

Use a fictional exercise rather than client material: an attributed request-owner statement says that a requester needs missing required information identified before submission. Learners draft the requester story and a Given/When/Then criterion, mark data source and permission details as unknown, obtain simulated Product Owner specification acceptance, and then triage those unknowns before readiness. The exercise ends at architecture entry, not implementation.

### Phase 1: content inventory and gap mapping

- inventory all existing docs in `governance/`, `standards/`, `skills/`, `templates/`, `qa/`, `portfolio/`, and `visuals/`
- identify high-value topics for developer onboarding
- classify content into: must-have, should-have, optional
- trim duplication and merge fragmented guidance

### Phase 2: page architecture and visual design

- define homepage structure
- align page templates to repository content folders
- choose the GitHub Pages stack and theme
- create a shared design system for headings, cards, buttons, and navigation

### Phase 3: content conversion

- convert markdown into a site-ready narrative
- create landing pages for each workstream
- add contextual links to source docs and examples
- package reusable templates and artifact references into simple, digestible modules

### Phase 4: developer onboarding experience

- [x] create a "Start here" path for new contributors
- [x] build a quick-reference section for common tasks
- add process flow visuals and role definitions
- write a brief FAQ for developers and approvers

### Phase 5: polish and publishing

- verify links and navigation
- tune typography, spacing, and responsiveness
- publish to GitHub Pages
- validate readability on desktop and mobile
- gather feedback from a pilot group

## Implementation workflow

1. Confirm repository source structure and site naming.
2. Decide whether to keep everything in a `docs/` or a dedicated `site/` folder.
3. Create the GitHub Pages project structure.
4. Draft the landing page and section templates.
5. Convert the most important content into page-ready modules.
6. Connect the site to the repo so docs stay synced with the source of truth.
7. Publish and refine based on user feedback.

## Suggested repository layout

```text
site/
  index.md
  _config.yml
  assets/
    css/
    images/
  pages/
    getting-started/
    lifecycle/
    platforms/
    qa/
    portfolio/
  templates/
    page-template.md
```

Alternative if the team prefers simpler management:

```text
docs/
  training/
    index.md
    getting-started.md
    lifecycle.md
    platforms/
    qa/
```

## Success criteria

The training portal is successful when:

- a new developer can understand the operating model in under 15 minutes
- each major process has a clear landing page and reference links
- the content is visually clean and easy to scan
- the site is easy to maintain alongside the repo
- the site can be updated with new standards, skills, and case studies without rework

## Immediate next step

Pilot the homepage and quick-start hub with three developers. Ask each person to start a solution, find a platform standard, and locate the release checklist without assistance. Use the results to refine labels before recording the final orientation video.

## Recommended owner model

- content owner: repo maintainers / process leads
- design owner: visual and user experience updates
- technical owner: GitHub Pages deployment and site maintenance
- review cadence: weekly content review with a monthly polish pass

This gives the project a clear path from source content to polished, accessible training materials.
