---
id: t-20261114-r28-perses-secure-access
card_number: "0428-089"
card_short_title: "Protect Perses operator access"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: review
kanban_lane: review
kanban_summary: "Integrate Perses with existing management access, verified transport and authorization; inspect selected upstream version…"
kanban_title: 0428-089 · Protect Perses operator access
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1599]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/7230e623033812ce2f5027ca029761ebf485b06a/evidence/r28-welle1-2026-11-15/perses-secure-access/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1599-0428-089.md"]
---

- [ ] t-20261114-r28-perses-secure-access · Protect Perses operator access #task #release/v0-4-28 #status/review #view/review #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** coord · **Priority:** normal  
    **PR:** [baseharbor#1599](https://github.com/mcpdev80/baseharbor/pull/1599)  
    **Needs:** [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/7230e623033812ce2f5027ca029761ebf485b06a/evidence/r28-welle1-2026-11-15/perses-secure-access/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1599-0428-089.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md)  
**Required by:** [t-20261114-r28-perses-contact-routing](t-20261114-r28-perses-contact-routing.md), [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** coord  
**Priority:** normal  
**PRs:** [baseharbor#1599](https://github.com/mcpdev80/baseharbor/pull/1599)  
**Source:** 
<!-- /generated:links -->

## Goal

Integrate Perses with existing management access, verified transport and authorization; inspect selected upstream version security and proxy SSRF protections.

## Scope and file ownership

Dedicated gateway/auth policy adapter; no privileged anonymous exposure or secret leakage. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/serviceaccess/http_gateway.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/http_gateway.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)
- [internal/application/management_ui.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/management_ui.go)
- [internal/metrics/management_ui.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/management_ui.go)

Use existing management/UI authorization and TLS; validate authentication, denied identities, isolation and endpoint trust. Review pinned Perses upstream release security and restrict datasource proxy SSRF/credential exposure. Do not invent unverified token mode.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Integrate Perses with existing management access, verified transport and authorization; inspect selected upstream version security and proxy SSRF protections.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

candidate 872c6c70 on lane-welle2-089-perses-secure-access, draft PR #1599 against base lane-0428-075-perses-seam (cb4367f3). 59 Perses cells pass; one failing check in internal/metrics reported as STATE and assigned to 0428-075.

delivered: 872c6c70 draft; base-defekt (seam r3) haengt an 075-korrektur

kandidat 2c44db837 (documentation-audit-fix, DE-rows ergaenzt), exact-head run 44058489510 SUCCESS (coord-uebernahme nach lane-idle), state behind => hopf in merge-welle

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1599-0428-089.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'
