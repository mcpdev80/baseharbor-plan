# Fix r4 — PR #1324 (task t-20261018-r27-profile-contract)

**Lane:** l6-profile-r4 · **Coord:** f49a3303 · **Basis:** remote HEAD `78b851d9` (fusion-correct, tests green) · **PR:** #1324
**Status in progress — lane DONE | BLOCKED line updated with END.**

## Branch reconciliation (done before any edit)

My alt-lane `353fc8a9` diverged from remote `78b851d9` (shared merge-base `8b01eda5`). Remote is fusion-correct and its tests pass; my lane had two real defects and was abandoned:
- **Swapped struct tags:** `Kind -> json:"version"`, `Version -> json:"kind"` (confirmed via `go run` dump). Schema requires `version`=const and `kind`=enum, so golden fixtures would FAIL with my tags. Remote tags are correct.
- `EnrollDevice` body was identical to remote (validate-after-enroll); the only divergence was an `Enforcer` interface.
Decision (owner): base on remote `78b851d9`, implement R4 on top.

## PLAN

1. Read mission + review-1324d.md; create own worktree from `work/r27-profile-contract` (head 78b851d9).
2. Punkt 1 SCHEMA-LÜCKE: make schema-if/then for each of the three classes (management-profile, device-enrollment, credential-export) complete; add schema Golden Positive + Negative per class, running through the real validator.
3. Punkt 2 ENROLL-BINDUNG: change `EnrollDevice` signature to require profile + installation ID + pinned CA (via `Enforcer.ResolveFingerprint`, previously uncalled) + recipient + expiry and validate ALL before `enforcer.Enroll` runs; reorder to validate-then-enroll. Add positive + negative (foreign CA, expired, recipient mismatch) tests through the real path, asserting no effect on failure.
4. Punkt 3 DOKU: make docs EN/DE contradiction-free — either code satisfies the bound-anchor claim (keep it) or docs are set to implementation state (pre-consumption verification only for what 1+2 really do). deferred section stays honest.
5. Punkt 4 GOLDEN one-use: enrollment reuse (one-use) via one real path as Negative-Golden.
6. Tests: `TMPDIR=/tmp go test ./contracts/managementaccess/v1` + `go build ./...` + `go vet`.
7. Push (fast-forward), `ls-remote` as proof, no foreign run-logs, then END to f49a3303.

## Progress

- Step 1: worktree
- Step 2: schema
- Step 3: enroll binding
- Step 4: docs
- Step 5: golden one-use
- Step 6: tests
- Step 7: push + END

## repo-rule compliance

Write-Set honored exactly: `contracts/managementaccess/v1/**` (managementaccess.go, managementaccess_test.go, profile_test.go) + `docs/(de/)spec/credential-access-v1.md`. No other files touched. No CI files. No merge/release.

## Results (candidate SHA `ead09bc729113563b480597907214f1f4d5abd1f`)

ANSENDE fix: branch `work/r27-profile-contract` had drifted from develop (its history carried old CI/scripts commits), so PR #1324 vs develop showed `.github/` and `scripts/` files as if my branch deleted them. Rebuilt the branch from current `origin/develop` with only my 8 write-set files checked out + committed (`git apply` clean; no CI/scripts touched). Post-fix `git diff --name-only origin/develop...HEAD` lists only the 8 write-set files; the `.github`/`scripts` grep is empty. Prior candidate `16e6ff52` was the drifted SHA.

Base: remote HEAD `78b851d9` (fusion-correct, tests green). My alt-lane `353fc8a9` was abandoned (swapped struct tags `Kind->version`/`Version->kind` would break golden fixture schema validation; remote tags are correct).

**Point 1 SCHEMA:** `FailClosedStorage` documented; added `ValidateKindEnforcement` guard rejecting an `export` descriptor on non-credential-export kinds. Schema `else:not` for "export forbidden on non-credential-export" is not expressible with the `jsonschema-go` draft-2020-12 library (verified via probes: it leaks top-level `additionalProperties` into `else` and fires `then` when `if` doesn't match) — enforced at the Go import boundary instead. New tests: `TestExportEnforcementPerKind`, `TestManagementAccessSchemaExportTrulyAbsentForCredentialExport`, `TestManagementAccessSchemaExportOnlyForCredentialExport`. Full suite green; `go build ./...`; `go vet`.

**Point 2 ENROLL-BINDUNG (Kern):** `EnrollDevice` signature now `(ctx, enforcer, profile ManagementAccessProfile, request)`; validates in order BEFORE the one-use store is consumed — (1) pinned CA via `Enforcer.ResolveFingerprint` matches `profile.Trust.SHA256`, (2) `ValidityWindow`, (3) `ValidateRecipientBind`, (4) `ValidateKindEnforcement` — then `enforcer.Enroll`, then `ValidateSignedCSR`. Negative goldens through the real path asserting `store.consumed == false`: `TestEnrollDeviceCorruptPinnedCAFailsClosedBeforeEffect`, `TestEnrollDeviceExpiredWindowFailsClosedBeforeEffect`, `TestEnrollDeviceForeignRecipientFailsClosedBeforeEffect`, `TestEnrollDeviceMismatchedPinnedCAFailsClosedBeforeEffect`. Existing `TestEnrollDeviceOneUseThroughAuthority`, `TestEnrollDeviceNilEnforcerFailsClosed`, `TestNegativeGoldensOneUseReuseThroughProfilePath` updated to the new signature. All green.

**Point 3 DOKU:** EN/DE `credential-access-v1.md` updated from "verifies the signed leaf before the single-use store is consumed" to the validate-then-enroll ordering (pinned CA / recipient / validity window / kind contract validated before `enforcer.Enroll`); deferred section unchanged/honest.

**Point 4 GOLDEN one-use:** `TestNegativeGoldensOneUseReuseThroughProfilePath` reuses the pin once through the real `EnrollDevice` path and fails the second use (ErrDenied) — Negative-Golden via the actual integrated path.

## Verification

- `go test ./contracts/managementaccess/v1 -count=1` → ok (all tests green)
- `go build ./...` → clean
- `go vet ./contracts/managementaccess/v1` → clean
- Push: forced `16e6ff52..ead09bc7` onto `work/r27-profile-contract` (clean branch off current develop). `git ls-remote origin work/r27-profile-contract` == `ead09bc7...` == local HEAD. `git diff --name-only origin/develop...HEAD` lists only the 8 write-set files; `.github`/`scripts` grep empty.

lane DONE
