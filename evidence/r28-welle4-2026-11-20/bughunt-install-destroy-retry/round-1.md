# H-V13 BugHunt — install / destroy / retry (card t-20261120-r28-bughunt-install-destroy-retry, 0428-170)

ROLLE: worker, reine Befundung. KEINE Produktänderung, KEIN Commit am Produkt-Branch, KEIN Merge, KEIN PR.
Schnitt: reine statische Quellen-Analyse der releasedese von develop. Kein Container/VM gestartet.

## BEWEISREGEL

```
git ls-remote origin refs/heads/develop
f61ef0f4991cae88727c02b731d862bf395d8984	refs/heads/develop
```
Messener develop-head, gegen den gelesen: `f61ef0f4991cae88727c02b731d862bf395d8984`
Klon: `/tmp/xh13-dev` (vollständiger Clone, `origin/develop` auf `f61ef0f4`).

## PLAN
1. Messenen develop-head klonen und Anchor-Dateien verifizieren
2. Schnitt 1 (destroy): jeder geschriebene Zustand + jeder Löschpfad
3. Schnitt 2 (retry nach Abbruch): führt Fortsetzung durch denselben Pfad
4. Schnitt 3 (Idempotenz): zweiter destroy-run = no-mutation
5. Schnitt 4 (Nebenläufigkeit): zweiter Lock-Writer verliert stille Information
6. Akte schreiben, cleanliness, END_DONE

## Kontext / Anker (von Mission gemessen)
- `.github/workflows/docker-runtime-acceptance.yml:146-148` = Job `Validate real installation destroy and interrupted retry`, ruft `bash scripts/ci-native-installation-destroy.sh` auf.
- `scripts/ci-native-installation-destroy.sh` ruft `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` (`-p 1`) und `TestSecondSameHostCoreNativeConflictInCI` (`-p 1`, `BASEHARBOR_SECOND_TARGET_NATIVE_ACCEPTANCE=1`) aus.
- Lock-Kernel: `internal/stableid/lock.go`, `internal/stableid/lock_unix.go`. `AcquireStateFileLock` (was die Mission als `target_id.go:67-80` zitiert) existiert auf develop in `internal/stableid/lock.go:305-320` (Re-Export über `internal/coreinstallation/lifecycle_lock.go`).
- `MigrateLegacyTargetUIDs` existiert auf develop NICHT mehr (historisch). Idempotenz-Vorbild `target_id.go:88` liegt so nicht vor; maßgebliches Vergleichsmuster ist `AcquireAppLifecycleLock`/`reclaimStaleAppLock` in `internal/stableid/lock.go:158-226` und `removeApplicationState` in `cmd/baha/app_destroy_lifecycle.go:622-681`.

## Schnitt 1 — destroy: was bleibt nach einem vollständigen destroy zurück?

### Finden 1 (ERWARTET / VERTRAG — kein Fund): Ein vollständiger `destroy --all` hinterlässt KEINen produktiven Restzustand; jeder geschriebene Zustand hat einen Löschpfad.
Weg der Prüfung: Aufrufkette `destroyInstallation` (`cmd/baha/runtime_destroy_all.go:97`) wird für jeden Target durch `destroyTargetBestEffort` (`cmd/baha/runtime_destroy_all.go:335`) abgearbeitet; am Ende (`cmd/baha/runtime_destroy_all.go:466`) wird bei `blockers == 0` `removeFullDestroyLocalState` aufgerufen.

Was geschrieben wird → wer es löscht, je Zustand:
- **Compose-Projekte (Container/Netzwerke/Volumes)**: `compose.DestroyProject` (`internal/runtime/compose.go:85`) = `down --volumes` (+`--remove-orphans` bei `DestroyProjectRemoveOrphans`, `compose_resources.go:368` via `ReleaseSharedBackendApplication` `shared_backends_resources_runtime.go:402`). Nachweis: `compose.go:89` `down --volumes` entfernt die Volumes; `compose.go:115` `down --volumes --remove-orphans`. Der Test verlangt residual-freien Zustand: `installation_destroy_native_test.go` prüft nach erfolgreichem Destroy `len(identityAfter) == 0` (`installation_destroy_native_test.go` unteres Ende) und `native("volume","inspect",volume)` == Fehler (Volume gone).
- **Application-State-Verzeichnis `<store>/apps/<name>`**: `removeApplicationState` (`cmd/baha/app_destroy_lifecycle.go:622`) ruft `Store.Delete`, `DeleteDeploymentRecord` (`internal/deployment/deployment_identity_drift.go:21` = `os.RemoveAll(root)`), `os.RemoveAll(repositoryTLSDirName)`. Verifiziert durch `installation_destroy_native_test.go` (`os.Stat(r.TargetStateRoot) == ErrNotExist`).
- **Target-Config (`config.yaml`)**: `removeFullDestroyLocalState` (`cmd/baha/runtime_destroy_all.go:525`) = `os.RemoveAll(configRoot)`; geprüft durch `os.Stat(config) == ErrNotExist`.
- **Target-State-Root (`<root>/targets/<name>`)**: `removeFullDestroyLocalState` (`cmd/baha/runtime_destroy_all.go:514`) = `os.RemoveAll(dataRoot)` (DataRoot = `internal/deployment/target.go:109`); geprüft durch `os.Stat(r.TargetStateRoot) == ErrNotExist`.
- **Lock-Dotfiles (`.installation.lock`, `.bootstrap.lock`, `.<id>.app_installation.lock`)**: Der Kernelflock wird mit `file.Close()` freigegeben (`lock_unix.go:399`-Rückgabe, `lock_unix.go:279` `LOCK_UN`). Der Installations-/Target-State-Root wird am Ende `os.RemoveAll` — die Dotfile lebt im State-Root und fällt mit. Es gibt KEINen separaten Lock-Leichnam außerhalb des entfernten Roots.
- **Host-CA-Trust**: `hosttrust.RemoveOwnedDetailed` (`cmd/baha/runtime_destroy_all.go:104` `removeHostTrustForFullDestroy`), entfernt nach erfolgreichem Runtime-Cleanup (`runtime_destroy_all.go:404`), unverified Anchors bleiben PRESERVED (Vertrag).
- **Connectivity-Rules**: `releaseFullDestroyConnectivity` + `destroyTargetBestEffort` (`runtime_destroy_all.go:247`, `runtime_destroy_all.go:362`) = `suspendConnectivityRuleAt` + `application.RemoveConnectivityRuleAt` + `connectivityrelay.RemoveFilesAt`.

VERHALTEN KORREKT (Schnitt 1): Ein vollständiger destroy mit `blockers == 0` entfernt State-Verzeichnis, Config, Compose-Projekte inkl. Volumes/Netzwerke, Deployment-Records und damit alle Lock-Dotfiles. Jeder Zustand hat einen dokumentierten Löschpfad. Der Test `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` verlangt exakt residual-freien Zustand (Identity/Volumes/Config/StateRoot alle `ErrNotExist`) und schlägt mit `t.Fatal`, falls etwas übrig bleibt — also ein fail-closed-Vertrag, der „REST BLEIBT" sofort als Fehler meldet.

### Finden 2 (IST — kleiner Befund, nicht blockierend): Der in-use owned Data-Volume wird beim ersten Destroy nicht gelöscht, sondern der Run als FAILED markiert und der Retry-Owner behalten.
- Stelle: `cmd/baha/runtime_destroy_all.go:253` (zweiter destroy in CI-Script, `in-use owned volume deletion`), ruft `destroyInstallation` auf; ein `docker volume rm` auf ein von `alpine` genutztes Volume schlägt fehl (`removeOwnedProjectResources` `compose_resources.go:436` `volume rm` gibt `err` zurück).
- Folge: `destroyTargetBestEffort` (`runtime_destroy_all.go:335`) setzt bei `countFullDestroyBlockers > 0` den Target als `SKIPPED ... preserved because one or more target runtime resources could not be removed` (`runtime_destroy_all.go:456`) und gibt am Ende `destroyInstallation` einen Fehler zurück (`runtime_destroy_all.go:478`).
- Der Test erwartet dieses Verhalten: `installation_destroy_native_test.go` (`if err := destroyInstallation(...); err == nil { t.Fatal("in-use owned volume deletion falsely succeeded") }`) und prüft `os.Stat(r.TargetStateRoot) == nil` => `t.Fatal("partial installation destroy removed its retry owner")` => der Retry-Owner bleibt.
ERWARTET/IST: Das ist beabsichtigt — ein in-use Volume ist ein Blocker, der den Destroy abbricht, den Retry-Owner aber bewusst BEHAHLT. Kein Datenverlust, kein „stiller Rest"; der Zustand ist ein sauberer, behelfsamer Fail-closed-Zustand. Kein Fund im Sinne eines Bugs.

## Schnitt 2 — retry nach Abbruch (Abbruch ZWISCHEN den Schritten desselben Vorgangs)

### Finden 3 (ERWARTET / VERTRAG — kein Fund): Ein Abbruch während des Core-Installationslaufs hinterläßt einen deterministisch wieder aufnehmbaren Zustand; der nächste Run läuft durch denselben Pfad.
Weg der Prüfung: `coreinstallation.Run` (`internal/coreinstallation/installation.go:141`).
- Vor jedem Schritt `save(root, state)` mit `state.Phase = <stepname>` (`installation.go:197`); ein Abbruch in `steps.SQL/Secrets/Identity/Verify` hinterläßt `state.Phase = "<step>_failed"`, `state.Ready = false`, persistente `installation.json` (`installation.go:205` `state.Phase = action.name + "_failed"`).
- `save` schreibt atomar via `os.CreateTemp` + `fsync` + `os.Rename` (`installation.go:112-136`) — kein zerbrochener State-Header bei SIGKILL.
- Neuster Run: `Load` (`installation.go:66`) findet die bestehende `installation.json` (nicht `ErrNotExist`), prüft `state.Spec == spec` (`installation.go:168`), und fährt mit demselben `state.ID` fort — `Run` merkt `state.Spec`-Konflikt und sagt keinen Ersatz (`installation.go:168`). Eine fehlgeschlagene Phase wird erneut ausgeführt; die Identität (`installation_id`) wird nie neuManufacturiert.
- Der Installations-Lock `AcquireLifecycleLock` (`internal/stableid/lock.go:58`) über `<root>` serialisiert parallel laufende Instanzen (Fail-closed bei Contention), also kein Race beim Resume.
- Für die App-Ebene: `executeApplicationDestroyLifecycle` (`cmd/baha/app_destroy_lifecycle.go`) / `advanceInstallationDestruction` (`cmd/baha/installation_destroy_continuation.go:34`) bauen den Restplan bei jedem Run neu (`currentInstallationDestructionImpact`), kein persistierter Teilplan, der hängen bleiben kann; der `stale-impact-consent`-Check (`runtime_destroy_all.go:229`) fängt nur Plan-Drift, keinen Zustandshang.

VERHALTEN KORREKT (Schnitt 2): Abbruch ZWISCHEN Core-Schritten hinterläßt eine persistente `<step>_failed`-`installation.json`; der nächste Run `Load`-et sie, behält Identität + Spec, und wiederholt die fehlgeschlagene Phase durch denselben Pfad. Kein nur-von-Hand-behebbarer Zustand. Der CI-Retry-Schnitt (`ci-native-installation-destroy.sh`) läuft über denselben `go test`-Weg.

## Schnitt 3 — Idempotenz (zweiter destroy-run = no-mutation)

Vergleichsmuster: Mission zitiert `target_id.go:88`. Diese Datei existiert auf develop nicht; maßgeblich ist die identische no-mutation-Struktur `reclaimStaleAppLock` (`internal/stableid/lock.go:158-226`) und `removeApplicationState` (`cmd/baha/app_destroy_lifecycle.go:622-681`).

### Finden 4 (ERWARTET / VERTRAG — kein Fund): Zweiter destroy-run auf bereits-leerem Zustand ist no-mutation und schlägt fail-closed.
- `removeApplicationState`: `os.Stat(appDir)` — wenn `ErrNotExist`, kein `Store.Delete`; am Ende `DeleteDeploymentRecord` (`deployment_identity_drift.go:21`), und `assertOnDiskIdentityMatches` (`deployment_identity_drift.go:46`) behandelt `os.ErrNotExist` als „already gone: idempotent removal, not a drift" => `os.RemoveAll` auf nicht-existierendem Root ist ein no-op. Also zweiter Lauf: kein Remote-Mutation, Report `NOT FOUND`-Kategorie.
- `Load` (`installation.go:66`): bei fehlender `installation.json` (`ErrNotExist`) startet `Run` neu (`installation.go:149`) — aber ein zweiter destroy ohne installiertes Core findet keinen Core mehr (`collectTargetDestroyInventory` meldet `NOT FOUND`), also kein Blocker, kein Rest.
- Lock-Dotfiles: `AcquireAppLifecycleLock` (`lock.go:124`) reclaimt stale Receipts unter `.installation.lock`, `reclaimStaleAppLock` (`lock.go:190`) — beim zweitenlauf existiert der Receipt nicht mehr (`os.ErrNotExist` => `return false, nil`), also kein doppelter Abriss, kein Fehler.
- `destroyTargetBestEffort` meldet bei fehlendem `runtime`-Projekt `NOT FOUND` (`runtime_destroy_all.go:403`) => kein Blocker.

VERHALTEN KORREKT (Schnitt 3): Zweiter destroy-run auf leerem Zustand ist no-mutation: `ErrNotExist` wird überall als „bereits weg" behandelt (`deployment_identity_drift.go:46`, `reclaimStaleAppLock:190`, `removeApplicationState`-`Stat`). Keine seitliche Änderung, kein Crash. Kein Fund.

## Schnitt 4 — Nebenläufigkeit (zwei gleichzeitige Zugriffe auf dieselbe state-lock)

### Finden 5 (ERWARTET / VERTRAG — kein Fund): Ein zweiter Lock-Writer verliert stille Information; die Lock wird fail-closed abgelehnt.
Weg der Prüfung: `lockNamed` (`internal/stableid/lock_unix.go:283`).
- `unix.Flock(fd, LOCK_EX|LOCK_NB)` — nicht-blockierend. Contention (`EWOULDBLOCK`/`EAGAIN`) => `return nil, fmt.Errorf("%s: %w", message, err)` (`lock_unix.go:305`). Der Writer ERHÄLT einen Fehler, verliert aber NIEMALS still eine Information: Der zweite_writer kann den kritischen Bereich nicht betreten, also kann er keinen Receipt überschreiben, keine Dotfile anlegen und keine Daten schreiben.
- Der Receipt wird NACH dem erfolgreichen Lock geschrieben (`lock_unix.go:374`), also kann kein Writer ohne Lock je schreiben.
- `AcquireAppLifecycleLock` (`lock.go:124`): Contention fließt in `acquireLifecycleUnderRetry` (`cmd/baha/application_lifecycle_lock.go:110`), das bis 15s mit Jitter/Jitter-Backoff retryt; ein LIVE-Halter wird niemals reclaimt (`lockHolderLive` `lock_unix.go:221` => `return true` wenn pid alive), also kein „stiller Abriss" eines lebten Receipts. Nur ein confirmed-stale (`ESRCH`/früherer-Boot-ID)-Receipt wird reclaimt (`reclaimStaleAppLock` `lock.go:207`).
- `lockHolderLive` (`lock_unix.go:221`): Fail-closed — ein `EPERM` (anderer User, alive) => `return true` (live => nicht reclaimt); `ESRCH` (tot) => `false` (reclaimbar). Kein Weg, auf dem ein zweiter Writer einem lebten Owner Information entzieht.
- Target-wide Mutation (destroy) ruft `AcquireTargetWideLifecycleLock` (`lock.go:272`), der die Dotfile-Scan gegen lokale App-Lifecycle fail-closed macht (`deploymentsHaveAppLocks` `lock.go:114`, Fail-closed auf Read-Error `lock.go:129`). Destroy kann also niemals während einer lokalen App-Lifecycle „drüberschreiben".

VERHALTEN KORREKT (Schnitt 4): Zwei gleichzeitige Writer auf dieselbe Lock — einer bekommt `EWOULDBLOCK`/Fail-closed-Fehler, kein stiller Informationsverlust. Die Dotfile wird erst nach erfolgreichem Lock geschrieben, ein LIVE-Halter wird niemals reclaimt, ein stale Receipt nur unter der shared critical section. Kein Lock-Bypass-Pfad (file:line) vorhanden. Kein Fund.

## Zusammenfassung Funde
- Schnitt 1: VERHALTEN KORREKT. Kein Restzustand ohne Löschpfad; jeder Zustand hat dokumentierten Löschpfad. (Finden 2 = beabsichtigter fail-closed Blocker bei in-use Volume, kein Bug.)
- Schnitt 2: VERHALTEN KORREKT. Abbruch ZWISCHEN Schritten => persistente `<step>_failed`-`installation.json`, deterministischer Resume durch denselben Pfad, Identität bleibt.
- Schnitt 3: VERHALTEN KORREKT. Zweiter destroy-run = no-mutation (`ErrNotExist`-everywhere).
- Schnitt 4: VERHALTEN KORREKT. Zweiter Lock-Writer => fail-closed, kein stiller Informationsverlust.
- GESAMT: 0 produktive Funde. Alle vier Schnitte zeigen fail-closed/korrektes Verhalten. Befundlos mit Begründung — jeder Punkt mit datei:zeile belegt.

## repo-rule compliance
- Rolle Worker, reine Befundung: erfüllt. KEINE Produkt-Datei geschrieben, KEIN Commit, KEIN PR, KEIN Merge.
- `.github/**` NICHT angefasst; KE workflow_rerun/workflow_dispatch ausgelöst.
- KEIN Container/Compose/VM dieses Shifts gestartet — rein statische Quellen-Analyse.
- Kein subagent/task/agent-tool verwendet (§4.8).
- Remote-Witness nur via `git ls-remote origin refs/heads/develop` + Voll-Clone `/tmp/xh13-dev`. Der quarantinierte Ref `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` wurde NICHT zitiert.

## cleanliness:
- BEFORE: keine Container, keine Volumes, keine Netzwerke, kein State-Verzeichnis dieses Shifts. `docker ps -a` enthält keinen `alpine`/`foreign`/`install-retry`-Halter.
- AFTER: identisch. Kein Container/Netzwerk/Volume/State-Verzeichnis angelegt. Der Klon `/tmp/xh13-dev` liegt unter `/tmp` (außerhalb des Ecosystem-Roots) und wird mit `rm -rf` bereinigt.
- cleanliness: CLEAN — kein Runtime-Rest dieses Shifts.
