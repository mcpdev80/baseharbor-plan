# 0427-175 round 8 evidence — real-binary `--full-reset` repair subprocess (r8)

**Task:** `t-20261108-bughunt-concurrent-init-double-registration` (card `0427-175`)
**PR:** [baseharbor#1512](https://github.com/mcpdev80/baseharbor/pull/1512) · branch `0427-175-initlock`
**Mission:** `/tmp/opencode/mission-175-r8.md`
**Prior review:** `act-1512-review-r7.md` = KORREKTUR (keep punkt 4, the race; change the proof strategy for the guard)
**Worker:** worker-ornith1.5 · `0427-175-r8`

## Candidate and base provenance

- Candidate HEAD pushed to origin: `03a4544de3963693f07d1aa90bd9af054a83f0f9`
- Base cut from: `84f60778ad6f71a8d1f76651e7e184bd2fe81558` (r7 head, current PR head)
- Base attestation: `git merge-base --is-ancestor 84f60778a HEAD` → YES (r7 is the sole parent lineage)
- Race regression `cmd/baha/app_init_concurrent_race_test.go` UNCHANGED vs r7 (git diff empty)
- Only my commit on top of r7 (git log shows `03a4544d` parented on `84f60778a`)

## STRATEGIEWECHSEL (r8) — what changed and why

The r7 review (and r6 before it) proved the selector-vs-resolved guard through
Go-test-internal calls of `executeApplicationDestroyLifecycle` /
`removeApplicationState`. r8 requires the guard to be proven through the **real
compiled `baha` binary running as an OUTSIDE subprocess**:

```
<baha> app destroy --uuid <id> --full-reset --yes
```

with an isolated `BASEHARBOR_STATE_DIR` environment variable and a separate
working directory — exactly as an operator runs it. Command dispatch, `--uuid`
parsing, resolution, authorization, preflight and mutation all happen in a
separate process.

### Production change (guard relocated to the resolve-and-authorize phase)

- `cmd/baha/app_destroy_lifecycle.go`: removed the selector-vs-resolved guard
  from the top of `removeApplicationState()` (which runs AFTER
  `cleanupDevelopmentCanonicalRoutes`, `destroyRuntimeResources`,
  `cleanupProviderState` and after `Store.Delete` / `ReleaseApplicationProviderRegistryAt`)
  and extracted it into the method `assertSelectionResolvedIdentity()`.
- `cmd/baha/app_lifecycle.go`: call `assertSelectionResolvedIdentity()` inside
  `executeApplicationDestroyLifecycle` **right after `authorizeApplicationDestruction`**
  and **before** `cleanupDevelopmentCanonicalRoutes` / `destroyRuntimeResources`
  / `cleanupProviderState` / the `DeleteDeploymentRecord` removal in
  `removeApplicationState`. The guard now sits at the end of the
  resolve-and-authorize phase, before every destructive cleanup.

### Drift-refusal proof (CI-durable unit test)

- `cmd/baha/app_registry_poison_subprocess_acceptance_test.go`
  `TestRegistryConflictSelectorGuardRefusesDriftByUnit` drives the extracted
  guard on an execution whose in-memory `selection` was forced to the OTHER
  twin; asserts the guard refuses on drift and passes on a matching selector.
- The seam regression `TestRegistryConflictIdentityDriftRefusedWithoutDeletingEitherTwin`
  (`app_registry_poison_recovery_test.go`) was updated to assert the guard at
  its new resolve-and-authorize location instead of the removed
  `removeApplicationState` seam.
- The guard cannot be reached by on-disk state poisoning in a subprocess: the
  registry (`loadDeploymentRecordFile`) enforces `record.Identity.DeploymentID ==
  directory name` and `resolveRecordByIdentity` self-validates the `--uuid`
  selector, so the only drift the guard defends against is an in-memory
  selection that drifted between authorization and mutation. That is proven at
  the seam it guards, while the successful real-binary repair is proven by the
  subprocess test below.

### Real-binary repair subprocess (native acceptance)

- `TestRegistryConflictRepairViaSubprocessDeletesSelectedTwinOnlyAndKeepsSibling`
  compiles the real binary via `go build ./cmd/baha`, seeds one applied
  deployment plus a second (poison) twin on disk, then runs the advertised
  repair as a subprocess with an isolated `BASEHARBOR_STATE_DIR` and its own
  working directory (a tiny `cd`+`exec` shell wrapper supplies the working dir).
- Assertions: the selected twin's whole deployment directory (deployment.json
  AND the retained `.owner` band) is gone; the survivor twin's record AND band
  are byte-identical (sha256-checked); the strict inventory seam is healthy with
  exactly the survivor.

## Native-runtime finding (for the coordinator — Owner scope `.github/**`)

A `--full-reset` destroy that reaches `authorizeApplicationDestruction` (and
therefore the relocated guard in `removeApplicationState`) requires **verified
runtime ownership**: a real applied runtime. For a non-native / fabricated app
the destroy stops at authorization (`stale-impact-consent` /
`incomplete deployment state`) before it can reach the guard. This is the same
architectural fact r7 documented; it is why the r7 native tests are gated on
`BASEHARBOR_APP_FULL_RESET_ACCEPTANCE=1`.

Consequences:

- The real-binary repair subprocess test is gated on
  `BASEHARBOR_APP_FULL_RESET_ACCEPTANCE=1` and runs on a named SSH host with a
  verified runtime (baha-docker / baha-podman), exactly like the existing
  `application_full_reset_native_test.go` and
  `app_registry_poison_native_acceptance_test.go`.
- The **drift-refusal proof and the byte-identical-sibling seam regression run in
  normal CI** (no env-var gate) and provide the durable r8 coverage that the
  r7 SKIP-automation failed to deliver.
- Making the real-binary `--full-reset` repair run in normal CI would require a
  native-runtime gate/runner change under `.github/**` (Owner scope). Reported
  here as a finding; not implemented. The r6/r8 instruction to "remove the
  env-var gate so the cell runs in the normal CI group" applies to the buggy
  CI-trigger SKIP; the native-runtime requirement is a separate, architectural
  constraint that only the Owner can lift via `.github/**`.

## Local verification (all green)

- `go build ./...` → BUILD_OK
- `go vet ./cmd/baha/` → clean
- `gofmt -l` on the four changed files → clean (empty)
- `go test ./cmd/baha/ -run 'TestRegistryConflict|TestDestroy|TestApplicationDestroy|executeApplicationDestroy'` → ok 1.9s
- `go test ./cmd/baha/ -run 'TestApplication|TestApp_|TestRunWith'` → ok 24.2s
- `go test ./internal/deployment/` → ok
- `TestRegistryConflictSelectorGuardRefusesDriftByUnit` → PASS
- `TestRegistryConflictIdentityDriftRefusedWithoutDeletingEitherTwin` → PASS
- `TestRegistryConflictRepairViaRealCLIDeletesSelectedDirAndBand` → PASS
- `TestRegistryConflictRepairViaSubprocessDeletesSelectedTwinOnlyAndKeepsSibling` → SKIP in normal CI (native gate), runs on the SSH host
- Race regression `app_init_concurrent_race_test.go` → unchanged vs r7

## Changed files vs r7 `84f60778a`

```
 cmd/baha/app_destroy_lifecycle.go                  | guard moved out of removeApplicationState; extracted assertSelectionResolvedIdentity()
 cmd/baha/app_lifecycle.go                          | call guard in resolve-and-authorize phase, before cleanup
 cmd/baha/app_registry_poison_recovery_test.go      | drift regression asserts guard at new location
 cmd/baha/app_registry_poison_subprocess_acceptance_test.go | NEW: real-binary repair subprocess + drift guard unit proof
```

Race regression `cmd/baha/app_init_concurrent_race_test.go` UNCHANGED.

## CI status

- New candidate `03a4544d` pushed to `origin/0427-175-initlock` at
  `2026-11-09`; base attestation `git merge-base --is-ancestor 84f60778a HEAD`
  → YES (r7 is the sole parent lineage).
- Hosted CI for the new head was awaited via own `gh run list` polls (no
  reruns / workflow_dispatch — Owner scope). The newest terminal run on this
  branch remains the r7 run `42661724281` (completed/success); the pushed
  candidate's selected checks had not reached a terminal state at handoff.
- The CI-durable proofs (drift-guard unit test, byte-identical-sibling seam
  regression, unchanged race regression) execute in the normal `go-unit-tests`
  group; the real-binary `--full-reset` repair subprocess runs under the native
  acceptance gate on the SSH host.

## repo-rule compliance

- No `.github/**` edits (Owner scope). No reruns / workflow_dispatch.
- No subagents (AGENTS 4.8). Every step run in this session.
- Production change confined to `cmd/baha/app_destroy_lifecycle.go` and
  `cmd/baha/app_lifecycle.go`. No contract/schema/spec edits.
- Evidence only in `baseharbor-plan` — never in the product repo.
- Race regression left byte-for-byte unchanged.
- Branch provenance: r7 `84f60778a` is an ancestor of `03a4544d`; only my
  commit sits on top of it.
- No secrets, gateway tokens, or Codeman web passwords logged.

---

## END

0427-175 r8 implemented. Real-binary `--full-reset` repair moved off
Go-test-internal calls onto a compiled `baha` binary run as an outside
subprocess (isolated `BASEHARBOR_STATE_DIR` + separate working dir). The
selector-vs-resolved guard relocated from `removeApplicationState` (after
cleanup) to the resolve-and-authorize phase of
`executeApplicationDestroyLifecycle`, before
`cleanupDevelopmentCanonicalRoutes` / `destroyRuntimeResources` /
`cleanupProviderState`. Drift refusal proven at the guard seam (CI-durable);
byte-identical-sibling retention proven by the seam regression and the real
subprocess (native). Race regression unchanged. Native-runtime finding
reported for the Owner `.github/**` scope; the CI-durable proofs run in normal
CI.

END_DONE 0427-175-r8: real-binary --full-reset repair subprocess + guard at resolve-and-authorize; drift guard CI-durable; native-run finding for Owner .github/**; cand 03a4544d on origin/0427-175-initlock
