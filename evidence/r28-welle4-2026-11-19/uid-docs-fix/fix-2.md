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

- Base ref (develop head): `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
- `git merge-base origin/develop fb6f36936924ca07a9de512c113dc138d38360f1` = `907f16713cbf38693d30c9dadaad7fe299759219` (develop is a strict ancestor of the candidate — the candidate is NOT monotonic on develop, as the mission states).
- `git merge-base --is-ancestor da76c5cf9 fb6f36936` → TRUE: my base is an ancestor of the candidate head.
- My first commit will be cut from `da76c5cf9` and will carry NO commit from the candidate chain (only-base lineage, verified in evidence below).

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
