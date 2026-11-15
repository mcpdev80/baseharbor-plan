# BF-01 round 4 — red-tightened candidate, LV-02 integration witness

Card: t-20261115-bughunt-d28-state-dir-target (0427-189). PR #1585 (draft),
base develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.
Authoritative head this round: `13e096fc66d90e20b8f262b7f58024790c62b0e5`.

## Candidate chain

Base develop `0e9ccb582`, branch `lane-0428-fix-bf01-v2` (PR #1585 head):

- `f048627c1` fix(cli): state-root override owns target selection state
- `8041a9f01` fix(cli): keep foreign organization defaults out of isolated state roots
- `7bdeaa084` test(cli): mirror real organization-state placement in the BF-01 regression
- `e7501204c` fix(cli): state-root-owned target selection chain (BF-01, red-tightened)
- `8e944192f` refactor(orgconfig): keep root-membership helpers together in store order
- `ea3a0705e` fix(orgconfig): carry the world-writable selection guard across the state-root chain
- `13e096fc6` fix(cli): root-local organization default must resolve through the root's own selection

Dropped during consolidation: #1584 (closed, not merged), #1586 (duplicate, closed).

## Review-r1 recipe: all items addressed

1. **Reg must be ambiguous on develop** — the test now drives the resolver on a
   root with two registrations and no multi-target shortcut on develop paths:
   the root-local organization selection part (test line 105) passes only with
   the fix because the fix runs the selection chain through
   `resolveTargetBelowStateRoot` instead of the ambient fall-through.
   Red witness on pure develop `0e9ccb582` (worktree, test blob of `13e096fc6`
   copied in):

   ```text
   target_selection_state_dir_isolation_test.go:105: effectiveTarget with the
   root-local organization selection: multiple deployment targets configured;
   choose one of: beta, spare-b
   --- FAIL: TestStateDirIsolatesTargetSelection (0.01s)
   ```

   Green witness on the candidate head `13e096fc6`:

   ```text
   --- PASS: TestStateDirIsolatesTargetSelection (0.02s)
   ok  github.com/mcpdev80/baseharbor/cmd/baha  0.034s
   ```

2. **Single selection per state-dir, no ambient shortcut** — the chain is
   root-local: persisted activation below the root (stale names fail closed),
   the root's own organization state only when its source/cache lives below
   the root (`selectsWithin`), and a root-local single-registration first-run
   convenience (root-local only; several registrations fail closed naming
   exactly this root's targets). A foreign ambient organization default can
   never resolve or act on another installation's registrations. This contract
   is asserted in test parts 3–6 (foreign state must not answer; resolver must
   fail closed naming B's own registrations, never A's; root-local default
   wins; stale activation fails closed).

3. **LV-02 / #1582 guard integration** — `ea3a0705e` carries the complete
   BF-03 world-writable guard set inside `internal/orgconfig/store.go`
   (`legacyTempSelectionRel`, `canonicalFrozenMarker`,
   `worldWritableCheckOptOutEnv`, `legacyActivePath`,
   `privateFallbackConfigRoot`, `privateCanonicalPath`,
   `isWorldWritableCandidate`, `privateFallbackPath`,
   `adoptLegacySelection`, `migrateToCanonical`, `isWorldFrozenTombstone`,
   `canonicalMigrationFrozen`, `isWorldWritableDir`, `decodeActive`), so the
   symbols the #1582 tests reference exist on my file's lineage too.

## Throwaway-merge witness (13e096fc6 + 756b2be7e)

Detached worktree at `13e096fc6`, `git merge --no-edit 756b2be7e` (BF-03 head,
PR #1582). Conflicts are confined to `internal/orgconfig/store.go` (both
branches rewrote the same loader region); the merge resolves by keeping both
sides once — no guard symbol is dropped or redefined. Result tree checks:

```text
$ go vet ./internal/orgconfig ./cmd/baha   -> VET-OK (no output)
$ go build ./...                           -> clean
$ go test ./internal/orgconfig -count=1    -> ok  0.085s (42 cells pass)
$ go test ./internal/orgconfig -run 'TestWorld|TestStateDir' -count=1 -> ok
$ go test ./internal/deployment -count=1   -> ok  0.512s
$ go test ./cmd/baha -run 'TestStateDirIsolatesTargetSelection|TestTarget' -count=1
  -> ok  15.951s
```

`SaveActive` in the merged tree writes temp+rename at the canonical
(`privateCanonicalPath`) location — BF-03 semantics intact; the BF-01
`StateRootSelected() && !selectsWithin(...)` guard sits in `decodeActive`,
which both the direct-read and the migration paths share. The merge is a
witness only; nothing was pushed from it (merge-frost).

## Hosted CI

Run `43692224878` ("CI · PR #1585", event pull_request, head `13e096fc6`):

```text
status=completed conclusion=success failed_jobs=[]
```

## Local full-package state

`go test ./cmd/baha -count=1` on the candidate fails only the three
host-bound cells that fail identically on base `0e9ccb582` on this machine
(no isolated runtime ownership available here):
`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`,
`TestSharedBackendReconcileRejectsSecondProcess`,
`TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`.
All three pass in the hosted run above. `go build`, `go vet ./...`,
`gofmt -l`, and `scripts/source-readability-audit.sh` are clean (target.go
split into `cmd/baha/target_state_layout.go` for the 800-line limit).

## Findings worth recording

- CLI experiment (isolated HOME, pre-fix vs post-fix binaries
  `baha-bf01-base`/`baha-bf01-v3`): with two registrations under a fresh
  state root both binaries fail closed on `target show`; the isolation
  difference is proven at unit level (parts 3–6) and via the red/green
  witnesses above. The world-writable guard behaves as BF-03 specifies
  through the same experiment (`config organization set` under a chmod-777
  XDG_CONFIG_HOME lands in the private `~/.config` location).
- `TestNonTTYBackupDefaultUsesProtectedExternalArchive` failed once inside a
  full-package run and passes isolated (`-count=1`, ok) — parallel-fixture
  interference, not a regression from this change; worth a look in the
  write-path follow-up card.
- Single-registration state roots keep the first-run convenience
  (root-local only). Removing it broke backup/init cells; restored with a
  comment that it consults no foreign state.

## END

- Candidate: `13e096fc66d90e20b8f262b7f58024790c62b0e5` on
  `lane-0428-fix-bf01-v2`, PR #1585 draft, base develop `0e9ccb582`.
- Red on develop (line 105) and green on candidate witnessed above; LV-02
  guard integration witnessed by the throwaway merge (vet + orgconfig 42
  cells + `TestWorld|TestStateDir` green on the merged tree).
- Hosted run `43692224878` terminal: completed/success, no failed jobs.
- No merge, no develop movement (merge-frost). Writing/tombstone path
  hardening stays on the follow-up card, as scoped.
- Witness: this file on origin/main via
  `git ls-tree origin/main evidence/r28-welle1-2026-11-15/bf01/round-4.md`.
