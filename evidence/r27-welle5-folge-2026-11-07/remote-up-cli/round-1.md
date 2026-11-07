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

## Local verification pending
- go vet ./... and full cmd/baha suite (background run in progress).

## END
- Lane still active.
