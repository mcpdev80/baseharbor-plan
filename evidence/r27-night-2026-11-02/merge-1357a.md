# Merge evidence — PR #1357

- Mission: `codex-merge-1357`, ROLLE=MERGE; squash merge authorized by `review-1357n.md` ACCEPT-WITH-DEFERRAL after reading `qualify-14.md`.
- Account: `mcpdev80` (`gh auth status`). No force push, admin merge, or branch protection bypass used.

## Before merge

- PR: https://github.com/mcpdev80/baseharbor/pull/1357
- State: OPEN, draft=false, mergeable=CLEAN, mergeState=CLEAN.
- Exact PR head: `e86d39c0ea3e3c516500b87e4589135fbb50aa78`.
- Base: `develop` at `2cadfcee8161ec087b6f50d80fb41428d414f9df`.
- `git ls-remote` confirmed `refs/heads/work/r27-ci-access-ab` at the exact head and `refs/heads/develop` at the base above.
- PR checks: all required/substantive checks terminal and passing, including `PR Selected Checks` (GitHub App 15368); source run `41763640650` completed success on the exact PR head. Conditional jobs were skipped.
- Planning dependencies were accepted; `qualify-14.md` documents completion of the review deferral.
- Rulesets queried before merge were disabled; no bypass was invoked.

## Merge and after

- Command: `gh pr merge 1357 --repo mcpdev80/baseharbor --squash --match-head-commit e86d39c0ea3e3c516500b87e4589135fbb50aa78`.
- PR state after: MERGED at `2026-11-04T05:25:32Z`.
- Squash commit: `3d08ef72a967704075805a511fb361f30684763b`.
- `git ls-remote` after merge: `refs/heads/develop` = `3d08ef72a967704075805a511fb361f30684763b`; PR head branch was removed.

## Develop run (own run, terminal)

- Workflow `CI · Source & Quality`, run `41779381721`, event `workflow_dispatch`, ref `develop`, head `3d08ef72a967704075805a511fb361f30684763b`.
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/41779381721
- Terminal state: completed / failure at `2026-11-04T05:28:50Z`.
- `Workflow policy` passed. `validate` failed at `Check formatting`; remaining validation steps were skipped.
- Failure output: `gofmt -l cmd internal spec contracts` reported files requiring gofmt. The reported file was `contracts/managementaccess/v1/nonce_crypto_test.go` (see run log for gofmt diff). Documentation validation and workflow syntax validation passed.
- STOP applied per mission: no rerun or follow-up mutation initiated after the newly failed develop check. The merge is complete, but the develop run is not green.

## Hosted-run input check

Before dispatch, inspected `.github/workflows/ci.yml`: `workflow_dispatch` has no user-supplied inputs, pins and environment are defined in the workflow/repository, and the workflow checks out the selected `develop` ref. The run therefore consumed the system-provided merged commit; no lane-supplied token, pin, or environment override was added.
