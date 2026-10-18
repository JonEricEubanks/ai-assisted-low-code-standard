# Training and Video Roadmap

## Purpose

The training experience should help a developer answer three questions immediately:

1. Where do I start?
2. What do I need for my task?
3. What do I do next?

The content should feel like a guided system, not a documentation dump.

## Core design principles

- Use short task-based entry points instead of long narrative pages.
- Keep the homepage decision-first, not process-heavy.
- Give every major path a direct route to a template, standard, or procedure.
- Reserve long-form references for deeper support.
- Add short video walkthroughs to reduce friction for new users.

## Updated learning structure

### Level 1: Orientation

Use a short overview to explain:

- what the system is
- the lifecycle in four steps
- where to start for common tasks
- where to find templates and standards

Recommended format:

- 60–90 second overview video
- embedded thumbnail on the homepage
- direct link to the overview page or modal

### Level 2: Quick-start journeys

Create short pages for the most common needs.

Recommended quick starts:

- Start a new solution
- Build a Power App
- Build a flow
- Validate a release
- Prepare a handoff
- Navigate the standards library

Each quick start should include:

- when to use it
- required inputs
- next steps
- required templates
- where to go for detail

### Level 3: Deep reference

Keep the detailed standards, skill procedures, QA files, templates, and governance content in the repository as the authoritative source.

Use the homepage and quick starts to route people into the source material rather than duplicating everything.

## Recommended page flow

1. Homepage
2. Task selection page
3. Quick-start page
4. Standards or template destination
5. Optional deep-dive reference

This creates a simple progression without overwhelming the user.

## Video plan

### Video 1: 90-second overview

Goal:

- Introduce the system and show the flow

Outline:

- What the repository is for
- The four-step path: Frame, Build, Validate, Handoff
- How to choose a playbook
- Where to find templates and standards
- What to do next

#### 90-second script and visual sequence

| Time | Narration | Visual |
|---|---|---|
| 0:00–0:08 | “The MGP Developer Delivery Guide gives every solution one clear path from request to handoff.” | Homepage hero and four-stage route |
| 0:08–0:22 | “Start where you are. Choose whether you need to frame a new request, build with a playbook, or validate a change.” | Homepage decision cards |
| 0:22–0:35 | “If you are new, the quick-start hub shows only the inputs, actions, and outputs for your current task.” | Quick-start route selection |
| 0:35–0:50 | “During build, open the standard for your platform. You do not need to read the entire repository.” | Platform standards grid |
| 0:50–1:06 | “Before release, test the requirement, capture evidence, pass the release gate, and transfer ownership.” | Validate and release checklist |
| 1:06–1:20 | “If you already know what you need, jump directly to a template, standard, procedure, or workflow.” | Homepage resource index |
| 1:20–1:30 | “Build clearly. Test visibly. Hand off confidently.” | MGP closing panel |

Production requirements:

- 1920×1080 recording canvas
- 30 frames per second
- captions and transcript required
- no autoplay when embedded
- cursor highlight only when selecting a route
- narration pace of approximately 135 words per minute
- host internally in Microsoft Stream or SharePoint unless public release is approved

### Video 2: Review a CSM handoff

Goal:

- Show how to begin from the approved SharePoint project folder

Outline:

- confirm the charter, scope, user stories, and owner are present
- copy the SharePoint project folder link
- launch the intake agent with the folder reference
- review normalized requirements, gaps, and risk
- route to the correct platform and existing/new solution path

### Video 3: Build using a playbook

Goal:

- Turn the standards into a simple execution path

Outline:

- open the relevant playbook
- identify required standards
- follow the lifecycle checkpoints
- document evidence during build

### Video 4: Validate and release

Goal:

- Show how to test, review, and release with evidence

Outline:

- run the validation checklist
- capture evidence
- complete the release checklist
- prepare the handoff package

## Screenshot plan for video production

Capture section-focused screenshots at a consistent 1440-pixel browser width. Compose them on a 1920×1080 video canvas during editing. Store them under `docs/assets/training-video/`.

| Sequence | Asset | Purpose |
|---|---|---|
| 1 | `01-homepage-hero.png` | Establish the guide and four-stage route |
| 2 | `02-homepage-playbooks.png` | Show platform-specific entry points |
| 3 | `03-homepage-resources.png` | Show direct access for experienced developers |
| 4 | `04-training-task-flow.png` | Introduce the three quick-start routes |
| 5 | `05-training-release-checklist.png` | Demonstrate the release sequence |
| 6 | `06-training-standards.png` | Demonstrate focused platform standards |

Screenshot rules:

- use the same browser width and zoom
- exclude browser chrome and personal information
- keep the MGP header or section title visible for context
- avoid hover states unless the narration explicitly discusses one
- recapture screenshots whenever the page structure changes materially

## Production sequence

1. [x] Finalize the homepage layout and quick-start card structure.
2. [x] Build the task-focused quick-start hub.
3. [x] Capture the six storyboard screenshots.
4. Validate labels and flow with three developers.
5. Produce the overview video first.
6. Add the video URL and transcript to the homepage.
7. Add additional short videos only where usability testing identifies confusion.

## Success criteria

The training system is successful when a developer can:

- understand the purpose of the site in under 30 seconds
- identify the correct starting point in under 30 seconds
- find a template or standard without reading long pages
- see the next step clearly after completing a task

## Immediate next action

Add the short overview video and quick-start cards to the homepage, then validate the visual flow with a quick dev walkthrough before building more training content.
