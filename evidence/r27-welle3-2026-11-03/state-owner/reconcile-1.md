# reconcile-1: work/r27-state-owner x develop (deployment_store.go) — state-owner

- Task: `t-20261018-r27-state-owner` / PR #1347
- Worker lane: `w36-stateowner-reconcile` · Coordinator: `f49a3303`
- Date: 2026-11-03
- Base (merge-base): `9a57107f` · work/r27-state-owner head: `33badf7d` · develop: `1c921c47`

## PLAN (board + JSON live board in sync)

1. ✅ Read mission, refresh remote SHAs (`develop=1c921c47`, `work/r27-state-owner=33badf7d`), create isolated worktree `/tmp/opencode/w36-stateowner-reconcile-wt`.
2. ⏳ `git merge --no-edit origin/develop`; resolve conflict in `internal/deployment/deployment_store.go` keeping BOTH semantics.
3. ⏳ Resolve `cmd/baha/app_context.go` / `cmd/baha/target_test_helpers_test.go` writes if conflicted.
4. ⏳ Build + test green (both contracts).
5. ⏳ Push FF, ls-remote==head, ancestry rc=0, PR stays ready.
6. ⏳ Write this evidence, post END_DONE.

## TASK / CONTRACT

Merge the delivered **develop** contract (one-writer guard + `normalisePersistedOwner`)
into **work/r27-state-owner** (deployment-owner seam `VerifyDeploymentOwner`). Both touch
`internal/deployment/deployment_store.go` => CONFLICT. Requirement: keep BOTH semantiken
on the same load/save/list path — first ownership-verify, then one-writer-guard, ONE path,
never a second "either/or".

## CONFLICT RESOLUTIONS (per file:zone)

### Zone A: `internal/deployment/deployment_store.go` — imports + top-level decls
- **Decision:** keep BOTH sets. Keep `coreinstallation` import (state-owner) and keep
  `delivery` import already present (delivery). Add state-owner error vars
  (`ErrDeploymentOwnerMissing`, `ErrDeploymentOwnerForeign`, `TenantOwnerResolver`) AND
  keep delivery's `ErrConflictingOneWriter`, `ErrUnauthorizedMutation`. Keep delivery's
  `ObservedDeployment` fields (`Conflict`, `Owner`) — the state-owner side had reverted
  them; develop must win here because `refuseOneWriterMutation` reads `Observed.Conflict`
  and `Observed.Owner`.
- **Rationale:** The one-writer guard is structurally coupled to the `Observed` struct
  fields. Dropping them (state-owner's version) breaks develop's `refuseOneWriterMutation`.
  Add both error sentinels; no name clash.

### Zone B: `internal/deployment/deployment_store.go` — `SaveDeploymentRecord` body
- **Decision:** keep BOTH guards, ordered **owner-verify first, then one-writer guard**,
  on the same path, single early-return per failure.
- **Rationale:** delivery reads the persisted previous record (`loadPersistedOwnerForGuard`)
  to fix `guardOwner`/`guardRecord` and serialises `guardRecord`; state-owner needs the
  owner check at the seam before any directory/record is written. They are independent
  invariants (owner-ownership vs one-writer), so both must run; neither subsumes the
  other. Order = owner first (fail on wrong owner before even attempting the guard),
  then guard (fail on ambiguous writer).

### Zone C: `internal/deployment/deployment_store.go` — `LoadDeploymentRecord`
- **Decision:** prepend state-owner's `verifyDeploymentOwnerAtSeam(id.Target, id.DeploymentID)`
  check before `DeploymentRoot`; keep develop's body otherwise.

### Zone D: `internal/deployment/deployment_store.go` — `listDeploymentRecords`
- **Decision:** keep develop's body; add state-owner's `verifyDeploymentOwnerAtSeam` per
  deployment directory, routed through best-effort warnings (bestEffort) / hard error
  (non-best-effort), matching develop's existing best-effort pattern.

### Zone E: `internal/deployment/deployment_store.go` — retention block
- **Decision:** keep develop's `previousExists`-guarded retention (reads through full
  loader, fail-closed on unreadable/missing). State-owner side did not touch retention.

## POST-MERGE (to be filled after green build/tests)

- head SHA, conflicts resolved count, test run-ID / results, push confirmation, ancestry rc.

## BLOCKER (reconcile STOP — both semantics must be kept)

**CONFLICT UNRECONCILABLE on a Coreless target. END_BLOCKED.**

Both contracts put two independent, non-derivable invariants on the SAME load/save/list
path, and they contradict on a Coreless Target:

- develop (delivery) one-writer guard: intentionally **no** Core installation is required.
  Its own deliver tests (`one_writer_guard_test.go`, `preferences_retention_test.go`) seed
  Target `first` (a plain docker target) into an **empty** temp state dir — no
  `installation.json` — and assert the save/retain/vanish **succeeds**. Baseline on
  develop: all these PASS (verified: `TestOneWriterGuardPositiveDirectPasses`,
  `TestRetentionFirstSaveWithoutPreviousAllowed`, `TestRetentionVanishedRecordFailsClosed`,
  `TestCorruptedOwnerDirectPassesUnsetPathIsWideningNeutral` all PASS on develop).
  develop's `deployment_store.go` has **0** coreinstallation refs, **0** owner-verify calls.
- work/r27-state-owner seam (`verifyDeploymentOwnerAtSeam` -> `VerifyDeploymentOwner`):
  Coreless Target => `coreinstallation.Load` ENOENT => `ErrDeploymentOwnerMissing`
  (fail closed). State-owner seam tests PASS (11/11 incl.
  `TestDeploymentOwnerMissingOnExistingRecordSeam`, `TestDeploymentOwnerTenantBypassRemoved`).

Combined result: `go test ./internal/deployment -run '...Guard|Retention|...'` fails on
**19** develop tests (every Coreless-target seed now returns
`ErrDeploymentOwnerMissing` on the first save/retain). The state-owner tests still pass.

Why this is not a minimal-structure fix:
- Ordering alone cannot resolve it. Owner-verify-first keeps state-owner correct but
  breaks the 19 deliver tests (Coreless must SUCCEED for the one-writer guard to even run).
- One-writer-first keeps the 19 deliver tests but drops the state-owner fail-closed guard
  on the write path — that is softening the state-owner semantic, which the STOP rule
  forbids.
- `TenantOwnerResolver` is the only escape hatch, but it **fails closed by default**
  (`TestTenantOwnerResolverGrantOnly`) and the deliver tests never set it; Target `first`
  is a plain docker target, not an authorized Coreless tenant. Enabling a blanket tenant
  bypass to admit Coreless targets would weaken the one-installation-owner rule the state
  seam was built to enforce.

No semantic was softened. Both contracts preserved byte-for-byte; the contradiction is at
the semantic layer (Coreless-target success vs fail-closed), which is an Owner scope
decision, not a Worker edit.

## END
END_BLOCKED — w36-stateowner-reconcile: two contracts contradict on a Coreless target (deliver: Coreless save must SUCCEED; state-owner: Coreless must fail-closed with ErrDeploymentOwnerMissing). 19 develop deliver tests break in the combine. No minimal ordering/structure fix keeps both; TenantOwnerResolver fails closed by default. Owner scope decision needed. Evidence: evidence/r27-welle3-2026-11-03/state-owner/reconcile-1.md
