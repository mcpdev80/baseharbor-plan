---
id: t-20261117-hunt-signals-102
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-102"
title: "application-Klasse fehlt in der Signal-Registry"
kanban_status: blocked
kanban_lane: blocked
kanban_title: 0428-102 · App-Klasse fehlt in der
kanban_summary: ""
sources: []
source_note: "hunt hunt-signals befund-1 (akte: evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)"
depends_on: []
owner: Codex
blocker: "PR #1677 Docker observability gate failed; awaiting terminal workflow logs before remediation or rerun."
wait_reason: ""
resolution: ""
superseded_by: ""
prs: [mcpdev80/baseharbor#1677]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md", "https://github.com/mcpdev80/baseharbor/pull/1677", "https://github.com/mcpdev80/baseharbor/actions/runs/44031866829"]
card_short_title: App-Klasse fehlt in der
---

- [ ] t-20261117-hunt-signals-102 · application-Klasse fehlt in der Signal-Registry #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** Codex  
    **PR:** [baseharbor#1677](https://github.com/mcpdev80/baseharbor/pull/1677)  
    **Blocker:** PR \#1677 Docker observability gate failed; awaiting terminal workflow logs before remediation or rerun.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44031866829)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261117-hunt-signals-103](t-20261117-hunt-signals-103.md), [t-20261117-hunt-signals-104](t-20261117-hunt-signals-104.md)  
**Owner:** Codex  
**Priority:** not set  
**PRs:** [baseharbor#1677](https://github.com/mcpdev80/baseharbor/pull/1677)  
**Source:** 
<!-- /generated:links -->

Einzelschritte in der referenzierten hunt-akte (befund-1.md); Umsetzung als normale task-kette (claim -> branch -> CI -> evidence -> review).


## Test binding

- **Test binding (select exactly one):** ☑ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Tests: `internal/observability.TestListApplicationMetricsRequiresExplicitClassAndApplicationScope`; `internal/metrics.TestBindWritesAttributedTargetAndPrunesOnlySameApplication`; `internal/metrics.TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata`; existing `internal/metrics.TestWorkloadOnlyRegistersSharedSnapshotOnDeploy`.
- Local route: `go test ./internal/observability ./internal/metrics -count=1` passed at PR head `58db26baf9dcd80566dcbb0042eed2818e5af822`; `go vet ./internal/observability ./internal/metrics` passed. Compile-only checks for updated List call sites in `cmd/baha` and `internal/identityprovider` passed.
- CI trigger/route: Ready PR #1677 with changed Go source paths selected `PR · Go unit · packages`, `PR · Go unit · owner`, `PR · Validation · go-build`, `PR · Validation · go-vet`, and `PR · Validation · identity-provider-package-tests`. Run [44031866829](https://github.com/mcpdev80/baseharbor/actions/runs/44031866829) is exact-head. Go unit shards, package/owner unit checks, build, vet, identity-provider package checks and Docker identity passed. Docker observability failed. The parent PR check is still in progress, so its failure logs are not yet available; no rerun has been started.
- The CI plan selected Docker observability for this PR; no Podman runtime job was selected. Acceptance remains open until the failure is diagnosed and applicable exact-head checks are green.
