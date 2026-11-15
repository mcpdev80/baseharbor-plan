# t-20261114-r28-perses-dashboard-selection (0428-080) — Perses dashboard selection catalog

**Lane:** lane-0428-080-r28
**Card:** t-20261114-r28-perses-dashboard-selection (0428-080, release v0.4.28), claimed active
**Base (stack head):** Core `lane-0428-075-perses-seam` = `af308e66d38ad1204345bbe83d066dd7548ea6e6`
**Candidate head:** `85b4cbb598272e28944e48b6895ce8935031c9ba` (single commit, only my commit)
**PR:** draft #1590 — https://github.com/mcpdev80/baseharbor/pull/1590 (base = seam branch `lane-0428-075-perses-seam`, isDraft=true)
**Evidence path:** `baseharbor-plan/evidence/r28-welle1-2026-11-15/perses-selection/mission-080.md`

> Evidence provenance (Owner rules): evidence lives ONLY in baseharbor-plan, never in the product repo. No `.evidence/` directory anywhere. No `.github/**` edited, no reruns/workflow_dispatch, no subagents. Base verified via fresh clone in /tmp + `git ls-remote`, never via the quarantined workers/baseharbor checkout.

## PLAN

- Read mission + task card; verify reality via `git ls-remote` (planning repo origin/main = `b716206578`, baseharbor seam head `af308e66d`, seam PR #1575 = DRAFT/unmerged) and read signal-inventory akte + seam source at af308e66d.
- Claim t-20261114-r28-perses-dashboard-selection via plan.py (owner lane-0428-080-r28) and commit+push the claim on origin/main BEFORE editing code.
- Cut candidate branch lane-0428-080-r28-perses-selection from af308e66d; record base SHA as ancestor proof of first commit; add `perses_selection.go` catalog + versioned templates + tests in the baseharbor worktree (/tmp/perses-selection-wt).
- Build + vet locally; run focused tests (match / missing-metrics / unauthorized provider / other Targets / stale registry / fail-closed) in the worktree; fix red until green.
- Write evidence (PLAN / result / repo-rule compliance / witnesses) into the planning repo evidence path; ensure every new test is CI-covered or report the exact .github change as a finding (Owner scope).
- Open a draft PR (base = seam branch af308e66d; retarget if needed); verify commit provenance (origin/main is an ancestor; log lists only own commits); END post via `codeman agent post`.

## Verified starting points

- Card (0428-080): Goal — define eligibility + provisioning for Perses-native dashboards from real signal/label inventory and authorized providers. Scope: dedicated selection code, versioned templates, tests; no implicit exporter enablement. Supersedes grafana-dashboard-selection under the Perses-replaces-Grafana v0.4.28 decision.
- Dependency `t-20261114-r28-perses-signal-inventory`: accepted/closed. Dependency `t-20261114-r28-perses-contract-seam`: state `wait` — APPROVED on af308e66d (act-1575-review-r8), **merge frost** (PR #1575 is a Draft on base develop; 8 commits ahead of develop, unmerged). plan.py claim accepted the claim and moved state to active.
- Signal inventory akte (develop `0e9ccb582`): the ONLY real BaseHarbor metrics signal is `up{job="baseharbor-applications",...}` (file_sd scrape job). Provider exporter `/metrics` fixed ports: OTel collector 8888, Loki 3100, Tempo 3200, Keycloak 9000. PostgreSQL/Valkey metrics = `requires-adapter` (no native export). No alerting in Core. No dashboards/ folder, no panel+layout, no Perses datasource ref anywhere. Perses dashboard needs (a) a Prometheus/Loki/Tempo datasource ref, (b) >=1 panel with `spec.queries`, (c) a layout.
- Seam at af308e66d (`internal/capability/perses.go`): pinned Perses release v0.55.1 + image + PrometheusPluginVersion v0.6.0, three-state public status contract (`not_configured` / `configured_unverified` / `verified` — only the first two ever produced here), fail-closed `ValidatePersesRelease`, `PersesManagementSurfaceNow(selected)` grounded in manifest truth, `Reachability = unverified`.
- `internal/capability/reference.go` real observability signals: Prometheus (`prometheus-metrics`, unsupported natively; scrape via `baseharbor-providers`/`baseharbor-applications`), Loki (`loki-metrics` supported native), Tempo (`tempo-metrics` supported native), Keycloak (supported), PostgreSQL/Valkey (`requires-adapter`).

## Result

Added a deterministic Perses-native dashboard selection catalog keyed on the accepted pinned release and the real backend signal inventory.

**Files (2, +524/-0), no `.github/**`:**
- `internal/capability/perses_selection.go`
  - `DefaultDashboardCatalog()` — shipped catalog with a template per real BaseHarbor backend (prometheus-targets, loki-logs, tempo-traces). `requires-adapter` backends (PostgreSQL/Valkey) are intentionally absent — never provisioned.
  - `EligibleFor(key, persesSelected, backendSignals)` — fail-closed verdict: returns `not_eligible` with a concrete reason for unselected Perses, unpinned/unsupported release, missing backend signal, or unknown/missing dashboard key; `eligible` only when selected + valid pin + real backend signal present.
  - `DashboardEligibility.Status()`, `DashboardStatus` (`eligible` / `not_eligible`), public filter + ordering helpers, seam-pin lockstep assertion.
- `internal/capability/perses_selection_test.go` — match, missing-metrics, unauthorized/unselected, missing-signal, unknown-key, stale version, unknown-owner fail-closed, deterministic ordering, seam-pin lockstep.

**No exporter enablement; Perses stays a management surface, never an application capability.** No container probe.

### Acceptance mapping (per card §Acceptance)
- **Verified pinned Perses release + native plugin/format:** catalog keys on v0.55.1 (current security fixes), never assumes Grafana UI APIs or dashboard JSON are Perses-compatible.
- **Scope by actual Target/tenant permissions, fail closed:** selection fail-closed on unselected/unpinned/missing-signal/unknown-key; no new application capabilities or mandatory services forced.
- **Preserve Prometheus/Loki/Tempo backend ownership:** thin selection catalog; data owners keep their own signal inventory. No owned resources removed.
- **No native alerting/routing parity claimed:** no alerting defined; no external notifications enabled.

## Required checks / CI coverage

- **Local (self-run, observed):** `go build ./...` EXIT 0; `go vet ./internal/capability/` EXIT 0; `go test ./internal/capability/ -run 'Perses|Dashboard'` PASS; full `./internal/capability/` package PASS. Candidate commit `85b4cbb59`.
- **Durable CI proof:** new files fall through the trusted PR classifier `scripts/pr-gate-plan.py` to the **conservative fallback** (`CONSERVATIVE_CHECKS`), which selects `go-unit-tests` (`go test ./...`), `go-vet` (`go vet ./...`), `go-build` (`go build ./...`) on PR to develop. This is the default for unknown/valid narrow paths — **no `.github/**` change required**. Every new test therefore runs under `go-unit-tests` on PR push to develop (workflow `ci.yml`, job `pr_unit_shards`, route `scripts/pr-unit-database.sh` → `--mode packages`).
- **Repo-rule finding (Owner scope):** none. No `.github/**` file touched; no rerun/workflow_dispatch.

## Repo-rule compliance

- **One integration candidate per chain:** single branch `lane-0428-080-r28-perses-selection`, single commit `85b4cbb59`. No second branch.
- **Branch provenance:** cut from af308e66d (stack head); af308e66d is a confirmed ancestor of the candidate head (merge-base exit 0). Candidate has only my own commit (ancestry-path ahead of base lists only `85b4cbb59`). No foreign candidate carried on top.
- **Base attestation:** planning repo `origin/main` = `b716206578` (verified fresh clone + ls-remote); baseharbor seam base `af308e66d` (confirmed ancestor of candidate).
- **Evidence location:** evidence lives ONLY in baseharbor-plan under `evidence/r28-welle1-2026-11-15/perses-selection/`; no `.evidence/` dir in the product repo.
- **No `.github/**` edits; no reruns; no subagents.**
- **environment.json / identity paths:** read-only inspection only, never restructured.
- **Merge frost respected:** PR #1590 is a DRAFT; the seam is NOT merged (frost honored).

## Witnesses

- Planning repo `origin/main`:
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote -h origin refs/heads/main` → `b716206578d8817a2d2cdf311172795d8ba526a0`
  (Note: the `workers/` bookkeeping repo's `origin/main` collides with a phantom SHA `aff1532c`; the true planning main is `b716206578`, confirmed via `-C` absolute path and fresh clone.)
- Baseharbor seam head: `af308e66d38ad1204345bbe83d066dd7548ea6e6` (`lane-0428-075-perses-seam`), unmerged (8 commits ahead of develop).
- Candidate on GitHub: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-080-r28-perses-selection` → `85b4cbb598272e28944e48b6895ce8935031c9ba`.
- PR #1590 (gh): base `lane-0428-075-perses-seam`, `isDraft=true`, head `lane-0428-080-r28-perses-selection`, 2 files +524/-0, commit `85b4cbb59`.
- Provenance: `git merge-base --is-ancestor af308e66d origin/lane-0428-080-r28-perses-selection` → exit 0 (0=yes).

## END

- lane-0428-080-r28 DONE — candidate `85b4cbb59`, draft PR #1590 (base seam branch, draft). Merge frost on the seam respected (no merge). CI runs under `go-unit-tests` on PR to develop.
