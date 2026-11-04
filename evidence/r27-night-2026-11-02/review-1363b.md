# CODEX-REVIEW — PR #1363, round 2

- Candidate: `e45e85ed5f22ca7ff51b811174fc0161ffbba701` (reviewed SHA exact)
- Base: `ecbb88545f96473986f8f41394cffce58b97d2df`
- Verdict: **REJECT**
- Role: REVIEW only; no approval or merge.

## Findings

1. **Secret canary is not checked across all serialized fields.** In `contracts/managementaccess/v1/store.go:443-458`, `scanContainerSecrets` checks `DestPath` and each record's `Recipient` only. At `store.go:783-790`, `scanRecordSecrets` checks only installation ID, recipient, and scope. `ExportToContainer` calls the former (`store.go:405-411`), so a secret marker in another serialized string field can be returned in export bytes. The test `contracts/managementaccess/v1/store_test.go:291-312` places its canary in `Scope` and only asserts that a later import fails; it does not assert export rejection. This contradicts the spec's “scans every serialized field” claim.

2. **Import commit is not atomic and there is no failed-write rollback probe.** `contracts/managementaccess/v1/store.go:738-747` writes directly to the final `commitPath` with `os.WriteFile`, then removes it only if the call returns an error. A partial/truncated final file can therefore be visible during the write and rollback is not guaranteed. `contracts/managementaccess/v1/store_test.go:470-492` tests detecting a deliberately corrupted pre-existing file on reopen, not a short write or failed commit. This does not establish the documented transactional/atomic guarantee.

The remaining reviewed probes were partial: unknown outer/nested fields and wrong version/installation/scope are rejected; replacement verifies the resulting record. Canonical round-trip checks only selected fields and does not compare full records or golden re-encoding. Trust self-consistency is conditional on `ExpectedBinding.TrustSelfConsistent` (`store.go:76-79`, `store.go:679-682`), so it is not enforced by default. The current hosted run `41849617084` also showed `documentation-audit` and `PR Selected Checks` failed. These are additional acceptance gaps; the two findings above independently require rejection.

## REZEPT

- **Datei:** `baseharbor/contracts/managementaccess/v1/store.go`; Tests in `baseharbor/contracts/managementaccess/v1/store_test.go`.
- **Änderung:** Scan every serialized field in the complete export/import record (with an explicit allowlist only for values that are proven safe), and reject before export bytes are returned or written. Replace direct final-path `os.WriteFile` with same-directory staging, complete-write verification, sync/close and atomic rename; remove staged artifacts on every failure. Define replacement cleanup failure behavior rather than ignoring it.
- **Testanforderung:** Inject a genuine canary independently into each serialized field category and prove `ExportToContainer` rejects it before exposing bytes. Add deterministic short-write/commit-failure injection and assert no partial final file or temp artifact remains. Verify successful replacement leaves the expected sole record. Run package tests, build, vet, gofmt, then required hosted checks through terminal green, including documentation audit and selected checks.
- **Stop-Kriterium:** Stop/reject if any serialized secret canary is returned/persisted, any failed commit leaves a final or staged partial artifact, replacement can leave ambiguous duplicate state, or any required CI gate is not terminal green on the reviewed candidate SHA.

## Review boundary and END

Read-only review of exact candidate `e45e85ed5f22ca7ff51b811174fc0161ffbba701`; no source mutation, approval, or merge. `END_DONE codex-r1363b: verdict=REJECT open=secret-scan,atomic-import,trust-binding,canonical-proof,hosted-gates | Secret coverage and transactional commit are not established on candidate e45e85ed.`
