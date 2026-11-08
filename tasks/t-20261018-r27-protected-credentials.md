---
id: t-20261018-r27-protected-credentials
card_number: "0427-047"
card_short_title: "retain and recover opted-in"
areas: [access]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: ChatGPT (0427-047 regression follow-up)
kanban_lane: active
kanban_summary: Explicit secure choice uses existing authoritative protected store when managed secrets exist; never bootstrap OpenBao solely to…
kanban_status: active
kanban_title: "0427-047 · retain and recover opted-in"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-native-auth, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1385, mcpdev80/baseharbor#1470]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-1.md", "https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-2.md", "https://github.com/mcpdev80/baseharbor-plan/evidence/r27-welle4-2026-11-05/protected-credentials/round-3.md", "https://github.com/mcpdev80/baseharbor/pull/1385"]
---

- [ ] t-20261018-r27-protected-credentials · Credentials: retain and recover opted-in local credentials #task #release/v0-4-27 #status/active #view/active #area/access #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (0427-047 regression follow-up) · **Priority:** normal  
    **PR:** [baseharbor#1385](https://github.com/mcpdev80/baseharbor/pull/1385), [baseharbor#1470](https://github.com/mcpdev80/baseharbor/pull/1470)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/evidence/r27-welle4-2026-11-05/protected-credentials/round-2.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/evidence/r27-welle4-2026-11-05/protected-credentials/round-3.md), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1385)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md)  
**Owner:** ChatGPT (0427-047 regression follow-up)  
**Priority:** normal  
**PRs:** [baseharbor#1385](https://github.com/mcpdev80/baseharbor/pull/1385), [baseharbor#1470](https://github.com/mcpdev80/baseharbor/pull/1470)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Explicit secure choice uses existing authoritative protected store when managed secrets exist; never bootstrap OpenBao solely to reuse working native auth. Keep human/service/machine classes separate; references only in ordinary state. Verify reuse, rotation/revocation and local recoverability; report external non-exportable credentials explicitly. Remote-secret placement never falls back to the workstation.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/credential/broker.go and prepared-material persistence integration; internal/credential/openbao/; focused tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused existing broker/OpenBao adapter tests plus bounded integration only for real persistence/rotation behavior not covered cheaply. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

w162: device-rebind recovery for opt-in local developer credentials (commit 74a74e49). opt-in local FilePreparedMaterialStore authority + recover; wires existing OpenBao managed path where present, fail-closed when absent. CI run 41974727140 = PR Selected Checks success. Pending: Codex review + Maintainer merge.

## Kandidat pruefbar 2026-11-05 (kopf 74a74e49fdc)
devaccess-erweiterung (rebind + verdrahtung des bestehenden bao-pfads), vier wiederherstellungszellen,
fail-closed-zelle namentlich rot belegt, selected-checks gruen am kopf. Kein neuer geheimnis-speicher.

## Rueckruf 2026-11-05 (1385a REJECT: zellen 4/4 ok, aber wiederholung kann OpenBao zweimal
beschreiben und kaemt mit konkurrierendem eintrag)
Runde 2: eine Set pro pfad (abgeleitet aus der bestehenden reconcile-naht), rueckgabe des wiedergewonnenen
wertes, zaehlung der Get/Set-paare DURCH den echten produktionspfad; kein neuer speicher.

round-2 fix pushed (e295127e), CI Selected Checks 41985472620 success, card to re-review

## Runde 2 pruefbar 2026-11-05 (kopf e295127e45b)
Gemessen: Vorfahr ja, zwei eigene commits, Querschnitt devaccess+befehlsverdrahtung. Rezeptpunkt erfuellt
meldet die Lane: genau EIN Schreibvorgang pro frischem Geraet, NULL bei vorhandenem Bestand, Wettlauf:
vorhandener Wert gewinnt, alles ueber die bestehende Vergleichs-Naht.

## Rückruf (1385b REJECT): Wettlauf-Sonde der Prüfung erwischt Überschreiben
Der eigene Race-Nachweis der Lane war unvollständig: der Test brach vor dem Wiederherstellungsschritt ab,
dahir blieb das Überschreiben eines konkurrierend erzeugten Werts unentdeckt. Runde 3: create-only/CAS-
Erstseedung über die bestehende Ablage-Autorität, vorhandener Wert gewinnt (ein Get, null Set), der Test-
ablauf heilt nachweislich bis zum Schritt durch, CAS-Mutante macht die Konfliktzelle rot.

Round 3: create-only CAS seed (SetManagedCredentialIfAbsent, -if-not-exists) over existing OpenBao authority; existing managed value wins (1 Get 0 overwrite Set on conflict); race test fixed (initial Get NOT-FOUND, concurrent injected between Exists and seed, seed no-ops winner wins) + mutant RED cell. PR #1385 head b3c3c1c1; hosted CI #4790 success.

Round 3: create-only CAS seed (SetManagedCredentialIfAbsent, -if-not-exists) over existing OpenBao authority; existing managed value wins (1 Get 0 overwrite Set on conflict); race test fixed (initial Get NOT-FOUND, concurrent injected between Exists and seed, seed no-ops winner wins) + mutant RED cell. PR #1385 head b3c3c1c1; hosted CI #4790 success.

## Runde 3 pruefbar 2026-11-05 (kopf b3c3c1c1405)
Nachgemessen: ls-remote echt==head, drei ketten-commits eigene, lauf 41998291745 terminal SUCCESS am
exakten kopf, round-3.md auf main. Rezept 1385b erfuellet: create-only CAS-Saat ueber bestehende
Ablage-Autoritaet, vorhandener Wert gewinnt (ein Get, null Set),竞 race-test laeuft jetzt BIS zum
Wiederherstellungsschritt (vorher vorzeitig endend — jetzt belegt), CAS-Mutante rot. operator_auth.go
begruendet in der akte (Sentiment-Heimat fuer beide aufrufer) — blob-probe obliegt der pruefung.
Basis 24c7d0492f3, develop-merge dem merge-zweig.

## Rueckruf (1385c REJECT, ein punkt): simulation statt produktiver pfad
Der Konkurrenz-Test faehrt eine simulierte Liste statt den echten SetManagedCredentialIfAbsent-adapter —
die '-if-not-exists entfernt'-Mutante bleibt GRUEN. Runde 4: produktiver adapterpfad durch gesteuerten
executor (echte create-only-atomik), option-mutante muss einzellauf-rot, echte goroutine-barrieren.

## Runde 4 pruefbar 2026-11-05 (kopf 0e2b4803736)
Nachgemessen: ls-remote echt==head, develop 77511c8a in den zweig gemergt (merge-commit oben), lauf
42043134426 terminal SUCCESS am exakten kopf (selected checks + openbao-package + alle basis-tore),
round-4.md auf main (fac87ea). SEITDEM ist develop weitergelaufen (a53c10a7, die 4er-owner-runde) —
zusatz-drift ist NOTIZ fuers merge-zweig, kein rueckschritt der kette. Inhalte laut akte: produktiver
SetManagedCredentialIfAbsent-pfad in der race-zelle, -if-not-exists-mutante ROT einzellauf doppel-barrier,
1 Get 0 Set im konflikt.

## Gemerged 2026-11-05 (CODEX-MERGE, Owner-Richtlinie 'fertig heißt mergen'): develop 10e8d646f0,
kopf-vor-merge 31cc10a0 (develop-abgleich konfliktfrei), akzeptierter kopf 0e2b4803736 + rerun gruen nach
fremdem flake-treffer. Urteile: 1385d ACCEPT.

## Reopened 2026-11-08 — Sicherheitsregression (ChatGPT)

Status `active` statt `closed`: PR #1385 wurde akzeptiert, aber der aktuelle `develop`-Produktionspfad erfüllt die Fail-closed-Akzeptanz noch nicht vollständig:

- `reconcileDeveloperCredentialAuthority` interpretiert **jeden** Fehler von `openBaoRuntime` als «OpenBao noch nicht eingerichtet» und gibt lokale Credentials ohne verifizierte Authority zurück. Eine nicht erreichbare bestehende Runtime darf nicht als Bootstrap behandelt werden.
- `devaccess.Ensure` erzeugt bei fehlender Projektionsdatei neue lokale Credentials **vor** dem Authority-Check; das ist bei Gerätewechsel und bestehendem Managed Store kein sicherer Recover-Mechanismus.
- `SetManagedCredentialIfAbsent` klassifiziert jeden fehlgeschlagenen CAS-Write bei anschließend erfolgreichem Read als `AlreadyExists`; der genaue Schreibfehler bleibt unbelegt.
- Die vorhandene CAS-Mutationszelle ist abhängig von `BAHA_ECOSYSTEM_ROOT` und kann übersprungen werden; CI-Grün allein belegt den Negativpfad daher nicht.

**Arbeitspaket:** echten Bootstrap von Runtime-Störung unterscheiden; bestehende Credentials authoritative lesen, ohne den Store durch einen lokalen Kandidaten zu ersetzen; Fehlerpfade testbar machen; CAS-/Recovery-Regressionen ergänzen. Alte Merge-/Review-Nachweise bleiben historisch gültig, sind aber kein Nachweis für diesen Follow-up-Fix. Kein erneutes `closed` ohne Codeprüfung, tatsächliche Testausführung und grünen CI-Nachweis am neuen PR-Head.

## Draft PR 2026-11-08

[baseharbor#1470](https://github.com/mcpdev80/baseharbor/pull/1470) (`fix/0427-047-credential-recovery` -> `develop`) eröffnet. Initialer Commit: `f7ef6bcf` entfernt den unsicheren lokalen Fallback bei Runtime-Auflösungsfehlern; Regression `cmd/baha/dev_access_authority_failure_test.go` ergänzt, Head `f9f184b4`. **Weiter active:** Bootstrap-/Recovery-Abgrenzung, CAS-Negativfälle und CI-Ausführung noch offen; kein Merge ohne Verifikation.

## Architekturabgleich 2026-11-08 — Host-Verbindung ist eigener Pfad

User-requested checkpoint before further fixes: `0427-047` covers **dev management UI credentials**, not developer workstation -> Core management OIDC nor Core -> Docker/Podman Node Connector mTLS. Code: `docs/how-to/developer-access.md`, `cmd/baha/node.go`, `cmd/baha/application_core_authority.go`, `cmd/baha/app_remote_lifecycle.go`, `docs/spec/target-access-v1.md`. `node add` requires a valid Core operator session, verified tenant membership, a scoped one-use grant, and a pinned CA; `node connect` installs the outbound connector. Remote apply uses the authorized target session and explicitly rejects unsupported provider intents. Draft #1470 must not be mistaken for an E2E connector fix. **Hold** broader changes until workstation->Core management, enrollment, session and remote apply are qualified separately. Existing draft code is unverified and must remain Draft.

## Implementierungsstand 2026-11-08 — PR #1470 Draft, End-to-End noch offen

Aktueller Head `4f52b177`: getrennte Coreless-Lokal-/Remote-Fail-closed-Pfade in `cmd/baha/dev_access.go` und fokussierte Regression `dev_access_authority_failure_test.go`. `cmd/baha/node.go` meldet nach `systemctl is-active` nur noch `started`, nicht fälschlich eine vom Core verifizierte Session. Die PR-CI `#5223` wurde **SKIPPED**, daher kein grüner Testnachweis.

**Weiterer eigentlicher Entwickler-zu-Core-Blocker festgestellt:** `cmd/baha/use_target.go:bindExplicitSelectionToConnection` verlangt `coreinstallation.Load(targetRuntimeStateRootByName(target))` aus **lokalem** Target-State. Ein Entwicklerrechner ohne Core kann damit einen externen Core nicht regulär über `baha use` binden. Der `connection-profile/v1`-Contract existiert, ist aber kein nachgewiesener aktiver Remote-Binder. Dieses Problem ist unabhängig von Credentials/Karte 0427-047 und muss als Management-Connection-/Remote-Client-Slice mit eigener Code-/CI-E2E-Qualifikation behandelt werden. Bis dahin kein vollständig behaupteter Remote-Durchlauf und keine Freigabe von #1470.


## Plan-validator correction — 2026-11-08

- The previous `resolution: reopened-regression` was invalid on an `active` card. Reopening remains documented in the audit narrative; the resolution field is intentionally empty until a verified final acceptance. Existing owner, PRs and dependencies remain unchanged.
