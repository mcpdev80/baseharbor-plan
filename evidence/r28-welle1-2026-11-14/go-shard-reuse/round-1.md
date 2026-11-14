# round-1 — 0427-185 CI Go shard-reuse (mission 0427-185)

Lane: `lane-0427-185-go-shard-reuse` · Model: worker-ornith1.5 · Date: 2026-11-14

## Bases (git ls-remote, before first commit)

```
origin/main       -> 334ff1a14cf7cbe4cac09af07f00ea74a43f0aa7
origin/develop    -> 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
planning origin   -> https://github.com/mcpdev80/baseharbor-plan.git
```

Planning repo verified at `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT `workers/baseharbor-plan`).
`git ls-remote origin develop` returned `0e9ccb582...`; mission basis `0e9ccb582` confirmed.

## Task

0427-185 `t-20261109-r27-ci-go-shard-reuse` — reuse green Go shards on successive PR commits when
exact unchanged coverage is cryptographically/auditably proven. Depends on #1519 (shards, merged
`4d827a55cb115f316c074b2e1d72d077fc577637`, develop head `0e9ccb58`).

## Feasibility finding (measured on develop 0e9ccb58)

- Shard reuse is ALREADY integrated on develop. Files present:
  - `scripts/pr-incremental-reuse.py` (trusted incremental planner + final gate).
  - `scripts/pr-go-unit-shard.py` (fail-closed sharder; modes `cli-0/cli-1/cli-2/cli-3/packages`,
    `CLI_SHARDS = 4`, owner-loan cohort, `REQUIRED_CLIENT_TESTS`).
  - `scripts/test_pr_incremental_reuse.py`, `scripts/test_pr_go_unit_shard.py` (regressions).
- `pr-incremental-reuse.py` reuse mechanism (lines 243-268, `filter_selected`): a previous **exact**
  PR run whose prior head is an ancestor of the current head, with identical immutable base, may
  reuse only `conclusion == "success"` completed jobs. `impacts()` (lines 209-237) returns True
  (re-run) for unknown scopes, Go changes under sensitive prefixes, changed Go/Python/doc, changed
  toolchain via `go list -deps`; unknown impact fails closed. Skipped/failed/pending/cancelled are
  never reused.
- `PR · Selected Checks` aggregation is fail-closed: a missing proof for a required shard blocks the
  gate; skipped is not success.

## Mission vs reality mapping

- Mission matrix: `cli-{0,1,2}`, `packages`, `owner`.
  - `cli-0/1/2`, `packages` — present (plus `cli-3`).
  - `owner` — NO shard named `owner` exists. The real construct is the **owner-loan cohort**
    (`deployment_owner_loan_regression_test.go` in `cmd/baha`, 7 regressions, `owner_loan_cohort()`),
    kept in one shard because Go test ordering over a shared fixture is observable.
  - The acceptance's `owner` shard is best read as this owner-loan cohort; the exact label differs.
- The referenced decision doc `decisions/2026-11-09...` (CI Go shard-reuse) does NOT exist in the
  planning repo — only `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md` exists.
  The card instead cites `decisions/2026-11-14-owner-close-inherited-work.md`.

## CONTRADICTION (Owner variant 3 — report only, no card change)

- Owner decision `2026-11-14-owner-close-inherited-work.md` (status: **accepted**), line 8:
  "Cards 012, 046, 053, **185** and 187 are accepted by explicit Owner direction... This records
  the Owner's statement and decision; it does not assert an independently reproduced test, an exact
  candidate SHA, or newly verified CI evidence."
- Card `t-20261109-r27-ci-go-shard-reuse.md` still has `kanban_status: active` (line 11), mirrored in
  `views/releases/v0.4.28.md` line 32 and `views/overview.md` line 29.
- develop (0e9ccb58) carries the already-integrated reuse (see finding above).

## Owner decision (2026-11-14, variant 3)

"Documente the contradiction precisely in round-1, leave the CARD UNCHANGED (no status/resolution
edits — board cleanup is a coordinator/Owner action), post END_BLOCKED with the one line
'zur Owner-annahme bereit, nichts zu tun'. No new branch, no run, no change."

Applied exactly. No branch cut, no CI run, no card/board edit.

## Merge-frost (mission)

- NO merge onto develop. PR only as DRAFT, base develop. No merge command, no develop-fortschreiben.
- Review + pushes on my AST allowed; pull_request runs proceed. Ignition-defekt: if the suite
  is absent, report the head — Owner finishes manually.

## Repo-rule compliance

- .github/** = Owner scope. Will NOT edit, rerun, or workflow_dispatch. A failing check is reported
  as STATE (check name + failing log line) and stopped.
- No subagents. Evidence only in planning repo. No product-repo operational text.

## TODO / PLAN

- Read mission, task card, decisions.
- Verify planning root + bases via git ls-remote.
- Inspect real shard-reuse implementation on develop.
- Map mission matrix to the real sharder.
- Document feasibility.
- Post ONE scope-question to Owner (act vs close-by-acceptance).
- Apply Owner decision.
- Write + push evidence to origin/main before END.

## STATUS

Resolved by Owner variant 3 — contradiction documented, card left unchanged. No scope action taken.

## END

END_BLOCKED mission-shard185.md: feasibility done, reuse already integrated on develop; one scope-question posed (act vs close-by-Owner-acceptance) — awaiting input.
