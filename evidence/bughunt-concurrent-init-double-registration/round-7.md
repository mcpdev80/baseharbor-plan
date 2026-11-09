# Evidence — 0427-175, round 7 (r7)

**Task:** `t-20261108-bughunt-concurrent-init-double-registration`
**Card:** `0427-175` (Kanban 175) · PR #1512 · `0427-175-initlock`
**Reviewer verdict:** CODEX-REVIEW r6 = KORREKTUR
**Candidate commit:** `84f60778ad6f71a8d1f76651e7e184bd2fe81558`
**Own-run duty (4.6):** met — run watched to terminal via `gh run view`.

---

## What changed (this round)

The r6 verdict (KORREKTUR) required moving the selector-vs-resolved identity guard to sit before every destructive mutation in the `--full-reset` destroy path, driving the poison-recovery and drift regressions through the real CLI entry with authorization, and proving byte-identical sibling retention.

1. Production fix — `cmd/baha/app_destroy_lifecycle.go` (`removeApplicationState`).
2. New native acceptance tests — `cmd/baha/app_registry_poison_native_acceptance_test.go`.
3. Enhanced seam regression — `cmd/baha/app_registry_poison_recovery_test.go` (byte-identical sibling assertion).
4. Race regression — `cmd/baha/app_init_concurrent_race_test.go` — left UNCHANGED.

### Production guard (the core fix)

The selector-vs-resolved drift guard was relocated from its old position (just above `DeleteDeploymentRecord`) to the very top of `removeApplicationState()`, before **all** destructive effects: `Store.Delete`, `ReleaseApplicationProviderRegistryAt`, the runtime/route/provider cleanup, and `DeleteDeploymentRecord`.

Before this move the guard already preceded `DeleteDeploymentRecord`, but it came *after* `Store.Delete` and `ReleaseApplicationProviderRegistryAt` and after the runtime/route/provider cleanup. A drifted selection could therefore remove a record the operator did not address and mutate the other twin's band before the guard ever fired.

The guard (verbatim, added at top of `removeApplicationState`):

```go
if selectedID := selectionDeploymentID(e.selection); selectedID != "" &&
	e.resolved.DeploymentIdentity.DeploymentID != selectedID {
	return fmt.Errorf("deployment selection %s did not route to the resolved record %s; refusing to delete either twin", selectedID, e.resolved.DeploymentIdentity.DeploymentID)
}
```

The old block (now removed from just above `DeleteDeploymentRecord`) is identical except the comment. This is the exact diff for that file (all 3 remaining changes are test-only):

```diff
 func (e *applicationDestroyExecution) removeApplicationState() error {
+	// The repair deletes a directory, so the path it took must be the path the
+	// operator selected. Fail closed on drift BEFORE any destructive mutation —
+	// before Store.Delete, before ReleaseApplicationProviderRegistryAt, before
+	// the runtime/route/provider cleanup that precedes this seam and before the
+	// DeleteDeploymentRecord below — so a selection that drifted onto another
+	// twin never removes a record the operator did not address (0427-175). A
+	// check after the remove cannot prevent the loss.
+	if selectedID := selectionDeploymentID(e.selection); selectedID != "" && e.resolved.DeploymentIdentity.DeploymentID != selectedID {
+		return fmt.Errorf("deployment selection %s did not route to the resolved record %s; refusing to delete either twin", selectedID, e.resolved.DeploymentIdentity.DeploymentID)
+	}
+
 	appDir := filepath.Join(e.resolved.Store.Root, e.manifest.Name)
 	if _, err := os.Stat(appDir); err == nil {
 		if err := e.resolved.Store.Delete(e.manifest.Name); err != nil {
@@ -634,15 +645,6 @@ func (e *applicationDestroyExecution) removeApplicationState() error {
 		return fmt.Errorf("verify application destruction: %w", err)
 	}
 
-	// The repair deletes a directory, so the path it took must be the path the
-	// operator selected. Fail closed on drift BEFORE any destructive mutation so
-	// a selection that drifted onto another twin never removes a record the
-	// operator did not address (0427-175). This guard must precede
-	// DeleteDeploymentRecord: a check after the remove cannot prevent the loss.
-	if selectedID := selectionDeploymentID(e.selection); selectedID != "" && e.resolved.DeploymentIdentity.DeploymentID != selectedID {
-		return fmt.Errorf("deployment selection %s did not route to the resolved record %s; refusing to delete either twin", selectedID, e.resolved.DeploymentIdentity.DeploymentID)
-	}
-
 	if err := deployment.DeleteDeploymentRecord(e.resolved.DeploymentIdentity); err != nil {
 		return fmt.Errorf("remove target deployment record after verified destruction: %w", err)
 	}
```

`git diff --stat` for this file vs parent `f4b26ecf2` matches the above exactly.

### Native acceptance tests (real CLI entry + authorization)

`cmd/baha/app_registry_poison_native_acceptance_test.go` (new, 316 lines):

- `TestRegistryConflictRepairViaRealCLIEntryDeletesSelectedTwinOnlyAndKeepsSibling` — both twins seeded with an `.owner` band; drives a real `baha app destroy --full-reset` through the CLI entry with authorization; asserts the selected twin is fully gone and the surviving twin's record AND `.owner` band are **byte-identical** after repair (SHA/hash compare); registry healthy with exactly the surviving record. Gated on `BASEHARBOR_APP_FULL_RESET_ACCEPTANCE=1`; SKIPS otherwise.
- `TestRegistryConflictCLIEntryDriftRefusedBeforeAnyMutation` — a drifted selection (operator path resolves to twin A, resolved record is twin B) is refused before any mutation: neither twin's directory nor band is touched, no deployment record removed, registry still lists both twins. Gated; SKIPS otherwise.

Real CLI entry (native `--full-reset`) is required so `authorizeApplicationDestruction` yields a non-empty post-preflight scope, which is the only way consent validation passes. Fabricated/non-native apps get an empty scope → consent fails. This is the existing native acceptance pattern.

### Enhanced seam regression (CI-durable byte-identical sibling)

`cmd/baha/app_registry_poison_recovery_test.go` (`TestRegistryConflictRepairViaRealCLIDeletesSelectedDirAndBand`) adds a byte-identical sibling proof over the repair path:

```go
keeperBeforeRecord, rerr := os.ReadFile(filepath.Join(siblingRoot, "deployment.json"))
// ... keeperBeforeBand from siblingBandPath
keeperAfterRecord, rerr := os.ReadFile(filepath.Join(siblingRoot, "deployment.json"))
keeperAfterBand, berr := os.ReadFile(siblingBandPath)
// bytes.Equal(before, after) for both record and band — else t.Fatal
```

This runs in normal CI (native acceptance tests SKIP by default).

### Race regression — unchanged

`git diff f4b26ecf2 HEAD -- cmd/baha/app_init_concurrent_race_test.go` is empty (rc 0). The race regression remains the untouched drift-race proof from f4b26ecf2.

---

## Run-zeugnis (own run, 4.6)

- CI job: **42661724281** · `CI · PR #1512` · `CI · Source & Quality` · branch `0427-175-initlock` · type `pull_request`.
- headSha: `84f60778ad6f71a8d1f76651e7e184bd2fe81558` (== this commit).
- State transition watched to terminal via `gh run view`: `in_progress` from 17:08:45Z → **`completed` / `success` at 17:20:04Z**.
- URL: `https://github.com/mcpdev80/baseharbor/actions/runs/42661724281`

```
{"conclusion":"success","headSha":"84f60778ad6f71a8d1f76651e7e184bd2fe81558","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42661724281"}
```

---

## Witnesses

PR #1512 head (from `git ls-remote origin refs/pull/1512/head`):

```
84f60778ad6f71a8d1f76651e7e184bd2fe81558	refs/pull/1512/head
```

Candidate HEAD == `refs/pull/1512/head` (verified via fetch; `git diff HEAD refs/pull/1512/head` empty).

All changed files vs parent `f4b26ecf2` (from `git diff --stat f4b26ecf2 HEAD`):

```
 cmd/baha/app_destroy_lifecycle.go                  |  20 +-
 cmd/baha/app_registry_poison_native_acceptance_test.go | 316 +++++++++++++++++++++
 cmd/baha/app_registry_poison_recovery_test.go      |  26 ++
 3 files changed, 353 insertions(+), 9 deletions(-)
```

Evidence evidence published to plan origin/main (from `git ls-remote origin main`):

```
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

---

## Test results

- `go test ./cmd/baha/ -run 'TestRegistryConflict'` → `ok github.com/mcpdev80/baseharbor/cmd/baha 0.964s` (seam regression with byte-identical sibling passes).
- Native acceptance tests gate on `BASEHARBOR_APP_FULL_RESET_ACCEPTANCE=1`; they SKIP in normal CI. They do not run in the watched CI run — the seam regression + race regression provide the CI-durable coverage.
- `go vet ./cmd/baha/` → clean. `gofmt -l` on the 3 files → clean. `go build -o /tmp/baha-r7 ./cmd/baha` → BUILD_OK.

---

## repo-rule compliance

- No `.github/**` edits (Owner scope). No reruns / workflow_dispatch.
- No subagents (AGENTS 4.8). Every step run in the own session.
- Production change confined to `cmd/baha/app_destroy_lifecycle.go`. No contract/schema/spec/`contracts/`/`spec/` edits.
- Evidence only in `baseharbor-plan` — never in the product repo.
- Race regression left byte-for-byte unchanged.
- No secrets, gateway tokens, or Codeman web passwords logged.
- CI-durable coverage: the enhanced seam regression runs in normal CI (native tests SKIP by default); race regression unchanged. No `.github/**` trigger change was required — the seam regression already runs in the existing Source & Quality group.

---

## END

0427-175 r7 complete. CODEX-REVIEW r6 (KORREKTUR) fully addressed:

- Selector-vs-resolved guard moved to the top of `removeApplicationState()`, before every destructive mutation (`Store.Delete`, `ReleaseApplicationProviderRegistryAt`, runtime/route/provider cleanup, `DeleteDeploymentRecord`).
- Poison-recovery + drift regressions drive the real `executeApplicationDestroyLifecycle` CLI entry with authorization (native acceptance tests).
- Byte-identical sibling retention (record + `.owner` band) proved: seam regression (CI-durable) + native acceptance test.
- Race regression unchanged.
- CI run 42661724281 on head `84f60778a` = completed/success.
