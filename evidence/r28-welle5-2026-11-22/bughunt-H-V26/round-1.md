# Bug-hunt H-V26: candidate-registry lock desk on develop (0428-192)

- bug-hunt H-V26, sitz f0f6c8b4. REINE BEFUNDUNG, KEINE aenderung/commit/push/subagent. READ-ONLY desk on the 0428-192 "registry has no lock" bereich.
- develop HEAD recorded: named target 62784eff7befadfaa8a08fc21eaffbd4e3cc8962 (present in this checkout), CURRENT origin/develop advanced to cdca12b6e87940d50dc1652ee47d01cd0b85c7e1. The named and current HEAD are IDENTICAL for registry_lock.go, registry_conflict.go, deployment_store.go (git diff empty). Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote.
- Method: read-only git show/grep/rg on develop (named 62784eff + current cdca12b6e). No git write. No containers/volumes/state. No product/.github/scripts change.

## PLAN

1. Establish reality (remote guard, develop HEAD). No git write.
2. Desk A (deployment registry, internal/deployment): read registry_lock.go + registry_conflict.go + SaveDeploymentRecord. Trace the production write path (deployment_record.go 520-542 chokepoint -> SaveDeploymentRecord -> registry lock). Positive: parallel first-registry serialization. Negative: TOCTOU between fingerprint and record; double-record.
3. Desk B (candidate store + lock): find candidate submission path (internal/delivery/candidate.go, app_candidate_consent.go, deployment_record.go 500-545) and confirm it writes through the same registry-locked store; check for any direct deployment.json write that bypasses the lock.
4. Verify the named develop 62784eff specifically carries the lock (not just a later SHA).
5. Classify each finding: ECHTER DEFECT / doku-luecke / kein-befund. File:line + rezept.
6. Write akte + Fundbilanz + cleanliness. No product change, no PR, no comment, no subagent.

## Befunde

### Desk A — deployment registry (internal/deployment)

**FUND 1: kein-befund — the deployment-registry write lock exists and covers first registration at the production write seam.**

- file:line `internal/deployment/registry_lock.go:1-46` defines `registryLockFile = ".registry.lock"` and `WithDeploymentRegistryWriteLock(target, fn)`. It takes `stableid.AcquireRegistryLock(root, registryLockFile)` with `LOCK_EX|LOCK_NB` (kernel flock, holder PID inside, auto-release on exit) and refuses `ErrRegistryConcurrentWrite` (another registration in progress) — never queues or silently retries.
- `internal/deployment/deployment_store.go:374-416` `SaveDeploymentRecord`: `DeploymentClaimExists` probe + `if claimed { return saveDeploymentRecord(record) }` (idempotent re-save, no lock) else `WithDeploymentRegistryWriteLock(...)` (first registration takes the lock around the whole save). Comment cites 0427-175 / hp4 BF-01: concurrent double registration is structurally impossible, not merely unlikely.
- Positive case (parallel writes serialized): two concurrent first registrations of a NEW deployment uuid. The second `SaveDeploymentRecord` takes `WithDeploymentRegistryWriteLock`; `AcquireRegistryLock` returns flock contention -> `ErrRegistryConcurrentWrite`. Two real processes: one succeeds, the other fails closed (not queued, not a double-record). Guarded by `internal/stableid/lock_cross_process_test.go:23` (TestCrossProcessFlockIsEnforcedProvesMutualExclusion) and `two_process_lock_test.go:70`.
- Negative case (TOCTOU / double-record): the fingerprint->record window is INSIDE the lock. `saveDeploymentRecord` runs `refuseDuplicateApplicationName` + `refuseDuplicateApplicationIDGuard` (both (application_id, environment) uniqueness) inside the locked region, then `persistDeploymentRecord` (deployment_store.go:582-623): `refuseForeignDeploymentClaim` (identity check before rename) + atomic temp-write + `os.Rename` (atomic replace) + retained ownership band. A process killed between temp-write and rename leaves at most a stale temp file, never a torn/clobbered record. No TOCTOU window between claim and create.
- Production callers all route through the same lock: `cmd/baha/app.go:151`, `app_remote_lifecycle.go:203/214`, `application_remote_reactivation_record.go:33`, `application_runtime_retirement_record.go:81/140`, `deployment_record.go:581/660/699`.

### Desk B — candidate submission path (internal/delivery/candidate.go, cmd/baha)

**FUND 2: kein-befund — the candidate apply chokepoint writes through the SAME registry-locked store; no direct deployment.json write bypasses the lock.**

- file:line `cmd/baha/deployment_record.go:500-545` `record.Source.Kind == "repository" && state == "applying"`: the deployment source IS the exact candidate identity. `finalizeCandidateConsent(rawCandidateConsent, "operator", submission)` (app_candidate_consent.go) pins the content-hash digest; a stale/absent digest fails closed BEFORE any record is written. Then the record is persisted via `SaveDeploymentRecord` (the registry-locked store).
- `internal/delivery/candidate.go:179-227` `Validate(consent)` enforces fail-closed candidate contract (consent required, content-pinned, exactly one immutable identity) before submission — the same contract the chokepoint validates against.
- The candidate itself is ephemeral (a consent-bound submission + digest), NOT a persistent store. Its durable effect is the deployment record, which is written ONLY by `persistDeploymentRecord` (`internal/deployment/deployment_store.go:573`, "the only place a deploy directory's record is persisted").
- No bypass: grep for `deployment.json` writers returns only `persistDeploymentRecord` (deployment_store.go:582) — no direct `os.WriteFile`/`os.Rename` of the record elsewhere in product code.

### Desk A/B — named develop 62784eff specifically

**FUND 3: kein-befund — the lock exists at the named develop 62784eff** (not just the current HEAD). `git show 62784eff:internal/deployment/registry_lock.go` contains `WithDeploymentRegistryWriteLock`/`registryLockFile` (5 hits); `registry_conflict.go` present; `deployment_store.go:SaveDeploymentRecord` present. `git diff 62784eff...cdca12b6 -- internal/deployment/{registry_lock.go,registry_conflict.go,deployment_store.go}` is EMPTY (no changes between named and current develop for these files).

## Fundbilanz

- echte defekte: 0. The 0428-192 "registry has no lock" gap is already closed on develop: the deployment-registry write lock (`.registry.lock`, flock LOCK_EX|LOCK_NB, PID-inside, auto-release) serializes first registration; the candidate apply chokepoint writes through the same locked store; no direct deployment.json write bypasses the lock. No TOCTOU window between fingerprint and record; no double-record path.
- doku-luecke: 0.
- kein-befund: 3 (FUND 1 lock present + serialized; FUND 2 candidate chokepoint through locked store; FUND 3 lock present at named develop 62784eff).

## cleanliness

- READ-ONLY. No product code, no test code, no .github, no scripts changed. No commit/push/merge/comment, no subagent, no PR.
- No git write beyond reading refs (checked out via the existing lane-0428-242-catalog-guardian branch at origin/develop; no commits created; no push).
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE — findings only, no change.
develop HEAD: named 62784eff7befadfaa8a08fc21eaffbd4e3cc8962 (current origin/develop cdca12b6e identical for these files).
Fundbilanz: 0 real defects / 0 docs / 3 no-befund.
Je fund: FUND1 deployment registry lock internal/deployment/registry_lock.go:1-46 + deployment_store.go:374 (serialize first registration; TOCTOU/double-record closed by lock-included scan+create+atomic-rename); FUND2 candidate chokepoint cmd/baha/deployment_record.go:520-542 -> SaveDeploymentRecord (same locked store; no bypass); FUND3 lock present at named develop 62784eff.
No product/test/.github change, no PR, no comment, no subagent.
