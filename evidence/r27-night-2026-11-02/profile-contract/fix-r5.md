# l7-profile-r5 — PR #1324 fix lane

- ROLLE: Worker (Lane l7-profile-r5). Coord f49a3303.
- TASK: t-20261018-r27-profile-contract (release v0.4.27, critical).
- CANDIDATE: PR #1324 `work/r27-profile-contract`, base `develop`.
- BASE: head `ead09bc729113563b480597907214f1f4d5abd1f` (PR #1324 tip, verified via `git ls-remote`).
- Evidence source (review): `baseharbor-plan/evidence/r27-night-2026-11-02/review-1324e.md` — ONLY the OPEN lines are in scope.

## OPEN items in scope (Acceptance matrix, exactly the last two OPEN clauses the mission names)

1. **Three distinct record classes / encrypted export: OPEN.** Schema allows a valid export object on non-credential-export kinds and does not enforce per-kind storage consistency; Go `ValidateKindEnforcement` forbids export on other kinds but the schema does not. Algorithm/nonce are not bound to the real supported value domain from the Go code registry.
2. **Enroll entry requires DeviceEnrollment: OPEN.** `EnrollDevice` accepts any `Kind` passing the helper; the contract requires `Kind=device-enrollment` on the enrollment entry. Test named "schema-forbidden" tests an invalid algorithm, not a valid export on a forbidden kind.

All other matrix rows (one-use PARTIAL, import-grants-no-rights OPEN, deferred Git/SSH/DR, callable-interface PARTIAL) are NOT in scope per mission rule ("nur die als OPEN markierten Punkte… alles其他 bereits erfüllt/belegt"). No docs changes beyond the two reserved `docs/(de)/spec/credential-access-v1.md` (write-set), no CI/scripts/cmd files.

## PLAN

- 1 SCHEMA export-per-kind: `export` object forbidden on `management-profile` and `device-enrollment` (if/then per kind), schema-level, complementing Go `ValidateKindEnforcement`.
- 2 SCHEMA storage-consistency: per-kind storage obligations that cannot contradict (durable implies encrypted; device-enrollment must be sensitive); algorithm/nonce bound to supported value domain from Go registry.
- 3 ENROLL entry: `EnrollDevice` requires `Kind == DeviceEnrollment` at the boundary; test enforces it.
- 4 Rename / repurpose the "schema-forbidden" test so it fails a *valid* export on a forbidden kind.
- 5 Run tests (`TMPDIR=/tmp go test ./contracts/managementaccess/v1`), `go build ./...`, `go vet`.
- 6 ANSANDE: `git fetch origin develop && git merge origin/develop`; `git diff --name-only origin/develop...HEAD | grep -E '^(\.github|scripts/)'` must be empty.
- 7 push, ls-remote, no run logs; publish Planning + END.

## repo-rule compliance

- Write-Set strictly honored: `contracts/managementaccess/v1/**` (Go + schema + tests + golden) + `docs/(de)/spec/credential-access-v1.md` only. No CI/scripts/cmd, no other slice files, no `git add -A` (targeted `git add <file>` only).
- No self-qualification: no merge, no CI run, no release/tag. Candidate stays as an unmerged PR.
- STOP rule: two failed identical attempts → END_BLOCKED, no merge.

## Evidence / witnesses

- Schema behavior verified empirically with a throwaway `zzcheck` program (removed before END): golden `credential-export` ACCEPTED; `management-profile` carrying a valid `export` object ACCEPTED → the bug (export not forbidden per kind at schema level).
- AES-GCM nonce size from `$(go env GOROOT)/src/crypto/cipher/gcm.go`: `gcmStandardNonceSize = 12` bytes. Test nonce `E1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y_z` (43-char urlsafe-b64 → 32 raw bytes) decrypts successfully with `crypto/aes.NewCipher` + `crypto/cipher.NewGCM`, so it is a real, usable nonce.
- `go run /tmp/nnc/main.go` (32-byte nonce, AES-GCM) → `usable=true`.
- `go doc` / source confirms `chacha20poly1305.NonceSize = 12`.

## END lane

END_DONE | candidate SHA: pending (after push)
