# Bug-Hunt H-V17 'NE-ANSETZER-DESK' — round-1 (purebefundung)

Lane: `w187-0428-187-huntrestart` · Task: Bug-Hunt-Schnitt H-V17 (§3.3.5) · Datum: 2026-11-20

Reine Befundung des develop-Standes. KEINE ProduktAenderung, KEINE Tests, KEIN `.github/**`, KEIN Board, KEIN PR.

## PLAN

- Mission H-V17 gelesen (Ziel, Pruefinhalte, Grenzen, Akte).
- Remote-Realitaet verifiziert (Remote-Name, develop-HEAD, frischer Klon).
- Basis 96f2ae11a25a gegen aktuelle develop-Quelle geprueft (STALE: nicht vorhanden).
- Schnitt 1 (Neustart/Dauerhaftigkeit) befunt: signals.json-Dump + Neuregistrierung.
- Schnitt 2 (Fehlerpfad statt Erfolgpfad) befunt: fail-closed-Stellen.
- Schnitt 3 (Signal-/Registry-Raum) befunt: RegisterProviderSignals vs Update/UpdateSignal + PruneOwnedProviderInstances.
- Evidence-Datei geschrieben.
- Evidence auf origin/main committen + Abgleich.
- END-SATZ an Owner.

## realitaets-zeugnisse (remote)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
f5ce95afce1cfec053dd7717ed05e89bfe153535	refs/heads/develop
```
```
$ cd /tmp/opencode/hunt-hv17-wt && git clone --depth 1 https://github.com/mcpdev80/baseharbor.git hunt-hv17-wt
From https://github.com/mcpdev80/baseharbor ... branch develop -> FETCH_HEAD
HEAD c000c5db fix(release): accept exact develop source after squash merge (#1675)
$ git fetch --unshallow origin develop   # Bestaetigung: develop-HEAD = c000c5db
```
Basis-Attest: der Klon ist am develop-HEAD `c000c5db2560c471fe84842136e03d6e54d96779` (fresh clone + unshallow, Remote github.com/mcpdev80). `96f2ae11a25a` ist auf dieser Quelle nicht der develop-HEAD; die im Mission-Pruefinhalt genannte Postgres-Runtime-Privilegien-Liste (#1711), legacy-signal-umschreibung (0428-168), collisions-guard (0428-166, provider_registration.go/migration.go) und per-terminal context (0428-068/0713) existieren auf diesem develop-Stand NICHT als Artefakt (keine `provider_registration.go`, kein `migration.go`, kein `legacy-signal`-Symbol; Postgres-GRANT steht in `internal/runtime/shared_core_sql.go`/`shared_backends_runtime.go`). Die Basis ist STALE. Befundung erfolgte am aktuellen develop-Top `c000c5d`.

## funde

### FUND 1 (Schnitt 1): Persistierung des Signaturzustands = DUMP, kein Query
- Datei: `internal/observability/registry.go:306-312` (`registryPath`) — `filepath.Join(dir, "observability", "signals.json")`, `dir` = `bhruntime.DataDir("")`.
- Schadensbild: Der Ueberlebende-Endzustand einer Anlage ist die physische `signals.json` im Data-Root. Ein Provider-Signal wird NUR durch `RegisterProviderSignals` (Descriptor-by-ID, Prune-vor-Anhaengen) neu in den Zustand geschrieben; es gibt auf diesem develop KEINen abgeleiteten Weg, einen fehlenden Signal-Eintrag aus dem laufenden Betrieb (Compose-Instanz / Deployment-Owner) zu re-Query und nachzuschreiben. Ueberlebt also nur, was in `signals.json` steht.
- FUND-FUER-KARTE: restart-persist-signals.json | internal/observability/registry.go:306-312 | Zustand = DUMP; Neuanlage nur ueber RegisterProviderSignals, kein Re-Query aus Betrieb/Deployment

### FUND 2 (Schnitt 2): `RuntimeTarget`/`ParseRuntimeTarget` fail-closed
- Datei: `internal/observability/registry.go:257-272`.
- Schadensbild: `RuntimeTarget(project, service)` leitet `runtime://<project>/<service>`; `ParseRuntimeTarget` akzeptiert nur `runtime://`-Prasfix mit nicht-leerem Projekt und ohne nachgestelltem `/`. Leere/Fremd-Ziele pruefen auf `ok=false` (kein stilles `return nil`). Call-Sites: `internal/logs/render.go:270`, `internal/logs/query.go:110,150`, `internal/logs/overrides.go:132`, `internal/application/runtime_observability.go:112`.
- FUND-FUER-KARTE: restart-runtimetarget-failclosed | internal/observability/registry.go:257-272 | Leere/Fremd-Targets pruefen ok=false, kein stilles nil; Call-Sites logs/query + runtime_observability

### FUND 3 (Schnitt 2): `RegisterProviderSignals` fail-closed, kein stilles null
- Datei: `internal/observability/registry.go:180-255`.
- Schadensbild: Jede Abweichung — leerer `ID`, ungultiges `Descriptor`, deklariertes-Signal-vor-`enabled`, nicht-`Collectable`, Signal ohne Runtime-Realisierung, fehlende Runtime-Realisierung — ist ein `error` (kein `return nil`). Call-Sites `internal/telemetry/realization.go:196`, `internal/logs/realization.go:232`, `internal/application/runtime_observability.go:86`, `internal/traces/tempo.go:403` propagieren den Fehler (kein Swallow).
- FUND-FUER-KARTE: restart-registerprovider-signal-failclosed | internal/observability/registry.go:180-255 | Unerwuenschter Zustand = error, kein stilles nil; propagiert durch alle Realisierungen

### FUND 4 (Schnitt 2): `mutate` reused in-place slice → Race gegen koncurrierende Signal-Write
- Datei: `internal/observability/registry.go:472-513` (`mutate`) / `read:515-530`.
- Schadensbild: `mutate` lockt nur `signals.json.lock` (`syscall.Flock`, exklusiv). Ein zweiter Prozess/Schreibpfad ohne dieses Lock (kein shared-FS-Lock ueber den Data-Root hinweg garantiert) kann Lese-Slice (`sources`) wiedernutzen waehrend `mutate` sortiert/`WriteFile` schreibt → interliegendes Schreiben in dieselbe Datei, nicht atomar. `RegisterProviderSignals` fuehrt ausserdem `out := sources[:0]` + Anhaengen IN-PLAACE aus; ein paralleler Reader ohne Lock liest teils sortierte/teils unveraenderte Slice.
- FUND-FUER-KARTE: restart-signalregistry-race | internal/observability/registry.go:472-513,515-530 | Kein prozessuebergreifendes Lock; in-place slice-Reuse atomar-Write gefahrdet

### FUND 5 (Schnitt 3): `RegisterProviderSignals` ist der EINE aktive Signal-Anlegungspfad
- Datei: `internal/observability/registry.go:180-255`; Call-Sites `internal/telemetry/realization.go:196`, `internal/logs/realization.go:232`, `internal/application/runtime_observability.go:86`, `internal/traces/tempo.go:403`.
- Schadensbild: `Update`/`UpdateSignal` (registry.go:314-336) haben AUF DIESEM develop KEINEN Live-Caller (nur Tests: `internal/observability/registry_test.go:19,193,218`, `internal/metrics/runtime_source_retention_test.go:23`). Der aktuelle Signaturanlegungsfad ist EIN (`RegisterProviderSignals`, per Descriptor-by-ID, Prune-vor-Anhaengen). Mischung alter/neue Pfade ist auf diesem Stand nicht realisierbar; ein "zweiter Weg" existiert nur als totem Codepfad.
- FUND-FUER-KARTE: signal-one-active-path | internal/observability/registry.go:180-255,314-336 | Update/UpdateSignal nur Tests; RegisterProviderSignals = EINE aktive Anlegung; kein Mischungsszenario

### FUND 6 (Schnitt 3): `PruneOwnedProviderInstances` loescht per X-Produkt (ID nicht im Prune-Key)
- Datei: `internal/observability/registry.go:274-291`.
- Schadensbild: Prune filtert nach `source.Provider && source.Class && source.Scope && source.OwnerApplication` und laesst alle uebrigen durch. Der Prune-Key (`keepIDs`) enthaelt nur die IDs der in `instances` erkannten Service-Instanzen. Loescht also alle Signale des (Provider,Class,Scope,Owner)-Tupels — unabhaengig vom `kind`. Trifft das Signal aus FUND 1 (`ID` ohne `kind`-Komponente) ueber `runtime://`-Target mit fremdem Projekt/Service, so loescht ein naechster Run ein Signal einer anderen `kind`/`project`-Kombination mit, wenn (Provider,Class,Scope,Owner) gleich ist. Kein fail-closed, kein stilles nil — ein Duplikats-/Ueberschreibefekt.
- FUND-FUER-KARTE: signal-prune-crossproduct-dup | internal/observability/registry.go:274-291 | Prune nach Provider/Class/Scope/Owner, loescht alle kinds der Gruppe; ID-Key nicht prune-key → Duplikat/Ueberschreibefekt

## befundlos (mit Zeugen)

- **Schnitt 1 Neustart-Dauerhaftigkeit:** keine andere Persistierungsstelle als `signals.json` gefunden. `grep -rn "signals.json\|registryPath" --include='*.go' internal/` → nur `observability/registry.go`. Kein Re-Query-Pfad aus Betrieb.
- **Schnitt 2 Postgres-Runtime-Privilegien:** Artefakt #1711 fehlt auf develop. `find . -name '*provider_registration*'; grep -rln "postgres.*priv\|runtimeUser\|RuntimeUser"` → keine Runtime-Privilegien-Zeile; GRANT/CREATE ROLE in `internal/runtime/shared_core_sql.go` (NOSUPERUSER/NOCREATEDB...) + `shared_backends_runtime.go`. Fail-closed-Verhalten stattdessen ueber `RuntimeTarget`/`RegisterProviderSignals` belegt (Funde 2/3).
- **Schnitt 3 collisions-guard (0428-166 provider_registration.go/migration.go):** diese Dateien existieren nicht auf develop. `find . -name '*provider_registration*' -o -name '*migration*.go'` → keine Treffer; collision-guard-Thema ist auf diesem Stand nicht im Signal-Registry-Bereich present.

## repo-rule compliance

- KEIN Produktcode geaendert (nur Lesen im frischen Klon `/tmp/opencode/hunt-hv17-wt`).
- KEINE Tests geaendert.
- KEIN `.github/**` geaendert.
- KEIN Board (`workers/todos` nur die Lane-todo, kein Produkt-board).
- KEIN PR, KEIN Push, KEIN Merge.
- KEIN Subagent/Task-Tool zum Schreiben/Pushen/Mergen.
- KEIN `git add -A`.
- Keine Container/Compose/Run auf dem Session-Host gestartet.
- Remote-Witness nur ueber `git ls-remote` + frischen Klon; quarantinierte Checkout-Ref (`workers/baseharbor`) NICHT zitiert.

## cleanliness: vorher/nachher

- container: keine gestartet (ps-witness: `n/a`).
- netzwerke: keine erstellt.
- volumes: keine erstellt.
- state-verzeichnisse: kein produkt-/board-state veraendert; Klon nur in `/tmp/opencode/hunt-hv17-wt` (temporaer, loeschtbar).
- ambient-core/ bilder fremder karren: unangetastet.

---

## END
END_DONE w187-0428-187-huntrestart: Bug-Hunt H-V17 NE-ANSETZER-DESK — 6 Funde (Basis STALE, Befundung am develop-top c000c5d), keine ProduktAenderung, kein PR.
