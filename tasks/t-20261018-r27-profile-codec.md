---
id: t-20261018-r27-profile-codec
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (lane w88)
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-profile-contract, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1363"]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-profile-codec · Profiles: import and export non-secret connection metadata #task #release/v0-4-27 #status/active #view/active #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (lane w88) · **Priority:** normal  
    **PR:** [baseharbor#1363](https://github.com/mcpdev80/baseharbor/pull/1363)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-profile-contract](t-20261018-r27-profile-contract.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md)  
**Owner:** coord-welle4 (lane w88)  
**Priority:** normal  
**PRs:** [baseharbor#1363](https://github.com/mcpdev80/baseharbor/pull/1363)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Validate version/trust/installation/scope before any writes; transactional import and explicit conflicts. Default export excludes remote secrets and short-lived/runtime/admin/recovery material; local path remapping is destination-local. Export/import never creates grants or changes a remote deployment.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded connection/profile codec/store implementation and component-specific tests; no CLI registration. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Round-trip/tamper/wrong-installation/partial-write/secret-exclusion tests; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

- 2026-11-04: base refreshed onto develop bb9bc0ef (lane w108), head 0eb8f231, gates terminal 2/0/14.
  Codex final review r1363a dispatched on this exact head.

## Review-Rueckruf 2026-11-04 (Codex review-1363a, verdict REJECT)
- Store prüfte importierte/exportierte Datensätze nicht gegen Version, Schema und die erwartete Bindung
  (Installation/Empfänger/Umfang/Vertrauen); Secret-material in serialisierten Feldern wurde nicht abgewiesen,
  der Secret-Test war inhaltlich leer.
- Unbekannte Felder gingen beim Dekodieren still verloren (auch verschachtelt).
- Kein kanonisches Container-Format, kein echter Import→Export-Rundlauf; goldenes Fixture folgte der
  Implementation statt der kanonischen Darstellung.
- Import war nicht atomar (direktes os.WriteFile, Teildatei blieb bei Fehler), Konflikt-Ersetzen prüfte nur
  den Zähler statt des ersetzt-alten Datensatzes.
- EN/DE-Spezifikation und Modell stimmten nicht exakt überein.
- Korrekturrunde: Lane w113 auf demselben Zweig/PR #1363 (Kopf vorher 0eb8f231).
