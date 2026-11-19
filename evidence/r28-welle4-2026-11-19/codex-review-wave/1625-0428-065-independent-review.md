# Independent read-only review — PR #1625 / 0428-065

Reviewed 2026-11-19.

- PR is open and Draft at head `da7a4e62cda17bcc167cd659c24f81bdff9f0d15`, based on `cli2-identity-secrets-head` (`f93564a0d707983bfe6a8b59375c1c1c914d7827`), itself an open stack entry (#1615).
- Current exact head has no checks/statuses and zero PR workflow runs. Rebase and exact-head checks are still required.

## Finding — advertised managed-secret export is unavailable

`cmd/baha/app_export.go:273-275` implements `managedSecretScopePresent` as unconditional `(false, nil)`. `collectExportEntries` (`:279-298`) handles only `local.developer-credentials`; it never collects `secrets/openbao`. Thus managed secret export can never become available or produce entries. The current test covers unauthenticated denial, not a successful authorized export. Also, interactive selection occurs after `authorizeExport`, so a managed-secret source selected in the prompt would not be authorized after selection.

Do not accept/merge until the intended managed-secret path is implemented or removed from the advertised contract, a positive authorized-path test exists, authorization is performed for the selected scope, and exact-head CI runs.

No PR/product files, comments, claims, or merge state were changed by this review.
