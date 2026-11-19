# 0428-122 appclass log writer — fix-2 (correction round: service dimension)

Mission: mission-122-service-dimension.md (mission tag 122-service-dimension).
Card: t-20261119-hunt-metrics-appclass-log-writer (0428-122), state `wait` →
correction round on the SAME candidate chain.
PR: mcpdev80/baseharbor#1692, branch `lane-0428-appclass-writer`.
Prior candidate head: `b7f245f1042f594adbbd89b19a5f09e1c68e74e7` (reviewed REQUEST_CHANGES at `8956bf08e`, comment still stands).
This round's candidate head: `876329f733c7706a5a8dfb9a4227fb2c2698660c`.

## PLAN

  - done: ls-remote reconciliation of develop / branch / PR head, `plan.py show`, PR review comment read.
  - done: Isolated worktree cut from the fetched candidate head, base attestation written first.
  - done: RED regression on the real path FIRST: two services, identical app class, different service ids; and a service that disappears loses its source at the next reconcile.
  - done: Fix in the writer / reconcile path: service dimension in source-id AND in the reconcile boundary; render-time reconciliation registers the actually active service set and removes stale entries.
  - done: Local matrix of the affected group, plus gofmt / go vet / source-readability.
  - done: Monotone hopf onto the base target, push, exact-head CI watched to a terminal state (self-run duty).
  - done: This akte committed and pushed to origin/main, END posted.

## Reviewer verdict this round answers

CODEX-REVIEW REQUEST_CHANGES at `8956bf08e40e52b84a0dae55a9f1cb54db957636` (PR #1692
comment): the writer closed the no-writer gap for one service and the selected
tests/CI were green, but the established runtime log contract identifies a source
by application, environment, class, provider AND service
(`docs/architecture/runtime-log-source-contract.md`), and `applicationLogSource`
built its ID from the constant `workload` while
`ReconcileMatching(ApplicationLogBoundary(...))` replaced the whole
application/environment class space with one desired entry. Binding a second
service therefore overwrote the first service's signal, and the new regression
asserted that collapse instead of forbidding it.

Recipe (verbatim from the mission): preserve the service dimension in the
source-id AND in the reconcile boundary; render-time reconciliation must register
the ACTUALLY active service set and remove stale entries (no appending old keys,
no swallowing new ones).

## What the corrected code does

- Identity: the ID and the Target both name the concrete workload service,
  through the existing `observability.ApplicationLogSourceID` token
  (`internal/observability/registry.go:594`). `workload`
  (`internal/logs/application_source.go:32`) is only the fallback for a caller
  that names no service — the bare workload identity — never a stand-in for the
  deployment's services.
- Whole-set boundary (`ReconcileApplicationLogSource`,
  `internal/logs/application_source.go:136`): builds the desired set from the
  caller's de-duplicated service names
  (`applicationLogSourceSet`, `internal/logs/application_source.go:91`;
  `deduplicateServiceNames`, `:157`) and reconciles it against the class space,
  so an enabled render replaces the space with exactly the active services:
  removed services are reclaimed, new ones registered, nothing accumulates.
- Per-service boundary (`ReconcileWorkloadLogSource`, the Loki driver Bind path,
  `internal/logs/application_source.go:207`): its predicate is narrowed to
  `applicationLogBoundary(m) && existing.ID == source.ID`, so one Bind updates
  or adds its own entry and leaves every sibling service's source untouched —
  the failure mode the review named.
- Render-time writer (`reconcileApplicationLogSource`,
  `internal/application/runtime_observability.go:110`) now derives its desired
  set from the deployment's workload service selection
  (`selectedWorkloadServiceNames`, `:87`): declared
  `Workload.Components`, else the single canonical workload service — the same
  selection `MaterializeWorkload` performs over the Compose document
  (`internal/application/workload.go:127`), so registry identity and the
  collector's `baseharbor_service` label cannot drift apart.
- `ConvergeManagedLogsForReconcile` (`internal/logs/application_source.go:194`)
  keeps its bare-identity contract by passing no service set.

## RED → GREEN

RED witness, on the prior candidate head `b7f245f10` with ONLY the new
regression file added (fresh clone in `/var/tmp/m122-red-fresh`, so no fix code
is present — this is the real path, not a fake):

```
--- FAIL: TestApplicationClassLogSourcesStayDistinguishablePerService
    appclass_log_writer_identity_test.go:98: workload log sources = 1 (SOURCE application:logs:demo:dev:workload), want 2
--- FAIL: TestApplicationClassLogSourceReconcileRegistersActiveServiceSet
    appclass_log_writer_identity_test.go:120: workload log sources = 1 (SOURCE application:logs:demo:dev:workload), want 2
--- FAIL: TestApplicationClassLogSourceBindKeepsSiblings
    appclass_log_writer_identity_test.go:152: unexpected workload log source SOURCE application:logs:demo:dev:workload
--- FAIL: TestApplicationClassLogSourceDisabledPolicyReclaimsEveryService
    appclass_log_writer_identity_test.go:181: workload log sources = 1 (SOURCE application:logs:demo:dev:workload), want 2
FAIL	github.com/mcpdev80/baseharbor/internal/logs
```

The first three are the review's identity regression; the fourth is the set
shrink case — one stale `workload` key where the two service entries belong.
Note the shape: the collapse was visible as `application:logs:demo:dev:workload`
carrying `runtime://bh-local-demo-dev/workload` instead of
`.../api` and `.../worker`.

GREEN witness, candidate tree `805587483` (pre-hopf tree, same content):

```
$ go test ./internal/logs/ -run TestApplicationClassLogSource -count=1 -v
--- PASS: TestApplicationClassLogSourcesStayDistinguishablePerService (0.00s)
--- PASS: TestApplicationClassLogSourceReconcileRegistersActiveServiceSet (0.00s)
--- PASS: TestApplicationClassLogSourceBindKeepsSiblings (0.00s)
--- PASS: TestApplicationClassLogSourceDisabledPolicyReclaimsEveryService (0.00s)
--- PASS: TestApplicationClassLogSourceSurvivesManagedReconcile (0.00s)
--- PASS: TestApplicationClassLogSourceHasProductionWriter (0.00s)
--- PASS: TestApplicationClassLogSourceDisabledPolicyReclaims (0.00s)
--- PASS: TestApplicationClassLogSourcePolicyDisableReclaims (0.00s)
--- PASS: TestApplicationClassLogSourceReferenceClassCounterCheck (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/logs
```

## New tests and what they pin

`internal/logs/appclass_log_writer_identity_test.go` (new, cross-package
`logs_test`, so it drives the same public entries production uses):

- `TestApplicationClassLogSourcesStayDistinguishablePerService` — two services,
  identical app class, different service ids; two rounds of the render-time
  reconcile plus a Bind of each service. Asserts exactly two sources, each with
  its own service-carrying ID and its own `runtime://<project>/<service>`
  target, i.e. neither overwrites the other.
- `TestApplicationClassLogSourceReconcileRegistersActiveServiceSet` — after a
  two-service render, the deployment loses `worker`: the next reconcile removes
  exactly `application:logs:demo:dev:worker` (also asserted through
  `observability.RegistryHasSignal`) and preserves `api`; then a new service
  `cron` appears and is registered instead of being swallowed by the stale keys.
- `TestApplicationClassLogSourceBindKeepsSiblings` — the per-Bind form: binding a
  service the render did not register adds its own source and keeps the
  sibling's, twice in a row without duplication.
- `TestApplicationClassLogSourceDisabledPolicyReclaimsEveryService` — with a
  managed SQL instance present, disabling the application collect bit through
  `BASEHARBOR_LOGS_COLLECT_SOURCES=application-provider` reclaims every
  class-application service entry while the application-provider class of the
  same application/environment is untouched (the protection matrix the review
  asked to keep).

Adjusted existing assertions (they asserted the collapse, which the review
named): `internal/logs/appclass_log_writer_test.go:168` and `:181` — the
re-target case now states that a reconcile resolving a different service
registers that service's own entry and reclaims the previous one.
`:71` documents why the single `workload` ID there is the canonical-service
case (the manifest declares no workload components). The same-ID /
different-class / different-provider protection tests are unchanged and pass.

## Change list (file:line per change)

- `internal/logs/application_source.go:25-32` — `applicationLogServiceName` →
  `applicationLogCanonicalService`, documented as a fallback only.
- `internal/logs/application_source.go:50-89` — `applicationLogSource`: ID built
  from the concrete service (`ApplicationLogSourceID(m.Name, m.Environment, service)`)
  and Target `RuntimeTarget(project, service)`; missing application now fails
  closed as well.
- `internal/logs/application_source.go:91-105` — `applicationLogSourceSet`:
  desired set from the caller's service names, de-duplicated, empty list =
  canonical workload entry.
- `internal/logs/application_source.go:107-114` — `applicationLogBoundary`
  comment: this is the shared class boundary every writer goes through.
- `internal/logs/application_source.go:136-151` — `ReconcileApplicationLogSource`
  reconciles the whole ACTIVE set instead of one first-named service.
- `internal/logs/application_source.go:157-171` — new `deduplicateServiceNames`
  (replaces the removed `firstNamedService`, which is what dropped the second
  service).
- `internal/logs/application_source.go:194-196` — `ConvergeManagedLogsForReconcile`
  passes no service set (bare workload identity contract preserved).
- `internal/logs/application_source.go:207-227` — `ReconcileWorkloadLogSource`
  (Bind path) narrows its predicate to its own ID inside the class boundary, so
  a Bind never replaces the class space.
- `internal/application/runtime_observability.go:82-92` — new
  `selectedWorkloadServiceNames`: the deployment's active workload services,
  canonical `workload` when nothing is declared.
- `internal/application/runtime_observability.go:110-123` — render-time writer
  builds the desired set from that service set (disabled policy reclaims the
  whole class space, as before).
- `internal/logs/appclass_log_writer_test.go:71`, `:168`, `:181` — assertions
  restated for the service-carrying identity (see above).
- `internal/logs/appclass_log_writer_identity_test.go` — new (203 lines, four
  tests above).
- `internal/observability/registry.go` — net zero change in this round: the
  candidate's `ReconcileMatching` primitive (`:458`),
  `ApplicationLogSourceID` (`:594`), `ApplicationLogBoundary` (`:604`) and
  `PruneApplicationLogs` (`:611`) stay as reviewed; the additional
  `ReconcileApplicationLogSource` helper that an earlier commit of this round
  introduced was REMOVED again in favour of the narrowed predicate at
  `internal/logs/application_source.go:224`, because it pushed
  `internal/observability/registry.go` to 840 lines and the fail-closed
  `scripts/source-readability-audit.sh` (800-line limit) rejects it. Witness
  below.

## Local checks (affected group)

```
$ gofmt -l cmd internal spec contracts            # clean
$ go build ./internal/... ./cmd/...               # ok
$ go vet ./internal/logs/ ./internal/observability/ ./internal/application/   # ok
$ bash scripts/source-readability-audit.sh        # exit 0
Go file size PASS / Function span PASS / Regression ratchet PASS
$ go test ./internal/logs/ ./internal/observability/ ./internal/application/ ./internal/metrics/ -count=1
ok  github.com/mcpdev80/baseharbor/internal/logs
ok  github.com/mcpdev80/baseharbor/internal/observability
ok  github.com/mcpdev80/baseharbor/internal/application
ok  github.com/mcpdev80/baseharbor/internal/metrics
```

The `internal/metrics` package is included because the hopf brought #1694 in;
it passes on the merged tree.

Out-of-scope local failures observed while running the whole `go test ./...`
suite ON THIS COORDINATOR HOST (not on this candidate's path, and of the same
"needs a runtime/engine" family that the fix-1 akte recorded; these are ambient
host failures, not regressions introduced here — the CI units are the
authoritative check):

- `cmd/baha`: `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`:
  "start real isolated Core for App Edit: existing native network lacks a
  protected Core or shared backend owner".
- `internal/development`: `TestStagePinnedGitTreeExportsCommitNotDirtyWorktree`:
  "native Git archive failed: signal: killed".
- `internal/database`: several tests need a live PostgreSQL (e.g.
  `TestConnectorEnrollmentPersistentAtomicScope`).
- `internal/controlplaneruntime`:
  `TestRunStartsTLSHealthReadinessAndProtectedAPI`.

## CI integration of the new tests

No `.github/**` change was needed: the new
`internal/logs/appclass_log_writer_identity_test.go` is a normal Go test in
package `logs_test` and is auto-discovered by `go test ./internal/...`, which is
the "Run release source tests" step of the existing selected PR job
`.github/workflows/ci.yml:126` (`go test ./contracts/... ./internal/... ./spec/...`).
The job that runs it is `PR · Go unit · packages`, triggered by the `pull_request`
event on this PR (and by develop integration). Selection proof: `PR · Native gate
plan` and `PR · Trusted Plan` succeeded for head `876329f73` and the Go-unit
shards plus `PR · Validation · go-build` / `go-vet` were selected while the
runtime/HA/full-matrix jobs were `skipped` — i.e. the mapping selected the
affected group and did not open the whole matrix. The coordinator's warning case
(`PR · Go unit · packages` red on #1691's similar head) is covered: it runs here
and its result is recorded below.

## Base attestation and ancestry (branch provenance is proof)

Basis round-up of this turn: the coordinator's two calls landed while this round
was already in flight. `21161b101` (#1694, 0428-125) was lifted by hopf commit
`876329f73`, whose second parent IS `da76c5cf9` (#1696, 0428-126):

```
$ git rev-parse 876329f73^1 876329f73^2
805587483309c6426002e676338f1fe8e3f95837
da76c5cf9c96307038d5599bd130b89ecb1e8a4
```

That happened because the branch is in GitHub's merge-queue/auto-merge
set: `git ls-remote origin refs/pull/1692/merge` returned
`e85f62526b280715edba786764911caf8e99318e`, the test-merge of my head onto
develop `da76c5cf9`. Correction after reading the run payload itself — the
`pull_request` run executed MY head, not the merge ref:

```
$ gh api repos/mcpdev80/baseharbor/actions/runs/44473809584 \
    --jq '{event, head_sha, commit_id: .head_commit.id}'
{"commit_id":"876329f733c7706a5a8dfb9a4227fb2c2698660c",
 "event":"pull_request","head_sha":"876329f733c7706a5a8dfb9a4227fb2c2698660c"}
```

so the exact-head CI ran on `876329f73` itself (its tree already contains both
`21161b101` and `da76c5cf9`), which is what the mission's exact-head duty
requires; the merge-ref observation is reported as the queue state it is, not
as the test input.

Consequence of the queue: `git merge origin/develop` on the candidate answers
"Already up to date", so the push the round-up asks for would be a no-op, and a
second branch for the same card is forbidden (AGENTS 3.8). I kept exactly one
candidate head, `876329f73`, and verified the same content three ways instead of
manufacturing a commit: the ancestor tests above, the hosted exact-head run
(below), and this local integration-tree check.

## Integration-tree check (develop da76c5cf9 + candidate)

```
$ git worktree add --detach /var/tmp/m122-integration-check origin/develop   # da76c5cf9
$ git merge --no-ff 876329f73           # no conflicts
$ go build ./internal/...               # ok
$ go test ./internal/logs/ ./internal/observability/ ./internal/application/ ./internal/metrics/ -count=1
ok  github.com/mcpdev80/baseharbor/internal/logs
ok  github.com/mcpdev80/baseharbor/internal/observability
ok  github.com/mcpdev80/baseharbor/internal/application
ok  github.com/mcpdev80/baseharbor/internal/metrics
$ bash scripts/source-readability-audit.sh                                # exit 0
```

If the reviewer wants the merged tree hosted as a branch commit, the monotone
hopf commit is prepared locally but NOT pushed, so no second candidate appears.

`git log --oneline da76c5cf9..HEAD` lists ONLY this card's own commits — no
foreign candidate rides on top:

```
876329f73 hopf-merge 0428-122 r2: integrate develop 21161b101 (PR #1694) before the service-dimension fix
805587483 fix(0428-122): keep the service dimension in the class-application log identity
b7f245f10 chore(0428-122): remove test scratch fixtures committed by accident
c5f282241 refactor(0428-122): route the log writer through its single workload identity
221eb82ab refactor(0428-122): settle the class-application log listing on the existing selector
a898ad779 refactor(0428-122): one class-application log signal per application/environment
7ca579ec7 fix(0428-122): settle the application-class log writer contract details
8d972e9d8 fix(0428-122): give class application a production log writer
```

Planning repo witness (evidence lives ONLY in baseharbor-plan; verified before
the first evidence commit of this round):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git ls-remote origin refs/heads/main   # in baseharbor-plan
ce0513db79bf2b1e8361c98b0d10412a94ea9aa9	refs/heads/main
```
The second-to-last action of this round re-ran exactly that command; its output
is the line above. origin/main `ce0513db` carries the akte's preceding content,
and the two witness lines added after it (this one and the ps-witness block) land
in the akte commit this push publishes.

Product repo remote truth (`git ls-remote origin`, before any push of this round):

```
21161b101f66a47fb1a253ae17e87fe82567ba4d	refs/heads/develop
b7f245f1042f594adbbd89b19a5f09e1c68e74e7	refs/heads/lane-0428-appclass-writer
```

`gh pr view 1692 --json headRefOid,baseRefName,state` → head
`b7f245f1042f594adbbd89b19a5f09e1c68e74e7`, base `develop`, state OPEN: the
mission's numbers match remote truth, so this round cut NO new branch: it
continues the named candidate chain.

- Base ref this work started from (exact SHA): `b7f245f1042f594adbbd89b19a5f09e1c68e74e7`
  (`origin/lane-0428-appclass-writer`, the PR head).
- Base target for the hopf (exact SHA): `21161b101f66a47fb1a253ae17e87fe82567ba4d`
  (`origin/develop`, PR #1694 merged).
- Ancestry of my first commit: `git merge-base --is-ancestor b7f245f10 805587483`
  → true, so the base I cut from is an ancestor of my first commit; no foreign
  candidate is carried on top.
- Hopf: `git merge-base --is-ancestor 21161b101 HEAD` → true. The branch carries
  develop merge commits, so the base lift is a merge (monotone hopf), not a
  rebase, exactly as the mission prescribes.

`git log --oneline 21161b101..HEAD` on the pushed candidate (ONLY my chain's own
commits plus the develop merges the chain already carried; the five
`0428-122`-labelled commits are this card's earlier rounds, `da76c5cf9`/`21161b101`
are develop content reached through the hopf):

```
876329f73 hopf-merge 0428-122 r2: integrate develop 21161b101 (PR #1694) before the service-dimension fix
805587483 fix(0428-122): keep the service dimension in the class-application log identity
da76c5cf9 feat(cli,docs): print Warning marker in every acknowledging stage; align EN docs with i18n rename (0428-126) (#1696)
21161b101 fix(0428-125): bind environment into the runtime-metrics target file key and resource id (#1694)
b7f245f10 chore(0428-122): remove test scratch fixtures committed by accident
c5f282241 refactor(0428-122): route the log writer through its single workload identity
221eb82ab refactor(0428-122): settle the class-application log listing on the existing selector
a898ad779 refactor(0428-122): one class-application log signal per application/environment
7ca579ec7 fix(0428-122): settle the application-class log writer contract details
8d972e9d8 fix(0428-122): give class application a production log writer
```

Push witness (`git ls-remote origin refs/heads/lane-0428-appclass-writer`, after push):

```
876329f733c7706a5a8dfb9a4227fb2c2698660c	refs/heads/lane-0428-appclass-writer
```

## Exact-head CI (self-run duty)

Run: `44473809584` — "CI · PR #1692", event `pull_request`,
`head_sha == head_commit.id == 876329f733c7706a5a8dfb9a4227fb2c2698660c`, i.e.
exactly the pushed candidate. Started 2026-11-19T06:39:53Z.
URL: https://github.com/mcpdev80/baseharbor/actions/runs/44473809584

This lane watched the run itself from creation to its terminal state
(`gh run view` polls and `gh pr checks 1692 --watch`):

```
$ gh run view 44473809584 --json status,conclusion -q '.status+" "+.conclusion'
completed success
$ gh run view 44473809584 --json jobs -q '[.jobs[] | select(.conclusion=="success")] | length'   # 14 executed
$ gh run view 44473809584 --json jobs -q '[.jobs[] | select(.conclusion=="failure")] | length'   # 0
```

Terminal: 14 executed jobs, 0 failures; the runtime/HA/full-matrix jobs are
`skipped` by the selector, not bypassed. Executed set, with `PR · Go unit ·
packages` — the job the coordinator flagged as red on the similar #1691 head —
present and PASS here:

| job | result | duration |
| --- | --- | --- |
| Workflow policy | pass | 23s |
| PR · Native gate plan | pass | 5s |
| PR · Trusted Plan | pass | 9s |
| PR · Source format | pass | 22s |
| PR · Validation · go-build | pass | 45s |
| PR · Validation · go-vet | pass | 45s |
| PR · Focused Python | pass | 57s |
| PR Selected Checks | pass | 12s |
| PR · Go unit · owner | pass | 1m32s |
| PR · Go unit · packages | pass | 2m35s |
| PR · Go unit · cli-0 | pass | 2m42s |
| PR · Go unit · cli-1 | pass | 2m36s |
| PR · Go unit · cli-2 | pass | 4m55s |
| PR · Go unit · cli-3 | pass | 2m25s |

`PR · Go unit · packages` is the shard that runs
`go test ./contracts/... ./internal/... ./spec/...`, so it is the hosted
execution of this round's four new regressions and of the whole
`internal/logs`/`internal/observability`/`internal/application` writer matrix.
Job URL: https://github.com/mcpdev80/baseharbor/actions/runs/44473809584/job/135389465795

PR rollup on the pushed head (`gh pr view 1692 --json mergeable,mergeable_state`):
`MERGEABLE` / `clean`, `reviewDecision` empty (the review is a comment, so the
state stays REQUEST-CHANGES-pending-Codex — no CODEX verdict claimed here).

## Scope and rule compliance

- Write-set stayed on the card's path: `internal/logs/application_source.go`,
  `internal/logs/appclass_log_writer_test.go`, new
  `internal/logs/appclass_log_writer_identity_test.go`,
  `internal/application/runtime_observability.go`. `internal/observability/registry.go`
  ended this round byte-identical to the reviewed candidate content (its
  `ReconcileMatching`/boundary helpers are this card's own earlier rounds; the
  extra helper this round briefly added is gone). NO files of 0428-121's
  environment-filter topic were touched: `internal/metrics/**` appears in the
  diff of the hopf only as #1694's own develop content.
- No `.github/**` edit, no rerun, no workflow_dispatch, no merge, no CODEX
  verdict, no force-push. `git log --oneline origin/develop..HEAD` contains no
  workflow file.
- No subagents; every step in this session (AGENTS §4.8). No native `todowrite`
  tool exists in this tool surface, so the plan lives in the board file
  `workers/todos/mission-122-service-dimension.md.json` and in this `## PLAN`
  list, per the mission's fallback rule.
- Docker/Podman: none started by this lane (unit/contract tests only). Host
  census before/after in the cleanliness section.
- Scratch lives under `/var/tmp` only (`/var/tmp/m122-appclass-wt`,
  `/var/tmp/m122-red-fresh`, `/var/tmp/m122-plan-wt`); nothing added to
  `/home/marcel/dev/baseharbor-ecosystem` itself.

## Report on the pre-existing worktree that held the candidate branch

The local branch `lane-0428-appclass-writer` was checked out in
`/tmp/opencode/w-appclass-writer-wt` at the STALE head `8956bf08e` (remote was
already `b7f245f10`), which blocked a checkout of the named candidate branch.
Per the coordinator's ruling of this turn that worktree is left completely
untouched — including the untracked scratch directories it carries under
`internal/application/` (`prune-owner/`, `prune-sameid/`, `trace-handoff/`,
`trace-intent-off/`, `trace-owner-managed-collector/`,
`trace-owner-registered-external/`, `trace-policy-ext/`, `trace-policy-off/`,
`trace-unbound-prune/`). This lane therefore works in its own worktree on local
branch `lane-0428-appclass-writer-m122` and pushes it to
`refs/heads/lane-0428-appclass-writer`: exactly ONE candidate chain, monotone on
`b7f245f10` (ancestry proven above), no second remote branch. The pre-existing
local branch ref was preserved as `wip/0428-122-r2 → b7f245f10` before any of
this (no `git branch -D`, nothing rewritten).

## cleanliness

- Before: `docker ps -a --format '{{.Names}}'` → 7 names, all ambient
  `bh-local-shared-*` (core/admin/member OpenBao + shared Postgres): not this
  lane's, left untouched. `docker network ls` → 5.
- After: same 7 containers, same 5 networks; this lane started no container, no
  compose project, no volume (`diff /var/tmp/m122-containers-before.txt
  /var/tmp/m122-containers-after.txt` → no output). No `baha` state directories
  created under the host state root: every test used
  `t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())`.
- ps-witness, both ends byte-equal:

```
$ docker ps -a --format '{{.Names}}' | sort      # before AND after this lane
bh-local-shared-openbao-1
bh-local-shared-openbao-admin-1
bh-local-shared-openbao-member-1-1
bh-local-shared-postgres-1
bh-local-shared-postgres-admin-1
bh-local-shared-postgres-init-1
bh-local-shared-postgres-member-1-1
$ docker network ls --format '{{.Name}}' | wc -l  # before AND after
5
```
- This lane's own residue: only its `/var/tmp` worktrees (removed after END
  bookkeeping), nothing in a product repo, no `.evidence/` anywhere.
- cleanliness: host besenrein übergeben — 7 ambient containers and 5 networks
  unchanged, 0 lane-owned containers/networks/volumes/compose projects.

## END

END mission-122-service-dimension.md DONE — candidate `876329f733c7706a5a8dfb9a4227fb2c2698660c`
(PR #1692, branch `lane-0428-appclass-writer`, hopf onto develop `21161b101`,
monotone on the reviewed `b7f245f10`): service dimension preserved in the
source-id AND in the reconcile boundary; render-time reconciliation registers the
actually active service set and reclaims stale entries; RED on `b7f245f10` →
GREEN on the candidate for the four new service-dimension regressions; affected
group green locally plus gofmt/vet/readability; exact-head CI run `44473809584`
watched to its terminal state by this lane.
