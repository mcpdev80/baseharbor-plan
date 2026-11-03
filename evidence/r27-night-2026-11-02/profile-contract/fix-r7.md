# l9-profile-r7 — PR #1324 closing lane

- ROLLE: Worker (Lane l9-profile-r7). Coord f49a3303.
- TASK: t-20261018-r27-profile-contract (release v0.4.27, critical).
- CANDIDATE: PR #1324 `work/r27-profile-contract`, base `develop`.
- BASE: head `593da4d9e5eeb8bbb721a3908618fac673fa1e1e` (verified via `git ls-remote`).
- Review basis: `baseharbor-plan/evidence/r27-night-2026-11-02/review-1324g.md` (REJECT, only the closeable lines) + board "Coordinator crypto decision on profile nonce (2026-11-03, r1324g)" and "Coordinator scope decision on profile integration depth (2026-11-03, r1324f)" — crypto decision is authoritative: AES-256-GCM, 12 random bytes, base64url without padding = 16 chars, canonical.

## END lane DONE | candidate SHA: `66c546390e4d41e6beb4e1b225f354f324405d2d` (PR #1324 `work/r27-profile-contract`, base develop) — verified via `git ls-remote`.

## PLAN

- 1 CRYPTO: algorithm restricted to `aes-256-gcm` (chacha20-poly1305 removed as an accepted value in v1); nonce pattern `^[A-Za-z0-9_-]{16}$`, decoded to exactly 12 bytes, canonical base64url (full octet count). Schema, Go helper (reject wrong length + non-canonical), golden, EN, DE all state THIS rule consistently.
- 2 IMPORT WITNESSES: three local fakes with counters (grant-registry / plugin-loader / credential-destination); accepted input => all counters zero; each negative axis (grant=true, plugin=true, redirect=true) fails closed at the real boundary before any witness; rejected input => zero side effects (before/after counter compare).
- 3 DOKU-PRESENT-TENSE: EN+DE `EnrollDevice` paragraph rewritten to self-bind (compares profile's pinned CA hash to its own cert hash; a self-consistent foreign CA passes the self-bind; independent anchor check deferred). DE targetenrollment-reuse-satz removed (aligned to EN). EN+DE nonce invariant updated to AES-256-GCM 12-byte / 16-char rule.
- 4 ANSANDE: merge origin/develop; `git diff --name-only origin/develop...HEAD | grep -E '^(\.github|scripts/|cmd/)'` empty.
- 5 CONTENT-PARITAET: `git diff --name-only origin/develop...HEAD` == write-set files only.
- 6 TESTS: `TMPDIR=/tmp go test ./contracts/managementaccess/v1` ok; `go build`/`go vet` rc=0; documentation-audit + DE integrity pass.
- 7 push FF, ls-remote, END to f49a3303.

## repo-rule compliance

- Write-Set strictly honored: `contracts/managementaccess/v1/**` (Go + schema + tests + golden) + `docs/(de)/spec/credential-access-v1.md` only. No CI/scripts/cmd/anchor files, no other slice files, no `git add -A` (targeted `git add <file>` only).
- Three commits (mission SCHRITTE = 3): 1) crypto nonce contract, 2) import side-effect witnesses, 3) docs present-tense.
- No self-qualification: no merge (other than develop base), no CI run, no release/tag/PR-push beyond push FF.
- STOP rule honored: two failed identical attempts => END_BLOCKED, no merge.

## Evidence / witnesses

- Nonce decode: golden `4fIDBAUGBwgJCgsM` -> 12 canonical bytes (16 base64url chars, no padding). `python3` check: 12 bytes, canonical re-encode equals itself.
- Crypto round-trip: real AES-256-GCM stdlib `cipher.NewGCM` seal+open round-trip passes; wrong key fails (GCM tag mismatch); wrong-length and non-canonical values fail the contract.
- Import witnesses: `TestImportSideEffectsZeroForAcceptedInput` (management-profile + credential-export, all three counters stay 0) and `TestImportSideEffectsRejectedInputNeverReachesWitnesses` (all 3 flags x 2 kinds fail closed, counters 0).
- Docs: `bash scripts/documentation-audit.sh` PASS (all sections); `python scripts/check_de_translation_integrity.py` PASS (159 paired pages); `python scripts/check_docs_locale_parity.py` PASS (159 pages).
- CI: none (candidate stays an unmerged PR; no run-logs).

## END lane

END_DONE | candidate SHA: `66c546390e4d41e6beb4e1b225f354f324405d2d` (PR #1324 `work/r27-profile-contract`, base develop) — verified via `git ls-remote`.

- Commit `66c54639` scoped to write-set only (3 commits: Go + schema + golden + 2 new test files; EN + DE docs). `git diff --name-only origin/develop...HEAD | grep -E '^(\.github|scripts/|cmd/)'` -> EMPTY.
- Tests: `TMPDIR=/tmp GOCACHE=/tmp/bh-l9-gocache GOPATH=/tmp/bh-l9-gopath go test ./contracts/managementaccess/v1` -> ok; `go build ./...` rc=0; `go vet ./contracts/managementaccess/v1` rc=0.
- ANSANDE: `git fetch origin develop && git merge --ff-only origin/develop` (already up to date); reserved-file diff empty vs develop.
- push FF: `593da4d9..66c54639`, `git ls-remote` -> `66c546390e4d41e6beb4e1b225f354f324405d2d refs/heads/work/r27-profile-contract`.
- No merge of PR / CI-run / release-tag (candidate stays an unmerged PR).
- No CI/scripts/cmd/anchor files; write-set strictly honored.

### Scope closure per review-1324g point

1. **Nonce consistency / crypto validity (REJECT -> closed).** Committed AES-256-GCM as the only AEAD in v1. nonce pattern `^[A-Za-z0-9_-]{16}$`, decodes to exactly 12 bytes, canonical base64url. Schema + Go `nonceIsAes256Gcm` (rejects non-canonical trailing bits + wrong length) + golden (`4fIDBAUGBwgJCgsM`) + EN + DE all state this consistently. Executable round-trip test proves AES-256-GCM seal/open; negatives: wrong-length, non-canonical, wrong-key, unknown-algorithm. chacha20-poly1305 OUT (removed from schema enum + Go accept-list + doc comments).
2. **Export kind / whitelist (addressed in r6, reinforced here).** `aes-256-gcm` is the sole algorithm enum; `ValidateKindEnforcement` rejects any other algorithm.
3. **Import side-effect witnesses (REJECT -> closed).** Three real fakes with counters around the genuine import boundary (`ValidateKindEnforcement`). Positive: accepted management-profile + credential-export produce zero grant/plugin/credential-redirect side effects (before/after counter equality). Each negative axis fails closed before any witness is reached.
4. **Deferred independent authority / present-tense claims (REJECT -> corrected).** `EnrollDevice` paragraph now says it SELF-BINDS (compares the profile's pinned CA hash to the fingerprint of the certificate it supplies; a self-consistent foreign CA passes this self-bind; independent anchor check deferred). Removed the misleading "rejects a foreign CA before token use" claim and the DE-only "targetenrollment-reuse" sentence. EN+DE deferred sections still link r27-authority-contract + r27-state-owner and assert no present verification.
