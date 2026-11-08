---
id: t-20261108-bughunt-rawmode-prompt-sigint
card_number: "0427-145"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: SIGINT am raw-prompt = sauberer abbruch mit meldung und wiederhergestelltem terminal; regression (signal-test) im bestehenden…
kanban_title: 0427-145 · app init Owner-Naht regression
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md"]
---
- [ ] t-20261108-bughunt-rawmode-prompt-sigint · Bug Hunt v0.4.27: Ctrl-C im Pfadprompt #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
SIGINT am raw-prompt = sauberer abbruch mit meldung und wiederhergestelltem terminal; regression (signal-test) im bestehenden feld.

## Problem (Fund aus Hunt H-P1, datei-/#beleg in der Akte)
Am raw-mode-pfadprompt (path_prompt_linux.go, ICANON/ECHO/ISIG aus) endet Ctrl-C ohne Interrupted-Meldung; terminal bleibt bis process-end im raw-zustand. Quelle Hunt H-P1 BF-10.

## Acceptance
SIGINT am raw-prompt = sauberer abbruch mit meldung und wiederhergestelltem terminal; regression (signal-test) im bestehenden feld.

## Dependencies and file ownership
Keine. Write-set: cmd/baha path prompt raw mode.
