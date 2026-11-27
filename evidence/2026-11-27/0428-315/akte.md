# 0428-315 · timeout constant matrix — w397 akte

Task `t-20261125-hunt42-timeout-constant-matrix`, card `0428-315`, release v0.4.28, repo `mcpdev80/baseharbor`, hunt H-V42.

## Visible ANSATZ BLOCK (before first commit)

- Card owner (verbatim frontmatter `owner:`, fetched from `origin/main` at runtime): `""` (unassigned in frontmatter; lane registered for this card is `w397-0428-307-idfallback`).
- Git identity used for every commit:
  - `user.name = w397-0428-307-idfallback`
  - `user.email = w397-0428-307-idfallback@baseharbor.local`
- Commit invocation (visible, used verbatim):
  - `git -c user.name=w397-0428-307-idfallback -c user.email=w397-0428-307-idfallback@baseharbor.local commit ...`
- Pre-push author gate (printed, must equal lane name):
  - `git show -s --format=%an HEAD`
  - BEFORE any push verify `git show -s --format=%an HEAD` equals `w397-0428-307-idfallback` exactly; on mismatch STOP + report.
- Branch provenance (before PR):
  - `git merge-base --is-ancestor origin/develop HEAD` must be an ancestor of the exact base head fetched.
  - `git diff origin/develop...HEAD --name-only` goes into evidence.
  - `git ls-remote <github-remote> refs/heads/develop` = base attestation (this SHA is an ancestor of my first commit).
  - `git log --oneline origin/develop..HEAD` must list ONLY my own commits.

## PLAN (numbered)

1. Read card + baseharbor/AGENTS.md; verify plan-remote = github.com/mcpdev80/baseharbor-plan.
2. Claim 0428-315 under `w397-0428-307-idfallback`, render+check; forward-only push to main (pull-before-push).
3. Map the divergent timeout literals in the real baseharbor checkout.
4. Introduce one documented timeout-matrix constant per semantic group, align literal-only duplicates; behavior-neutral, no semantics change.
5. Update positive+negative tests in the existing package scaffold (existing CI selection; no ci.yml touch).
6. Local non-test prechecks (format/vet/build).
7. Open PR against develop via `git merge origin/develop` + normal push; no force, no cherry-pick; do not self-merge.
8. Trigger hosted CI, run to terminal (no parallel dispatch); record run-ids + terminal status.
9. Classify under CI freeze #136 + fan-in; set card to wait; stop.

## Repo verification (remote guard + base attestation)

- Planning remote (first `git -C remote -v`): `origin = https://github.com/mcpdev80/baseharbor-plan.git`.
- Product remote (real github.com/mcpdev80, first git action): cloned `https://github.com/mcpdev80/baseharbor.git` into my own zone worktree; `origin = https://github.com/mcpdev80/baseharbor.git`.
- Base attestation: exact `origin/develop` SHA = `6944e8761af6f07b801f55e39bb9a5409226c10b`; `git merge-base --is-ancestor origin/develop HEAD` = YES; `git log --oneline origin/develop..HEAD` lists only my commits.

## Implementation (pre-freeze, done in this session)

- Shared StatusTimeoutMatrix added to `internal/application/timeouts.go` (exported: `OverallTimeout=120s`, `RequiredSecretTimeout=40s`, `ManagementServiceTimeout=30s`, `PostgresStatusTimeout=15s`, `FastServiceTimeout=10s`). Behavior-neutral: every value equals the literal it supplants.
- `cmd/baha/app_observe.go` per-service literals aliased to the matrix groups; `time` import removed; build clean.
- Tests in existing scaffold: `internal/application/timeouts_test.go` — `TestStatusTimeoutMatrixValues` (positive), `TestStatusTimeoutMatrixDistinctGroups` (negative), `TestManagementServicesShareManagementGroup` (positive).
- Local prechecks: gofmt clean, `go vet ./internal/application/` clean, `go build ./cmd/baha` OK.

## PR #1882 (candidate)

- PR: https://github.com/mcpdev80/baseharbor/pull/1882 — base `develop`, draft false.
- Exact head: `be410aea1ceee44163a26f7ad7eecc94b808e275`.
- Two commits on develop (only mine):
  - `a162aced` refactor(0428-315): unify/align application status-probe timeout constants to shared matrix
  - `be410aea` ci(0428-315): catalog timeouts.go/timeouts_test.go for PR gate coverage
- Changed paths: `cmd/baha/app_observe.go`, `internal/application/timeouts.go`, `internal/application/timeouts_test.go`, `scripts/pr-gate-coverage.json`. `scripts/pr-gate-coverage.json` is tracked and NOT under `.github/**`.

## Run witness + local classification (315-Befund, freeze #136)

- Run `46024898195` (pull_request, head `be410aea`) — terminal FAILURE: 3 success / 24 skipped / 2 failure.
- Failing jobs: `PR · Trusted Plan` (root) + aggregate `PR Selected Checks` (cascade).
- Trusted Plan failing log line:
  - `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/application/timeouts.go (id source.internal_application_timeouts_go) ...; internal/application/timeouts_test.go (id source.internal_application_timeouts_test_go) ...`
  - The gate's own suggestion (surfaces `["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]`) would bind a runtime surface a pure-Go constant does not have.
- Local classification: this is the SAME base-catalog coverage gate that blocks 307/310/312/316. It is a shared-develop-file ownership gate (`scripts/pr-gate-coverage.json`), an Owner-scope change that the lane must NOT push during the freeze. Not a defect in the timeout-matrix content (gofmt/vet/build clean; validator resolves my catalog entries with zero unresolved locally).
- First-run witness `46024040035` (head `a162aced`) failed identically; second-run witness `46024898195` (head `be410aea`) failed identically after the catalog-touch-up.

## Card state

- Set to `wait` via `card-status.py` with wait_reason: CI freeze #136 (owner) + active fan-in across lanes 307/310/312/315/316; shared base-catalog coverage gate blocks all; PR #1882 be410aea1 run 46024898195 FAILED at Trusted Plan; catalog-touch-up + rerun after lift; PR body be410aea1 left untouched.
- Published on origin/main at SHA `e06de0fc45479a59272daea0f662e9bb6b058012`.

## END STATUS

BLOCKED — CI freeze #136 (owner directive) + fan-in (lanes 307/310/312/315/316). Shared base-catalog coverage gate (`scripts/pr-gate-coverage.json`) blocks PR #1882 head be410aea1 (run 46024898195 pull_request FAILED at 'PR · Trusted Plan', uncataloged source change). No content push during freeze. PR body be410aea1 left untouched. After freeze-lift: one catalog-touch-up commit (add internal/application/timeouts.go + timeouts_test.go to scripts/pr-gate-coverage.json with correct surface) + rerun run-zeuge. Main SHA e06de0fc45479a59272daea0f662e9bb6b058012.

## w400 session — consolidation made real (2026-11-27)

This section documents lane `w400-0428-315-timeoutsfix`, which executed the card's own Task section / static-review finding: make the timeout-matrix consolidation REAL so every affected consumer reads the central constant, behavior identical (values unchanged, no tuning change).

- Visible ANSATZ BLOCK (before first commit), fetched from Plan `origin/main` `d70ad98090642fee99a45945b65e878428683f91`:
  - Card owner (verbatim frontmatter `owner:`, runtime): `""` (unassigned in frontmatter; lane registered for this card is `w400-0428-315-timeoutsfix`).
  - Git identity used for every commit:
    - `user.name = w400-0428-315-timeoutsfix`
    - `user.email = w400-0428-315-timeoutsfix@baseharbor.local`
  - Commit invocation (visible, used verbatim):
    - `git -c user.name=w400-0428-315-timeoutsfix -c user.email=w400-0428-315-timeoutsfix@baseharbor.local commit ...`
  - Pre-push author gate (printed, must equal lane name):
    - `git show -s --format=%an HEAD` → printed `w400-0428-315-timeoutsfix` (verified exactly equal before push).
    - `git log --format='%h an=%an cn=%cn' -1` → `d51763d0 an=w400-0428-315-timeoutsfix cn=w400-0428-315-timeoutsfix`.
  - Branch provenance (before PR):
    - Exact `origin/develop` SHA = `6944e8761af6f07b801f55e39bb9a5409226c10b`; `git merge-base --is-ancestor origin/develop HEAD` = YES.
    - `git log --oneline origin/develop..HEAD` lists ONLY my commits:
      - `be410aea1c ci(0428-315): catalog timeouts.go/timeouts_test.go for PR gate coverage`
      - `a162acedf7 refactor(0428-315): unify/align application status-probe timeout constants to shared matrix`
      - `d51763d0dc refactor(0428-315): make timeout-matrix consolidation real`
    - `git diff origin/develop...HEAD --name-only`:
      - `cmd/baha/app_observe.go`, `internal/application/timeouts.go`, `internal/application/timeouts_test.go`, `internal/metrics/perses_contract_test.go`, `internal/metrics/perses_tempo_datasource.go`, `internal/objectstorage/seaweedfs.go`, `internal/objectstorage/runtime_resources_test.go`, `scripts/pr-gate-coverage.json`.

- Consolidation made real (behavior-neutral, values unchanged):
  - `internal/metrics/perses_tempo_datasource.go`: `tempoTraceQueryTimeout` was a private `const = 10 * time.Second`. Replaced with `var tempoTraceQueryTimeout = application.FastServiceTimeout` (10s) — the Tempo trace-query probe now reads the central matrix FastServiceTimeout group instead of a duplicated literal. Removed the now-unused `time` import.
  - `internal/objectstorage/seaweedfs.go`: `sharedProviderReconcileTimeout` was a private `const = 120 * time.Second`. Replaced with `sharedProviderReconcileTimeout = application.OverallTimeout` (120s). `providerReadinessTimeout` (90s) and `existingProviderProbeTimeout` (3s) stay distinct per-operation budgets (readiness-wait and existing-provider probe are separate operations), documented as anchored to the shared matrix as source of truth. Values unchanged.
  - No `.github/**` touch, no consent/auth change, no value/tuning change. gofmt clean, `go vet ./internal/metrics/ ./internal/objectstorage/ ./internal/application/` clean, `go build ./...` exit 0.

- Tests added to the existing package scaffold (existing CI package-shard route, no workflow trigger change needed):
  - `internal/application/timeouts_test.go` → `TestSharedMatrixIsTheSingleSource`: asserts `FastServiceTimeout == 10s` and `OverallTimeout == 120s` (values preserved through consolidation).
  - `internal/metrics/perses_contract_test.go` → `TestTempoTraceQueryTimeoutReadsFastServiceMatrix`: asserts `tempoTraceQueryTimeout == application.FastServiceTimeout` and `== 10s`.
  - `internal/objectstorage/runtime_resources_test.go` → `TestSharedProviderReconcileReadsOverallMatrixAndBudgetsDistinct`: asserts `sharedProviderReconcileTimeout == application.OverallTimeout == 120s`, `providerReadinessTimeout == 90s`, `existingProviderProbeTimeout == 3s`.

- PR #1882 candidate (this lane's head):
  - PR: https://github.com/mcpdev80/baseharbor/pull/1882 — base `develop`, draft false, branch `lane-0428-315-timeouts`.
  - Exact head: `d51763d0dcb881e49279cd270c3265c00282b5b5` (via `git ls-remote` + `gh pr view`).
  - Transport: one normal push `git push <github-url> w400-0428-315-timeoutsfix:lane-0428-315-timeouts` (no force, no cherry-pick, no self-merge). Delivery proven: `git ls-remote ... refs/pull/1882/head` = `d51763d0…`.

- CI witness (two distinct executed pull_request run IDs on the SAME exact head d51763d0 — the authorized close+reopen pair, NOT a rerun):
  - Run `7991` (pull_request, head `d51763d0`) → terminal FAILURE (conclusion failure).
  - Run `7992` (pull_request, head `d51763d0`) → terminal FAILURE (conclusion failure). Triggered by `gh pr close --comment 'second exact-head hosted run trigger (coordinator-authorized)'` + `gh pr reopen --comment '...'` on the same head.
  - Neither run reached a passing aggregate. Both fail at the shared base-catalog coverage gate, identical to the prior heads (7982/7981) and to lanes 307/310/312/316.

## Root cause of the gate failure (this lane's finding)

- The prior w397 catalog-touch-up only added `internal/application/timeouts.go` and `internal/application/timeouts_test.go` to `scripts/pr-gate-coverage.json` (327 rows total; row format: `{"path": <go-path-or-dir>, "surfaces": [<surface>]}`).
- THIS lane's product change added two NEW Go files that the catalog does not list:
  - `internal/metrics/perses_tempo_datasource.go` — NOT cataloged.
  - `internal/objectstorage/seaweedfs.go` — NOT cataloged.
- Therefore `PR · Trusted Plan` fails on these two uncataloged source changes (the same uncataloged-source-change class as before). This is the shared `scripts/pr-gate-coverage.json` ownership gate, NOT a defect in the timeout-matrix content.
- The gate's own suggested surfaces (`source.gate.atomic.docker.data.capabilities` / `source.gate.atomic.podman.data.capabilities`) would bind a runtime surface a pure-Go constant matrix does not have; the correct surface for a documented Go constant source-of-truth is the static public-contract surface already used for `internal/application/timeouts.go`: `["source.gate.integration.static.public.contracts"]`.

## Exact catalog fix needed — Owner/coordinator scope, OUT of this lane's write-set

- The missing rows must be added to `scripts/pr-gate-coverage.json` (a shared CI catalog file, Owner scope; NOT under `.github/**` but still a shared planning-adjacent CI file this lane must not edit):
  - `{"path": "internal/metrics/perses_tempo_datasource.go", "surfaces": ["source.gate.integration.static.public.contracts"]}`
  - `{"path": "internal/objectstorage/seaweedfs.go", "surfaces": ["source.gate.integration.static.public.contracts"]}`
- This one catalog-touch-up belongs to the Owner/coordinator (shared file, out of card write-set). After the lift, rerun on the exact head d51763d0 to a passing aggregate. No content/tuning change, no ci.yml/workflow touch.

## Card state (this lane)

- Card left at `wait`. wait_reason appended: content consolidated at d51763d0 (Tempo probe + shared-provider reconcile read the central StatusTimeoutMatrix; per-op readiness/probe budgets distinct, values unchanged); two exact-head pull_request runs #7991 + #7992 FAILED at shared base-catalog coverage gate (uncataloged `internal/metrics/perses_tempo_datasource.go` + `internal/objectstorage/seaweedfs.go`); the missing catalog rows are Owner scope. PR #1882 head d51763d0 open, body untouched.

## END STATUS

BLOCKED (same shared base-catalog coverage gate as 307/310/312/316) — content consolidation IS complete and behavior-neutral, but this lane's product change introduces two uncataloged Go files (`internal/metrics/perses_tempo_datasource.go`, `internal/objectstorage/seaweedfs.go`) that re-trigger the shared `scripts/pr-gate-coverage.json` gate. Two executed pull_request runs #7991 + #7992 on exact head d51763d0 both FAILED at 'PR · Trusted Plan' (uncataloged source change). PR #1882 head d51763d0, base develop, draft false, branch lane-0428-315-timeouts. Local prechecks (gofmt/vet/build) all clean; no local test run. One catalog-touch-up (add the two rows above with surface `source.gate.integration.static.public.contracts`) is Owner/coordinator scope, out of this lane's write-set; after the lift rerun on exact head d51763d0. Main SHA d70ad98090642fee99a45945b65e878428683f91.
