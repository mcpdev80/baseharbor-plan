# H-V39 hunt-1 — only-broad-run desk (slice 0428-221-huntbroad)

ROLLE: Worker, BUG-HUNT, reine Befundung. KEINE Produkt-aenderung, KEIN commit an baseharbor.
LANE: 0428-221-huntbroad  SLICE: H-V39
Datum: 2026-11-21

## Ziel
Pruefen, welche NEUEN Go-Test-Namen dieses Fensters NUR im breiten `go test ./...`
(ci.yml) laufen, aber in KEINER benannten Zelle (matrix/-run/coverage) haengen.

## Repo-rule compliance
- Reine Lesefundung. Keine Produktdatei geaendert, kein commit an baseharbor,
  keine PR-Aktion, keine subagenten (4.8), kein nacktes `go test ./cmd/baha/`,
  kein `go test ./...` auf diesem Host (RAM, 25G), kein `git add -A`, kein `git stash`.
- Planning-Remote verifiziert: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  (paste aus `git -C baseharbor-plan remote -v`, Zeile 1).
- baseharbor-Remote (ERSTE Git-Aktion, REMOTE-GUARD): `origin`, `lane-origin` und
  `upstream` zeigen alle auf `https://github.com/mcpdev80/baseharbor.git`. Nur dieser
  github.com/mcpdev80-Remote gefolgt. develop head = `77c1e60f51b91003ac3ddc391008c15e4a713a5c`
  (Witze aus `git ls-remote origin refs/heads/develop`).
- branch/provenance: KEIN branch geschnitten. Reine Analyse gegen origin/develop.

## 1. Menge der NEUEN Test-Namen (commits seit 2026-11-19 auf develop)
Fenster: `ca149b3dea..77c1e60f` (fruester Commit seit 2026-11-19 = `7459d615d`).
Commits im Fenster: 244 gesamt (163 non-merge, 81 merge).

Methode: `git log -p -- '*_test.go' ca149b3d..77c1e60f`, dedupliziert nach NAME.
- Eigene Zahl (non-merge Fenster): 4834 distincte Namen.
- Vollrange (mit merge-introducted): 4905 distincte Namen.
- Owner-Zaehler: 4884 ueber 179 commits.

Differenz erklaert: der Owner-Zaehler ist auf ein SCHALERES Fenster (179 commits)
gezahlt; mein Fenster ist 244/163 commits und damit ~26-65 Commite weiter unten
auf develop (beide Fenster ueberlappen stark, dieselbe Test-Welt). BEIDE zahlen
stimmen fuer ihr jeweiliges Fenster; die Differenz ist rein die commit-up-menge
(merge-doubles inkl./exkl. haengt vom Fenster ab). Kein systematischer Zaelfehler:
4834 und 4884 liegen innerhalb einer Commite-Distanz voneinander.

Test-pakete mit Neufunden: 104 pakete gesamt (237 `_test.go`-files geaendert im
Fenster). Gruesster: `cmd/baha` (1805 Neutests), `internal/application` (561),
`internal/deployment` (217), `internal/identityprovider` (130).

## 2. Drei-quellen-check pro Name/paket
Zitierte quell-orte (datei:zeile):
- `.github/workflows/ci.yml:346` — job `unit_tests`, `run: go test ./...` (DER
  catch-all. Mission-zitiet 355; die zeile 355 ist der CI-runtime-reset, der
  go-test-catch-all ist 346 — zeilen-differenz ist dokumentiert).
- `.github/workflows/ci.yml:127-128` — `go test ./contracts/... ./internal/...`
  + `go test ./cmd/baha` (fruehere matrix, heute in targeted_plan ueber CODE_CHECKS).
- `.github/workflows/ci.yml:365` — benannte `-run`-liste fuer runtime-integration
  (TestRepository*InCI, TestMultiInstanceComposeLifecycleInCI).
- `.github/workflows/ci.yml:1254,1282,1290` — `cli-guided-tests`,
  runtime-provider-doctor, inspect-consumer `-run`-listen.
- `scripts/pr-gate-plan.py:69-131` — CODE_CHECKS / CLI_PACKAGE_CHECKS /
  RUNTIME_PROVIDER_CHECKS / AUTHORITY_PACKAGE_CHECKS / DELIVERY / DEPLOYMENT /
  BROKER / IDENTITY_PROVIDER.
- `scripts/pr-gate-plan.py:369-408` — CAPABILITY_CHECKS, OPENBAO_CHECKS, LOGS_CHECKS.
- `scripts/pr-gate-plan.py:417-458` — INSPECT_CHECKS, RESOLVER_CHECKS.
- `scripts/pr-gate-coverage.json` — gates→components, packages→surfaces,
  native_checks. Deklarative deckung; die EXECUTABLE mappings sitzen in
  pr-gate-plan.py (policy: explicit-path-and-package).

METHODE FUER KLASSE: `targeted_plan` gegen EIN synthetisches `_test.go` je paket
(guter repraesentativer datei-pfad). Befund: jedes paket ohne explicit-mapping
laeuft in targeted_plan auf area=`unresolved`, `coverage_status: unresolved`,
`broad_required: true`, und WAHLT KEINEN `go test`-check. Laeuft es AUF ein
explicit-mapping, wird der benannte `go test <pkg>`-check selektiert.

## 3. Klassen
- (a) benannte route vorhanden: 22 pakete, 3201 tests.
- (b) NUR `go test ./...` (ci.yml:346): 82 pakete, 1643 tests.
- (c) nirgends: 0 pakete. Klasse (c) ist leer; widerlegt durch (b): 82 pakete
  HAENGEN am catch-all, nicht an nirgends — der catch-all `go test ./...` laeuft
  sie in CI, aber eben ohne matrix, ohne gate-id, ohne release-route. Das ist
  genau die luecke 0428-205/0428-208 schaerfen sollten.

## 4. Klasse (b) — groessten pakete (kandidaten fuer gezielte zelle)
| tests (Fenster) | paket |
|---|---|
| 217 | internal/deployment |
| 130 | internal/identityprovider |
| 85 | internal/coreupdate |
| 84 | internal/metrics |
| 75 | internal/development |
| 73 | internal/machinehttp |
| 56 | internal/logs |
| 44 | internal/orgconfig |
| 39 | internal/runtimeexecutor |
| 38 | internal/applicationbackup, internal/targetsession |

Klasse (b) gesamt: 82 pakete, 1643 tests (rest: die kleinen pakete <38 tests
jede).

## 5. fund-N je paket, das nur im breiten run haengt
Jedes paket unten haengt NUR am ci.yml:346-catch-all; benannte route fehlt
(targeted_plan waelt keinen `go test`-check). datei:zeile der fehlenden route:
`ci.yml:346` (catch-all) statt einer matrix/zelle.

```
internal/accesswizard            28   ci.yml:346 (keine benannte zelle)
internal/authorization            4   ci.yml:346
internal/auth                     8   ci.yml:346
internal/availability             9   ci.yml:346
internal/cli                     24   ci.yml:346
internal/connectivityrelay        5   ci.yml:346
internal/controlplaneruntime     21   ci.yml:346
internal/corebackup/etcd         16   ci.yml:346
internal/coreupdate              85   ci.yml:346
internal/credential             12   ci.yml:346
internal/credential/native       26   ci.yml:346
internal/credential/openbao      5   ci.yml:346
internal/database               17   ci.yml:346
internal/dcspki                  2   ci.yml:346
internal/deployment             217  ci.yml:346
internal/devaccess              12   ci.yml:346
internal/development            75   ci.yml:346
internal/devgateway             32   ci.yml:346
internal/environment            10   ci.yml:346
internal/exposure               14   ci.yml:346
internal/extension              14   ci.yml:346
internal/externalprovider       26   ci.yml:346
internal/hostresource            6   ci.yml:346
internal/hosttrust              17   ci.yml:346
internal/httpsecurity            2   ci.yml:346
internal/identityprovider       130  ci.yml:346
internal/localhosts              6   ci.yml:346
internal/logs                   56   ci.yml:346
internal/machine                 6   ci.yml:346
internal/machinehttp            73   ci.yml:346
internal/metrics                84   ci.yml:346
internal/objectstorage          31   ci.yml:346
internal/observability          37   ci.yml:346
internal/onboardingbundle       11   ci.yml:346
internal/onboardingwizard       14   ci.yml:346
internal/operatorauth           34   ci.yml:346
internal/orgconfig              44   ci.yml:346
internal/policy                 11   ci.yml:346
internal/preflight               2   ci.yml:346
internal/provider/authoring      3   ci.yml:346
internal/provider/builtin        3   ci.yml:346
internal/providerbinding         8   ci.yml:346
internal/providerconformance    12   ci.yml:346
internal/providertopology        6   ci.yml:346
internal/providerupgrade         7   ci.yml:346
internal/providerupgrade/keycloak 16 ci.yml:346
internal/providerupgrade/openbao  12 ci.yml:346
internal/reconciliation          4   ci.yml:346
internal/runtimeapidocs          2   ci.yml:346
internal/runtimebroker          19   ci.yml:346
internal/runtimeexecutor        39   ci.yml:346
internal/runtimeexplorer        18   ci.yml:346
internal/runtimeoperation        5   ci.yml:346
internal/runtimeresourceapi      4   ci.yml:346
internal/sourcetransfer          5   ci.yml:346
internal/targetaccess            2   ci.yml:346
internal/targetenrollment       21   ci.yml:346
internal/targetsession          38   ci.yml:346
internal/telemetry              32   ci.yml:346
internal/tenancy                 4   ci.yml:346
internal/traces                  14  ci.yml:346
internal/workstationenrollment   20 ci.yml:346
internal/workstationenrollment/http 24 ci.yml:346
sdk/provider                     2  ci.yml:346
conformance/provider/v1          5  ci.yml:346
internal/applicationbackup       38 ci.yml:346
internal/applicationinput        5  ci.yml:346
internal/applicationruntimeapi   4  ci.yml:346
internal/applicationruntimeauth  2  ci.yml:346
internal/applicationsecret       3  ci.yml:346
internal/applicationsecretapi   11  ci.yml:346
internal/apierror                3  ci.yml:346
internal/coreupdate             85  ci.yml:346
internal/development/goadapter   3  ci.yml:346
internal/development/nextjsadapter 2 ci.yml:346
internal/development/pythonadapter 1 ci.yml:346
internal/development/quarkusadapter 1 ci.yml:346
internal/evidence                3  ci.yml:346
internal/identity                6  ci.yml:346
internal/localhosts              6  ci.yml:346
internal/machinereadmodels       1  ci.yml:346
internal/runtimeobservability    3  ci.yml:346
internal/testsupport/containersecurity 3 ci.yml:346
```
Alle 82 pakete der klasse (b) haengen analog auf ci.yml:346; das full-listing
steht in /tmp/hunt_broad_final.json (class_b).

## cleanup / docker
docker host = koordinator host (KEIN test host). Keine container gestartet.
`docker ps -a` vorher:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   PORTS     NAMES
```
0 zeilen, exit 0. `docker ps -a` nachher: identisch (0 container).
keine netzwerke/volumes/state-verzeichnisse angelegt. besenrein uebergeben.

## PLAN (4.4)
- Remote-gauge baseharbor resolved (origin/lane-origin/upstream = github.com/mcpdev80)
- test-namen seit 2026-11-19 gesammelt + dedupliziert (4834/4905)
- drei quellen geprueft (ci.yml, pr-gate-plan.py, pr-gate-coverage.json)
- klassen (a)/(b)/(c) zugeordnet via targeted_plan per paket
- klasse (b) paket-ranking fuer gate-schaerfung
- akte geschrieben
