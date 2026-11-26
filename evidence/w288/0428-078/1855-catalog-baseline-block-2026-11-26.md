# w288 — PR #1855 (card 0428-078) catalog-block akte

Card **0428-078**, product repo `baseharbor`, PR **#1855** (draft=false, base `develop`, head `572d64891d27bb72caa748c5c7611663463836a7`).
Lane `w288-0428-078-1855fix`. Worker identity `w288-0428-078-1855fix`.
Date 2026-11-26 (host clock, corrected by owner: the 04:31Z stamp on the row directive was void; the
host read 04:27Z; the binding directive resolves to 2026-11-26T04:26Z).

## Objective (restated by owner 04:07Z, corrected 04:26Z)
Correct three Codex-review findings on PR #1855 in the product candidate, then qualify it with
two distinct hosted `pull_request` runs on the SAME final head. The candidate carries the **content
fix only**; the catalog baseline that makes the new tests executable in hosted CI is a **separate
baseline PR** routed by Codex w267.

## Content fix — COMPLETE on head 572d64891
- `internal/metrics/perses_dashboards.go`: Perses identity dashboard definition + no-data + real-queried identity fixtures.
- `internal/metrics/identity_dashboard_witness.go:145-154`: per-Target registration binding now includes the Target (state-root + keycloak:9000 endpoint guards).
- `cmd/baha/app_identity_dashboard_status_test.go`: no-data + real-queried identity CLI fixtures.
- `internal/metrics/identity_dashboard_witness_test.go`: witness unit fixtures.
- Production derivation fixed; no test-expectation edit, no skip/deletion/narrowing.
- Zero local test execution on host (gofmt/vet/build prechecks only).

## The catalog rule (the blocker)
The trusted PR-gate planner reads the **BASE catalog** (`.github/workflows/ci.yml:865-876`, immutable trusted base)
to select gates. A candidate-side catalog addition is **never trusted**, ever: the trusted planner fails
closed on an uncataloged source change with no declared runtime gate owner. Adding test/catalog rows to the
product candidate and calling CI green is explicitly forbidden by the owner. The catalog rows belong in the
separate baseline PR (Codex w267), not here.

## Three failure records — VERBATIM

### 1. Run 45752959319 — head **7d805dc6bbd6df2636d1b51999f3af53b989a676** (attempt=1, pull_request)
Failing jobs: `PR · Trusted Plan` (job 139684831988) and `PR Selected Checks` (139684969682, cascade).
Verbatim validator line:
```
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/app_identity_dashboard_status_test.go (id source...)
```
Conclusion: candidate-side test-file additions are not trusted; the trusted planner reads the base catalog.

### 2. Run 45755906112 — head **123666c82250617b49a2daa8b17a943e3c811538** (attempt=1, pull_request)
Added two catalog rows to the candidate (`scripts/pr-gate-plan.py` `NATIVE_TEST_GATE_COMPONENTS` + `scripts/pr-gate-coverage.json`
components), then failed again with the identical ValueError on `cmd/baha/app_identity_dashboard_status_test.go`.
Conclusion: same — candidate-side catalog additions are never trusted.

### 3. Run 45756612395 — head **572d64891d27bb72caa748c5c7611663463836a7** (attempt=1, pull_request)
Removed both catalog-row edits (forward-only revert commit), candidate now carries the content payload only.
Job census (run 45756612395, 29 jobs):
- `PR · Native gate plan` — success
- `PR · Source format` — success
- `Workflow policy` — success
- **`PR · Trusted Plan` (job 139696604375) — FAILURE** (verbatim uncataloged-source ValueError, same as above)
- `PR Selected Checks` (job 139696750385) — FAILURE (cascade)
- Every other job — skipped (native runtime suites, Go unit shards, pre-release, consumer pins, demo pin, public contracts, etc.)

## Actions taken (accepted by owner 04:44Z)
1. Removed candidate-side catalog rows via forward-only commit `572d64891` ("remove candidate-side catalog rows"),
   no rebase, no amend, no force, no history rewrite.
2. Payload guard `git diff 43326cf57 HEAD --name-status` still lists the 4 content files intact.
3. PR #1855 left **OPEN** as the content vehicle; no close, no close+reopen, no further trigger, no rebase.
4. Head `572d64891` is frozen — the content payload, not a green CI.

## Why a second run must wait
Run 45755906112 (123666c82) and 45756612395 (572d648) are both terminal FAILURE. A second `pull_request`
trigger on a failing head cannot qualify anything and only wastes a hosted run. The two qualifying runs must
run **sequentially** on the SAME final corrected head, and the close+reopen second trigger is requested only
**after** the first run on that head is green — never concurrently (owner 04:39Z).

## Blocker
Catalog baseline (Codex w267 baseline PR) has not landed on `develop` yet. Until it does, the base catalog still
fails the trusted planner on the new test files, and #1855 stays a content-only vehicle.

## Next move
- On catalog baseline landing on develop: re-apply the content payload to a clean successor, run the two distinct
  `pull_request` runs sequentially, post the census + the executed-gate log lines proving both new tests ran, then
  ask for the close+reopen second trigger only after the first is green.
- Record any moved develop with one ordinary merge commit (`git merge origin/develop`), never rebase/force/cherry-pick.
