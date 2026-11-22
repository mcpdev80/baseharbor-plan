---
id: t-20261122-core-network-protected-owner-assertion-stale
card_number: "0428-244"
card_short_title: "core-network assertion stale"
type: bug
areas: [testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: owner (bereitet #1766 vor) / 1450c201 (CODEX-REVIEW+MERGE_assigned) / coord (zeugnis)
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-244 · core-network assertion stale
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1766]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1766"]
---

- [ ] t-20261122-core-network-protected-owner-assertion-stale · Static test asserts protected-owner while product emits a valid longer core/shared-backend owner diagnostic #task #release/v0-4-28 #status/review #view/review #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** owner (bereitet \#1766 vor) / 1450c201 (CODEX-REVIEW+MERGE\_assigned) / coord (zeugnis) · **Priority:** high  
    **PR:** [baseharbor#1766](https://github.com/mcpdev80/baseharbor/pull/1766)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1766)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** owner (bereitet #1766 vor) / 1450c201 (CODEX-REVIEW+MERGE_assigned) / coord (zeugnis)  
**Priority:** high  
**PRs:** [baseharbor#1766](https://github.com/mcpdev80/baseharbor/pull/1766)  
**Source:** 
<!-- /generated:links -->

## Found by #1765 exact hosted run 45018856573 on develop 8629450ef3c

Native Keycloak/Core fails on BOTH runtimes at `cmd/baha/operator_core_network_binding_native_test.go:86`: Podman job 137197826980
and Docker job 137197826981 run `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork`, which expects the phrase
"protected-owner" (asserted via the `Contains(..."existing native network lacks a protect...")` check at line 78 and the fatal at
line 86), but the product now returns a valid, longer diagnostic ("no verifiable protected Core or shared backend owner"). The
rejection BEHAVIOR is correct (the unowned native network is refused, not adopted as external); only the test's expected phrase is
out of sync with the current diagnostic wording.

## Acceptance

1. Update the assertion in `cmd/baha/operator_core_network_binding_native_test.go:78/86` to match the CURRENT valid product
   diagnostic substring (assert on the stable semantic core, not the exact phrasing), so the unowned-native-network rejection is
   still proven but tolerant of the longer message. Do NOT weaken the rejection check (must still assert refusal + not-external).
2. If the longer product diagnostic itself is unintended, instead fix the product message — but the run shows the product message
   is valid; expected route is the test-assertion sync.
3. Regression via the existing native Keycloak/Core shards; no `.github` change.

## Boundaries

`cmd/baha/operator_core_network_binding_native_test.go` only. Outside card 0428-209 / PR #1765 write-set (its 2-file delta is not
the cause). Blocks #1765's native Keycloak/Core gate until synced.

PR #1766 (head 405be63, develop-basiert) korrigiert NUR die stale expected-diagnostic in operator_core_network_binding_native_test.go:78/86, product-verhalten unveraendert, ablehnung bleibt belegt. Review 1450c201 = PENDING (beim beobachtungspunkt war KEIN exact-head native docker/podman job terminal green; checks queued/in_progress). Bei terminal green native keycloak/core (137197826981 docker / 137197826980 podman) -> APPROVE + MERGE VOR #1765-rerun. f0f6c8b4 wurde abgezogen (dupliziert #1766).

EXAKTER head 405be63, native Keycloak/Core docker+podman BEIDE SUCCESS (gemessen). Assertion-phrase correct, produktverhalten unveraendert, ablehnung bleibt belegt. Review flippt PENDING->APPROVE, danach CODEX-MERGE #1766 in develop (additiv, develop-head aus refs/heads/develop, kein force). MERGE VOR #1765-rerun.t #1765 native keycloak/core + jede lane mit derselben stale assertion. 0428-209 (#1765) rerun nach diesem land.
