# CODEX-REVIEW — PR #1386, round 2 (read-only)

Verdict: **ACCEPT** — exact candidate `aa62518c6a65c207db5a0b49e37d03ca470c7b26`; merge-ready for owner round.

## Identity, resolver, and scope

PR #1386 is open, ready, and based on `develop`; the API head equals the requested SHA. `ls-remote` reports `develop=24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and `work/r27-connection-authority=aa62518c6a65c207db5a0b49e37d03ca470c7b26`. Develop is an ancestor. The exact name-only diff is the two reserved files:

```
internal/coreinstallation/authority.go
internal/coreinstallation/w168_boundary_probe_test.go
```

Resolver-path grep plus source inspection finds no `EnsureLocalIssuer` call, `Mkdir`, write, or certificate-creation call. `ResolverForTargetSelection` calls `observeLocalIssuer`, whose only preflight is read-only `serviceaccess.CheckLocalIssuer`; the returned `LocalIssuer` reads its existing key/certificate on demand. The `EnsureLocalIssuer` occurrences in `authority.go` are explanatory comments only. The existing consumer-path blobs match develop and round 1 exactly:

| Consumer file | Blob at develop and candidate |
| --- | --- |
| `cmd/baha/use_target.go` | `63bbd4015bdf514f8a4a6ff3b5ff34439a9f7dc6` |
| `cmd/baha/target.go` | `675215650d738465e7343d63c3eadc8c02d87184` |
| `cmd/baha/target_activate_wizard.go` | `10a88ad383a55ca9f2c9e0f3ae3edbcf1fcd5ecf` |
| `cmd/baha/application_management_dependency.go` | `3c28bb06129535772abb359c0f117824a61c3c29` |
| `cmd/baha/application_service_issuer.go` | `1c713bed24310aeb34ff88edcb8895494e66eefd` |

## Four independent fail-closed probes

At the exact head I ran the checked-in unverified-installation, foreign-target, unreadable-root, absent-issuer-directory, and empty-issuer-directory tests; all passed. I also ran a temporary independent four-case probe that checks the requested cells and their filesystem effects:

| Probe | Result |
| --- | --- |
| Unverifiable installation with empty target root | `ErrUnverifiableInstallation`; no issuer directory created |
| Foreign target root | `ErrForeignTarget`; pre-existing issuer bytes unchanged |
| Verified installation, issuer directory absent | `ErrUnverifiableInstallation`; directory remains absent |
| Verified installation, zero-byte `issuer.pem` | `ErrUnverifiableInstallation`; file remains zero bytes, no replacement material |

All four temporary probes passed. This specifically checks a zero-byte `issuer.pem`; the checked-in test named `TestResolverFailsClosedOnEmptyIssuerFile` creates an empty issuer directory without a file, so the additional probe covers the literal empty-file case.

## Failed-creation mutant

In the disposable exact-head worktree I restored the old creation behavior at the resolver call site by replacing `observeLocalIssuer(issuerDir)` with `serviceaccess.EnsureLocalIssuer(issuerDir)`. `TestResolverFailsClosedOnAbsentIssuerDir` then went **red** (rc 1): it received nil instead of `ErrUnverifiableInstallation` and observed that the issuer directory had been created. I restored the candidate source; the worktree is clean. The mutant therefore proves the new fail-closed probe detects the original authority-creation defect.

## Gates

Run `41988118382` is terminal success at the exact candidate SHA. `PR Selected Checks` is **success**, not skipped; focused authority-package tests, CLI build/guided tests, vet, source format, trusted plan, and source checks passed. Runtime and unrelated consumer checks were skipped by selection.

No PR, branch, merge, comment, or card action was taken.
