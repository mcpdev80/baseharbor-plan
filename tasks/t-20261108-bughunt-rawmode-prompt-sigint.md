---
id: t-20261108-bughunt-rawmode-prompt-sigint
card_number: "0427-145"
card_short_title: "Ctrl-C breaks raw prompt"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: SIGINT at a raw prompt = clean cancel with message and restored terminal; signal regression in the existing field.
kanban_title: 0427-145 · Ctrl-C breaks raw prompt
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md"]
---
- [ ] t-20261108-bughunt-rawmode-prompt-sigint · Bug Hunt v0.4.27: Ctrl-C breaks raw prompt #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
SIGINT at a raw prompt = clean cancel with message and restored terminal; signal regression in the existing field.

## Problem (source evidence in the dossier)
At the Project location prompt the path input runs in raw mode (path_prompt_linux.go, ICANON/ECHO/ISIG off): Ctrl-C ends without an Interrupted line and the terminal stays raw until process exit. Source: hunt H-P1 BF-10.

## Acceptance
SIGINT at a raw prompt = clean cancel with message and restored terminal; signal regression in the existing field.

## Dependencies and file ownership
None. Write-set: cmd/baha path prompt raw mode.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (zuerklaeren): the missing Interrupted line was observed non-deterministically; the deterministic part (terminal restore) is what acceptance must pin. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)
