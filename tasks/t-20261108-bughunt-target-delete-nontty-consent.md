---
id: t-20261108-bughunt-target-delete-nontty-consent
card_number: "0427-164"
card_short_title: "target delete fails non-TTY ev"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0427-164 · target delete fails non-TTY ev
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1494]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42520608394", "https://github.com/mcpdev80/baseharbor/commit/b3a8042d18ea60f162a32a51df34a499cad6a237"]
---
- [x] t-20261108-bughunt-target-delete-nontty-consent · Bug Hunt v0.4.27: Target delete needs TTY #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1494](https://github.com/mcpdev80/baseharbor/pull/1494)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42520608394), [proof 3](https://github.com/mcpdev80/baseharbor/commit/b3a8042d18ea60f162a32a51df34a499cad6a237)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1494](https://github.com/mcpdev80/baseharbor/pull/1494)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
--yes honors non-TTY for the config-only delete with the same fail-closed semantics as the interactive flow; a real destructive step (if any remains) keeps its confirmation. Regression with shared cancel-path decision of 138/157.

## Problem (source evidence in the dossier)
target delete demands 2 interactive provider-impact confirmations and fails with impact-confirmation-required on non-TTY even with --yes, although the action is config-only and non-destructive to state (BF-03). Same consent-gate root cause as 0427-157 but on the delete path.

## Acceptance
--yes honors non-TTY for the config-only delete with the same fail-closed semantics as the interactive flow; a real destructive step (if any remains) keeps its confirmation. Regression with shared cancel-path decision of 138/157.

## Dependencies and file ownership
None. Write-set: target delete confirmation path.

## Accepted / merged — 2026-11-09

- [PR #1494](https://github.com/mcpdev80/baseharbor/pull/1494) squash-merged into `develop` as [`b3a8042d`](https://github.com/mcpdev80/baseharbor/commit/b3a8042d18ea60f162a32a51df34a499cad6a237), exact PR source head `95afe20411d6949335cb902f621c1cca5a7f8ec5`.
- [CI #42520608394](https://github.com/mcpdev80/baseharbor/actions/runs/42520608394) completed SUCCESS: Go unit, build, vet, formatting, PR Selected Checks and both **native Docker/Podman destroy-retry** jobs SUCCESS. Unrelated CI jobs skipped by selector are not treated as acceptance.
- Production `target delete NAME --yes` honors non-TTY config-only detach via CLI arg parsing and scoped consent; without yes, non-TTY refuses. Regression covers actual dispatcher `--yes` and `-y`, including refused no-yes.
- This is acceptance of the scoped **non-destructive target-definition detach**; it does not grant destructive data deletion without approval. No release or tag created.
