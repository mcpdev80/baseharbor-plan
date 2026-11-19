# 0428-110 r2 — XDG ghost-guard route restriction (fix-2)

Lane: `lane-0428-110-mutation-loud` / PR #1682 / card t-20261117-hunt-uid-docs-110
Working worktree: `/tmp/opencode/mission-110-ghost-fix-wt` (isolated; pre-existing `/tmp/opencode/mission-110-xdg-ghost-guard-wt` left untouched, reported)

## TASK

Correct the reviewed candidate `fb6f36936924ca07a9de512c113dc138d38360f1`
(0428-110 r2). The reviewed `Config.saveWithPreparation` rejected the grandparent
`config.yaml` on every route. On the `BASEHARBOR_STATE_DIR` route the resolved
root is `<state>/config`; a sibling `<state>/config.yaml` one level up is a
legitimate coincidence, not an XDG double-append — yet the save route rejected it
with an XDG-ghost error.

Verdict (CODEX-REVIEW `1682-0428-110.md`): REQUEST CHANGES. Restrict the ghost
guard to the XDG route (`configGhostRoot` or an explicit route predicate), keep
the generic rejection of the genuine XDG ghost, add the missing state-dir
regression test, STOP if the XDG ghost is accepted or the state-dir operation
writes outside its configured location.

## BASE ATTESTATION

- Base ref at mission start (develop head): `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
- **Window update (Owner 2026-11-19):** develop was moved by squash-merge of #1691 (0428-121). New develop head: `e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88` (merged_by mcpdev80, 2026-11-19T11:56:52Z). Content witness: `internal/observability/environment.go`, `envfilter_route5_listseam_test.go`, `envfilter_route2_test.go` are file-hash-identical between PR head `e5a943d1b` and develop; `SplitN(value, ":", 3)` at `environment.go:134` in develop.
- `git merge-base --is-ancestor origin/develop 171a32e90(old)` → NO (old head based on da76c5cf9).
- Rebased onto new develop → new head `7cc41858b`; `git merge-base --is-ancestor origin/develop 7cc41858b` → YES.
- `git merge-tree --write-tree origin/develop HEAD` conflict count: **0**; tree SHA `549d746316cafc792154013145309431f1c7ad75`.
- Commit count `origin/develop..HEAD`: **1** (only my commit `7cc41858b`).
- Candidate `fb6f36936` is NOT in my ancestry (no foreign commit).
- **New develop touching my write-set?** NO. `internal/deployment/config_mutation.go`/`config_mutation_test.go` are untouched by #1691. develop's other changes (`internal/observability/environment.go`, `envfilter*` tests, `internal/runtime/project_names.go`) are disjoint from my scoped fix — confirmed by the zero-conflict rebase.

## FIX

File: `internal/deployment/config_mutation.go`, function `saveWithPreparation`.

Before (candidate line ~100):
```go
if _, statErr := os.Lstat(root); os.IsNotExist(statErr) {
    if gp := filepath.Dir(filepath.Dir(path)); gp != filepath.Dir(path) {
        if _, err := os.Lstat(filepath.Join(gp, "config.yaml")); err == nil {
            return configRootMisconfiguration(path, true)
        }
    }
}
```

After (route-restricted via the XDG-scoped `configGhostRoot`):
```go
if _, statErr := os.Lstat(root); os.IsNotExist(statErr) && configGhostRoot(root) {
    return configRootMisconfiguration(path, true)
}
```

`configGhostRoot(resolvedDir)` is route-specific: it returns true only when
`filepath.Base(resolvedDir) == "baseharbor"` (the XDG route) and a sibling
`config.yaml` sits one level up. On the state route the resolved dir is
`"config"`, so the guard is false and the sibling `<state>/config.yaml` no longer
blocks the first write. The genuine XDG double-append is still rejected.

Added in this file: `configGhostRoot` and `configRootMisconfiguration` helpers.
Reverted the candidate's wider `LoadConfigForMutation`/`LoadConfig`/`Save`
additions (they referenced a `configRootUnusable` that lives in `target.go`,
outside this write-set) to keep the change minimal and scoped to the ghost route.

## WRITE-SET / target.go

`internal/deployment/target.go` is UNCHANGED (reverted to develop). The fix only
reuses the `configGhostRoot` route predicate logic; it does not modify any
existing function in `target.go`. No change to `target.go` was required.

## REPRODUCTION (confirmed on candidate)

`go test ./internal/deployment/ -run Ghost -count=1` against the reviewed head
`fb6f36936` failed the state-dir case with:
```
BaseHarbor config root is configured but the config.yaml is missing: .../config/config.yaml.
The config root resolves into an extra directory level (XDG double-append):
BaseHarbor state also sits one level up at .../config.yaml. ...
```
After the fix the same test passes.

## PLAN

- Read mission, review verdict, config_mutation.go, target.go, mutation tests
- Fetch origin --prune; confirm develop base is ancestor of candidate; isolate own worktree
- Reproduce the false positive (state-route first write rejected as ghost)
- Apply minimal fix (reuse configGhostRoot route predicate in saveWithPreparation)
- Run focused tests + build + vet + gofmt + readability audit
- Write evidence, commit/pull --rebase only my files, push ancestor-checked draft, run exact-head CI terminal
- Bring down any docker/podman projects (cleanliness witness), post END

## REPRO TEST ADDED

`internal/deployment/config_mutation_test.go`:
- `TestSaveStateRouteFirstWriteNotRejectedAsGhost` (line ~218): `<state>/config.yaml` present, `<state>/config/config.yaml` absent, first `SaveExpected(nil)` must succeed, write lands only in the configured config root, no `.config-*` temp leaked into state or config.
- `TestSaveRouteXDGGhostStillRejected` (line ~255): XDG route `<xdg>/baseharbor/config.yaml` present, nested `config.yaml` absent → `Save` still returns `ErrConfigMissing`.

## CI RUN EXACT-HEAD (§4.6)

Run #6580, run-id `44520608459` (https://github.com/mcpdev80/baseharbor/actions/runs/44520608459) at head `7cc41858b771bb0e2cc4e1d8ffac0f4feadbf4e1`, status **completed / success**; 0 failure/error jobs (native gate, Go unit owners/CLI, Go vet, go build, deployment-package-tests, selected Docker lifecycle gate all green).

| CI job | result |
| --- | --- |
| PR · Native gate plan / Trusted Plan / Workflow policy | success |
| PR · Source format / Runner Interface / Demo Pin / Focused Python | success |
| PR · Go unit · owner / cli-0..3 / packages | success |
| PR · Validation · go-vet / go-build / deployment-package-tests | success |
| PR · Exact Candidate | success |
| Docker lifecycle gate | success |
| Release Source Preflight / Main release / Consumer Pins | skipped (not a release branch) |

## repo-rule compliance

- Write-set limited to `internal/deployment/config_mutation.go` and its test.
- `internal/deployment/target.go` unchanged (mission §3 / AGENTS 4.2).
- No `.github/**` or `scripts/**` edits — none needed.
- No merge, no second branch, no subagent (AGENTS 4.8).
- Evidence lives only in `baseharbor-plan` (no `.evidence/`, no product-repo writes).
- Fixtures/worktrees isolated under `/tmp/opencode/`; ecosystem root untouched.

## CLEANLINESS

- No docker/podman projects started this lane.
- `docker ps -a` pre: n/a (none). post: n/a (none).

---

END lane-0428-110-mutation-loud DONE — 0428-110 r2 XDG ghost-guard route restriction; head 7cc41858b; CI run 44520608459 SUCCESS; evidence on origin/main.
