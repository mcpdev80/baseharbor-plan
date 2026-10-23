---
id: t-20261022-r27-evidence-resolver
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: o70
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-resolver · evidence resolver #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** o70 · **Priority:** high  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Owner:** o70  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->


# Evidence resolver: stable lookup without workflow artifacts

## Goal
Resolve retained evidence by candidate, run and manifest digest from baseharbor-plan independently of an existing PR branch or GitHub Actions artifact.

## Scope
- Read-only lookup and bounded payload retrieval. Never infer trust from a task status, a mutable link or a successful lookup.
- Explicit not-found, incomplete, corrupt, stale and unauthorized outcomes; retain existing evidence references and older planning data.
- Avoid coupling to CI producer or reviewer write sets.

## Acceptance
- Tests resolve archived fixtures after source branch and Actions artifacts are unavailable.
- Negative tests cover missing files, mismatched digest, ambiguous IDs and untrusted references.
- No new registry/database/service.
