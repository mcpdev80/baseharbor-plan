---
id: t-20261018-r27-access-wizard
card_number: "0427-013"
card_short_title: "guide profile assignment and"
areas: [wizard]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: lane-0427-access-wizard-r2
kanban_lane: active
kanban_summary: "Name->search/select Targets->rights->review; preserve selections across pagination/back, show effective scope. Distinguish…"
kanban_status: active
kanban_title: "0427-013 · guide profile assignment and"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-access-profiles, t-20261018-r27-client-commands, t-20261018-r27-device-lifecycle, t-20261018-r27-managed-users, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1430]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-access-wizard · Access: guide profile assignment and deliberate offboarding #task #release/v0-4-27 #status/active #view/active #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-access-wizard-r2 · **Priority:** normal  
    **PR:** [baseharbor#1430](https://github.com/mcpdev80/baseharbor/pull/1430)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-profiles](t-20261018-r27-access-profiles.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-managed-users](t-20261018-r27-managed-users.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Owner:** lane-0427-access-wizard-r2  
**Priority:** normal  
**PRs:** [baseharbor#1430](https://github.com/mcpdev80/baseharbor/pull/1430)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Name->search/select Targets->rights->review; preserve selections across pagination/back, show effective scope. Distinguish connection removal, device revoke, owned grant removal and explicit managed-user disable/delete. Authorization/current-state recheck, offline/empty/no-match feedback; no remote installation deletion from local cleanup.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded team profile/user/device removal wizard adapters/tests; no onboarding wizard file writes. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Entry-point tests for duplicate/large lists, cancel/EOF/stale/denied/offline; machine-equivalent validated domain calls. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

head 3a699a287 drift-frei (develop 812c99c88 vorfahr), #110-lifecycle/fixture-kollision behoben (delta nur eigene wizard-dateien), PR#1430 mechanisch geoeffnet (laptop ohne gh). CI pending->terminal abwarten dann CODEX-REVIEW. lane geliefert -> sitz frei.

PR#1430 3a699a287 drift-frei+sauberer write-set, ABER 3 FAILS = kommando-registrierung: 'baha access assign' ist NICHT klassifiziert (TestMachineDocumentationTracksRegistryAndCommandTree + TestMachineCoverageCIRealTreeAndJSONClassification registration_ci_readiness_test.go:82) UND docs/cli/command-index.md drift (TestHumanCommandIndexTracksExactCommandMetadata human_documentation_test.go:101). Kein review bis behebt. Korrektur: kommando in die classification registrieren + command-index.md neu erzeugen. frische lane noetig (orig freigegeben), pool voll -> queued.

korrektur dispatched (df554d91): nur die 3 kommando-registrierung FAILS heben (baha access assign classification + command-index.md neu), wizard-code bleibt. node-cli-lane freigegeben (geliefert, #1427 in review).

## Mitarbeit / CI-Abnahme — 2026-11-07

- **Mitwirkender:** ChatGPT (CI-Tests/Review). PR [#1430](https://github.com/mcpdev80/baseharbor/pull/1430), unklassifizierte `baha access assign`/`offboard` Machine-Registry-Operationen und generierte CLI-Index-Drift analysiert; verbindlichen Befund als PR-Kommentar dokumentiert. Die `lane-0427-access-wizard-r2` bleibt fachlicher Owner. Zusätzliche Negative- und Trennungsregressionen in eigenständigem Test-Scope beauftragt; **kein CI-Gate abschwächen, keine Karte ohne Review schließen**.
