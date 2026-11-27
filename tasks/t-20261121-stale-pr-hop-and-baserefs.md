---
id: t-20261121-stale-pr-hop-and-baserefs
card_number: "0428-216"
card_short_title: "0428-216 stale PR hops"
type: task
areas: [ci, coordination]
release: v0.4.28
version: ""
parent: ""
owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)
kanban_status: wait
kanban_lane: wait
kanban_summary: "Every open PR that belongs to a Codeman card is either a descendant of current develop, or carries the base ref its card…"
kanban_title: 0428-216 · 0428-216 stale PR hops
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "lane released; awaiting Codex/Owner content disposition under the 2026-11-27 sweep resume (per-card holds apply)"
resolution: ""
evidence: []
---

- [ ] t-20261121-stale-pr-hop-and-baserefs · 0428-216 hop the stale PRs of our cards and fix their base refs #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/coordination #kind/task
    <!-- generated:card -->
    **Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds) · **Priority:** normal  
    **Waiting:** lane released; awaiting Codex/Owner content disposition under the 2026-11-27 sweep resume (per-card holds apply)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Every open PR that belongs to a Codeman card is either a descendant of current `develop`, or carries the base ref its card
declares - so CODEX-MERGE can act inside the window without rediscovering staleness per PR.

## Why

H-V25 measured all 30 open PRs with patch-ids (akte
`evidence/bug-hunt-2026-11-21/duplicate-superseded-desk/round-1.md`): **no duplicate exists**, but twelve non-draft PRs of
our cards are not descendants of current develop, and five PRs have a base ref that is not develop
(`#1730` -> `lane-0428-143-verify-none`, `#1684` -> `perses-tmpfs-mountpoint-wt`, `#1665` ->
`lane-0428-083-datasources-r2`, `#1625`/`#1623` -> `cli2-identity-secrets-head`). Two of the five are correct stacking
(§3.3.8), the others are leftovers. The desk's sentence "1732/1734 unrelated content" is corrected here: both PRs add the
same `ExistingTLSMaterial`/`client-cert` fixture material (#1734 supersedes #1732, which is closed).

## Scope

Allowed:

- `git push --force-with-lease` on the **lane branches of Codeman-owned cards only**, after `merge-base --is-ancestor` was
  recorded per PR
- `gh pr edit <n> --base <ref>` where the card's `depends_on` declares a different base lane (stacked PRs keep their stack)

Forbidden:

- any PR whose card is Owner-held: #1614, #1615, #1650/#1606 (0428-078), #1731, #1704 (0428-073) - list them, do not touch
- closing PRs (only the coordinator closes, after proof), and `.github/**` / `scripts/**` content changes

## Acceptance criteria

1. A table in the evidence: `PR | card | base-ref vorher | ancestor(entwickelt)? vorher | aktion | base-ref nachher |
   ancestor nachher`, one row per open PR of a Codeman card.
2. Every action names the command that proved it before and after (`git merge-base --is-ancestor`, `gh pr view --json baseRefName`).
3. Stacked PRs are re-stated as stacked, not flattened: after a base merge, the follow-up lanes hop - documented in §3.3.8.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | PR Selected Checks on each affected PR |
| Test identifier | `0428-216` |
| Route | `new check/catalog not needed - metadata only` |

## Stop and report

If a hop would require touching a file an Owner rail owns, stop at that PR, record it in the table, continue with the next.

## Handoff

Evidence: `evidence/r28-welle4-2026-11-21/stale-pr-hop-and-baserefs/round-1.md`. No product commit by this card is
expected; if one appears, the card was exceeded.

COMMISSIONED from hunt H-V25: metadata + hop sweep over our own PRs, hard-bounded to PRs whose card has no live session (no force-push under a working lane).
