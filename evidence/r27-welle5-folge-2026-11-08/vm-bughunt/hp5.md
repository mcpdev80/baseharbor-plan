# H-P5 — Adversarial Bug Hunt: target-wide lifecycle lock (develop fea92f379)

**Mission type:** JAGD (bug hunt), NO product change.
**Candidate:** `develop` at `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`
**Files under attack:** `internal/stableid/lock.go`, `internal/coreinstallation/lifecycle_lock.go`, `cmd/baha/application_lifecycle_lock.go` + the new target-wide scan section (`AcquireTargetWideLifecycleLock` / `deploymentsHaveAppLocks`).
**Author:** worker session (this lane).
**Date:** 2026-11-09.

## Repo / branch provenance (reality witnesses)

- `git ls-remote origin develop` => `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (matches the mission's `develop fea92f379`).
- Working tree for analysis: `git clone` to `/tmp/mission-hp5-repo`, checked out `origin/develop`, HEAD `fea92f379`.
- Planning evidence repo root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT `workers/baseharbor-plan`).
- Evidence will be pushed to `origin/main` of the planning repo.

## PLAN (work steps)

- Step 1 — Read all three locked files + the scan kernel + call sites to fix the coordination contract precisely.
- Step 2 — Verify the per-app-dotfile-vs-targetwide-scan critical section: does `.installation.lock` really cover both dotfile creation and the scan (no TOCTOU)? Test with a two-process docker cell.
- Step 3 — Dotfile-leak / torn teardown: does a crash mid-`AcquireAppLifecycleLock` (kill -9 between `wideUnlock()` release and dotfile persist, and after dotfile but before holder release) leave a `.scope.app_installation.lock` that a later target-wide scan would mis-read as a live app?
- Step 4 — Crash window inside a critical section: kill -9 while `.installation.lock` is held by the target-wide scan; confirm no half-written `.owner`/`.installation` artifacts and that a re-run re-acquires cleanly.
- Step 5 — destroy-vs-up starvation past the 15s deadline: confirm the bounded retry with destroy-priority actually returns the 15s closed error and does not let up starve or destroy be starved.
- Step 6 — Record every finding: command + output + date per claim, in a docker cell (vm-slice), NOT in test isolation. If a boundary holds, record positive proof. END.

## Findings

### Scenario A: TOCTOU between target-wide scan and per-app dotfile creation

Contract (lock.go `AcquireAppLifecycleLock`): take `.installation.lock` (via `lock(root)`), create the per-app dotfile via `lockNamed(deploymentsDir, lockName)`, then release `.installation.lock` immediately. Contract (`AcquireTargetWideLifecycleLock`): hold `.installation.lock`, call `deploymentsHaveAppLocks(root)`, fail closed if held. The `.installation.lock` flock is the single critical section shared by both, so creation and scan cannot interleave. This is the intended F3 design.

Observation to prove in a docker cell: a process holding `.installation.lock` (simulating the target-wide scan) makes a competing `AcquireAppLifecycleLock` block/fail on the flock — i.e. no app can create its dotfile during a held scan, and conversely the scan sees any dotfile already persisted by an earlier app.

Result: <to be filled after docker cell run>

### Scenario B: dotfile leak / torn teardown (crash between create and release)

The per-app dotfile `.scope.app_installation.lock` persists after the brief `.installation.lock` critical section; it is only removed on clean release (`os.Remove` in the returned closure). A `kill -9` after the dotfile is created but before the holder finishes its app mutation leaves the dotfile on disk as a "live app" signal. The scan is fail-closed: a target-wide mutation would then refuse to run until the holder releases or the file is manually removed. This is the intended fail-closed behaviour (never a silent pass), NOT a correctness bug — but it IS a liveness hazard: a crashed app leaves a dangling `.scope.app_installation.lock` that blocks all target-wide destroy/stop/definition-change until an operator removes it manually.

To be confirmed by docker cell: after `kill -9` of a holder that has persisted the dotfile, the dotfile remains and `deploymentsHaveAppLocks` returns true.

Result: <to be filled after docker cell run>

### Scenario C: crash window inside the target-wide scan critical section

`AcquireTargetWideLifecycleLock` holds `.installation.lock`, reads the deployments dir, then returns. A `kill -9` mid-scan releases the flock (kernel) automatically; no `.owner`/`.installation` state file is written inside this function, so a re-run re-acquires cleanly. No torn-artifact bug here.

Result: <to be filled after docker cell run>

### Scenario D: destroy-vs-up past the 15s deadline

`acquireLifecycleUnderRetry` in `cmd/baha/application_lifecycle_lock.go`: `total = 15 * time.Second`, exponential backoff capped at 500ms with jitter, `allowPriority` (destroy/stop) takes one immediate try. On deadline exceeded it returns the 15s closed error. destroy-priority is honoured (immediate first attempt). Up/apply wait for first attempt.

Result: <to be filled after docker cell run>

## Conclusion

<to be filled>
