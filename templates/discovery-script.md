# Discovery Script

Use this public-safe conversation guide to capture business needs and user outcomes. Discovery supplements intake; it does not authorize architecture, build, production change, or release.

## Session information

- Project:
- Product Owner:
- Facilitator:
- Date:
- Participants and roles:
- Approved source ID for transcript/notes:

## Before capture

- [ ] The meeting platform, recording, and transcription features are approved.
- [ ] Participants received the required notice and consented, or approved non-recorded notes will be used.
- [ ] Data classification is recorded.
- [ ] The proposed content is permitted inside the approved AI boundary; excluded content is identified.
- [ ] Recording, transcript, notes, prompts, and generated drafts have named owners, approved storage/access, retention, and disposal rules.
- [ ] External participants and sharing restrictions are recorded.

If any check is unresolved, do not record, transcribe, or submit the content to AI. Use an approved alternative or escalate.

## Opening

Explain that the session will answer four questions:

1. What problem are we solving?
2. Who will use the outcome?
3. What must users be able to accomplish?
4. What limits, dependencies, and unknowns apply?

State that any approved recording or notes will support a draft User Story Specification. Product Owner acceptance will confirm accuracy only and will not approve architecture, build, production change, or release.

## 1. Business need

- What is difficult today, who is affected, and why does it matter?
- What observable outcome would demonstrate improvement?
- What current process or system is affected?

Playback: “Today, [users] experience [problem and impact]. Success means [observable outcome]. Is that accurate?”

## 2. Users and ownership

- Who performs the work day to day, and what must each role accomplish?
- Who owns the business process and solution after go-live? Who is the backup?
- Who approves scope changes, supports users, and handles escalation?
- Will external or public users view, enter, or receive information?

Playback each role and goal.

## 3. User outcomes

Describe outcomes, not screens or technical design.

- What are the must-have outcomes?
- What must the product prevent, validate, or handle?
- What is explicitly out of scope or optional?

For each distinct outcome, confirm:

> As a [role], I want [capability], so that [business value].

Then elicit only the acceptance scenarios needed to remove ambiguity:

- Given what starting condition,
- when what action or event occurs,
- then what observable result proves success?
- What permission, validation, exception, or failure behavior matters?

Assign stable IDs in the draft (`US-001`, `US-001-AC-01`); do not reuse retired IDs.

## 4. Controls and delivery constraints

Ask explicitly:

- What data is entered, viewed, generated, or received; where does it originate; and what is its classification?
- Is any content an official record, subject to retention, legal hold, public-records, or disposal requirements?
- Who may view or edit each category of data?
- What volumes, growth, concurrency, peak periods, attachment sizes, and processing windows apply?
- Which devices, operating systems, orientations, connectivity/offline conditions, and assistive technologies must be supported?
- What accessibility baseline and additional user needs apply?
- What systems, people, vendors, projects, or decisions are dependencies?
- What licensing, premium capability, or recurring cost may apply, and who approves it?
- Who supports the outcome, maintains connections/reference data, receives alerts, and handles escalation?
- What deadlines, calculations, approvals, permissions, security rules, and status changes apply?

Record unknowns with an owner and decision date. Do not turn an unknown into an assumption.

## Confirm and close

- Play back the problem, outcome, users, scope, stories, and acceptance criteria.
- Confirm business rules, required information, source systems, constraints, dependencies, assumptions, and open questions.
- Identify who will review the draft for accuracy.
- Explain that source attribution will be preserved and unsupported statements will remain assumptions or questions.

## Facilitator check

- [ ] Focused on user needs and business outcomes, not design.
- [ ] Used a real example where an answer was unclear.
- [ ] Separated must-haves from optional items.
- [ ] Assigned an owner to every material question.
- [ ] Captured source timestamps or note-section locators.
- [ ] Covered classification, records, external access, volume, devices, accessibility, licensing, and support.
- [ ] Repeated the approval distinction before close.
