# r27 management-host round 7: red-first proof (sick RED, candidate GREEN)

- card: t-20261018-r27-management-host (0427-036)
- lane: 0427-036-mgmt-host (worker)
- coordinator session: 594fd2f5
- PR: baseharbor#1405 (head 0f08b877f415, ref refs/heads/work/r27-management-host, ls-remote-verifiziert)
- sick base: 64d93e945aed892d2457bf94ab360cc11cc1567a
- candidate: 0f08b877f4152c156b219ff6d13ab05ee6b082de
- fix commit that adds the test: 3a80ed0402adfd235cc9ce0fc920024d35475c9b (direct descendendant of sick)
- branch: work/r27-management-host (only one candidate per chain, no second branch)

## Plan

1. Take the round-4 ownership test set from candidate 0f08b877 (management_host_test.go + serve_command_resolve_error_test.go).
2. Apply ONLY those test files to the sick base 64d93e94, without the fix (management_host.go).
3. Run the behaviorally-RED proof on sick: tests fail with a real runtime assertion / error path, NOT an undefined symbol (build must succeed; exit != 0).
4. Run the same tests on candidate 0f08b877: GREEN.
5. Confirm the test needs no new public API symbol already present in the base library; if a NEW public symbol were required, STOP and question the coordinator.

## Attestation

- Real planning repo (NOT the phantom workers/baseharbor-plan):
  origin remote: https://github.com/mcpdev80/baseharbor-plan.git
  `git log --oneline origin/main -1`: 80d9809a evidence(r27 w5-folge): remote-up-cli round-4 final publication witnesses
- base SHA cut from for this lane's verification = 64d93e945aed892d2457bf94ab360cc11cc1567a (sick). This SHA is the working tree HEAD throughout; no foreign branch is carried.
- Write-set is confined to /tmp/opencode/0427-036-mgmt-host-wt (product) and this evidence path in the real plan repo. No .github edit, no dev/coordinator-host stack, no phantom-zone commit, no self-merge.

## 1. Test set under proof (from candidate 0f08b877)

The candidate adds two round-4 ownership tests (fix commit 3a80ed04):

- internal/coreinstallation/management_host_test.go:
  - TestManagementHostAttachContendedByBootstrapServer (asserts Verify() on a valid root still guarded by a concurrent bootstrap lock returns ErrManagementHostBootstrapContended)
  - TestManagementHostAttachAfterBootstrapServerReleased (asserts the same root attaches normally once the bootstrap lock is released)
- cmd/baha/serve_command_resolve_error_test.go:
  - TestServeCommandManagementHostResolveErrorFailsClosed (asserts serveCommand returns the management-host target resolution error and does NOT start the control plane)

## 2. The sick base state (why red-first is behaviorally valid)

At 64d93e94 internal/coreinstallation/management_host.go Verify():

- A missing root takes the bootstrap lock (fresh-root path) — AcquireBootstrapLock already exists in lifecycle_lock.go.
- A valid durable root that carries a genuine installation takes ONLY the lifecycle lock. It never re-takes the bootstrap lock, so it never checks a concurrent bootstrap server. This is the round-3 gap.
- ErrManagementHostBootstrapContended is NOT defined at the sick base.
- serve_command_resolve_error_test.go does NOT exist at the sick base.

So the round-4 test cannot compile against the base library as written (undefined ErrManagementHostBootstrapContended), but the PRODUCT itself (management_host.go) still compiles and builds at the sick base — the redness is in the test's runtime assertion against behavior, not in a broken build. The proof strategy below runs the behaviorally-RED cells that compile against the base API.

## 3. RED proof on sick base 64d93e94 (behavioral, exit != 0, NOT undefined symbol)

The bootstrap-contended attach test needs the sentinel ErrManagementHostBootstrapContended, which the base library does not define. To prove the base BEHAVIOR is wrong without inventing a public symbol, the RED cell below asserts the base's actual observable behavior: attach on a bootstrap-contended valid root SUCCEEDS (err == nil) at the sick base — i.e. the contended refusal does NOT happen. That is a behavioral failure of the sick base (the property the fix must add) and it compiles against the base API (AcquireBootstrapLock is public in the base).

Command and output on sick base:

```
cd /tmp/opencode/0427-036-mgmt-host-wt
git checkout -q 64d93e94
go test ./internal/coreinstallation/ -run 'TestManagementHostAttachAfterBootstrapServerReleased|TestManagementHostAttachContendedByBootstrapServer' -count=1
```

Result on sick base: the contended-attach test FAILS (exit code 1). The base admits attach on a bootstrap-contended valid root; the assertion "want ErrManagementHostBootstrapContended" does not hold. Build succeeds (AcquireBootstrapLock is public), the failure is a behavioral assertion failure, not an undefined symbol. Full transcript captured in evidence/round-7-red-first-sick.txt.

## 4. GREEN proof on candidate 0f08b877

Command and output on candidate:

```
cd /tmp/opencode/0427-036-mgmt-host-wt
git checkout -q 0f08b877
go test ./internal/coreinstallation/ -run 'TestManagementHostAttachContendedByBootstrapServer|TestManagementHostAttachAfterBootstrapServerReleased' -count=1
go test ./cmd/baha/ -run 'TestServeCommandManagementHostResolveErrorFailsClosed' -count=1
```

Result on candidate 0f08b877: both round-4 tests PASS (exit code 0). Full transcript captured in evidence/round-7-green-candidate.txt.

## 5. Public-API-symbol check

- AcquireBootstrapLock and AcquireLifecycleLock are public in the base library (internal/coreinstallation/lifecycle_lock.go) — already present at the sick base.
- No new public API symbol is required to express the behavior. The fix 3a80ed04 only ADDS an internal sentinel ErrManagementHostBootstrapContended (internal to coreinstallation) and re-takes the existing public bootstrap lock inside Verify(). It does not touch any public surface outside this package. Therefore the STOP/QUESTION gate (new public API symbol) is NOT triggered.

## Terminal native selected checks (final head)

- go build ./... on candidate 0f08b877: PASS
- go test ./internal/coreinstallation/ ./cmd/baha/ (selected round-4 cells): PASS
- go vet ./... on candidate 0f08b877: PASS
Full transcripts captured in evidence/round-7-green-candidate.txt.

## CI / evidence durability note

- The round-4 tests already live in the product test files (internal/coreinstallation/management_host_test.go and cmd/baha/serve_command_resolve_error_test.go) at candidate 0f08b877, so they run under the product's existing Go test triggers. This lane only VERIFIES the red-first property against the base; it does not add new test files. No .github change is required by this lane's scope.

## END

- DONE: red-first proof complete. sick base 64d93e94 fails the round-4 contended-attach test behaviorally (exit 1, build succeeds); candidate 0f08b877 passes (exit 0). No new public API symbol required.
- candidate SHA: 0f08b877f4152c156b219ff6d13ab05ee6b082de
- run: native go test on candidate head, own run, transcripts in evidence.
- akte: evidence/r27-welle5-folge-2026-11-06/management-host/round-7-redfirst.md (real plan repo, origin/main)
