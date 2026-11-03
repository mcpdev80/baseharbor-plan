## r27 delivery-boundary — fix-r3 (last two-pixel guard fix)

**Lane:** w5-delivery-r4 (Coordinator f49a3303). **Role:** WORKER.
**Base:** head `d2a88e09` (work/r27-delivery-boundary). **Candidate SHA:** `122ec95638c94164acef35db6a4d2f72fe854fc4` (tree `…`, pushed FF, remote confirmed via `git ls-remote`).
**Evidence path:** `baseharbor-plan/evidence/r27-night-2026-11-02/delivery-boundary/fix-r3.md`.

### Context

PR #1333 was REJECTED at `review-1333c.md` (Codex GPT-6, session `01a19e29…`). Point 4 (history) is non-blocking, handled separately by the Coordinator. This micro-fix addresses review points **1** and **3** — the store guard is now *wortglaubwürdig* (credibly truthful): the one-writer guard reads an authoritative persisted owner instead of accepting a caller-forged `Observed.Owner`.

### Root cause (review point 1)

`internal/deployment/deployment_store.go:SaveDeploymentRecord` ran `refuseOneWriterMutation(record)` on **caller-supplied** fields, and only read the previous record afterwards — for provider-preferences retention — without comparing its owner. The production hook `observeReconciliationOwner` (added on develop, removed here — see write-set) only set the real owner on the CLI apply path. Callers that bypass that hook (e.g. `internal/application/provider_preferences.go`, which calls `SaveDeploymentRecord` directly with a caller-supplied `Observed`) could forge `Observed.Owner=""` or `Owner=baseharbor` and overwrite a previously externally-owned record. The previously shipped tests constructed the second record with `OwnerExternal` already copied in, so they never exercised the attack.

### Changes (candidate `122ec956` vs base `d2a88e09`)

- **`internal/deployment/deployment_store.go`** — moved the previous-record read ABOVE the one-writer guard. The guard now evaluates the **persisted** `previous.Observed.Owner` when a previous record exists; otherwise the applied selection's mode fixes the owner (a direct/BaseHarbor apply has no prior external owner, so the guarded happy path stays green). The caller-supplied `Observed.Owner` is never used by the guard. Preferences retention now only runs when `previousExists`.
- **`cmd/baha/application_backend_placement_owner.go`** — restored to develop (`git checkout origin/develop -- …`): removed `observeReconciliationOwner` + the now-unused `delivery` import. The guard lives in the store; the CLI hook is outside the card's minimal write-set and callers bypass it anyway (review point 2, satisfied by centralizing in the store).
- **`internal/deployment/one_writer_guard_test.go`** — replaced the two forgeable-field tests with attacker regression tests:
  - `TestAttackerEmptyOwnerDoesNotMutateExternalProof`: seed external owner → submit `Owner=""` and forged `Owner=baseharbor` (Mode=direct), assert `ErrUnauthorizedMutation` and **no `deployment.json` written** (store/runtime no-mutation).
  - `TestAttackerForgedBaseharborOwnerCannotMasquerade`: seed external → forged baseharbor direct apply → `ErrUnauthorizedMutation`, no mutation.
  - Positive direct/delegated happy paths seeded first, remain green; `TestPersistedDirectOwnerPassesDirectApply` kept for the alt-gap.
- **ADR 0022 (EN/DE) + `docs/spec/delivery-provider-v1.md` (EN/DE)** — present-tense detection verbs; decision §2 and spec state that the invariant is enforced at `SaveDeploymentRecord` *before any state is written* (now provably true); DE 'gleiche CA' no-GitOps negation corrected; DE ADR `fehlerfrei fehl` → `bei Konflikt fehl` (the prior reading meant "fails error-free", wrong).

### repo-rule compliance

- Write-set inside card: no `.github/`, no `scripts/`, no CI files. Net diff: CLI file −48 lines (restored), store +42/−…, test rewritten, 2 ADRs + 2 specs wording only.
- FF push on the shared branch (no force), no merge (mission STOP).

### Verification (local, isolated)

```
go build ./...                                   # ok
go vet ./internal/deployment/ ./internal/delivery/ # ok
TMPDIR=/tmp go test ./internal/deployment/ ./internal/delivery/ -count=1   # deployment: 5 guard tests PASS (1 pre-existing target_test.go env-isolation fail, identical on develop); delivery ok
TMPDIR=/tmp BASEHARBOR_STATE_DIR=/tmp/... go test ./cmd/baha/ -count=1     # TestNoImpactPlan... PASS; net-zero regressions vs develop (same 282 shared-env isolation fails as develop)
```
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-delivery-boundary` → `122ec95638c94164acef35db6a4d2f72fe854fc4` (confirmed post-push).
- No hosted CI logs (mission: none). Net diff includes no ADR 0021/target-access changes.

### Review-1333c compliance

1. **Resolved.** Authoritative resource-owner observation = the persisted previous record; selection normalized and checked at the mutation boundary (store guard); all conflict/unknown paths fail closed (`ErrConflictingOneWriter`/`ErrUnauthorizedMutation`); regression seeds external ownership and submits empty + forged BaseHarbor without copying the prior value; direct happy path stays green.
2. **Resolved (minimized).** CLI file reduced to minimum — restored to develop since the store hook supersedes it; net diff 5 files, no CI files.
3. **Resolved.** EN/DE ADR + specs describe actual implementation honestly (enforced at `SaveDeploymentRecord` before write); DE wording corrected.
4. **Non-blocking** — history hygiene left to Coordinator (per mission).

**END lane DONE** — candidate `122ec956`, FF pushed, no merge. Two-attempt STOP not hit.
