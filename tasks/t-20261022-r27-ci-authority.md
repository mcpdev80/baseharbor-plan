---
id: t-20261022-r27-ci-authority
card_number: "0427-063"
card_short_title: "authority"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: coord-welle3 (lane w41)
kanban_lane: closed
kanban_summary: ""
kanban_status: closed
kanban_title: "0427-063 · authority"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261103-ci-plain-checks]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1354h.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/codex-merge-1354a.md"]
---

- [x] t-20261022-r27-ci-authority · Deferred trusted CI readiness: authority #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle3 (lane w41) · **Priority:** critical  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1354h.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/codex-merge-1354a.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md)  
**Required by:** [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-execution-journal](t-20261018-r27-execution-journal.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md)  
**Owner:** coord-welle3 (lane w41)  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

# Deferred trusted CI readiness: authority

## Observable outcome and preconditions
Qualify only missing domain-specific trusted selection, execution and verification for accepted product interfaces. Wait for the accepted normal CI baseline and this card's product/startup dependencies; do not expand gates to keep workers busy during the current repair.

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
W1: existing trusted domain mapping and actual test discovery; W2: bounded producer/executor and domain-local fixture; W3: normal required-job result handling and relevant negatives. Coordinator reserves exact files from the actual accepted product interface before assigning writes. Shared central files have one writer; Use a flexible shared worker pool; coordinator reserves non-overlapping files and runner capacity. Independent ready domains may be prepared in disjoint files without a blanket ci-lanes lock.

## Acceptance and exclusions
Actual selected checks execute and fail on missing/invalid required coverage; source/integration/ref and runner isolation stay authenticated. Record available accepted check identity for dependent product slices. Execute the affected checks directly; no full matrix, wildcard allowlist, self-reported green, unqualified new lane or duplicate authority. Run only targeted native checks justified by the actual scope and available isolated runners.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman is resumed by the Owner; the coordinator preserves claims and unpublished work and assigns small non-overlapping iterations under the current order. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-ci-authority.md) remain immutable history, not competing operational instructions.

## Owner update 2026-10-29

Separate current CI baseline readiness from later tests of product interfaces that do not yet exist. Coordinator records the real dependency graph and coverage mapping; no fabricated readiness or blanket product development before the new CI cutover. Assign only bounded independent slices with exclusive files.

## Current CI contract — 2026-11-03

The Owner retires the evidence and receipt approval chain. This task supplies only the missing ordinary test selection/execution for its domain. Job results flow through normal dependencies; no gate manifests, archived-run verification or evidence reuse. The only CI receipt is merge SHA plus PR number. The replacement baseline task remains open until its actual checks pass.


## Coordinator-Vermerk 2026-11-04 00:30 (w75 runde 14, plattenbelegt)
- head c0febdd1: B2+B3 GELIEFERT und gruen (fragment=uncertain; sync/close-fehler => rollback, kein event).
- B1 (retention-budget vs. alle-aktiven-unter-cap) = OWNER-ENTSCHEIDUNG ausstehend (optionen 1/2/3 im
  schichtprotokoll 23:20). Lane released; nach entscheidung frische korrektur-lane.


## Owner-Entscheid B1 2026-11-04 (PR #1354 comment 10:26Z): OPTION 1 genehmigt
- 16-MB-budget UNVERAENDERT; im test aeltere gross-buchungen in terminal/finished state laufen lassen
  (newest-per-id bleibt klein). Umsetzung: neue lane auf work/r27-ci-authority-ab, danach luna abschluss.


## Abschluss-Vermerk 2026-11-04 (coord f49a3303)
- CODEX-REVIEW ABSCHLUSS verdict=ACCEPT open=none auf head 5a5f1b38 (evidence/r27-night-2026-11-02/review-1354h.md).
- CODEX-MERGE: PR #1354 squash-merged, develop bb9bc0ef, post-merge checks 19 pass / 0 fail.
- B1 nach Owner-Entscheid Option 1 (Budget 16 MiB unveraendert, aeltere Eintraege terminal im Test).
