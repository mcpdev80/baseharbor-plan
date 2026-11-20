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
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-180 · CI on real stacked bases
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1594", "mcpdev80/baseharbor#1615"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44735405029"]
---

- [ ] t-20261120-r28-ci-stacked-base-conditions · CI: stacked PRs on cli2-*/w0* base branches get no exact-head checks #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** Codex (baseharbor-pr-sweep-fortsetzen)  
    **PR:** [baseharbor#1594](https://github.com/mcpdev80/baseharbor/pull/1594), [baseharbor#1615](https://github.com/mcpdev80/baseharbor/pull/1615)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44735405029)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
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

The pull_request FILTER is already wide — .github/workflows/ci.yml lines 14-22: develop, main, 'lane-*', 'cli2-*', 'w0*'.
The JOB CONDITIONS were never widened, they still test only develop/lane-*:

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

1. One edit in .github/workflows/ci.yml: replace the repeated `base_ref == 'develop' || startsWith(base_ref,'lane-')`
   condition at the eight lines above with a single documented expression that also covers the stacked bases in use
   (`startsWith(github.base_ref,'cli2-')` and `startsWith(github.base_ref,'w0')`), preferably via one workflow-level env
   or reusable condition so future stacks cannot silently miss a job again. Main-only conditions (ci.yml:557, :606, :630,
   :655) stay untouched.
2. PROOF, not assertion: one stacked PR whose base is a `cli2-*-head` (use #1615 or #1623) shows `PR Selected Checks`,
   `PR · Go unit · packages` and the gate-plan aggregate completed with a headSha equal to the PR head. Record run id,
   head sha, job names, executed-vs-skipped in the evidence file (AGENTS 5.3).
3. A second proof point: one PR based on a `w0*` branch (e.g. #1665 base) shows the same, or the card documents why a
   `w0*` base cannot be covered without a separate change.
4. gofmt/readability of any touched script helpers; the existing workflow-lint/self-test cell must be green.

## Boundaries

Only .github/workflows/ci.yml (plus the planner script only if the condition lives there). No product code, no test
changes, no gate deletion, no runner work. If a needed condition lives outside ci.yml (reusable workflow, org settings),
report file:line to the coordinator and stop.
