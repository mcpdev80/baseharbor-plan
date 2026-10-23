---
id: t-20261022-r27-evidence-resolver
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-resolver · evidence resolver #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **PR:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
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
> Pre-research evidence retained (o64/o66/o68, console-2 PR #8, nc-3 PR pending): v0.4.26 ist noch nicht geschlossen (D2/W1/verify pending) => Release-27-Arbeit formal zurueck auf waiting, Outcome-Referenzen bleiben verlinkt.

## Handoff – isolated preparation, 2026-10-24

- Product prototype: [BaseHarbor PR #1048](https://github.com/mcpdev80/baseharbor/pull/1048). The resolver, staging publisher, and regression fixtures are preparatory work only; they are not trusted CI evidence or accepted dependencies.
- Current security hardening: the archive verifier rejects unbound artifact digests and the resolver/publisher reject Boolean byte lengths. Focused changes are on the draft PR branch, not on `develop`.
- This task remains **planned / waiting** until the v0.4.26 closeout, v0.4.27 release-start updates, and evidence contract are accepted. No owner is claimed, no production rollout or merge is authorized.
- Remaining acceptance: independent runtime regression and negative security tests; source/manifest and run provenance validation by the existing trusted owners; hostile concurrent-writer directory confinement; recovery after source artifact expiry; exact digest verification; independent review.
- CardBoard: keep the canonical `#status/planned`, derived `#view/waiting`, and `#board/planned`. Do not mark complete or set `early: true`; generated card previews and views belong to `scripts/plan.py render`.
