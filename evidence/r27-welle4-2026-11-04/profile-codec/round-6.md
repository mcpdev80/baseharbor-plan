# CODEX-WORKER w133 — profile codec round 6

Card: `t-20261018-r27-profile-codec`; PR #1363; branch `work/r27-profile-codec`; owner/coord f49a3303.

## PLAN

1. Refresh PR head, remote branch, develop ancestry, existing worktrees, and the round-5 review/evidence. Preserve the stale local branch ref and all other sessions.
2. On exact remote head `064ba01820bd6544705a27b87748ad91583b67d7`, repair `atomicCommit` to use exactly one injectable write and fail on a real `n < len(data)` before Sync/Rename; prove typed failure, measured prefix, no final file/temp.
3. Close the six other review points: false trust switch counterprobe; full serialized round-trip with nonempty export descriptor; canonical full field order/golden bytes; per-category canaries; deterministic replace-cleanup failure and on-disk state; EN/DE specifications in parallel.
4. Keep all edits within `contracts/managementaccess/v1` and the paired credential-access specifications. Read-only grep proves production consumer boundary; do not edit workflow, CLI, or delivery code.
5. Run focused recipe tests and package tests, go build, go vet, gofmt. Commit once on the existing remote candidate lineage and push fast-forward to the existing PR branch.
6. Verify exact `ls-remote`, `develop` ancestry and name-only diff. Observe exact-head hosted checks to terminal and record run IDs/statuses.

## Base and candidate

Pending.

## Findings and proof blocks

Pending.

## Hosted checks

Pending.

## repo-rule compliance

No second branch or PR, no merge, no subagents, no workflow changes, no removed tests. Worktree is under `/tmp`; unrelated local branches/worktrees remain untouched. This file contains no checklist checkbox syntax.
