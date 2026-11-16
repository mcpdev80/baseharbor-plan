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

- DONE pending: resolver surface is an 080 scope expansion -> STOP (file:line above), no own build.
- PR #1650 left untouched (still DRAFT). No push. No evidence path committed to a product repo
  (this akte lives only in baseharbor-plan; workers/baseharbor-plan is bookkeeping and untouched).
- END post required.
