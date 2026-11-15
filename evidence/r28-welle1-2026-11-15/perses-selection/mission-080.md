# t-20261114-r28-perses-dashboard-selection (0428-080) — Perses dashboard selection catalog

**Lane:** lane-0428-080-r28
**Card state claimed:** active (claimed via plan.py, committed + pushed on origin/main)
**Base (stack head):** Core `lane-0428-075-perses-seam` = `af308e66d38ad1204345bbe83d066dd7548ea6e6`
**Candidate branch:** `lane-0428-080-r28-perses-selection` (cut from af308e66d)

> Evidence provenance (Owner rules): evidence lives ONLY in baseharbor-plan, never in the product repo. Base verified via fresh clone in /tmp + `git ls-remote`, never via the quarantined workers/baseharbor checkout. No `.github/**` edited, no reruns/workflow_dispatch, no subagents.

## PLAN

- Read mission + task card; verify reality via `git ls-remote` (planning repo origin/main = `b716206578`, baseharbor seam head `af308e66d`, seam PR #1575 = DRAFT/unmerged) and read signal-inventory akte + seam source at af308e66d.
- Claim t-20261114-r28-perses-dashboard-selection via plan.py (owner lane-0428-080-r28) and commit+push the claim on origin/main BEFORE editing code.
- Cut candidate branch lane-0428-080-r28-perses-selection from af308e66d; record base SHA as ancestor proof of first commit; add `perses_selection.go` catalog + versioned templates + tests in the baseharbor worktree (/tmp/perses-selection-wt).
- Build + vet locally; run focused tests (match / missing-metrics / unauthorized provider / other Targets / stale registry / fail-closed) in the worktree; fix red until green.
- Write evidence (PLAN / result / repo-rule compliance / witnesses) into the planning repo evidence path; ensure every new test is CI-covered or report the exact .github change as a finding (Owner scope).
- Open a draft PR (base = seam branch af308e66d; retarget if needed); verify commit provenance (origin/main is an ancestor; log lists only own commits); END post via `codeman agent post`.

## Verified starting points

- Card: `t-20261114-r28-perses-dashboard-selection` (0428-080, release v0.4.28). Goal: define eligibility + provisioning for Perses-native dashboards from real signal/label inventory and authorized providers. Scope: dedicated selection code, versioned templates, tests; no implicit exporter enablement. Supersedes the grafana-dashboard-selection card under the Perses-replaces-Grafana v0.4.28 decision.
- Dependency `t-20261114-r28-perses-signal-inventory`: accepted/closed. Dependency `t-20261114-r28-perses-contract-seam`: state `wait` — APPROVED on af308e66d (act-1575-review-r8), **merge frost** (PR #1575 is a Draft on base develop; 8 commits ahead of develop, unmerged). plan.py claim still accepted the claim and moved state to active.
- Signal inventory akte (develop `0e9ccb582`): the ONLY real BaseHarbor metrics signal is `up{job="baseharbor-applications",...}` (file_sd scrape job). Provider exporter `/metrics` at fixed ports for OTel collector (8888), Loki (3100), Tempo (3200), Keycloak (9000). PostgreSQL/Valkey metrics = `requires-adapter` (no native export). No alerting in Core. No dashboards/ folder, no panel+layout, no Perses datasource ref anywhere. Perses dashboard needs (a) a Prometheus/Loki/Tempo datasource ref, (b) >=1 panel with `spec.queries`, (c) a layout.
- Seam at af308e66d (`internal/capability/perses.go`): pinned Perses release v0.55.1 + image + PrometheusPluginVersion v0.6.0, three-state public status contract (`not_configured` / `configured_unverified` / `verified` — only the first two ever produced here), fail-closed `ValidatePersesRelease`, `PersesManagementSurfaceNow(selected)` grounded in manifest truth, `Reachability = unverified`.
- Seam PR #1575 files touched: `internal/capability/perses.go`, `internal/metrics/management_ui.go`, `internal/application/management_ui.go`, `cmd/baha/app_perses_cli_test.go`, manifest + render + validation, specs. My selection catalog must key on the accepted Perses version and real provider/label/permission requirements from the inventory.
- `internal/capability/reference.go`: real observability signals per provider — Prometheus (`prometheus-metrics`, unsupported natively; scrape via `baseharbor-providers`/`baseharbor-applications`), Loki (`loki-metrics`, supported native), Tempo (`tempo-metrics`, supported native), Keycloak (supported), PostgreSQL/Valkey (`requires-adapter`).

## Base attestation

- Cut candidate branch from af308e66d38ad1204345bbe83d066dd7548ea6e6.
- origin/main (planning repo) = b716206578d8817a2d2cdf311172795d8ba526a0 (verified fresh clone + ls-remote); seam PR #1575 head af308e66d NOT an ancestor of baseharbor develop (merge frost confirmed).

## END

- lane-0428-080-r28 PENDING
