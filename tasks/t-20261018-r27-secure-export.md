---
id: t-20261018-r27-secure-export
card_number: "0427-054"
card_short_title: "encrypt explicitly selected"
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle5 (codex-worker, entlassen)
kanban_lane: closed
kanban_summary: Opt-in local eligible credentials only; authenticated encryption/version/KDF using existing reviewed primitives. Password never…
kanban_status: closed
kanban_title: "0427-054 · encrypt explicitly selected"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-profile-codec, t-20261018-r27-protected-credentials, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1396]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1396"]
blocker: ""

---

- [x] t-20261018-r27-secure-export · Profiles: encrypt explicitly selected local credential export #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (codex-worker, entlassen) · **Priority:** normal  
    **PR:** [baseharbor#1396](https://github.com/mcpdev80/baseharbor/pull/1396)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1396)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-protected-credentials](t-20261018-r27-protected-credentials.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md)  
**Owner:** coord-welle5 (codex-worker, entlassen)  
**Priority:** normal  
**PRs:** [baseharbor#1396](https://github.com/mcpdev80/baseharbor/pull/1396)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Opt-in local eligible credentials only; authenticated encryption/version/KDF using existing reviewed primitives. Password never in argv/logs; no plaintext intermediate. Validate/decrypt before transactional destination writes; separate recovery/seal material; never export remote provider secrets or fresh device identities by default.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded secure-profile archive adapter/tests; reuse internal/applicationbackup/crypto.go through existing API without modifying it in parallel. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Archive tamper/wrong-password/truncation/cleanup/destination-store round-trip tests; no runtime backup journey. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Coordinator-scope-call 2026-11-06 (w204 QUESTION, praeszedenz registry-kette selben tags):
command-registrierung/dispatch in cmd/baha/commands.go erLAUBT als begrenzte ausnahme — nur anhaengen,
fremde zeilen unangetastet, keine dritte datei. Begrundung: karten-outcome verlangt benutzbaren export;
adapter ohne kommando = tote technik (1395a-lehre). E2E-zelle + anbindungs-mutante als nachweis.

## Runde 2 pruefbar 2026-11-06 (kopf 0001ca02d19, basis-refresh nach coord-halt)
Nachgemessen: ls-remote echt==head, develop f01d2fb VORFAHR (rc=0), lauf 42147787627 TERMINAL SUCCESS am
exakten kopf, akte round-2-ci-receipt.md + decision-log.md auf origin/main (coord-record). Zusammenbau
echt (registrier-zeile, koord-freigabe B), mutante rot + gegenprobe gruen, race ok.

## Rueckruf (1396a REJECT): die zusammenbau-Zelle ruft den adapter DIREKT (eigene manifeste),
nie rootCommand->secureProfileExportCommand; der registrier-mutant rot war ein doku-sync-Tor, kein
zusammenbau-beweis. Rezept zeilen 74-101: echte befehlspfad-zelle die durch den mutant rot wird.

## Stand r3 (w216): inhalt fertig, befehlspfad-zelle ECHT (rootCommand->...->entschluesseln),
mutante ROT in der BEFEHLSZELLE + gegenprobe, base-0001ca02-lauf war success. Finaler lauf 42154778495
TERMINAL FAILURE an EXAKT der kur-zeile (MutationAcked, internal/development byte-identical) —
w207/w211-gleichbehandlung: parkt bis kur-r7 in develop, dann rebasis + EIN gruenlauf (mission w220).
