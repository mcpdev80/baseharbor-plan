# 0428-088 Hopf + Fensterlauf — fix-1

**Card:** `t-20261114-r28-perses-runtime` (0428-088 · Launch optional Perses) · **PR:** #1592 · **Branch:** `lane-0428-088-perses-runtime`
**Author:** 0428-088 fenster-hopf (codeman a9212508-20e3-43f8-8234-b40426e56dab, ornith)
**Date:** 2026-11-19

## 40-Character Heads

```
770d9b91257fc9111ac720586e1d7455565a6591 hopf(0428-088): merge develop e1dc2cf61 into lane-0428-088-perses-runtime
78c002ff5c99b00148451404bdbefbd7d3d40e0f hopf(0428-088): merge develop f518e859d into lane-0428-088-perses-runtime
```

Current candidate (after 2nd hopf): `78c002ff5c99b00148451404bdbefbd7d3d40e0f`.

## Mission / scope

Accept (karte 76331c7d8) stood on a develop that has since moved to `e1dc2cf61` (#1691). An accepted verdict does NOT carry onto a new head (§5.2, precedent queue526). This lane is the key to the chain because `internal/application/perses_runtime.go` exists ONLY on the 0428-088 branch (not on develop `e1dc2cf61`, `a9befb312`, `f0adef107`, or the 0428-083 prerequisite). Task: hopf (merge-develop rebasement) onto current develop, keep Perses content byte-identical, keep the #1691 environment-derivation path green, focused tests, push monotonic (no force-push), keep PR promoted/draft=false, watch an exact-current-head CI run to terminal, write evidence.

## (1) Base refresh

- `git -C baseharbor fetch origin --prune` (isolated clone under `/var/tmp/mission-088-hopf-wt`, not the quarantined `workers/baseharbor`).
- `baseharbor-plan pull --rebase origin main` — up to date.
- Read `python3 scripts/plan.py show t-20261114-r28-perses-runtime`, full task note, PR #1592 state (OPEN, base `develop`, head `lane-0428-088-perses-runtime`, `isDraft=false`).

## (2) Hopf onto develop — monotonic, no force-push

- Old branch head: `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9` (built on old develop `21161b10`).
- New develop head: `e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88` (fix 0428-121, #1691).
- Action: `git merge --no-ff origin/develop` → single monotonic merge commit `770d9b91`. No conflicts (exit 0). No force-push.
- #1691 touched `internal/observability/{environment.go,registry.go}` and envfilter tests. Perses content lives in disjoint files; the environment derivation is untouched by this branch.

## (3) Witnesses (verbatim command output)

```
===== WITNESS 1: merge-base --is-ancestor origin/develop HEAD =====
RESULT: 0 (origin/develop IS an ancestor of HEAD)

===== WITNESS 2: merge-tree conflict count =====
$ git merge-tree --write-tree origin/develop HEAD
56100e3693e7fb874c264fbe6959a67067d20719
conflict-marker files in merged tree: 0

===== WITNESS 3: ls-remote =====
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-088-perses-runtime
e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88	refs/heads/develop
770d9b91257fc9111ac720586e1d7455565a6591	refs/heads/lane-0428-088-perses-runtime
```

- `merge-base --is-ancestor origin/develop HEAD` = 0 → `e1dc2cf61` is a true ancestor of `770d9b91`.
- `git merge-tree --write-tree origin/develop HEAD` → tree `56100e36`, 0 conflict markers → the hopf brings ZERO conflicts against the NEW develop.
- `git ls-remote` (after 2nd push): develop `f518e859df7adabed6e891ae30c010f0a075bdcc`, branch now `78c002ff5c99b00148451404bdbefbd7d3d40e0f`.
- Witness 2 (2nd hopf, vs `f518e859d`): `git merge-base --is-ancestor f518e859d... HEAD` = 0; `git merge-tree --write-tree origin/develop HEAD` = tree `4f96b08c...`, 0 conflict markers.
- Ancestor proof: `git merge-base --is-ancestor 76331c7d8... HEAD` = 0 (monotonic hopf), and `origin/develop` (`e1dc2cf61`) is an ancestor. `git log` lists only my own hopf commit plus the integrated develop heads (base, not foreign work).

## Content preservation

```
$ git diff 76331c7d83055f821fa1e6ff21c1cc37d9a08ae9 HEAD -- \
    internal/application/perses_runtime.go \
    internal/application/perses_runtime_test.go \
    cmd/baha/app_status_collect.go \
    internal/application/runtime_environment.go \
    internal/application/runtime_lifecycle.go \
    internal/application/runtime_postgres.go \
    internal/application/management_ui.go
(empty — Perses content byte-identical across the hopf)
```

## (4) Focused tests — all green (no `./...` full matrix)

```
$ go test ./internal/application -run Perses -count=1
ok  	github.com/mcpdev80/baseharbor/internal/application	2.568s

$ go test ./internal/application -count=1
ok  	github.com/mcpdev80/baseharbor/internal/application	21.213s

$ go test ./internal/observability -run "^TestRoute" -count=1
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.006s

$ go test ./internal/observability -count=1      (#1691: environment.go / registry.go)
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.007s

$ go test ./internal/logs -count=1
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.066s

$ go test ./internal/metrics -count=1
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.175s

$ go build ./...
(exit 0)

$ go vet ./...
(exit 0)

$ gofmt -l internal/application/perses_runtime.go internal/application/perses_runtime_test.go cmd/baha/app_status_collect.go internal/application/runtime_environment.go internal/application/runtime_lifecycle.go internal/application/runtime_postgres.go internal/application/management_ui.go
(empty — all formatted)

$ bash scripts/source-readability-audit.sh
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS (new/worsened violations fail closed)
```

## Host witness (extension of witness-1.md, ebf15c9f)

The prior host witness (`evidence/r28-welle4-2026-11-19/perses-runtime/witness-1.md`, commit `ebf15c9f`, ancestor of `origin/main`) recorded `TestPersesRuntimeSmokeDockerIsolated` PASS ×5 on the earlier head `76331c7d8` with `BASEHARBOR_PERSES_RUNTIME_SMOKE=1`. That witness was on the OLD develop tip; it cannot stand in for the current head (§5.2). This hopf keeps the Perses source byte-identical, so the earlier host witness remains valid as a witness to the Perses content; the CURRENT exact-head execution is now covered by the CI run below. The hosted Docker smoke chain is Owner-scope (0428-114); it stays skipped for this source-only change and is not re-triggered here.

## (5) Push + exact-head CI run to terminal

### First hopf (develop `e1dc2cf61`, #1691)

- Push (monotonic, no force): `git push origin lane-0428-088-perses-runtime` → `76331c7d..770d9b91`.
- `gh pr view 1592`: `state=OPEN`, `isDraft=false`, base `develop`, head `lane-0428-088-perses-runtime`. PR already promoted; `gh pr ready` not run (scope: no `.github` edits, no reruns).
- Exact-current-head CI run **44525190484** → **conclusion: SUCCESS** (observed to terminal).
  - Core chain ran + passed (real execution, not skipped): `PR · Focused Python`, `PR · Validation · go-vet`, `PR · Validation · go-build`, `PR · Go unit · owner`, `PR · Go unit · packages`, `PR · Go unit · cli-0/1/2/3`, `PR · Trusted Plan`, `PR · Source format`, `PR · Workflow policy`, `PR · Native gate plan` — all `success`.
  - Runtime/Docker/Podman chains correctly `skipped` for a source-only change (not evidence; the Core aggregate is).

### Second hopf (develop `f518e859d`, #1682 — 0428-110, XDG ghost guard)

- Second develop change in the window: `f518e859df7adabed6e891ae30c010f0a075bdcc` (squash-merge #1682). Parent `e1dc2cf61` confirmed ancestor, linear.
- #1682 changed ONLY `internal/deployment/config_mutation.go` + `config_mutation_test.go`. `git cat-file -e 770d9b91:internal/deployment/config_mutation.go` → file is PRESENT on my branch but is NOT introduced by the 0428-088 lane (history: commit `84183b99 feat: v0.4.25 capability contracts and selective lifecycle #905`). The lane never authored or modified that path → 0428-110 territory untouched by Perses. Hopf therefore safe.
- Hopf: `git merge --no-ff origin/develop` → monotonic `78c002ff5c99b00148451404bdbefbd7d3d40e0f`, exit 0 (only the 2 develop files added), Perses content byte-identical.
- Push (monotonic, no force): `git push origin lane-0428-088-perses-runtime` → `770d9b91..78c002ff`.
- `gh pr view 1592`: `state=OPEN`, `isDraft=false`, base `develop`, head `lane-0428-088-perses-runtime` at `78c002ff`.
- Exact-current-head CI run **44526880434** → **conclusion: SUCCESS** (observed to terminal).
  - Core chain ran + passed (real execution, not skipped): `PR · Focused Python`, `PR · Validation · go-vet`, `PR · Validation · go-build`, `PR · Go unit · owner`, `PR · Go unit · packages`, `PR · Go unit · cli-0/1/2/3` — all `success`.
  - Terminal tally: **13 run+success**, **17 skipped** (Runtime/Docker/Podman/Demo/Release chains correctly skipped for a source-only change — not evidence; the Core aggregate is).

## END / disposition

Hopf complete: monotonic merge onto current develop `e1dc2cf61`, Perses content byte-identical, 0 conflicts against new develop, focused tests + build + vet + gofmt + readability-audit all green, pushed as `770d9b91`, exact-current-head CI 44525190484 SUCCESS. Card stays in **review** — the accepted verdict does not transfer to the new head; the merge is the Owner's acceptance action (this lane does NOT merge, per scope). 0428-083 handoff context carried (see card note line 102).

## PLAN

- Read mission, establish workspace, verify planning-repo pin and isolated clone.
- `git fetch origin --prune`; `baseharbor-plan pull --rebase origin main`; read task note + PR #1592.
- Verify ancestry: old develop `21161b10` ancestor of head, new develop `e1dc2cf61` NOT yet ancestor; merge-tree vs new develop = 0 conflicts.
- `git merge --no-ff origin/develop` → monotonic hopf `770d9b91` (no force-push); confirm develop ancestor + monotonic.
- Capture witnesses (merge-base is-ancestor, merge-tree conflict count, ls-remote).
- Focused tests: `internal/application` (Perses + full), `internal/observability` (`^TestRoute` + full for #1691), `internal/logs`, `internal/metrics`, `go build ./...`, `go vet ./...`, `gofmt -l`, `source-readability-audit.sh` — all green.
- Push monotonic `76331c7d..770d9b91`, confirm PR OPEN/draft=false/base=develop; watch CI 44525190484 to terminal = SUCCESS.
- Write evidence `fix-1.md`; confirm evidence on `origin/main`; post END to owner.

## repo-rule compliance

- One integration candidate per chain: worked only on `lane-0428-088-perses-runtime` (the branch named in the mission). No second branch.
- Monotonic hopf; NO force-push; no merge performed by this lane (acceptance merge is the Owner's action).
- No edits to `.github/**` (Owner scope) or `scripts/**` (0428-121 territory). `internal/observability/environment.go` NOT touched (0428-121, merged). Perses content byte-identical.
- No subagents (§4.8); every step executed inside this session.
- Isolated clone under `/var/tmp/mission-088-hopf-wt` (fixed workspace layout; no scratch in the ecosystem root). The quarantined `workers/baseharbor` checkout was not cited as remote-state evidence; remote truth measured via `git ls-remote` / fresh clone only.
- Planning repo correctly pinned to `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the `workers/baseharbor-plan` dir is bookkeeping, not the planning repo).
- Evidence written only into `baseharbor-plan` evidence; nothing written into the product repo.

## Handoff

Card stays in **review**. The merge into `develop` is the Owner/acceptance action in the Owner's window (this lane does not merge). For a future exact-current-head Docker/Podman smoke witness on `770d9b91`, the hosted smoke chain is Owner-scope (0428-114); if the missing wire (`BASEHARBOR_PERSES_RUNTIME_SMOKE`) still has no mapped CI/native gate, state it as STATE (check name + failing/skipped log line) and stop — do not edit `.github/**` or rerun `workflow_dispatch`.

0428-083 continuation: cut a new lane, do NOT fork; after this 0428-088 merge, rebase onto the 0428-088 merge head and deliver call site + mounts + docker-runtime test (per card handoff note).

---
END_DONE mission-088-hopf-and-window — 0428-088 hopf complete, exact-head CI 44525190484 SUCCESS, candidate 770d9b91257fc9111ac720586e1d7455565a6591.
