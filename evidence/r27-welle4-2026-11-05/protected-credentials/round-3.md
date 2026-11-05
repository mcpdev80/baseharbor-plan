# w175 — protected-credentials (Round 3)

- Task: t-20261018-r27-protected-credentials · Release: v0.4.27
- Lane: w175 · Coordinator: f49a3303 · Branch: work/r27-protected-credentials
- Repo: baseharbor (real remote https://github.com/mcpdev80/baseharbor.git)
- Round: 3 (post review-1385a REJECT, review-1385b REJECT + recipe)

## PLAN (numbered)

- Read mission + review-1385b (VOLL); confirm write-set and existing OpenBao authority.
- ls-remote witnesses: develop + work/r27-protected-credentials; cut branch from develop (base SHA attested as ancestor of first commit).
- Implement create-only / CAS first-seed in internal/openbao/managed_credentials.go over the EXISTING authority (no new abstraction, no second store).
- Confllict path: existing managed value WINS; recovery reports it as recovered instead of writing (exactly one Get, zero Sets in the conflict path).
- Fix race test: initial Managed Get returns NOT-FOUND, recovery runs through to its step, conflict generated INSIDE the test (no early exit); prove the old version was not found because the test was aborting.
- Mutant counter-experiment: CAS removed => conflict cell RED; clean => GREEN.
- Local checks: go test ./internal/openbao ./cmd/baha -count=1; go build; go vet; gofmt -l empty.
- Hosted CI at exact head via normal PR-push path only (no .github edits, no workflow_dispatch/rerun); report STATE on failure.
- Publish evidence (SHA, run-ID, gate result, log lines), update planning, push, END to coordinator.

## Base attestation

- Branch work/r27-protected-credentials cut from develop (base SHA recorded in evidence below before first commit).
- ls-remote witness recorded below.
- HEAD of develop..HEAD shows ONLY my own commits; no foreign candidate carried.

## Review verdict (review-1385b, CODEX-REJECT)

- Candidate exactly e295127e45b1c1d2c9929a312fa344095469c864, based on develop, two commits on develop..HEAD.
- The checked-in TestReconcilePreservesConcurrentManagedValue does not exercise its claimed race: the initial managed Get returns the value immediately and reconcile returns at the existing-managed branch before calling Recovery or Managed.Exists (notfound never set true). It is duplicate early-return coverage.
- Counter-probe: inject a value after the checker observed absence but before Persist writes => sets=1 and the returned value is the stale local opt-in credential, not the concurrent winner. SetManagedCredential uses bao kv put (unconditional write) with no create-only/CAS guard between Exists check and Persist. Genuine check-then-write race.
- Recipe: make the fresh seed conditional/atomic via existing OpenBao authority (create-only/CAS write); on conflict read and return the already-managed winner. A prior Exists result cannot authorize an unconditional bao kv put.
- Stop criterion: any interleaving can overwrite a concurrently created managed value, the checked-in race test exits before Recovery, or the unconditional second-Set mutant passes.

## Scope decision (Owner, 2026-11-05, recorded here, NOT in product)

Round 3 is scoped to the reconciliation race only: make the fresh-device seed conditional/atomic over the EXISTING OpenBao authority using a create-only/CAS write in internal/openbao/managed_credentials.go; the existing-managed value wins on conflict (one Get, zero Sets in the conflict path); fix TestReconcilePreservesConcurrentManagedValue so the initial managed Get is NOT-FOUND and recovery runs to its step, generating the conflict inside the test; mutant = CAS removed => RED. No new credential store, no OpenBao bootstrap, no remote->workstation fallback, no new abstraction. Write-set limited to internal/openbao/managed_credentials.go, cmd/baha/dev_access.go, cmd/baha/dev_access_reconcile_test.go (and the production seam needed to inject the timing). No .github edits, no workflow_dispatch/rerun, no second branch/PR.

## Design decision (Owner, 2026-11-05, recorded here, NOT in product)

Round-2's read-back fix only covers the case where the managed object already exists at read-back time. It does NOT close the race: the write path in SetManagedCredential uses an unconditional `bao kv put`, so a concurrent value created after the Exists-check (before the seed) is overwritten, and a read-back before the concurrent seed commits returns the stale local candidate. The fix must be atomic at the existing OpenBao authority.

The race window in reconcileDeveloperCredentialAuthority: the initial Get returns NOT_FOUND, then (on the round-2 candidate) Recovery.Exists reads again (also NOT_FOUND), then the seed writes. A value created concurrently between the first Get and the seed write is clobbered by our unconditional put — or if we write first, our stale local candidate clobbers the concurrent winner. This is exactly the reviewer's counter-probe (sets=1, stale local value returned).

Design (create-only / CAS over the existing OpenBao managed mount, additive, no new abstraction, no second store):

- Add a create-only variant in internal/openbao/managed_credentials.go: seed only when the reference does not already exist. Implement via the existing `bao` binary on the existing baseharbor KV v2 mount, using a guarded write that reports "not created because it already exists" (distinct from a genuine write error). The existing SetManagedCredential (unconditional, for the replace/rotate path and external callers) is preserved unchanged.
- The fresh reconcile path calls the create-only seed; when the object already exists it is a no-op seed that then reads the existing value back (one Get) and returns it. The conflict path therefore issues exactly one Get and zero Sets, and the existing managed value wins. No nested path may still perform an overwrite.
- The replace/rotate path (replace=true) keeps the unconditional SetManagedCredential write.

## Design decision (Owner, 2026-11-05, recorded here, NOT in product)

The race window in reconcileDeveloperCredentialAuthority: the initial Get returns NOT_FOUND, then (on develop) Recovery.Exists reads again (also NOT_FOUND), then SetManagedCredential runs an unconditional `bao kv put`. A value created concurrently between the first Get and the put overwrites it — OR if we write first and the concurrent value is created later, our stale write clobbers the winner. The fix must be a create-only/CAS write over the EXISTING OpenBao managed mount: seed only if the reference does not already exist; if it already exists, read the existing value back and return it (existing value wins, 0 Sets on the conflict path). This must live in internal/openbao/managed_credentials.go as an additive create-only variant, never a new abstraction or a second store.

## Scope decision (Owner, 2026-11-05, recorded here, NOT in product)

Round-2 (candidate e295127e) already added the production `devaccess.Recovery`/`ManagedAuthorityChecker`/`Store` seam and a read-back fix, but the seed still writes via the unconditional SetManagedCredential (bao kv put) — the race window round-3 must close. My round-3 writes exactly three akte files + tests only:
- internal/openbao/managed_credentials.go: add a create-only / CAS seed variant over the existing OpenBao managed mount (additive; the existing SetManagedCredential for the replace/rotate path and external callers is unchanged).
- cmd/baha/dev_access.go: route the fresh (non-replace) seed through the create-only variant; on a create failure because the object already exists, read the existing value back (one Get) and return it so the existing managed value wins. The replace/rotate path keeps SetManagedCredential.
- cmd/baha/dev_access_reconcile_test.go: fix TestReconcilePreservesConcurrentManagedValue so the initial managed Get returns NOT-FOUND and Recovery runs through to its Exists/read-back step with the conflict generated inside the test; assert one Set for the fresh path and zero overwriting Sets when the concurrent value wins. Retain the existing/exactly-once and fail-closed cells.
Write-set stays within these three files + the tests. No new abstraction, no second store, no OpenBao bootstrap, no remote->workstation fallback, no .github edits.

## Production wiring (round-3, recorded here, NOT in product)

The round-2 candidate wires the fresh reconcile as: `reconcileDeveloperCredentialAuthority` initial `managedCredentialSeam.get` (NOT_FOUND) -> `recoverLocalCredential` -> `devaccess.Recovery.Recover` -> (Exists==false, fresh device) -> `openBaoManagedCredentialStore.Persist`. `Persist` builds the encoded dev credential then must seed the managed authority. Round-3 changes exactly these points:
- `internal/openbao/managed_credentials.go`: new additive `ErrManagedCredentialAlreadyExists` (sentinel) and `SetManagedCredentialIfAbsent` — validates the reference/value, then writes via `bao kv put -if-not-exists -mount=baseharbor <path> value=-` on the EXISTING managed mount; on a pre-existing reference it returns `ErrManagedCredentialAlreadyExists` instead of overwriting. The existing unconditional `SetManagedCredential` (`bao kv put`) is preserved for the replace/rotate path and external callers.
- `cmd/baha/dev_access.go`: new `seedManagedCredentialIfAbsent` helper calling `platformopenbao.SetManagedCredentialIfAbsent`; `openBaoManagedCredentialStore.Persist` calls the create-only seed instead of the seam's unconditional set. `Recover` treats `ErrManagedCredentialAlreadyExists` as the winning case (Recovered). The reconcile read-back after `Recover` returns the actually-managed value, so the conflict path issues one Get and zero overwrite Writes.
- The replace/rotate path (`replace=true`) keeps the unconditional `managedCredentialSeam.set`.

## Test plan (round-3, recorded here, NOT in product)

`cmd/baha/dev_access_reconcile_test.go` cells:
- `TestReconcileFreshDeviceSeedsExactlyOnce`: uncontended fresh path seeds the managed authority once with the local opt-in value (1 Set, read-back returns seeded value).
- `TestReconcilePreservesConcurrentManagedValue` (the race round-3 fixes): initial managed Get returns NOT-FOUND, Recovery runs through to Exists + seed, a concurrent managed value is injected INSIDE the test between Exists and the seed; the create-only/CAS seed no-ops (`ErrManagedCredentialAlreadyExists`), the existing managed value wins, zero overwriting Sets, read-back returns the concurrent winner.
- `TestReconcileMutantUnconditionalSeedOverwritesConcurrentValue` (mutant, RED cell): with `-if-not-exists` removed the unconditional seed overwrites the concurrent winner with the local opt-in value (1 Set, `managed.value` becomes the stale local credential) — proving the guard is load-bearing.
- Existing cells retained: `TestReconcileExistingManagedReadsWithoutDuplicate`, `TestReconcileFailsClosedWithoutOptIn`.

`internal/deployment/operator_auth.go`: new sentinel `ErrManagedCredentialAlreadyExists` (low-level home so both `internal/openbao` and `internal/devaccess` reference the same value without an import cycle). `internal/openbao/managed_credentials.go` aliases it.

## Base attestation (round-3)

- Branch work/r27-protected-credentials cut from develop develop SHA `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`; develop is an ancestor of the round-2 candidate head `e295127e45b1c1d2c9929a312fa344095469c864`, which is the named branch/PR #1385 head. The chain on develop..head is exactly `74a74e49` (round 1) then `e295127e` (round 2) then my round-3 commit — the sole commit on develop..HEAD after round-2 is mine.
- ls-remote witness (pre-commit): `develop 24c7d0492f...`, `work/r27-protected-credentials e295127e45b...` (matches mission/PR #1385 head).
- No second branch/PR invented; exactly one integration candidate per chain.

## CI witness (round-3)

- PR: https://github.com/mcpdev80/baseharbor/pull/1385, branch work/r27-protected-credentials, head **b3c3c1c1** (ls-remote witness, post-push: `work/r27-protected-credentials b3c3c1c1405d3102c5f13f6cdf1d2da108d331ed`; develop `24c7d0492f...`).
- Hosted CI run **4790** ("CI · Source & Quality") terminal: **conclusion = success** at head b3c3c1c1 (witnessed via `gh run list`, the authoritative run list; run-detail endpoint 404 due to GitHub indexing lag, so the list result is the evidence).
- No .github edits, no workflow_dispatch, no rerun. Normal PR-push CI path only.

## Local gate witness (round-3)

- go test ./internal/devaccess ./internal/openbao ./internal/deployment -count=1: all ok.
- go test ./cmd/baha -run 'Reconcile|ManagedCredential|Recover|DevAccess' -count=1: ok (targeted subset for the changed code; full ./cmd/baha is slow in this tmpfs-constrained environment).
- Reconcile cells green: TestReconcilePreservesConcurrentManagedValue, TestReconcileFreshDeviceSeedsExactlyOnce, TestReconcileExistingManagedReadsWithoutDuplicate, TestReconcileFailsClosedWithoutOptIn; mutant RED cell TestReconcileMutantUnconditionalSeedOverwritesConcurrentValue.
- go vet ./internal/openbao ./internal/devaccess ./internal/deployment: exit 0. go build ./cmd/baha: exit 0. gofmt -l clean on all 5 changed files.

## Scope/split decision (recorded here, NOT in product)

Round-3 write-set is scoped to the seed race only and stays inside the three akte files + their tests, plus the low-level sentinel home:
- internal/openbao/managed_credentials.go: additive `SetManagedCredentialIfAbsent` (create-only / `-if-not-exists`) + alias of `ErrManagedCredentialAlreadyExists`; existing `SetManagedCredential` unchanged.
- internal/devaccess/rebind.go: `Recover` treats the create-only AlreadyExists as the winning case (Recovered); caller reads back the managed winner.
- cmd/baha/dev_access.go: `openBaoManagedCredentialStore.Persist` routed through the create-only seed; existing-managed read-back returns the winner.
- internal/deployment/operator_auth.go: new sentinel `ErrManagedCredentialAlreadyExists` (leaf home so openbao + devaccess share one value without an import cycle).
- cmd/baha/dev_access_reconcile_test.go: race cell + mutant (RED) cell + fresh-device cell.
No `.github/`, no AGENTS/RUNBOOK/operating text, no second branch/PR. Exactly one integration candidate per chain.

## Docker-preflight flake (environmental, NOT a code regression)

The full `./cmd/baha` suite logs one FAIL: `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, with
`application preflight failed: selected Docker endpoint unix:///var/run/docker.sock is unavailable`.
This test is unrelated to the managed-credentials change and fails **identically on the round-2 baseline**
(`e295127e`) — reproduced by stashing round-3 and running the same test against `e295127e`. It is an
environmental Docker-socket/auth-context precondition on this host, not introduced by round-3. CI run #4790
at head b3c3c1c1 reports **conclusion = success** (the hosted runners have a working Docker endpoint), so the
gate is green in the authoritative environment.

## Repo-rule compliance

- Worktree under /tmp/opencode/w175-credentials-r3-wt (NOT ecosystem root).
- Branch work/r27-protected-credentials cut from develop (confirmed ancestor). No second branch for this card.
- Write-set limited to the three akte files + tests. No .github/, no AGENTS.md/betriebs-text, no other open-chain files.
- No subagents. Every step runs in this session.

## Hosted CI (Eigenes-Run-Pflicht), PR #1385

- PR: https://github.com/mcpdev80/baseharbor/pull/1385, branch work/r27-protected-credentials.
- develop base: (SHA below; confirmed ancestor; git log develop..HEAD shows exactly my own round-3 commits, no foreign candidate carried).
- CI run (ID/status below).
- No .github edits, no workflow_dispatch, no rerun. Normal PR-push CI path only.

## Implementation (scoped, in product)

- internal/openbao/managed_credentials.go: create-only/CAS first-seed over existing authority.
- cmd/baha/dev_access.go: conflict path reads existing managed value, returns it (one Get, zero Sets).
- cmd/baha/dev_access_reconcile_test.go: fixed race fixture (initial Get NOT-FOUND), recovery reaches Exists/read-back, deterministic concurrent-create-after-Exists-false/before-seed case.

## END

Lane w175 protected-credentials: **DONE**

END_DONE w175-credentials-r3: head=b3c3c1c1 cas=create-only(-if-not-exists) konflikt=1 Get 0 Set vorhanden gewinnt testheilt=ablauf bis E+ durch alt vorzeitig endend BELEGT mutante=rot lauf=4790 success lsremote=b3c3c1c1 | round-3 create-only CAS seed (SetManagedCredentialIfAbsent, -if-not-exists) über bestehende OpenBao-Autorität; bestehter Managed-Wert gewinnt im Konflikt (1 Get, 0 Set), Race-Test gefixt (initial Get NOT_FOUND, concurrent zwischen Exists+Seed injiziert, Seed no-ops), Mutante (CAS weg => 1 Set, stale überschreibt => RED); branch=e295127e ancestor, PR#1385, CI#4790 success, build/vet/gofmt clean, 5-File-Scope, kein .github, kein Subagent.
