---
id: t-20261018-r27-state-owner
areas: [state]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: w2-state-owner
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1347"]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-state-owner · State: enforce installation-owned deployment storage #task #release/v0-4-27 #status/review #view/review #area/state #kind/task
    <!-- generated:card -->
    **Owner:** w2-state-owner · **Priority:** high  
    **PR:** [baseharbor#1347](https://github.com/mcpdev80/baseharbor/pull/1347)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md)  
**Owner:** w2-state-owner  
**Priority:** high  
**PRs:** [baseharbor#1347](https://github.com/mcpdev80/baseharbor/pull/1347)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Bind existing deployment/provider state to the selected installation and server-owned durable root. Workstation paths are cache/source hints only. Local and server execution resolve the same owner; reject foreign/missing/corrupt installation state and copied caches. Reuse existing state format/owner rather than a second state database.

Preserve the existing deployment identity (application ID + Target + environment), DeploymentSource and applied/observed records. Deliver the accepted owner-scoped read/write seam for later release-selection extensions, including isolation and serialization tests. Environment already exists; do not introduce a second stage identity, new coreinstallation state model or another database. This task owns storage authority, not the downstream version/configuration implementation.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/deployment/deployment_store.go; cmd/baha/app_context.go; cmd/baha/deployment_record.go; matching state-owner tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused deployment/context tests using two isolated homes, foreign identity and corrupt-state fixtures; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

### Handoff (2026-11-03, coordinator)

Candidate: PR #1347 head cdfc75bf (branch work/r27-state-owner, base develop, stacked note present);
duplicate #1340 closed with supersession proof. Review pending on windows-compile + production-consumer
points of review-1326b; state-owner content itself delivered by the earlier lane round.

### Coordinator note on installation-ID binding (2026-11-03, s2 round)

Same-target installation identity binding is deferred to the authority contract surfaces
(internal/installauthority plus serviceaccess issuer identity), where the durable installation ID
already lives; this card consumes it at its Load/Save seams once that lands. Recorded per s2 END.

### Coordinator acceptance note (2026-11-03, r1347i)

CODEX-REVIEW verdict on head 33badf7d: **ACCEPT-WITH-DEFERRAL** (evidence/r27-night-2026-11-02/review-1347i.md).
Deferrals as noted on this and the authority card (same-target installation-ID binding lives
on these seams once authority-contract lands). Merge via CODEX-MERGE in flight; closes on proof.


## Coordinator-Statusvermerk 2026-11-03 (review s + hosted CI)
CODEX-REVIEW r1347s: ACCEPT-WITH-DEFERRAL (ID-Bindung an Authority-Vertrag delegiert;
Prioritätsabsicherung = kombinierter Save-Test, angenommen als Deckung). Neutraler CLI-Beweis:
evidence/r27-night-2026-11-02/verify-cli-1347.md (Branch- und develop-Seitig identische cmd-Fehlschläge).
ABER Merge zurückgestellt: gehosteter Lauf 41632606424 auf Head be00b1c8 zeigt 4 Fehlschläge im
source-contracts-Job (internal/application/preferences + cmd/baha Doctor/AppEdit — Fixture-Seed ist
HOME-abhängig). Korrekturrunde w52 läuft; Merge erst nach grünem Lauf auf neuem Head.


## Coordinator-Block-Vermerk 2026-11-04 (w95 runde 3, formel+optionen urkundlich)
- Counter-beleg: ProtectedStateOwner verwirft docker-mount 0755 backend-dir; happy-path braucht core
  (owner-binding), core loest ADR-0022 retire-check aus — kein test-only ausweg (drei sonden, alle clean
  zurueckgesetzt, siehe evidence/state-owner/round3.md abschnitt 5+7).
- Owner-stoff: option 1 retire-check erweiterung (ScopeShared), 2 tenant-owner-pfad docker-dev,
  3 tenant-grant-fixture. Empfehlung lane: option 1 NACH ADR-freigabe. Karte blocked bis entscheidung.

### Owner decision and implementation scope (2026-11-04)

Owner authorizes a **narrow product correction** of the App Edit / provider-retirement interaction exposed by PR #1347, not a general relaxation of ADR-0022. This supersedes the undecided option-1 recommendation in the previous block note for this specific correction.

**Reproduced conflict:** The state-owner seam requires an authoritative Core installation to load the deployment. With Core present, the provider union adds management dependencies and may mark the plan incomplete; `prepareApplicationProviderRetirement` then returns `provider_retirement_unverifiable` before the edit can apply. The trace also identifies an application-scoped PostgreSQL instance with zero consumers and unverifiable observed runtime; skipping only `ScopeShared` resources is therefore insufficient. See [the recorded reproduction](../evidence/r27-welle3-2026-11-03/state-owner/isolation-1.md) and current product implementation.

**Required semantics / acceptance:**
- Distinguish a normal edit that retains/reuses existing resources from an actual attempt to retire a provider. Never treat a `preserve` plan entry as permission to stop/remove runtime.
- An unrelated, unchanged Core-managed resource must not veto a safe App Edit solely because its retirement facts are unavailable. Narrow the *retirement decision boundary*, not global inventory/ownership validation.
- Keep ADR-0022 **fail-closed for any actual release, stop or removal** when ownership, runtime state or the last-consumer inventory is unverifiable. Preserve data and ownership; do not bypass a refusal for a real provider release.
- Prove a real Core-backed App Edit reaches its intended converged result. Also prove unsafe last-consumer retirement still fails with the expected typed error, and foreign/missing installation owners remain rejected.
- No blanket `ScopeShared` / `OwnershipBaseHarbor` exemption, simulated success, fixture-only bypass, disabled tests or CI modifications. Reuse the existing resolver/authority; no new framework.
- Focused positive/negative tests including `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`; verify unchanged behavior of unrelated retirement cases.

**Write-set coordination:** `cmd/baha/application_provider_retirement.go` and any necessary provider-plan tests touch the retirement/consumer authority outside the original state-owner write-set. Coordinate exclusive ownership with the corresponding worker before edits; do not overwrite concurrent consumer/ADR work. If the fix requires changing the normative ADR-0022 contract rather than correctly distinguishing non-retirement, stop and return a concrete minimal decision proposal. Existing PR #1347 remains unaccepted until real tests pass; no release authorization.

**Developer Experience:** The developer must be able to finish an ordinary app edit without installing fictitious tenants or manually repairing fixture/runtime state. Only real unsafe retirement is blocked.

## Evidence-Nachlieferung 2026-11-04 (coord f49a3303)
- Lane w101 delivered head 03e4e01b (develop bb9bc0ef is an ancestor, ls-remote verified) and reported a
  side-by-side comparison, but the named evidence file does not exist on disk or on origin/main. A claim
  without a written proof is not accepted (owner directive 2026-10-28), so lane w111 re-runs the identical
  five-case comparison on neutral develop and on the candidate and commits
  evidence/r27-welle4-2026-11-04/state-owner/adr22-fix-1.md before its END.
- Hosted #1347 gates: 16 pass / 4 fail (PR Selected Checks, cli-package-tests, go-unit-tests,
  wizard-app-edit-tests). Reported cause is a docker-endpoint-dependent test that fails identically on develop;
  pending the written proof above. No rerun, no CI changes from lanes (owner-owned CI field).
