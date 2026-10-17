# Operating Model

## Roles

| Role | Accountable for |
|---|---|
| Program owner | Goal, scope, evidence portfolio, gates, and leadership reporting |
| Solution owner | Business outcome, acceptance criteria, UAT, release decision |
| Solution architect | Architecture, data, integration, security, licensing, and impact decisions |
| Builder | Approved implementation and developer validation |
| Independent reviewer | QA execution, defect classification, and evidence quality |
| Platform/control owners | Environment, DLP, identity, records, accessibility, licensing |
| Successor developer | Independent reuse and handoff verification |
| AI orchestrator | Procedure routing and evidence coordination; never release authority |

## RACI summary

| Activity | Program | Solution | Architect | Builder | QA | Controls | Successor |
|---|---|---|---|---|---|---|---|
| Charter | A/R | C | C | I | I | C | I |
| Requirements | I | A/R | C | C | C | C | I |
| Architecture | I | C | A/R | C | C | C | I |
| Build | I | C | C | A/R | C | I | I |
| QA | I | C | C | C | A/R | C | I |
| Release | I | A | C | R | R | C | I |
| Handoff | C | A | C | R | C | I | R |
| Standard update | A | C | R | R | R | C | C |

## Escalation triggers

- Production access or mutation
- Security role, permission, DLP, retention, or deletion changes
- Premium/custom connector or licensing uncertainty
- Client or regulated data entering an unapproved AI service
- Inability to deterministically validate a critical path
- Missing rollback or support owner
- Vision/computer-use result conflicts with deterministic evidence

