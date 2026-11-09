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
owner: lane-0427-013-access-r7
kanban_lane: closed
kanban_summary: "Name->search/select Targets->rights->review; preserve selections across pagination/back, show effective scope. Distinguish…"
kanban_status: closed
kanban_title: "0427-013 · guide profile assignment and"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-access-profiles, t-20261018-r27-client-commands, t-20261018-r27-device-lifecycle, t-20261018-r27-managed-users, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1430, mcpdev80/baseharbor#1433]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://raw.githubusercontent.com/mcpdev80/baseharbor-plan/main/evidence/r27-welle5-folge-2026-11-07/access-wizard/round-3.md", "https://github.com/mcpdev80/baseharbor/commit/07ae6c3e91b081a189266ca4b162ba705d4aa78f", "https://github.com/mcpdev80/baseharbor-plan/blob/0ec5bdaee01860ab0bb9d7c94cfd86f2c58e68e9/evidence/r27-welle5-folge-2026-11-08/access-wizard/act-1430-review-r7.md"]
wait_reason: ""

---

- [x] t-20261018-r27-access-wizard · Access: guide profile assignment and deliberate offboarding #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-013-access-r7 · **Priority:** normal  
    **PR:** [baseharbor#1430](https://github.com/mcpdev80/baseharbor/pull/1430), [baseharbor#1433](https://github.com/mcpdev80/baseharbor/pull/1433)  
    **Evidence:** [proof 1](https://raw.githubusercontent.com/mcpdev80/baseharbor-plan/main/evidence/r27-welle5-folge-2026-11-07/access-wizard/round-3.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/07ae6c3e91b081a189266ca4b162ba705d4aa78f), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/0ec5bdaee01860ab0bb9d7c94cfd86f2c58e68e9/evidence/r27-welle5-folge-2026-11-08/access-wizard/act-1430-review-r7.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-profiles](t-20261018-r27-access-profiles.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-managed-users](t-20261018-r27-managed-users.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261108-bughunt-0427-greenfield-isolation](t-20261108-bughunt-0427-greenfield-isolation.md)  
**Owner:** lane-0427-013-access-r7  
**Priority:** normal  
**PRs:** [baseharbor#1430](https://github.com/mcpdev80/baseharbor/pull/1430), [baseharbor#1433](https://github.com/mcpdev80/baseharbor/pull/1433)  
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

## ChatGPT CI-Sicherheitsregression — 2026-11-07

- **Bearbeiter:** ChatGPT (CI/Owner-Unterstützung), zusätzlich zu `lane-0427-access-wizard-r2`.
- [Stacked Test-PR #1433](https://github.com/mcpdev80/baseharbor/pull/1433) basiert auf PR #1430 und prüft beide `access assign`/`offboard`-CLI-Befehle: getrennt von Core Login/Node Connect, fehlende/mehrfache PERSON ablehnen, Name aus CLI muss exakt dem im Wizard geprüften Personennamen entsprechen, JSON-Antwort bleibt auf Person/Decision beschränkt. Kleine fail-closed-Korrektur vor beiden Policy-Mutationscallbacks.
- Card bleibt **active**, bis #1433 übernommen, #1430 CI grün und die finale Review-Abnahme erfolgt. Keine falsche Closed-/Merge-Markierung.

## ChatGPT CI Offboarding-Finding — 2026-11-07

- **Bearbeiter:** ChatGPT (CI/Sicherheitsregression). In [PR #1433](https://github.com/mcpdev80/baseharbor/pull/1433) weitergehenden echten Bug gefunden: `RevokeAssignment` erwartete Profilname, CLI übergab Target-Name; bei Namenskollision potenziell falsches Profil betroffen. Mit exakter Person+Target-Prüfung vor `Manager.Revoke` korrigiert; targeted Regressionen für erlaubtes Offboarding, falsch benannte Targets, unbekannte Person, nil Authority und Bestandsschutz anderer Profile hinzugefügt (`794377d`, `1a36cb2`).
- Keine endgültige CI-Aussage für den gestapelten PR: #1433 basiert auf `work/r27-access-wizard` und löst derzeit keinen eigenständigen `develop`-PR-Lauf aus. Testübernahme in #1430 plus dessen vollständiger CI-/Review-PASS bleibt notwendig. **Active**, kein Merge, keine Abnahme.

3 registration fails fixed: baha access assign/offboard classified; command-index regenerated from registry; DE parity mirrored; CI terminal green run 5054 SUCCESS wizard-registration-tests and documentation-audit. Ready for CODEX-REVIEW.

3 registration fails fixed: baha access assign/offboard classified; command-index regenerated from registry; DE parity mirrored; CI terminal green run 5054 SUCCESS wizard-registration-tests and documentation-audit. Ready for CODEX-REVIEW.

r2 registration ok, aber drift gegen develop 8a3f58da9 (#119 merged) -> OCI-dateien im diff = drift nicht collision. rebase (delta nur wizard-dateien) dann review. #1433 korrigierter kopf.

r2 Kandidat PR#1430 head e651cb1c drift-frei (develop 8a3f58da9 ancestor), kollisionsfrei (delta nur wizard/accesswizard), CI terminal 14-pass (wizard-registration + documentation-audit + go-vet/build/unit/gofmt). CODEX-REVIEW. #1433 = veraltetes duplikat (alter kopf mit drift+collision) -> nach #1430 merge schliessen.

review REQUEST-CHANGES (4 punkte: persistenz der zuweisung/offboarding, cancel schreibt weiterhin, multiple targets gekuerzt, non-profile offboarding kinds ohne routes). r3 korrektur auf frischer laptop-lane c3f838ed. karte active MIT worker.

r3 Kandidat head 5ccb81472: drift-frei, CI terminal success (coord-uebernahme nach 3x stillstand ohne END), punkte 1-3 behoben (persistence/cancel/multi-target + indices neu), punkt 4 = cross-card befund managed-users. CODEX-REVIEW laeuft.

review r3: registration OK + CI gruen, aber 4 funktionale kernpunkte offen (persistenz-zueckeschreiben, cancel-write, multi-target-loop, kinds fail-closed) — rezept mit file:line in act-1430-review.md (20810abd). r4 frisch auf ornith 496759eb. karte active.

review r3: registration OK+CI gruen, 4 funktionale kernpunkte offen (persistenz-rueckschreiben, cancel-write, multi-target, kinds fail-closed); rezept mit file:line in act-1430-review.md (20810abd). r4 frisch auf ornith 496759eb. karte active.

r4 head be65de6d: CI run 42421669238 TERMINAL success (14/0), drift-frei, fail-closed-guard fuer unimplementierte kinds neu (finding 4); these 'findings 1-3 schon in 5ccb' mit stelle-nachweisen in round-4.md — reviewer-recheck entscheidet mit file:line-pflicht. CODEX-REVIEW dispatched.

recheck: persistenz/cancel/kinds ok, NEUER befund: multi-target assignment UEBERSCHREIBT fruehere targets + multi-target revoke kann PARTIELL persistieren (atomarität je batch fehlt). rezept in neuester act-1430-review.md. r5 folgt auf freiem ornith-sitz (H-P1 hunt wird dafuer eingezogen).

hunt H-P1 sofort gestoppt (owner-direktive: echte arbeit > hunt) — sitz an access-r5 c38f521b: multi-target atomaritaet (alle-oder-nichts je batch) laut recheck-befund. H-P1-slice kehrt bei naechstem freien sitz zurueck in die matrix.

r6 candidate 9dd2f779fa2445257d4f7f3c99a43b1245493818 on PR #1430; hosted run 42438784031 completed/success; evidence round-6.md

PR #1430 was reviewed and squash-merged at 07ae6c3e91b081a189266ca4b162ba705d4aa78f. Exact-head CI run 42445068559 passed; post-merge Receipt · Commit run 42447092067 succeeded. The develop head matches the merge commit.

## PR #1433 reconciliation — 2026-11-08

- Historical [PR #1433](https://github.com/mcpdev80/baseharbor/pull/1433) closed without merge as redundant: production functions and all added test cases already exist on develop, which contains additional fail-closed safeguards. Do not overwrite newer production implementations with the stale 205-commit-behind branch.
- This source-code reconciliation is **not** a full acceptance of the access-wizard card; existing lane/status and any independent end-to-end checks stay unchanged.
