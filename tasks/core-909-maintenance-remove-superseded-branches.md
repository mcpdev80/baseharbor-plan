---
id: core-909
areas: [maintenance]
type: maintenance
release: maintenance
version: ""
parent: ""
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#909"]
source_updated: "2026-10-15T16:47:13Z"
labels: [kind/maintenance]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-909 · Maintenance: safely remove superseded branches #task #release/maintenance #status/planned #view/ready #area/maintenance #kind/maintenance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [maintenance](../releases/maintenance.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#909](https://github.com/mcpdev80/baseharbor/issues/909)
<!-- /generated:links -->

## Goal

Remove verified-superfluous branches; every remaining branch has a justified owner, work or evidence purpose. Not a product feature or release blocker.

## Scope

- Maintainer decision (2026-10-15): remove all archived remaining branches except `main`, `develop`, `feature/kubernetes-runtime-foundation`, `test/kubernetes-adoption-contract-demo` and any macOS/Darwin work. A complete mirror backup including the original branch refs is held by the Maintainer locally (path recorded in the source snapshot). 14 branches had already been removed per the local deletion log; 37 further refs were planned for archive-backed removal. This is deliberate archive cleanup, not proof that every historical change is in develop; open bugs stay open and their old sources remain in the mirror. Release tags and Actions evidence are not deleted.
- Rules before each removal: each branch exists in the mirror at exactly the current remote SHA; new/changed branches, new open PRs and new macOS/Kubernetes work are kept; historical candidate/evidence refs leave the remote inventory but keep their Git states in the mirror; keep the mirror safe for later verification.
- Already done (per source): draft #861 closed (selective integration via #837); Renovate PRs #724/#779/#782 and single updates #725/#778 closed (the pending host-trust checkout/Alpine update is **not** delivered and stays visible in the dependency dashboard, see [external tooling](../migration/external-tooling.md)); duplicate dashboard #17 closed; #616 kept open (real Kubernetes pre-freeze proof); core-750/751/752 and core-754/766/815 kept open.
- The 55-branch inventory with audit SHAs (develop `33b7ca94b42cc45e908c0d964cfbe0cc8349f231`, main `54acc4b66715681213788fdba395a569ddc95a1b`) is in the [source snapshot](../migration/source-snapshot/baseharbor/909.json).

## Acceptance

- Re-check branch heads, open PRs, new commits and active sessions before execution; never delete an old audit SHA blindly.
- Preserve main lines, open #616 pre-work and active task branches; do not merge branches merely to get rid of them.
- Remove only confirmed candidates individually at their unchanged SHA; no wildcard deletion or force-push.
- Afterwards re-read the remote inventory and document every actually removed ref with its original SHA and reason.
- No claim "branches cleaned up" while only the inventory exists. No new product/release CI runs for this hygiene task.

## Required checks

- Remote branch inventory before and after; mirror presence per SHA.

## Dependencies and file ownership

- No task dependencies. Needs authenticated GitHub access for ref deletion.

## Handoff

- Observed 2026-10-15T20:35Z during this migration: the remote has 8 branches (`develop`, `main`, `feature/kubernetes-runtime-foundation`, `test/kubernetes-adoption-contract-demo` and active task branches `task/895-review-protection`, `work/v0.4.26-893-pr-check-enforcement`, `work/v0.4.26-896-isolated-pr-runners`, `work/v0.4.26-910-read-context`). The removal therefore appears executed; **the per-ref deletion record (original SHA + reason) is not yet documented** — record it here to accept this task.
