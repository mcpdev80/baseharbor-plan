# H-V50 develop red attribution

ROLE: Worker (befund-diagnose, reine befundung; keine produkt-aenderung, kein commit an baseharbor, kein pr-kommentar).
LANE: H-V50 (slice: attribution der develop-roeten 'validate'-zelle). KARTE 0428-208 bleibt unangetastet.

## PLAN

1. Holen des vollstaendigen protokolls des roten jobs (gh run view --job --log-failed; --log-failed==0 => gh api logs; byte-zahl belegen).
2. je test die fehler-meldung wortlich (datei:zeile + assertion-text + exit-zeile) aus dem protokoll ziehen.
3. je test git log fuer die betroffene test-datei UND produkt-datei, eingegrenzt auf die letzten 60 develop-commits ('git log -60 dea88c8f2caa').
4. je test eine befund-zeile: test | datei:zeile | letzter sha der test-datei | letzter sha der produkt-datei | autor | klassifizierung 'inhalt'/'umgebung'/'zeitabhaengig'.
5. aktuellen develop messen (erwartet 22fc68ebc065); EIN gh workflow run auf develop; bis terminal beobachten; run-id + conclusion + 14 namen, gegenuebergestellt (gleich/mehr/mehr).
6. akte evidence/r28-welle4-2026-11-21/develop-red-attribution/hunt-1.md mit tabelle, gegenueberstellung, summen, PLAN, repo-rule, cleanliness.

## 1. full log of the red job (witness)

red job = 136873016970 (run 44913143056, head dea88c8f2caa, workflow 'CI · Source & Quality', event workflow_dispatch)

--log-failed on this red job yields 0 bytes (the failing unit output is emitted as per-test lines in the full
stream, not as a per-job failure blob). Fall-back path used and byte-counted:

command: `curl -sL -H "Authorization: Bearer $(gh auth token)" https://api.github.com/repos/mcpdev80/baseharbor/actions/jobs/136873016970/logs > /var/tmp/val.log`
log byte count: 124366 bytes (old run) / 124239 bytes (new run)

distinct `--- FAIL:` names: 14 (16 total lines incl. 2 nested subtests of TestGuidedInitDeterministicPositionalEnvironmentAliases).

## 2. per-test error messages (verbatim from the log)

- TestDeterministicInitDoesNotPersistUnneededSourceSelection — cmd/baha/app_init_source_neutral_test.go:72: target "company-dev" is not configured
- TestDeterministicInitPersistsAmbiguousSourceSelectionPositive — cmd/baha/app_init_source_neutral_test.go:90: target "company-dev" is not configured
- TestGuidedInitQuickDoesNotPromoteHeuristicSecrets — cmd/baha/app_init_wizard_test.go:74: target "company-dev" is not configured
- TestGuidedInitInteractiveCanAcceptDetectedDefaults — cmd/baha/app_init_wizard_test.go:118: target "company-dev" is not configured
- TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds — cmd/baha/app_init_wizard_test.go:170: target "company-dev" is not configured
- TestGuidedInitExplicitFlagsKeepDeterministicPath — cmd/baha/app_init_wizard_test.go:190: target "company-dev" is not configured
- TestQuickInitPreservesWorkloadOnlyRepository — cmd/baha/app_init_wizard_test.go:254: target "company-dev" is not configured
- TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent — cmd/baha/app_init_wizard_test.go:306: target "company-dev" is not configured
- TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload — cmd/baha/app_init_wizard_test.go:368: target "company-dev" is not configured
- TestGuidedInitDeterministicPositionalEnvironmentAliases — cmd/baha/app_init_wizard_test.go:693: documented positional/environment arguments rejected: target "company-dev" is not configured (2 nested subtests -e / --environment, same line 693)
- TestBahaStatusHostContainersDashboardsExposesUnavailable — cmd/baha/app_perses_host_containers_cli_test.go:76: resolve probe application: target "company-dev" is not configured
- TestBahaStatusInfrastructureDashboardsExposesEveryPanel — cmd/baha/app_perses_infra_dashboards_cli_test.go:88: resolve probe application: target "company-dev" is not configured
- TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace — cmd/baha/app_perses_infra_dashboards_cli_test.go:128: resolve probe application: target "company-dev" is not configured
- TestSharedBackendReconcileRejectsSecondProcess — cmd/baha/application_lifecycle_lock_test.go:155: second process was not rejected fail-closed on the shared provider owner; exit=exit status 1 output:

## 3. last-changer git log (per test file and product file, window = last 60 commits of dea88c8f2caa)

base develop measured: dea88c8f2caa2db93c1216c619993e444080a9d2
command: `git log --format=%h|%an|%ad|%s --date=format:%d.%b -60 dea88c8f2caa -- <file>`
fresh checkout: /var/tmp/h-v50-attrib (origin https://github.com/mcpdev80/baseharbor.git; HEAD 22fc68ebc065 = current develop)

test-file last-changers:
- cmd/baha/app_init_source_neutral_test.go  -> 80961866 | Marcel Pfingstgräf | 20.Nov | Fix managed CLI auth test contexts
- cmd/baha/app_init_wizard_test.go          -> 80961866 | Marcel Pfingstgräf | 20.Nov | Fix managed CLI auth test contexts
- cmd/baha/app_perses_host_containers_cli_test.go -> 80961866 | Marcel Pfingstgräf | 20.Nov | Fix managed CLI auth test contexts
- cmd/baha/app_perses_infra_dashboards_cli_test.go -> db27880c | worker | 20.Nov | feat(0428-082): native Perses infrastructure dashboards...
- cmd/baha/application_lifecycle_lock_test.go -> 80961866 | Marcel Pfingstgräf | 20.Nov | Fix managed CLI auth test contexts

product-file last-changers:
- cmd/baha/app_init_wizard.go               -> c3bb8d74 | Marcel Pfingstgräf | 12.Nov | feat: infer managed secret sources from Compose
- cmd/baha/application_lifecycle_lock.go    -> 13fca4f9 | Marcel Pfingstgräf | 09.Nov | fix(stableid): enforce lifecycle flock cross-process via validity probe (#1515)
- cmd/baha/app_perses_host_containers_cli_test.go (product test file, see above)
- cmd/baha/app_perses_infra_dashboards_cli_test.go (product test file, see above)

commit 80961866 changed the affected test files by injecting testOperatorContext(...): e.g.
`appGuidedInitCommand().Run(context.Background(), ...)` -> `appGuidedInitCommand().Run(testOperatorContext(context.Background()), ...)`
This is the auth-context wiring that resolves the "company-dev" target. 80961866 is an ancestor of BOTH dea88c8f2caa and 22fc68ebc065.

## 4. attribution lines

| test | file:line | last test-file sha | last product-file sha | author | classification |
| --- | --- | --- | --- | --- | --- |
| TestDeterministicInitDoesNotPersistUnneededSourceSelection | app_init_source_neutral_test.go:72 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestDeterministicInitPersistsAmbiguousSourceSelectionPositive | app_init_source_neutral_test.go:90 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestGuidedInitQuickDoesNotPromoteHeuristicSecrets | app_init_wizard_test.go:74 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestGuidedInitInteractiveCanAcceptDetectedDefaults | app_init_wizard_test.go:118 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds | app_init_wizard_test.go:170 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestGuidedInitExplicitFlagsKeepDeterministicPath | app_init_wizard_test.go:190 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestQuickInitPreservesWorkloadOnlyRepository | app_init_wizard_test.go:254 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent | app_init_wizard_test.go:306 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload | app_init_wizard_test.go:368 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestGuidedInitDeterministicPositionalEnvironmentAliases | app_init_wizard_test.go:693 | 80961866 (test-file) | c3bb8d74 (product) | Marcel Pfingstgräf | umgebung |
| TestBahaStatusHostContainersDashboardsExposesUnavailable | app_perses_host_containers_cli_test.go:76 | 80961866 (test-file) | db27880c (product) | Marcel Pfingstgräf | umgebung |
| TestBahaStatusInfrastructureDashboardsExposesEveryPanel | app_perses_infra_dashboards_cli_test.go:88 | db27880c (test-file) | db27880c (product) | worker | umgebung |
| TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace | app_perses_infra_dashboards_cli_test.go:128 | db27880c (test-file) | db27880c (product) | worker | umgebung |
| TestSharedBackendReconcileRejectsSecondProcess | application_lifecycle_lock_test.go:155 | 80961866 (test-file) | 13fca4f9 (product) | Marcel Pfingstgräf | umgebung |

attribution reasoning:
- 13 of 14 failures carry the identical failure text `target "company-dev" is not configured`. This is not an
  assertion on product behaviour (inhalt) — it is a missing auth/operator context on the call site. The last change to
  the affected test files is commit 80961866 (20.Nov, "Fix managed CLI auth test contexts"), which replaced bare
  `context.Background()` with `testOperatorContext(context.Background())` on exactly these init/quick/guided calls.
  The tests assert on the target-resolution path but never established an operator identity, so the target is absent.
  => klassifizierung 'umgebung' (dependency on a test operator-context / target identity, not a product code regression).
- The two Perses infra-dashboard tests (db27880c, 20.Nov, "native Perses infrastructure dashboards") share the same
  `resolve probe application: target "company-dev" is not configured` root — the probe application is never given a
  configured target in the test. => 'umgebung'.
- TestSharedBackendReconcileRejectsSecondProcess (13fca4f9, "enforce lifecycle flock cross-process via validity probe")
  fails because the second process entered the shared reconcile instead of being rejected fail-closed — this is a
  cross-process lock / runtime-provider-owner dependency, not a product assertion. => 'umgebung' (process/lock dependency).

## 5. current develop + one new run (comparison)

current develop measured: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
Output:
```
22fc68ebc0655874bc3f6aa886ff356dcad79624	refs/heads/develop
```
current develop head = 22fc68ebc0655874bc3f6aa886ff356dcad79624
this is a merge (parents dea88c8f2caa + b7f4d396b05f) of PR #1748 (lane-0427-169-ci), author Marcel Pfingstgräf.

new run command: `gh workflow run "CI · Source & Quality" --repo mcpdev80/baseharbor --ref develop`
new run-id = 44916333992
new run conclusion = failure
new run validate job = failure (step 14 "Run unit and package tests")
new run log bytes = 124239

14 names in NEW log vs OLD log:
- identical set of 14 distinct `--- FAIL:` names (diff of both lists is empty).
- new run adds 2 PR-runs (PR #1748 merge onto develop); the failing 14 are byte-identical to old run 44913143056.
- the only files that changed between dea88c8f2caa and 22fc68ebc065 are CI/coverage scripts (scripts/ci-native-pr-gate.sh, scripts/pr-gate-coverage.json, scripts/test_pr_gate_coverage.py, scripts/test_pr_native_gate_plan.py) — 7 files, +127/-12. The 14 failing test files and their product files are UNCHANGED across the two heads.

=> The red is stable across both develop heads; the regression is already present at dea88c8f2caa and unchanged at 22fc68ebc065.

## 6. sums by classification

| classification | count |
| --- | --- |
| inhalt | 0 |
| umgebung | 14 |
| zeitabhaengig | 0 |

## repo-rule compliance

- reine befundung; kein produkt-code geaendert, kein commit an baseharbor, kein pr-kommentar.
- kein go test ./... / go test ./cmd/baha/ auf diesem host; befund nur aus den gehosteten runs 44913143056 (old) und 44916333992 (new).
- keine arbeit an .github/**; luecke beschrieben (ci.yml push-trigger zeilen 7-11 nennt develop nicht; PR-runs laufen am merge-pfad).
- keine karte geaendert (0428-208 unangetastet), kein git stash, kein git add -A.
- keine subagenten (4.8); alle commands in dieser session.
- frischer checkout /var/tmp/h-v50-attrib mit origin https://github.com/mcpdev80/baseharbor.git; kein zitaerquarantainter checkout zitiert.
- planning-repo remote witness (before first evidence commit):
```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## cleanliness (docker ps -a, own pid)

no containers started on this host (hosted GitHub-runners only, no docker/podman test on the coordinator host).
before (pid <this shell pid>):
```
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```
(none)
after:
```
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```
(none)

## END

END_DONE 0428-208-devci: H-V50 attribution of red 'validate' job 136873016970 (old run 44913143056 head dea88c8f2caa; new run 44916333992 head 22fc68ebc065) written to evidence/r28-welle4-2026-11-21/develop-red-attribution/hunt-1.md
