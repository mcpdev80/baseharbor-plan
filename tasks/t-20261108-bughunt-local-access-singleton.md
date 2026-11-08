---
id: t-20261108-bughunt-local-access-singleton
card_number: "0427-155"
card_short_title: "Local targets cannot be isolat"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-local-core"
kanban_status: active
kanban_lane: active
kanban_summary: "Decision card: document the single-core boundary in help/docs with the exact error and the multi-target way out…"
kanban_title: 0427-155 · Local targets cannot be isolat
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1481]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd5.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-local-access-singleton · Bug Hunt v0.4.27: One host, one local access #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-local-core · **Priority:** normal  
    **PR:** [baseharbor#1481](https://github.com/mcpdev80/baseharbor/pull/1481)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd5.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-local-core  
**Priority:** normal  
**PRs:** [baseharbor#1481](https://github.com/mcpdev80/baseharbor/pull/1481)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Decision card: document the single-core boundary in help/docs with the exact error and the multi-target way out (remote/connector targets), or scope a follow-up epic for per-target local isolation; no silent behavior change; if documented: regression on the message/path.

## Problem (source evidence in the dossier)
All local-access targets share one core runtime and one provider/deployment registry: a second target with a different provider/reference fails on the access singleton (config.yaml local access is a singleton; fresh targets fall back to the shared core). Source: hunt H-D5 ARCHITEKTUR-GRENZE-BF (cuts 1/3/4 unreachable on a single host).

## Acceptance
Decision card: document the single-core boundary in help/docs with the exact error and the multi-target way out (remote/connector targets), or scope a follow-up epic for per-target local isolation; no silent behavior change; if documented: regression on the message/path.

## Dependencies and file ownership
None. Write-set: docs + target/access registry help.


## Architecture-decision implementation — 2026-11-08

- Owner `chatgpt-r27-local-core`. [PR #1481](https://github.com/mcpdev80/baseharbor/pull/1481): documents one local Core per host and the safe separate-host Connector alternative in English/German CLI docs; strengthens the exact local-access conflict message without relaxing admission.
- Regression test on error/next-step message; does **not** claim independent local Core per Target was implemented. CI exact-head pending, card remains active.
- Existing `superseded_by` pointer is historical and not automatically a completed decision; preserve until acceptance reconciliation.
