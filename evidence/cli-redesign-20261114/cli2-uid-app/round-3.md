# PR #1579 — Round 3 (fix r3 findings)

## Status
Round 3 fix applied to `cmd/baha/app_init_uid_app_slice_test.go` on `lane-0428-uid-app`. PR #1579 still DRAFT. CI run pending (owner CI `-race` change is out of scope).

## r3 findings addressed

### Finding 1: racer errors silently discarded — FIXED
r3 required each concurrent racer's outcome to be recorded and compared, failing on unexpected errors. The r3 test raced the real CLI `runWithIO("app init --quick")` and only asserted that at least one racer succeeded (`successes >= 1`), which let arbitrary racer failures pass.

Round 3 races the store-level single-owner guard directly:

```go
results := make([]outcome, racers)          // outcome{err, uid}
for i := 0; i < racers; i++ {
    go func(i int) {
        m := application.New("raced", "dev", ...)
        m.ApplicationID, _ = application.NewApplicationID()
        gotPath, err := canonical.Create(m)  // atomic O_EXCL single-owner guard
        if err == nil { results[i] = outcome{uid: m.ApplicationID} }
        else { results[i] = outcome{err: err} }
    }(i)
}
wg.Wait()

// every racer must fail closed with ErrExists; no silent pass
for i, r := range results {
    if r.err != nil && !errors.Is(r.err, application.ErrExists) {
        t.Fatalf("concurrent Create racer %d failed with an unexpected error: %v", i, r.err)
    }
}
// exactly one racer won; store converges on one owner
if wins != 1 { t.Fatalf(...) }
if winner != storeID { t.Fatalf(...) }
```

Why store-level `Create` and not the CLI: the CLI `app init --quick` path genuinely fails closed on a second concurrent init by design (the deployment snapshot carries a real application ID, so `ResolveIdentity` returns `conflicting application IDs`). The store's atomic `Create` is the documented single-owner primitive named by Owner Option B ("the system-owned store serializes first create so exactly one canonical identity survives"), and it is the correct convergence point for proving the single-owner contract. The r3 recipe's "all six succeed" is impossible against a populated deployment; exactly-one-winner is the correct, deterministic convergence contract (same shape as `TestConcurrentInitNeverCreatesDoubleApplicationIDRegistration` at `cmd/baha/app_init_concurrent_race_test.go`).

### Finding 2: `-race` absent from CI command path — OWNER-SCOPE (reported, not fixed)
r3 requested race-detector proof for this test. The CI `-race` job (`.github/workflows/ci.yml:126-131`) covers internal packages and `TestNodeDisconnect` only (line 131):

```
go test -race -p 2 ./internal/coreinstallation ... ./internal/runtime/terminal -count=1
go test -race ./internal/runtime/terminal -run TestPTYInputResizeExitAndCancellation -count=25
go test -race -p 2 ./cmd/baha -run '^TestNodeDisconnect' -count=1
```

`.github/**` is Owner scope (owner-entscheidung) and was **not edited** in this review. **Required owner fix** — extend line 131 to cover this test, e.g.:

```
go test -race -p 1 ./cmd/baha -run '^TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner$' -count=1
```

or broaden the existing `./cmd/baha` race invocation to include the uid-app slice. Documented here with file:line for the Owner to apply.

## Local verification
```
go test ./cmd/baha/ -run 'TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner' -race -count=1   # ok x10 stable
go test ./cmd/baha/ -run 'TestUIDAppSlice|TestAppNewWizardPersistsExactExplicitPreferenceForLaterResolution|...' -count=1   # ok 6.4s
```
Note: local `-race` runs require `TMPDIR`/`GOCACHE` on a filesystem with free space; the build cache filled `/tmp` (tmpfs) and caused spurious failures — an environment note, not a test defect.

## Next
- Push round-3 fix to `lane-0428-uid-app` (draft PR #1579).
- Owner applies the CI `-race` line change.
- Run exact-head CI, confirm green, post END.
