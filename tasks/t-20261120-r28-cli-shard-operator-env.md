---
id: t-20261120-r28-cli-shard-operator-env
card_number: "0428-198"
card_short_title: "cli shards need operator env"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: w198-0428-198-cligate
kanban_status: active
kanban_lane: active
kanban_summary: "Jeder Pull Request, der auf develop 40cb28c758b0 (Merge von #1594, cli2-env-policy-head) gehopft wird, verliert die vier shards…"
kanban_title: 0428-198 · cli shards need operator env
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-r28-cli-shard-operator-env · cli shards need operator env #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w198-0428-198-cligate  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w198-0428-198-cligate  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Jeder Pull Request, der auf develop `40cb28c758b0` (Merge von #1594, `cli2-env-policy-head`) gehopft wird, verliert
die vier shards `PR · Go unit · cli-0` bis `cli-3` mit Betreiber-/OIDC-Meldungen, obwohl seine Änderung nichts mit
diesen Tests zu tun hat. Ziel: die PR-Gate wieder gangbar machen, ohne dass eine Lane ihre Prüfumgebung selbst
setzen muss (§3.8 letzter Absatz).

## Fundstelle und Zeuge (gemessen 2026-11-20)

- PR #1718 (0428-178, Inhalt APPROVED, 1 Datei `cmd/baha/context_terminal_test.go`, nur Test):
  head `ce5aa9633630b88a017f501da7c2f0bd00e44714`, run `44774783515` `completed/failure`, alle vier cli-shards
  `Execute selected Go tests with isolated PostgreSQL` = failure.
- Wörtlich: `main_test.go:60: create failed: Managed-environment machine operations require an authenticated
  BaseHarbor operator` und `app_secrets_shared_runtime_test.go:44: actual source-only shared Secrets
  initialization: operator OIDC configuration`.
- Derselbe Ausfall an PRs, die nicht diesem Ökosystem-Lane-Stapel gehören: run `44770516960`
  (`cli2-identity-secrets-head` @ `1bc3362155`) und run `44765885244` (`cf7d1e6014`) = `completed/failure`.
- develop selbst meldet am selben sha `4 success / 6 skipped / 0 failure`: die Push-Pfade laufen nicht über die
  cli-shards. Der Fehler ist also ein PR-Gate-Defekt, der auf develop unsichtbar bleibt.
- Akten: `evidence/r28-welle4-2026-11-20/codex-review-wave/1718-0428-178-merge.md` (CODEX-MERGE END_BLOCKED,
  kein merge) und `codex-review-wave/1718-0428-178.md` (APPROVE).

## Akzeptanz

1. Ein PR, der nur Testcode außerhalb dieser Stellen ändert, läuft nach dem Hop auf develop-spitze mit
   `PR · Go unit · cli-0..3` zu `success` - oder die betroffenen Tests werden in einer Zelle ausgeführt, deren
   Voraussetzung sie wirklich erfüllen.
2. Kein Worker, keine Lane und kein Reviewer setzt Authentifizierung, Pins oder ENV selbst (§3.8). Was an
   Betreiber-/OIDC-Identität nötig ist, kommt aus der Workflow-Umgebung oder aus einer dokumentierten
   Owner-Einstellung.
3. Ein hosted run am exakten head belegt beides: vorher failure, nachher success (run-ids in der Akte).

## Grenzen und Stop

- Kein Produktwechsel an der Autorisierung selbst: die Verschärfung aus #1594/0428-053 ist vom Owner angenommen;
  diese Karte repariert den PR-Gate, nicht die Sicherheitsentscheidung.
- Wenn die Reparatur eine Änderung an `internal/operatorauth/**` oder `internal/identityprovider/**` verlangt
  (Arbeitsfeld von #1650, owner laeuft dort): STOP + MELDEN mit der einen Zeile (§4.3).

ARBEITET JETZT, kante gegen session gemessen (w198-0428-198-cligate, laptop, worktree aus develop 40cb28c758b0): der weg zurueck zu gruenen cli-shards ohne owner-env. ansatz: die zwei tests bauen ihre operator-identitaet im test auf (fixture, wie es sie im repo schon gibt), statt sie von der workflow-umgebung zu verlangen - am alten base f5ce95af war 'PR · Go unit · cli-2' naemlich executed/success (run 44759243414), die forderung kam mit #1594.Produkt-kode ist verschlossen, nur test-dateien; ist es WIRKLICH nur per umgebung loesbar, stoppt die lane und meldet (AGENTS 3.8).

ZEugen erweitert (16:5x-17:0xZ, develop noch 40cb28c758b0), damit der Befund nicht an meinem diff haengt: (1) #1718 head ce5aa9633630 = 5 failure / 9 success / 20 skipped, die vier 'PR · Go unit · cli-0..3' + 'PR Selected Checks'. (2) #1714 head 5159192dadee (gerade von der korrekturrunde gepusht) = cli-0..3 failure, ZUSAETZLICH 'PR · Go unit · packages' failure - gleiche meldung, ganz anderer inhalt. (3) STAERKSTER ZEUGE: #1615 head 80961866f9, ein PR, den der owner selbst fuehrt = 20 FAIL-CHECKS. (4) develop-eigene pushes am selben sha: 0 failure, weil die push-pfade die cli-shards nicht fahren. lane 45dddcfc arbeitet zuerst die frage, die alles entscheidet: gibt es den erlaubten test-seitigen weg, eine operator-identitaet aufzubauen (main_test.go:60 und app_secrets_shared_runtime_test.go:44 nutzen ihn nicht), oder ist es umgebung = owner. die anderen lanes erhalten von mir keine weiteren runs mehr, bis der gate gangbar ist.
