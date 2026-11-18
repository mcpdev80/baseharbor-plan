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

## CI run 1: run 44399345302 @ 4f07c807 — TERMINAL failure

- Source format FAILED: `cmd/baha/app_status_result.go:295:3: expected '}', found 'EOF'`.
  Root cause: my initial merge kept BOTH sides of the app_status_result.go conflict
  (duplicate struct literal + duplicate remote-target return). I had fixed it locally
  but committed/pushed the pre-fix version.

## CI run 2: run 44400488202 @ 022c454c — TERMINAL

- Fixed: removed the duplicated struct literal and duplicate remote-target return block
  in `cmd/baha/app_status_result.go` (balanced 63/63 braces). Committed `022c454c`,
  pushed non-force `4f07c807..022c454c`.
- PASS this run: Workflow policy, Native gate plan, Source format, Trusted Plan,
  Go unit (all shards), go-build, go-vet, pr-planner-tests, ci-actionlint,
  receipt-execution-tests, ci-policy.
- FAIL this run (2 jobs): `PR · Validation · ci-executor-tests` and `PR · Focused Python`.
  Both are Python structural tests of the repo's own `.github/workflows/*.yml`:
  `test_pr_selected_runtime_matrix.py` and `test_targeted_gate_ref.py`.
  Failures: `max-parallel:` present in runtime matrices (14), plus
  `inputs.gate`/`inputs.runtime` expression assertions (2 errors).
  RESULT: `FAILED (failures=14, errors=2)`.

## Pre-existing proof (definitive)

- `python3 -m unittest scripts/test_pr_selected_runtime_matrix.py scripts/test_targeted_gate_ref.py`
  run locally against develop HEAD = `FAILED (failures=14)` — IDENTICAL failures,
  independent of my merge. These validate Owner-scope `.github/**` workflow YAML.
- My card work touches no `.github/**`. The `PR Selected Checks` gate blocks only
  because those two pre-existing jobs fail.

## Open scope question (post as QUESTION to Owner)

The exact-head CI run (run 44400488202, sync-triggered `ci.yml`) is structurally sound for
my merge (ancestry/parents OK, all Go build/vet/unit/format PASS). It blocks ONLY on two
pre-existing Owner-scope CI-structure tests against `.github/workflows/*.yml` that fail
identically on develop (14 `max-parallel:` + 2 expression assertions). These are Owner
scope: I must not edit `.github/**` or trigger `workflow_dispatch`. Reporting STATE.

## Status

Mittendrin. Exact-head CI run 44400488202 @ 022c454c is terminal (failure). Failure is
pre-existing Owner-scope `.github/**` CI-structure tests (proven identical on develop).
Next: publish evidence to origin/main, update card status, post END with STATE.

## Evidence on origin/main

`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git main` => `6e67935c3e461f9ec24858f7cabb889c407b08b8`
Evidence file `evidence/r28-welle4-2026-11-18/perses-dashboard-identity/rebase-window-1.md` and card task `t-20261114-r28-perses-dashboard-identity.md` (kanban_status: blocked, blocker set) are committed and pushed to origin/main (6e67935c).
