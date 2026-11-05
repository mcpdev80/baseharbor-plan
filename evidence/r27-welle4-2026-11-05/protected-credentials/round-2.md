# w170 — protected-credentials (Round 2)

- Task: t-20261018-r27-protected-credentials · Release: v0.4.27
- Lane: w170 · Coordinator: f49a3303 · Branch: work/r27-protected-credentials
- Repo: baseharbor (real remote https://github.com/mcpdev80/baseharbor.git)
- Base develop head (ls-remote witness): 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7

## PLAN (numbered)

- Read mission, review-1385a (VOLL), round-1; confirm write-set and authority.
- Verify remote develop + PR head via ls-remote; cut work/r27-protected-credentials from develop (ancestor attested).
- Implement single-Set-per-path fix in cmd/baha/dev_access.go: one Set per path, already-set => only Get no Set, communicate already-seeded, return actually-managed value, no overwrite of concurrent value.
- Production-flow test at existing reconcile seam: count Get/Set pairs through the real production path.
- Local checks: go test affected packages -count=1, go build, go vet, gofmt -l empty.
- Baseline regression (mutate => red; clean => green) counter-experiment.
- Hosted CI run of exact head to terminal (no .github edits, no workflow_dispatch/rerun); report STATE on failure.
- Publish evidence (SHA, run-ID, gate result, log lines), update planning, push, END to coordinator.

## Base attestation

- Branch work/r27-protected-credentials cut from develop 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7.
- ls-remote witness: develop 24c7d049..., PR head 74a74e49 (matches mission).
- HEAD 74a74e49 is the sole commit on develop..HEAD (predecessor w162). develop 24c7d049 is its parent, confirmed ancestor of the first fix commit e295127e.

## Review verdict (review-1385a, CODEX-REJECT)

- Write set at head 74a74e49 is exactly cmd/baha/dev_access.go, internal/devaccess/rebind.go, internal/devaccess/rebind_test.go. No new internal/credential or store file; all 57 internal/openbao/ and 277 internal/application/ blobs and the existing prepared_material.go blob unchanged.
- Verdict REJECT. The four recovery tests exercise stubs and miss the production reconcile flow. On a fresh opt-in device the path seeds the managed authority once via Store.Persist (SetManagedCredential), then the switch falls through and unconditionally calls SetManagedCredential(candidate) again. Double write, plus a lost-update race: a managed object created after the first not-found read but before Recover.Managed.Exists yields Recovered without persist, yet the unconditional second SetManagedCredential(candidate) overwrites it. Violates existing managed-authority precedence.
- Recipe: make recovery return/communicate that it already seeded the managed authority and return the recovered candidate without the unconditional second SetManagedCredential; before any write preserve a managed object that appeared concurrently; do not overwrite it with a stale local candidate.
- Stop criterion: if recovery can issue two writes or overwrite a concurrently-created managed value, reject; do not add a new credential store or bypass existing OpenBao authority.

## Scope decision (Owner, 2026-11-05, recorded here, NOT in product)

Round 2 fix is scoped to the single reconciliation seam only: cmd/baha/dev_access.go::reconcileDeveloperCredentialAuthority, plus a focused production-flow test at the existing reconcile seam. Fix = one Set per path, already-seeded => only Get no Set, communicate already-seeded, return the actually-managed value, preserve a concurrent managed value, never overwrite it. No new store, no OpenBao bootstrap, no remote->workstation fallback. No .github edits, no workflow_dispatch/rerun.

## Design decision (Owner, 2026-11-05, recorded here, NOT in product)

Root cause sits in cmd/baha/dev_access.go::reconcileDeveloperCredentialAuthority, not in internal/devaccess/rebind.go's Recovery result semantics. Recovery.Recover already returns the correct Recovered/Unrecovered outcome; the bug is that the caller ignores the outcome and unconditionally issues the second SetManagedCredential(candidate). Fix:

- The caller must not fall through to the unconditional encode + SetManagedCredential(candidate) after a fresh-device recovery that already seeded the managed authority.
- The authoritative value returned to the caller must be the actually-managed value (GetManagedCredential), not the stale local candidate, so a concurrent managed value wins.
- One Set per path: the fresh-device seed (via Store.Persist) is the ONLY Set on that path; the existing-managed path does zero Sets; the not-found-and-no-opt-in path is fail-closed.
- Test requirement: inject/count managed Get/Set calls through the full production reconcile path. Assert one Set for absent-managed + opted-in local; zero Sets and preserve the winning value when a managed object appears between checks; existing-managed reads do not duplicate; retain the two fail-closed cells and exact-head selected checks.

## Repo-rule compliance

- Worktree under /tmp/opencode/w170-credentials-r2-wt (NOT ecosystem root).
- Branch work/r27-protected-credentials cut from develop 24c7d049 (confirmed ancestor). No second branch for this card.
- Write-set limited to cmd/baha/dev_access.go + tests. No .github/, no AGENTS.md/betriebs-text, no other open-chain files.
- No subagents. Every step runs in this session.

## Hosted CI (Eigenes-Run-Pflicht), PR #1385

- PR: https://github.com/mcpdev80/baseharbor/pull/1385, branch work/r27-protected-credentials, head **e295127e** (ls-remote witness: e295127e45b1c1d2c9929a312fa344095469c864).
- develop base: 24c7d049 (confirmed ancestor; git log develop..HEAD shows exactly my one round-2 commit on top of 74a74e49, no foreign candidate carried).
- CI run **41985472620** (run_number 4767) terminal: **PR Selected Checks = success**.
- Gates all success (witnessed via GitHub API): PR Trusted Plan, Workflow policy, PR Source format, PR Focused Python, cli-build, go-vet, cli-guided-tests, cli-vet, cli-gofmt, cli-package-tests, source-contracts, go-build, go-unit-tests, PR Selected Checks.
- Skipped (correctly — no Docker/Podman/runtime files changed): Targeted HA docker/podman, Release Source Preflight, validate, Runner Interface, Consumer Pins, Exact Candidate, Selected Runtime, Demo Pin, Public Contracts.
- No .github edits, no workflow_dispatch, no rerun. Normal PR-push CI path only.

## Implementation (scoped, in product)

- MODIFIED cmd/baha/dev_access.go (reconcileDeveloperCredentialAuthority): the fresh-device recovery case now reads the managed object back and returns the actually-managed value via decode(...) instead of falling through to the unconditional second SetManagedCredential(candidate). Exactly one Set on the fresh path (the single seed via Store.Persist); existing-managed path issues zero Sets; fail-closed path issues zero Sets.
- MODIFIED cmd/baha/dev_access.go (recoverLocalCredential): returns the RecoveryResult so the caller decides the write; comment updated to state one Set per path + read-back.
- NEW seam vars (default to the production platformopenbao authority, overridable in tests): openBaoRuntime (wraps original), openBaoInspect, openBaoCheckManager, managedCredentialSeam (typed managedCredentialSeamFuncs), devRecoveryFactory. Production control flow unchanged except the fix itself.
- NEW cmd/baha/dev_access_reconcile_test.go (4 cells + mutation guard): seeds-managed-exactly-once (1 Set + read-back), concurrent-managed-wins (0 Set, existing value preserved), existing-managed-reads-no-duplicate (0 Set), fail-closed-without-opt-in (0 Set). Mutation guard: reintroducing the unconditional second Set makes exactly-once go RED (2 Sets).

## END

Lane w170 protected-credentials: END_DONE w170-credentials-r2: head=e295127e zaehlung=1 set je fresh-device/0 set je existing+failclosed konkurranz=vorhanden gewinnt pfadecht=reconcile-only lauf=41985472620 success lsremote=e295127e | round-2 fix pushed to PR #1385, CI Selected Checks success, card -> re-review.
