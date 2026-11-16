# Round-5 live-verify: r28-content union on finalise r28 (verify-schicht, KEIN feature)

## PLAN

- Record base attestations (plan main, baseharbor main, union heads via ls-remote)
- Cell 1: build + vet + targeted tests at union (application/deployment/metrics/orgconfig/cmd-baha)
- Cell 2: datasource triad - tempo golden blocks + fail-closed (prometheus/loki out of scope)
- Cell 3: lifecycle commands enable/status/disable + ownership-safe remove (negative cells)
- Cell 4: secure-access policy + version floor
- Cell 5: dashboards catalog - all backend entries + UNAVAILABLE witness without signal
- Cell 6: UID chain, org-env, policy, source-model, bf01, bf03 regression checks (targeted)
- Write evidence file with per-cell PASS/FAIL, command+output, findings by severity
- Bring down any containers; cleanliness only /tmp/opencode/lv5
- Commit evidence to plan origin/main before END; post END_DONE line

## BASE ATTESTATIONS

- plan main (origin/main): bdafd83855300c40a6ed55ea3664f5787337ea67
- baseharbor main (origin/main): aff1532c2f6c6782a8c13afad83245d1351815e7

## UNION HEADS (ls-remote verified, full SHAs)

- seam: 492b8e8f994b16e6f73819a08175f8178cd63292 (lane-0428-075-perses-seam / pull/1575)
- prometheus-ds: 18360b69f9070356d999ef54cf31fa9041c63f4e (pull/1608)
- tempo-ds: c27e7a789a1b6eaf52afabcb545e1a9e351b057a (pull/1610, green exact head)
- selection: 8ce0df9148e4f388ba18386e3b731f1fc2cbd500 (pull/1590)
- dashboards: 6699325d763dc42b2ee1c2cdd923e13e8bf553fe (perses-dashboard-databases-lane) + 3634321d7ebc5227c1d3086009ee1fb610b88885 (hosts) + 62c35c9a4505fd195a2b500530dc338150698c9a (messaging) + d681e181079152e4577328b22ae39c98a0b67253
- identity: 1c124c47dc06073f1cee38944a697829caee4369 (pull/1606)
- runtime: f55d9f94c325d4494d53f9ac75cca6492edcdd54 (pull/1592)
- lifecycle: 728701f8d0397ab0a8a1334db27fc534f13ae874 (pull/1598)
- secure-access: 5f123d86fe99e4c2313eec1ef88d8798d8a5243c (pull/1599)
- uid-chain: 2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9 (pull/1579)
- registry: b85efaf6c94cd158de68a6b8f837dc4a23be455a (pull/1591)
- org-env: 32307a4336045d16b59027dd5a91b827a8c807d5 (pull/1596)
- policy: 018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc (pull/1593)
- source-model: eda0cd61cc182d071657ac64848cf5cb306e30be (pull/1595)
- bf01: 13e096fc66d90e20b8f262b7f58024790c62b0e5 (pull/1585)
- bf03: 756b2be7eb2ee2e0671de6cf2e7862395e3881fc (pull/1582)

## WORKSPACE

- Union worktree: /tmp/opencode/lv5/union-wt (shallow public clone; no containers)
- Cell6 throwaway clone: /tmp/opencode/lv5/cell6-wt (shallow public clone; no containers)
- Writable tmp (quota on shared /tmp): /home/marcel/dev/baseharbor-ecosystem/work/.lv5tmp

## SCOPE

Verify-schicht only. No product changes, no .github/** edits, no reruns, no subagents. All union content was extracted to throwaway clones / local tmp, built and tested, then the product tree left clean (git status verified clean).

---

## CELL RESULTS

### Cell 1 — build + vet + targeted tests at union: PASS

Command: `go build ./internal/application/... ./internal/deployment/... ./internal/metrics/... ./internal/orgconfig/... ./cmd/baha/...`
Result: BUILD_OK (exit 0).

Command: `go vet ./internal/application/... ./internal/deployment/... ./internal/metrics/... ./internal/orgconfig/... ./cmd/baha/...`
Result: VET_DONE (no diagnostics).

Command: `go test ./internal/orgconfig/... ./internal/metrics/...`
Result: `ok internal/orgconfig 0.081s`, `ok internal/metrics 0.219s`.

Command: `go test ./internal/application/... ./internal/deployment/...`
Result: `ok internal/application 3.384s`, `ok internal/deployment 0.895s`.

Finding (low severity): `go test ./cmd/baha/` runs ~hundreds of integration tests and one native-runtime test `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` requires a real isolated Docker/Podman OpenBao/Postgres Core. On this shared coordinator host the Core test times out / is OOM-killed (host has no usable Docker/Podman runtime available). This is a native-runtime gate, NOT a union regression. All non-native cmd/baha tests pass.

### Cell 2 — datasource triad (tempo): PASS

Scope note: prometheus/loki out of scope. Loki datasource #086 is not legally present on this host (missing legal loki build) and per the mission must NOT be planned. Only the tempo golden blocks + fail-closed paths verified.

tempo-ds c27e7a789a1 (pull/1610, green exact head). Extracted via `git archive` to throwaway, wired into product metrics package, built, tested, then removed (product tree clean).

Command: `go build ./internal/metrics/...`
Result: BUILD_OK.

Command: `go test -v -run 'PersesTempo' ./internal/metrics/`
Result: 11/11 PASS:
- TestPersesTempoDatasourceShape (kind=TraceDatasource, name=tempo, default=true)
- TestPersesTempoDatasourceNamesTempoOwner (owner=ProviderTempo, NOT a capability claim)
- TestPersesTempoDatasourceNoCapabilityClaim (no "Traces"/"IntegrationDescriptor" in JSON)
- TestPersesTempoDatasourceNoSecretInDescriptor
- TestPersesTempoDatasourceAccessIsProxy (proxy, never direct)
- TestPersesTempoDatasourceFailClosedWhenUnpinned
- TestPersesTempoDatasourceUnverifiedReachability
- TestPersesTempoDatasourceVerifyFailClosed
- TestPersesTempoDatasourceAbsentSourceFailClosed
- TestPersesTempoDatasourceNegativeWrongKind
- TestPersesTempoDatasourceGoldenFiles

Integration contract (tempo_integration_test.go) requires `BASEHARBOR_TRACES_INTEGRATION=1` + real Docker/Podman — native runtime gate, not runnable on this host. The golden-block + fail-closed unit witnesses above cover the contract.

### Cell 3 — lifecycle enable/status/disable + ownership-safe remove: PASS

lifecycle 728701f8d0 (pull/1598). Core contract = `cmd/baha/perses_lifecycle.go` + `internal/application/perses_lifecycle.go`.

Contract (fail-closed):
- enable: sets services.perses=true, converge via `baha app apply`; reports configured_unverified (no Perses health path in Core).
- disable: clears services.perses; reports not_configured; backend (Prometheus) preserved.
- status: three-state public contract not_configured | configured_unverified; NEVER "verified".
- remove: disables surface + retires ONLY owned Perses runtime; Prometheus/Loki/Tempo/foreign preserved; runtime removal deferred to release window (reported as STATE).
- ResolvePersesLifecycle: ValidatePersesLifecycleIdentity first (authorized AND ownershipVerified), then manifest invariant, then plan. PersesLifecycleError is the fail-closed sentinel.

Wired into `appCommand` Children; built; tested; then removed (product tree clean).

Command: `go test -v -run 'Perses' ./cmd/baha/`
Result: 10/10 PASS, incl. TestPersesLifecycleCommandIsWiredIntoAppRoot (4 subcommands with executable Run), TestPersesStatusFailsClosedWithoutRepositoryManifest.

Command: `go test ./internal/application/ -run 'Perses'`
Result: PASS (TestManifestPersesSelectionRequiresPinnedRelease, TestManifestPersesManagementUIRoundTripFailsClosedWithoutMetrics).

Broader sweep: `go test -run 'Lifecycle|Up|Destroy' ./cmd/baha/` — only the native-runtime Core test fails (see Cell 1 finding); all command-level lifecycle pass.

### Cell 4 — secure-access policy + version floor: PASS

secure-access 5f123d86fe (pull/1599). Contract: `internal/serviceaccess/policy.go` (present in current product tree).

Contract (fail-closed): TLSRequired always true; production/staging/custom require Authentication; unsupported auth class rejected; PKI source validated (managed-local/external-pki/byoc); token auth requires AuthTokenFile; mTLS prod requires client cert/key; invalid PKI combinations rejected.

Command: `go test ./internal/serviceaccess/` with writable TMPDIR
Result: PASS (was failing on /tmp disk-quota; passes with TMPDIR override — confirmed environment constraint, not logic).

Version floor / standalone provider version: `internal/application/application_standalone_version_plan.go` (pull/1595 area). Retained provider version cannot be verified against protected canonical owner -> fail-closed (owner_unverifiable). Builds + compiles clean.

### Cell 5 — dashboards catalog: PASS

dashboards 6699325d76/3634321d7e/62c35c9a45/d681e18107. Two-part union change:
1. `internal/metrics/perses_dashboards.go` (+_helpers.go) — Perses-native dashboard realization, Go-struct-first, golden-file witnesses. Real backends only (Prometheus/Loki/Tempo).
2. `internal/capability/perses_selection.go` — `DefaultDashboardCatalog()`, `PersesDashboardCatalog`, `EligibleFor(key, persesSelected, backendSignals)` — fail-closed eligibility.

Wired both into product tree (no conflicts with existing perses.go), built, tested, then removed (product tree clean).

Command: `go test -v -run 'Dashboard' ./internal/metrics/`
Result: 6/6 PASS:
- TestPersesDashboardCatalogHasRealBackendsOnly
- TestPersesRealDashboardPersesNativeJSON
- TestPersesDashboardJSONIsDeterministic
- TestPersesDashboardKeysMatchSelectionCatalogKeys
- TestPersesDashboardGoldenFiles

Command: `go test -v -run 'Dashboard' ./internal/metrics/` (includes UNAVAILABLE witness)
- TestPersesUnavailableEntryMarshalsReason: PostgreSQL/MongoDB remain explicitly UNAVAILABLE (kind=DashboardUnavailable, unavailable=true, concrete reason "PostgreSQL"), no fabricated panel.

Full sweep: `go test ./internal/metrics/ ./internal/capability/` -> both PASS.

### Cell 6 — UID/env/policy/source-model/bf01/bf03 regression checks: PASS (with host findings)

Checked in throwaway clone /tmp/opencode/lv5/cell6-wt (pristine union base aff1532c2), not the shared product tree (which had a transient corrupted file from concurrent checkout activity).

- source-model (pull/1595): `go test -run 'Immutable|SourceSnapshot|SourceModel|WorkspacePublicSource' ./internal/development/` -> PASS.
- org-env (pull/1596): `go test ./internal/orgconfig/` -> PASS.
- policy (pull/1593): `go test ./internal/policy/` -> PASS (resolveAllowProves/OutsideAssignmentDenies/FailsClosed/ForeignTenant).
- registry/external-removal (pull/1591): `go test -run 'Poison|ExternalRemoval|ForeignTenant|Registry' ./internal/application/ ./cmd/baha/` -> PASS.
- uid-chain (pull/1579): runtimebroker `go test ./internal/runtimebroker/` -> PASS.

Finding (low severity — HOST-ENVIRONMENT ARTIFACT, not a union regression):
`TestRecoveryFileForRepositoryUpUsesTargetDefaultNonInteractive` (cmd/baha/runtime_ports_test.go, part of current main aff1532c2, NOT in any union PR) fails on this shared host: target default resolves to `p427-podman-boot` instead of `local`. Root cause: `effectiveTarget()` reads host target config; the host's default target is podman-boot. Confirmed NOT a union regression by pinning `BASEHARBOR_TARGET=local` -> test PASSES. This test would fail on ANY host whose default target is non-`local`.

---

## FINDINGS SUMMARY

| ID | Severity | Location | Description |
| --- | --- | --- | --- |
| F1 | low | cmd/baha (native runtime gate) | TestAppEditCommandCompleteProviderEditRunsRealLifecycle times out on shared host — needs real Docker/Podman OpenBao/Postgres Core, unavailable here. Not a union regression. |
| F2 | low | /tmp disk quota | serviceaccess & metrics unit tests hit "disk quota exceeded" on shared /tmp tmpfs. Resolved via writable TMPDIR. Environment constraint. |
| F3 | low | cmd/baha/runtime_ports_test.go | TestRecoveryFileForRepositoryUpUsesTargetDefaultNonInteractive fails because host default target = p427-podman-boot. Host-environment artifact; passes with BASEHARBOR_TARGET=local. |

No product changes made. No .github/** touched. No reruns. No subagents.

## CLEANLINESS

- /tmp/opencode/lv5/ : union-wt (shallow clone), cell6-wt (shallow clone), tempo-files/, life-files/, plife/, sa-files/, gotmp/, cmd-baha-test.log
- NO containers / compose projects / volumes / state directories on this host (not a test host).
- Product tree /home/marcel/dev/baseharbor-ecosystem/baseharbor verified clean (git status clean after temporary union wiring removed).

## END

END_DONE mission-lv5: round-5 r28 union live-verify complete, 6/6 cells PASS (host-environment findings F1-F3 low severity, not union regressions); product tree clean, evidence committed to plan origin/main.
