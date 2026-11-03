# Fix r8 — PR #1324 last 3 craft points (t-20261018-r27-profile-contract)

Lane: l10-profile-r8 (Worker). Coord: f49a3303 (Codeman). Base: 66c54639.
Evidence lane: baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/fix-r8.md

## PLAN

1. Point 1 — nonce test correctness: fully valid baseline profile; invalid alphabet / padding char / wrong length (15/17) => reject; valid 16-char variants => accept; decoded golden via real AEAD roundtrip; unknown-algorithm with valid profile (no masking). No "changed first char = noncanonical" claim.
2. Point 2 — import witnesses: wire fakes to a real injected orchestration boundary (package-internal importProfile/prof, grants, plugins, credDir); accepted input untouched (counter unchanged), rejected input rejects + untouched. New orchestration function allowed (testable, no production consumer claim). Existing deferral text stays.
3. Point 3 — doc contradiction: EN+DE paragraphs claiming installation-ID binding / validated-through-anchor now reflect self-bind reality (reference deferral); verify DE negations. No new production claims.
4. Ansende: merge origin/develop; diff grep -E '^(.github|scripts/|cmd/)' empty; write-set parity. Tests all green, build/vet. Push FF, ls-remote.

## Status by point

- Point 1: DONE. Rewrote TestNonceContractRejectsNonCanonicalAndWrongLength -> TestNonceContractRejectsInvalidAlphabetPaddingWrongLength (invalid alphabet, padding, 15/17 => reject) + added TestNonceContractAcceptsValid16CharVariants (valid 16-char variants accepted; changed first char = different valid 12-byte nonce, NOT noncanonical). Fixed TestNonceUnknownAlgorithmFailsClosed to use a fully valid baseline (no masking) and assert a supported-algorithm baseline validates first. Fixed misleading "43 chars/32 bytes" comments in profile_test.go and schema description. All go test ./contracts/managementaccess/v1 green.
- Point 2: DONE. Added package-internal Export: ImportProfile(orc importOrchestrator, profile) orchestration seam in managementaccess.go; importWithWitnesses now fakes through ImportProfile via the injected importOrchestrator.Import (fail-closed check + no channel touched). Before/after counter per axis for accepted AND rejected input. Tamper check proved witnesses are genuinely reached (incrementing a counter in Import makes the test fail). No production claim; deferral text present.
- Point 3: DONE at HEAD. EN+DE self-bind reality already reflects deferral at 66c54639; nonce claim EN/DE parity verified (12 random bytes / 16 base64url chars); DE negations consistent. No doc change needed.

## Evidence

- go test ./contracts/managementaccess/v1: ok (all pass, incl. new nonce tests + witness tests).
- go build ./... : ok. go vet ./contracts/... : ok.
- Tamper proof: incrementing w.loader.plugins in Import -> TestImportSideEffectsZeroForAcceptedInput FAILS with "unexpected side effects before={grants:0 plugins:0 redirects:0} after={grants:0 plugins:1 redirects:0}", proving the witnesses are reached through the orchestrator, not disconnected.
- Committed faca47d6 on work/r27-profile-contract (merge origin/develop already up to date). Pushed FF; git ls-remote confirms remote head faca47d6. diff vs origin/develop: 5 files in write-set (contracts/managementaccess/v1/** + docs/(de/)spec/credential-access-v1.md parity); zero .github/scripts/cmd files.

## EN DONE / END BLOCKED

END_CODE_READY — all 3 recipes applied/verified, all tests green, no CI/cmd/scripts changes. No merge (no production consumer; PR #1324 already at HEAD). Candidate SHA: faca47d6d6494f2eac6d4565c6c2bc47f735e0e0 on work/r27-profile-contract.
