# 0428-101 — project-scoped Keycloak signal IDs

Date: 2026-11-20

## Ownership and starting point

- Product base: `develop` at `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978`.
- Before implementation, live Codeman sessions showed the Coordinator busy and active workers on #1684, #1690, #150 and #160; no worker owned 0428-101, `internal/identityprovider/keycloak_realization.go`, or #1650.
- #1650 was OPEN/DIRTY at head `022c454ce482cce51cab47b4797caaaccd0bc175`. Its current diff changed workflow files, `cmd/baha/app_status_result.go`, runtime fixtures, capability selection tests and Perses witness files; it did not touch the Keycloak realization or identity-provider package. The previous literal file-overlap blocker was therefore stale. #1650 remains an unresolved PR but is not a write-set conflict for this patch.

## Change and regression

`localKeycloakRealization.registerKeycloakSignals` used the global registry identity `keycloak-metrics`. The registry replaces a source when both ID and provider match, so registering a second Keycloak project removed the first project's source. The fix uses `keycloak:<compose-project>`, following the project-scoped identity pattern used by Loki and Tempo. The declared signal name remains `keycloak-metrics`.

Added `TestKeycloakSignalRegistrationKeepsProjectsDistinct`, which registers two projects into the same registry and verifies each source remains visible to its owning application after both registrations. Red test on the unmodified base failed: after registering project `identity-beta`, app `alpha` saw only the replaced `keycloak-metrics` source owned by beta. The regression passed after the ID change.

## Exact candidate and verification

- Draft PR: [#1707](https://github.com/mcpdev80/baseharbor/pull/1707)
- Exact head: `162ac67022aceb0dbddc4e78a00fdc62391ce25e`
- `go test ./internal/identityprovider -count=1` — PASS
- `go vet ./internal/identityprovider` — PASS
- `git diff --check` — PASS

## CI routing and outstanding gates

The test is ordinary package-discovered coverage. The existing `PR · Go unit · packages` shard calls `go test` for every non-CLI package and includes `internal/identityprovider`; no test registry change is needed. Per `scripts/pr-gate-plan.py`, a production Go change in `internal/identityprovider` also routes to the existing identity-provider package checks, Go build/vet, CLI checks and Docker/Podman lifecycle gates.

Exact-head run [44643902576](https://github.com/mcpdev80/baseharbor/actions/runs/44643902576) completed successfully on exact head `162ac67022aceb0dbddc4e78a00fdc62391ce25e`. `PR · Draft source and routing` and all five Draft Go shards passed. Draft policy skipped regular source-format/selected-check and native/runtime gates, so those outcomes are not evidence of success. Keep the card in review and PR as draft through review; before merge, make the PR Ready and require fresh exact-head CI including the selected impact gates.
