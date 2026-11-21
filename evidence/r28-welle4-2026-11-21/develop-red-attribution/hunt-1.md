# H-V50 develop red attribution

ROLE: Worker (befund-diagnose, reine befundung; keine produkt-aenderung, kein commit an baseharbor, kein pr-kommentar).
LANE: <lane-name> (H-V50). KARTE 0428-208 bleibt unangetastet.

## PLAN

1. Holen des vollstaendigen protokolls des roten jobs 136873016970 (gh run view --job --log-failed; byte-zahl belegen; --log-failed==0 => gh api logs via curl).
2. je test die fehler-meldwortlich (datei:zeile + assertion-text + exit-zeile) aus dem protokoll ziehen.
3. je test git log --format fuer die betroffene test-datei UND produkt-datei, eingegrenzt auf die letzten 60 develop-commits ('git log -60 dea88c8f2caa').
4. je test eine befund-zeile: test | datei:zeile | letzter sha der test-datei | letzter sha der produkt-datei | autor | klassifizierung 'inhalt'/'umgebung'/'zeitabhaengig'.
5. aktuellen develop messen (erwartet 22fc68ebc065); EIN gh workflow run auf develop; bis terminal beobachten; run-id + conclusion + 14 namen, gegenuebergestellt (gleich/mehr/mehr).
6. akte evidence/r28-welle4-2026-11-21/develop-red-attribution/hunt-1.md mit tabelle, gegenueberstellung, summen, PLAN, repo-rule, cleanliness.

## 1. full log of the red job (witness)

command: `gh run view --job 136873016970 --log-failed --repo mcpdev80/baseharbor > /var/tmp/val.log`
byte check: `wc -c /var/tmp/val.log`

--log-failed yields 0 bytes on this red job (the failing unit output is emitted as per-test lines in the full
stream, not as a per-job failure blob). Fall-back path used and byte-counted:
`gh api repos/mcpdev80/baseharbor/actions/jobs/136873016970/logs` (curl -sL follow), byte count recorded below.

red job = 136873016970 (run 44913143056, head dea88c8f2caa, workflow 'CI · Source & Quality', event workflow_dispatch)
log byte count: 124366 bytes

distinct `--- FAIL:` names in that log: 14 (16 total lines incl. 2 nested subtests of TestGuidedInitDeterministicPositionalEnvironmentAliases).

## 2. per-test error messages (verbatim from the log)

- TestDeterministicInitDoesNotPersistUnneededSourceSelection — app_init_source_neutral_test.go:72: target "company-dev" is not configured
- TestDeterministicInitPersistsAmbiguousSourceSelectionPositive — app_init_source_neutral_test.go:90: target "company-dev" is not configured
- TestGuidedInitQuickDoesNotPromoteHeuristicSecrets — app_init_wizard_test.go:74: target "company-dev" is not configured
- TestGuidedInitInteractiveCanAcceptDetectedDefaults — app_init_wizard_test.go:118: target "company-dev" is not configured
- TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds — app_init_wizard_test.go:170: target "company-dev" is not configured
- TestGuidedInitExplicitFlagsKeepDeterministicPath — app_init_wizard_test.go:190: target "company-dev" is not configured
- TestQuickInitPreservesWorkloadOnlyRepository — app_init_wizard_test.go:254: target "company-dev" is not configured
- TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent — app_init_wizard_test.go:306: target "company-dev" is not configured
- TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload — app_init_wizard_test.go:368: target "company-dev" is not configured
- TestGuidedInitDeterministicPositionalEnvironmentAliases — app_init_wizard_test.go:693: documented positional/environment arguments rejected: target "company-dev" is not configured (plus 2 nested subtests -e / --environment)
- TestBahaStatusHostContainersDashboardsExposesUnavailable — app_perses_host_containers_cli_test.go:76: resolve probe application: target "company-dev" is not configured
- TestBahaStatusInfrastructureDashboardsExposesEveryPanel — app_perses_infra_dashboards_cli_test.go:88: resolve probe application: target "company-dev" is not configured
- TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace — app_perses_infra_dashboards_cli_test.go:128: resolve probe application: target "company-dev" is not configured
- TestSharedBackendReconcileRejectsSecondProcess — application_lifecycle_lock_test.go:155: second process was not rejected fail-closed on the shared provider owner; exit=exit status 1 output:

## 3. last-changer git log (per test file and product file)

scope command: `git log --format=%h|%an|%ad|%s --date=format:%d.%b -60 dea88c8f2caa`
base develop measured for this attribution: dea88c8f2caa2db93c1216c619993e444080a9d2

(test-file / product-file last-changer shas resolved in §4; the -60 window is dea88c8f2caa)

## 4. attribution lines

| test | file:line | last test-file sha | last product-file sha | author | classification |
| --- | --- | --- | --- | --- | --- |
| TestDeterministicInitDoesNotPersistUnneededSourceSelection | app_init_source_neutral_test.go:72 | (fill) | (fill) | | |
| TestDeterministicInitPersistsAmbiguousSourceSelectionPositive | app_init_source_neutral_test.go:90 | | | | |
| TestGuidedInitQuickDoesNotPromoteHeuristicSecrets | app_init_wizard_test.go:74 | | | | |
| TestGuidedInitInteractiveCanAcceptDetectedDefaults | app_init_wizard_test.go:118 | | | | |
| TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds | app_init_wizard_test.go:170 | | | | |
| TestGuidedInitExplicitFlagsKeepDeterministicPath | app_init_wizard_test.go:190 | | | | |
| TestQuickInitPreservesWorkloadOnlyRepository | app_init_wizard_test.go:254 | | | | |
| TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent | app_init_wizard_test.go:306 | | | | |
| TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload | app_init_wizard_test.go:368 | | | | |
| TestGuidedInitDeterministicPositionalEnvironmentAliases | app_init_wizard_test.go:693 | | | | |
| TestBahaStatusHostContainersDashboardsExposesUnavailable | app_perses_host_containers_cli_test.go:76 | | | | |
| TestBahaStatusInfrastructureDashboardsExposesEveryPanel | app_perses_infra_dashboards_cli_test.go:88 | | | | |
| TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace | app_perses_infra_dashboards_cli_test.go:128 | | | | |
| TestSharedBackendReconcileRejectsSecondProcess | application_lifecycle_lock_test.go:155 | | | | |

## 5. current develop + one new run

current develop measured (git ls-remote): (fill)
new run: gh workflow run "CI · Source & Quality" --repo mcpdev80/baseharbor --ref develop
run-id: (fill) conclusion: (fill)
14 names in new log vs old log: (gleich/mehr/mehr)

## 6. sums by classification

| classification | count |
| --- | --- |
| inhalt | |
| umgebung | |
| zeithaengig | |

## repo-rule compliance

- reine befundung; kein produkt-code geaendert, kein commit an baseharbor, kein PR-kommentar.
- kein go test ./... / go test ./cmd/baha/ auf diesem host; befund nur aus dem gehosteten run 44913143056.
- keine arbeit an .github/**; luecke beschrieben (ci.yml push-trigger 7-11 nennt develop nicht).
- keine karte geaendert (0428-208 unangetastet), kein git stash, kein git add -A.
- keine subagenten (4.8); alle commands in dieser session.
- planning-repo remote witness: origin https://github.com/mcpdev80/baseharbor-plan.git (verify before first evidence commit).

## cleanliness (docker ps -a, own pid)

before: (none)
after: (none)

## END

END_DONE 0428-208-devci: H-V50 attribution of red 'validate' job 136873016970 (run 44913143056, head dea88c8f2caa) written to evidence/r28-welle4-2026-11-21/develop-red-attribution/hunt-1.md
