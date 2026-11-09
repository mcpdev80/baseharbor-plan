# 0427-175 round 1 — concurrent `baha app init` double-registration: implementation candidate

Mission: `/tmp/opencode/mission-175-impl.md`. Lane: `lane-w175-initlock` (worker-flash).
Candidate: branch `0427-175-initlock`, single commit `f32f3557614` (verified ancestry:
`git merge-base --is-ancestor b3a8042d1 HEAD` → OK; `git log b3a8042d1..HEAD --oneline` shows
only this commit). Base develop pin `b3a8042d18ea60f162a32a51df34a499cad6a237`
(remote develop has since moved to `942111d5a`; the diff touch-set below is against the pinned base).
PR: https://github.com/mcpdev80/baseharbor/pull/1512 (draft→ready per workflow; no `.github/**` files changed).

## PLAN

- Read mission, contract, hp4 BF-01/BF-10 evidence; verify remote state
- Design the write-seam serialization (registry lock) and the read-seam conflict report
- Implement lock primitive + first-registration atomic claim/scan/create
- Implement foreign-claim rename guard and structured RegistryConflictError
- Implement planning-surface classification and the --uuid repair door
- Regression tests: in-process race, two-OS-process race, recovery face, detector
- Full-suite parity vs develop baseline; race runs; format/vet/readability audits
- Commit, ancestry-proof, push, PR, watch hosted CI to terminal state

## What was broken

Two `baha app init` processes racing in the check-then-create window of
`SaveDeploymentRecord` could each pass the (name-keyed) duplicate scan and persist a second
deployment record for ONE `application_id`. The pair poisoned the Target: every
provider-consumer inventory read (`ListDeployments` fan-out in plan/up/destroy of EVERY app)
failed closed with a generic "inventory damaged" text, both twins were unreachable by NAME
(ambiguity guard) and the advertised healings (`app prune`, plain destroy) did not work on
this shape (hp4 BF-10; lesson 162).

## The fix (candidate f32f3557614)

Write seam (`internal/deployment`):
- `registry_lock.go` — `WithDeploymentRegistryWriteLock` + `DeploymentClaimExists`. Non-blocking
  `stableid.AcquireRegistryLock` on `.registry.lock` inside the Target state root. The lock root is
  NEVER created by this path (`MkdirAll` side effects broke loan/discovery tests on develop; the
  lock is taken only when the root already exists, and the seam is entered only for FIRST
  registrations, so the lock graph of running lifecycle commands is byte-identical to before).
- `SaveDeploymentRecord` split: first registration runs claim → duplicate scans → create under the
  registry lock (one atomic claim); idempotent re-saves keep the old lock-free path (0427-149).
- `refuseDuplicateApplicationIDGuard` (new) + existing name guard (0427-149) both run inside the
  lock: racer → `ErrDuplicateApplicationID` naming the winner, or `ErrRegistryConcurrentWrite`
  wrapping the flock refusal (`IsRegistryConcurrentWriter` classifier).
- `refuseForeignDeploymentClaim` at the final rename: a `deployment.json` belonging to a DIFFERENT
  uuid is never replaced; pid-suffixed temp file so a killed racer leaves at most a stale temp.

Read seam:
- `ListDeployments` (the single inventory seam every planning path shares) now reports an existing
  poison as `RegistryConflictError` (sentinel `ErrRegistryConflict`) naming BOTH colliding uuids and
  the repair text. `ListDeploymentsForDisplay` (what `app list` uses) stays tolerant — the operator
  must be able to SEE the twins to destroy them.

CLI/MCP surfaces (`cmd/baha`):
- `invalidProviderConsumerInventory` renders the conflict with `CauseCode
  provider_consumer_inventory_invalid`, Message + Next = the VERIFIED repair
  `baha app destroy --uuid <id> --full-reset` for each twin (no reference to `app prune` — #1505 is
  unmerged and it refuses twins because their source is present).
- `refuseRegistryApplicationIDConflict` gate in `resolveApplicationEnvironment`: poisoned-registry
  commands without `--uuid` fail closed before routing at an arbitrary twin; skipped when `--uuid`
  is present so the repair path never self-blocks.
- `--uuid`/`-e` option pairs no longer count toward the one-NAME limit (the MCP arg shape
  `name + ["--uuid", id]` was rejected as "at most one NAME"); `app <cmd> --uuid <id>` with no NAME
  now resolves through the registry seam.

## Tests (all pure-Go; CI carrier: the "Go unit & quality" job of ci.yml, which runs
## `go test ./cmd/baha ./internal/...` on every PR — no new trigger needed, no test added in
## `.github/**` scope)

- `internal/deployment/registry_poison_test.go`: write-seam refusal names the winner and writes
  nothing; same-identity re-save stays idempotent; poison listing yields the structured conflict
  through `ListDeployments` AND `FindDeployment`; display listing tolerates it; detector is
  order-independent (sorted ids, env-scoped, empty app ids never collide); message parsers
  (`IsRegistryConflict`/`RegistryConflictIDs`/`RegistryConflictKey`) round-trip through wraps.
- `cmd/baha/app_init_concurrent_race_test.go`: 8-way goroutine race (exactly one record persists)
  and a REAL two-OS-process race via test-binary re-exec with the critical section parked through
  `TestHookAfterRegistryClaimEnter` (child exits 3 on fail-closed refusal; the registry count is
  the authority).
- `cmd/baha/app_registry_poison_recovery_test.go`: planning path on a poisoned Target yields the
  machine error with both uuids + working repair verbatim; `--uuid` reaches a twin (or names the
  structured conflict); NAME refuses and names both twins.
- `internal/deployment/target_test.go` (existing cell adapted): `findDeploymentMatches` ambiguity
  proof seeds by direct write since the write seam itself now refuses.

## Runs and results

- `go build ./...`, `go vet` (changed packages), `gofmt -l` → clean.
- `go test ./internal/deployment ./internal/stableid -count=1` → ok; `-race` → ok (no data race).
- `go test -race ./cmd/baha -run TestConcurrentInit` → ok.
- `go test ./cmd/baha -count=1` full package → failure set EXACTLY equals the develop baseline at
  `b3a8042d1` (14 pre-existing failures: the `TestQuickInit*/TestGuidedInit*/TestDeterministicInit*`
  corrupt-home-state family + `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`). Verified
  twice plus a parallel develop-worktree baseline diff (`comm`/`diff` empty both directions).
- `go test ./cmd/baha ./internal/... -count=1` → 9 identical failures both trees (native
  postgres/controlplane cells, environmental).
- `bash scripts/source-readability-audit.sh` → all PASS (store file split into
  `registry_conflict.go` to stay under the 800-line ceiling; no shared-script edits).
- `bash scripts/documentation-audit.sh` → all PASS.

## repo-rule compliance

- plan → preflight → apply → verify separation untouched; no runtime/capability/delivery mixing.
- No `.github/**` change; no subagents used (§4.6, the test-binary re-exec is the harness's own
  pattern from `internal/stableid/two_process_lock_test.go`, not a subagent); targeted-only
  `git add`; evidence here only.
- Ancestry proven against the pinned base; single candidate branch/PR per §3.8.
- Secret protection: no credentials in this evidence; tests use temp XDG roots.
- Recovery text verified against the BUILT binary behavior (lesson 162), not assumed from docs.

## Stop/open items for the review

- Hosted CI outcome for `f32f3557614` is appended to this note when the run reaches terminal state
  (Eigenes-Run observation §4.6; monitor running in the lane).
- Native Docker/Podman cells are not required: every new/changed behavior is pure-Go storage/CLI
  logic and is covered by the Go unit job.
