# Scaling Guide

## Team growth

When another developer joins:

1. Add the developer to the private GitHub repository.
2. Replace or extend the applicable `CODEOWNERS` entry.
3. Assign the developer a workstream issue and branch.
4. Require the first contribution to use the PR template and receive owner review.
5. Record onboarding feedback as an improvement issue.

## Adding another platform

Create:

- `standards/<platform>.md`
- `skills/<platform>-delivery/SKILL.md`
- `workstreams/<platform>/README.md`
- a branch named `feature/<platform>-standard`
- CODEOWNERS coverage
- requirement, plan, task, and validation mappings

Do not add a platform-specific agent until a stable standard and reusable skill exist.

## Repository boundaries

- This repository contains reusable standards and sanitized examples.
- Client/source evidence remains in an approved internal evidence store and is linked by stable IDs.
- Production exports, credentials, tenant URLs, personal data, and client documents are never committed.
- Large generated evidence belongs in controlled artifact storage, not Git history.

## Versioning

- Use semantic tags for approved standard releases, such as `v1.0.0`.
- Skills should record meaningful behavioral changes in PR descriptions.
- Breaking changes require migration notes.
- Pilot-specific changes become standards only after retrospective validation.

## Automation roadmap

1. Repository structural validation
2. Markdown linting and link checks
3. Schema validation for evidence and templates
4. Skill contract tests using sanitized fixtures
5. Platform-specific deterministic test runners
6. Visual comparison and evaluation
7. Bounded computer-use exploration

Each layer must preserve deterministic evidence and human release authority.
