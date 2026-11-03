## r27 delivery-boundary — fix-r3 (serialization-bypass fix, lane w6-delivery-r5)

**Lane:** w6-delivery-r5 (Coordinator f49a3303). **Role:** WORKER.
**Base:** head `122ec956` (work/r27-delivery-boundary, r2 guard already landed).
**Candidate SHA:** `8463417589b26b75dae5d26f13bb96c2bc30ae13` (two commits on the shared branch, FF, remote confirmed via `git ls-remote`).
**Evidence path:** `baseharbor-plan/evidence/r27-night-2026-11-02/delivery-boundary/fix-r3.md`.

### Context

PR #1333 re-review `review-1333d.md` (Codex GPT-6, 2026-11-03) REJECTED head `122ec956`. Point 1: the guard reads the persisted previous owner into `guardRecord`, checks `guardRecord`, but the JSON write still serialised the caller-supplied `record` — so a forged/empty `Observed.Owner` was persisted and a later direct read bypassed the guard. Point 3: `Conflict` carry was not wired into the guard. This micro-fix is exactly those two pixels plus honest EN/DE docs.

### Root cause

`SaveDeploymentRecord` built `guardRecord` = copy of `record` with the canonical `guardOwner` set, evaluated `refuseOneWriterMutation(guardRecord)` correctly, then did `json.MarshalIndent(record, ...)` — the caller's value, not `guardRecord`. A delegated update with a caller-forged `Observed.Owner` persisted that forged owner; the next direct read saw the forged/empty owner and passed the guard. `guardRecord` also only inherited the caller's own `Conflict` (empty), never the persisted previous conflict, so a recorded two-active-owner conflict was silently dropped on the next same-owner write.

### Changes (candidate `84634175` vs base `122ec956`)

- `internal/deployment/deployment_store.go`:
  - `SaveDeploymentRecord` now serialises `guardRecord` instead of `record`, so the persisted owner is canonical and any carried `Conflict` is written. When the guard refuses a mutation the file is never written (store bytes unchanged).
  - The guard now carries a persisted-previous `Conflict` into `guardRecord` (`guardRecord.Observed.Conflict = true` only when `previous.Observed.Conflict`); a caller-supplied `Conflict` is never trusted.
- `internal/deployment/one_writer_guard_test.go` (new, all pass):
  - `TestForgedDelegatedUpdateThenDirectRefused`: seed external owner -> delegated update with caller-forged empty owner -> persisted owner stays canonical external -> subsequent direct (baseharbor) apply refused with `ErrUnauthorizedMutation`.
  - `TestRejectedWriteLeavesBytesIdentical`: seed external owner -> attacker direct write refused -> `os.ReadFile` bytes before == after (store untouched).
  - `TestPreviousConflictIsCarried`: hand-inject a conflict into the stored record -> same-owner update refused with `ErrConflictingOneWriter` (fail closed; conflict neither hidden nor cleared).
  - Positive direct/delegated happy paths (pre-existing) remain green.
- `docs/decisions/0022-...md` and `docs/de/decisions/0022-...md`: added a Scope / deferred-dependency section stating the invariant is enforced at record-save (`SaveDeploymentRecord`) and that cross-process active-reconciler observation is an explicit, not-yet-implemented dependency deferred until `t-20261018-r27-state-owner` + `t-20261018-r27-authority-contract` are accepted.
- `docs/spec/delivery-provider-v1.md` (EN) and `docs/de/spec/delivery-provider-v1.md` (DE): same scope/deferred note.
- No `.github/`, no `scripts/`, no `cmd/baha`.

### repo-rule compliance

- Write-set inside card: `internal/deployment/**` authorised + docs delivery-provider + 0022 EN/DE. Net diff 6 files; zero `.github`/`scripts`/`cmd` touches (`git diff --name-only 122ec956..84634175 | grep -E '^(\.github|scripts/|cmd/)'` is empty).
- FF push on the shared branch (no force), no merge (mission STOP).
- No hosted CI, no Run-Logs (mission).

### Verification (local, isolated)

```
go build ./...                                   # ok
TMPDIR=/tmp go test ./internal/deployment/ ./internal/delivery/ -count=1
   deployment: ok
   delivery:   ok
git diff --name-only 122ec956..84634175 | grep -E '^(\.github|scripts/|cmd/)'   # empty (CLEAN)
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-delivery-boundary
   8463417589b26b75dae5d26f13bb96c2bc30ae13   (confirmed post-push)
```

### Review-1333d compliance

1. **Resolved.** Per-resource authoritative owner = persisted previous record; owner resolved and checked only through `guardRecord`; forged/empty caller owner cannot mutate a persisted external owner; `Conflict` carried from the previous record into the guard and persistence; every conflict/unknown path fails closed (`ErrConflictingOneWriter`/`ErrUnauthorizedMutation`); regression = actual delegated-then-direct bypass + byte-identity of a refused write + carried conflict; direct/delegated happy paths green.
2. **Resolved (minimized).** EN/DE ADR + delivery-provider spec describe actual scope honestly (enforced at `SaveDeploymentRecord`); cross-process active-reconciler observation named explicitly as deferred; no non-taetliche runtime-lock claim.
3. Non-blocking history hygiene left to Coordinator.

**END lane DONE** — candidate `8463417589b26b75dae5d26f13bb96c2bc30ae13`, FF pushed, no merge. Two-attempt STOP not hit.
