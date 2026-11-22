# 0428-231 round-2 — correction round: fan-out complete in all five CLI test files

Verdict of reviewer (static-cells-operator-auth-helper/review-1761-head5794874302f.md): REQUEST CHANGES, "helper fan-out unvollständig", HOLD, PR bleibt DRAFT. Diese Runde zieht jeden einzelnen beweis-punkt nach.

KANIDATEN-KETTE: 57948743 (round-1, unverändert erhalten) -> e0d4a0e3 (vollständiger fan-out der fünf dateien) -> d275e50c (semantik-fix: WithVerifiedTestOperator behält die if-absent preserve-existing-principal route der 30 testOperatorContext-call-sites; ohne diesen commit hätte e0d4a0e3 ein nicht-verifiziertes principal in target_definition_change_test.go durch das kanonische ersetzt und das denial-verhalten geaendert). Finaler head: d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0. KEIN rebase/amend/force; alles additive commits auf demselben kandidat.

## PLAN

- (done) 1. Review-akte vollständig gelesen (plan origin/main, ls-tree-witness unten); beweis-punkte: drei dateien mit handkomposition (app_env_test.go:35-38, app_export_command_test.go:369-377 + :392-400, installation_destroy_native_test.go:45-47), target_definition_change_test.go dateiname unverändert (nur transitiv), static-cell/native jobs auf dem draft-run skipped.
- (done) 2. Fan-out vollständig gemacht: helper exportiert jetzt WithVerifiedTestOperatorPrincipal (Haupt-Einstieg, principal-first wie die ersetzte hand-sequence) + WithVerifiedTestOperatorPrincipalForced (force-reihenfolge) + WithVerifiedTestOperatorPrincipalIfAbsent (reines if-absent-primitive) + TestPrincipal(issuer, subject) für fixture-identitäten; ALLE fünf dateien rufen den helper auf; keine zweite provider-definitie; keine produkt-semantik (assert-Zahlen unverändert, nur setup-Zeilen).
- (done) 3. Develop-abgleich: ls-remote develop = 52a3c5446f41a1dd8678d99875e4cb1eee67874c (#1756 gemergd, wie befohlen); base-behind=0, kein merge-commit nötig; KEIN rebase/amend/force — commit 57948743 bleibt erhalten, e0d4a0e3 und d275e50c ADDIV darauf.
- (done) 4. bash scripts/ci-fast-check.sh OK (302 tests); source-readability-audit PASS; gofmt clean; pushes ohne force; delivery-witness: refs/pull/1761/head = d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0.
- (done) 5. Gehoster run 44998552411 (head d275e50c) terminal completed SUCCESS, failed 0; CLI-suite job-ids: cli-0 137134801858, cli-1 137134801765, cli-2 137134801777, cli-3 137134801792, packages 137134801752 (alle success). Der zwischen-run 44997681554 (head e0d4a0e3, SUCCESS failed 0) blieb als vorlaeufiger beweis erhalten; static cells/Native bleiben auf draft-route skipped — ready-schalten ist keine lane-aktion, PR bleibt DRAFT.
- (done) 6. Diese akte, publiciert auf plan origin/main mit ls-tree-witness.
- (done) 7. END post aan 9142ab1f (met both missions: 236 STOP + 231 korrektur DONE).

## beweis-punkt für beweis-punkt: befund -> was geaendert wurde -> job-id

- befund: `runWithIOAndOperator` (app_env_test.go:35-38) komponierte enforcement/principal/provider selbst -> geaendert: eine zeile `operatorauth.WithVerifiedTestOperatorPrincipalForced(ctx, principal)` (force-reihenfolge wie zuvor; das EXPLIZITE principal-argument bleibt, identitäten erhalten; die zwei inline `&identity.Principal{...}` fixture-operator literals in app_env_test.go sind jetzt `operatorauth.TestPrincipal(...)`); die table-driven denial case (:170-172) nutzt `WithVerifiedTestOperatorPrincipal` + ihren expliziten firstRunMembershipProvider (bewusst — sie testet DENIAL, der helper-provider darf ihre memberships nicht ersetzen) -> job-id 137134801765 (cli-1, success; TestAppEnv* in ./cmd/baha shard).
- befund: `appExportAuthorizedTestContext` (:369-377) und `appExportFixtureContext` (:392-400) wiederholten die handkomposition -> geaendert: beide sind jetzt ein aufruf `WithVerifiedTestOperatorPrincipalForced(context.Background(), TestPrincipal(issuer, subject))` mit ihren eigenen identitäten (export-operator / export-fixture-operator bleiben getrennt) -> job-id 137134801777 (cli-2, success).
- befund: installation_destroy_native_test.go:45-47 komponierte manuell -> geaendert: `operator := operatorauth.TestPrincipal("https://issuer.example", "installation-destroy-operator")` + `ctx = operatorauth.WithVerifiedTestOperatorPrincipalIfAbsent(ctx, operator)`; das vorher im ctx gesetzte, NICHT-verifizierte principal bleibt erhalten und die if-absent-semanitik wirkt weiter (identisches fail-closed verhalten); dieselbe identität läuft via runWithIOAndOperator -> job-id cli-shard (native test skipped ohne native runtime — wie bisher, nicht verschleiert).
- befund: target_definition_change_test.go war unbedate (nur transitiv via testOperatorContext) -> geaendert: datei jetzt dabei: die anderen call-sites nutzen testOperatorContext->helper; die override-zeile :41 nutzt `WithVerifiedTestOperatorPrincipal(..., TestPrincipal("https://issuer.example", "synthetic-operator"))` — principal-first wie vorher, also ersetzt das NICHT-verifizierte synthetic-principal das kanonische (deny-verhalten identisch; der haupt-Einstieg hat genau diese semantik; d275e50c stellt zusaetzlich sicher, dass die 30 reinen testOperatorContext-sites ihr bestehendes principal weiter erhalten) -> job-id 137134801765 (cli-1: TestTargetDefinitionRejectsUnprovenTenantOwnership, success).
- befund: static-cell evidence fehlte (draft-run skipped Validation/Native/Selected-Runtime) -> stand: draft-route fuehrt die shard-suite aus (4 cli shards + packages, alle success auf d275e50c); die static cells sind an den ready-schalter gebunden — der liegt beim handoff bei coordinator/owner; die lane schaltet nicht ready, PR bleibt DRAFT.

## helper: welche der fuenf dateien rufen jetzt den helper auf

- cmd/baha/test_operator_context_test.go — `testOperatorContext` = `operatorauth.WithVerifiedTestOperator(ctx)`.
- cmd/baha/app_env_test.go — runWithIOAndOperator + table-case + beide fixture-operators: helper.
- cmd/baha/app_export_command_test.go — beide context-funktionen: helper.
- cmd/baha/installation_destroy_native_test.go — principal + composition: helper (TestPrincipal + WithVerifiedTestOperatorPrincipalIfAbsent).
- cmd/baha/target_definition_change_test.go — override-zeile: helper (WithVerifiedTestOperatorPrincipal + TestPrincipal).

Diff-stat develop...HEAD (finaler head d275e50c):

```
 cmd/baha/app_env_test.go                     |  37 +++-----
 cmd/baha/app_export_command_test.go          |  21 +----
 cmd/baha/installation_destroy_native_test.go |  12 +--
 cmd/baha/target_definition_change_test.go    |   4 +-
 cmd/baha/test_operator_context_test.go       |  13 +--
 internal/operatorauth/test_operator.go       | 132 +++++++++++++++++++++++++++
 6 files changed, 153 insertions(+), 66 deletions(-)
```

## Provenance + witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = 52a3c5446f41a1dd8678d99875e4cb1eee67874c; `git merge-base --is-ancestor 52a3c5446f41 HEAD` → yes (base-behind=0).
- `git log --oneline origin/develop..HEAD` → genau drei commits, ALLE von mir (57948743, e0d4a0e3, d275e50c), kein fronder commit.
- `git diff origin/develop...HEAD --name-only` → die 6 pfade oben; KEINE .github/**, KEINE scripts/**.
- pushes ohne force; `git ls-remote … refs/heads/lane-0428-231-static-auth-helper refs/pull/1761/head` → beide `d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0`.

## Gehostete runs

- run 44998552411 (pull_request, head d275e50c): completed SUCCESS, failed 0. Jobs: cli-0 137134801858, cli-1 137134801765, cli-2 137134801777, cli-3 137134801792, packages 137134801752.
- run 44997681554 (pull_request, head e0d4a0e3): completed SUCCESS, failed 0 (jobs 137132145738/…5700/…5697/…5608/…5737) — zwischenkandidat, superseded by d275e50c (semantik-fix noetig; Grund in der Kette oben).

## Checks lokal (kein Ersatz fuer hosted)

- go build ./... ok; go vet ./cmd/baha ./internal/operatorauth ok; gofmt 0; go test -run XXX_NONE (compile-only); named runs `go test ./cmd/baha/ -count=1 -run 'TestAppEnvMasksSecrets|TestAppCredsReveal|TestAppExport|TestTargetDefinitionRejectsUnproven' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` ok; ci-fast-check.sh 302 tests OK; source-readability-audit PASS.

## repo-rule compliance

- Write set: internal/operatorauth/** (dieselbe datei wie round-1) + die fuenf cmd/baha test-dateien. Keine produkt-semantik, keine interface-erweiterung, keine .github/**-, keine scripts/**-aenderung, kein broker, keine aktion auf PR #1753/#1746. PR #1761 bleibt DRAFT. Keine subagenten; hosted runs sind der beweis.

## cleanliness

cleanliness: nothing started. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries (host of this session is not a test host; nichts gestartet). Keine container/netzwerke/volumes; GOCACHE=/var/tmp/go-cache-0428-231; worktree workers/0428-231-authhelper-wt (Lane-Zone).

## plan-repo remote witness

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (erste zeile):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
```

END 0428-223-testctx DONE (0428-231 korrekturronde: branch lane-0428-231-static-auth-helper, neuer head d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0, base 52a3c544 base-behind=0, PR #1761 draft, run 44998552411 completed SUCCESS failed 0, alle fuenf dateien auf dem helper, cleanliness: nothing started)

## origin/main evidence witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep static-cells-operator-auth-helper`:

```
evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/review-1761-head5794874302f.md
evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/round-1.md
evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/round-2.md
tasks/t-20261122-static-cells-operator-auth-helper.md
```
