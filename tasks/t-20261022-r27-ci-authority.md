---
id: t-20261022-r27-ci-authority
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-evidence-acceptance]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-ci-authority · Deferred trusted CI readiness: authority #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** t-20261017-release-0-4-27-updates, [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** t-20261017-release-0-4-27-updates, [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-execution-journal](t-20261018-r27-execution-journal.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

# Deferred trusted CI readiness: authority

## Observable outcome and preconditions
Qualify only missing domain-specific trusted selection, execution and verification for accepted product interfaces. Wait for the accepted automatic receipt skeleton and this card's product/startup dependencies; do not expand gates to keep workers busy during the current repair.

## Covered slices
- authority-contract
- state-owner
- mutation-lock
- execution-journal
- journal-wiring
- app-binding
- candidate-ingress
- management-host

## Parallel work split when assignable
W1: existing trusted domain mapping and actual test discovery; W2: bounded producer/executor and domain-local fixture; W3: result/receipt verification and relevant negatives. Coordinator reserves exact files from the actual accepted product interface before assigning writes. Shared central files have one writer; Use a flexible shared worker pool; coordinator reserves non-overlapping files and runner capacity. Independent ready domains may be prepared in disjoint files without a blanket ci-lanes lock.

## Acceptance and exclusions
Actual selected checks execute and fail on missing/invalid required coverage; source/integration/ref and runner isolation stay authenticated. Record available accepted check identity for dependent product slices. Reuse valid compatible evidence; no full matrix, wildcard allowlist, self-reported green, unqualified new lane or duplicate authority. Run only targeted native checks justified by the actual scope and available isolated runners.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman is resumed by the Owner; the coordinator preserves claims and unpublished work and assigns small non-overlapping iterations under the current order. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-ci-authority.md) remain immutable history, not competing operational instructions.

## Owner update 2026-10-29

Separate current CI baseline readiness from later tests of product interfaces that do not yet exist. Coordinator records the real dependency graph and coverage mapping; no fabricated readiness or blanket product development before the new CI cutover. Assign only bounded independent slices with exclusive files.
