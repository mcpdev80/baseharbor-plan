---
id: t-20261018-r27-managed-users
card_number: "0427-035"
card_short_title: "invite users through the"
areas: [identity]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle5 (w265, entlassen)
kanban_lane: closed
kanban_summary: "Optional managed Identity path: discover/invite owned users through least-privilege native API; IdP owns…"
kanban_status: closed
kanban_title: "0427-035 · invite users through the"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-access-profiles, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1397]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-06/managed-users/act-1397g.md"]
blocker: ""

---

- [x] t-20261018-r27-managed-users · Identity: invite users through the native provider admin adapter #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/identity #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w265, entlassen) · **Priority:** normal  
    **PR:** [baseharbor#1397](https://github.com/mcpdev80/baseharbor/pull/1397)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-06/managed-users/act-1397g.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-profiles](t-20261018-r27-access-profiles.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md)  
**Owner:** coord-welle5 (w265, entlassen)  
**Priority:** normal  
**PRs:** [baseharbor#1397](https://github.com/mcpdev80/baseharbor/pull/1397)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Optional managed Identity path: discover/invite owned users through least-privilege native API; IdP owns password/activation/MFA. Explicit idempotency/ambiguity and unsupported capability handling; profile assignment remains a separate authorized action. No generic application-user management or shared admin credentials.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/identityprovider/developer_user_profile.go and bounded managed-user admin adapter/tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Native admin API fixture tests for invite/repeat/ambiguity/denial/owned deletion boundaries; live evidence in later access gate. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Runde 1 pruefbar 2026-11-06 (kopf b3cb622a2e2)
Nachgemessen: ls-remote echt==head, develop VORFAHR, lauf 42137459404 TERMINAL SUCCESS, akte round-1.md auf
main. Echter provider-admin-aufruf (kein pwd-griff), idempotenz+ambiguity wie kartentext, mutante rot +
gegenprobe gruen, zusammenbau echt, red-first belegt.

## Rueckruf (1397a REJECT, zwei punkte): (1) ECHTER DEFKT — create-fallback kann fremdes/unverifiziertes
KONTO aktivieren (lookup-leer-zweig); (2) der eingreichte 'mutante' war keine echte quellcode-mutation.
Rezept in review-1397a.md zeilen 21-22.

## Stand r2 (w211): inhalt fertig + basis-refresh gemessen (head 44e18f1b43d, vorfahr rc=0, akte
auf main). HOSTED zweimal ROT an ANDEREN zeilen (:363 am alten, :247 am neuen kopf), lokal alles gruen,
identityprovider- paket in BEIDEN laeufen gruen, internal/development byte-identical — dieselbe
zeitlimitierte kur-erkrankung, die kur-r7 gerade heilt (praeszedenz w207-gleichbehandlung). REZEPT NACH
kur-r7-LANDEUNG: rebasis auf develop-mit-r7 + EIN eigener gruenlauf, dann abnahme. Lane freigegeben.
