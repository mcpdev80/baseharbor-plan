---
id: t-20261018-r27-state-owner
card_number: "0427-056"
card_short_title: "enforce installation-owned"
areas: [state]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: Owner/ChatGPT (externe Übernahme 2026-11-05, Direktive)
kanban_lane: closed
kanban_summary: Bind existing deployment/provider state to the selected installation and server-owned durable root. Workstation paths are…
kanban_status: closed
kanban_title: "0427-056 · enforce installation-owned"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1347]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/41991822834", "https://github.com/mcpdev80/baseharbor/pull/1347"]
---

- [x] t-20261018-r27-state-owner · State: enforce installation-owned deployment storage #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/state #kind/task
    <!-- generated:card -->
    **Owner:** Owner/ChatGPT (externe Übernahme 2026-11-05, Direktive) · **Priority:** high  
    **PR:** [baseharbor#1347](https://github.com/mcpdev80/baseharbor/pull/1347)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/41991822834), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1347)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md)  
**Owner:** Owner/ChatGPT (externe Übernahme 2026-11-05, Direktive)  
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

## CI cause on this candidate 2026-11-04 (owner handed CI back to coordinator)
- Side-by-side proof is on main (evidence/r27-welle4-2026-11-04/state-owner/adr22-fix-1.md): all five disputed
  cases behave identically on develop and on the candidate; locally the app-edit case stops at a Docker
  endpoint preflight that is absent on this host. No product regression from the boundary fix.
- Hosted red on PR #1347 is therefore an environment cause, named by the Owner: the core lifecycle/PKI fixture
  lacks runtime/compose.yaml. Lane w111 is making that fixture self-contained (no skip, no bypass, no .github
  edits); if a workflow change is required the lane stops and reports, and I clear it with the Owner.

## Status 2026-11-04 (Kanban-Setzung über card-status.py)
- Candidate: PR #1347 head fd4980a1, develop ecbb8854 is an ancestor, hosted checks 16 pass / 4 fail.
- Blocked on the CI environment cause that lane w122 is locating, not on product work. PR #1374 was closed with
  supersession proof so this chain keeps exactly one candidate.

## Fortschritt 2026-11-04 (lane w111, Kanban-Setzung über card-status.py)
- Fixture-Stufe 1 (nur cmd/baha/app_edit_apply_test.go, 18 Zeilen, Commit 069b02b5) hat die fehlende
  compose.yaml behoben; der PR #1347-Kopf ist fd4980a1 mit develop ecbb8854 als Vorfahr.
- Die nächste Blockerstufe ist lokalisiert und dokumentiert: die Fixtur erzeugt compose.yaml und runtime.env,
  aber nicht runtime/openbao-admin.env, das die Produktion beim Bootstrap schreibt.
- PR #1374 wurde mit Supersession-Beleg geschlossen (Kommentar 6634103570), damit die Kette genau einen
  Kandidaten behält.
- Umgebungsbefund 2026-11-04 (Koordinator): Der vollständige Anwendungsänderungs-Durchlauf schlägt in der
  Prüfumgebung mit dem nicht laufenden Tresordienst fehl (service openbao-admin is not running), unabhängig
  von der Datenbankverbindungsumstellung.
- Einordnung 2026-11-04 (unabhängig nachgemessen, class-a-verification.md Zeile 2): Klasse B, keine A —
  der Prüfungsaufbau stellt nur die Datenbank her, der Produktionspfad verlangt absichtlich den
  verwalteten Tresordienst und lehnt ohne ihn geschlossen ab. Nächster Auslöser: Prüfaufbau mit
  Tresordienst herstellen und genau diese Prüfung erneut laufen; erst ihr Ausgabeergebnis entscheidet.
- Nachmessung 2026-11-04 (zweiter Durchgang, Lane w139, Kopf 4decc28ecb7 auf der neuen Hauptlinie): die
  Datenbankpaarung ist auf dem Läufer grün (Lauf 41898648858, Paket internen Bereich in Ordnung). Es bleibt
  GENAU EINE Stelle: der vollständige Anwendungsänderungsdurchlauf verlangt den verwalteten Tresordienst
  ("openbao-admin läuft nicht"), gemessen an cmd/baha/app_edit_apply_test.go im Änderungsnachweisblock.
  Klasse B, ein Prüfaufbau-Eingriff, keine Produktänderung — die Entscheidung liegt beim Eigentümer.

## Review-Nachmessung 2026-11-05 (Head 76d4df9ef284)

- [PR #1347](https://github.com/mcpdev80/baseharbor/pull/1347) ist nach der Konfliktauflösung gegen develop `0476164a96d7` technisch konfliktfrei; Branch-Head `76d4df9ef284511e871797fd4b08416e2219d77f`. Das versehentlich eingecheckte Binärprogramm `baha` wurde aus dem resultierenden PR-Diff entfernt (44 Quelldateien bleiben).
- [CI-Run 41964700685](https://github.com/mcpdev80/baseharbor/actions/runs/41964700685) ist **rot**: `go-unit-tests`, `cli-package-tests` und `wizard-app-edit-tests` fehlgeschlagen. Deshalb **kein Merge** und **keine Acceptance**.
- `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`: managed-service PKI scheitert am echten `openbao-admin`-Dienst (nicht gestartet). Die derzeitige test-only `openbao-admin.env` enthält ausdrücklich nur Platzhalter, die sich niemals am echten OpenBao anmelden können. Erforderlich ist ein **wirklich gestarteter und gebootstrappter OpenBao-Core** mit gültiger Manageridentität im isolierten Testaufbau; kein Mock, kein Skip und keine Abschwächung des produktiven PKI-Fail-Closed.
- Weitere sieben regressierende Tests in `cmd/baha`: vier `TestW138*`-Lifecycle/Destory-Fälle und drei `TestStopRepositoryWorkload*`/`TestDestroyRepositoryWorkloadStop*`-Fälle. Konkreter Fehler: `ErrDeploymentOwnerMissing`, weil die neue produktive Storage-Seam eine Core-Installation verlangt, während diese lokalen Testfälle ohne Core-Installation angelegt werden. Vor einem Testfixture-Fix die **fachliche Local/Coreless-Semantik** prüfen: die Release-Grenze verspricht weiterhin lokale Nutzung ohne zwangsweise laufenden Core. Ein künstlich installierter Core in allen Local-Tests würde die Regression möglicherweise nur verdecken.
- Nächster fachlicher Schritt: Local-Owner-Vertrag explizit abgrenzen (lokaler eigenständiger Zustand vs. managed Core-Target), mit negativen Fremd-Owner-Tests und realen lokalen Lifecycle-Gegenproben. Separat OpenBao-Integration auf GitHub-hosted Docker mit echter Bootstrap-Identität qualifizieren. Erst wenn alle gewählten CI-Checks auf dem exakten PR-Head erfolgreich sind, mergen.

## Externe Übernahme — durch Coordinator nur markiert, nicht bearbeitet
PR #1347 (Kopf 76d4df9ef2) inkl. Fixture-Frage (openbao-admin Umgebungsdatei) liegen bei Owner+ChatGPT:
Implementierung, CI, Review, Merge und Planning-Abschluss. Keine Lane von dieser Seite aendert an den
State-Owner-Dateien; abhaengige Karten bleiben bis zurueckgemeldetem Abschluss gesperrt. Bisheriger
Blocker-Text bleibt als Historie stehen, seine Bearbeitung liegt jetzt bei der Uebernahme.


## Abschluss 2026-11-05 – Owner/ChatGPT

- PR [#1347](https://github.com/mcpdev80/baseharbor/pull/1347) merged into `develop`, squash commit `42bfcb1cb481c9e37ecd6ce30580e27829284113`.
- Final source head `4a5f45e5bbe089e0baf50b9584f3d9c0b01b8df2` verified against [Actions #41991822834](https://github.com/mcpdev80/baseharbor/actions/runs/41991822834): completed / success, all selected jobs successful.
- Verified real Core/OpenBao bootstrap and manager authentication, App Edit SQL provider resume, local never-delivered destroy with one-shot proof, explicit fail-closed foreign/retained owner cases; full CLI package and Go unit tests passed.
- Former blocker resolved; no new CI policy or runtime bypass. Downstream dependencies may now use merged state-owner seam. No assertion here that post-merge receipt publication or release qualification has completed.
