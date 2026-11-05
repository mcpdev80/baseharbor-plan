# CODEX-REVIEW — PR #1386 (read-only)

Verdict: **REJECT** — exact candidate `b730243cbe100387db5ce89611028a3487a89894`.

## Identity, scope, and gates

The PR is open, ready, based on `develop`, and its API head equals the requested SHA. `ls-remote` reports `develop=24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and `work/r27-connection-authority=b730243cbe100387db5ce89611028a3487a89894`. The candidate has the current develop commit as its parent. Its exact diff contains only the two card-reserved files: `internal/coreinstallation/authority.go` and `internal/coreinstallation/w168_boundary_probe_test.go`.

The requested resolver takes verified installation state and a target-state root; it takes no application/workload context. The existing consumer-path blobs are identical between develop and this head:

| Consumer file | Blob at develop and candidate |
| --- | --- |
| `cmd/baha/use_target.go` | `63bbd4015bdf514f8a4a6ff3b5ff34439a9f7dc6` |
| `cmd/baha/target.go` | `675215650d738465e7343d63c3eadc8c02d87184` |
| `cmd/baha/target_activate_wizard.go` | `10a88ad383a55ca9f2c9e0f3ae3edbcf1fcd5ecf` |
| `cmd/baha/application_management_dependency.go` | `3c28bb06129535772abb359c0f117824a61c3c29` |
| `cmd/baha/application_service_issuer.go` | `1c713bed24310aeb34ff88edcb8895494e66eefd` |

Run `41981375241` is terminal success at this exact SHA. The focused authority-package tests, CLI build, guided CLI tests, vet, source contracts/format, trusted plan, and `PR Selected Checks` all pass; `PR Selected Checks` is success.

## Fail-closed checks and counter-probe

At the exact candidate I ran `go test ./internal/coreinstallation -run 'TestResolver|TestResolveIntegrationOnHead' -count=1 -v`; all five resolver/integration tests passed. The suite covers unverified installation, foreign target, unreadable installation root, and a valid target.

An additional disposable counter-probe started with a verified installation and an empty issuer directory, called the resolver, and asserted no authority file was created. It **failed**: the resolver returned success and created `service-access/issuer/issuer.pem`. The cause is `authority.go:352`, which calls `serviceaccess.EnsureLocalIssuer`. `EnsureLocalIssuer` generates and persists a new CA when `issuer.pem` is absent (`internal/serviceaccess/local_issuer.go:59` onward). This is authority creation during resolution, despite the resolver's read-only/derive-only contract comments and the existing consumer path's separation between `CheckLocalIssuer` and the expressly authorized materialization phase (`cmd/baha/application_service_issuer.go:74-79`). A missing authority therefore does not fail closed; selection can silently create a new trust root.

## Recipe

- **Files:** `internal/coreinstallation/authority.go` and `internal/coreinstallation/w168_boundary_probe_test.go`.
- **Change:** make target selection resolution read-only. Open/observe the existing issuer without calling `EnsureLocalIssuer`; missing or incomplete issuer state must return a named fail-closed error and must not create the directory or CA. Keep explicit issuer materialization in its authorized lifecycle phase.
- **Test requirement:** retain the existing unverified-installation and foreign-target checks; add absent-directory and empty-issuer-file probes asserting an error and no new files; prove an already initialized issuer still resolves; rerun `go test ./internal/coreinstallation ./cmd/baha -count=1`, build, vet, gofmt, and the required hosted checks at the corrected SHA.
- **Stop criterion:** any resolution attempt creates issuer material, or a missing/foreign authority returns issuer material.

No PR, branch, or card action was taken. The dispatch mission file was absent from this checkout; the review used the owner's stated acceptance points and the task card.
