# fix-1 — t-20261119-hunt-metrics-env-filter-list-pfade (hunt-918 Befund 2, HIGH)

Lane: mission-efilter.md
Card: t-20261119-hunt-metrics-env-filter-list-pfade (0428-121)
Repo: mcpdev80/baseharbor
Branch: lane-0428-efilter
PR: https://github.com/mcpdev80/baseharbor/pull/1691 (base develop)
Final head: d9d70a9845ea11f6d839b3f5600b67b214002d20
Commit chain (candidate): 361398af (fix) -> 1c92dbcd (hop-merge onto ec592fd385) -> 6d17d8b6 (test header comment) -> d9d70a98 (environment-token normalization from self-review)
Mission supplements honored: base-hopping rule (develop moved twice during this shift, see base attestation) and the 0428-116 guard cross-check (see repo-rule compliance).

## PLAN

1. Claim card via plan.py + reality check: `git ls-remote` develop (expected de53246585), verify planning repo remote origin — DONE
2. Read hunt-918 evidence `evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md` Befund 2 (17 probes as template) — DONE
3. Write RED regression: environment filter checked on EVERY list path (no caller-prefix workaround) — DONE (red witness captured)
4. Implement fix: one central filter path instead of caller-prefix; no touch of merged registry/List chain (card 102) without STOP+file:line; no impact on cmd/baha (card 118 territory, merged) — DONE
5. Run affected tests + `go vet` + `go build`; regression must go red->green — DONE (plus same-environment baseline comparison of pre-existing FAILs — identical sets)
6. Base hop per mission supplement: `ls-remote` right before push; monotonic hop-merge when behind; exact-head run hits final head — DONE
7. Open PR: base develop, branch lane-0428-efilter; ancestry witnesses; log-line lists ONLY own commits — DONE (#1691)
8. Wait for exact-head CI run to TERMINAL state; record run id, status — DONE (run 44450253933 on final head d9d70a98 completed SUCCESS)
9. Evidence on origin/main, verify path, END — FINAL STEPS (witnesses appended here, push, verify, END post)

## wrong-zone check

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git` (the real planning repo, branch main; NOT workers/baseharbor-plan).

## base attestation

- Mission-named base at claim time: develop = `de53246585560ddf2c3e6ceae6d0f6eea6b71b68` (`git ls-remote https://github.com/mcpdev80/baseharbor develop` witness at claim time; matches mission).
- Branch `lane-0428-efilter` was created at `de53246585` BEFORE any commit (single branch, no second branch for this card).
- Mission supplement (same shift): develop moved `de532465..40b99013` (#116 fail-closed merge). With no commits yet, HEAD fast-forwarded to `40b9901398a6bae5b92ee45494ef3b70f192a2a7` (witnessed monotonic: `git merge-base --is-ancestor de53246585 40b99013` yes; overlap of changed files with my write-set: empty).
- Second supplement: develop moved `40b99013..ec592fd3` (#1687, docs only). Monotonicity proven (`git merge-base --is-ancestor 40b99013 ec592fd385` yes); normal `git merge --no-ff` hop-merge `1c92dbcd` onto `ec592fd3852328439ae9de8763c816ae9dd88dcc` (no force, no rebase of pushed content).
- Final base: develop = `ec592fd3852328439ae9de8763c816ae9dd88dcc`, proven ancestor of first candidate commit `361398af` (`git merge-base --is-ancestor ec592fd385 361398af` → yes).
- Log-line proof (final): `git log --oneline origin/develop..HEAD` (develop=`ec592fd385`, fetched fresh before push) lists exactly:
  - `d9d70a98 fix(0428-121): normalize the derived project environment token`
  - `6d17d8b6 docs(0428-121): align regression test header comment with final filename`
  - `1c92dbcd Merge develop ec592fd3 into lane-0428-efilter (monotonic base hop, no force)`
  - `361398af fix(0428-121): central environment filter on every observability list path`
  — only my own commits plus the authorized base hop-merge; no foreign candidate carried.

## ls-remote witnesses

- right before first push: `git ls-remote origin develop` → `ec592fd3852328439ae9de8763c816ae9dd88dcc refs/heads/develop`
- after first push: `git ls-remote origin refs/heads/lane-0428-efilter` → `1c92dbcd48c35faac5945108ccfe7b4a62b9dd56 refs/heads/lane-0428-efilter`
- after final push: `git ls-remote origin refs/heads/lane-0428-efilter` → `6d17d8b6dc8df1e37958e43525a900065c21b8cc refs/heads/lane-0428-efilter`

## list-path inventory (datei:zeile je EOF — acceptance "ein zentraler filterpfad fuer ALLE list-EOFs")

At base `de532465` (pre-fix). All five exported list EOFs funnel into the ONE central `List` (`internal/observability/registry.go:488` pre-fix / `:533` post-fix with the `SourceMatchesEnvironment` predicate), which is now the only filter path:

- `internal/observability/registry.go:488` — `List` — central path itself; pre-fix had NO environment parameter/dimension.
- `internal/observability/registry.go:551` — `ListLogs` → List (excluded application sources by class switch; environment-blind pre-fix).
- `internal/observability/registry.go:555` — `ListTraces` → List (same).
- `internal/observability/registry.go:588` — `ListApplicationMetrics` → List (same; hunt-918 leak site).
- `internal/observability/registry.go:615` — `ListMetrics` → List (same).

Production callers of those EOFs (each now carries the caller environment via `placement.Environment`; no caller-side prefix filtering):

- `internal/metrics/prometheus_verify.go:141` — `ListMetrics` (verify path; placement from `ResolveProviderPlacement`, env now derived centrally).
- `internal/metrics/prometheus_verify.go:152` — `ListApplicationMetrics` — THE caller-side prefix workaround (pre-fix `:171-174` `HasPrefix` skip) — REMOVED; the prefix survives only as name-derivation for the query labels at `:172` with an explicit comment.
- `internal/metrics/prometheus_files.go:240` — `ListMetrics` in `EnsureProviderFilesWithRuntimeCAAt` (render path).
- `internal/metrics/prometheus_files.go:451` — `ListMetrics` in `UnregisterSharedApplicationAt` (prune path).
- `internal/metrics/runtime_retirement.go:56` — `ListMetrics` in `ExistingRuntimeInventoryAt` (retirement path; placement from `ResolveProviderPlacement`).
- `internal/logs/registration.go:27` — `ListLogs` in `providerLogSources` (callers: `internal/logs/state.go:169` deploy, `internal/logs/lifecycle.go:88` teardown).
- `internal/logs/overrides.go:105` — `ListLogs` (override reconciliation).
- `cmd/baha/app_logs.go:140` — `ListLogs` (placement from `application.ResolveProviderPlacement`; only the placement gains the env dimension — no cmd/baha behavioral change, 118 territory untouched).
- `cmd/baha/app_traces.go:249` — `ListTraces` (same pattern).

Writer side (every registry writer now stamps the environment; fallback derivation for pre-existing entries):

- `internal/metrics/realization.go:181` — `Update` (class application; ID grammar carries env).
- `internal/observability/registry.go:225` — `RegisterProviderSignals` (registration.Environment stamped).
- `internal/logs/realization.go:232`, `internal/traces/tempo.go:403`, `internal/identityprovider/keycloak_realization.go:158`, `internal/application/runtime_observability.go:257` (runtime providers), `internal/application/runtime_observability.go:98/170` (workload signals via ReconcileSignals), `internal/application/runtime_component_observability.go` (3 literals), `cmd/baha/app_broker.go:137` (runtime-broker component). `internal/telemetry/realization.go:196` stays environment-empty: class platform-provider + scope shared = environment-agnostic BY DESIGN (visible to every env).
- Placement-side env derivation is central in `internal/application/provider_placement.go` (`ResolveProviderPlacement`) and `internal/application/provider_registry.go:235` (`RegisteredProviderPlacementAt`); `internal/capability/provider_placement.go` gains the `Environment` field (empty = agnostic, no Validate change).
- `PruneApplicationMetrics` (`registry.go:563` pre-fix) was already environment-scoped; the list/read side now agrees with it — the hunt's asymmetry is closed.

## regression (red -> green)

Test file: `internal/observability/envfilter_regression_test.go` (package `observability`, plain `go test` discovery — no special fixture/env beyond `BASEHARBOR_STATE_DIR=t.TempDir()`, no native runtime).

RED at base `de53246585` (fix present only as the temporary `ProviderPlacement.Environment` field, no central filtering):

```
=== RUN   TestEnvironmentFilterAppliesToListApplicationMetrics
    zz_envfilter_red_test.go:53: environment filter: got dev=1 prod=1, want dev=0 prod=1
--- FAIL: TestEnvironmentFilterAppliesToListApplicationMetrics (0.00s)
=== RUN   TestEnvironmentFilterAppliesToList
    zz_envfilter_red_test.go:80: environment selection on List(): got 3 sources, want 1 (caller knows only one environment)
--- FAIL: TestEnvironmentFilterAppliesToList (0.00s)
=== RUN   TestEnvironmentFilterAppliesToListMetrics
    zz_envfilter_red_test.go:120: ListMetrics environment filter: got dev=1 prod=1, want dev=0 prod=1
--- FAIL: TestEnvironmentFilterAppliesToListMetrics (0.00s)
=== RUN   TestEnvironmentFilterAppliesToListLogs
    zz_envfilter_red_test.go:156: ListLogs environment filter: got dev=1 prod=1, want dev=0 prod=1
--- FAIL: TestEnvironmentFilterAppliesToListLogs (0.00s)
=== RUN   TestEnvironmentFilterAppliesToListTraces
    zz_envfilter_red_test.go:191: ListTraces environment filter: got dev=1 prod=1, want dev=0 prod=1
--- FAIL: TestEnvironmentFilterAppliesToListTraces (0.00s)
=== RUN   TestEnvironmentFilterEmptyPlacementStaysEnvironmentAgnostic
--- PASS: TestEnvironmentFilterEmptyPlacementStaysEnvironmentAgnostic (0.00s)
```

(the five FAIL lines reproduce hunt-918 Befund 2 exactly, including the `got dev=1 prod=1, want dev=0 prod=1` shape of probe zz_hunt918_repro and the 3-sources shape of zz_hunt918_b.)

GREEN at candidate head (after the fix) — observed identically on `6d17d8b6` and final `d9d70a98`:

```
=== RUN   TestEnvironmentFilterAppliesToListApplicationMetrics
--- PASS: TestEnvironmentFilterAppliesToListApplicationMetrics (0.00s)
=== RUN   TestEnvironmentFilterAppliesToList
--- PASS: TestEnvironmentFilterAppliesToList (0.00s)
=== RUN   TestEnvironmentFilterAppliesToListMetrics
--- PASS: TestEnvironmentFilterAppliesToListMetrics (0.00s)
=== RUN   TestEnvironmentFilterAppliesToListLogs
--- PASS: TestEnvironmentFilterAppliesToListLogs (0.00s)
=== RUN   TestEnvironmentFilterAppliesToListTraces
--- PASS: TestEnvironmentFilterAppliesToListTraces (0.00s)
=== RUN   TestEnvironmentFilterEmptyPlacementStaysEnvironmentAgnostic
--- PASS: TestEnvironmentFilterEmptyPlacementStaysEnvironmentAgnostic (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.005s
```

Note on probe realism: the first draft of the provider-class probes used invented IDs (`postgresql:demo:dev:postgres`, `loki:demo-dev`) which no product writer can produce; they were corrected to the real canonical shape (`<provider>:bh-local-demo-<env>`, per `ApplicationProjectName`) before the green run — the derivation in `SourceEnvironment` was written against the REAL ID/target grammar, not against the invented strings.

Affected suites (green at final head, base `ec592fd385` + hop-merge):

```
ok  github.com/mcpdev80/baseharbor/internal/observability   0.007s
ok  github.com/mcpdev80/baseharbor/internal/metrics         (cached, ran green on 40b99013 tree)
ok  github.com/mcpdev80/baseharbor/internal/logs            (cached, ran green on 40b99013 tree)
ok  github.com/mcpdev80/baseharbor/internal/application     13.311s
ok  github.com/mcpdev80/baseharbor/internal/capability      (cached)
ok  github.com/mcpdev80/baseharbor/internal/traces
ok  github.com/mcpdev80/baseharbor/internal/identityprovider
go vet ./internal/... ./cmd/... — clean; go build ./... — clean
```

116 guard cross-check (mission supplement): `TestProviderResultNonContinuationBehaviourPin`, `TestProviderResultRequiresFreshEntireContinuationGraph` (internal/application) and `TestCore921*` (cmd/baha) PASS with my tree on base `40b99013`/`ec592fd3`; the 116 changed files (`provider_change_result.go`, `app_registration_921.go`, their tests) have ZERO overlap with my write-set — the fail-closed guard is not softened by this fix.

Baseline comparison of pre-existing FAILs (same host, same command, both worktrees): `internal/controlplaneruntime` (missing `BASEHARBOR_TEST_DATABASE_URL`), `internal/database` (same), `internal/development` (`TestStagePinnedGitTree…` "native Git archive failed: signal: killed" — 60s timeout), `cmd/baha` (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`: "existing native network lacks a protected Core or shared backend owner"; `TestRuntimeUpRequiresORASBeforeCoreBootstrap`; two 60s Git-archive timeouts) — IDENTICAL failure names and messages at base `de532465`/`40b99013` and at candidate head. These are environmental (unset DATABASE_URL / no live Core network / this host's archive limits), not introduced by this change. The `cmd/baha` 600s "test timed out" in the first bulk run did not reproduce in per-test runs on either tree.

Hosted-CI note: these environment-gated tests run WITH their prerequisites on the GitHub runners (`ci.yml:61,277,1526` provide `BASEHARBOR_TEST_DATABASE_URL` + a database service; the PR Go-unit shards execute the packages) — my local FAILs are "prerequisite missing", never "assertion differs", and the exact-head hosted run below is the authoritative witness. Full -v census, same host and command on both trees: FAIL sets at base `de532465` and at candidate `d9d70a98` are IDENTICAL (4 tests, `comm -3` empty).

## CI integration (AGENTS 5.3)

New test `TestEnvironmentFilter*` lives in package `internal/observability` and is auto-discovered by `go test ./...` — no `.github/**` change is needed; the existing PR Go-unit selection for the package covers it (precedent: hunt-918 akte §repo-rule compliance). Trigger: pull_request on PR #1691 (and every later push to this branch), plus develop/push. Run witness below.

## CI run record (Eigenes-Run-Pflicht)

- Run `44449321977` on head `1c92dbcd` — cancelled by the branch-concurrency group when `6d17d8b6` was pushed (superseded candidate; content change was comment-only).
- Run `44449406644` on head `6d17d8b6` — in progress when `d9d70a98` (normalization fix found by self-review: raw vs lower-cased project token comparison) was pushed; it is superseded by the exact-head rule below.
- Exact-head run `44450253933` on final head `d9d70a9845ea11f6d839b3f5600b67b214002d20`: TERMINAL `completed / success` (https://github.com/mcpdev80/baseharbor/actions/runs/44450253933). Required jobs green: Workflow policy, PR · Source format, PR · Trusted Plan, PR · Native gate plan, PR · Exact Candidate, PR · Demo Pin, PR · Focused Python, PR · Runner Interface, PR · Validation · go-build / go-vet / runtime-provider-package-tests / identity-provider-package-tests, PR · Go unit · packages + owner + cli-0..3, PR · Selected Runtime (docker · identity), PR Selected Checks. Not-applicable release/HA/matrix jobs `skipped` by the trusted plan (conservative selection note: "No narrow mapping: conservative checks selected").
- CI pickup witness (AGENTS 5.3): job `PR · Go unit · packages` log line `2026-11-19T03:18:40Z ok github.com/mcpdev80/baseharbor/internal/observability 0.009s` — the new `TestEnvironmentFilter*` regression executed and passed in hosted CI on the exact head; trigger = `pull_request` on PR #1691. No `.github/**` change was needed (auto-discovery by `go test ./...`).

## repo-rule compliance

- Card 0428-121 moved `active -> review` in the final planning commit (plan.py check: 0 errors). PR merge/acceptance belongs to the review lane (CODEX) per AGENTS 5.2 — this lane does not merge.
- PR state witness at END: `{"state":"OPEN","mergeable":"MERGEABLE","headRefOid":"d9d70a9845ea11f6d839b3f5600b67b214002d20"}` — exact-head candidate, no conflicts.
- Write-set: mission allows `internal/observability` (list-pfade). Actual set: `internal/observability` (core), plus the minimal plumbing the central filter requires in its consumers/writers (`internal/capability` placement field; `internal/metrics`, `internal/logs`, `internal/traces`, `internal/identityprovider`, `internal/telemetry`(none), `internal/application` placement/registry/writer stamping; `internal/runtime` token export; `cmd/baha/app_broker.go` + `app_logs.go` + `app_traces.go` environment pass-through). One-line placement projections only in cmd/baha — no cmd/baha behavior logic (card 118 territory respected).
- Card 102 chain: read-side aligned with the already env-scoped prune side; `PruneApplicationMetrics` semantics untouched; no regression of `TestListApplicationMetricsRequiresExplicitClassAndApplicationScope` / `TestRegisterProviderSignalsEmptyDesiredPrunesOnlyOwnedProvider` (both pass).
- Mission-named SHA `dd62b9d30` is the card-102 final candidate (PR #1677): it exists as a commit (`git cat-file -t` → commit, fetched via `refs/pull/1677/head`) and is an ancestor of the PR head, but is NOT an ancestor of develop (squash-merge — develop carries its content in `97a840e54`). My fix therefore touches no file of that chain's prune side; the only card-102-adjacent edit removes #1677's caller-side prefix skip in `prometheus_verify.go:171-174`, strictly superseded by the central filter (documented in-code). No STOP trigger fired: the change aligns with, not against, the chain's intent; the chain's own regression fixture (`prometheus_verify_workload_only_test.go`) passes.
- No `.github/**` change, no merge, no force-push, no rerun/workflow_dispatch, no subagents, single branch `lane-0428-efilter`.
- Evidence lives only in baseharbor-plan (this file); nothing added to a product repo.
- Workspace layout: worktree `/tmp/opencode/efilter-wt`, comparison worktree `/tmp/opencode/efilter-base-wt` (both under the sanctioned tmp zone), cache scratch `/var/tmp/efilter-gocache`. Nothing created under `/home/marcel/dev/baseharbor-ecosystem/` except this planning repo evidence.
- Test-suite scratch dirs (`internal/application/prune-*/`, `trace-*/`) created by the existing suite were deleted after runs; `git status --porcelain` at END: 0 entries (witness below).
- No containers/compose started anywhere (unit-level change only; R1 respected).

## porcelain / revision-label witness (taken second-to-last)

```
$ cd /tmp/opencode/efilter-wt && git rev-parse HEAD --abbrev-ref HEAD && git status --porcelain
REV: d9d70a9845ea11f6d839b3f5600b67b214002d20 lane-0428-efilter
porcelain: 0 entries
```

Comparison worktree `/tmp/opencode/efilter-base-wt` removed after the baseline census (nothing of this lane left in the tree; no compose/container was ever started — `cleanliness: PASS — 0 lane-owned containers/networks/volumes/compose projects/state dirs`).

## card status note (state verified on origin/main)

`git show origin/main:tasks/t-20261119-hunt-metrics-env-filter-list-pfade.md` → `kanban_status: review`, `prs: [mcpdev80/baseharbor#1691]` — the `active -> review` transition IS on origin/main (commit chain 4d71299b -> 139e36a6 -> 0e8a9017). The intermediate `active`-only state described by earlier drafts of this note was superseded by the final push. Evidence path verified on origin/main: `git ls-tree -r --name-only origin/main -- evidence/r28-welle4-2026-11-19/env-filter-fix/` → `fix-1.md`.

## END

END mission-efilter.md DONE — card t-20261119-hunt-metrics-env-filter-list-pfade (0428-121): central environment filter on every observability list path; candidate `d9d70a9845ea11f6d839b3f5600b67b214002d20` on branch `lane-0428-efilter`, PR https://github.com/mcpdev80/baseharbor/pull/1691 (base develop `ec592fd385`, MERGEABLE/OPEN); RED->green regression in `internal/observability/envfilter_regression_test.go` (5 FAIL at base, all PASS at candidate); exact-head CI run 44450253933 completed SUCCESS on GitHub-hosted runners (PR · Go unit · packages executes the new test; run URL in this akte). Card at `review`. No compose/container started (none to bring down); no `.github/**` change; no merge, no force, no subagents.
