# fix-1 — t-20261119-hunt-metrics-appclass-log-writer (hunt-918 Befund 3, HIGH)

- Lane: mission-appclass-writer.md (worker-flash), no subagents
- Card: t-20261119-hunt-metrics-appclass-log-writer (0428-122)
- Repo: mcpdev80/baseharbor, branch `lane-0428-appclass-writer`, PR #1692 (base develop)
- Mission: /var/tmp/missions/mission-appclass-writer.md (+ coordinator addenda: base-pflicht, develop 40b990139 then ec592fd38)

## PLAN

1. Claim card via plan.py + `ls-remote` develop (mission said 7d3438364) and attest base SHA
2. Reality check: who writes log-sources of which class (file:line)
3. Decide within contract: (a) writer vs (b) remove class + reject; document choice
4. RED regression first, GREEN after; matrix application + reference class
5. No touch: env-filter paths (121), dd62b9d3 chain, outcomeMatchesImpact/116, cmd/baha
6. Branch + PR base develop with ancestry proof
7. Watch exact-head CI to terminal; record runs
8. Evidence to baseharbor-plan origin/main, verified on origin/main
9. Cleanliness, END post

## Wrong-zone check (first evidence commit)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

## Base attestation

- Claim commit (baseharbor-plan main): `346c6232` (pushed, verified via ls-remote at the time).
- Product base: `git ls-remote origin develop` → `7d343836447f976ec613fa4ae1cb09afcabbbbe0` (mission-named SHA confirmed). Branch `lane-0428-appclass-writer` created AT that SHA: `git merge-base --is-ancestor 7d3438364 HEAD` → yes.
- Coordinator base-pflicht: develop advanced to `40b990139` (#116 merged) and then `ec592fd38` (#1687 merged). `git ls-remote origin develop` immediately before push: `ec592fd3852328439ae9de8763c816ae9dd88dcc`. Monotonic merge `1c41ae7fd` (Merge commit 'ec592fd38…' into lane-0428-appclass-writer, no conflicts, no force). Ancestry proof: `git merge-base --is-ancestor 7d3438364 HEAD` → yes; `git merge-base --is-ancestor ec592fd385 HEAD` → yes.
- Log line (own commits only; merge commit of the base hopf carries no foreign candidate):

```
0150f0cf1 refactor(0428-122): route the log writer through its single workload identity
799c66ec9 refactor(0428-122): settle the class-application log listing on the existing selector
0132087be refactor(0428-122): one class-application log signal per application/environment
973e1c4c2 fix(0428-122): settle the application-class log writer contract details
282ef0dfa fix(0428-122): give class application a production log writer
1c41ae7fd Merge commit 'ec592fd38…' into lane-0428-appclass-writer (develop base-pflicht)
```

- PR head: `1c41ae7fd18e7e21331cce9bfedfe745c9e79dfb` (witness below).

## KARTE-ENTSCHEID (writer, not removal)

Chose (a): implement the production writer. Begründung within the contract:

- The collector ALREADY realizes class application today: `internal/logs/render.go:187` (Docker syslog listener labelled `baseharbor_source_class = "application"`) and `render.go:261` (Podman journald source, same label). The class is a working ingest path, not an unimplemented plan; removing it from `docs/architecture/runtime-log-source-contract.md` would falsify what ships.
- The class is a documentation promise with release history: `docs/releases/v0.4.17.md:210` ("BaseHarbor normalizes workload, application-provider and platform-provider log sources"), `docs/internal/release-audits/v0.4.15.md:49-55` ("Current source classes remain: application / application-provider / platform-provider"). The class name is not schema/contract-enumerated (no spec/ or contracts/ occurrence of log source classes), so option (b) would have touched only docs — but docs describe real collector behavior, so removal = docs-vs-code falsification.
- Deployment policy already carries the class: `internal/application/logs_policy.go:18,35,42` — `LogsSourceApplication` is selected by `logs.collect` and honored by Preflight/workload paths (`internal/logs/driver.go:93`, `internal/logs/overrides.go`), so the eligibility knob exists; only the registry WRITE was missing.
- #1680's reclaim comment (`internal/application/runtime_observability.go:75-77,90-92`) states "workload logs are collected under the application source" — the codebase's own narrative treats the class as the intended owner of the workload stream. The metrics twin (`reconcileApplicationMetricsSource`) shows exactly how a class-application signal is written; logs were the asymmetry.

Third state avoided: the class is neither kept-doc-quietly-dead (current bug) nor removed; it gains a writer and becomes effective.

## Realityabgleich: who writes log-sources of which class (at develop 7d3438364)

| Class | Writer (production) | Evidence |
| --- | --- | --- |
| application-provider | `observability.RegisterProviderSignals` / `ReconcileSignals` | `internal/logs/realization.go:210-241` (Loki self), `internal/application/runtime_observability.go:242-268` (postgres/valkey per-instance), `internal/application/runtime_component_observability.go:122-140`, `internal/traces/tempo.go:403`, `internal/telemetry/realization.go:196`, `internal/identityprovider/keycloak_realization.go:158` |
| platform-provider | same primitives | `internal/logs/realization.go:211`, `internal/telemetry/realization.go:202`, `internal/application/runtime_component_observability.go` |
| application (LOG) | NONE — the Befund | registry `Update` used only by `internal/metrics/realization.go:183` (SignalMetrics); `internal/logs/realization.go:165-178` wrote only Registration state (syslog ports), never a SignalSource |

Read gate: `observability.ListLogs` hardwired `includeApplicationSources=false` (`internal/observability/registry.go:551-553`); callers `internal/logs/registration.go:27`, `internal/logs/overrides.go:105`, `cmd/baha/app_logs.go:140`. After the fix the class has a writer; `ListLogs` keeps provider-only defaults and the new policy-aware reader is `logs.ListWorkloadLogSources` (`internal/logs/application_source.go`).

## Regression (red → green)

RED measurement (recorded): the regression cannot compile against the untouched develop base — `go vet` at `7d3438364`: `internal/logs/appclass_log_writer_test.go:43:36: undefined: observability.ApplicationLogSourceID` (witness copied into a base worktree above). The API absence IS the silent-success shape: no production path ever wrote the class, so no reader-side function existed either. The hunt's behavioral witnesses (`evidence/.../hunt-metrics/scripts/zz_hunt918_e_test.go`, `zz_hunt918_l_test.go`, PASS at `97a840e54`) showed the class never present and the same-ID+Kind silent overwrite; `ReconcileMatching`'s fails-closed test removes that second shape.

Green AFTER (local, at merge `1c41ae7fd`):

```
--- PASS: TestApplicationClassLogSourceSurvivesManagedReconcile
--- PASS: TestApplicationClassLogSourceHasProductionWriter
--- PASS: TestApplicationClassLogSourceDisabledPolicyReclaims
--- PASS: TestApplicationClassLogSourcePolicyDisableReclaims
--- PASS: TestReconcileMatchingFailsClosedOnForeignProviderSource
--- PASS: TestApplicationClassLogSourceReferenceClassCounterCheck
ok  github.com/mcpdev80/baseharbor/internal/logs
```

Matrix: class application (writer/idempotency/reclaim/policy-disable) + reference-class counter-checks (`application-provider` in SurvivesManagedReconcile and HasProductionWriter; `platform-provider` in ReferenceClassCounterCheck). Existing suites green: `go test ./internal/logs ./internal/observability ./internal/metrics ./internal/application` (all ok), `go build ./...`, `go vet ./internal/...`, `gofmt` clean.

CI pickup (no `.github/**` change needed): all six tests are ordinary auto-discovered unit tests (`normal` binding). They run in CI through the existing PR selection: `PR · Go unit · packages` executes `./internal/logs/...` and `./internal/observability/...` on any PR (observed IN_PROGRESS for #1692 below); the develop workflow runs the same packages. The pre-existing `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` cmd/baha failure is an environment-dependent real-lifecycle test (fails identically at the untouched base `7d3438364` — verified in a second worktree; CI cli shards decide, recorded below).

## Implementation summary (candidate 1c41ae7fd)

- `internal/observability/registry.go`: `ApplicationLogSourceID` (`application:logs:<app>:<env>:<service>`), `ApplicationLogBoundary`, `PruneApplicationLogs`, `ReconcileMatching` — predicate-scoped atomic replace that fails closed when a desired source lies outside its own boundary (removes the Befund-3 same-ID+Kind overwrite shape).
- `internal/logs/application_source.go` (new): the writer (`ReconcileApplicationLogSource`, `ReconcileWorkloadLogSource`, `ConvergeManagedLogsForReconcile`), the policy-aware reader `ListWorkloadLogSources` (calls the existing generic `List` with its own policy bit — no registry list function changes), identity builder, boundary helper.
- `internal/logs/realization.go`: Loki `RegisterSource` now registers the class-application signal after the syslog registration, using the registration-derived project (the value renderers label streams with).
- `internal/application/runtime_observability.go`: `reconcileApplicationLogSource` wired into `reconcileManagedRuntimeObservability` (render-time writer for BOTH transports, before metrics/traces policy early-returns; disabled policy reclaims). Exported `ReconcileManagedRuntimeObservability` for the render-boundary regression.
- Kept untouched: `ListLogs` defaults (0428-121 territory), `pruneApplicationTargetsFromFiles`/`PruneApplicationMetrics` (dd62b9d3/registry-list chain), `outcomeMatchesImpact` (116), `cmd/baha` (118). No overlap found with 121: that lane (PR #1691) changes `logs/query.go`, `logs/registry_retirement.go`, `metrics/*`, `runtime_observability.go`'s prune call — my hunks are disjoint functions; merge-time text conflicts, if any, are for the integration order, flagged here per mission rule 5 (no STOP needed: files `internal/logs/query.go` and `internal/metrics/*` are NOT in my write-set at all).
- UPDATE (reality check at #1691's file list, 2026-11-19): card 0428-121's PR #1691 DOES touch my write-set files: `internal/observability/registry.go`, `internal/logs/realization.go`, `internal/application/runtime_observability.go` (plus `internal/logs/{state,lifecycle,overrides,registration}.go` and metrics files). Our hunks are function-disjoint (mine: new functions + RegisterSource + reconcile wiring; theirs: the central environment filter), but both lanes edit the same files. This is exactly the mission-rule-5 case, reported here and via the END line — NOT a blocker for my candidate (my PR is green and mergeable against develop ec592fd38), but the integration order needs a coordinator decision: whoever merges second rebases the disjoint hunks; GitHub may show a merge conflict between #1691 and #1692 until then. No lane stopped on the other; both run on develop.

## revision-labels (rounds)

- r1 (`282ef0dfa`): writer + primitives + regressions, red→green.
- r2 (`973e1c4c2`): per-service IDs considered — WRONG (registry holds one signal per app/env identity); settled to canonical workload token; prune boundary pinned.
- r3 (`0132087be`): ID = workload token, Target = resolved service (retarget semantics + test).
- r4 (`799c66ec9`): listing settles on the existing generic `List` selector; `ListLogsAt` wrapper removed — `ListLogs` stays byte-identical (0428-121 conflict avoidance).
- r5 (`0150f0cf1`): both writer paths land on one code path (`ReconcileApplicationLogSource` → `ReconcileWorkloadLogSource`); the Disabled/PolicyDisable reclaim tests were retargeted honestly to the r3 semantics (one signal per app/env, retarget replaces, disabled policy reclaims, prune boundary equals write boundary) and pass on the final tree (6/6 PASS observed).
- base hopf (`1c41ae7fd`): develop `ec592fd38` merged in per base-pflicht (monotonic; #116/#118/#120/#1687 diffs do not intersect my write-set; build, vet, gofmt and the logs/observability/metrics/application suites re-run green on the merged tree).
- r6 (`8956bf08e`): contamination cleanup — the nine `internal/application/{prune-*,trace-*}/runtime/runtime.env` scratch files swept in by `git add internal/` in r1 are deleted from the branch (see cleanliness); suites re-verified green; exact-head CI terminal on this SHA.

## witnesses

- Planning repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Develop ls-remote (pre-push, final): `ec592fd3852328439ae9de8763c816ae9dd88dcc refs/heads/develop`
- Branch ls-remote (after push): `1c41ae7fd18e7e21331cce9bfedfe745c9e79dfb refs/heads/lane-0428-appclass-writer`
- PR: https://github.com/mcpdev80/baseharbor/pull/1692 (head `1c41ae7fd…`, base develop)

## CI (exact-head run, terminal)

- Final head observed: `8956bf08e40e52b84a0dae55a9f1cb54db957636` (PR #1692; supersedes `1c41ae7fd` as the exact-head candidate — the r6 cleanup commit changed the head, monotonic push, develop unchanged at `ec592fd385` verified immediately before the push).
- Check census at the final head (all terminal): **14 SUCCESS / 0 FAILURE / 19 SKIPPED** (skips are release/native/matrix gates not selected by this PR's paths, per the selection discipline). SUCCESS set includes Workflow policy, PR · Native gate plan, PR · Source format, PR · Trusted Plan, PR · Focused Python, PR · Validation · go-build, PR · Validation · go-vet, PR · Go unit · owner and the Go-unit shards `cli-0..3` + `packages` — the packages containing my six new tests ran and passed at the exact head.
- `mergeable: MERGEABLE` against develop.
- Local re-verification on the final tree: `go build ./...`, `go vet`, `gofmt` clean; `go test ./internal/logs/ ./internal/observability/ ./internal/metrics/` ok; `go test ./internal/application/` ok (154s, scratch dirs regenerate at test time — proof the deletion is safe); the six `TestApplicationClassLogSource*`/`TestReconcileMatching*` regressions PASS.

## repo-rule compliance


- No `.github/**` edit, no rerun, no workflow_dispatch, no merge, no force-push.
- No subagents; every step in this session (no native todowrite in this tool surface — the board file `workers/todos/mission-appclass-writer.md.json` and this PLAN carry it, per mission rule).
- No containers/compose projects started on this host (R1); unit tests only; caches under /var/tmp.
- Evidence lives only in baseharbor-plan (this file); no `.evidence/` in any product repo.
- Write-set: internal/observability/registry.go, internal/logs/{application_source.go,appclass_log_writer_test.go,realization.go}, internal/application/runtime_observability.go — plus this planning evidence. No cmd/baha, no query.go, no metrics/ files.

## cleanliness

- **Incident (lane-owned contamination, FOUND AND FIXED in r6 `8956bf08e`):** my `git add internal/` in commit `282ef0dfa` swept 9 scratch directories that the *existing* `internal/application` unit suite leaves untracked in a dirty worktree (`prune-owner/ prune-sameid/ trace-handoff/ trace-intent-off/ trace-owner-managed-collector/ trace-owner-registered-external/ trace-policy-ext/ trace-policy-off/ trace-unbound-prune/` — each `runtime/runtime.env`; the hunt akte `befund-1.md` documents the same dirs as suite residue). `git check-ignore` shows they are NOT gitignored in this repo, and the precedent commit `022c454ce` shows another lane committed them the same way. r6 deletes them (monotonic, no force); the full `internal/application` suite passes after the deletion (it recreates the dirs at run time), so the true write-set is the five intended product files only.
- After the cleanup: no compose project started by this lane; host census unchanged (coordinator host: only the ambient `bh-local-shared` stack, not mine); worktree scratch under /var/tmp/w-appclass-* only; no containers on this host (R1).

## END

END mission-appclass-writer.md DONE — candidate `8956bf08e40e52b84a0dae55a9f1cb54db957636` (PR #1692, base develop `ec592fd38`; decision (a): class application got a production log writer + fails-closed reconciliation primitive; RED witness = writer API undefined at base, GREEN = 6 regressions + all touched suites; exact-head CI terminal 14 SUCCESS/0 FAILURE; file-overlap with 0428-121's PR #1691 reported above for the integration decision; r6 cleanup of lane-committed scratch state included).
