# Worked Example — Cross-Department Inspection Workflow

Sanitized from a real submitted Project Scope Intake Form. Client name, personal names, email addresses, and phone numbers removed. The substance is unchanged because the substance is the teaching value.

**Why this example was chosen:** the form reads like a modest departmental request. It scores XL complexity and High risk. That divergence is the entire point of triage.

---

## Source summary

A municipal client requests a repeatable shared process for managing annual commercial and multifamily building inspections across two departments. Today there is no centralized workflow, the departments use separate systems that do not communicate, and there is limited visibility into inspection status, enforcement actions, and historical records.

Deliverable recorded as: *Other — M365 Solution*.
Constraints recorded as: *None*.
Target completion date: *blank*.

For this sanitized example, the submitted scope form is registered as `SRC-01`. The numbered narrative requirements below use stable `IR-##` identifiers and cite `SRC-01`; a live intake would also retain a paragraph, section, or transcript timestamp locator.

---

## Stage 1 — Four-bucket parse

### Confirmed facts

- Annual inspections of commercial and multifamily properties
- Two departments involved: Fire, and Community Development
- No centralized workflow exists today
- Current departmental systems do not communicate
- All current processes are manual
- No internal databases or external vendor platforms involved
- Deliverable is a Microsoft 365 solution
- Desired start date equals the submission date

### Implied requirements

Every item below appears only in narrative success-criteria text. None appear in a structured field. This is typical.

| ID | Implied requirement |
|---|---|
| IR-01 | Both departments access the same system with shared visibility |
| IR-02 | Inspection status and history visible across departments |
| IR-03 | Inspections completed on iPads in the field |
| IR-04 | Checklist-driven pass/fail or yes/no responses |
| IR-05 | Minimal manual data entry |
| IR-06 | Identify properties awaiting inspection, completed, failed, and requiring enforcement |
| IR-07 | Track and manage annual inspection cycles |
| IR-08 | Notify Community Development when a follow-up-requiring inspection completes |
| IR-09 | Generate reminders when inspections become due |
| IR-10 | Failed inspections move into enforcement and adjudication |
| IR-11 | Track compliance, fines, court actions, and case resolution |
| IR-12 | Attach photos as evidence |
| IR-13 | Require photo documentation on failed items |
| IR-14 | Documentation supports code enforcement and adjudication |
| IR-15 | Maintain master inventory of commercial and multifamily properties |
| IR-16 | Store inspection history, notes, contacts, photos, and outcomes in one place |
| IR-17 | Preserve organizational knowledge regardless of staff changes |

### Assumptions a developer would otherwise make silently

Each of these is recorded rather than adopted.

- Property is the master entity and inspections hang from it
- One inspection cycle per property per year
- Inspectors are licensed internal users
- iPads are organization-managed devices
- Field connectivity is reliable
- Adjudication tracking lives in M365 rather than integrating with a court case system
- A usable property list exists and can be imported

### Unknowns

- Target completion date
- Which department owns the solution after go-live
- Whether inspection and enforcement output constitutes an official record, and the applicable retention schedule
- Evidentiary standards for photos used in adjudication
- Source, format, and volume of the property inventory
- Whether an inspection checklist already exists, and whether one checklist or several
- Cross-department visibility and edit boundaries
- Whether adjudication must integrate with an existing court or case system
- Whether fines and payments are tracked, calculated, or collected
- iPad management and licensing position
- Whether historical inspection data must migrate

---

## Stage 2 — Silent gaps

| Field | State | Interpretation |
|---|---|---|
| Target completion date | Blank | Not "flexible." Unasked. |
| Objective categories | None checked | Narrative indicates process improvement, system implementation, and compliance. Confirm. |
| Estimated analyst hours | Blank | No effort position exists yet. |
| Vendor coordination | Neither Yes nor No | Unanswered. |
| Existing project impact | Neither Yes nor No | Unanswered. |
| Risk categories | None checked | Contradicted by the narrative. Enforcement and adjudication imply compliance and legal risk. Unclear requirements also apply. |
| Constraints | "None" | Not credible for a public-sector client handling enforcement records. |
| Requester contacts | Two names, one shared email address | Likely transcription error. Confirm before relying on either contact. |

**Teaching point:** the structured sections of this form contain almost no usable requirements. The narrative contains seventeen. A process that triages only the checkboxes would conclude this is a small reporting request.

---

## Stage 3 — Scoring

### Complexity

| Dimension | Score | Basis |
|---|---|---|
| Entities | 3 | Property, Inspection, Checklist Item, Enforcement Case, Contact, Photo evidence |
| Personas | 3 | Fire inspector, CD inspector, enforcement staff, adjudication/clerk, supervisor |
| Departments | 1 | Two |
| Process stages | 3 | Due → assigned → inspected → pass/fail → follow-up → enforcement → adjudication → resolution, with branching |
| Device surface | 2 | iPad field work is primary; offline position unknown |
| Integrations | 2 | Multiple M365 services |
| Media | 3 | Mandatory evidentiary photos, likely generated notices |
| Scheduling | 3 | Annual cycle plus due reminders and escalation |
| Reporting | 2 | Cross-status visibility for both departments |
| Migration | 2 | Existing property inventory, volume unknown |
| **Total** | **24** | **Tier XL** |

### Risk

**High.** Triggered by:

- Output feeds enforcement and adjudication action
- Likely records-bearing under public-records obligations
- Fines and court actions imply financial and legal exposure
- Photos used as evidence carry evidentiary handling requirements

Records-bearing: **yes, pending confirmation.**
External-party exposure: **unknown — property owners may receive notices.**

### Consequence

Per the scoring standard, **XL requests are not estimated as a single unit.** This request is phased before any estimate is produced.

---

## Stage 4 — Recommended shape

Phase 1 only. Later phases are named but not designed.

| Component | Forcing requirement |
|---|---|
| Property list | IR-15 — master inventory with independent lifecycle |
| Inspection list | IR-06, IR-07 — inspections have their own status and annual cycle |
| Checklist Item list | IR-04, IR-13 — per-item pass/fail with conditional photo evidence |
| Evidence document library | IR-12, IR-14 — binaries used as enforcement evidence need versioning and retention |
| Reference list | Rule: repeated values across lists need one auditable source |
| Canvas app, role-aware | IR-01, IR-03, IR-05 — field tablet work with persona separation |
| Event-triggered flow | IR-08 — notify on completion requiring follow-up |
| Scheduled flow | IR-09 — due and overdue reminders on an annual cycle |

**Deferred to Phase 2:** enforcement case management, adjudication outcome tracking, fines, court actions, and case resolution. Reason: IR-10 and IR-11 depend on a records decision, an external-integration decision, and a financial-handling decision that are all currently unknown.

**Not recommended:** Dataverse at this stage. No requirement yet forces it. Revisit if property or inspection volume, row-level security, or relational integrity requirements emerge during discovery.

---

## Stage 5 — Acceptance criteria

| Stable ID | Criterion | Source and locator | Status |
|---|---|---|---|
| US-001-AC-01 | A Fire inspector and a Community Development user both retrieve the same property's inspection history from one system | `SRC-01`: IR-01, IR-02 | Phase 1 |
| US-002-AC-01 | An inspector completes a full inspection on a tablet without free-text entry except notes | `SRC-01`: IR-03, IR-04, IR-05 | Phase 1 |
| US-002-AC-02 | A failed checklist item cannot be saved without at least one attached photo | `SRC-01`: IR-13 | Phase 1 |
| US-001-AC-02 | A user filters properties by awaiting, completed, failed, and enforcement-required | `SRC-01`: IR-06 | Phase 1 |
| US-003-AC-01 | The system identifies properties whose annual inspection is due or overdue | `SRC-01`: IR-07, IR-09 | Phase 1 |
| US-003-AC-02 | Community Development receives a notification when an inspection requiring follow-up completes | `SRC-01`: IR-08 | Phase 1 |
| US-002-AC-03 | Photos are retrievable against the originating inspection item with capture date intact | `SRC-01`: IR-12, IR-14 | Phase 1 |
| US-001-AC-03 | A master inventory of commercial and multifamily properties exists with history, notes, and contacts | `SRC-01`: IR-15, IR-16 | Phase 1 |
| US-001-AC-04 | A new staff member locates a property's full inspection history without assistance from prior staff | `SRC-01`: IR-17 | Phase 1 |
| US-004-AC-01 | A failed inspection initiates an enforcement case | `SRC-01`: IR-10 | **Deferred — Phase 2** |
| US-004-AC-02 | Compliance, fines, court actions, and resolution are tracked to closure | `SRC-01`: IR-11 | **Deferred — Phase 2** |

Deferral reason for US-004-AC-01 and US-004-AC-02 recorded as: dependent on unresolved records, external-integration, and financial-handling decisions.

**Nothing from the narrative was dropped.** Seventeen implied requirements map to eleven criteria, two of which are explicitly deferred.

---

## Stage 6 — Tier 1 questions

Capped at eight. Routed by role.

| # | Question | Route to |
|---|---|---|
| 1 | Which department owns this solution after go-live, who is the named backup, and who decides when the two departments disagree on process? | SDM + both department heads |
| 2 | Are inspection records, photos, and enforcement documentation official records, and what retention schedule applies? | Village clerk / records officer |
| 3 | Do photos used in adjudication carry evidentiary handling requirements such as unalterability or chain of custody? | Legal / adjudication officer |
| 4 | What must each department be able to view versus edit in the other department's inspection data? | Both department heads + IT |
| 5 | Does enforcement and adjudication tracking need to integrate with an existing court or case system, or is M365 the system of record for case outcomes? | Community Development + IT |
| 6 | Are fines and payments recorded, calculated, or collected within this solution? | Finance |
| 7 | Where does the property inventory exist today, in what format, and how many records? | Community Development |
| 8 | Are the iPads organization-managed with licensed accounts, and is connectivity reliable at inspection sites? | IT |

Not asked this round — deferred to round two: checklist content, notification channel and escalation, historical migration, volume and concurrency, reporting needs.

---

## Disposition

**Discovery, with mandatory phasing.**

Reasoning:

1. Direction is sound and the business problem is clearly articulated.
2. Complexity scores XL. The standard prohibits estimating XL as a single unit.
3. Risk is High and three High-risk triggers have no recorded position.
4. Eight Tier 1 questions are open, five of which change the architecture.

Recommended next action: a scoped discovery session covering ownership, records, cross-department permissions, and the adjudication boundary — then a Phase 1 estimate covering AC-01 through AC-09 only.

---

## Risk register seed

| Risk | Impact | Owner |
|---|---|---|
| Records obligation discovered after build | Rework of storage, retention, and export | Records officer |
| Adjudication requires external case-system integration | Phase 2 scope and cost change materially | Community Development |
| Field connectivity unreliable | Offline requirement changes app architecture | IT |
| Property inventory incomplete or unusable | Migration effort unbounded | Community Development |
| Cross-department permission disagreement | Blocks release | SDM |
| Photo evidentiary standard not met | Enforcement actions challenged | Legal |

---

## What this example demonstrates

1. The structured form fields produced almost no requirements. The narrative produced seventeen.
2. "Constraints: None" was wrong. Four constraints surfaced within one triage pass.
3. No risk box was checked on a request feeding court proceedings.
4. A request that reads as a departmental tracker scored XL and High.
5. Phasing was derived from unknowns, not from preference.
6. Two success criteria were deferred — explicitly, with reasons, in writing.
7. Estimating this form on submission would have produced a materially wrong number.
