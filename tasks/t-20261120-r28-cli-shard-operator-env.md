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
prs: [mcpdev80/baseharbor#1726]
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
    **PR:** [baseharbor#1726](https://github.com/mcpdev80/baseharbor/pull/1726)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w198-0428-198-cligate  
**Priority:** not set  
**PRs:** [baseharbor#1726](https://github.com/mcpdev80/baseharbor/pull/1726)  
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

GROESSER ALS ANFANGS VERMUTET: die gate-map 1 (evidence/r28-welle4-2026-11-20/cli-shard-operator-env/gate-map-1.md) zaehlt 14+ BRUCHSTELLEN ueber cli-0..3 UND packages, alle mit derselben meldung 'Managed-environment machine operations require an authenticated BaseHarbor operator' (plus 'operator OIDC configuration' in app_secrets_shared_runtime_test.go:44). Ancestry ist sauber (PR #1723 head 26755fc1edfb, parent EXAKT 40cb28c758b0, branch == refs/pull/1723/head) - also KEIN basis-drift und kein diff von uns. die lane arbeitet mit dieser karte: gesucht wird der EINE test-seitige weg, eine operator-identitaet in den kontext zu bringen (ihre eigene beobachtung: identity.Principal{Issuer:..., Subject:synthetic-operator} und die operatorauth.WithInteractive-naht), nicht 14 einzeln richtungen. ist die stelle durch die #1594-entscheidung WIRKSAM abgeschaltet (test kann die identitaet nicht mehr erlangen, ohne die sicherheitsentscheidung zu umgehen), lautet ihr auftrag: STOPP + MELDEN, sofort. querverweise: #1718 (APPROVED) faellt an cli-0..3, #1714 an cli + packages, #1645 an internal/identityprovider (#1650), ihre #1615 an runtime- UND cli-zellen; develop-push faehrt diese shards nicht (nur Runtime docker/podman, runs 44769994971/44769994909).

ENTSCHEIDENDER BEFUND VON MIR SELBST GEMESSEN (read-only, develop 40cb28c758b0), an die lane uebergeben - der offene owner-punkt fuer DIESEN teil ERLEDIGT sich damit: die test-seitige Betreiber-Identitaet existiert bereits als MUSTER, kein ENV und kein neuer mechanismus noetig. (1) HELFER internal/operatorauth/context.go:54 'func WithVerifiedPrincipal(ctx, principal *identity.Principal) context.Context'. (2) VERBREITUNG: git grep -l operatorauth. -- '*_test.go' = 27 test-dateien nutzen ihn schon (15x Login, 14x WithVerifiedPrincipal, 11x EnvIssuer, 10x WithEnforcement, 9x WithMembershipProvider). (3) KANONISCHES BEISPIEL cmd/baha/app_input_resolver_first_run_test.go:21-27 (principal Subject 'authenticated-fixture', Issuer https://issuer.example, IssuerVerified true, Groups [editor], dann WithVerifiedPrincipal + WithMembershipProvider). (4) BRUCHSTELLE cmd/baha/adoption_bug_regression_test.go:42/65/91/107/167 rufen 'runWithIO(context.Background(), ...)' - der context traegt KEINE principal; seit 2af892e4e (policy.go:47-48 TLSRequired/AuthenticationRequired, :64/:68 environment/provider is required) ist das genau die meldung aus internal/operatorauth/authorization.go:285. AUFTRAG: eine sammelstelle (ihre cmd/baha/operator_test_fixture_test.go) nach diesem muster, die 14+ stellen aus gate-map-1 rufen sie an; was test-seitig NICHT geht (internal/logs Loki-multi-source = karte 0428-202, policy-seite, owner-rail) aussenpunkten + file:line melden, kein test faellt weg (§5.4). ZUSATZ: todo-datei haengt bei 2/6 seit 80 min (AGENTS 4.4), nach jedem schritt neu schreiben.

PR EXISTIERT, ABER DER GATE IST NICHT ZU - MESSEN, DARUM BLEIBT active UND SITZ IST ANGEBHALTEN. #1726 head 8b2cb2a97cab, base develop, draft=false, 5 dateien, ancestry auf develop JA. run 44796949092 am exakten head: 9 success / 8 failure / 19 skipped - rot: cli-0..3, packages, 'PR Selected Checks', 'PR · Native Keycloak/Core · docker' UND 'podman'. cli-0 job 136499688758: 63x 'authenticated BaseHarbor operator.', 15x 'operator OIDC configuration is required for managed envir...', fehlende falling laut log-zaehler: TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools (15), TestPersesLifecycleTransportActionMatrix (13), TestRestoreBindsOriginalExternalIdentityAndProtectedDestination (9), TestRestoreBindsCurrentExternalReceiverAndAuthorization (6), TestGuidedRepositoryRuntimeFixtureRegressionSuite (6). ANSATZ, aus dem patch gelesen: test-seam im produkt-code cmd/baha/main.go (+9: 'if testOperatorContext != nil { ctx = testOperatorContext(ctx) }', in produktion nil) + cmd/baha/operator_test_fixture_test.go (+59) + main_test.go / app_secrets_shared_runtime_test.go (+4 je) + app_init_wizard.go (+7). ICH HABE DEN PRODUKT-EINGRIFF AKZEPTIERT, UNTER DER AUFLAGEDASS die akte ihn ausdruecklich als test-seam nennt mit der belege-zeile (§4.2: dokumentiert = loesung, verschwiegen = verstoss). DREI FORDERUNGEN AN DIE LANE (kurz, ohne neuen matrix-run, §5.4): (1) wirkt der seam GLOBAL (ein shared helper/TestMain in cmd/baha) oder stellenweise, und wie viele der 14+ bruchstellen aus gate-map-1 damit verdrahtet SIND; (2) warum fallen die zwei 'Native Keycloak/Core'-zellen aus - das sind keine cli-unit-zellen, wenn dort eine andere ursache spricht, wird daraus eine eigne karte; (3) was liegt ausserhalb ihres write-sets. ZUSAETZLICH ANGEBOten als entscheidungshilfe: das muster, das ES AUF develop schon gibt - 't.Setenv(operatorauth.EnvIssuer / EnvClientID)' + 'operatorauth.WithVerifiedPrincipal' + 'WithMembershipProvider', so wie cmd/baha/app_input_resolver_first_run_test.go:21-27 es zeigt und 27 test-dateien es nutzen; ein einziger shared helper in cmd/baha ersetzt ZAHLREICHE einzeln verdrahtete falling. PFLICHTVERSTOESE DER LANE, von mir angehalten: todo-datei 104 minuten nicht beruehrt (AGENTS 4.4) und KEIN AKTEN-COMMIT unter evidence/r28-welle4-2026-11-20/cli-shard-operator-env/ seit 19:08 ('git log -- <pfad>'), waehrend der PR laeuft - ein PR ohne aktenstand ist halbe arbeit (§5.3). wenn die naechste runde wieder ohne zeugen endet, ist das ein fall fuer §3.6 (strategiewechsel, nicht ausdauer).
