---
id: t-20261117-workload-only-metrics-source-unregistered
card_number: "0428-100"
card_short_title: "deploy of a workload-only app"
type: task
areas: []
release: v0.4.28
version: ""
parent: v0.4.28
owner: codex
kanban_status: active
kanban_lane: active
kanban_summary: "Before the fix, real EnsureRuntime deployment of a workload-only app left the shared Prometheus runtime-sources.json empty, so…"
kanban_title: 0428-100 · deploy of a workload-only app
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1676]
sources: []
source_note: "contract-ruling (coord 2026-11-17): workload-only Prometheus source is snapshot-only; see task Handoff contract-ruling and review-2 evidence"
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/workload-only-registration/round-4.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/workload-only-registration/round-3.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/workload-only-registration/review-2.md"]
---

- [ ] t-20261117-workload-only-metrics-source-unregistered · Runtime: deploy of a workload-only app registers no metrics source in shared runtime-sources snapshot #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** codex  
    **PR:** [baseharbor#1676](https://github.com/mcpdev80/baseharbor/pull/1676)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/workload-only-registration/round-4.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/workload-only-registration/round-3.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/workload-only-registration/review-2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** codex  
**Priority:** not set  
**PRs:** [baseharbor#1676](https://github.com/mcpdev80/baseharbor/pull/1676)  
**Source:** 
<!-- /generated:links -->

## Goal

Before the fix, real `EnsureRuntime` deployment of a workload-only app left the shared Prometheus `runtime-sources.json` empty, so downstream dashboard/identity signal discovery had no runtime identity to report. The workload has no declared service, port, or scrapeable `/metrics` endpoint. Owner decision (2026-11-17): represent this as logical snapshot metadata only; do not invent a scrape target.

One or two sentences: the observable outcome.

## Scope

- In scope: register an app-owned workload identity in the shared runtime source snapshot through the actual deploy path; ensure the symbolic `runtime://<project>/workload` value is never emitted as a Prometheus file_sd target or provider network attachment; retain service-app registration compatibility.
- Out of scope: inventing a workload service, port, exporter, or `/metrics` endpoint; changing verification of real scrape-enabled provider sources.

## Acceptance

- A workload-only real deploy produces a non-empty shared runtime source snapshot with the expected app-owned logical workload identity.
- The logical identity is metadata only: it is absent from Prometheus file_sd targets and provider network projection; `VerifyProviderSourcesAt` succeeds without attempting to scrape it.
- Existing real scrape-enabled provider sources continue through the normal verification path; no verification is skipped for those sources.
- Service-app deploy registration remains compatible.
- Regression tests exercise `EnsureRuntime -> EnsureProviderFiles -> snapshot assertion -> VerifyProviderSourcesAt`; no manual registry update or mirrored helper may stand in for deployment.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- r3-owner: codex (parallel-autorisiert 2026-11-17T04:17Z)
- 2026-11-17 owner clarified the contract: workload-only runtime identity is logical snapshot metadata, with no invented scrape endpoint; real scrape sources retain normal verification. PR #1676 head `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c` passed exact-head run [44018836577](https://github.com/mcpdev80/baseharbor/actions/runs/44018836577) and local build/vet/package tests. Review-1 `CHANGES_REQUESTED` is superseded by this explicit owner decision; Codex requested a sequential review-2 against the revised card acceptance. PR is not merged pending review-2.
## contract-ruling (coord 04:5xZ)

Snapshot-only registration ist der gebilligte contract fuer workload-only apps: source erscheint im snapshot-metadata, aber NICHT als scrape-target (file_sd/network/query) — ein erfundener endpoint waere der gemeldete perpetually-down-bug. Evidenz-pflicht: positiver absence-test im generierten file_sd + unveraenderte pruefung echter endpoints. Review hat gegen diesen contract zu pruefen.

## round-4 progress (Codex + Codeman, 2026-11-17)

- Product commit `178b8a00aa72acd11c29499038834bdbcc0fb038` pushed to PR #1676 after merging current develop `2581000b5fdb78f4af577fc13ce1205ca32a84e8`.
- Added Compose network absence coverage for workload-only registration, retained service-app network compatibility coverage, and added a query recorder proving the real endpoint source still reaches verification while the logical workload ID is not queried. Existing provider-network fixture now declares a real metrics source.
- Targeted package tests, `go test ./internal/application ./internal/metrics`, `go build ./cmd/baha`, `go vet ./internal/application ./internal/metrics`, and `git diff --check` passed locally. Exact-head PR run [44022175082](https://github.com/mcpdev80/baseharbor/actions/runs/44022175082) is running on `178b8a00`; this is the only valid CI run for the changed head.
- Separate review-3 requested. Status remains active until exact-head CI is green and review-3 passes. No merge yet.
