---
id: t-20261022-r27-evidence-resolver
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "w2-lane (post-run + task link, dormant PR2)"
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1090, mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: superseded
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODE-AUDIT-2026-10-27.md]
superseded_by: t-20261022-r27-evidence-publisher
---

- [x] t-20261022-r27-evidence-resolver · Retired standalone resolver; lookup is part of verifier #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w2-lane (post-run + task link, dormant PR2) · **Priority:** high  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODE-AUDIT-2026-10-27.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** w2-lane (post-run + task link, dormant PR2)  
**Priority:** high  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->

# Retired standalone resolver; lookup is part of verifier

## Disposition
Superseded by the W2 publication integration; read-only lookup remains inside the existing W3 verifier. There is no separate resolver service or second worker assignment. Earlier archive resolver/publisher instructions are historical. Existing receipt/parser/API validation code remains reusable; no HMAC/Ed25519/retention code is revived.

The successor is open, so supersession is not acceptance. Actual automatic chain proof remains on shadow-run. Preserve old source/handoffs via the immutable link below.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman is resumed by the Owner; the coordinator preserves claims and unpublished work and assigns small non-overlapping iterations under the current order. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-evidence-resolver.md) remain immutable history, not competing operational instructions.
