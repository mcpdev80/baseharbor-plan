# CODEX-REVIEW — PR #1375 consent-abort (round 2, lane w131)

- Candidate: `edd38d316095d3bf3c481060f092ebfbe432d5e8` (w120-fix head after Owner merge, SHA exact)
- Base (post merge): `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1` (`origin/develop`, confirmed with `ls-remote`)
- Branch provenance: `merge-base --is-ancestor 2ea2c6f1 edd38d31` => **develop is an ancestor of w120-fix** (AST verified). w120-fix pushed via fast-forward (no force, no rewrite), verified with `ls-remote`.
- PR: OPEN, DRAFT. Name-only diff `develop..w120-fix`: `cmd/baha/deployment_record.go`, `cmd/baha/w120_consent_abort_repro_test.go`, `cmd/baha/w120_fix_helpers_test.go`. No `.github` or specification files changed.

## Review findings, resolved this round

The r1 verdict (REJECT) named three missing proofs. Round 2 delivers them:

1. **Real destroy-durchlauf — EXECUTED, not resolver-only.** The candidate test `TestW120RefusedApplyWritesNothingLeavesDestroyableState` drives the REAL candidate choke point `recordDeploymentBeforeMutation(... "applying", wrong)` (not `resolveApplication(..., "destroy")`) and asserts the refused apply writes NO deployment state, then re-resolves on the destroy command. The rollback-free invariant (record stays `configured`, no consent, no `previous_intent`) is the exact reported-bug assertion.
2. **Follow-up after approval — EXECUTED.** `TestW120ConsentedApplyPassesChokePointAfterRefusal` runs the wrong digest first (refused, writes nothing) then the canonical digest `confirmDigestForResolved(...)` and asserts a validated `applying` record with consent is written — no manual cleanup in between.
3. **No rollback path, no invalid consent saved — preserved.** The choke point returns before `SaveDeploymentRecord` on digest mismatch; the candidate code diff in `deployment_record.go` remains comments only (the fix's product delta was already in base `ecbb8854`). No rollback semantics introduced; invalid consent never persisted.

## Red-first proof (deterministic)

Against a simulated no-choke-point state (validation block commented out), BOTH tests FAIL with `wrong confirm digest accepted; candidate must fail closed`. On the candidate they PASS. This is a genuine red-first regression: the reported-bug failure mode (partial applying record with dangling runtime owner) is what the assertions catch.

## Mandatory checks

- `go build -buildvcs=false ./...` => clean (exit 0)
- `go vet ./cmd/baha` => clean (exit 0)
- `gofmt -l` on all three changed files => empty (clean)
- `go test ./internal/deployment/... -count=1` => `ok`
- `go test ./cmd/baha -run 'TestW120' -count=1` => `ok` (both tests PASS)
- Full `go test ./cmd/baha -count=1` => **class-B environment blocker (not a code defect).** See STATE below.

## STATE: full-package CI gate blocked by shared-host Docker (class-B, PR #1377)

The full `go test ./cmd/baha -count=1` run fails with a 10m test timeout, NOT from any change in this lane. The exact failing check and log line:

```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (0.49s)
    app_edit_apply_test.go:875: baseline workload-only lifecycle failed:
       application preflight failed: selected Docker endpoint
       unix:///var/run/docker.sock is unavailable; start its rootless daemon
       or correct the Target endpoint/context; no fallback to System Docker
panic: test timed out after 10m0s
```

`TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (`cmd/baha/app_edit_apply_test.go:826`) is a pre-existing test that drives a full native-Docker apply/destroy lifecycle. Its failure is a class-B environment blocker: the shared-host docker daemon at `unix:///var/run/docker.sock` is unavailable/contended on this host. This is the open lever cited in PR #1377. Per the mission this is a class-B environment, not a defect introduced by this lane — the failing line is left verbatim, the test is not rewritten or skipped.

The deterministic, non-runtime portion of the suite that IS in scope for this lane is green:
- `go test ./cmd/baha -run 'TestW120' -count=1` => `ok` (both regression tests pass)
- `go test ./internal/deployment/... -count=1` => `ok`
- `go build -buildvcs=false ./...`, `go vet ./cmd/baha`, `gofmt -l` => clean

## Hosted / CI

No `.github` editing, no reruns, no workflow_dispatch (Owner scope). The full-package CI gate is owned by the Coordinator (f49a3303).

## Review boundary

Candidate diff inspected against `origin/develop` and `origin/w120-fix` via `ls-remote` + `git diff --name-only`. No force-push, no branch protection bypass. No `.github` touched.

END_DONE codex-w131-r2: verdict=ACCEPT-conditions (tests execute choke point + follow-up, red-first verified, build/vet/gofmt/deployment-package/TestW120 green; w120-fix head edd38d31 via fast-forward merge of develop, AST confirmed). Full-package CI gate is a class-B environment blocker (shared-host docker unavailable, PR #1377) — left verbatim, not rewritten/skipped.
