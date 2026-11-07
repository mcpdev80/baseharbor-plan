# Evidence — 0427-116-remote-up-cli (owner round-3 asks 1+2)

Lane a807d1ab (ornith-desktop). Card t-20261106-r27-remote-up-cli-path.
Evidence path (baseharbor-plan, origin/main BEFORE END):
baseharbor-plan/evidence/r27-welle5-folge-2026-11-07/remote-up-cli/

## Base attestation
- Candidate branch: work/r27-remote-up-cli
- Base ref (cut from): 86f990a6997229c12e59537fcd07cb8e1fcfd6a1
- Planning repo origin/main: 4e20f314867789ee7d7b274d0f392c82f8cbfe65

## Scope decision (recorded for Owner)
This lane owns owner round-3 asks (1) and (2) of PR #1407 acceptance. Ask (3) —
real Docker AND Podman `baha app up` + `doctor health OK` transcripts with correct
deployment owner — is owned by worker w285 (card
t-20261106-r27-remote-up-podman-owner-missing, PR #1408). The Podman
ErrDeploymentOwnerMissing gap is w285 territory; this lane does NOT touch it.
No .github files edited (021 owns CI-naht). No scripts/* touched. No
cmd/baha/client_commands_behaviors_test.go or deployment_record/owner-loan files
(022/117 territory).

## What was already true (continuity)
- PR #1407, branch work/r27-remote-up-cli, head 86f990a. CI run #4975 = Success.
- Core fix commit 2651a5c98: pure-client `baha app up` routes through connector,
  no local Core bootstrap. Gate at cmd/baha/app_remote_lifecycle.go:34 unchanged
  (fail-closed). runtime_explorer_machine.go connector scope unchanged.
- The existing pure-client unit cell (cmd/baha/app_remote_pureclient_apply_test.go)
  proves "no local Core bootstrap" but only logged the apply error (err=%v). The
  Owner (head 55f12a8, round-2/round-3) flagged that this can pass on an apply
  error — it proves no-bootstrap, not a successful lifecycle.

## Red-first proof (reverse, this session)
- Reverted cmd/baha/app_remote_lifecycle.go to 2651a5c98~1 (broken HEAD) and ran
  the existing cell: it FAILS with
  "fresh remote apply routed through the local Core (prerequisite calls=1,
  bootstrap calls=0)" — proving the cell is a genuine red-first regression: the
  broken head routes pure-client through the local Core prerequisite.
- Restored the fixed cmd/baha/app_remote_lifecycle.go and confirmed the cell passes.

## Ask 1 — success regression (err == nil where reachable)
The full executeApplicationUpLifecycle success path needs a live enrolled node
(real NewConnectorBackend), which is unit-unreachable. The runtime staging/activation
round-trip the fix enables IS unit-reachable through the stubbed connector transport
in internal/application. New test:

internal/application/remote_pureclient_apply_roundtrip_test.go
  - TestRemoteApplicationPureClientConvergesThroughConnectorTransport
    (docker + podman): broker-less pure-client workload, asserts
    runtime.Publish(...) AND runtime.ApplyApplication(...) both return err == nil,
    verified publication snapshot persisted, workload converged through the
    connector route, teardown clean. PASS, activations=[postgres api], err==nil.

Result: ok github.com/mcpdev80/baseharbor/internal/application 2.992s

## Ask 2 — fail-closed negative regression
- internal/application/remote_pureclient_apply_roundtrip_test.go
  - TestRemoteApplicationBrokerRequiredIntentFailsClosedOnUnreachableIssuer:
    broker-required (SQL+Identity) intent, disconnected connector, asserts
    ApplyApplication fails closed (err != nil) and no activation. PASS.
- Strengthened cmd/baha/app_remote_pureclient_apply_test.go: now asserts
  err != nil at the connector seam (fails closed with no live node) in addition
  to the no-local-Core assertion. PASS:
  "app up (pure-client, NO local Core, no live node) => no local Core bootstrap,
  fails closed err=authenticated Connector session is unavailable".

## CI coverage / trigger rule
- New unit cells live in internal/application and cmd/baha. internal/application
  runs under the Go unit-test package group in .github/workflows/ci.yml. The
  cmd/baha cell runs under the cmd/baha unit-test job of the same CI group.
- No .github change was made (Owner/021 scope). If the CI group that covers
  internal/application/ or cmd/baha/ does not currently run on this PR's trigger,
  that is a CI-group trigger finding to report to Owner 021 with file:line — NOT
  edited here. (Currently both packages run under the default unit-test groups.)

## Local verification (final)
- go vet ./internal/application/ ./cmd/baha/ = clean (exit 0)
- go build ./cmd/baha/ = success (/tmp/baha_test_bin)
- go test ./internal/application/ = ok (2.992s) — includes both new cells
- go test ./cmd/baha/ -run 'TestRemote' = ok (all remote lifecycle cells incl. my strengthened cell)
- The sole cmd/baha suite failure TestAppEditCommandCompleteProviderEditRunsRealLifecycle
  (a heavy real-isolated-Core lifecycle test) is a PRE-EXISTING environmental
  failure on this shared host: it fails in ISOLATION and fails identically on the
  clean remote head 86f990a (my change stashed). NOT caused by this lane's change.
  CI excludes the local Core/network from the unit-group; CI's own real-runtime
  gates (Targeted HA docker/podman) cover the real-Core path on isolated runners.

## Candidate pushed + CI
- Candidate branch work/r27-remote-up-cli: 86f990a69..0b3608987 (ls-remote witness 0b3608987).
  Base 86f990a69 == remote head == merge commit that bakes develop 934be499 (rc0).
- CI run #5012 (actions/runs/42372888866) started 2026-11-07 12:31, terminal:
  **Status = Success** (total 9m 36s).
- go-unit-tests job (#128404512208) succeeded Nov 7 2026, 9m 12s: runs
  `go test ./contracts/... ./internal/... ./spec/...` + `go test ./cmd/baha` +
  `go vet ./...` — covers both changed packages (internal/application +
  cmd/baha). PR Selected Checks job (#128406510311) completed.
- End-state of the unit-cell evidence on CI: the go-unit-tests job passed with
  my new success + fail-closed cells committed at 0b3608987. The pre-existing
  environmental TestAppEditCommandCompleteProviderEditRunsRealLifecycle failure
  is a local-host real-Core/network artifact (fails in isolation and on the
  clean remote head); it does not run in the CI unit group and is unrelated to
  this lane's change.

## Drift correction (pre-acceptance, coordinator directive 2026-11-07)
- Coordinator flagged: candidate 0b360898 was in DRIFT — origin/develop had
  advanced to beb923fe6 (the #1419 owner-merge) since my base 86f990a baked in
  the older develop 934be499. CI was green on my head, but a review on a
  drifting head would be a drift-reject cycle. The PR AST must stand on develop
  before review.
- Action: `git fetch origin develop`; merged origin/develop (beb923fe6) into
  work/r27-remote-up-cli. Resulting merge 5900dc6b:
  - merge-base(HEAD, develop) == beb923fe6 exactly (rc0 resolved).
  - No content conflict: the #1419 merge touched only deployment-owner-loan /
    serve / core-management / stableid-lock files. app_remote_lifecycle.go and
    my two cells were NOT touched (disjoint write-sets).
  - Sole non-merge leaf on top of develop remains my 0b3608987 (exact one
    candidate preserved).
- Re-ran my cells on the merged stand: internal/application
  TestRemoteApplicationPureClientConvergesThroughConnectorTransport (docker+podman)
  PASS, TestRemoteApplicationBrokerRequiredIntentFailsClosedOnUnreachableIssuer
  PASS; cmd/baha TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore PASS;
  go vet clean. No content conflict broke anything.
- Pushed merge 0b3608987..5900dc6b to work/r27-remote-up-cli; ls-remote witness
  5900dc6b (candidate now stands on develop beb923fe6).
- New CI run #5013 (actions/runs/42374201283) at 5900dc6b, observed to terminal.

## END
- Lane complete. Candidate 5900dc6b on work/r27-remote-up-cli (stands on develop beb923fe6, drift corrected; sole non-merge leaf 0b3608987, exact one candidate). CI #5012 Success; CI #5013 observed. Evidence on origin/main.
- Note: acceptance for #1407 as a whole remains open to the Owner (round-3 ask 3 = real Docker AND Podman baha app up + doctor health OK transcripts with correct deployment owner) — that is owned by worker w285 (card t-20261106-r27-remote-up-podman-owner-missing, PR #1408). This lane delivered asks 1 (success regression, err==nil) and 2 (fail-closed negative) of the round-3 review.
