---
id: t-20261017-release-0-4-26-publish
type: acceptance
areas: [release]
release: v0.4.26
version: v0.4.26
release_stage: publish
parent: v0.4.26
owner: Codex (Owner-authorized v0.4.26 publication)
priority: normal
depends_on: [t-20261017-release-0-4-26-qualify]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor#1089]
sources: []
blocker: ""
resolution: superseded
evidence: [https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26, https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/releases/v0.4.26.md]
superseded_by: t-20261026-v0426-owner-publication-closeout
---

- [x] t-20261017-release-0-4-26-publish · v0.4.26 · Release: promote the approved candidate and deliver exact tagging commands #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** Codex (Owner-authorized v0.4.26 publication) · **Priority:** normal  
    **PR:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
    **Needs:** [t-20261017-release-0-4-26-qualify](t-20261017-release-0-4-26-qualify.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/releases/v0.4.26.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.26](../releases/v0.4.26.md) (v0.4.26)  
**Depends on:** [t-20261017-release-0-4-26-qualify](t-20261017-release-0-4-26-qualify.md)  
**Required by:** [t-20261017-release-0-4-26-verify](t-20261017-release-0-4-26-verify.md)  
**Owner:** Codex (Owner-authorized v0.4.26 publication)  
**Priority:** normal  
**PRs:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
**Source:** 
<!-- /generated:links -->

# v0.4.26 board closeout — 2026-10-26

The normal gated lifecycle route is superseded by the [accepted Owner-directed publication closeout](t-20261026-v0426-owner-publication-closeout.md). Actual publication and verification are complete; this does not assert complete pre-release qualification. The original dependency chain is retained as historical data.

Marcel explicitly directed publication despite incomplete/failing CI and subsequently requested cleanup of the remaining release cards. v0.4.26 is published; the release tag and delivered source remain unchanged.

## Preserved history

[Pre-closeout task and all original scope, evidence and handoffs](https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/tasks/t-20261017-release-0-4-26-publish.md). This immutable history is retained in Git; old active-run statements are not current work instructions.

## Actual release

[Stable release](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26) · [successful publisher run](https://github.com/mcpdev80/baseharbor/actions/runs/40355992335) · [promotion PR #1089](https://github.com/mcpdev80/baseharbor/pull/1089). No new tests, runtime jobs or release operations were started for this Planning cleanup.
