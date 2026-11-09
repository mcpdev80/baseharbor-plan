# ROUND 180-1 — stale lifecycle-lock holder detection + auto-reclaim

**Card:** 0427-180 impl · **Mission:** `/tmp/opencode/mission-180-impl.md`
**Worker:** worker-ornith1.5 (session 594fd2f5-4e80-43b6-9841-92879146a85e)
**Evidence path (origin/main only):** `evidence/bughunt-flock-enforcement-cells/round-180-1.md`

## PLAN

- Resolve the develop-pin discrepancy and pick the working base; record base SHA + ancestry.
- Set up an isolated worktree under `workers/.w180-impl`; cut branch `0427-180-stale-reclaim`.
- Extend `lock_unix.go` to record holder PID + process start time + boot id in the dotfile (179 probe unchanged).
- Add stale detection + auto-reclaim in the acquire path (per-app + target-wide), without weakening the 179 validity probe.
- Add focused tests: `kill -9` on a real child -> later lifecycle acquire on the same target succeeds after reclaim; 179 probe still enforced; same-scope exclusion still holds.
- Run `go vet`, `go build`, `go test ./...`; bundle one coherent candidate commit.
- Push candidate branch; PR; wire the new test into the CI group covering `internal/stableid`.
- Hosted gate on exact PR head (SOP raw lines); tear down compose; commit evidence to origin/main; post END.

## SCOPE / STATE

- **Branch (named candidate):** `0427-180-stale-reclaim-8a29` (PR #1517 on develop)
- **Base SHA (attested before branch cut):** `8a2912c62869cc89adc35bd6680b18724c5eac8d`
- **179 base commit (unchanged, carried forward):** `13fca4f91`
- **CI group covering new test:** ci.yml `validate` job, step "Run release-source tests" (ci.yml:122 `go test ./contracts/... ./internal/... ./spec/...`) — covers `internal/stableid` as a standard Go test. **No `.github/**` change needed** (Owner directive satisfied). See CI-findings below.

## CI-TRIGGER FINDING (STATE — Owner action required)

- The new test is covered by an existing CI group (above) so no workflow edit is required. **The hosted run itself is blocked by my token scope.**
- `gh auth status` token scopes: `gist`, `read:org`, `repo`. **No `actions:write`.**
- `POST /repos/mcpdev80/baseharbor/actions/workflows/ci.yml/runs` with `{"ref":"0427-180-stale-reclaim-8a29"}` returns **404** (confirmed twice via curl + gh api). `GET .../actions/runs` returns 200, so the token reads Actions but cannot create runs.
- **Finding for Owner:** trigger the `CI · Source & Quality` (ci.yml) run on PR #1517 head `bf1fe2dad` (or mark the PR ready / push). Record the `validate` job run-id + PASS line from `gh run view <id> --json` in the handoff. No CI gate-manifest reuse is allowed (AGENTS CI section); this is a fresh run on an unchanged SHA.

## Base attested + discrepancy resolved

- **Authoritative base = mission pin `8a2912c62`** (`fix(0427-178): truthful owner-failure classification in batched app-list (r3)`), HEAD `8a2912c62869cc89adc35bd6680b18724c5eac8d`, verified via `git ls-remote origin` / `git merge-base` / `git cat-file`.
- Branch cut from exact base, base is ancestor of HEAD (base only, no foreign commit):
  `git merge-base --is-ancestor 8a2912c62 HEAD` => YES.
- 179 probe base (unchanged, carried forward): `13fca4f91` (`fix(stableid): enforce lifecycle flock cross-process via validity probe`, #1515).
- **Discrepancy resolved:** `8a2912c62` is a forward of the current `refs/heads/develop` (`cdb4350a6`) by 4 commits (d9bf3d94e, 13fca4f91, 230221700, 8a2912c62). Current develop dropped the per-app scan lineage; `8a2912c62` retains both the 179 probe (FINDING-1) AND the FINDING-2 scan (`deploymentsHaveAppLocks` / `AcquireTargetWideLifecycleLock` / `AcquireAppLifecycleLock`). The mission's stated base is the correct target and has exactly the code the FINDING describes.

## FINDING-1 (unchanged, carried forward)

- `internal/stableid/lock_unix.go` writes **only** `os.Getpid()` into the lock dotfile (line 81, pre-fix). The 179 validity probe runs before this write and is UNCHANGED by this task.

## FINDING-2 (this task)

- A SIGKILLed holder leaves its dotfile behind (kernel releases flock; the receipt persists); the target-wide scan `deploymentsHaveAppLocks` reports the per-app dotfile as held, so every later lifecycle acquire fails closed with no self-help.
- Fix in the acquire path: write holder PID + process start time + boot-id into the dotfile; on contend, read the receipt, check holder liveness (pid alive + boot-id generation match), and reclaim a confirmed-stale holder atomically under the target-wide scope — no manual intervention.

## REPO-RULE COMPLIANCE

- No `.github/**` edits (Owner scope).
- No subagents (4.8) — every step run in this session.
- Write-set stays on `internal/stableid/lock.go`, `lock_unix.go`, new tests.
- Evidence committed only to `baseharbor-plan` origin/main.

## IMPLEMENTATION (candidate `bf1fe2dad` on `0427-180-stale-reclaim-8a29`)

- `internal/stableid/lock_unix.go`:
  - `lockNamed` now writes an enriched receipt instead of a bare `os.Getpid()` line: `lockHolderRecord{pid, startTime (unix seconds), bootID}.lockHolderBytes()`. The 179 validity probe still runs BEFORE this write and is byte-for-byte unchanged — cross-process enforcement is not weakened. The receipt carries a magic header line so a reader distinguishes a genuine receipt from foreign text / a pre-0427-180 bare-pid line.
  - New: `lockHolderHeader` (`"baseharbor-lock v1 pid="`), `lockHolderRecord` + `lockHolderBytes`, `parseLockHolderRecord` (decodes pid / startTime / bootID; ok=false for foreign or bare-pid receipts), `lockHolderBootID()` (reads `/proc/stat` `boot` field on Linux; empty otherwise), `lockHolderLive` (a holder is LIVE when its pid is alive and, when a boot id is present on both sides, on the current boot; a dead holder (ESRCH) is reclaimable; a live holder still blocks — fail-closed, never reclaims a live process).
  - `lifecycleLockHolderMessage` decodes the pid from the receipt via `parseLockHolderRecord` (the diagnostic still contains `pid=<pid>`, `state=alive`, `ps -p`, `never delete`).
- `internal/stableid/lock.go`:
  - New `reclaimStaleAppLock(deploymentsDir, lockName)`: reads the receipt, decodes it, and removes it ONLY when `lockHolderLive` is false (dead holder). Missing dotfile = nothing to reclaim; unreadable namespace fails closed; foreign/malformed receipt left untouched (never destroy another writer's state on a decode guess).
  - `AcquireAppLifecycleLock`: after taking the shared `.installation.lock` exclusively, reclaims a confirmed-stale per-app dotfile BEFORE creating the new one — atomically under the same critical section the target-wide scan shares. The kernel flock still blocks a live same-scope writer (contention not bypassed); only a confirmed-stale receipt is removed.
- `internal/stableid/lock_holder_unix_test.go`: the pid-receipt test now asserts the pid via `parseLockHolderRecord` (the pre-fix whole-line bare-pid assertion was superseded by the versioned format this task introduces; the diagnostic still exposes `pid=`).
- `internal/stableid/lock_reclaim_unix_test.go` (NEW, `//go:build !windows`): the FINDING-2 regression cells (see below).
- `internal/stableid/two_process_lock_test.go`: merged the reclaim child dispatch into the single package `TestMain`.

## TESTS (proven, local) — `internal/stableid`

```
ok  github.com/mcpdev80/baseharbor/internal/stableid
```
17 cells green, including:
- `TestStaleAppLockReclaimedBySubsequentAcquire` — the FINDING-2 proof: a **real** child process (re-exec) holds the per-app lock, is `kill -9`'d (no cleanup), and a subsequent `AcquireAppLifecycleLock` on the SAME scope/SAME root SUCCEEDS by auto-reclaim — no manual intervention.
- `TestStaleAppLockStillBlocksLiveHolder` — a live holder still blocks; after normal release the next acquire succeeds.
- `TestStaleAppLockLiveBootStillBlocks` — current live process (matching boot id) is live; a dead pid is stale.
- `TestReclaimLeavesForeignReceiptUntouched` — a foreign receipt is never destroyed.
- 179 probe cells (`TestCrossProcessFlockIsEnforced...`, `TestAcquireLifecycleLockFailsClosedOnUnenforcingFilesystem`) still green — probe unchanged.
- `TestLocalAppLifecycleCannotOverlapTargetWideMutation` / `TestAcquireAppLifecycleLockIsPerAppScope` still green — per-app coordination intact.

## LOCAL CHECKS (all green)

- `go build ./...` => exit 0.
- `go vet ./internal/stableid/ ./internal/coreinstallation/ ./internal/deployment/` => clean.
- `go test ./internal/stableid/` => ok (17 cells).
- `go test ./internal/coreinstallation/` => ok.
- `go test ./cmd/baha/ -run 'Lock|Lifecycle|Unenforcing'` => the only failure is `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, which **fails identically on the clean base** (`existing native network lacks a protected Core`) — a native-runtime gate, unrelated to this change.
- `gofmt -l internal/stableid/` => clean (committed a gofmt pass).
- `bash scripts/source-readability-audit.sh` => Go file size / function span / regression ratchet PASS.

## BRANCH / PR PROVENANCE (reality witnesses)

- Product base: `git ls-remote .../refs/heads/develop` = `cdb4350a6` (current develop). Mission pin `8a2912c62` is a 4-commit forward of it and is the correct target.
- Base attested (ancestor of HEAD, base only — no foreign commit): `git merge-base --is-ancestor 8a2912c62 HEAD` => YES; `git log --oneline 8a2912c62..HEAD` lists ONLY my commit(s).
- Candidate branch pushed: `git ls-remote github 0427-180-stale-reclaim-8a29` => `bf1fe2dad16d9aea8901f2383af0a9a0a4aecfc4`.
- PR: **#1517** open on base `develop`, head `0427-180-stale-reclaim-8a29`, non-draft. URL: https://github.com/mcpdev80/baseharbor/pull/1517
- CI trigger blocked by token scope (gist/read:org/repo; no actions:write) — see CI-findings; **Owner must trigger the CI validate run.**

## END STATUS

State: **BLOCKED** — implementation, tests, PR (#1517) and CI-coverage wiring are complete and local checks are green; the only open step is the hosted CI run, which requires an Owner token with `actions:write` (my token 404s on the Actions create endpoint). Hosted run-id + PASS line to be recorded from the Owner's CI trigger, then evidence committed to origin/main and END re-posted as DONE.
