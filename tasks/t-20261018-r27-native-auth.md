---
id: t-20261018-r27-native-auth
card_number: "0427-038"
card_short_title: "reuse native Auth before"
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: coord-welle4 (Lane w135)
kanban_lane: closed
kanban_summary: "Reuse Git credential helper/SSH agent/config, registry/native credential references and native kube contexts; cloud credential…"
kanban_status: closed
kanban_title: "0427-038 · reuse native Auth before"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-profile-contract, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1362]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/0476164a96d7e8bccdacf4ffc1f2179a6b73f70e", "https://github.com/mcpdev80/baseharbor/actions/runs/41963065275"]
---

- [x] t-20261018-r27-native-auth · Credentials: reuse native authentication before prompting #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/access #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w135) · **Priority:** high  
    **PR:** [baseharbor#1362](https://github.com/mcpdev80/baseharbor/pull/1362)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/0476164a96d7e8bccdacf4ffc1f2179a6b73f70e), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/41963065275)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-profile-contract](t-20261018-r27-profile-contract.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-protected-credentials](t-20261018-r27-protected-credentials.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md)  
**Owner:** coord-welle4 (Lane w135)  
**Priority:** high  
**PRs:** [baseharbor#1362](https://github.com/mcpdev80/baseharbor/pull/1362)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Reuse Git credential helper/SSH agent/config, registry/native credential references and native kube contexts; cloud credential chain boundary gets contract fixtures, not new cloud providers. Native success asks nothing and preserves user configuration. Session-only material is not persisted; any necessary temporary files are protected and cleaned on cancel/error.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/credential/ bounded native-source adapters and tests; existing Git/workspace/native-context adapters only via accepted interface. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Fake native toolchain and filesystem tests for success/failure/cancel/cleanup and no-secret-output; Kubernetes contract-only. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Handoff-decision (w97, 2026-11-04)

Production round delivered on PR #1362 (branch work/r27-native-auth, exact head 8f4cbd2b7394036b23bdb59a9540a41134595151). The three Luna review-1362a findings are closed: (1) callable path — `internal/credential/native` now exposes `Broker` implementing the accepted `credential.Broker` consumption path (compile-time proof); (2) git-helper protocol fixed to the real stdin/stdout `fill` line protocol; (3) `ExecRunner` stderr redacted to class+exit only. 19 tests green locally; PR #1362 CI run 41813494855 terminal green (go-build/go-vet/go-unit-tests/Source-format/Policy all success, product gates correctly skipped). Evidence: `evidence/r27-welle4-2026-11-04/native-auth/production-1.md`. Candidate is exact-SHA and review-ready for Codex closure + Maintainer merge; card status stays `active` until acceptance/merge.

## Base refresh commissioned 2026-11-04 (Owner option A)
- Lane: Codex worker seat cx02, same mission as team-auth (second branch in the same pass).
- From head a3eee132e3 onto develop ecbb8854. The running acceptance review (r1362b) judges the OLD head; its
  verdict is informational until the refreshed head is reviewed. PR stays ready, no merge before a positive
  verdict on the new SHA.

## Review-Rueckruf 2026-11-04 (Codex review-1362b, verdict REJECT)
- Der Native-Abfrage-Broker ist nicht in den echten Abfragefluss vor der interaktiven Eingabe eingebunden; ein
  Bool-Wert 'gefunden' ohne Inhalt wird als Erfolg gewertet (internal/credential/native/broker.go plus Aufrufer).
- Erwartet: Auflösung über den bestehenden geschützten In-Memory-Vertrag weiterreichen, dokumentierter
  Fallback bleibt fail-closed, keine Secrets in Fehler oder Log, End-to-End-Gegenprobe auf Aufrufer-Ebene.
- Korrekturen sind produktseitig; die Grundlagen-Auffrischung auf develop ecbb8854 läuft parallel in cx02.

## Schreibfelderweiterung 2026-11-04 (Coordinator-Autorisation, dokumentiert für die Abnahme)
- Lane w125 meldete korrekt, dass der Native-Broker im Produktionspfad null Aufrufer hat; die Karte verlangt
  aber die Wiederverwendung vor der interaktiven Eingabe, ein nicht aufgerufener Adapter erfüllt sie nicht.
- Autorisiert ist ausschließlich der Aufrufer-Punkt in cmd/baha/app_init_prompts.go (promptSecretPolicies /
  promptSecretProvisionPolicy, Aufrufer app_init_selection.go:137) plus die nötige winzige Registrierung.
  Kein anderer Bereich von cmd/baha, keine Workflow-Datei, kein Umbau des Init-Ablaufs.
- Gegenprobe auf Aufrufer-Ebene ist Pflicht: bei gesetztem nativem Treffer wird der echte Prompt nullmal
  gerufen und die Auflösung läuft über den geschützten In-Memory-Vertrag; Fehltreffer hält den fail-closed
  Fallback.

## Einbauort präzisiert 2026-11-04 (Coordinator, nach eigenem Quellennachweis)
- Der interaktive Geheimnislese im Produktionspfad liegt in cmd/baha/app_apply.go: Zeile 23 definiert die
  auswechselbare Lese-Funktion, Zeile 249 beginnt promptAndStoreMissingRequiredSecrets, Zeile 287 liest pro
  fehlendem Pflichtgeheimnis verdeckt. Dort — nicht im Einrichtungs-Assistenten — muss die native Abfrage vorher
  einsetzen.
- Erwartetes Verhalten: Treffer mit Inhalt reicht die Auflösung über den geschützten In-Memory-Vertrag weiter und
  ruft den Prompt nullmal; Treffer ohne Inhalt ist kein Erfolg; Fehltreffer hält den dokumentierten Fallback
  und der Nichteingabe-Pfad bleibt unverändert.

## Einbauort berichtigt 2026-11-04 (nach Quellennachweis, Lane-Einwand recht gegeben)
- Der zuvor freigegebene Punkt in cmd/baha/app_apply.go ist thematisch falsch: dort werden anwendungsbezogene
  Schlüsselnamen über die Tresoranbindung behandelt, es gibt dort keinen Rechnername. Die Stelle bleibt unbearbeitet.
- Richtige Stellen sind die Git-Aufrufe gegen HTTPS-Fernziele, wo eine Nachfrage entstehen würde:
  cmd/baha/app_inspect_remote.go:33, cmd/baha/app_update.go:252, internal/development/workspace_git.go:201,
  internal/orgconfig/source.go:123. Freigegebenes Schreibfeld: diese vier Stellen minimal plus
  internal/credential/native und Tests.
- Wertevertrag: der Broker bleibt bewusst wertfrei. Aus einem Treffer ohne Inhalt darf nirgends
  'authentifiziert' gefolgert werden; die einzige Wirkung ist, dass der Git-Lauf nicht-interaktiv startet, und
  Erfolg oder Misserfolg entscheidet Git selbst.

## Handoff 2026-11-04 (Runde 4, Kandidatenstand, plattenfest nachgemessen)
- Kandidat: PR #1362, Zweig work/r27-native-auth, Kopf 0a67092ca31 (ls-remote == Kopf), develop ist Vorfahr.
- Die vier echten Git-Aufrufstellen tragen die Anbindung wirklich (von mir im Zweig nachgesehen):
  cmd/baha/app_inspect_remote.go, cmd/baha/app_update.go, internal/development/workspace_git.go,
  internal/orgconfig/source.go — je mit Rechnername-Gewinnung, Stummschaltung der interaktiven
  Passwortabfrage und dem Wertaustausch-Helfer; der Tresorvermittler bleibt wertfrei (found-only).
- Geänderte Dateien: 16, alle in cmd/baha und internal/{credential/native,development,orgconfig};
  keine Workflow-, keine Migrationsdatei.
- Lokales Bild der Lane: build, vet, gofmt und die vier Paketttests grün, Gegenprobe über den Aufrufer.
- Der gemeldete Runner-Stand war ungenau: die Läufe sind nicht ausgefallen, sie stehen in der gemeinsamen
  Warteschlange (mein Nachmesser: Läufe 17:20 / 17:23 / 17:30 wartend, ältere Läufe fertig). Das ist ein
  Warten, kein Blocker; die Prüfung läuft trotzdem gegen den Kopf.

## Handoff 2026-11-04 (Runde 5, plattenfest nachgemessen)
- Kandidat: PR #1362, Zweig work/r27-native-auth, Kopf 848d9512728 (ls-remote == Kopf, wörtlich in der
  Beweissammlung), develop e444ae11 ist Vorfahr; Prüfprotokoll 14 grün, null rot, Lauf 41903525411.
- Die Grundsatzentscheidung ist umgesetzt: Die Umweltprüfung gilt nur auf dem echten Pfad ohne eingesetzten
  Prüfer (internal/credential/native/sshagent.go:53-61); ein eingesetzter Prüfer entscheidet umweltunabhängig.
  Beide bisherigen Aussagen bleiben unverändert, der Zusatzfall (Prüfer gesetzt, Ziel nicht vorhanden) belegt
  die Trennung, und der Fehlschlag vorher ist auf dem Ausgangskopf ad0ea646 gesichert.
- Beweissammlung auf der Platte (round-5.md, 3252 Byte).

## Merge-Abschluss 2026-11-05

- [PR #1362](https://github.com/mcpdev80/baseharbor/pull/1362) nach develop per Squash gemergt: [0476164a96d7e8bccdacf4ffc1f2179a6b73f70e](https://github.com/mcpdev80/baseharbor/commit/0476164a96d7e8bccdacf4ffc1f2179a6b73f70e).
- Zugehörige selektierte Tests/Builds im GitHub-Run [41963065275](https://github.com/mcpdev80/baseharbor/actions/runs/41963065275) erfolgreich. Nicht gewählte Gates nicht als ausgeführt bewertet.

## Recheck r1362e 2026-11-05
ACCEPT am Owner-seitigen kopf f37cda334b0 (delta zum geprueften 2209436c =
inhaltlicher Owner-fix fetch-only-once, blobs der credential-kette intakt, gates am kopf).
Merge-obliegt der Owner-Runde — kein Channel-Merge (Direktive 04:4x).
