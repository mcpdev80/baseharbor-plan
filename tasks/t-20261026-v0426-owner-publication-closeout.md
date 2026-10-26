---
id: t-20261026-v0426-owner-publication-closeout
type: acceptance
areas: [release, acceptance]
release: v0.4.26
version: ""
parent: v0.4.26
priority: high
owner: "Codex (Owner-authorized release closeout)"
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor#1089]
sources: []
blocker: ""
resolution: "accepted"
evidence: [https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26, https://github.com/mcpdev80/baseharbor/actions/runs/40355992335]
---

- [x] t-20261026-v0426-owner-publication-closeout · Close v0.4.26 Owner-directed publication #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/acceptance #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** Codex (Owner-authorized release closeout) · **Priority:** high  
    **PR:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/40355992335)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (Owner-authorized release closeout)  
**Priority:** high  
**PRs:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
**Source:** 
<!-- /generated:links -->

# Close v0.4.26 Owner-directed publication

## Accepted scope
The actual release/publication and observable delivery are complete under Marcel's explicit exception, followed by his instruction to clean the release board. This accepts publication closeout only, not missing pre-release/native qualification.

- Stable release, not draft/prerelease, published 2026-10-26T16:17:03Z: https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26.
- Release API rechecked on 2026-10-26: Linux AMD64/ARM64 archives, checksums.txt and owner-release-decision.json are present.
- Publisher run 40355992335, attempt 1, rechecked completed/success. Original publication verification, artifact hashes, Pages and source/tag identities remain in the [historical verify card](https://github.com/mcpdev80/baseharbor-plan/blob/6ea0e8dc08a9a8e335721fcd6982d36da8832ecb/tasks/t-20261017-release-0-4-26-verify.md).
- No tag/source changes, no fabricated complete-approval receipt and no new native/test matrix.

## Resolution semantics
Publish/verify are superseded by this narrower accepted exception closeout. Prepare/qualify are dropped because the normal retrospective gated route will not be run. core-923 and the defect audit are superseded by open v0.4.27 carryover triage; that triage is not accepted. Old missing evidence never becomes green through this change.
