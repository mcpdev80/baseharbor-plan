# CODEX-REVIEW 0427-173 r6 — PR #1505

ROLLE: REVIEW
URTEIL: korrektur

## PLAN

1. Verify live PR head, develop head, ancestry, and the terminal hosted run.
2. Trace the MCP test and production handler order: registration, resolution, authorization, drift injection, and mutation.
3. Recheck the on-disk identity guard, already-missing idempotency, version-mismatch classification, and successful prune path.
4. Record the exact remaining correction and the hosted/local verification state.
5. Publish this SHA-specific review to baseharbor-plan origin/main and post END.

## Candidate and hosted state

- PR #1505 exact head: `df9af471dc0b058ed7a59a36e6cb41279ed54475`.
- Live `develop`: `b3a8042d18ea60f162a32a51df34a499cad6a237`; PR head is based directly on develop. `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 df9af471dc0b058ed7a59a36e6cb41279ed54475` returned 0.
- `git ls-remote` confirmed `refs/heads/develop` at `b3a8042d18ea60f162a32a51df34a499cad6a237` and `refs/pull/1505/head` at `df9af471dc0b058ed7a59a36e6cb41279ed54475`.
- Hosted run `42578280694` is terminal `completed/success` on that exact head. `PR Selected Checks` passed (job `129034751870`); `go-unit-tests` passed (`129031035923`); `deployment-package-tests` passed (`129031035985`); source format, build, vet, and documentation jobs passed. Native Keycloak/Core, Selected Runtime, and Targeted HA jobs were skipped and are not counted as passes. Native destroy-retry Docker and Podman executed and passed (`129031038306`, `129031038282`).
- Exact-head focused local test `go test ./cmd/baha/ -run 'TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation|TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord' -count=1` passed. A broader local group stopped at `TestAppPruneIsRegisteredAndRefusesLiveSource`, which attempted to write under the read-only default `/home/marcel/.local/share/baseharbor`; the hosted go-unit and package jobs above passed.
- The r6 commit delta from develop is limited to `cmd/baha/app_prune.go`, `cmd/baha/app_prune_test.go`, and `internal/deployment/deployment_store.go`; no `.github/**` files changed.

## Findings

### 1. Blocking: drift injection is before authorization, not after it

The test now goes through the live in-memory MCP client and `registerMCPAppPruneTool`, and the registered handler performs the eventual mutation. However, the required ordering is not present. In `cmd/baha/app_prune.go:418-435`, the handler captures `authorizedIdentity`, invokes `pruneDriftHook` at lines 428-430, and only then calls `authorizeResolvedMCPOperation` at line 431. The hook therefore rewrites the on-disk identity before the authorization function executes. Capturing a value named `authorizedIdentity` is not the completed authorization step.

`cmd/baha/app_prune_test.go:747-760` performs the record rewrite from that hook; the test invokes the registered tool at lines 763-765 and checks the refusal and byte preservation at lines 774-790. This proves the registered handler sees a changed record after its initial resolution, but it does not prove a record drift occurring after successful authorization and before the handler's mutation is rejected. This is the precise r5 stop criterion.

### 2. The three neighboring storage protections remain in source

- `internal/deployment/deployment_store.go:623-631` still calls `assertOnDiskIdentityMatches` before `os.RemoveAll`.
- At `:641-647`, a missing `deployment.json` returns nil for idempotent already-removed state; other read failures remain errors.
- At `:650-657`, malformed state, wrong record version (`DEPLOYMENT_RECORD_VERSION`), and identity mismatch (`IDENTITY_DRIFT`) have separate fail-closed paths.
- `TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord` at `cmd/baha/app_prune_test.go:798-864` still drives the registered MCP tool and asserts the record is removed on success.

The focused local MCP tests and the exact-head hosted unit/package suites passed. I did not find a dedicated test asserting repeated deletion of an already-missing record or the named version-mismatch code in the current test sources, so those two source behaviors are confirmed but their specific regression coverage is not independently established by this review.

## Verdict

**KORREKTUR** for `df9af471dc0b058ed7a59a36e6cb41279ed54475`.

The registered-handler path and handler-owned mutation are now exercised, and the other storage protections remain in place. The mandatory drift timing is still wrong: the injection occurs before `authorizeResolvedMCPOperation`, so the test does not establish the post-authorization race required by the r5 review.

## Actionable correction recipe

- File: `cmd/baha/app_prune.go`, around lines 428-435. Move the `pruneDriftHook` invocation to after `authorizeResolvedMCPOperation` succeeds and immediately before `executeApplicationPruneResolved`. Keep the hook inside the registered handler and nil in production.
- File: `cmd/baha/app_prune_test.go`, `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation`. Keep the live `mcp.NewServer` registration and `clientSession.CallTool`; inject the replacement only through the handler seam after successful authorization; assert the handler's own mutation returns `IDENTITY_DRIFT`, leaves the replacement record byte-identical, and does not remove its directory. The drift test itself must not invoke `executeApplicationPruneResolved` or `DeleteDeploymentRecord` directly.
- Retain the separate successful MCP happy-path check and the storage checks for already-absent idempotency plus distinct malformed/version/drift causes. Add focused regression assertions for idempotent repeated deletion and `DEPLOYMENT_RECORD_VERSION` if the neighboring changes are not already covered by a CI-selected test.
- Test requirement: the focused MCP drift and happy-path tests must pass locally; the changed `cmd/baha` tests must execute in hosted `go-unit-tests` on the exact new head; `deployment-package-tests` and `PR Selected Checks` must also be terminal success. Existing native skipped jobs remain reported as skipped, not as passes.
- Stop criterion: do not approve until the registered handler successfully authorizes identity A, the hook then replaces the on-disk record with identity B, and the handler's own mutation rejects B as `IDENTITY_DRIFT` while preserving the replacement bytes and directory. Require refreshed develop ancestry and exact-head hosted unit/package/Selected Checks success.

## repo-rule compliance

- Review-only: no product files or workflow files changed.
- Candidate verified unchanged before and after the review: `df9af471dc0b058ed7a59a36e6cb41279ed54475`.
- Evidence stored only in baseharbor-plan.
- No containers or compose projects were started.

END_DONE 0427-173-r6-review: KORREKTUR PR #1505 head `df9af471dc0b058ed7a59a36e6cb41279ed54475`; drift hook precedes `authorizeResolvedMCPOperation`, so post-authorization drift remains unproven; hosted run `42578280694` success on exact head.
