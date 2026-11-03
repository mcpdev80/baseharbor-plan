# Fix r9 — PR #1324 final 3 Fix-Points (t-20261018-r27-profile-contract)

Lane: l11-profile-r9 (Worker). Coord: f49a3303 (Codeman). Base: faca47d6 = head faca47d6.
Evidence lane: baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/fix-r9.md
Source: coordinator/missions/l11-profile-r9.txt + review-1324i.md (REJECT) + card section.

Strategy-change (mission): the Witness-behavioral part is NOT tested — it is formally deferred
(card section "Coordinator decision on import side-effect clause"). NO new orchestration
construction. Scope = remove witness TEST + fix golden-nonce AEAD + doc links. No new interface,
no production claim. STOP: no merge/release.

## PLAN

1. Point 1 — remove witness TEST (import_witness_test.go); no new orchestration construction; mission defers witness behavioral test.
2. Point 2 — NONCE: AEAD roundtrip with the DECODED GOLDEN nonce (not newly generated); each negative variant gets its OWN fresh baseline profile (deep copy before mutation, no pointer sharing).
3. Point 3 — DOCS EN+DE: ../../tasks/... links replaced by official Planning destination (card filename in text, no path link, verified); self-bind/deferral phrasing already present.
4. Ansende — merge origin/develop; diff grep -E '^(\.github|scripts/|cmd/)' empty; 9-10 write-set files. Tests TMPDIR=/tmp go test ./contracts/managementaccess/v1 + go build/vet. Push FF, ls-remote, END at f49a3303.

## Status by point

- Point 1 (witness TEST): DONE. Deleted contracts/managementaccess/v1/import_witness_test.go (review-1324i says it proves test-authored no-op behavior, not import orchestration; mission explicitly defers the witness behavioral test, no new orchestration construction). Replaced the witness-driven TestImportSideEffectsWitnessed in managementaccess_test.go with a schema/contract-only check at the real fail-closed boundary ValidateKindEnforcement (clean golden records validate with zeroed ImportCapability; any true import flag fails closed) — NO side-effect claim. No leftover references (grep clean). No new orchestration function.
- Point 2 (nonce golden AEAD roundtrip): DONE. Added TestNonceGoldenAEADRoundtripWithDecodedGoldenNonce (seals/opens a blob with the bytes of the DECODED golden nonce "4fIDBAUGBwgJCgsM" -> 12 bytes, proving the golden is a real AEAD nonce end-to-end) and TestNonceContractRejectsNegativeVariantsWithFreshBaselineProfiles (each negative variant — invalid alphabet, padding char, 15-char, 17-char — starts from its OWN fresh, fully valid baseline profile; Export descriptor copied fresh before mutation, no shared pointer). Golden baseline validates first. No new interface.
- Point 3 (docs EN/DE): DONE. Both EN and DE still defer the independent anchor as "future work" (self-bind/recipient-window phrasing only) — verified at HEAD. Replaced the two broken ../../tasks/t-20261018-r27-authority-contract.md and ../../tasks/t-20261018-r27-state-owner.md links with the official Planning destination https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/<card>.md (card filename in text, no path link) in BOTH files. Verified with git cat-file that no ../../tasks link remains anywhere in docs/; new links resolve (curl raw.githubusercontent -> HTTP 200 for both task files). No new production claim.
- Ansende: DONE. No merge (STOP: no merge/release; PR #1324 already at HEAD faca47d6 — I did not merge, only pushed my branch-internal fix commit). diff vs my base faca47d6 restricted to .github/scripts/cmd is empty (zero touched); exactly 5 write-set files (contracts/managementaccess/v1/** + docs/(de/)spec/credential-access-v1.md). go build ./... ok, go vet ./contracts/managementaccess/v1 ok, go test ./contracts/managementaccess/v1 ok (20 tests pass, incl. 2 new).

## Evidence

- go test ./contracts/managementaccess/v1: ok (all 20 pass, incl. TestNonceGoldenAEADRoundtripWithDecodedGoldenNonce + TestNonceContractRejectsNegativeVariantsWithFreshBaselineProfiles; witness tests gone).
- go build ./... : ok. go vet ./contracts/managementaccess/v1 : ok.
- Ansende write-set: exactly 5 files vs base faca47d6 (import_witness_test.go deleted; managementaccess_test.go, nonce_crypto_test.go, docs/spec/credential-access-v1.md, docs/de/spec/credential-access-v1.md modified). Zero .github/scripts/cmd files.
- Link integrity: grep -rn '\.\./\.\./tasks/' docs/ -> none; new Planning links curl 200.
- Committed c50747a5 on work/r27-profile-contract; pushed FF to origin. git ls-remote confirms remote head c50747a5fe2a548a16cba70e597cf5f42de4ced7 on refs/heads/work/r27-profile-contract.
- Vulnerability notice on push is a pre-existing dependabot advisory on baseharbor's default branch, unrelated to this change.

## EN DONE / END BLOCKED

END_CODE_READY — all 3 recipes applied/verified, all tests green, zero .github/scripts/cmd changes, doc links fixed and verified, pushed FF. No merge (STOP: no merge/release; candidate branch work/r27-profile-contract at c50747a5, PR #1324 already at HEAD faca47d6). Candidate SHA: c50747a5fe2a548a16cba70e597cf5f42de4ced7 on work/r27-profile-contract.
