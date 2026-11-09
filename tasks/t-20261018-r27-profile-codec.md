---
id: t-20261018-r27-profile-codec
card_number: "0427-044"
card_short_title: "import and export non-secret"
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: coord-welle4 (Lanes w90 bis cx06)
kanban_lane: closed
kanban_summary: Validate version/trust/installation/scope before any writes; transactional import and explicit conflicts. Default export…
kanban_status: closed
kanban_title: "0427-044 · import and export non-secret"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-profile-contract, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1363]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/profile-codec/review-1363e.md", "https://github.com/mcpdev80/baseharbor/commit/e444ae1171", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/profile-codec/round-6.md"]
---

- [x] t-20261018-r27-profile-codec · Profiles: import and export non-secret connection metadata #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lanes w90 bis cx06) · **Priority:** normal  
    **PR:** [baseharbor#1363](https://github.com/mcpdev80/baseharbor/pull/1363)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/profile-codec/review-1363e.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/e444ae1171), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/profile-codec/round-6.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-profile-contract](t-20261018-r27-profile-contract.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md)  
**Owner:** coord-welle4 (Lanes w90 bis cx06)  
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

- 2026-11-04 round 2 (lane w113): the seven Codex probes pass locally on head f935fa18, but nothing reached the
  remote — branch work/r27-profile-codec still points at 0eb8f231 and the lane had built a separate branch
  instead of continuing the candidate. Order given: merge current develop 2a43984a, push onto the candidate
  branch, record the ls-remote witness, keep the PR draft until the coordinator flips it with the review.

## Review-Rueckruf 2026-11-04 (Codex review-1363b, verdict REJECT)
- Secret-Prüfung deckt nicht alle serialisierten Felder: Export verwendet den Container-Scan, der ZielPfad und
  Empfänger sieht, aber nicht die übrigen Textfelder (store.go:405-411, 443-458, 783-790); der Test behauptet
  nur eine spätere Import-Ablehnung (store_test.go:291-312).
- Import-Festschreibung ist nicht atomar: direktes `os.WriteFile` auf den Zielpfad, kein Nachweis gegen
  Kurzschreiben (store.go:738-747, store_test.go:470-492).
- Vertrauens-Selbstkonsistenz ist an eine Bedingung geknüpft und damit nicht erzwungen (store.go:76-79, 679-682).
- Kanonischer Rundlauf vergleicht nur ausgewählte Felder statt vollständiger Datensätze plus Neukodierung.
- Gehostete Gate auf diesem Kandidaten rot (Lauf 41849617084: Documentation-Audit und PR Selected Checks).
- Korrekturrunde = Lane w123 auf demselben Zweig/PR #1363 (Kopf vorher e45e85ed5f).

## Handoff 2026-11-04 (Runde 4, Kandidatenstand)
- Kopf 952299b5a7, develop ecbb8854 ist Vorfahr, Gatebild terminal 10 grün / 0 rot / 10 übersprungen
  (Documentation-Audit und ausgewählte Prüfungen nach der Spezifikationsangleichung grün).
- Prüfauftrag für diesen Kopf ist geschrieben und läuft, sobald der Abnahmekanal frei ist
  (coordinator/missions/codex-r1363c.txt).

## Review-Rueckruf 2026-11-04 (Codex review-1363c, verdict REJECT)
- Kanonische Datensatzversion war nur an Aufruferargumente gekoppelt, nicht Pflicht in Export und Import.
- Empfängersbindung war nicht zwingend; ein anderer gültiger SPIFFE-Empfänger konnte durchkommen.
- Vertrauensselbstkonsistenz blieb schalterabhängig statt unbedingt.
- Kurzschrift nach dem Schichten und Fehler beim Aufräumen des Ersatzes waren nicht echte geprüft (kein
  Testnaht-Nachweis, Entfernenfehler ignoriert).
- Canary-Prüfungen deckten nicht jede Kategorie, Rundlauf verglich Teilfelder, Ersetzen bewies nicht den
  Inhalt.
- Korrekturrunde = Lane w129, frisch von develop geschnitten (der alte Zweig trägt fremde Historie).
- Konsumenten-Abgrenzung 2026-11-04: Punkt 7 des letzten Prüfauftrags (der Produktionsaufrufer der Schnittstelle)
  liegt nach plattenfestem Befund außerhalb der Schreibrechte dieser Karte und ist auf
  t-20261018-r27-public-surfaces vermerkt. Diese Karte liefert die Kodierung vollständig gegenprüfbar.
- Stand 2026-11-04 (Runde 5, plattenfest nachgemessen): Kopf 064ba01820b, develop ecbb8854 ist Vorfahr,
  Schreibgut genau sieben Dateien im Vertragsordner, Prüfumfeld läuft noch (sechs wartend).
- Nachliefer-Pflicht vor der Abnahme: die Runden-5-Beweisdatei fehlt im Evidence-Baum (Kopf in keiner Datei);
  die Lane liefert die Blöcke nach, ohne den Kandidaten zu verändern. Abnahmeauftrag ist vorgemerkt.

## Handoff 2026-11-04 (Runde 5, Kandidatenstand, plattenfest nachgemessen)
- Kandidat: PR #1363, Zweig work/r27-profile-codec, Kopf 064ba01820b (ls-remote == Kopf), develop ecbb8854 ist
  Vorfahr; Schreibgut sind genau sieben Dateien im Vertragsordner, keine fremden Pfade.
- Beweissammlung ist nachgeliefert und liegt auf der Platte (round-5.md, 10513 Byte) - Prüfung läuft dagegen.
- Punkt 7 (Produktionsaufrufer der Schnittstelle) bleibt als Grenzbeleg geführt: Zuständigkeit liegt bei
  t-20261018-r27-public-surfaces, dort vermerkt, nicht hier.

## Handoff 2026-11-04 (Runde 6, plattenfest nachgemessen)
- Kandidat: PR #1363, Zweig work/r27-profile-codec, Kopf ac6a048e290 (ls-remote == Kopf), develop 2ea2c6f1 ist
  Vorfahr (Basis nach der Hebelkarten-Verbindung aufgefrischt).
- Beweissammlung liegt auf der Platte (round-6.md); der Kurzschreib-Beweis nennt einen echten Wert (809 von
  1619 Bytes geschrieben), die Vertrauensselbstkonsistenz ist ohne Schalter, und der Rundlauf vergleicht den
  vollständigen Datensatz samt goldener Bytes.

## Abschluss 2026-11-04 (verbunden, plattenfest nachgemessen)
- Verbundenschnitt in Deiner Hauptlinie: e444ae1171; der inhaltliche Vergleich des Prüfordsners gegen den
  geprüften Kopf ac6a048e290 ist leer und der Zweig ist gelöscht (mein eigener Befund, nicht die Lane-Meldung).
- Sechs Runden: sechs Rezepte aus der ersten Prüfung sind erfüllt — geheime Prüfung je Kategorie statt nur
  einmal, unbekannte Felder typisch abgewiesen, Pflichtversion und Empfängerbindung ohne Schalter,
  kanonische Reihenfolge mit goldenen Bytes, atomarer Import mit echtem angebrochenem Schreiben und
  typisiertem Aufräumfehler, englische und deutsche Fassung inhaltgleich.
- Der Produktionsaufrufer der Schnittstelle liegt weiter auf t-20261018-r27-public-surfaces (dort vermerkt);
  diese Karte liefert die Kodierung vollständig gegenprüfbar, nicht den Verbindungs draht.
