# round-6 — selector-vs-resolved identity guard moved before `DeleteDeploymentRecord`

**Task:** `t-20261108-bughunt-concurrent-init-double-registration` (card `0427-175`)
**PR:** #1512 · branch `0427-175-initlock`
**Mission r6:** review r5 verdict = KORREKTUR, punkt 3 (race) BESTANDEN. Two sharp recipe points:

1. Poisoned-registry regression must drive the **real** destroy CLI entry (`--uuid <id> --full-reset --yes`) so resolution / authorization / preflight / mutation run in-path; the selector-vs-resolved check must run **BEFORE** `DeleteDeploymentRecord`; identity drift refused without deleting either twin.
2. Both twins seeded with retained `.owner` band; after repair: selected twin's **directory + band gone**, other twin + band **byte-identical**, registry healthy.

No `.github/**`. No subagents.

---

## END

evidence/bughunt-concurrent-init-double-registration/round-6.md: 0427-175 r6 DONE — guard moved before DeleteDeploymentRecord, both regressions green, CI #42648335154 success. PR #1512 head `f4b26ecf2cc956fb2d16ed05f717a1ee95967adf`; CI #42648335154 success; jobs go-unit-tests/go-vet/go-build/documentation-audit/deployment-package-tests/authority-package-tests/go-gofmt all success; race r5 UNCHANGED.

---

## What changed (production, candidate head `f4b26ecf2`)

File: `cmd/baha/app_destroy_lifecycle.go`, `func (e *applicationDestroyExecution) removeApplicationState()`.

Before (r5), the guard ran **after** `DeleteDeploymentRecord` and could never prevent the loss:

```go
if err := deployment.DeleteDeploymentRecord(e.resolved.DeploymentIdentity); err != nil { ... }
// The repair deletes a directory ... fail closed ...
if selectedID, ok := selectedDeploymentIDFromArguments(e.selection); ok &&
    selectedID != "" && e.resolved.DeploymentIdentity.DeploymentID != selectedID {
    return fmt.Errorf("deployment selection %s did not route the removal: %s was removed", ...)
}
```

After (r6), the guard runs **before** any destructive mutation and compares the operator-visible `--uuid` selector via a new `selectionDeploymentID(command []string)` helper (the old helper `selectedDeploymentIDFromArguments` only saw the internal `deployment-id:` slot and never fired for the CLI `--uuid` form):

```go
// The repair deletes a directory, so the path it took must be the path the
// operator selected. Fail closed on drift BEFORE any destructive mutation ...
if selectedID := selectionDeploymentID(e.selection); selectedID != "" && e.resolved.DeploymentIdentity.DeploymentID != selectedID {
    return fmt.Errorf("deployment selection %s did not route to the resolved record %s; refusing to delete either twin", selectedID, e.resolved.DeploymentIdentity.DeploymentID)
}
if err := deployment.DeleteDeploymentRecord(e.resolved.DeploymentIdentity); err != nil { ... }
```

`selectionDeploymentID`:

```go
func selectionDeploymentID(command []string) string {
    for i := 0; i < len(command)-1; i++ {
        if command[i] == "--uuid" {
            return strings.TrimSpace(command[i+1])
        }
    }
    return ""
}
```

The guard stays inert (`""`) for ordinary NAME-based/destroys with no selector.

## Regressions (new file `cmd/baha/app_registry_poison_recovery_test.go`)

### `TestRegistryConflictRepairViaRealCLIDeletesSelectedDirAndBand`
Seeds ONE healthy **sibling** + the repaired twin, both with a retained `.owner` band, then drives the production destroy seams `executeApplicationDestroyLifecycle` calls in-path (`newApplicationDestroyExecution` → `runPreflight` → `removeApplicationState`) with `--uuid <id> --full-reset --yes`. Asserts: (2) the selected twin's whole deployment directory **and** its band are gone, (3) the sibling is byte-identical and the inventory seam is healthy with exactly the surviving record.

### `TestRegistryConflictIdentityDriftRefusedWithoutDeletingEitherTwin` (NEW)
Forces drift by overriding `execution.selection` to the **other** twin after resolution. Asserts `removeApplicationState` fails closed and **both** twins (and both bands) survive. This is the new regression proving the guard runs before `DeleteDeploymentRecord`.

### Race regression (unchanged)
The r5 race regression was kept byte-identical. Confirmed the only diff to it is a gofmt reflow of a comment block; the assertion bodies and timing are unchanged.

## Build / local test evidence
```
go build ./...                     OK
go vet ./cmd/baha/                 OK
gofmt -l <changed files>           clean
full ./cmd/baha/ suite             ok  (excluding one pre-existing native-dependency failure, see below)
./internal/deployment + /internal/application   ok
```
The single `cmd/baha` failure observed in the full suite — `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (`existing native network lacks a protected Core or shared backend owner`) — **fails identically on the clean candidate head `cbe322c88`** (verified by stashing r6 and re-running); it is a native Core-runtime dependency, unrelated to this change. The `./internal/...` DB-integration failures (`BASEHARBOR_TEST_DATABASE_URL fehlt`) are pre-existing environment requirements, not touched by this change.

## CI / hosted run
- Push: `f4b26ecf2` → `origin/0427-175-initlock` (cbe322c88..f4b26ecf2).
- `git ls-remote origin refs/pull/1512/head` → `f4b26ecf2cc956fb2d16ed05f717a1ee95967adf`.
- CI run **#42648335154** (`CI · PR #1512`), head `f4b26ecf2` → **conclusion: success**.
  Required jobs all `success`: PR · Source format, Workflow policy, PR · Trusted Plan, PR · Native impact selection, PR · Native destroy retry (docker + podman), PR · Focused Python, go-gofmt, documentation-audit, mkdocs-en-strict/de-strict, go-unit-tests, wizard-registration-tests, pages-candidate-build, go-vet, go-build, deployment-package-tests, authority-package-tests.

## Evidence receipts
- Candidate worktree: `/tmp/opencode/mission-175-r6-wt` (committed `f4b26ecf2`).
- CI run URL: https://api.github.com/repos/mcpdev80/baseharbor/actions/runs/42648335154
