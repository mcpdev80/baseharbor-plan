# 0428-082 Perses Infra dashboards — r1 evidence (worker w208)

## Task

t-20261114-r28-perses-dashboards (card 0428-082). PR #1665, draft, base `refs/heads/w083-perses-datasources`.
Goal: native Perses infrastructure dashboards with verified Prometheus metrics and explicit missing-signal behavior.

## Scope write-set (my card)

Own: `internal/metrics/prometheus.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/prometheus_verify.go` (+ `prometheus_files.go`, `prometheus_shared.go`), the `internal/metrics/*_test.go`, and `internal/metrics/testdata/perses-infra-dashboard/`.
Touch (product wiring, permitted): `cmd/baha/app_status_result.go` + perses CLI tests, `internal/capability/perses_selection.go`, `docs/spec/*.md`.
Do NOT touch: `internal/serviceaccess/**` (owner rail #1594/0428-053), `internal/observability/registry.go`, `internal/capability/perses_selection` runtime, `internal/identityprovider/**`, `internal/logs/**` (that is 0428-202, lane w207), `.github/**`, `internal/metrics/perses_dashboards*.go`, `internal/metrics/testdata/perses-dashboard-*/`, `internal/metrics/perses_prometheus_datasource*` (076 lane, #1597), `go.mod`/`go.sum` without proof.

## Reality witnesses

Planning repo remote (verified before first evidence commit):
`git remote -v` on `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`:
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`

Real remote heads via `git ls-remote https://github.com/mcpdev80/baseharbor.git`:
`e580d32414565442376f23ace9a4a2dd7ed03838  refs/pull/1665/head`  (my 082 PR head)
`b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe  refs/pull/1684/head`  (base lane 0428-083, moved)
`408b18d2dc7b0abe299749bb3a506c8cbd089098  refs/pull/1724/head`  (grandparent 0428-177)
`ed55d893374b593a7a6032f0de496ca9920ad08d  refs/heads/w083-perses-datasources`  (082 PR base)

Base attestation SHA I rebase from: the new base head `b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe`
(measured at refs/pull/1684/head, confirmed by ls-remote). This is the current content of the 083 base lane;
177 -> 083 -> 082 stacks correctly (wait on CONTENT, not merges, 3.3.8).

## PLAN (numbered)

1. Rebase the 082 candidate onto the new base head b71c6da27e8b so the candidate carries only 082 content on top of current 083. DONE: cherry-picked the 082-only commit chain (3a4599539..e580d3241) onto b71c6da27; resolved the app_status_result.go seam conflict by keeping the base version (new base already carries 083's perses wiring). New candidate head `db27880c1`.
2. Prove ancestry: `git merge-base --is-ancestor b71c6da27e8b <new head>` == YES. DONE: `git merge-base --is-ancestor b71c6da27e8b db27880c1` -> YES.
3. Scope check: `git diff --name-only b71c6da27e8b <new head>` must list only the write-set above. DONE: lists only `cmd/baha/app_perses_infra_dashboards_cli_test.go`, `internal/metrics/perses_infra_dashboards.go` + `_test.go`, `internal/metrics/testdata/perses-infra-dashboard/*`, and `git log b71c6da27..HEAD` shows only `db27880c1`. No foreign files.
4. Undraft the PR via `gh api -X POST repos/mcpdev80/baseharbor/pulls/1665/mark_ready` (PATCH draft=false is inert).
5. Verify live: `gh pr view 1665 --json isDraft,baseRefName,headRefOid` — isDraft MUST be false; paste all three values.
6. Run one hosted run on the exact new head, watched to terminal (4.6). Prove with smallest matching gate: `go test ./internal/metrics/ -count=1` and `go build ./...`.
7. If the CLI cells stay red: that is field-gate 0428-198 (`internal/operatorauth/authorization.go:285`); record exact line + `GATE-FAIL 0428-198`, do not chase. If the packages cell stays red: field-gate 0428-202, missing client-cert.pem in `internal/logs/loki_test.go` (another lane); name it, do not fix.
8. Keep PR DRAFT until implementation AND gate are complete; move to review only at handoff.
9. Commit evidence to baseharbor-plan (never a product repo), push to origin/main, verify path present on origin/main, post END.

## Work plan (board file)

Board file `/home/marcel/dev/baseharbor-ecosystem/workers/todos/w208-0428-082-dashboards.json` kept in sync with these steps.

## Retarget of PR #1665 base (Owner note 2026-11-20)

The hop to db27880c1 was clean and stayed on-card (git log 408b18d2 -> b71c6da27 -> db27880c1, one 082 commit). The old PR base `w083-perses-datasources` (= ed55d893374b) was a stale branch NAME; 083 publishes content at `lane-0428-083-datasources-r2` (= b71c6da27e8b, confirmed via gh api pulls/1684 head-branch). The 333-file count was the base-diff against the stale branch, not a scope problem.

Single metadata command executed (once), then verified:
`gh api -X PATCH repos/mcpdev80/baseharbor/pulls/1665 -f base=lane-0428-083-datasources-r2`

Verification value (1): `gh api repos/mcpdev80/baseharbor/pulls/1665 -q ".base.ref,.head.sha,.changed_files,.draft,.updated_at"`
```
lane-0428-083-datasources-r2
db27880c108a84c6c11bcb5a02484d3da00244bd
14
false
2026-11-20T21:29:37Z
```
base = lane-0428-083-datasources-r2 (correct), head = db27880c1, changed_files = 14 (write-set order, not 333), draft = false.

Files list (2): `gh api --paginate repos/mcpdev80/baseharbor/pulls/1665/files?per_page=100 -q ".[].filename"`
```
cmd/baha/app_perses_infra_dashboards_cli_test.go
internal/metrics/perses_infra_dashboards.go
internal/metrics/perses_infra_dashboards_test.go
internal/metrics/testdata/perses-infra-dashboard/prometheus-targets.json
internal/metrics/testdata/perses-infra-dashboard/upstream/dev-data-dashboard.json
internal/metrics/testdata/perses-infra-dashboard/upstream/perses-dashboard-model.go.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/perses-datasource-model.go.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/perses-metadata-model.go.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/perses-prometheus-datasource-schema.cue.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/perses-prometheus-time-series-query.cue.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/shared-datasource-selector.cue.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/spec-dashboard-model.go.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/spec-layout-model.go.txt
internal/metrics/testdata/perses-infra-dashboard/upstream/spec-plugin-model.go.txt
```
Free of internal/capability/perses_selection*, internal/identityprovider/**, internal/serviceaccess/**, .github/**. No rail file remains. Scope is clean.

## Container/composition hygiene (3.3.5)

No docker/podman compose project started this round. pre/post list: none. `cleanliness: OK`.

## Acceptance points (one line each, per 082 note)

- Verified pinned Perses release + native plugin/format, real provider signals, explicit missing-signal: Erfuellt durch internal/metrics/perses_infra_dashboards.go:26-37 (native Perses v1 Dashboard resource, pinned at release Core pin v0.55.1, native `PrometheusTimeSeriesQuery` plugin, inline datasource static selector) and internal/metrics/perses_infra_dashboards.go:63-70 (missing signal -> visible `MissingSignal`, no silent 0); proven by test TestPersesInfraDashboardNegativeMissingSignalPerPanel (internal/metrics/perses_infra_dashboards_test.go:162) and TestPersesInfraDashboardSchemaMatchesPinnedUpstream (:292).
- Scope by Target/tenant, fail-closed on missing authorization, no new capability, secrets out of logs: Erfuellt durch internal/metrics/perses_infra_dashboards.go:192-193 (unpinned/unselected/missing/denied -> PersesInfraDashboardError, fail closed) and internal/metrics/perses_infra_dashboards.go:48-51 (no Metrics capability claimed); proven by TestPersesInfraDashboardFailClosedWhenUnselected, TestPersesInfraDashboardFailClosedWhenNoProvider, TestPersesInfraDashboardFailClosedWhenNoAuthorizedSource (:162+), TestPersesInfraDashboardNoCapabilityClaim (:235).
- Preserve independent Prometheus/Loki/Tempo ownership, remove only owned resources: Erfuellt durch internal/metrics/perses_infra_dashboards.go:15-24 (binds the existing Prometheus-owned metrics endpoint read-only, declares no capability of its own) and testdata/perses-infra-dashboard/upstream/perses-prometheus-datasource-schema.cue.txt:35 (reuses the lane-083 datasource selector, does not redefine the backend).
- Alerting rule evaluator + notification owner in approved contract, no default external notifications: NICHT betroffen — this card builds an infrastructure dashboard only; no Perses alerting rules or routing are in scope or created (write-set contains no rule/notification files). The acceptance item is therefore not applicable to this candidate; no silent claim of alerting parity.

## Gate run on exact head db27880c1 (own run, 4.6)

- `go build ./...` -> exit 0 (worktree /tmp/opencode/w208-0428-082-wt, checked out at db27880c1)
- `go test ./internal/metrics/ -count=1` -> ok (no fail)
- `go vet ./internal/metrics/` -> exit 0
- 082-specific tests executed (none skipped): TestPersesInfraDashboardPositiveFilledSignal, TestPersesInfraDashboardNegativeMissingSignalPerPanel, TestPersesInfraDashboardProbeErrorStaysMissing, TestPersesInfraDashboardNoGenericProbeFillsPanels, TestPersesInfraDashboardQueriesUseRealScrapedSeries, TestPersesInfraDashboardSchemaMatchesPinnedUpstream, TestPersesInfraDashboardFailClosedWhenUnselected, TestPersesInfraDashboardFailClosedWhenNoProvider, TestPersesInfraDashboardFailClosedWhenNoAuthorizedSource, TestPersesInfraDashboardNoCapabilityClaim, TestPersesInfraDashboardJSONGolden, TestPersesInfraDashboardAvailabilityProductEntry, TestPersesInfraDashboardVerifiesOverRealHTTPPath — all PASS.
- CI route in THIS PR (no .github/** change needed): ci.yml pr_validations job (draft==false, base_ref lane-/develop) runs go-unit-tests via scripts/pr-unit-database.sh (packages shard -> go test ./... which covers internal/metrics/), plus go-vet and go-build. Trigger: pull_request (draft false). The release_source_preflight job (ci.yml:127) also runs go test ./internal/... but triggers only on runtime-validation/source-preflight/ push, so the operative required check is pr_validations.go-unit-tests.

## PR #1665 live state (verified, gh pr view 1665 --json)

`{"baseRefName":"lane-0428-083-datasources-r2","headRefOid":"db27880c108a84c6c11bcb5a02484d3da00244bd","isDraft":false,"state":"OPEN"}`

## CI hosted run on exact head db27880c1 (STATE, not a pass)

Run 44820434283 (CI · PR #1665, pull_request, base lane-0428-083-datasources-r2, head db27880c1) TERMINAL.
Required check `PR · Trusted Plan` = FAILURE. Root: the base-resolution step failed, cascading a required-gate fail.
Failing log line (job 136579771958):
```
python3 scripts/pr-diff-base.py --target-base "$effective_base" --head "$HEAD_SHA" --integration "$INTEGRATION_SHA" > "$RUNNER_TEMP/pr-diff.json"
##[error]Process completed with exit code 1.   (2026-11-20T21:29:43.1203975Z)
```
Code context at the step: `# Resolver independently checks exact parents, clean tree and diff.`
Downstream effect: `PR Selected Checks` = FAILURE via `NATIVE_REQUIRED: true` but `NATIVE_RESULT: failure` (native gate job SKIPPED), `Workflow policy` = FAILURE. `PR · Go unit · ${{ matrix.shard }}` and `PR · Validation` were SKIPPED (required checks did not execute).
Interpretation: this is a base-resolution / trusted-planner failure on the base, NOT a Go test failure. The `mark_ready` POST returns 404 through gh and curl; the PR is draft=false only because the base_ref became a `lane-` branch (some org draft policy). The required Go-unit receipt has NOT executed on db27880c1, so per the proof rule (success only for executed required jobs) this head is NOT yet green.

Root cause of base rejection: base b71c6da27 (lane-0428-083-datasources-r2) is NOT an ancestor of develop (40cb28c758). `git merge-base --is-ancestor b71c6da27 develop` -> exit 1. b71c6da27 carries ~20+ divergent commits not in develop (cli2 policy routing #1594/#1720/#1721/#1722, serviceaccess gateway, 0428-184/166/068, 0428-177). The resolver checks "exact parents, clean tree and diff" and rejects a base that is not a develop-ancestor. The 082 content itself is a clean 14-file write-set addition on top of that base.

Action boundary: the failing step is the CI base-resolution planner, which lives under .github/** (Owner scope). Per scope split I do NOT edit .github/** and do NOT trigger reruns/workflow_dispatch. STATE recorded here for the Owner; next needed step is an Owner/coordinator decision on the base resolution (e.g. land 083 into a develop that the planner accepts, or a coordinator fix to the base resolver) before this PR can pass its required checks.

## END status: END_BLOCKED

Candidate db27880c1 is correct (clean hop, 14-file write-set, all 13 082 tests pass locally, build+vet clean). Blocked on an Owner/coordinator base-resolution decision (083 lane not merged to develop; CI base-resolution planner rejects it). No further push on #1665.

Cleanup (one candidate per chain, AGENTS 3.8): my earlier test-push branch `0428-082-dashboards-r1` (= db27880c1) was a duplicate. ls-remote BEFORE: `db27880c108a84c6c11bcb5a02484d3da00244bd refs/heads/0428-082-dashboards-r1`; after `--delete`: absent. Only one 082 candidate branch remains: `lane-0428-082-perses-dashboards` = db27880c1; PR #1665 head = db27880c1.

Evidence on origin/main (verify):
```
evidence/r28-welle4-2026-11-20/perses-dashboards-r1/round-1.md
```

## REPRODUCTION COMMAND (for CI run)

`go test ./internal/metrics/ -count=1` and `go build ./...` in repo `mcpdev80/baseharbor` at candidate head.

## repo-rule compliance

- No subagents (4.8): every step ran in this session.
- Evidence only in baseharbor-plan, never in a product repo. No `.evidence/` dir, no main-branch writes in product.
- No `.github/**` edits (Owner scope); no reruns/workflow_dispatch.
- One candidate branch per chain: the 082 branch named in mission.
