# on-resolver-round-2 — 078 r2 chain (mission-identity-078-r2-chain)

Lane: lane-0428-078-perses-identity-on-resolver
Card: t-20261114-r28-perses-dashboard-identity
Date: 2026-11-16
Owner: worker-ornith1.5 (this session)
Base attest: fd82668f1cab2b5c90eb6f961816a55f7ec68ecd (lane-0428-080-r28-perses-selection, #1590 r3, APPROVE CONTENT)
Candidate: 3b56ed05c (merge 7935655fe c8430f826 onto fd82668f1 + name-reconcile + test fix)

## Mission (r2)

1. Rebase my stack from 1781277d3 onto fd82668f1 (new merge-commit, no force-push).
2. Clean up duplicate identity-catalog API/key names present in my diff vs base.
3. Set the production status-result call-site (app_status_result.go -> persesStatus) through
   the resolver: identity-keycloak eligible only via EligibleFor with NonForgeableAvailable +
   per-backend keycloak signal (fail-closed). STOP if the resolver surface is missing.

## Task 1 — rebase (DONE)

- Base moved from 1781277d3 to fd82668f1 (080-r3 batch13 landed) while this lane sat on the
  old base. Both are descendants of 1873ba33f (my old base), so the rebase is a merge against
  the r3 head:
  - merge-base(c8430f826, fd82668f1) = 1781277d3 (my old base, confirmed via git merge-base)
  - fd82668f1 is NOT an ancestor of c8430f826 (divergent) -> a new merge-commit is the correct
    chain path (inhalt warten, keine force-push).
- Method: `git merge --no-ff fd82668f1` into the branch (produced the merge 7935655fe with two
  parents c8430f826 + fd82668f1), resolved the two conflict regions against the base naming,
  then committed. Confirmed fd82668f1 IS now an ancestor of HEAD (git merge-base --is-ancestor).
- New HEAD 7935655fe: `git rev-list --parents -n 1` = `7935655fe c8430f826 fd82668f1` (two parents).

## Task 2 — duplicate identity-catalog names (DONE)

My original commit c8430f826 introduced `DashboardBackendKeycloak` (="keycloak") and the
catalog key `"identity-keycloak"`. The r3 base fd82668f1 ALREADY ships:

  - const `DashboardBackendIdentity DashboardBackend = "identity"` (perses_selection.go)
  - catalog template `"keycloak-identity"` with `Backend: DashboardBackendIdentity`
    (`Datasource: "keycloak"`)
  - tests using `"keycloak-identity"` / `DashboardBackendIdentity`

My duplicate const/template now collide with the base. Reconciliation (content-only rename to
the base vocabulary, no behavior change):

  - perses_selection.go: the merge conflict was resolved to KEEP the base naming
    (DashboardBackendIdentity / "keycloak-identity"); my DashboardBackendKeycloak /
    "identity-keycloak" removed. `git diff fd82668f1 -- perses_selection.go` is EMPTY (matches base).
  - perses_selection_test.go: my 4 test functions re-keyed from `DashboardBackendKeycloak` /
    "identity-keycloak" to `DashboardBackendIdentity` / "keycloak-identity"; the duplicate
    `want` map entry removed; the per-backend reason assertion changed from "keycloak" to
    "identity" (the reason string renders the backend name, which is now "identity").

Net diff vs base fd82668f1 = only the 104-line identity test block (my original content, now
renamed). No catalog/gate/content change. Build/vet/gofmt clean. All 20+ identity/dashboard
tests pass, including the 4 new ones.

## Task 3 — production call-site (STOP: resolver surface missing)

The call-site at cmd/baha/app_status_result.go line 143 currently computes:

  persesStatus := capability.PersesStatusNow(resolved.Manifest.Services.ObservabilityManagementUI && resolved.Manifest.Services.Perses)

This is a manifest-declaration three-state (not_configured | configured_unverified |
never-verified) and does NOT run the identity-selection witness or per-backend signal gate. To
wire it through EligibleFor/NonForgeableAvailable the resolver must produce an
IdentitySelectionWitness { SelectionConfirmed, MetricPresent, MetricCurrent, TargetAuthorized }
plus the per-backend signal inventory. VERIFIED GAP:

- No production resolver derives any of the four witness flags:
  - grep -rn "^func.*Resolve\|Witness\|Selection\|Eligible\|Available" internal/identityprovider/ => none
  - internal/capability/perses_selection.go exposes the FAIL-CLOSED gate only
    (NewIdentitySelectionWitness / NonForgeableAvailable / EligibleFor / FilterEligibleDashboards);
    no production consumer calls it (r1 akte auf-resolver-round-1 confirmed the same).
- MetricPresent / MetricCurrent (real Keycloak native metrics signal, pinned to current release):
  no production code reads the keycloak-metrics signal. internal/metrics/ has NO keycloak metrics
  provider (ls internal/metrics/ | grep keycloak => empty). reference.go:160 only STATICALLY
  declares the descriptor (ReferenceIntegration is a descriptor, not a runtime resolver).
- TargetAuthorized (real non-forgeable provider placement / authorization): ResolveProviderPlacement
  exists (internal/application/provider_placement.go:99) but nothing maps a Keycloak placement into
  the witness TargetAuthorized flag.
- SelectionConfirmed: nothing maps manifest identity-selection into the flag.

STOP file:line:

  - build the witness resolver + per-backend signal collection (identity-selection confirmation,
    keycloak-metrics native/current resolution, TargetAuthorized from placement) => an 080-scope
    expansion. This lane must NOT build it.
  - the production call-site in cmd/baha/app_status_result.go (persesStatus, line 143) must NOT be
    switched to a caller-supplied or fabricable status; it must wait for the 080 resolver surface.

No .github/** touched, no force-push, no PR mutation, no subagent. Every step in this session.

## STOP CORRECTED BY OWNER (2026-11-16)

Owner grep on the merged stack 1369328e7: the resolver surface is NOT missing. The gate
(NonForgeableAvailable / backendSignals / EligibleFor / FilterEligibleDashboards) lives in
internal/capability/perses_selection.go (my own rebase output), and reference.go:160 statically
declares the keycloak-metrics native openmetrics signal (Mode: ObservabilityNative). The missing
piece was NOT a new 080 resolver — it was the production witness derivation from real primitives.
Wiring through reference.go -> gate is the task. RESOLVED, no STOP.

## Run status

### Task 3 — production call-site wiring (DONE)

Design (reference.go as path, gate as decision — NO new 080 resolver):

  - metrics.IdentitySelectionWitnessAt(m, placement, dataDir, namespace) in
    internal/metrics/perses_identity_witness.go builds the non-forgeable witness from real
    production primitives only (never a caller status):
      * SelectionConfirmed   = application.HasIdentity(m), never an assumed exporter.
      * TargetAuthorized     = ProviderPlacement.Validate() ok AND Scope != ScopeExternal (valid
        BaseHarbor-owned Keycloak placement, never external OIDC).
      * MetricPresent        = keycloak-metrics signal registered for this Target in the
        observability signal registry (observability.List, prometheus_verify.go pattern).
      * MetricCurrent        = that signal matches the native openmetrics realization declared in
        capability.ReferenceIntegration(Keycloak).Observability.Signals (reference.go:160).
    Any missing flag fails closed to the zero witness. Available is derived (AND) inside the
    constructor — cannot be forged by a caller. metrics was the only package importing
    application + capability + observability without a cycle (capability cannot import application).
  - Call-site cmd/baha/app_status_result.go: resolve the Keycloak placement, build the witness
    (metricsprovider.IdentitySelectionWitnessAt with resolved.TargetStateRoot / target name),
    compute NonForgeableAvailable(), surface it as new JSON field `identity_dashboard_eligible` on
    BOTH the local and remote-target status faces (computed before the remote-target early return).
  - Eligibility decision: identity-keycloak eligible ONLY via NonForgeableAvailable() + real
    per-backend keycloak-metrics signal. No caller can obtain a positive claim by supplying a status
    boolean.

Build / vet / gofmt / tests:
  - go build ./... => OK (local TMPDIR: shared system /tmp tmpfs 80% full).
  - go vet ./internal/metrics/... ./cmd/baha/... => OK.
  - gofmt -l on all three changed files => clean.
  - go test ./internal/metrics/... ./internal/capability/... => OK.
  - 4 new witness tests (internal/metrics/perses_identity_witness_test.go): 1 POSITIVE (real signal
    + valid target auth -> NonForgeableAvailable()==true, all four flags true) + 3 NEGATIVE (no
    signal / identity not selected / external OIDC placement -> fail-closed).

Repo-rule compliance:
  - No .github/** touched. No force-push. No PR mutation. No subagent. Only three files changed:
    1 new witness builder, 1 new test, 1 call-site edit (additive JSON field).
  - Evidence lives only in baseharbor-plan (not in the product repo).

## Commit + push (DONE)

  - Commit d94d477d9: "fix(0428-078): wire Perses identity-keycloak call-site through resolver gate (r2)".
    Staged precisely (never `git add -A`): perses_identity_witness.go + perses_identity_witness_test.go +
    app_status_result.go. 3 files, 328 insertions / 18 deletions.
  - Pushed via refspec to lane-0428-078-perses-identity-on-resolver; ls-remote attest:
    d94d477d92f16c9fba5f76b681a332ee03f8456e.
  - CI run #6365 "CI · PR #1650" @ d94d477d9 => completed / SUCCESS (run-id 43913569730).
  - PR #1650 still OPEN / DRAFT, base lane-0428-080-r28-perses-selection (isDraft confirmed true).

## Run status

  - go build ./internal/capability/... => OK
- go vet ./internal/capability/... => OK
- gofmt -l => clean
- go test ./internal/capability/... -run Identity|Dashboard|Eligible|Catalog|Filter|Backend => PASS (20+)
- The two unrelated failures in the full suite (TestRegistryStorePersistsOwnerOnlyValidatedState,
  TestRegistryStoreSerializesConcurrentUpdates) are `write ... /tmp/...: disk quota exceeded`
  (shared system /tmp tmpfs 80% full). Not caused by this change: the capability identity/dashboard
  tests pass in isolation; the two failing tests write provider-registry JSON into system /tmp.
- No CI gate run (build/vet/gofmt/tests only; no push yet). No compose project started.

## END status

- PRODUCTION call-site wiring DONE and CI-green @ d94d477d9.
- PR #1650 still OPEN/DRAFT, base lane-0428-080-r28-perses-selection (verified isDraft==true).
- Evidence path lives only in baseharbor-plan (this akte); no product-repo evidence written.
- END post below.
