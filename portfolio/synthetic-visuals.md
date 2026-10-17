# Synthetic Portfolio Visuals

All diagrams below are original, fictional process illustrations. They are not screenshots or reconstructions of pilot systems. Source: synthetic examples authored for this repository. Publication approval for an external venue is still required.

## Before and after process

**Alt text:** Before, a fictional training request arrives as an unstructured message and is manually re-entered into a tracker. After, a structured request is checked against acceptance criteria, validated, and routed to a human owner.

**Caption:** A synthetic example of moving from informal intake to a validated, human-owned workflow; it does not show measured time savings.

```mermaid
flowchart LR
    subgraph Before["Before: synthetic"]
        M[Unstructured request] --> R[Manual re-entry]
        R --> Q[Repeated status checks]
    end
    subgraph After["After: synthetic"]
        F[Structured request] --> V[Validation and acceptance criteria]
        V --> H[Human owner reviews]
        H --> S[Visible status]
    end
```

## Architecture

**Alt text:** A fictional request form sends synthetic data to a structured list, where validation and a human review step precede a status view. No external integrations are shown.

**Caption:** Minimal synthetic architecture with an explicit human decision point.

```mermaid
flowchart LR
    U[Synthetic user] --> F[Request form]
    F --> L[Structured synthetic list]
    L --> V[Validation]
    V --> H[Human review]
    H --> D[Status view]
```

## QA

**Alt text:** Synthetic requirements map to deterministic checks, accessibility review, and a human release decision. A failed check loops through correction and rerun.

**Caption:** A fictional QA path that makes the correction and human release gate visible.

```mermaid
flowchart LR
    R[Acceptance criteria] --> T[Deterministic checks]
    T --> A[Accessibility review]
    A --> G{Human release decision}
    T -->|Fail| C[Correct]
    C --> T
    G -->|Approve| E[Release evidence]
```

## Adoption

**Alt text:** A fictional developer studies an approved example, completes a bounded synthetic challenge, receives peer review, and records feedback for a later revision.

**Caption:** Proposed independent-reuse evidence path; no training completion or independent success is claimed.

```mermaid
flowchart LR
    S[Standard and synthetic example] --> D[Developer challenge]
    D --> P[Peer review]
    P --> F[Feedback and revision]
```

## Outcome evidence

**Alt text:** A baseline and comparable activity are measured with a stated sample, median, range, exclusions, and source before any realized outcome is reported. Projections are shown separately.

**Caption:** Measurement and claim controls; no values or realized benefit are asserted.

```mermaid
flowchart LR
    B[Baseline defined] --> C[Comparable activity]
    C --> M[Sample, median, range, exclusions]
    M --> S[Source and approval]
    S --> R[Realized claim]
    P[Projection] --> A[Assumptions labeled]
```
