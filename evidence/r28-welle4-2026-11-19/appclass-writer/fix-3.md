# 0428-122 appclass log writer — fix-3 (implicit Compose workload selection)

Mission: mission-122-service-dimension.md (mission tag 122-service-dimension).
Card: t-20261119-hunt-metrics-appclass-log-writer (0428-122), active — correction
round on the SAME candidate chain, following fix-1 and the fix-2 CODEX review.
PR: mcpdev80/baseharbor#1692, branch `lane-0428-appclass-writer`.
Prior candidate head: `876329f733c7706a5a8dfb9a4227fb2c2698660c`.
This round's candidate head: `35069547245b0ba460e7fd57e4a56e0f51518991`
(merge onto develop `e1dc2cf61`, i.e. monotone hopf; the fix is `102fcd907`).

## PLAN

  - done: ls-remote compare develop / branch / PR head, `plan.py show`, PR
    review comment 7002202503 + CODEX akte fix-2 read.
  - done: isolated worktree cut at PR head `876329f`, base attestation written.
  - done: RED regression on the real path FIRST: an implicit Compose workload
    (manifest declares no Workload.Components) with two services registers a
    single synthetic `application:logs:demo:dev:workload` instead of `api` and
    `worker` — the exact CODEX hole.
  - done: fix in the render-time reconcile path (write-set eng:
    `internal/application/runtime_observability.go`,
    `internal/application/runtime_postgres.go`, `internal/logs/application_source.go`
    and the two test groups): carry the actually selected service set into the
    reconcile boundary, reclaim stale entries; the render-time identity stays
    manifest-only by design (repositoryRoot threaded, no process-CWD lookup).
  - done: targeted local checks — `go test ./internal/application
    ./internal/observability -run "^TestRoute5|^TestRoute2|^TestManagedRuntimeObservability|^TestWorkload"
    -count=1`, `gofmt -l .`, `go build ./...`, `go vet` on the affected
    packages; NO full `./...` run.
  - done: monotone hopf onto develop `e1dc2cf61` (the exact base #1694 merged
    into), resolve the single `internal/observability/registry.go`
    content-conflict keeping BOTH sides (0428-121 env-derivation UNCHANGED +
    0428-122 service-dimension), merge-tree → 0 conflict lines.
  - pending: push, exact-head CI self-watched to terminal SUCCESS (§4.6).
  - pending: this akte committed and pushed to origin/main, END posted.

## Reviewer verdict this round answers

CODEX-REVIEW REQUEST CHANGES at `876329f733c7706a5a8dfb9a4227fb2c2698660c`
(comment 7002202503, still the binding target): empty `Workload.Components`
maps to the synthetic singleton `workload` at
`internal/application/runtime_observability.go:87-94`, but
`internal/application/workload.go:214-248` selects ALL available
non-managed Compose services when `requested` is empty, so a normal
multi-service Compose workload was registered under one synthetic `workload`
source. Recipe: carry the actual result of `selectWorkloadServices` /
`MaterializeWorkload` into the writer's reconcile boundary, and add an implicit
two-service Compose regression with a shrink case proving stale cleanup while
the sibling survives.

## Weg confirmation (Owner clarification 2026-11-19)

Fix path is Weg 1 exactly — thread the repository root through the render-time
reconcile boundary, NOT a process-CWD lookup. The render-time contract is
manifest-only / render-time; a CWD lookup would make `selectedWorkloadServiceNames`
depend on an uncontrolled state (different in CI vs local), and `t.Chdir`
would be exactly the CWD-dependency this round refuses to introduce. That
`MaterializeWorkload(repositoryRoot, m, runtime)` and
`SelectedWorkloadServices(repositoryRoot, m)` in `internal/application/workload.go`
already derive the selected set AND the compose path FROM a repository root is
the proof that Weg 1 is the existing contract, not an invention. No new
signatures were pulled across packages; only the render-reconcile boundary got
its repository root.

## What the corrected code does

- `selectedWorkloadServiceNames(m, repositoryRoot)` resolves the ACTUALLY active
  workload service set in the order MaterializeWorkload reads it: (1) the
  manifest's declared `Workload.Components`; (2) the non-managed Compose
  services of the workload when the manifest declares none (implicit workload —
  `selectWorkloadServices` selects ALL available non-managed services when
  `requested` is empty), instead of the synthetic singleton `workload`; (3) the
  single canonical workload service when no compose source is resolvable.
- New `implicitComposeWorkloadServices(m, repositoryRoot)` reuses
  `ResolveWorkloadCompose` + `composeServiceNames` + `selectWorkloadServices`,
  so registry identity and MaterializeWorkload cannot drift for the same
  manifest; it returns false (not an error) when no workload compose source
  exists, keeping the manifest selection.
- `ReconcileManagedRuntimeObservability`, `reconcileManagedRuntimeObservability`,
  `reconcileApplicationLogSource` and `selectedApplicationLogSources` now carry
  `repositoryRoot` through; `runtime_postgres.go` passes `files.Dir` (best
  available root at realization), an empty value keeps the manifest selection
  so the identity never depends on a checkout being present.
- `ListWorkloadLogSources` (the class-application listing boundary) now threads
  `m.Environment` into `observability.List`, the #1691 env-threading the
  merge brings in.

## RED → GREEN

RED witness, on the candidate tree BEFORE this fix (only the new regression
file added, fresh worktree at `876329f` so no fix code is present — the real
path, not a fake):

```
--- FAIL: TestImplicitComposeWorkloadRecordsSelectedServiceSet (0.00s)
    appclass_writer_implicit_selection_test.go:80: implicit workload sources =
    []observability.SignalSource{... ID:"application:logs:demo:dev:workload" ...,
    Target:"runtime://bh-local-demo-dev/workload" ...}, want exactly [api worker]
--- FAIL: TestImplicitComposeWorkloadShrinkReclaimsStaleService (0.00s)
    appclass_writer_implicit_selection_test.go:89: same synthetic workload,
    want [api worker]
```

The two services of one implicit Compose workload collapse into a single
synthetic `workload` source — the CODEX hole made visible.

GREEN witness, candidate tree `102fcd907` (pre-hopf tree, same content):

```
$ go test ./internal/logs/ -run 'TestImplicitComposeWorkload' -count=1 -v
--- PASS: TestImplicitComposeWorkloadRecordsSelectedServiceSet (0.00s)
--- PASS: TestImplicitComposeWorkloadShrinkReclaimsStaleService (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/logs
```

Both regressions on the real path through `ReconcileManagedRuntimeObservability`:

- `TestImplicitComposeWorkloadRecordsSelectedServiceSet`: writes `compose.yaml`
  with two services in a temp root and passes THAT root through, asserts
  exactly `api` and `worker` keep separate IDs/targets (RED before: one
  synthetic `workload`).
- `TestImplicitComposeWorkloadShrinkReclaimsStaleService`: same root, then a
  SECOND reconcile with only `api` in `compose.yaml` at the SAME root asserts
  the concrete set shrinks to `[api]` — the stale `worker` entry is reclaimed,
  the sibling `api` survives. Asserted on the concrete service set
  before/after, not "something is left behind".

## New tests and what they pin

`internal/logs/appclass_writer_implicit_selection_test.go` (new, cross-package
`logs_test`):

- `TestImplicitComposeWorkloadRecordsSelectedServiceSet` — implicit Compose
  workload, two services, no `Workload.Components`; both service IDs/targets
  registered through the render-time reconcile.
- `TestImplicitComposeWorkloadShrinkReclaimsStaleService` — a compose service
  disappears; the next reconcile removes exactly that service's source and
  keeps the sibling, on the same temp root.

## Change list (file:line per change)

- `internal/application/runtime_observability.go` —
  `selectedWorkloadServiceNames(m, repositoryRoot)`: explicit components, then
  implicit Compose selection via `implicitComposeWorkloadServices`, then
  canonical `workload`; new `implicitComposeWorkloadServices(m, repositoryRoot)`.
  Threaded `repositoryRoot` through
  `reconcileManagedRuntimeObservability`, `reconcileApplicationLogSource`,
  `selectedApplicationLogSources`; updated
  `ReconcileManagedRuntimeObservability(m, project, repositoryRoot)` doc.
- `internal/application/runtime_postgres.go:131` —
  `reconcileManagedRuntimeObservability(m, files.Project, files.Dir)`.
- `internal/logs/application_source.go:184` —
  `ListWorkloadLogSources` threads `m.Environment` into `observability.List`
  (the #1691 env-threading the merge brings in).
- `internal/application/runtime_observability_test.go`,
  `internal/application/runtime_observability_trace_source_test.go`,
  `internal/logs/appclass_log_writer_identity_test.go`,
  `internal/logs/appclass_log_writer_test.go` — updated call sites for the new
  signatures and the #1691 `ListLogs` env arg.
- `internal/observability/registry.go` — net merge result of #1691 and #1692:
  BOTH sides kept. `SourceMatchesEnvironment` (0428-121 env-derivation,
  unchanged), `ApplicationLogSourceID` / `ApplicationLogBoundary` /
  `PruneApplicationLogs` / `pruneApplicationSignals` / `ReconcileMatching`
  (0428-122 service-dimension) and the threaded `List` / `ListLogs` /
  `ListTraces` signatures. Single `ListTraces`, no duplicate functions.

## Local checks (the requested targeted set)

```
$ go test ./internal/application ./internal/observability -run "^TestRoute5|^TestRoute2|^TestManagedRuntimeObservability|^TestWorkload" -count=1
ok  	github.com/mcpdev80/baseharbor/internal/application
ok  	github.com/mcpdev80/baseharbor/internal/observability   (no matching tests)
$ go test ./internal/application/ ./internal/logs/ ./internal/observability/ ./internal/identityprovider/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/application
ok  	github.com/mcpdev80/baseharbor/internal/logs
ok  	github.com/mcpdev80/baseharbor/internal/observability
ok  	github.com/mcpdev80/baseharbor/internal/identityprovider
$ gofmt -l .                      # clean (empty)
$ go build ./...                  # ok
$ go vet ./internal/application/ ./internal/logs/ ./internal/observability/   # ok
```

No full `./...` run (per the Owner clarification 2026-11-19). The ambient
"needs a runtime/engine" family failures recorded in fix-2 are out of scope;
they are not on this card's path.

## CI integration of the new tests

No `.github/**` change was needed: the new
`internal/logs/appclass_writer_implicit_selection_test.go` is a normal Go test
in package `logs_test` and is auto-discovered by `go test ./internal/...`, the
"Run release source tests" step of the existing selected PR job
`.github/workflows/ci.yml` (`go test ./contracts/... ./internal/... ./spec/...`).
The job that runs it is `PR · Go unit · packages`, triggered by the
`pull_request` event on this PR (and by develop integration). The #1691
env-threading the merge brings in touches existing `List` callers only, no new
CI group; no `.github/**` file is in this round's write-set.

## Base attestation and ancestry (branch provenance is proof)

Basis round-up: the branch is in GitHub's merge-queue/auto-merge set, so the
base is the hopf target, not a rebase — a merge, exactly as the mission
prescribes.

```
$ git -C baseharbor rev-parse 350695472^1 350695472^2
102fcd90707ecd1e0792fc3930e0ad09ef732af2
e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88
```

so the merge's second parent IS the exact hopf base `e1dc2cf61` (#1694
merged into develop). `git log --oneline e1dc2cf61..HEAD` lists ONLY this card's
own commits (the nine `0428-122` chain commits up to `102fcd907`) plus the two
develop merges the chain already carried (`876329f73` from the prior round,
`350695472` this round); no foreign candidate rides on top:

```
350695472 Merge remote-tracking branch 'origin/develop' into HEAD
102fcd907 fix(0428-122 r3): carry the implicit Compose service set into the render-time log reconcile
876329f73 hopf-merge 0428-122 r2: integrate develop 21161b101 (PR #1694) before the service-dimension fix
805587483 fix(0428-122): keep the service dimension in the class-application log identity
b7f245f10 chore(0428-122): remove test scratch fixtures committed by accident
c5f282241 refactor(0428-122): route the log writer through its single workload identity
221eb82ab refactor(0428-122): settle the class-application log listing on the existing selector
a898ad779 refactor(0428-122): one class-application log signal per application/environment
7ca579ec7 fix(0428-122): settle the application-class log writer contract details
8d972e9d8 fix(0428-122): give class application a production log writer
```

Ancestry of my first commit: `git -C baseharbor merge-base --is-ancestor
876329f73 102fcd907` → true, so the base I cut from is an ancestor of my first
commit; no foreign candidate is carried on top. Hopf:
`git -C baseharbor merge-base --is-ancestor e1dc2cf61 HEAD` → true.

merge-tree conflict check (the mission's exact predicate):

```
$ git -C baseharbor merge-tree --write-tree origin/develop HEAD    # exit 0, no CONFLICT line
$ git -C baseharbor merge-base --is-ancestor origin/develop HEAD   # true
```

The single `internal/observability/registry.go` content-conflict from
`git merge-tree --write-tree origin/develop 876329f` is resolved keeping BOTH
sides — 0428-121's env-derivation (unchanged) and 0428-122's service-dimension
reconcile primitives.

Product repo remote truth (`git ls-remote origin`, before any push of this
round):

```
e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88	refs/heads/develop
876329f733c7706a5a8dfb9a4227fb2c2698660c	refs/heads/lane-0428-appclass-writer
```

## Report on the pre-existing worktree that held the candidate branch

The local branch `lane-0428-appclass-writer` was checked out in
`/tmp/opencode/w-appclass-writer-wt` at the stale head `8956bf08e`, which
blocked a checkout of the named candidate branch. That worktree is left
completely untouched — including the untracked scratch directories it carries
under `internal/application/` (`prune-owner/`, `prune-sameid/`,
`trace-handoff/`, `trace-intent-off/`, `trace-owner-managed-collector/`,
`trace-owner-registered-external/`, `trace-policy-ext/`, `trace-policy-off/`,
`trace-unbound-prune/`). This lane works in its own worktree
`/tmp/opencode/m122-r3-wt` on local branch `lane-0428-appclass-writer-m122` and
pushes it to `refs/heads/lane-0428-appclass-writer`: exactly ONE candidate
chain, monotone on `876329f` (ancestry proven above), no second remote branch.
The pre-existing local branch ref was preserved as `wip/0428-122-r2 →
b7f245f10` before any of this (no `git branch -D`, nothing rewritten).

## evidence origin (on origin/main BEFORE the END post)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main
75dd7558e0bb9a01f50335a9390c8d3b6bfea08e	refs/heads/main
$ gh api "repos/mcpdev80/baseharbor-plan/contents/evidence/r28-welle4-2026-11-19/appclass-writer/fix-3.md?ref=main" --jq '.name'
gh: could not find file: ... (committed to origin/main in this round)
```

Evidence lives ONLY in baseharbor-plan (the planning repo, verified above);
nothing of this round is in a product repo, no `.evidence/` anywhere.

## Scope and rule compliance

- Write-set stayed on the card's path:
  `internal/application/runtime_observability.go`,
  `internal/application/runtime_postgres.go`,
  `internal/logs/application_source.go`, new
  `internal/logs/appclass_writer_implicit_selection_test.go`, and the two
  existing appclass test groups for the new signatures. NO `.github/**` file,
  NO `internal/metrics/**` (0428-121's environment-filter topic) touched; the
  #1691 env-threading only reaches `observability.List` callers, not the
  environment-filter behavior.
- No merge by this lane, no CODEX verdict, no force-push, no subagent (§4.8).
- No Docker/Podman compose project started (unit/contract tests only). Host
  census before/after in the cleanliness section.
- Scratch lives under `/tmp/opencode/m122-r3-wt` only; nothing added to
  `/home/marcel/dev/baseharbor-ecosystem` itself.

## cleanliness

- Before: `docker ps -a --format '{{.Names}}'` → ambient
  `bh-local-shared-*` (core/admin/member OpenBao + shared Postgres): not this
  lane's, left untouched. `docker network ls` → 5.
- After: same ambient containers, same networks; this lane started no
  container, no compose project, no volume (`diff` of before/after → no
  output). No `baha` state directories created under the host state root:
  every test used `t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())`.
- This lane's own residue: only its `/tmp/opencode/m122-r3-wt` worktree (to be
  removed after END bookkeeping), nothing in a product repo, no `.evidence/`
  anywhere.
- cleanliness: host besenrein übergeben — ambient containers/networks
  unchanged, 0 lane-owned containers/networks/volumes/compose projects.

## END

END mission-122-service-dimension.md DONE — candidate `35069547245b0ba460e7fd57e4a56e0f51518991`
(PR #1692, branch `lane-0428-appclass-writer`, hopf onto develop `e1dc2cf61`,
monotone on the reviewed `876329f`, fix `102fcd907`): the render-time reconcile
carries the actually selected Compose service set into the reconcile boundary
instead of the synthetic `workload`, reclaims stale entries, and the
implicit two-service + shrink regressions pass on the real path; targeted
`go test`/`gofmt`/`go build`/`go vet` green; single `registry.go` conflict
resolved keeping both #1691 and #1692 (merge-tree → 0 conflict); no `.github/**`
edit, no merge, no CODEX verdict, no subagent. Exact-head CI still to run before
this is accepted (§4.6).
