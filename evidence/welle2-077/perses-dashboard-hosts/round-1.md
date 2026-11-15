# round-1 — Perses host and container dashboards (0428-077)

## PLAN

1. Read task contract in baseharbor-plan, verify base stacking head and dependency state.
2. Study reference source (prometheus_render.go, prometheus_files.go, perses_selection.go) and the #1597 (076) precedent for perses-native JSON + CLI wiring.
3. Determine real available host/container signals on prometheus/loki/tempo; mark UNAVAILABLE explicitly where no native signal ships.
4. Create own host/container panel files (stack on 080, NOT on 1597) with perses-native JSON + real query.
5. Write deterministic golden-file tests per panel + CLI availability face.
6. Build, vet, run focused tests; record SHAs and outputs.
7. Record CI coverage (report .github change as finding if needed), cleanliness.
8. Commit evidence to origin/main; draft PR; END post.

## Scope, base and ownership

- Card: 0428-077 — Perses host and container dashboards (t-20261114-r28-perses-dashboard-hosts).
- Owner: lane-0428-077 (this lane). PR title carries card number 0428-077.
- Base-stacking head (rule 8): `lane-0428-080-r28-perses-selection` = PR #1590 head.
- Base head SHA (witnessed, ancestor of all my commits): `85b4cbb598272e28944e48b6895ce8935031c9ba`.
- FAECHREGEL (Owner 2026-11-04): I stack on 080, NOT on #1597 (database-dashboards). No edit to #1597's files. My write-set is fully disjoint (own panel files, own testdata, own CLI struct field).
- Dependency state at start: t-20261114-r28-perses-dashboard-selection in state `wait` (NOT accepted). I proceed with implementation (the card permits building the candidate), but the active->review transition cannot complete until the prerequisite is accepted. Reported as STATE below.

## Real signal inventory (grounding, not fabricated)

BaseHarbor ships exactly two real Prometheus jobs, verified in source:
- `baseharbor-applications` — per-application up-signal with labels baseharbor_application/baseharbor_environment/baseharbor_source (internal/metrics/realization.go:147).
- `baseharbor-providers` — per-provider targets with label baseharbor_provider (internal/metrics/prometheus_render.go:217, prometheus_files.go:68).

Loki and Tempo realize the same application job's logs/traces; the three backends are the only native signal axes (perses_selection.go catalog).

Host/container coverage decision:
- AVAILABLE: container/metrics for BaseHarbor's own provider services (the Prometheus provider is a Docker/compose container) — queried via the provider job. Host up-signal for BaseHarbor services.
- EXPLICITLY UNAVAILABLE: arbitrary host node metrics (host CPU/RAM/node_exporter) and raw cAdvisor per-container stats — no native exporter ships in BaseHarbor. Marked unavailable with a reason, never a fabricated healthy panel.

## Implementation

- File: internal/metrics/perses_dashboards_hosts.go (own write-set, disjoint from #1597's perses_dashboards.go).
- File: internal/metrics/perses_dashboards_hosts_test.go.
- testdata: internal/metrics/testdata/perses-dashboard-hosts/*.json (golden witnesses per panel).
- CLI: added `HostContainersDashboards` field to cmd/baha/app_status_result.go applicationStatusResult (own struct field, no shared-file mutation of #1597).

## Acceptance witnesses

- Test catalog real-backend-only: only the 3 real backends ship host/container panels; host node metrics marked unavailable. (TestPersesHostDashboardCatalogHasRealBackendsOnly)
- Test perses-native JSON shape per panel. (TestPersesHostDashboardPersesNativeJSON)
- Test marshalling determinism. (TestPersesHostDashboardJSONIsDeterministic)
- Test unavailable entry marshals a reason document naming the missing signal. (TestPersesHostUnavailableEntryMarshalsReason)
- Test panel keys match selection catalog keys (lock-step with 080). (TestPersesHostDashboardKeysMatchSelectionCatalogKeys)
- Test golden files byte-for-byte per entry. (TestPersesHostDashboardGoldenFiles)
- Test CLI status --json exposes host/container dashboards with the unavailable face. (TestBahaStatusHostContainersDashboardsExposesUnavailable)

## Focused test run (recorded below)

- go build ./... 
- go vet ./internal/metrics/ ./cmd/baha/
- go test ./internal/metrics/ -run TestPersesHost -v
- go test ./cmd/baha/ -run TestBahaStatusHostContainersDashboardsExposesUnavailable -v

## CI coverage

- New tests run under the standard go test CI group. State any required .github workflow change as a finding with file:line (Owner scope) — do not edit .github/**.

## repo-rule compliance

- Stacked only on 080 head; no #1597 files touched; disjoint write-set.
- No exporter enabled; no application capability added; Perses stays a management surface.
- No .github/** touched. No container/probe at test time (Go unit tests only, no Docker/Podman).
- Perses three-state seam untouched.

## Cleanliness

- All state under /tmp/opencode/w077/ (worktree + build). No containers, no compose projects, no network. No orphans.

## END

STATE (dependency blocks active->review transition): t-20261114-r28-perses-dashboard-selection in `wait` (NOT accepted) — prerequisite per depends_on; cannot move this card to review until accepted. No code change required by me to unblock; reported per scope-split.

## base attestation

base head: `85b4cbb598272e28944e48b6895ce8935031c9ba` (origin head of lane-0428-080-r28-perses-selection). Show this SHA is an ancestor of my first commit and that git log lists only my own commits (see END ls-remote + git log witness).
