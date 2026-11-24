# 0428-078 Keycloak Perses dashboard query label fix + Hosted regression

**Card:** 0428-078 (PR #1650, lane `lane-0428-078-perses-identity-on-resolver`)
**Date:** 2026-11-24
**Author:** w078 worker

## Finding (Owner acceptance)

The Keycloak identity dashboard panel queries in `internal/metrics/perses_dashboards_keycloak.go`
selected `{job="keycloak",baseharbor_application="$application",baseharbor_environment="$env"}`.
Keycloak is a **PROVIDER**, so its production target is a provider-class source
(`targetGroupPayload`, `internal/metrics/prometheus_files.go:171-183`) that emits
`job="baseharbor-providers"`, `baseharbor_provider="keycloak"`, `baseharbor_source`,
`baseharbor_source_class`, `baseharbor_metrics_path` — with **no** `baseharbor_application`/
`baseharbor_environment` labels. Those app/environment labels belong only to
application-class sources (`job="baseharbor-applications"`, `prometheus_files.go`).
The old selectors could therefore never match any real Keycloak series.
`capability.ProviderKeycloak = "keycloak"` (internal/capability/domain.go:54).

## Fix (write-set only)

- `internal/metrics/perses_dashboards_keycloak.go`: each of the 3 `http_server_*`
  queries (`http_server_requests_seconds_count` / `_sum` / `http_server_active_requests`)
  now selects the real provider-class contract
  `job="baseharbor-providers",baseharbor_provider="keycloak"`; the non-existent
  `baseharbor_application`/`baseharbor_environment` selectors are dropped.
  `prometheus_files.go` (established production contract) **not edited**.
- `internal/metrics/perses_dashboards_test.go`:
  - Scoped `assertValidPromQL` so the `keycloak-identity` panel is asserted against the
    provider contract (`job="baseharbor-providers"`, `baseharbor_provider="keycloak"`) and
    explicitly **rejected** for `baseharbor_application`/`baseharbor_environment` and for
    `job="keycloak"`; application-class backends keep their app/environment assertion.
  - Added Hosted regression `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels`:
    drives the real `persesDashboardCatalog()`, asserts every keycloak query selects the
    real provider labels and a documented `http_server_*` metric, never
    `job="keycloak"` or application/environment labels. Negative witness confirmed:
    the test **fails** on the original broken query and **passes** on the fix.
- `internal/metrics/testdata/perses-dashboards/keycloak-identity.json`: regenerated via
  `persesPanelJSON` — byte-identical to the prior golden except the 3 queries now select
  the provider labels.

## Hosted CI verification (exact head)

**Run id:** r7565 — `45297432220`
**Head:** `84943695b` (PR #1650 head; remote lane head `84943695b`)

Run conclusion: **success** (0 failures, 0 non-success/non-skipped).

| Job | Conclusion |
| --- | --- |
| PR · Trusted Plan | success (the job that failed on `cf4eacb67` now passes) |
| PR · Native · native/docker/data-capabilities | success |
| PR · Native · native/podman/data-capabilities | success |
| PR · Go unit · cli-0/1/2/3/owner/packages | success |
| PR · Validation · go-build / go-vet / cli-gofmt | success |
| PR · Validation · ci-integration-operator-seam-tests | success |
| PR · Validation · identity-provider-package-tests | success |
| PR · Exact Candidate | success |

Root cause of the prior failure (run `45294385817`): the **only** uncataloged path was
`cmd/baha/.ci_touch_1`, a 0-byte incidental file introduced by a CI-trigger commit
(`1f2ef3c1e`, no product/test purpose; not referenced anywhere). Removed from the PR by
amending the head (`cf4eacb67` -> `84943695b`). The 3 baseline paths
(`internal/identityprovider/keycloak_files.go`, `keycloak_realization.go`,
`testdata/perses-dashboards/keycloak-identity.json`) are baseline rows a separate owner PR
(#1817 pattern) lands on develop — **not** added to #1650 per instruction.

## Attestation

- PR #1650 head (verified via `gh pr view 1650`): `84943695be19300ef006a7986e1d110130943ce8`
- Remote lane head (`git ls-remote lane-origin refs/heads/lane-0428-078-perses-identity-on-resolver`): `84943695b`
- Local HEAD: `84943695b` (amend of the 3-file product fix)
- `.ci_touch_1` absent from the PR tree (0-byte file deleted)
- Local: `go build ./...` ok; `go vet ./internal/metrics/` ok; full `./internal/metrics/` suite green
- No `.github/**` edits; no force-push of shared refs other than this lane's own PR head

## Scope / merge hold

- Merge **still HELD** on the #1810 real-probe dependency and the label fix above. No
  merge, no Codex. Full delivery (Option A) — the production Perses export/provision
  consumer (0428-181), not a dashboard-only artifact — remains outstanding and required.
