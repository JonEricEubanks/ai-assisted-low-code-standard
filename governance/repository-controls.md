# Repository Controls

## Current hosting

- Repository: `JonEricEubanks/ai-assisted-low-code-standard`
- Visibility: private
- Default branch: `main`
- Internal evidence: excluded from Git and retained only in approved local/internal storage

## Automated controls

- CODEOWNERS defines accountable review ownership.
- Pull requests use the repository PR template.
- GitHub Actions runs `scripts/validate_repo.py` on pull requests and pushes to `main`.
- Workstream branches and issues provide isolated scopes.
- Branch deletion after merge is enabled.
- Force-push and direct-write restrictions are operating-policy controls until platform protection is available.

## Platform limitation

GitHub branch protection is unavailable for a private repository on the current personal GitHub plan. GitHub returned HTTP 403 and requires GitHub Pro, a qualifying organization plan, or a public repository.

The repository must remain private because it supports internal working practices. Do not make it public merely to obtain branch protection.

## Required interim policy

Until technical branch protection is enabled:

1. No developer or agent pushes feature work directly to `main`.
2. All work is completed on the assigned feature branch.
3. All changes use a pull request and pass the validation workflow.
4. The program owner reviews changes to shared or governed files.
5. Agents never receive a reusable personal access token.
6. Internal/client evidence is never committed.
7. The program owner verifies the PR merge commit and closes the linked issue.

## Preferred future control

Move the repository to the approved MGP GitHub organization or upgrade the applicable plan, then enable:

- Require a pull request before merging
- Require one approval
- Dismiss stale approvals
- Require CODEOWNERS review
- Require `validate` status
- Require conversation resolution
- Require linear history
- Block force pushes
- Block branch deletion

After enabling these controls, capture the repository rules screenshot as governance evidence.
