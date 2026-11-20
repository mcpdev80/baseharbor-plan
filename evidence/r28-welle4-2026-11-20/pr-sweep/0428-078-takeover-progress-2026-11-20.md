# 0428-078 takeover progress — 2026-11-20

## Verified local work

- Product base is PR #1650 head `9add5e8a2122c5555c2403d5ea04073cfb2dc842`, based on current `develop@96f2ae11a25a508998c44a9854ef17f8fa15c112`.
- Isolated local commit `b02a5052655618dec1dd203c408d6ff7c6b881fb` on `codex/0428-078-takeover` changes the Keycloak witness to match the real registration identity and metadata: project-scoped ID, provider endpoint, consumer network, placement scope/class/boundary, native OpenMetrics descriptor, and backend verification.
- A new `identityprovider` integration test invokes `localKeycloakRealization.registerKeycloakSignals()` and checks that its producer registration satisfies the witness.
- Public local and remote status serialization now emits `identity_dashboard_eligible: false` explicitly; tests inspect the raw JSON key and the remote test uses `writeJSON`.
- Focused tests passed: `go test ./internal/metrics ./internal/identityprovider ./cmd/baha -run 'TestIdentity(Witness|Availability|DashboardEligible)|TestKeycloakProducerRegistrationSatisfiesIdentityWitness' -count=1`.
- `go vet ./internal/metrics ./internal/identityprovider ./cmd/baha`, `go build -o /tmp/baseharbor-baha-check ./cmd/baha`, and `git diff --check` passed.
- A full `go test ./internal/metrics ./cmd/baha -count=1` attempt ran for 291 seconds and was stopped after unrelated existing failures: trusted-directory guard failures in access/config-org tests and a host-memory approval failure in `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`. It did not complete successfully; this is not evidence of a clean full package suite.

## Acceptance blockers and publication hold

- Two independent reviews of the prior exact PR head requested changes. The genuine positive public JSON case remains unreachable: `PersesStatusNow` has no verified-producing path. Do not forge `verified` or relax the fail-closed gate.
- The observability registry is global and lacks target state-root/tenant provenance. The project-scoped Keycloak identity separates ordinary namespaces/projects, but it cannot prove isolation when distinct state roots share the same namespace and project. The local diff documents this limit; it does not claim state-root isolation.
- The dashboard catalog is sequenced on 0428-181 after #1684. `perses_selection.go` remains owner-locked and `perses_runtime.go` remains owned by #1684.
- Coordinator was notified through the live Coordinator transport. Per the Coordinator's published direction, keep this commit local until 0428-186/Owner decides whether a real Perses health probe is required or a false-only status contract is accepted. No PR head was pushed and no merge occurred.

## Fresh sweep review findings

- 20 BaseHarbor PRs are open.
- #1702 exact CI was green but independent review is HOLD: its predicate is manifest-only rather than a real backend signal witness; it is behind develop and changes an owner-locked capability file without recorded approval.
- #1704 exact CI was green but independent review is HOLD: alert evaluator contract is constant-false, has no production caller or notification owner, and it is behind develop.
- #1714 exact run `44743031789` succeeded but independent review requested changes: its Valkey positive witness is a caller-set boolean, current descriptor has no verified native producer, the dashboard query lacks an expression, and title/body were placeholders.
- #1715 run `44743111417` had all visible jobs green but was still in progress at review time. Independent review requested changes: tests use `UpdateSignal` rather than the guarded producer registration path, omit Valkey cases, and the PR body lacks a concrete evidence link.
- #1684 still has a failed native Perses runtime smoke; #1645 has a failing Go packages shard; #1615's exact stacked-base checks ran but 17 checks failed. None of these is merge-ready.
- Coordinator received these review outcomes and was asked to map all five worker seats to current missions, blockers, next actions, and release conditions. No GitHub review or merge was submitted for the reviewed PRs.

## 13:37 UTC delta — #1715 exact run failed

- Run `44743111417` is now terminal `FAILURE` at head `c1485721f1305fe4f3b5ef3984df15fe53e937a4`. Its Podman `data-capabilities` selected runtime failed because candidate submission lacked explicit operator/automation consent (`--confirm-candidate`); the wizard cancelled without changes, then `new-edit-new-sql-remove` exceeded the 180-second no-output timeout at 241 seconds. `PR Selected Checks` failed because selected runtime did not succeed.
- The Coordinator was told to track this as an active CI blocker and route the consent fixture/flow plus timeout reproduction to the existing owner. This supersedes the earlier review-time note that the workflow was still in progress.
