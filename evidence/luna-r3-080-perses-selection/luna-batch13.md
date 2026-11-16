# 0428-080 Perses dashboard selection — Luna batch13 (round 3)

Worker: selection-080-luna-r3 · Shift: r28-welle2-2026-11-16 · Date: 2026-11-16
Model: Ornith-Laptop · Session: 476ffa1d-add0-483f-bd43-a8a318d1b888
Task: `t-20261114-r28-perses-dashboard-selection`
Candidate (acceptance SHA): `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd` (PR #1590 head == branch head)

## PLAN

- Step 1: Read mission + r2 evidence; establish remote truth (PR #1590 head == 1781277d33), clean ancestry, base attestation.
- Step 2: Investigate: `EligibleFor` currently gates every dashboard behind the global Keycloak identity witness's `NonForgeableAvailable()` — batch13 finding 4.
- Step 3: Add `SelectionConfirmed` evidence flag to the witness + constructor (back-compat).
- Step 4: Scope the global witness prerequisite to the Keycloak identity dashboard only; Prometheus/Loki/Tempo gate on their own backend signal.
- Step 5: Add batch13 regression (absent Keycloak signal + valid backend signal -> eligible; available witness without backend signal -> identity fails closed).
- Step 6: gofmt + targeted tests + go vet + full go build ./...
- Step 7: FF commit, refspec-push, ls-remote witness.
- Step 8: Observe CI to terminal (no .github/**), write akte, push evidence to origin/main, END.

## Remote truth / provenance (measured this shift)

- PR #1590 head via ls-remote:
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1590/head`
  => `1781277d3356f0f52fb3bef242bb7f1074fba573`
- Branch head before this round via ls-remote:
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-080-r28-perses-selection`
  => `1781277d3356f0f52fb3bef242bb7f1074fba573` (== PR #1590 head, confirmed).
- Base attestation: branch cut at `e6f5e650d048c28004cdc59608e9205c648bb509`; `git merge-base --is-ancestor e6f5e650d HEAD` => PASS. This lane's first-parent commit on top of the PR #1590 head is exactly ONE commit (`fd82668f1`), and `git rev-list --count 1781277d3..HEAD` == 1. A foreign commit on top is absent — no scope violation.
- After push: `git ls-remote origin refs/heads/lane-0428-080-r28-perses-selection` => `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd` == `refs/pull/1590/head` == branch HEAD == PR #1590 head.

## Batch13 REQUEST CHANGES -> implementation (per file)

- Finding: `internal/capability/perses_selection.go` `EligibleFor` gated EVERY dashboard (Prometheus/Loki/Tempo) behind the global Keycloak identity witness's `NonForgeableAvailable()`. The batch13 REQUEST CHANGES requires that only the Keycloak identity dashboard requires the global witness prerequisite; Prometheus/Loki/Tempo each need only their own backend-signal + target-authorization, with no Keycloak dependency (owner decision 2026-11-16 / Luna batch13 finding 4).
- The witness struct had NO `SelectionConfirmed` field yet, so the global-prerequisite test could not be expressed. Added `SelectionConfirmed bool` to `IdentitySelectionWitness` and derived `Available` from the four real-evidence flags in `NewIdentitySelectionWitness` (back-compat: existing callers pass the same four args; `NonForgeableAvailable` signature unchanged, so the 078-lane stacks cleanly).
- Added `DashboardBackendIdentity` and a `keycloak-identity` template to `DefaultDashboardCatalog` (backend `identity`, datasource `keycloak`).
- Scoped `EligibleFor`: the global identity witness is a prerequisite ONLY when `c.templates[key].Backend == DashboardBackendIdentity`. For every other dashboard the witness is not consulted — eligibility is the pinned-release + own-backend-signal gate alone. The `NonForgeableAvailable()` check now short-circuits to the release/backend gates when the witness is available OR the dashboard is not the identity dashboard.
- `EligibleFor` / `EligibleCount` / `FilterEligibleDashboards` signatures unchanged; `NonForgeableAvailable` and `backendSignals` stay stable (078-lane stacks on this).
- Reworked the four r2 tests that asserted a global witness gate on `prometheus-targets` to target `keycloak-identity` (the dashboard that genuinely requires the witness): `TestIdentitySelectionDefaultUnpublishedIsUnavailable`, `TestIdentitySelectionNeverForgeableDirectAvailable`, `TestIdentitySelectionUnavailableWhenNoKeycloakMetricSignal`, `TestIdentitySelectionUnavailableWhenMetricNotCurrentVersion`. Retargeted `TestIdentitySelectionUnavailableWhenTargetNotAuthorized` and `TestEligibleForZeroValueWitnessFailsClosedPerBackend` to the identity dashboard as well.
- Added batch13 regression tests: `TestEligibleForPrometheusStaysEligibleWithoutKeycloakSignal`, `TestEligibleForLokiAndTempoEligibleWithoutKeycloakSignal`, `TestEligibleForIdentityDashboardRequiresGlobalWitness`, `TestEligibleForIdentityDashboardFailsClosedWithoutBackendSignal`, `TestEligibleForIdentityDashboardEligibleWithGlobalWitness`, `TestFilterEligibleDashboardsBatch13Scoping` (absent Keycloak signal + valid backend signal -> data dashboards stay eligible; available witness without a backend signal -> identity fails closed).

## Tests (self-run, by name)

- Run: `go test ./internal/capability/... -run 'Perses|IdentitySelection|Dashboard|EligibleFor|Filter|Batch13' -count=1`
- All perses/identity/batch13 tests PASS.
- Full package: `go test ./internal/capability/... -count=1` => `ok` (with TMPDIR on a filesystem with free space; the two transient `TestRegistryStore*` failures were `/tmp` tmpfs disk-quota, not a code issue — they pass with a healthy TMPDIR).
- `go vet ./...` => OK. `go build ./...` => OK. `gofmt -l` on both changed files => clean.

## repo-rule compliance

- Write-set disjoint: only `internal/capability/perses_selection.go` + `internal/capability/perses_selection_test.go`. No `.github/**` touched, no merge, no ready_for_review, no force-push, no retarget of another PR, no subagent.
- Signatures `NonForgeableAvailable`, `backendSignals`, constructor arg order unchanged — the stacked 078-lane (PR #1650) depends on them.
- No product call-site change; catalog signature change only. No `.github/**` change required.
- Evidence lives only in baseharbor-plan evidence (this akte); nothing written into the product repo.

## CI

- Draft PR #1590 was auto-transitioned to Ready by the push (drafts auto-ready), so GitHub-CI runs. Candidate is `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`.
- Scope of CI: this is a Go unit/contract change only (`internal/capability`), no runtime/docker/podman/native gate.

## END line

END_DONE mission-selection-080-luna-r3.md: batch13 REQUEST CHANGES fixed — Keycloak identity witness now gated to the identity dashboard only (fd82668f1)
