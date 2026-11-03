# l8-profile-r6 — PR #1324 fix lane

- ROLLE: Worker (Lane l8-profile-r6). Coord f49a3303.
- TASK: t-20261018-r27-profile-contract (release v0.4.27, critical).
- CANDIDATE: PR #1324 `work/r27-profile-contract`, base `develop`.
- BASE: head `e57ecf89a3a0dbbac8a691a0c01b6e866789faa6` (verified via `git ls-remote`).
- Review basis: `baseharbor-plan/evidence/r27-night-2026-11-02/review-1324f.md` (REJECT, only the closeable lines) + board "Coordinator scope decision on profile integration depth (2026-11-03, r1324f)" — IN-SCOPE vs DEFERRED is authoritative there.

## IN-SCOPE items (exakt diese, mission + board scope decision)

1. NONCE-WAHRHEIT: 43 base64url chars = 32 bytes (verified `python3 -c 'import base64; ...'`). Document the actual wire format consistently across schema + EN + DE + golden fixture — OR commit to an agreed value.
2. TEST `TrulyAbsent...`: the export object is genuinely omitted (not only the algorithm removed).
3. `ValidateKindEnforcement`: algorithm/nonce bound to the schema whitelist (no arbitrary nonempty); combined schema+Go import test (positive + one negative per axis).
4. SIDE-EFFECT WITNESSES for import: no grants / no plugin execution / no redirect through the real import entry, before/after state.
5. DE Doku: remove the stale `targetsession` assertion, align to EN, correct doc-links.
6. DEFERRED-TEXT (instead of false present-tense claims): EN+DE "Enforced later, with" section — independent anchor + installation/scope binding + production consumer hang on t-20261018-r27-authority-contract + t-20261018-r27-state-owner (unaccepted, same files). No sentence claiming the profile path verifies them now.

## PLAN

- 1 NONCE: fix schema `nonce` pattern (43 base64url), golden nonce, EN nonce wording, DE nonce wording — all identical, all 43-char/32-byte.
- 2 TRULY-ABSENT: rename `TestManagementAccessSchemaExportTrulyAbsentForCredentialExport` so the export object is deleted from the map entirely (present=false), schema rejects.
- 3 WHITELIST: `ValidateKindEnforcement` restricts `Algorithm` to the schema enum and `Nonce` to 43-char base64url; add combined positive + negative(algorithm,nonce) Go import test.
- 4 SIDE-EFFECT: prove `import.{rights_granting,plugin_execution,credential_redirect}` all false (already FailClosedImport) through the real entry with before/after witness; document that no production import entry exists for credential-export — the only wired entry is `EnrollDevice` (device-enrollment).
- 5 DE: remove `targetsession` reuse sentence, align wording to EN, fix doc-links.
- 6 DEFERRED-TEXT: EN+DE "Enforced later, with" for independent anchor + installation/scope binding + production consumer; delete any present-tense "verifies now" claim.
- 7 ANSANDE: merge origin/develop; `git diff --name-only origin/develop...HEAD | grep -E '^(\.github|scripts/|cmd/)'` must be empty.
- 8 Tests: `TMPDIR=/tmp go test ./contracts/managementaccess/v1`, `go build ./...`, `go vet`.
- 9 push FF, ls-remote, no run-logs; publish Planning + END.

## repo-rule compliance

- Write-Set strictly honored: `contracts/managementaccess/v1/**` (Go + schema + tests + golden) + `docs/(de)/spec/credential-access-v1.md` only. No CI/scripts/cmd/anchor files, no other slice files, no `git add -A` (targeted `git add <file>` only).
- No self-qualification: no merge (other than develop base), no CI run, no release/tag/PR-push beyond push FF.
- STOP rule: two failed identical attempts → END_BLOCKED, no merge.
- Scope discipline: DEFERRED items documented (not silent, not converted to implemented claims).

## Evidence / witnesses

- Nonce decode: `python3 -c 'import base64; n="E1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y_z"; print(len(n), len(base64.urlsafe_b64decode(n+"="*((4-len(n)%4)%4))))'` → `43 32`.
- No production consumer: `grep -rln "managementaccess" --include="*.go" internal/ contracts/ | grep -v managementaccess/v1/` → empty. Only wired entry is `EnrollDevice`.

## END lane

END_DONE | candidate SHA: `593da4d9e5eeb8bbb721a3908618fac673fa1e1e` (PR #1324 `work/r27-profile-contract`, base develop) — verified via `git ls-remote`.

- Commit `593da4d9` scoped to write-set only (6 files: Go + schema + tests; EN + DE docs). `git diff --name-only origin/develop...HEAD | grep -E '^(\.github|scripts/|cmd/)'` → EMPTY.
- Tests: `TMPDIR=/tmp GOCACHE=/tmp/bh-r6-gocache go test ./contracts/managementaccess/v1` → ok; `go build ./...` rc=0; `go vet ./contracts/managementaccess/v1` rc=0.
- ANSANDE: `git fetch origin develop && git merge origin/develop` (already up to date); reserved-file diff empty.
- push FF: `e57ecf89..593da4d9`, `git ls-remote` → `593da4d9e5eeb8bbb721a3908618fac673fa1e1e refs/heads/work/r27-profile-contract`.
- No merge of PR / CI-run / release-tag (candidate stays an unmerged PR).
- No CI/scripts/cmd/anchor files; write-set strictly honored.

### Scope closure per item

1. NONCE-WAHRHEIT: 43 base64url = 32 bytes (verified decode). Schema `description` + EN + DE invariant + DE invariant all state 43-base64url/32-byte; golden nonce unchanged (already 43-char, 32-byte). Consistent across schema/EN/DE/fixture.
2. TEST `TrulyAbsent...`: `TestManagementAccessSchemaExportTrulyAbsentForCredentialExport` now deletes the `export` key entirely (present=false); schema rejects (passes).
3. `ValidateKindEnforcement`: algorithm restricted to `{aes-256-gcm, chacha20-poly1305}` (new constants), nonce restricted to 43-char base64url (new `nonceIsBase64Url43` helper); `TestCredentialExportCombinedSchemaAndGoImport` proves positive + negative algorithm + negative nonce through BOTH gates.
4. SIDE-EFFECT: `TestImportSideEffectsWitnessed` proves the valid golden records pass the real import boundary (`ValidateKindEnforcement`) with all three import flags false (no grant/plugin/redirect), and any true flag fails closed at the boundary before any effect. Documented that no production import entry exists for credential-export (only wired entry is `EnrollDevice`).
5. DE Doku: removed stale `internal/targetsession` reuse claim (aligns to EN's `internal/targetenrollment`); nonce wording aligned; doc-links corrected to `t-20261018-r27-authority-contract` + `t-20261018-r27-state-owner`.
6. DEFERRED-TEXT: EN + DE anchor/installation/scope binding bullet now reads "enforced later, with" + names both unaccepted cards; added explicit "no claim asserts this path verifies them now" / "Keine Aussage ... prüft" — no present-tense enforcement claim survives.
