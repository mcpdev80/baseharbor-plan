---
id: t-20261108-bughunt-0427-appnew-contradictory-exit
card_number: "0427-125"
card_short_title: "App new: Erfolg plus Fehler"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: "0427-125 · App new: Erfolg plus Fehler"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [ ] t-20261108-bughunt-0427-appnew-contradictory-exit · 0427-125 · App new meldet Erfolg plus Fehler #task #release/v0-4-27 #status/planned #view/ready #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
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

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-1 podman2 hunt on develop 0fe53052: wizard-completed run prints success then an restore-required error at exit; string is composed, repro in the act.

## Acceptance

app new exits with exactly one truthful verdict (success XOR actionable error + next command); no success+error pairing; regression covers the exit path.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.
