---
id: t-20261018-r27-remote-material
card_number: "0427-051"
card_short_title: "project exposure material to"
areas: [providers]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: 0427-051-exposure-node
kanban_lane: closed
kanban_summary: Build remote provider/exposure/TLS projections using existing provider owners. Secrets/keys remain protected at required…
kanban_status: closed
kanban_title: "0427-051 · project exposure material to"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-artifact-resolution, t-20261018-r27-candidate-ingress, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1418]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-material/act-1418c-merge.md", "https://github.com/mcpdev80/baseharbor/pull/1418"]
---

- [x] t-20261018-r27-remote-material · Remote providers: project exposure material to the actual target #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/providers #kind/task
    <!-- generated:card -->
    **Owner:** 0427-051-exposure-node · **Priority:** normal  
    **PR:** [baseharbor#1418](https://github.com/mcpdev80/baseharbor/pull/1418)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-material/act-1418c-merge.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1418)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [t-20261018-r27-remote-docker-web](t-20261018-r27-remote-docker-web.md)  
**Owner:** 0427-051-exposure-node  
**Priority:** normal  
**PRs:** [baseharbor#1418](https://github.com/mcpdev80/baseharbor/pull/1418)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Build remote provider/exposure/TLS projections using existing provider owners. Secrets/keys remain protected at required execution boundary; no provider on developer machine and no forced management service set. Preserve receiver/consumer/rotation consequences and required native protocols; describe supported limit explicitly. Do not enable the broad remote guard yet.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/application/remote_application_projection.go; remote_runtime_projection.go; bounded exposure/material files and tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Projection/ownership/secret-leak/TLS material fixtures; bounded protocol probe where cryptographic consumption cannot be proven by fixtures. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

bahn nach system-reboot frisch beauftragt (takeover der toten lane), konfliktfreie produkt-/testarbeit unter aufgehobenem basis-HOLD (develop 934be499b), .github weiterhin owner-tabu

kandidat efb6c2d2c auf develop 934be499b (vor-reboot von w287 geliefert, uebernahme-bahn hat konvergiert + nichts neu gepusht); akte round-1..4 auf main; docker+podman-runtime-zellen SKIPPED am kopf — CODEX-REVIEW prueft ausdrucklich ob das ein CI-aufnahmepflicht-reject ist (AGENTS 5.3).

CODEX act-1418a REJECT am kopf efb6c2d2c: go-unit gruen, aber (a) echte produktmaengel runtime_postgres.go exposure-only ohne gateway + gateway ohne Caddy-serving + rotation/node-consumption ohne verhaltensabdeckung, (b) docker+podman runtime-zellen SKIPPED weil .github/ci.yml:171-176,213-218 sie auf push-refs beschraenkt (OWNER-Scope, im END als befund gemeldet). frische korrektur-bahn 0427-051-exposure-node dispatched.

single-owner caddy.go gelandet: head a91debbb0 auf develop 934 (ancestor), totes round-4 duplikat efb6c2d2c ersetzt, F1/F2/F3 behoben, run 4984 terminal, go-unit deckt internal/exposure, runtime cells skipped=owner-gate, akte round-5 auf main. re-review act-1418b.

PR #1418 merged unchanged as eee11d50b7a7b55675a282f03d4a1a78e4511cf0; accepted head a91debbb047d6ea7a0f258194c0a3474978687bd verified as ancestor of develop. Review and merge evidence are published under evidence/r27-welle5-folge-2026-11-06/remote-material/.

CODEX act-1418b ACCEPT + act-1418c MERGE in develop (eee11d50b7a7b55675a282f03d4a1a78e4511cf0). single-owner caddy.go serving route + node rotation regression; F1/F2/F3 erfuellt.
