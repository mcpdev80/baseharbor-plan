# 0428-122 fix-4 — FINAL candidate evidence (published by coordinator)

Recovered verbatim from the lane's local-only commit `3019c5136895737c4c5d7c9fbc0dc0c68baba960`, which was cut
out of its own worktree by a reset onto `origin/main`; the lane's clone is shallow, so the coordinator
reconciled it against current GitHub `origin/main` in an isolated worktree (no force, no history rewrite).
Coexists with the older `fix-3.md` on main, which predates the 859654861/695ad5494 CI moves.

# 0428-122 appclass log writer — fix-3 (implicit Compose workload selection)

Mission: mission-122-service-dimension.md (mission tag 122-service-dimension).
Card: t-20261119-hunt-metrics-appclass-log-writer (0428-122), state `blocked`
— correction round on the SAME candidate chain, following fix-1 and the fix-2
CODEX review.
PR: mcpdev80/baseharbor#1692, branch `lane-0428-appclass-writer`.
FINAL candidate head (this akte): `14f279867e76ddedaa5fe82488b7f5a827d410e7`
(monotone merge-hopf onto develop `695ad5494`, the in-window develop where
#1602/0428-077 and the CI-migration controller live; fix `102fcd907`).

## HEAD CHAIN (this round's monotone hopf sequence)

Each head is the merge-commit ancestor of the next; develop advanced through the
window every time, and each hopf kept my fix on top of the latest develop:

| Head | Base it landed on (develop) | Note |
| --- | --- | --- |
| `c21dc623532f30dd0caeb9695eeb1594d6057461` | `3b634232f` (#1592/0428-088) | registry.go extraction → `registry_log.go`, registry.go back to 765 lines (≤800) |
| `3f8024e81c1625c0ba83d5f34c12117560549765` | `3b634232f` (same) | intermediate; fix + env-threading + extraction in one hopf tree |
| `aac6b2f8ee8b5705c30c5d67571beb5ec4b5f3ed` | `5a68196a1` (#1602/0428-077) | first hopf onto 077 |
| `97eb3625af9203f269ec6f516dc0ae586a47d00c` | `859654861` ("CI fast feedback with base-owned required checks") | hopf onto CI-semantics migration |
| `14f279867e76ddedaa5fe82488b7f5a827d410e7` | `695ad5494` ("Pin lane-compatible CI migration controller") | FINAL hopf onto latest develop |

Ancestry witnesses on the final head `14f279867`:

```
$ git -C baseharbor rev-list --parents -n 1 14f279867
14f279867...  97eb3625af...  695ad54944734e9976fe9cc1dbae117482677dc6
$ git -C baseharbor merge-base --is-ancestor origin/develop 14f279867        # exit 0 (ancestor)
$ git -C baseharbor merge-base --is-ancestor 97eb3625af9203f269ec6f516dc0ae586a47d00c 14f279867   # exit 0
$ git -C baseharbor merge-base --is-ancestor 5a68196a1e6bf627fbd8e17f106d58f1e63f6ce6  14f279867   # exit 0 (all prior bases carried)
$ git -C baseharbor merge-base origin/develop 14f279867                      # 695ad5494 (monotone hopf)
$ git -C baseharbor merge-tree --write-tree origin/develop 14f279867         # exit 0, 0 CONFLICT lines
$ git -C baseharbor merge-base --is-ancestor 102fcd90707ecd1e0792fc3930e0ad09ef732af2 14f279867   # exit 0 (my fix carried)
```

No foreign candidate rides on top: `git log --oneline --no-merges origin/develop..HEAD`
lists only this card's own commits (the eleven `0428-122` chain commits up to
`102fcd907`, plus the three fix-3 commits `a64c6373e`/`5d147f71c`/`c21dc6235`).

## CI WITNESSES (exact-head runs, §4.6 self-run duty)

| Run | Head | Base integrated | Conclusion | Why not final |
| --- | --- | --- | --- | --- |
| `44530261060` | `3f8024e81` | `3b634232f` | **FAILURE** — `PR · Source format` (registry.go 833 lines > 800) | fixed by the extraction → `c21dc6235` |
| `44532116583` | `c21dc6235` | `3b634232f` | SUCCESS | base `3b634232f` no longer the in-window develop |
| `44534195307` | `aac6b2f8` | `5a68196a1` | SUCCESS (0 fehljobs) | develop `859654861` (13:32:13Z) post-dates run start (13:30:53Z); required checks now base-owned |
| `44535325043` | `97eb3625a` | `859654861` | SUCCESS (informative) | develop `695ad5494` (13:39:54Z) post-dates run start (13:37:35Z) |
| **`44536505959`** | **`14f279867`** | **`695ad5494`** | **SUCCESS** | **final run on the latest in-window develop** |

Run `44534195307` was never final: it started 13:30:53Z under the *approaching*
base-workflow file, while develop `859654861` ("CI fast feedback with
base-owned required checks") was created 13:32:13Z — the run integrated a base
whose required-check rules were superseded 1m20s later. Same logic for
`44535325043` (start 13:37:35Z < develop `695ad5494` at 13:39:54Z). The final
run `44536505959` started 13:44:47Z, **6 minutes after** the last develop change
(13:39:54Z) — the queue560 timestamp check (`git show -s --format=%cI origin/develop`)
passes: run start is strictly after the last develop move.

Run `44536505959` conclusions (all executed jobs):

```
success | PR · Source format            (registry.go 765 ≤ 800; extraction c21dc6235)
success | PR · Validation · go-build
success | PR · Validation · go-vet
success | PR · Go unit · packages
success | PR · Go unit · owner
success | PR · Go unit · cli-0
success | PR · Go unit · cli-1
success | PR · Go unit · cli-2
success | PR · Go unit · cli-3
success | PR · Focused Python
success | PR · Native gate plan
success | PR Selected Checks   <—— aggregate (the only owner-accepted evidence)
skipped | Targeted HA · docker       (see runtime-evidence note below)
skipped | Targeted HA · podman       (see runtime-evidence note below)
skipped | PR · Exact Candidate       (base-owned advisory migration, not evidence)
skipped | PR · Candidate-added checks (advisory)   (base-owned advisory migration)
skipped | PR · Selected Runtime
skipped | PR · Selected Core-less · ${{ matrix.runtime }}
skipped | all release/pre-release/matrix gates (out of this card's scope)
```

## NEW base-owned CI semantics (develop `859654861` / `695ad5494`) — read the final run against

The two commits that develop added after my base `859654861` are **both CI-half**:

```
$ git -C baseharbor diff --name-only 859654861 origin/develop
.github/workflows/ci.yml
scripts/test_ci_check_routes.py
```

NONE of these are my code files and NONE of them are the three 0428-077 files I
was warned about (`internal/metrics/perses_dashboards_hosts.go`,
`internal/logs/render.go`, `internal/telemetry/otlp_payload.go`). The
`859654861` change to `ci.yml` adds `MIGRATION_CONTROLLER: 8596548615…`
(comment: "Merged lane-compatible planner; old lane bases fall back to this
immutable commit") and moves `Run candidate-added validation checks OUTSIDE the
required plan`; `695ad5494` ("Pin lane-compatible CI migration controller")
tightens the controller. This is exactly why `44534195307` (base `5a68196a1`)
and `44535325043` (base `859654861`) are intermediate: the required checks the
acceptance sees now come from the base, not from the head's own diff.

`candidate_advisory_required` for MY diff — computed by the trusted planner
`.github/workflows/ci.yml:794-804` (`any(path.startswith('.github/workflows/')
or path.startswith('scripts/') …)`): my diff touches **zero** `ci.yml`/`scripts/`
paths, so `candidate_advisory_required == 'false'` → my candidate-added
validations stay in the required plan, NOT loosened by me. Observed in the final
run: `PR · Exact Candidate` and `PR · Candidate-added checks (advisory)` are
**skipped** (not run) under the migration controller because my diff is not a
lane-CI change — this is the base-owned policy, not a relaxation I introduced.
Evidence of the planner's classification, run locally on the final diff:

```
$ git diff --name-only --diff-filter=ACDMRT origin/develop 14f279867   (my changed paths)
internal/application/runtime_observability.go
internal/application/runtime_observability_test.go
internal/application/runtime_observability_trace_source_test.go
internal/application/runtime_postgres.go
internal/logs/appclass_log_writer_identity_test.go
internal/logs/appclass_log_writer_test.go
internal/logs/appclass_writer_implicit_selection_test.go
internal/logs/application_source.go
internal/logs/realization.go
internal/observability/environment.go
internal/observability/registry.go
internal/observability/registry_log.go
$ python3 pr-native-gate-plan.py --changed-paths <above>   →   {"include":[]}
```

`{"include":[]}` = the trusted native gate planner selects **no** docker/podman
gate for this diff. That is why `Targeted HA · docker`/`podman` are skipped on
this base: my changed paths (`internal/application/*`, `internal/observability/*`,
`internal/logs/*`) resolve to no native gate in the coverage catalog
(`pr-native-gate-plan.py:31-32`: only rows with `runtime ∈ {docker, podman}`
are ever selected).

## RUNTIME-EVIDENCE DECISION (owner decides; not mine to close)

The card acceptance (~line 69 "prove native Docker and rootless Podman/Quadlet
separately where required; unit fakes do not replace live runtime evidence") is
met here by **negative evidence**: the trusted native-gate planner classifies
this diff as `{"include":[]}` (no docker/podman gate applies), so
`Targeted HA · docker`/`podman` are correctly skipped and the aggregate
`PR Selected Checks` gates on `NATIVE_REQUIRED=false` (skipped) — which the
base's `ci.yml` `PR Selected Checks` step accepts (case `false) test "$NATIVE_RESULT" = skipped`).

I did NOT fire a docker/podman cell myself (no guessing, no scope creep). This
is recorded as **explicit CI coverage debt item 114**: the runtime-evidence
acceptance question is left for the owner to close, with the selection-rule
witness `internal/*` → no native gate (`{"include":[]}`, plannable locally) and
the exact file:line of the selection rule
(`.github/workflows/ci.yml:426-475` `pr_native_impact`, gated by
`scripts/pr-native-gate-plan.py` against the changed paths). If the owner's
reading of the acceptance is that unit fakes are insufficient even for a
non-native diff, this is the 114-draht point — documented here with the
selection-rule evidence, not buried as my own relaxation.

## LOCAL CHECKS (final head `14f279867`)

```
$ wc -l internal/observability/registry.go
765 internal/observability/registry.go          (≤ 800; extraction c21dc6235)
$ bash scripts/source-readability-audit.sh
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS
Regression ratchet PASS
$ go build ./...                                   # ok
$ go vet ./internal/observability ./internal/application   # ok
$ go test ./internal/observability ./internal/application -run "^TestRoute|^TestManagedRuntimeObservability|^TestWorkload" -count=1
ok  github.com/mcpdev80/baseharbor/internal/observability
ok  github.com/mcpdev80/baseharbor/internal/application
```
(no full `./...` run; the only source-readability baseline hit is
`internal/providers/runtime/podman/lifecycle.go` at 843 lines, a pre-existing
baseline file, NOT this card's change).

## WHAT THE CORRECTED CODE DOES

- `selectedWorkloadServiceNames(m, repositoryRoot)` resolves the ACTUALLY active
  workload service set in the order MaterializeWorkload reads it: (1) the
  manifest's declared `Workload.Components`; (2) the non-managed Compose services
  of the workload when the manifest declares none (implicit workload —
  `selectWorkloadServices` selects ALL available non-managed services when
  `requested` is empty), instead of the synthetic singleton `workload`; (3) the
  single canonical workload service when no compose source is resolvable.
- New `implicitComposeWorkloadServices(m, repositoryRoot)` reuses
  `ResolveWorkloadCompose` + `composeServiceNames` + `selectWorkloadServices`,
  so registry identity and MaterializeWorkload cannot drift for the same
  manifest; returns false (not an error) when no workload compose source exists.
- `ReconcileManagedRuntimeObservability`, `reconcileManagedRuntimeObservability`,
  `reconcileApplicationLogSource`, `selectedApplicationLogSources` carry
  `repositoryRoot` through; `runtime_postgres.go` passes `files.Dir` (best
  available root at realization), an empty value keeps the manifest selection.
- `ListWorkloadLogSources` threads `m.Environment` into `observability.List`
  (#1691 env-threading). `SourceEnvironment` (environment.go) completes #1691's
  env-filter for the `application:logs:` grammar via
  `applicationLogSourceEnvironment` (logs twin of `applicationMetricsSourceEnvironment`).
- **Extraction (post-hopf, `c21dc6235`):** after the hopf onto develop,
  `registry.go` had crossed the readability limit (833 lines; `PR · Source format`
  failed, 0428-121 precedent). Moved `ApplicationLogSourceID`,
  `ApplicationLogBoundary`, `PruneApplicationLogs`, `pruneApplicationSignals`
  and `ListTraces` into a same-package `internal/observability/registry_log.go`;
  `registry.go` is now 765 lines (≤800). Same primitives, same callers.

## BASE ATTESTATION (branch provenance is proof)

Monotone merge-hopf, not a rebase — the chain is in GitHub's merge-queue set, so
the base is the hopf target. Final head `14f279867`'s transitive parents trace
back through `97eb3625a` → `859654861` → `5a68196a1` → `3b634232f`, every one an
in-window develop tip; `merge-base origin/develop HEAD == 695ad5494`.

Product remote truth (`git ls-remote origin`, after push):

```
695ad54944734e9976fe9cc1dbae117482677dc6	refs/heads/develop
14f279867e76ddedaa5fe82488b7f5a827d410e7	refs/heads/lane-0428-appclass-writer
```

## EVIDENCE ORIGIN (own clone, NOT the shared copy)

Evidence was written to an OWN clone at `/var/tmp/m122-plan-wt` (remote =
`https://github.com/mcpdev80/baseharbor-plan.git`) and pushed to `origin/main`
after `git fetch origin main` + `git rebase origin/main` (no force, no reset over
foreign commits). The shared working copy
`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` was NOT touched this
round (Owner directive 2026-11-19, `receive.denyCurrentBranch`).

## SCOPE AND RULE COMPLIANCE

- Write-set stayed on the card's path:
  `internal/application/runtime_observability.go`,
  `internal/application/runtime_postgres.go`,
  `internal/logs/application_source.go`, new
  `internal/logs/appclass_writer_implicit_selection_test.go`, the two existing
  appclass test groups, `internal/observability/environment.go`, and the
  `internal/observability/registry_log.go` extraction. NO `.github/**` edit, NO
  `internal/metrics/**` (0428-121 topic) and NONE of the 0428-077 files
  (`perses_dashboards_hosts.go`, `render.go`, `otlp_payload.go`) touched — the
  077 files live in develop and the hopf only brought in `runtime_postgres.go`'s
  `RuntimeComposeYAMLForProject` (+7, outside the reconcile path) plus the CI-half
  `ci.yml`/`test_ci_check_routes.py` (which this card does not edit).
- No merge by this lane, no CODEX verdict, no force-push, no subagent (§4.8).
- Runtime-evidence: NO docker/podman/compose project started (unit/contract
  tests only); the native-gate planner classifies the diff as `{"include":[]}`
  → `Targeted HA · docker`/`podman` correctly skipped; recorded as explicit
  coverage-debt item 114 for the owner (see above).
- Scratch lives under `/tmp/opencode/m122-r3-wt` only; evidence under
  `/var/tmp/m122-plan-wt` only; nothing added to `/home/marcel/dev/baseharbor-ecosystem`.

## CLEANLINESS

- Before/after: this lane started no container, no compose project, no volume
  (`diff` of before/after → no output). Every test used
  `t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())`. Ambient
  `bh-local-shared-*` containers left untouched.
- cleanliness: host besenrein übergeben — ambient containers/networks unchanged,
  0 lane-owned containers/networks/volumes/compose projects.

## END

END mission-122-service-dimension.md DONE — FINAL candidate
`14f279867e76ddedaa5fe82488b7f5a827d410e7` (PR #1692, branch
`lane-0428-appclass-writer`, monotone merge-hopf onto in-window develop
`695ad5494`, fix `102fcd907`): the render-time reconcile carries the actually
selected Compose service set into the reconcile boundary instead of the
synthetic `workload`, reclaims stale entries, and the implicit two-service +
shrink regressions pass on the real path; targeted `go test`/`gofmt`/`go build`/`go vet`/source-readability
green; registry.go 765 lines (≤800) via the `registry_log.go` extraction. Final
exact-head CI `44536505959` on develop `695ad5494` (run start 13:44:47Z > last
develop change 13:39:54Z): `PR Selected Checks => success` (aggregate), all Go
shards + source-format + go-build/vet green; `Targeted HA · docker`/`podman`
skipped because the trusted native-gate planner classifies this diff as
`{"include":[]}` — recorded as CI coverage-debt item 114 for the owner's
runtime-evidence decision, NOT closed by me. No `.github/**` edit, no merge, no
CODEX verdict, no subagent. Card stays BLOCKED pending owner's 114 decision and
CI-list final verification.
