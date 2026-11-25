---
id: t-20261125-hunt45-cli-unknown-command-hardening
card_number: "0428-325"
card_short_title: "unknown-command exit-2"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-325 · unknown-command exit-2
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/cli/cli.go#L145-L190","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/commands.go#L20-L40","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/intake-1.md"]
---

- [x] t-20261125-hunt45-cli-unknown-command-hardening · CLI: unknown-command hardening #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/cli/cli.go#L145-L190), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/commands.go#L20-L40), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/intake-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Disposition

DROP after current-source recheck at `3a2ae6b1139570c98b8924e3b19975c56a289400`. The proposed runnable-parent edge case is not exercised by the shipped command tree: the root and current subcommands with children dispatch through those children, and no current command combines a runnable action with child commands. The remaining proposal is helper deduplication plus defensive rejection of blank hints; the intake did not show a shipped blank-hint caller or incorrect user-visible suggestion. This is maintenance hardening without a release defect. Reopen only if a concrete command reproduces the behavior.

## Source finding

H-V45 F6 was explicitly classified as latent because no shipped parent combines a runnable action with child commands. F9 identified duplicate suggestion construction and a renderer that skips blank hints, but no shipped caller with a blank hint or incorrect suggestion. Source and call-site evidence is recorded in the [H-V45 intake](../evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/intake-1.md).
