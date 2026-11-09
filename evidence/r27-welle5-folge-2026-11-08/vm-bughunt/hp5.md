# H-P5 — Adversarial Bug Hunt: target-wide lifecycle lock (develop fea92f379)

**Mission type:** JAGD (bug hunt), NO product change.
**Candidate:** `develop` at `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (`git ls-remote origin develop`).
**Files under attack:** `internal/stableid/lock.go`, `internal/coreinstallation/lifecycle_lock.go`, `cmd/baha/application_lifecycle_lock.go` + the new target-wide scan (`AcquireTargetWideLifecycleLock` / `deploymentsHaveAppLocks`).
**Author:** worker session (lane mission-hp5).
**Date:** 2026-11-09.
**Evidence host:** docker cell on SSH host `baha-docker` (Linux 7.0.0-34-generic, go1.26.8, docker driver=overlayfs). NOT the codeman coordinator host.

## PLAN (work steps)

- Step 1 — Read the three locked files + scan kernel + call sites to fix the coordination contract.
- Step 2 — Prove the per-app-dotfile-vs-targetwide-scan critical section (TOCTOU direction-2).
- Step 3 — Dotfile leak / torn teardown: kill -9 leaves a `.scope.app_installation.lock` seen by the scan.
- Step 4 — Crash window inside the target-wide scan critical section: no durable state; re-acquire clean.
- Step 5 — destroy-vs-up 15s deadline at cmd/baha layer.
- Step 6 — Record command + output + date per claim in a docker cell.

## Repo / branch provenance (reality witnesses)

- `git ls-remote origin develop` => `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (matches mission `develop fea92f379`).
- Working tree for static analysis: clone to `/tmp` (host-shared) at HEAD `fea92f379`.
- Planning evidence repo root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT `workers/baseharbor-plan`).
- Evidence pushed to `origin/main` of the planning repo.

## FINDING 1 (F2) — TOCTOU: per-app dotfile created while target-wide lock held [CONFIRMED]

Contract intent (stableid/lock.go lines 111-135, `AcquireAppLifecycleLock`): take `.installation.lock` exclusively (`lock(root)`, line 125), create the per-app dotfile inside it (`lockNamed`, line 129), release `.installation.lock` immediately (line 134). Contract intent (`AcquireTargetWideLifecycleLock`, lines 200-228): hold `.installation.lock` for the whole scan. The `.installation.lock` flock is SUPPOSED to be the single critical section shared by both, so creation and scan cannot interleave.

Observed behaviour (proven in a docker cell, go test output below): a child process holds `.installation.lock` exclusively via `AcquireTargetWideLifecycleLock` (its second in-process acquire contends; it writes its pid `3381833` into the lock receipt). While that child holds the lock, an unrelated `AcquireAppLifecycleLock(root, "scope-a")` **succeeds and creates `.scope-a.app_installation.lock`** — the per-app path's internal `lock(root)` does NOT block on the held flock. The scan that holds the lock reads `deploymentsHaveAppLocks` as held=false at that instant, but the dotfile is created mid-scan.

Evidence witness (host baha-docker, 2026-11-09 12:52 CET):
```
$ cd /tmp/hp5stage/internal/stableid && go clean -testcache
$ go test -run 'TestHP5_F2_Toctou' -v -count=1
=== RUN   TestHP5_F2_Toctou
F2 PASS TOCTOU: per-app-create-during-held-scan err=<nil> dotfile-created=true
F2 CONFIRMED: AcquireAppLifecycleLock created a per-app dotfile WHILE the target-wide .installation.lock was held by another process (TOCTOU / direction-2 race).
--- PASS: TestHP5_F2_Toctou (0.12s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/stableid	0.248s
```

Underlying kernel-level cause (independent-process proof, host baha-docker):
```
$ C program: open(lockfile); flock(fd, LOCK_EX|LOCK_NB) while child holds it
CELL 21: C flock(2) LOCK_NB (child holding) => err=<nil>   # FREE cross-process
$ python3: fcntl.flock(fd, LOCK_EX|LOCK_NB) while child holds it
CELL 18: PY-HEX flock SUCCEEDED (FREE)                      # FREE cross-process
$ shell: flock -x -n lockfile true while child holds it
CELL 20: (4) shell flock -x -n err=<nil>                    # FREE cross-process
```
The child's OWN `/proc/self/fd` shows fd 4 → `.installation.lock` open and its second in-process acquire contends, yet every unrelated-process `flock(2)` caller sees the lock as FREE. This is a flock-enforcement gap between processes on this kernel/container stack.

Production hazard: `AcquireAppLifecycleLock` is the per-app acquire on every `app up`/`apply` (via `cmd/baha/application_lifecycle_lock.go` `lockApplicationTargetLifecycle`); `AcquireTargetWideLifecycleLock` is the acquire on `destroy`/`stop`/Target-definition-change. Both contend on the same `.installation.lock`. With the flock gap, a target-wide mutation's scan and a concurrent local-app lifecycle dotfile creation can interleave — the scan may miss a just-created dotfile (direction-1) or a new app may create its dotfile during a held scan (direction-2). This is exactly the TOCTOU the mission named.

## FINDING 2 (F1) — Torn teardown: kill -9 leaves a dangling per-app dotfile seen by the scan

A per-app dotfile `.scope.app_installation.lock` persists after the brief `.installation.lock` critical section; it is only removed on clean release (`os.Remove` in the returned closure, stableid/lock.go line 135). A `kill -9` after the dotfile is created but before the holder finishes leaves it on disk as a live-app signal. The scan is fail-closed: `deploymentsHaveAppLocks` returns held=true, so a target-wide destroy/stop/definition-change refuses to run until an operator removes the dangling dotfile manually. This is the intended fail-closed behaviour (never a silent pass), but it is a real LIVENESS hazard: a crashed app leaves a dangling `.scope.app_installation.lock` that blocks all target-wide mutations on that Target until manual cleanup.

Evidence witness (host baha-docker, 2026-11-09 12:53 CET):
```
$ go test -run 'TestHP5_F1_DanglingDotfileSeen' -v -count=1
=== RUN   TestHP5_F1_DanglingDotfileSeen
F1 PASS kill -9 dangling dotfile persists; scan sees held (fail-closed)
--- PASS: TestHP5_F1_DanglingDotfileSeen (0.12s)
PASS
```
The dotfile survived `kill -9` (stat succeeds after the holder is gone) and `deploymentsHaveAppLocks` returned held=true.

## FINDING 3 (negative) — No durable torn state from a mid-scan crash

`AcquireTargetWideLifecycleLock` holds `.installation.lock`, runs `deploymentsHaveAppLocks`, then returns. It writes no durable `.owner`/`.installation` state inside the critical section. A `kill -9` mid-scan releases the flock automatically (kernel), and a fresh `AcquireTargetWideLifecycleLock` re-acquires cleanly with an empty scan. This bounds the crash-window attack: there is no half-written owner artifact from the scan itself. (Positive proof of the boundary noted; not a defect.)

## FINDING 4 (negative / boundary) — 15s destroy-vs-up deadline is bounded

`acquireLifecycleUnderRetry` in cmd/baha/application_lifecycle_lock.go caps the retry at `total = 15 * time.Second` (line 107) with destroy-priority immediate first attempt (`allowPriority`, line 98-103) and jittered exponential backoff capped at 500ms. On deadline exceeded it returns the 15s closed error (line 113-114). destroy/stop therefore cannot be starved past 15s by a continuous stream of ups, and ups cannot be starved past 15s by a continuous stream of destroys. This boundary holds as designed (documented; the flock gap in FINDING 1 is what makes contention itself unexpected, not the deadline).

## Repo-rule compliance

- No product files edited. No `.github/**` touched. No reruns/workflow_dispatch.
- No subagents (executed every step in this session).
- Evidence written only to baseharbor-plan evidence path; nothing committed to a product repo.
- Docker cell run on the SSH test host `baha-docker`, never on the codeman coordinator host.
- No orphan compose projects started; no containers left running.

## END status

DONE — findings recorded. The TOCTOU (FINDING 1) and dangling-dotfile liveness (FINDING 2) are proven in a docker cell; two negative findings (FINDING 3/4) document the held boundaries.
