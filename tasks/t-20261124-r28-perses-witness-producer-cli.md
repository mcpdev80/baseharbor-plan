---
id: t-20261124-r28-perses-witness-producer-cli
card_number: "0428-265"
card_short_title: "backend witness never proven"
type: bug
areas: [metrics, observability, cli]
release: v0.4.28
version: ""
parent: ""
owner: Codex (w118-0428-265)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: Make the configured verdict of PersesBackendWitness reachable through real observation instead of a hard-coded empty witness.…
kanban_title: 0428-265 · backend witness never proven
priority: ""
depends_on: [t-20261119-r28-perses-status-backend-witness]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "Owner-CI-mapping dependency: scripts/pr-gate-coverage.json:147 requires an Owner-owned source coverage row for internal/metrics/perses_dashboards_hosts.go before Trusted Plan can select checks; cmd/baha status sources also remain unresolved at scripts/pr-gate-plan.py:1420-1424."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-perses-witness-producer-cli · PersesBackendSignalWitness is passed as a zero-value literal at every CLI call site, so the configured verdict is unreachable on every status surface. #task #release/v0-4-28 #status/blocked #view/blocked #area/cli #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (w118-0428-265)  
    **Blocker:** Owner-CI-mapping dependency: scripts/pr-gate-coverage.json:147 requires an Owner-owned source coverage row for internal/metrics/perses\_dashboards\_hosts.go before Trusted Plan can select checks; cmd/baha status sources also remain unresolve…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-perses-status-backend-witness](t-20261119-r28-perses-status-backend-witness.md)  
**Required by:** [t-20261124-r28-app-status-unauthorized-live-probe](t-20261124-r28-app-status-unauthorized-live-probe.md), [t-20261124-r28-perses-state-spelling-drift](t-20261124-r28-perses-state-spelling-drift.md)  
**Owner:** Codex (w118-0428-265)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F4+F5 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

Make the `configured` verdict of `PersesBackendWitness` reachable through real observation instead of a hard-coded empty witness. Witnessed on develop 3ebfb90d:

- `cmd/baha/perses_lifecycle.go:366` (`baha app perses status`) passes the literal `metricsprovider.PersesBackendSignalWitness{}`.
- `cmd/baha/app_status_result.go:328` (remote face) and `:436` (local face) pass the same literal; `internal/metrics/perses_dashboards_hosts.go:338` and `:612` use the same zero-value internally.
- With all three `Proven` fields false (`internal/metrics/perses_dashboards_hosts.go:546-555`), `persesBackendSignalWitnessFromManifest` (`cmd/baha/app_status_result.go:117`) can never answer `configured`: every declared backend shows `unreachable` even on a fully working stack (False-Red on both the human and the machine surface).
- Grep on develop: no production call site anywhere constructs a witness with a `Proven` field set — the producer the surfaces claim to consume does not exist.
- The comment at `cmd/baha/app_status_result.go:112-116` defers the probe to "card 0428-143"; that card closed as #1729 with a different scope (Verification=none semantics), so the deferral is stale — this card is the missing wiring.

## Acceptance

1. One witness producer derives `PrometheusProven` / `LokiProven` / `TempoProven` from real backend answers (the per-signal probe paths already in `internal/metrics`), not from manifest declaration alone; every CLI call site (`perses_lifecycle.go:366`, `app_status_result.go:328`, `:436`) passes it instead of the literal.
2. One executable regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit"): with a scripted answering backend the JSON shows `configured` for that backend; with a silent backend it shows `unreachable`. Fail-closed in both directions, never an inferred `configured`.
3. The stale "card 0428-143" comment is replaced by a reference to this card's wiring.
4. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

## Boundaries

`cmd/baha/app_status_result.go`, `cmd/baha/perses_lifecycle.go`, a witness producer in `internal/metrics` (the `perses_dashboards_hosts.go` family) and their tests. No new manifest fields, no new state holders. The human and machine faces must keep sharing the one witness (0428-142 rule).

## Related

- F4 and F5 verified real on develop 3ebfb90d (see goal); the zero-value literal is the only witness any call site passes.
- Sequel to 0428-142 (`perses status` backend witness, accepted): the shape landed there, this card lands the producer. The 0428-143 comment the dossier called stale is NOT this card's scope (that card closed accepted as #1729, Verification=none semantics); its witness deferral is resolved here.
- Probe unification is card [0428-263](t-20261124-r28-perses-backend-status-real-probe.md); use whichever probe path it fixes.


## Handoff

Claimed by Codex (w118-0428-265) and published as Planning commit ac53222e9. A product candidate at `e8cf352e25e2d8c3ce2e34e29f2de6a3c753b74f` was briefly evaluated in PR #1829, then closed without merge and its branch deleted after Hosted CI showed that the implementation's test route was not operational. No product changes are retained.


## Befund — Hosted CI routing

- Static rule only: `scripts/pr-gate-plan.py:1407-1414` maps `cmd/baha/*_test.go` to `CLI_PACKAGE_CHECKS`; `scripts/pr-gate-plan.py:90-91` defines `cli-package-tests` as `go test ./cmd/baha -count=1`. That selection rule alone does not prove an operational Hosted CI test route.
- The product source paths are not resolved by that test rule. `scripts/pr-gate-plan.py:1420-1424` routes `cmd/baha/*.go` sources to `cli-unresolved-runtime-impact`. In addition, `scripts/pr-gate-coverage.json:147` starts the `components` catalog, and the candidate's `internal/metrics/perses_dashboards_hosts.go` change has no source row. Trusted Plan therefore rejects the candidate before Go unit checks execute.
- Proposed selector diff only (NOT applied; scripts/** remains Owner-scope):

```diff
--- a/scripts/pr-gate-plan.py
+++ b/scripts/pr-gate-plan.py
@@
-        elif path.startswith('cmd/baha/') and path.endswith('.go'):
+        elif path in ('cmd/baha/perses_lifecycle.go',
+                      'cmd/baha/app_status_result.go'):
+            area = 'perses-status-witness'
+            require(CLI_PACKAGE_CHECKS + CODE_CHECKS + CLI_CHECKS + WIZARD_BASE_CHECKS)
+        elif path.startswith('cmd/baha/') and path.endswith('.go'):
```

The earlier continuation claim was disproven by this actual Hosted CI result. Implementation remains held because the existing route was not proven to execute tests for this candidate.

- Hosted CI evidence: [run 45459222545](https://github.com/mcpdev80/baseharbor/actions/runs/45459222545), candidate `e8cf352e25e2d8c3ce2e34e29f2de6a3c753b74f`, PR [#1829](https://github.com/mcpdev80/baseharbor/pull/1829). `PR · Trusted Plan` and `PR Selected Checks` failed. Trusted Plan reported `uncataloged source change, no declared runtime gate owner: internal/metrics/perses_dashboards_hosts.go` and suggested source id `source.internal_metrics_perses_dashboards_hosts_go`, path `internal/metrics/perses_dashboards_hosts.go`, surfaces `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`. `PR · Go unit` shards were skipped, so `cli-package-tests` and the regression tests did not run. PR #1829 was closed unmerged, the branch was deleted, and the product candidate was removed from the working tree.
- Owner-scope catalog mapping proposal (NOT applied): add the source row above to `scripts/pr-gate-coverage.json` at the `components` catalog beginning at line 147. Owner-CI-mapping dependency remains blocking.
- Exact proposed selector-line diff (NOT applied; `scripts/**` remains Owner-scope):

```diff
--- a/scripts/pr-gate-plan.py
+++ b/scripts/pr-gate-plan.py
@@ -1420,1 +1420,5 @@
-        elif path.startswith('cmd/baha/') and path.endswith('.go'):
+        elif path in ('cmd/baha/perses_lifecycle.go',
+                      'cmd/baha/app_status_result.go'):
+            area = 'perses-status-witness'
+            require(CLI_PACKAGE_CHECKS + CODE_CHECKS + CLI_CHECKS + WIZARD_BASE_CHECKS)
+        elif path.startswith('cmd/baha/') and path.endswith('.go'):
```
