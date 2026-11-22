# Bug-hunt gate-selection round-1 — read-only (PR #1763 is under review at 1450c201 elsewhere)

Schnitt: Pre-Release/runtime-beleg-abdeckung van develop-releasedesse `8629450ef3c`, thema GATE-AUSWAHL (geen overlap met de 227/237/241-hunts). Read-only; geen product-/workflow-/scripts-wijziging, geen commit/push/merge/kommentar, geen subagenten.

## PLAN

1. (done) Read-only vastgesteld: eigen pid 3738731, `docker ps -a` BEFORE = 0; remote truth alleen via `git ls-remote https://github.com/mcpdev80/baseharbor.git` en `gh api`/`gh run view` op de URL-repo; PR #1763 head = `c698d1310ed5a2d5178affb956ba8af2051d0a5b`, develop = `8629450ef3c` (beide gemeten vóór de lezing).
2. (done) Fund (a): matrix-Ableitung en de lege-matrix-oorzaak, file:line hieronder.
3. (done) Fund (b): de EINE bedingung die bij lege matrix SKIPPED i.p.v. FAIL geeft, voor alle vier selected-runtime-reihen, job-if + datei:zeile.
4. (done) Fund (c): PR #1763 diff vs develop, welke tests (datei:funktion) het diagnostics-pad ECHT dekken, in welke shard-rij, met aktions-bewijs.
5. (done) Akte + publicatie (deze file), ls-tree-witness op plan origin/main.
6. (pending) END post aan 9142ab1f.

## Fund (a) — waar de native-gate matrix wordt afgeleid, en waarom app_broker.go ledig is

- Afleiding: `.github/workflows/ci.yml:478-524` (job `pr_native_impact`, name 'PR · Native gate plan'): regel 502 `git cat-file -e "$BASE_SHA:scripts/pr-native-gate-plan.py"`, regels 507-509 roepen `scripts/pr-native-gate-plan.py --changed-paths-file … --coverage scripts/pr-gate-coverage.json`; regel 516 `required="true" if matrix["include"] else "false"`. De planner resolveert paths via `scripts/validate-pr-gate-coverage.py:66-83` (`resolve_native_checks`: exact `component.get("path") in changed_paths` — geen prefix, geen glob).
- Waarom LEEDIG voor deze kandidat: `cmd/baha/app_broker.go` en `cmd/baha/app_broker_diagnostics_test.go` hebben GEEN component-rij in `scripts/pr-gate-coverage.json` (gemeten: `'app_broker' in catalog == False` op develop `8629450ef3c`; de 190 components zijn exact-path). De component-lijst in de catalog wordt gespiegeld door de owner-reviewde path-map in `scripts/pr-gate-plan.py:161-177` (`NATIVE_TEST_GATE_COMPONENTS`) — ook daar ontbreekt app_broker. De PR-diff van #1763 raakt uitsluitend die twee paden, dus `include=[]` en `required=false`.
- Aktie-bevestiging op de kandidaat: job `137175578131` (PR · Native gate plan, run 45011815553) success; step 'Select exact PR native impact' toont de afleiding en `Set output 'matrix'`; de downstream-reihen zijn daarna skipped (fund b). Dit sluit aan op kaart **0428-242** (catalogus-gat): een aendering alleen in cmd/baha/app_broker.go kan NOOIT een native gate selecteren tot er component-rijen bestaan.

## Fund (b) — de vier selected-runtime-reihen: EINE required-vlag per reeks geeft SKIPPED i.p.v. FAIL bij lege selectie

(elke reeks is gekoppeld aan één booleaanse plan-output; bij false slaat de hele job over — er is geen "else fail"-tak, dus een lege/leadige selectie is ONZICHTBAAR groen in het run-aggregat.)

- `PR · Native · ${{ matrix.id }}`: `.github/workflows/ci.yml:527`, if op zeile 531 eindigt met `needs.pr_native_impact.outputs.required == 'true'` — de vlag uit fund (a) (`matrix['include']` leadig => false).
- `PR · Selected Runtime`: `.github/workflows/ci.yml:1425`, if zeile 1427: `needs.pr_plan.outputs.runtime_required == 'true'` (plus candidate/runner-interface success-poorten). De vlag komt uit `scripts/pr-selected-runtime-matrix.py` via de plan-job (ci.yml:902-903 `runtime_required="$(…["required"]…)"`).
- `PR · Selected Core-less · ${{ matrix.runtime }}`: ci.yml:1444, if zeile 1446: `needs.pr_plan.outputs.integration_required == 'true'` — weerom één vlag, false => skipped.
- `PR · Native Keycloak/Core · ${{ matrix.runtime }}`: ci.yml:1461, if zeile 1463: `needs.pr_plan.outputs.owner_node_required == 'true'`.
- Bewijs 'skipped != groen' op deze kandidat: run 45011815553 jobs 137175608612 / 137175634681 / 137175634905 / 137175634276 allemaal conclusion=skipped terwijl het run-aggregat SUCCESS is — de aggregate kan dus SUCCESS zijn zonder dat EEN native/selected-runtime-gate heeft gedraaid. Dat is precies de val die deze hunt snijdt: gate-selectie is afwezig, niet geslaagd.

## Fund (c) — PR #1763 diff vs develop: echte dekkende tests en hun shard-rij

- Diff (gemeten `git diff 8629450ef3c…c698d1310 --name-only`): `cmd/baha/app_broker.go` (+173), `cmd/baha/app_broker_diagnostics_test.go` (nieuw, +134).
- Echte dekkende tests (datei:funktion), allemaal in `cmd/baha/app_broker_diagnostics_test.go`:
  - `TestRuntimeBrokerReadinessFailureCarriesDependencyDiagnostics` — rijgt de ECHTE failure-tak `failRuntimeBrokerReadiness` (het pad dat `ensureAndStartRuntimeBrokerWithCore` bij readiness-falure teruggeeft, app_broker.go:230) en asserteert de dependency-NAAM in de fouttekst.
  - `TestRuntimeBrokerReadinessDiagnosticsNameTheDependency` — asserteert beide kanalen (log-woord + readyz name/status/version) in `runtimeBrokerReadinessDiagnostics`.
  - `TestRuntimeBrokerReadinessDiagnosticsProbeFailureIsNoted` — vaste note bij probe-falure, geen raw exec-detail.
  - `TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker` — security-beleg (5 subcases): `token=abc123` mag in GEEN enkele kanaalvariant in de uitgaande tekst verschijnen, de veilige naam wél.
  - `brokerDiagnosticsFixture` (`LogsProject`/`ExecProject` antwoorden) dekt de diagnose-kanalen; de producerende code in app_broker.go wordt alleen via de vier functies hierboven geoefend — de echte container-combinatie blijft native-gate-werk (fund a: niet selecteerbaar zonder catalogus-rij).
- Shard-plaatsbepaling met aktions-bewijs: deterministische replica van `scripts/pr-go-unit-shard.py:60-72` (sha256(cohort:name)-hash % 4) over de 1865 ontdekte cmd/baha testnamen: `…FailureCarriesDependencyDiagnostics`, `…NameTheDependency` en `…NeverEchoesValueMarker` => **cli-0**; `…ProbeFailureIsNoted` => **cli-1**. Aktie: jobs 137175633047 (cli-0) en 137175633032 (cli-1) in run 45011815553, beide executed+success; het shard-script faalt leadig als een geselecteerde test niet uitgevoerd wordt (`missing = set(selected) - executed`, regel 107), dus success == de tests zijn WERKELIJK gedraaid op head c698d1310.

## Stop-criteria niet geraakt

Geen produkt-/workflow-/scripts-wĳziging nodig voor deze snit; alles leesbaar uit de bron en de gehoste jobs.

## cleanliness

cleanliness: read-only, besenrein. Eigen pid 3738731. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries. Niets gestart, geen commit/push in enig repo; scratch `/var/tmp/0428-223-hunt-*` (logs/yml-extracten) verwijderd voor END; worktrees workers/0428-240-brokerdiag-wt onverandert (git status 0).

END 0428-223-testctx DONE (hunt gate-selection: fund a ci.yml:478-524 + validate-pr-gate-coverage.py:66-83 + catalogus zonder app_broker; fund b ci.yml:531/1427/1444/1461 required==true => skipped-niet-fail, bewezen skipped in run 45011815553; fund c vier tests in app_broker_diagnostics_test.go dekken het diagnostics-pad echt, cli-0 job 137175633047 + cli-1 137175633032 executed success; cleanliness: read-only, besenrein)
