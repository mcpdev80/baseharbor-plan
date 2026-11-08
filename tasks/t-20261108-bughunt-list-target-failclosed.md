---
id: t-20261108-bughunt-list-target-failclosed
card_number: "0427-148"
card_short_title: "List needs target choice"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Decision documented (keep fail-closed OR add an all-targets view with a target column); if kept: quickstart/help line mentions…"
kanban_title: 0427-148 · List needs target choice
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1466]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42480521183", "https://github.com/mcpdev80/baseharbor/commit/ad49d2d2129657e2e09c40b534c6a8030413a083"]
---
- [ ] t-20261108-bughunt-list-target-failclosed · Bug Hunt v0.4.27: List needs target choice #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-cli-diagnostics · **Priority:** normal  
    **PR:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-cli-diagnostics  
**Priority:** normal  
**PRs:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Decision documented (keep fail-closed OR add an all-targets view with a target column); if kept: quickstart/help line mentions the behavior; regression covers the chosen semantics.

## Problem (source evidence in the dossier)
baha list without BASEHARBOR_TARGET fails closed when more than one target is configured (the error text with choices+Next is correct, but it stalls quickstart flows on multi-target setups). Source: hunt H-D4 BF-hd4-3 (low).

## Acceptance
Decision documented (keep fail-closed OR add an all-targets view with a target column); if kept: quickstart/help line mentions the behavior; regression covers the chosen semantics.

## Dependencies and file ownership
None. Write-set: cmd/baha list + target docs.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (zuerklaeren): fail-closed was called intentional in the dossier; open owner PR #1466 documents it - decision may reduce to a docs line. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)


## Acceptance — 2026-11-08

- [PR #1466](https://github.com/mcpdev80/baseharbor/pull/1466) merged into `develop`: `ad49d2d2129657e2e09c40b534c6a8030413a083`; exact PR head `daacddbbe9d011c3fd48ae7cc798e560dd591258`.
- [CI #42480521183](https://github.com/mcpdev80/baseharbor/actions/runs/42480521183): terminal SUCCESS (Go-unit, build, vet, source/docs checks, native Docker/Podman destroy-retry). No standalone end-to-end deployment result is claimed.
- Retains Target fail-closed default; help identifies existing `baha list --all-targets` read-only inventory with Target column and target activation. TestListHelpExplainsFailClosedTargetSelection and existing target-list ambiguity tests PASS. No cross-target implicit mixing.
- `resolution: accepted`; no active worker claim remains.
