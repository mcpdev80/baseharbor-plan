---
id: t-20261018-r27-stage-versions
card_number: "0427-055"
card_short_title: "isolate version and Conf per"
areas: [state]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: coord-welle5 (Lane w197, freigegeben)
kanban_lane: closed
kanban_summary: "Persist desired, last applied and observed release/component references independently for application identity + selected Target…"
kanban_status: closed
kanban_title: "0427-055 · isolate version and Conf per"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-app-binding, t-20261018-r27-candidate-contract, t-20261018-r27-state-owner, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1391]
sources: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1391"]
---

- [x] t-20261018-r27-stage-versions · Deployments: isolate version and configuration per stage #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/state #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w197, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1391](https://github.com/mcpdev80/baseharbor/pull/1391)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1391)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md)  
**Owner:** coord-welle5 (Lane w197, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1391](https://github.com/mcpdev80/baseharbor/pull/1391)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Persist desired, last applied and observed release/component references independently for application identity + selected Target + environment. Reuse root intent and complete envs/<env>/baseharbor.yaml semantics; no new overlay DSL. Target != stage != version; support several environments on one target and different targets/installations, no runtime-name-based prod policy. Target owns placement preferences; each stage uses its own configuration, scoped secret references/consumer identity and data owner, with explicitly authorized sharing only. One checkout may submit different revisions without rewriting another deployment. Preserve IDs through version changes; Git SHA is optional for image-only inputs. Tests run three different versions simultaneously and changing one never touches the others. Source/schema versions are app-owned; image rollback is not database rollback.

This is a real extension of deployment release/configuration state, not merely a presenter or lock change. Extend the existing Environment-keyed deployment records through the accepted state-owner seam: specify desired/applied/observed component references, configuration revision and scoped references, persistence/reopen behavior, incomplete/failed transition semantics and isolation. Reuse DeploymentIdentity, DeploymentSource and existing applied/observed fields where sufficient; stage is the user-facing environment concept, not another identity dimension. Do not store secret values in release inventories or create a parallel coreinstallation store. The candidate contract fixes the minimal typed extension before assignment.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

internal/application/environment.go; bounded deployment release-selection/revision files and tests under internal/deployment/; cmd/baha/app_context.go serialized after state-owner. Reserved paths for this slice only; proposed filenames are fixed in the accepted contract predecessor before assignment. Shared command/HTTP/MCP/help/golden registrations belong to public-surfaces. If another write owner is needed, coordinate and serialize before implementation; no branch-to-branch dependencies or duplicate state.

## Required checks

Three-version state/reopen tests, same-target two-environment isolation, different-target/installation conflicts, complete-env fallback and shared-provider boundaries; deterministic filesystem/contract tests first. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.

## Runde 1 pruefbar 2026-11-05 (kopf 13192efa5d5)
Nachgemessen: ls-remote echt==head, develop VORFAHR (rc=0), lauf 42103327299 TERMINAL SUCCESS am exakten
kopf, akte round-1.md auf main (nach nachforderung — urspruenglich ungecommittet gelassen, beleg-pflicht
wirkt). Matrix 3x unabhaengigkeit, beide trennungs-/stale-mutanten rot, zusammenbau echter lebenszyklus.

## Rueckruf (1391a REJECT): der ECHTE lebenszyklus-pfad verwirft applied/intended beim erzeugen
neuer referenz-maps — produkt-defekt, nicht nur testluecke. Matrix- und mutantennachweise fehlen. Rezept
in review-1391a.md.

## Runde 2 pruefbar 2026-11-06 (kopf 60d5896c9c4)
Nachgemessen: ls-remote echt==head, develop 21d8d05cf1a VORFAHR (rc=0), lauf 42131821530 TERMINAL SUCCESS
am exakten kopf, akte round-2.md traegt jetzt die finalen zeugen (END-zeile blieb alt — messe gilt,
praeszedenz w185). Datenverlust-fix load-merge-refs drin, matrix+beide mutanten rot belegt.

## ACCEPT 2026-11-06 (1391b + head-followup): merge UNTERWEGS (ac51c8819c9); schliesst bei develop-beleg.

## Gemerged 2026-11-06 (CODEX-MERGE nach 1391b+followup ACCEPT): develop f01d2fbdea6, kanditat
ac51c8819c9 (nach vorwaerts-revert des querverbund-commits). Gewuenschte/angewandte/beobachtete referenzen
getrennt haltbar + datenverlust-fix. Abhaengige (version-view, maintenance-client) pruefen bereitchaft.
