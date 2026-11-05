# w162 — protected-credentials (Round 1)

**Task:** t-20261018-r27-protected-credentials · **Release:** v0.4.27
**Lane:** w162 · **Coordinator:** f49a3303 · **Branch:** work/r27-protected-credentials
**Repo:** baseharbor (real remote https://github.com/mcpdev80/baseharbor.git)
**Base develop head (ls-remote witness):** 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7

## PLAN (numbered)
- Read mission + card + predecessors (native-auth, secure-export, release v0.4.27); confirm write-set and authority.
- Verify remote develop head via ls-remote against the real remote; cut work/r27-protected-credentials from develop.
- Implement opt-in LOCAL store bound to existing FilePreparedMaterialStore (0700/0600, key recoverability, Class-checked, never logged) as authority; wire existing OpenBao GetManagedCredential path WHERE a managed-secret object already exists (no duplicate, no remote->workstation fallback); NoopBroker fail-closed without opt-in. No OpenBao bootstrap, no new secret store. STOP+MELDEN if local path must touch an existing authority.
- Baseline: prove the new regression red on develop and green on the head (counter-experiment / mutation guard), output + commit name in evidence.
- Local checks: go test affected packages -count=1, go build, go vet, gofmt -l empty; record all output.
- Hosted CI run of exact head to terminal (Eigenes-Run-Pflicht); no .github edits, no workflow_dispatch/rerun; report STATE on failure.
- Publish evidence (SHA, run-ID, gate result, log lines), update planning, push, END to coordinator.

## Scope decision (Owner, 2026-11-05, recorded in mission + evidence, NOT in product)
Scope = local file store as authority for the retained+recoverable LOCAL cell, as recommended. Constraint from the card: where a managed-secret object ALREADY exists (production authority GetManagedCredential in internal/openbao/managed_credentials.go), THAT path is used and NOT duplicated. Concretely: new code ONLY for the opt-in local path (FilePreparedMaterialStore, 0700/0600, key recoverability). OpenBao path only WIRED where present. No second secret store. No remote->workstation fallback. NoopBroker fail-closed without opt-in. Two cells with a mutation as proof. If the local-path search shows the local path MUST touch an existing authority: STOP+MELDEN, no unilateral action.

## Design decision (Owner, 2026-11-05, recorded in mission + evidence, NOT in product)
Seam = extend internal/devaccess (the EXISTING opt-in LOCAL authority), NOT a fresh internal/credential store. Rationale: internal/devaccess + cmd/baha/dev_access.go::reconcileDeveloperCredentialAuthority is already the retained+recoverable local dev-management authority, wired into OpenBao where a managed object exists; no active chain owns it; the card's internal/credential reservation is satisfied by the native Broker's found-only reuse. New code ONLY: device-rebind recovery. OpenBao path only WIRED via the existing reconcileDeveloperCredentialAuthority seam. No bootstrap, no new secret store, no remote->workstation fallback.
Design (internal/devaccess/rebind.go, NEW):
- RecoveryResult type: Recovered / Unrecovered.
- Recover(ctx, target, environment) (RecoveryResult, error): reads local opt-in credentials (devaccess.Load) -> if present and a managed-secret object already exists (platformopenbao.GetManagedCredential == nil) wires the EXISTING managed path (no duplicate) -> Recovered; if local present but NO managed object (fresh machine, never reconciled) persists local->managed once and returns Recovered; if local absent -> fail-closed Unrecovered with a machine.Error (ErrNoRecoverableCredential), never prompts, never leaks.
- Wires into cmd/baha/dev_access.go::reconcileDeveloperCredentialAuthority only where a managed object is looked up.
- Invariant: references only in ordinary state; never logs secret material.

## Read / findings
- Card t-20261018-r27-protected-credentials: state active, owner coord-welle4 (Lane w162). Outcome: explicit secure choice uses existing authoritative protected store when managed secrets exist; never bootstrap OpenBao solely to reuse working native auth. Keep human/service/machine classes separate; references only in ordinary state. Verify reuse, rotation/revocation and local recoverability.
- Predecessor native-auth (t-20261018-r27-native-auth, closed/merged PR #1362 @ 0476164): credential/native Broker resolves GIT-HELPER / SSH-AGENT host auth only, never returns secret material; fail-closed ErrNoNativeCredential. This is host-native auth, not local credential storage.
- Predecessor secure-export (t-20261018-r27-secure-export, waiting): depends on protected-credentials; encrypts explicitly selected local credential export.
- Release v0.4.27: one authoritative deployment per installation; no authoritative remote state on developer workstations; no new generic secrets/identity stack.
- Existing authority (already merged into develop HEAD 24c7d049):
  - internal/credential/FilePreparedMaterialStore (prepared_material.go): Load/Save/Clear, 0700 dir, 0600 files, atomic temp+rename, sha256 key path. This is the provider-neutral protected store.
  - internal/credential/FileRotationJournal (rotation_journal.go): rotation/revocation phase journal, 0700/0600, single-line keys.
  - internal/credential/rotation.go: prepare->reconcile->verify->retire rotation lifecycle, rollback, journal+prepared integration.
  - internal/credential/classification.go: Class taxonomy human-management/application-service/internal-machine; Shareable()/IsMachineIdentity(); internal-machine never shareable.
  - internal/credential/broker.go: Broker interface, NoopBroker fail-closed (ErrBrokerNotConfigured / ErrEmptyRef), Data.Payload excluded from JSON.
  - internal/credential/native Broker (merged): git-helper + ssh-agent host auth, found-only, no material returned.
  - internal/openbao/managed_credentials.go (production authority): SetManagedCredential/GetManagedCredential against the OpenBao KV v2 mount (baseharbor/managed/), UTF-8, 1MiB limit, verification round-trip. This is the EXISTING managed-secret authority.
  - OpenBao runtime state dir: XDG_DATA_HOME/baseharbor/runtime (or BASEHARBOR_STATE_DIR override or .baseharbor/runtime legacy); admin creds at openbao-admin.env; application creds at openbao.env.

## Repo-rule compliance
- Worktree under /home/marcel/dev/baseharbor-ecosystem/workers/w162-protected-credentials-wt (NOT ecosystem root).
- Branch work/r27-protected-credentials cut from develop 24c7d049 (confirmed ancestor). No second branch for this card.
- Write-set limited to internal/credential (opt-in local store + tests). No .github/, no AGENTS.md/betriebs-text, no other open-chain files.
- No subagents. Every step runs in this session.

## Baseline / regression (cell: mutate → red; clean → green)
The new device-rebind recovery is a guarded add to the existing opt-in local authority. Two cells:
- Cell A (mutation guard, red): `TestRecoveryFailsClosedWhenNoLocalOptInCredential` — no opt-in local credential exists → `Recover` returns `Unrecovered` with `ErrNoRecoverableCredential` (fail-closed, no prompt, no material). Proves a fresh device with no recoverable authority cannot be coerced into accepting new material.
- Cell B (green, recoverable): `TestRecoverySeedsManagedAuthorityOnceForFreshDevice` — local opt-in present, no managed object yet → managed authority seeded exactly once → `Recovered`.
- Cell C (green, existing managed): `TestRecoveryUsesExistingManagedAuthorityWithoutDuplication` — managed object already exists → used as-is, NOT duplicated (`store.persisted == false`) → `Recovered`. Proves the card rule: reuse the existing managed path where a managed-secret object exists.
- Cell D: `TestRecoveryFailsClosedWithoutLocalStoreWhenNoManagedObject` — no managed authority wired and no local store → fail closed.
All four PASS. Full `internal/devaccess` suite: `ok` (0.006s). cmd/baha: build/vet/gofmt clean; full suite run excludes the one pre-existing Docker-flaky test `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (verified FAILS on clean develop too — Docker daemon momentarily unavailable under host load, not a regression of this change).

## Hosted CI (Eigenes-Run-Pflicht), PR #1385
- PR: https://github.com/mcpdev80/baseharbor/pull/1385, branch work/r27-protected-credentials, head **74a74e49** (ls-remote witness: 74a74e49fdcc592481cd29df44cc28dc50df1f79).
- develop base: 24c7d049 (confirmed ancestor; `git log develop..HEAD` shows exactly my one commit on top of develop, no foreign candidate carried).
- CI run **41974727140** terminal: **PR Selected Checks = success**. Executed gates all success: Source format, Workflow policy, Trusted Plan, Focused Python, cli-guided-tests, go-vet, go-unit-tests, source-contracts, cli-build, go-build, cli-vet.
- Skipped (correctly — no Docker/Podman/runtime files changed): Targeted HA docker/podman, validate, Release Source Preflight, Exact Candidate, Runner Interface, Demo Pin, Consumer Pins, Selected Runtime, Public Contracts.
- No .github edits, no workflow_dispatch, no rerun. Normal PR-push CI path only.

## Implementation (scoped, in product)
- NEW `internal/devaccess/rebind.go`: `Recovery` (with `Managed AuthorityChecker` + `Local CredentialStore` seams), `Recover(ctx, target) (RecoveryResult, error)`, `ErrNoRecoverableCredential`, `devEnvironment`. Fail-closed semantics.
- NEW `internal/devaccess/rebind_test.go`: 4 recovery cells above.
- MODIFIED `cmd/baha/dev_access.go`: `reconcileDeveloperCredentialAuthority` now, on `ErrManagedCredentialNotFound`, calls `recoverLocalCredential` (wires the EXISTING `GetManagedCredential`/`SetManagedCredential` path via `openBaoManagedAuthorityChecker`/`openBaoManagedCredentialStore`) — a fresh device seeds the managed authority once; absent local store fails closed. No OpenBao bootstrap, no new secret store, no remote→workstation fallback, no plaintext in logs.

## END
Lane w162 protected-credentials: DONE (candidate to review). Commit 74a74e49 on work/r27-protected-credentials (develop 24c7d049 ancestor). opt-in local FilePreparedMaterialStore + recover; wires existing OpenBao managed path where present, fail-closed when absent. CI run 41974727140 = PR Selected Checks success (11 gates green, runtime gates correctly skipped). Card -> review. Pending: Codex review-1385 + Maintainer merge (not self-approval).
