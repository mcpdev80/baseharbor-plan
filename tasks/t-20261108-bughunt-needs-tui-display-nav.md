---
id: t-20261108-bughunt-needs-tui-display-nav
card_number: "0427-143"
card_short_title: "TUI rows break silently"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-needs-tui"
kanban_status: active
kanban_lane: active
kanban_summary: Back navigation visible; wrap-safe rows; choicesForSelection errors surfaced instead of swallowed; key hint consistent (p vs P);…
kanban_title: 0427-143 · TUI rows break silently
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1476]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md"]
---
- [ ] t-20261108-bughunt-needs-tui-display-nav · Bug Hunt v0.4.27: TUI rows break silently #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Back navigation visible; wrap-safe rows; choicesForSelection errors surfaced instead of swallowed; key hint consistent (p vs P); one regression per point in the existing tui field.

## Problem (source evidence in the dossier)
needs-TUI shows no visible back path (cancel only), provider rows wrap past 120 columns (appProviderChoice.View), rows are silently swallowed when choicesForSelection() errors (app_wizard_controller.go:329-339), and the hint prints capital P for a lowercase key. Source: hunt H-P1 BF-02/BF-08/BF-09/BF-11.

## Acceptance
Back navigation visible; wrap-safe rows; choicesForSelection errors surfaced instead of swallowed; key hint consistent (p vs P); one regression per point in the existing tui field.

## Dependencies and file ownership
None. Write-set: cmd/baha tui needs-screen + provider choice views.


## PR-/CI-Übernahme — 2026-11-08

- Owner: `chatgpt-r27-needs-tui`; Umsetzung im [PR #1476](https://github.com/mcpdev80/baseharbor/pull/1476) auf Basis `develop` `4786c541`.
- Behebt Key-Hinweise (`p`, `b/←`), vorherige Zeile, zu lange Provider-Zeilen und versteckte `choicesForSelection`-Fehler. Regressionstests ergänzt.
- Exact-Head-CI noch ausstehend. Kein Merge, keine Acceptance und kein Closed bis zum vollständigen PASS. Karte bleibt Active.
