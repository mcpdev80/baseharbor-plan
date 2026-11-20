---
id: t-20261120-r28-ci-stacked-base-conditions
card_number: "0428-180"
card_short_title: "CI on real stacked bases"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Codex (baseharbor-pr-sweep-fortsetzen)
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-180 · CI on real stacked bases
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1594", "mcpdev80/baseharbor#1615"]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44735405029"]
---

- [x] t-20261120-r28-ci-stacked-base-conditions · CI: stacked PRs on cli2-*/w0* base branches get no exact-head checks #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Codex (baseharbor-pr-sweep-fortsetzen)  
    **PR:** [baseharbor#1594](https://github.com/mcpdev80/baseharbor/pull/1594), [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44735405029)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex (baseharbor-pr-sweep-fortsetzen)  
**Priority:** not set  
**PRs:** [baseharbor#1594](https://github.com/mcpdev80/baseharbor/pull/1594), [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
**Source:** 
<!-- /generated:links -->

## Owner decision (2026-11-20, option B — authorization for .github/**)

"Gestapelte PRs sollen CI auf den tatsaechlichen Basisbranches erhalten. Basis-Branches werden nicht bloss umbenannt, um
den Workflow-Filter zu umgehen. Zuerst die verwendeten Basis-Branch-Namen und die betroffenen Job-Bedingungen erfassen,
dann gezielt erweitern und mit einem gestapelten PR nachweisen, dass exakte Head-Checks laufen. Bis der Nachweis
vorliegt, gelten gestapelte PRs ohne exakten CI-Lauf als nicht abnahmefaehig." This card is that work item; it is the
exception to AGENTS 4.5 ("workflow files belong to the Owner") for exactly the files named below.

## Measurement at develop 96f2ae11a25a (coordinator, this tick)

Historical baseline at develop 96f2ae11: the pull_request filter already listed develop, main, lane-*, cli2-* and w0*, while only develop/lane-* job conditions were present. The PR branches below now carry the widened routing; see the current run evidence appended below.

- ci.yml:431, :481, :517 (gate plan / selected checks / source-quality family)
- ci.yml:714 (aggregate), :976, :1000, :1032, :1075 (native and runtime cell families)
  each: `github.base_ref == 'develop' || startsWith(github.base_ref, 'lane-')`

Base branches actually in use by open stacked PRs (gh api pulls, state=open):

- cli2-env-policy-head → #1615 (0428-057, 14 red/absent checks), #1627 (0428-055, draft), #1620 (0428-067, draft)
- cli2-identity-secrets-head → #1625 (0428-065, draft), #1623 (0428-063, draft)
- w083-perses-datasources → #1665 (0428-082, draft, parked by 0428-176)

So the workflow starts on these PRs but the check graph conditions evaluate false: no exact-head evidence. That is why
0428-176 was blocked on a write-set conflict instead of being restacked and accepted.

## Acceptance

1. Keep the real PR base names. Extend the existing workflow branch trigger and every non-main job guard on both stack branches to cover the bases actually in use (`cli2-*`, `w0*`), preserving `develop` and `lane-*`. Main-only release guards stay unchanged. The parent branch has 17 non-main guards; the newer child has 18 because it includes the integration-gate family.
2. Exact-hosted proof on stacked PR #1615: the exact head `ca930ce63c4ff080a736c6e3439dc1d87d017e0c` and base `cli2-env-policy-head` at `bfa7d80fafc71f9b4d773dbbcb0cd043239da9e1` ran workflow [44735405029](https://github.com/mcpdev80/baseharbor/actions/runs/44735405029). `PR · Native gate plan`, `PR Selected Checks`, and all four `PR · Go unit · cli-0/1/2/3` completed on this exact head; the latter five required checks failed. This proves trigger/guard routing only, not feature acceptance.
3. The workflow guards include `w0*`. The only open w0-based PR, #1665 on `w083-perses-datasources`, remains Draft/parked; draft guards intentionally skip selected checks and Go shards. No second hosted w0 proof is available without a separate eligible PR or owner state transition, so preserve that limitation.
4. Existing workflow-policy validation passed on both branches. No product behavior, branch name, gate, or runner was changed.

## Resolution

The branch routing defect is verified fixed: a real stacked CLI PR now executes its exact-head check graph instead of silently skipping it. The exact graph is red for separate product/runtime-fixture failures, so #1615 is not accepted and no PR is merged by this CI-only resolution. Per the Owner decision, every other stacked PR without its own exact-head CI remains unaccepted. The `w0*` source routing is in place, with the Draft-only hosted-proof limitation recorded above.

## Boundaries

Only .github/workflows/ci.yml (plus the planner script only if the condition lives there). No product code, no test
changes, no gate deletion, no runner work. If a needed condition lives outside ci.yml (reusable workflow, org settings),
report file:line to the coordinator and stop.
