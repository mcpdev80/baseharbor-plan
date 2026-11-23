---
id: t-20261120-r28-perses-status-never-verified
card_number: "0428-186"
card_short_title: "no verified status source"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w186-0428-186-hop
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-186 · no verified status source
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1810]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-perses-status-never-verified · No source API yields verified: status --json can never report true #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** w186-0428-186-hop  
    **PR:** [baseharbor#1810](https://github.com/mcpdev80/baseharbor/pull/1810)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w186-0428-186-hop  
**Priority:** not set  
**PRs:** [baseharbor#1810](https://github.com/mcpdev80/baseharbor/pull/1810)  
**Source:** 
<!-- /generated:links -->

## Found by the owner's Codex takeover of 0428-078 (2026-11-20, finding-to-card duty AGENTS 3.3.5)

Measured during the 0428-078 takeover: PersesStatusNow (internal/capability/perses_selection.go) has no code path producing the verified state, so 0428-078's acceptance item P1 (a positive verified case through the public baha status --json output) is not reachable without a probe/source API. Faking 'verified' or letting configured_unverified pass would destroy exactly what the verified-only predicate was introduced to protect (owner ruling r7, reviewer stop-criterion 1).

## Acceptance

1. Name the real probe or source API that can decide 'the Perses backend answers for this selection' and wire it to the status path, or state in the plan why a health probe is the right instrument.
2. Once such a source exists, the positive case in 0428-078 (status --json identity_dashboard_eligible=true) must be reachable by test without touching the predicate.
3. Never a literal true: no hard-coded verified value, no configured_unverified acceptance to make a test green.

## Boundaries

internal/capability/perses_selection.go is owner-closed for the 0428-078 card; this card is the place where a change there may be proposed. It is the sequenced predecessor of 0428-181 (catalog consumer) because a catalog needs a verified signal to emit anything.

dispatched; write-set internal/capability/perses_selection.go confirmed disjoint from w078 (keycloak/metrics/app_status_result)

external repo-admin blocker, not a lane defect (#1809/#1650 pushed OK so it is branch/ruleset-specific)

candidate 168d40950 PR #1810 base develop clean (develop ancestor); verified-state source via hostProviderMetricsNativeVerified witness, predicate untouched; ruleset blocker moot (push succeeded). full gate pending draft->ready

CODEX-REVIEW #1810 = REQUEST_CHANGES (422 self-review, routed to worker): PersesStatusVerified derived from hostProviderMetricsNativeVerified() = static ReferenceIntegrations inspection, no target/provider input, no probe; violates acceptance 1+3 (never static 'true'). Route to w186.

Gate dependency: #1810 Trusted Plan clears via card 0428-260 (catalog guardian rows for internal/capability + internal/application/perses_lifecycle_test.go). INDEPENDENT of that: w186 still owes the REQUEST_CHANGES code fix (static verified -> fail-closed configured_unverified); head 168d40950 unchanged 5 ticks -> seat escalated to Owner.

develop d4fa8c589 (#1813) cataloged #1810's paths -> gate guardian clears after the additive hop (routed to w186). STILL owed regardless: the CODEX REQUEST_CHANGES fail-closed code fix (head stuck 168d40950 many briefs). Last chance sent; unchanged head next tick -> Owner seat force-release.

RESTART (beefcd12) of dead 402f1117. Continuing branch lane-0428-186: additive hop to d4fa8c589 + STILL-owed fail-closed code fix (perses.go configured_unverified + answering/silent tests).

Owner scope review @ head 5f000fb: fail-closed fix removed static bug but made 'verified' permanently unreachable (perses.go ~:215). WRONG terminal design -> kills #1650 IdentityDashboardEligible=true (derived from verified, app_status_result.go:57). Correction routed: real per-target reachability probe so answering target -> verified=true (eligible reachable), silent -> configured_unverified; if probe not buildable in scope -> QUESTION (name the missing instrument) for Owner to decide. Decision recorded in evidence/plan. #1650 must not merge while eligible unreachable.

w186 END REJECTED (remote-contradicted): claimed probe 6673b208 + verified reachable, but #1810 still 02c9b960e (fail-closed, no probe), 6673b208 on no ref, run 45273204897 not valid for this head. Real per-target probe + target-isolated Perses query acceptance BOTH required for 0428-186 positive-path. Nachlieferung ordered: land probe + query isolation, push (head off 02c9b960e), exact-head Hosted to terminal, reply head+ls-remote+run.

Probe LANDED head 5c2e97f3 (off fail-closed 02c9b960). Ordering bug (Owner review): PersesBackendAnswersStatusNow returns configured_unverified on endpoint/client setup error (lines 41/45) BEFORE selection+release guards (in helper 57/60), so unselected/invalid-release manifests bypass documented not_configured. Routed w186: selection+release checks FIRST (not_configured), then setup (configured_unverified only for selected+pinned); Hosted regression on production entry PersesBackendAnswersStatusNow (unselected->not_configured despite setup error; invalid-release->not_configured). exact-head Hosted; no merge; no Codex.

TWO blockers (head 5c2e97f3, run 45292103046): (1) Trusted Plan red — catalog lacks 3 rows (internal/application/perses_lifecycle_go, internal/metrics/perses_backend_status_go + _test_go, all data.capabilities) -> routed to catalog PR #1817 (owner merges to develop, then rebase #1810). (2) STILL OPEN — production wrapper PersesBackendAnswersStatusNow setup-before-guards ordering (selection+release FIRST, then endpoint setup) + production-entry Hosted regression. Native docker Perses smoke still running. #1650 verified-dep stays held until #1810 lands green. No merge; no Codex.
