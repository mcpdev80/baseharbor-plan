# r27 welle3 · state-owner · runde-2: Probe-Befund (END_BLOCKED)

**Task / lane:** state-owner (PR #1347), lane 11 = `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
**Datum:** 2026-11-04
**Autoritativer Zweig:** `work/r27-state-owner` @ `d9a48d42` (FF von develop `3d08ef72`)
**Ergebnis runde-2:** END_BLOCKED — der 11. Failure ist ein **echter Produktions-Konflikt**, den **kein testseitiger Pfad** auflösen kann; die Platte entscheidet.

> Der Probe-Befund schließt sich an runde-1 an (isolation-vs-selection-Hypothese widerlegt: alle 10 host-env-Kreise sauber isoliert, Commit `63d7ea51`; Fix #2 inverted-mode proof `dc157b5c`). runde-2 hat die Fail-Kette per Edit-Debug lückenlos instrumentiert und die Strasse zwischen zwei kontradiktoren Production-Pfaden gezeigt.

---

## 1. Tatsachenstand (instrumentiert, reproduzierbar)

Der 11. Failure ist **nicht** `docker`-mode rootless/rootful und **nicht** ein fehlendes postgres-service im matrix-job. Die Fail-Kette ist lückenlos verfolgt:

- **Terminal-Ursache:** `runApplicationApplyLifecycle` (`cmd/baha/app_apply.go:117`) schlägt in `prepareApplicationProviderRetirement` (`cmd/baha/application_provider_retirement.go:36`) fest zu:
  `machine.ErrorOwnershipAmbiguous` / `provider_retirement_unverifiable` → *"The last consumer cannot be released without verified runtime and complete consumer inventory."*
- Der Mutate-/Apply-Pfad wird **nie** erreicht; die Failure ist ADR-0022 fail-closed auf dem RESUME-Retire-Check.
- **Reproduziert under develop's green runner state** (rootful dockerd via `sudo -n DOCKER_HOST=unix:///var/run/docker.sock go test …`) — **identisch** zu CI go-unit `126399618419` (sha `d9a48d42`):
  - lokal: `app_edit_apply_test.go:1022: real Edit lifecycle did not converge: application machine: partial … The last consumer cannot be released …`
  - CI: `DIAG_EXEC adapter executionErr=The last consumer cannot be released …` + `app_edit_apply_test.go:1007: measured post-Edit fact: … state=stopped-but-owned`.

### 1.1 Instrumentierte Fail-Kette (probe /tmp/acc-probe)

```
DBG-LOADER target="docker-dev" LoadErr=<nil> hasFile=true   # Core-Installation ist PRESENT
DBG-UNION app-pg  InstanceID="postgresql/application/…/dev-ef260e9a/default-37a8eec1"
                 Action=preserve Complete=false deps=[] anc=false   # app-eigene postgres, kein consumer
DBG-TRIP  InstanceID="runtime/bh-docker-dev-core-shared/keycloak" Complete=false consumers=1
DBG-TRIP  InstanceID="runtime/bh-docker-dev-shared/control-plane/openbao" Complete=false consumers=1
DBG-TRIP  InstanceID="runtime/bh-docker-dev-shared/control-plane/postgresql" Complete=false consumers=1
DBG-TRIP  InstanceID="postgresql/application/…/dev-ef260e9a/default-37a8eec1" Complete=false consumers=0
DBG-FACT  postgresql/application/…/…: state=stopped-but-owned anc=false deps=[]   # <- trippt zuerst (sortiert)
→ app_edit_apply_test.go:1022: partial
```

Der RESUME-Retire-Check (`prepareApplicationProviderRetirement.go:31-36`) iteriert `plan.Changes`; der **app-eigene** `postgresql/application/…` ist `stopped-but-owned`, `deps=[]`, **0 consumer** → `Action=preserve, Complete=false` → fail-closed.

### 1.2 Woher kommt die app-eigene postgres (unverifizierbar, 0 consumer)?

- `observeNativeBackendProviderFacts` (`cmd/baha/application_native_backend_observation.go`) iteriert den **von dem Test vorgeprägten** `provider-registry.json` (line 978: `Save(available)`) und leitet aus `observeCanonicalProviderContainers` (0 container → `stopped-but-owned`) die app-postgres-Fakt ab.
- Der RESUME-consumer für die app-postgres-`binding` kommt aus `resolveApplicationProviderPlanFromSnapshot` (`cmd/baha/application_provider_plan.go:94-101`), **aber** die app-eigene Zeile (`Key == "application/<appID>/…"`) ist dort **explizit ausgenommen** (`consumers[index].Key != "application/…"`). Es gibt **keinen deployment-consumer** (single-deployment-test): `DBG-DEPLOY-LOAD`/`DBG-BIND-INJECT` bleiben leer.
- **Ergebnis:** app-postgres hat in beiden Bäumen `deps=[]`, 0 consumer → `preserve, Complete=false`. Identisch.

---

## 2. Der decisive divergence: Core ist zwingend erforderlich UND fatal

Der **einzig reale** production-divergenz zwischen den Bäumen ist **nicht** die retire-pruefung (byte-identisch, siehe §3), sondern **`configureTestTarget`** in `cmd/baha/target_test_helpers_test.go`:

| Baum | `registerInstallationForTarget` in `configureTestTarget` | Core im happy-path | Retire-Check |
| --- | --- | --- | --- |
| **develop** (`3d08ef72`) | **nicht aufgerufen** | **core-free** | **kein** `control-plane/postgresql` → grün |
| **my-branch** (`d9a48d42`) | **aufgerufen** | **Core present** (`DBG-VDO installOK=true`) | injects unverifizierbaren Control-Plane → **rot** |

### 2.1 Gegenbeweis A — Core ist für die Owner-Bindung **Pflicht** (Probe: Core auskommentiert)

`configureTestTarget` **ohne** `registerInstallationForTarget` → `registerTestDeployment` (line 935) schlägt fehl:

```
app_edit_apply_test.go:935: missing deployment state for docker-dev/edit-runtime-integration/dev
  [22222222-...]: deployment has no authoritative installation owner for its Target;
  the installation must be restored before its state is loadable
  → ErrDeploymentOwnerMissing (VerifyDeploymentOwner, deployment_store.go)
```

Core ist also zwingend notwendig; ein Coreloser Pfad scheitert an der Bindung.

### 2.2 Gegenbeweis B — Core ist für den Retire-Check **fatal** (Probe: Core aktiviert)

`configureTestTarget` **mit** `registerInstallationForTarget` → `appendManagementProviderDependencies`
(`cmd/baha/application_management_dependency.go:22`) injectt die Core-Management-Fakte, deren
`Dependencies = [RuntimeStorageDependencyID(target)]` = `control-plane/postgresql`
(`internal/application/runtime_storage_dependency.go:10`, `ScopeShared`, `OwnershipBaseHarbor`,
`state=ProviderUnverifiable`) → `provider_union.go:159` setzt `Action=preserve, Complete=false` → ADR-0022.

### 2.3 Probe-Ergebnis: beide testseitigen Pfade schlagen fehl

`cmd/baha` full unit suite im sauberen git-worktree `/tmp/acc-probe` (FF my-branch HEAD), rootful dockerd:

```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (20.61s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	193.317s
```

**Einziger** Misserfolg in der gesamten `cmd/baha`-Suite; alle anderen ~280 Tests grün.
- Probe-Baum 1 (Core auskommentiert): `line 935: missing deployment state … ErrDeploymentOwnerMissing`.
- Probe-Baum 2 (Core aktiviert): `line 1022: partial … The last consumer cannot be released …`.

Beide testseitigen Wege sind damit **ausgeschöpft**.

---

## 3. Produktions-Differenz ist minimal und belegt (byte-Prüfung)

`diff` develop `d9a48d42` vs ci-access-ab/e86d39c0 — **production-only** (`*.go`, nicht `_test.go`):

| Datei | diff |
| --- | --- |
| `cmd/baha/deployment_record.go` | **nur** `TenantOwnerResolver` init + one-installation-owner binding + `installationRootFor` |
| `cmd/baha/docker_engine.go` | leer (identisch) |
| `cmd/baha/app_edit_apply.go` | leer (nur comment) |
| `cmd/baha/app_machine_adapters.go` | leer (nur comment) |
| `internal/deployment/deployment_store.go` | `VerifyDeploymentOwner` (byte-identisch zur Logik) |
| `cmd/baha/application_provider_retirement.go` | leer (identisch) |
| `cmd/baha/application_provider_plan.go` | leer (identisch) |

Die retire-pruefung (`application_provider_retirement.go:31-36`) und `VerifyDeploymentOwner` sind **byte-identisch** zwischen den Bäumen. Der einzige productive change ist die `TenantOwnerResolver`/one-installation-owner-Bindung; der retire-check unverändert.

---

## 4. Counter-belege (beide Pfade, datei:leile)

**Bindung (Core Pflicht):**
- `cmd/baha/target_test_helpers_test.go:935` (happy-path `registerTestDeployment`) → `ErrDeploymentOwnerMissing`.
- `internal/deployment/deployment_store.go` `VerifyDeploymentOwner`: `err == os.ErrNotExist → ErrDeploymentOwnerMissing`.

**Retire (Core fatal):**
- `cmd/baha/application_provider_retirement.go:33-36`: `if !plan.Complete || change.Action == "preserve"` → fail-closed.
- `cmd/baha/application_management_dependency.go:22`: Core-Installation → injectt `control-plane/postgresql` als unverifizierbare ancillary.
- `internal/application/runtime_storage_dependency.go:10`: `RuntimeStorageDependencyID` = `control-plane/postgresql`.

---

## 5. Konfliktformel (3 Zeilen)

```
core-noetig-fuer-owner-bindung : VerifyDeploymentOwner verlangt installation.json (ErrDeploymentOwnerMissing, line 935)
core-fatal-fuer-retire-check   : Core injectt control-plane/postgresql unverifizierbar → ADR-0022 (retirement.go:36)
core-notwendig-und-verifizierbar: nicht durch test-only erreichbar; Production-Aenderung an retire.pruefung = stiller ADR-0022-umbau
```

Der Happy-path braucht Core (Binding), aber Core löst den ADR-0022 fail-closed aus. Der Retire-Check überspringt `ScopeShared`-Core-Backends nicht → der Core-`control-plane/postgresql` trifft zuerst.

---

## 6. Vorschlag fuer Nachfolge-Karte

Eine Karte, die **nicht** in dieser Lane liegt (Owner-Entscheidung), mit folgenden Optionen:

1. **Production-Fix retire-check** (vorschlag): `prepareApplicationProviderRetirement` so erweitern, dass `ScopeShared && OwnershipBaseHarbor` Control-Plane-Backends (`control-plane/postgresql`/`openbao`/`keycloak`) **vor** der ADR-0022-Pruefung als `preserve`-skipped markiert werden (z.B. `change.InstanceID == RuntimeStorageDependencyID(target)` **und** `ScopeShared`/`OwnershipBaseHarbor` abfragen). Korrekt, aber **ADR-0022-Semantik-Änderung** → Owner-Freigabe erforderlich.
2. **Tenant-owner-Pfad für docker-dev**: `configureTestTarget`/`registerTestDeployment` so führen, dass `docker-dev` über `TenantOwnerResolver` (Coreless, valid access scope) admitted wird — dann kein Core, kein Control-Plane-Inject, retire-grün. Erfordert, dass `docker-dev` als echter tenant registriert ist (aktuell `TenantID=""` → `isTenant=false` → durch Core-Check).
3. **Test-Fixture**: happy-path ohne `registerInstallationForTarget`, sondern Core via eine `tenantResolvedForTarget`-grantbare tenant-target-Konfiguration; isoliert den RESUME von der Core-Dependency.

**Empfehlung:** Option 1 als korrekter Bugfix, aber nur nach Owner-Autorisierung (ADR-0022-Release-Note). Bis dahin: `blocked`/`waiting` mit dieser Evidence.

---

## 7. Hygiene

- **keine Production-Aenderung** unternommen; alle debug-Ergenzungen im probe /tmp/acc-probe zurueckgesetzt (`git checkout -- .`), `wt-branch` HEAD `d9a48d42`, working tree clean (nur `?? baha`).
- probe-baeume: `/tmp/acc-probe` (FF HEAD), `/tmp/acc-check` (FF HEAD), `/tmp/acc-ab` (FF ci-access-ab) — alle clean, **kein** commit darauf.
- CI matrix: my-branch `ci.yml` hat `go-unit-tests` = `go test ./...` → `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` wird ausgeführt; develop `validate` läuft `go test ./...` (identisch).
