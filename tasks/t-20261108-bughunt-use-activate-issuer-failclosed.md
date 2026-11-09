---
id: t-20261108-bughunt-use-activate-issuer-failclosed
card_number: "0427-162"
card_short_title: "use/activate fails closed when"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-178-rebase
kanban_status: active
kanban_lane: active
kanban_summary: "Selection reconciles issuer state the way the read path already does (status works): either re-establishes/derives the issuer…"
kanban_title: 0427-162 · use/activate fails closed when
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1489, mcpdev80/baseharbor#1510]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-use-activate-issuer-failclosed · Bug Hunt v0.4.27: Select fails without issuer #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-178-rebase · **Priority:** normal  
    **PR:** [baseharbor#1489](https://github.com/mcpdev80/baseharbor/pull/1489), [baseharbor#1510](https://github.com/mcpdev80/baseharbor/pull/1510)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-178-rebase  
**Priority:** normal  
**PRs:** [baseharbor#1489](https://github.com/mcpdev80/baseharbor/pull/1489), [baseharbor#1510](https://github.com/mcpdev80/baseharbor/pull/1510)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Selection reconciles issuer state the way the read path already does (status works): either re-establishes/derives the issuer from the live Core or offers a named recovery command that actually exists; never a dead-end error pointing at an unreachable subcommand. Regression per branch in the cli-surface/lifecycle group.

## Problem (source evidence in the dossier)
A running target whose state dir has no service-access/issuer (fresh bootstrap, partial install, moved state) cannot be selected at all: use/activate error "installation not verifiable ... fails closed" even though status reports the Core READY on the same machine (BF-02, blocker candidate). The error also points at an unreachable "core install" command. Sources: cmd/baha/use_target.go:61-112, internal/coreinstallation/authority.go:356-396 and :73, cmd/baha/target.go:249.

## Acceptance
Selection reconciles issuer state the way the read path already does (status works): either re-establishes/derives the issuer from the live Core or offers a named recovery command that actually exists; never a dead-end error pointing at an unreachable subcommand. Regression per branch in the cli-surface/lifecycle group.

## Dependencies and file ownership
None. Write-set: target selection / coreinstallation authority paths.
