---
id: t-20261019-v0426-complete-defect-audit
type: review
areas: [release, ci]
release: v0.4.26
version: ""
parent: v0.4.26
owner: Codex (Maintainer complete v0.4.26 defect audit)
priority: critical
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: ["mcpdev80/baseharbor#1085", "mcpdev80/baseharbor#1084", "mcpdev80/baseharbor-demo#124", "mcpdev80/baseharbor#1083", "mcpdev80/baseharbor#1077", "mcpdev80/baseharbor#1082", "mcpdev80/baseharbor#1076", "mcpdev80/baseharbor#1075", "mcpdev80/baseharbor#1074", "mcpdev80/baseharbor-node-connector#16", "mcpdev80/baseharbor-console#15", "mcpdev80/baseharbor-demo#123", "mcpdev80/baseharbor#1073", "mcpdev80/baseharbor#1072", "mcpdev80/baseharbor#1071", "mcpdev80/baseharbor-console#13", "mcpdev80/baseharbor-console#12", "mcpdev80/baseharbor-node-connector#13", "mcpdev80/baseharbor-console#11", "mcpdev80/baseharbor-node-connector#12", "mcpdev80/baseharbor#1070", "mcpdev80/baseharbor-demo#122", "mcpdev80/baseharbor-console#10", "mcpdev80/baseharbor-node-connector#11", "mcpdev80/baseharbor#1004", "mcpdev80/baseharbor#1005", "mcpdev80/baseharbor#1046", "mcpdev80/baseharbor#1047", "mcpdev80/baseharbor#1053", "mcpdev80/baseharbor#1058", "mcpdev80/baseharbor#1059", "mcpdev80/baseharbor#1050", "mcpdev80/baseharbor#1055", "mcpdev80/baseharbor#1056", "mcpdev80/baseharbor#1052", "mcpdev80/baseharbor#1060"]
sources: []
blocker: ""
resolution: superseded
evidence: [https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26, https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/releases/v0.4.26.md]
superseded_by: t-20261026-r27-v0426-acceptance-carryover
---

- [x] t-20261019-v0426-complete-defect-audit · Audit and repair the complete v0.4.26 release scope #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/ci #area/release #kind/review
    <!-- generated:card -->
    **Owner:** Codex (Maintainer complete v0.4.26 defect audit) · **Priority:** critical  
    **PR:** [baseharbor#1085](https://github.com/mcpdev80/baseharbor/pull/1085), [baseharbor#1084](https://github.com/mcpdev80/baseharbor/pull/1084), [baseharbor-demo#124](https://github.com/mcpdev80/baseharbor-demo/pull/124), [baseharbor#1083](https://github.com/mcpdev80/baseharbor/pull/1083), [baseharbor#1077](https://github.com/mcpdev80/baseharbor/pull/1077), [baseharbor#1082](https://github.com/mcpdev80/baseharbor/pull/1082), [baseharbor#1076](https://github.com/mcpdev80/baseharbor/pull/1076), [baseharbor#1075](https://github.com/mcpdev80/baseharbor/pull/1075), [baseharbor#1074](https://github.com/mcpdev80/baseharbor/pull/1074), [baseharbor-node-connector#16](https://github.com/mcpdev80/baseharbor-node-connector/pull/16), [baseharbor-console#15](https://github.com/mcpdev80/baseharbor-console/pull/15), [baseharbor-demo#123](https://github.com/mcpdev80/baseharbor-demo/pull/123), [baseharbor#1073](https://github.com/mcpdev80/baseharbor/pull/1073), [baseharbor#1072](https://github.com/mcpdev80/baseharbor/pull/1072), [baseharbor#1071](https://github.com/mcpdev80/baseharbor/pull/1071), [baseharbor-console#13](https://github.com/mcpdev80/baseharbor-console/pull/13), [baseharbor-console#12](https://github.com/mcpdev80/baseharbor-console/pull/12), [baseharbor-node-connector#13](https://github.com/mcpdev80/baseharbor-node-connector/pull/13), [baseharbor-console#11](https://github.com/mcpdev80/baseharbor-console/pull/11), [baseharbor-node-connector#12](https://github.com/mcpdev80/baseharbor-node-connector/pull/12), [baseharbor#1070](https://github.com/mcpdev80/baseharbor/pull/1070), [baseharbor-demo#122](https://github.com/mcpdev80/baseharbor-demo/pull/122), [baseharbor-console#10](https://github.com/mcpdev80/baseharbor-console/pull/10), [baseharbor-node-connector#11](https://github.com/mcpdev80/baseharbor-node-connector/pull/11), [baseharbor#1004](https://github.com/mcpdev80/baseharbor/pull/1004), [baseharbor#1005](https://github.com/mcpdev80/baseharbor/pull/1005), [baseharbor#1046](https://github.com/mcpdev80/baseharbor/pull/1046), [baseharbor#1047](https://github.com/mcpdev80/baseharbor/pull/1047), [baseharbor#1053](https://github.com/mcpdev80/baseharbor/pull/1053), [baseharbor#1058](https://github.com/mcpdev80/baseharbor/pull/1058), [baseharbor#1059](https://github.com/mcpdev80/baseharbor/pull/1059), [baseharbor#1050](https://github.com/mcpdev80/baseharbor/pull/1050), [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055), [baseharbor#1056](https://github.com/mcpdev80/baseharbor/pull/1056), [baseharbor#1052](https://github.com/mcpdev80/baseharbor/pull/1052), [baseharbor#1060](https://github.com/mcpdev80/baseharbor/pull/1060)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/releases/v0.4.26.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (Maintainer complete v0.4.26 defect audit)  
**Priority:** critical  
**PRs:** [baseharbor#1085](https://github.com/mcpdev80/baseharbor/pull/1085), [baseharbor#1084](https://github.com/mcpdev80/baseharbor/pull/1084), [baseharbor-demo#124](https://github.com/mcpdev80/baseharbor-demo/pull/124), [baseharbor#1083](https://github.com/mcpdev80/baseharbor/pull/1083), [baseharbor#1077](https://github.com/mcpdev80/baseharbor/pull/1077), [baseharbor#1082](https://github.com/mcpdev80/baseharbor/pull/1082), [baseharbor#1076](https://github.com/mcpdev80/baseharbor/pull/1076), [baseharbor#1075](https://github.com/mcpdev80/baseharbor/pull/1075), [baseharbor#1074](https://github.com/mcpdev80/baseharbor/pull/1074), [baseharbor-node-connector#16](https://github.com/mcpdev80/baseharbor-node-connector/pull/16), [baseharbor-console#15](https://github.com/mcpdev80/baseharbor-console/pull/15), [baseharbor-demo#123](https://github.com/mcpdev80/baseharbor-demo/pull/123), [baseharbor#1073](https://github.com/mcpdev80/baseharbor/pull/1073), [baseharbor#1072](https://github.com/mcpdev80/baseharbor/pull/1072), [baseharbor#1071](https://github.com/mcpdev80/baseharbor/pull/1071), [baseharbor-console#13](https://github.com/mcpdev80/baseharbor-console/pull/13), [baseharbor-console#12](https://github.com/mcpdev80/baseharbor-console/pull/12), [baseharbor-node-connector#13](https://github.com/mcpdev80/baseharbor-node-connector/pull/13), [baseharbor-console#11](https://github.com/mcpdev80/baseharbor-console/pull/11), [baseharbor-node-connector#12](https://github.com/mcpdev80/baseharbor-node-connector/pull/12), [baseharbor#1070](https://github.com/mcpdev80/baseharbor/pull/1070), [baseharbor-demo#122](https://github.com/mcpdev80/baseharbor-demo/pull/122), [baseharbor-console#10](https://github.com/mcpdev80/baseharbor-console/pull/10), [baseharbor-node-connector#11](https://github.com/mcpdev80/baseharbor-node-connector/pull/11), [baseharbor#1004](https://github.com/mcpdev80/baseharbor/pull/1004), [baseharbor#1005](https://github.com/mcpdev80/baseharbor/pull/1005), [baseharbor#1046](https://github.com/mcpdev80/baseharbor/pull/1046), [baseharbor#1047](https://github.com/mcpdev80/baseharbor/pull/1047), [baseharbor#1053](https://github.com/mcpdev80/baseharbor/pull/1053), [baseharbor#1058](https://github.com/mcpdev80/baseharbor/pull/1058), [baseharbor#1059](https://github.com/mcpdev80/baseharbor/pull/1059), [baseharbor#1050](https://github.com/mcpdev80/baseharbor/pull/1050), [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055), [baseharbor#1056](https://github.com/mcpdev80/baseharbor/pull/1056), [baseharbor#1052](https://github.com/mcpdev80/baseharbor/pull/1052), [baseharbor#1060](https://github.com/mcpdev80/baseharbor/pull/1060)  
**Source:** 
<!-- /generated:links -->

# v0.4.26 board closeout — 2026-10-26

This release-specific acceptance/audit assignment is superseded by [bounded v0.4.27 carryover triage](t-20261026-r27-v0426-acceptance-carryover.md). No unresolved requirement is relabelled as PASS. Reconcile only genuinely outstanding obligations against shipped source; do not rerun obsolete candidates.

Marcel explicitly directed publication despite incomplete/failing CI and subsequently requested cleanup of the remaining release cards. v0.4.26 is published; the release tag and delivered source remain unchanged.

## Preserved history

[Pre-closeout task and all original scope, evidence and handoffs](https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/tasks/t-20261019-v0426-complete-defect-audit.md). This immutable history is retained in Git; old active-run statements are not current work instructions.

## Actual release

[Stable release](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26) · [successful publisher run](https://github.com/mcpdev80/baseharbor/actions/runs/40355992335) · [promotion PR #1089](https://github.com/mcpdev80/baseharbor/pull/1089). No new tests, runtime jobs or release operations were started for this Planning cleanup.
