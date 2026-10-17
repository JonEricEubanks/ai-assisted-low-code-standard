# Foundry Visual Validation Evaluation

## Purpose and status

This document defines a design-time evaluation protocol for supplemental screenshot review by an approved Foundry vision model. It does not approve a model, project, identity, dataset, pilot, or release decision. No Foundry evaluation has been run and no labeled evaluation artifact is approved or included.

Keep the Foundry tasks in `BACKLOG.md` open until the deterministic evidence contract is stable and the applicable control approvals are recorded. In particular, do not treat this protocol as evidence that those prerequisites or approvals exist.

## Evaluation boundary

- Evaluate only screenshots from stable, identified, non-production journeys using synthetic data and an approved visual baseline.
- Limit the scope to alignment, clipping, overlap, missing labels, blank states, responsive rendering, and differences from the approved baseline.
- Run deterministic checks first. Vision review is supplemental and cannot override deterministic results, establish functional correctness, verify data or permissions, certify accessibility, or make release decisions.
- Keep the vision reviewer read-only. Do not enable computer-use actions as part of this evaluation.
- Route uncertain, conflicting, or out-of-scope observations to an independent human reviewer as `review-needed`.
- Do not include client data, production screenshots, credentials, tokens, tenant identifiers, or unapproved artifacts.

## Labeled evaluation set

Create the set only after data-boundary, classification, retention, and artifact approvals are recorded.

1. Capture representative synthetic screenshots from the approved journeys, including both known visual defects and no-defect examples across the supported viewports and states.
2. Assign each screenshot a stable case ID and record its requirement, test, solution version, environment, viewport, state, approved baseline, and artifact classification.
3. Have two reviewers label each case independently using the visual criteria above. Record the defect category and affected region where applicable; resolve disagreements through a named adjudicator before scoring.
4. Separate any development/tuning cases from a held-out evaluation set at the journey or scenario level to avoid near-duplicate screenshots crossing the split.
5. Preserve the labels, adjudication, model/deployment and skill versions, prompt/configuration, and artifact references under approved retention. Do not commit raw screenshots or internal evidence to this repository.

## Measurements and disposition

Compare model observations with the adjudicated labels and the deterministic and human review results. Report counts and rates for false positives and false negatives, precision and recall overall and by defect category, and the number of uncertain (`review-needed`) observations. Retain the confusion counts so the rates can be independently checked.

No numeric acceptance threshold is approved by this document. The control owner and QA owner must define and approve thresholds before evaluating the held-out set. Any missed high-impact defect, unresolved label disagreement, provenance gap, or result that conflicts with a deterministic check blocks a favorable evaluation disposition and requires human review. Report results as supplemental evaluation evidence, never as an automated release gate.

## Evidence and stop conditions

Map each run to the required fields in `qa/evidence-schema.md`, including stable evidence and run IDs, requirement and test IDs, exact solution/environment context, executor, model/skill version when AI is used, timestamp, expected and actual observations, artifact references, independent reviewer, classification, and retention tag. Proposed visual-specific fields (such as case ID, baseline reference, finding category, region, confidence, and adjudication) must not be presented as part of the approved schema until the evidence contract is updated and approved.

Stop and mark the run blocked or review-needed if the screenshot or baseline lacks provenance, the model/configuration differs from the approved evaluation setup, synthetic-data constraints cannot be verified, artifacts violate classification or retention rules, or review conflicts with deterministic evidence. Preserve the reason and do not infer a pass from missing or unusable evidence.

## Unresolved decisions

- Evidence-contract owner and approval of machine-readable schema changes, including whether to add visual-specific fields.
- Approved Foundry project, model/deployment, identity, network boundary, logging/tracing, consumption budget, and kill switch.
- Dataset owner, approved synthetic scenarios, label rubric, independent reviewers, adjudicator, and evaluation-set size/split.
- QA and control-owner-approved thresholds, including treatment of high-impact false negatives and uncertain findings.
- Artifact classification, storage location, retention period, and approval record for labeled cases and evaluation outputs.
- Threat-review completion and the human owner authorized to accept the evaluation disposition before any pilot.
