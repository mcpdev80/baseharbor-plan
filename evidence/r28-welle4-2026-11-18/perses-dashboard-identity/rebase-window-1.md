# 0428-078 perses dashboard identity — rebase window 1

Mission: mission-078-retarget.md (Karte t-20261114-r28-perses-dashboard-identity, 0428-078, PR #1650).

## Goal

Retarget PR #1650 (head `325ab0d4f`) from its original base lane-0428-080 onto `develop`, re-verify the full diff, get a fresh exact-head CI run to terminal, and deliver a complete diff + fresh evidence. No merge, no force, no `.github/**` edits, no subagent.

## Scope boundaries (from mission + card owner decision 2026-11-18)

- No `.github/**` edits, no reruns/workflow_dispatch.
- No merge of lanes, no force-push, no subagent (§4.8).
- tmp /var/tmp only for scratch; worktree under /tmp/opencode or /tmp.
- One integration candidate per chain: keep working on the PR #1650 head.
- Report any needed `.github/**` CI trigger change as a finding with file:line, never edit.

## Reality witnesses (measured via `git ls-remote` in my own clone)

- Planning repo root (verified): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Planning `origin/main`: `e77d28a45fd546b0cd07e367e642dba0b74d63a9`
- baseharbor `develop`: `907f16713cbf38693d30c9dadaad7fe299759219`
- PR #1650 head: `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d` (refs/pull/1650/head)
- base-lane-0428-080 merged into develop since 409444854 (per card), so no prerequisite remains.
- `325ab0d4f` is NOT an ancestor of develop (confirmed `git merge-base --is-ancestor`).
- merge-base of develop and PR #1650 head: `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95` (PR #1624).

## Base attestation

- Cutoff SHA for the PR head branch: `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`.
- develop base SHA: `907f16713cbf38693d30c9dadaad7fe299759219`.
- I will show `325ab0d4f` is an ancestor of my first commit after merge, and my git log lists only my own commits.

## Work plan

1. Reality check: confirm develop, PR #1650 head, card state (done above).
2. claim via plan.py (if available / in-scope).
3. Retarget PR #1650 onto develop: `gh pr edit 1650 --base develop`.
4. `git merge origin/develop` on the PR #1650 head branch (normal merge, no force). develop-structure-wins + port own identity additions (1602-rule). Resolve any genuine conflict with the trusted-plan gate (longer theme) => STOP + recipe, no bypass attempt.
5. build / vet / gofmt + identity/perses tests green.
6. Push via refspec + ls-remote witness + git-show HEAD completeness (108-rule).
7. Run exact-head CI to terminal (Eigenes-run-pflicht); record run ID and status.
8. Evidence file + END + GUI todos.

## Status

Mittendrin. Next: step 2-3.

## Evidence on origin/main

TODO: paste `git ls-remote origin main` before END.
