# BF-05 — bad config quiet (0428-094), round 1

- Mission: `/var/tmp/missions/mission-094-config-quiet.md` (karte t-20261115-bughunt-d28-bad-config-quiet, 0428-094)
- Rolle: Worker — Implementierung + Regression, keine Prüfung
- Basis der Lane: `develop@14d8f17d` (Merge PR #1624, DSR3-Precedenz: HEAD = Merge, nicht develop-Tip `34c2ede5`)
- Ziel-Branche: `lane-0428-094-config-fail`, PR-Base `develop`, DRAFT (frost)
- Build-Zeugnis: `go1.26.8`, `go build -o baha ./cmd/baha` exit 0

## STATUS: fertig — Fix + Tests green, CI #1666 grün, PR DRAFT, Evidence auf origin/main (END_READY)

## 1. Reproduktion — wo die config-beladung fehler verschluckt (file:line)

BF-05: eine korrumpierte `config.yaml` wird vom daemon STILL ignoriert; `baha target list` läuft mit
implizitem Default-Target (exit 0), statt laut zu scheitern.

**Exakter Evidence-Repro (auf `develop@0e9ccb582` und `develop@34c2ede5` beide reproduziert):**

```
$ printf 'version: 1\n\tBAD INDENT {{{\n' > $H/.config/baseharbor/config.yaml
$ env HOME=$H XDG_CONFIG_HOME=$H/.config/baseharbor baha target list
TARGET               RUNTIME      ACCESS               ACCESS PROVIDER      SCOPE            SELECTOR
local                docker       local                local                default          implicit,effective
exit=0
```

**Ursache (file:line):** `internal/deployment/target.go` — `ConfigPath()` (XDG-Zweig, Zeile ~99-101)
prepended `baseharbor/` auf `XDG_CONFIG_HOME`. Bei `XDG_CONFIG_HOME=$H/.config/baseharbor` aufgelöst:

```
$H/.config/baseharbor/baseharbor/config.yaml   <- diese Datei existiert nicht
```

Die vom Nutzer geschriebene Datei `$H/.config/baseharbor/config.yaml` liegt eine Ebene HÖHER und wird
**nie gelesen**; `LoadConfig()` sieht `os.ErrNotExist` am aufgelösten Pfad und liefert sauber den
leeren Default zurück. `target list` synthetisiert dann den impliziten `local`-Target. Exit 0, kein
Fehler, kein Hinweis. Der Nutzer arbeitet gegen ein anderes Target als beabsichtigt.

**Zweite, erreichbare Oberfläche (identische stillschiegende Kategorie):** eine leere/whitespace-only
`config.yaml` aufgelöst scheitert früher mit obskurem `unsupported BaseHarbor config version 0` — auch
kein klares "dies ist keine Konfiguration".

**Gegenprobe, dass die Umgebung (nicht ein Test-Artefakt) entscheidet:** Standardpfad
(`XDG_CONFIG_HOME=$H/.config`, also `$H/.config/baseharbor/config.yaml` als aufgelösten Pfad) schlägt
bereits laut fehl — der Bug betrifft specifically die XDG-Doppel-Append-Konstellation und den
leeren-Default-Durchlauf.

## 2. Fix — fail loud statt stillschiegend

Variante gewählt: **fail loud mit klarer Meldung** (nicht dokumentierter Fallback), konsistent mit der
bestehenden error-handling-Präzedenz im Produkt — `decodeConfig` schlägt bereits laut bei
Unparsebarkeit an (`parse BaseHarbor config: %w`), und Target-Referenz-Fehler scheitern hart
(`references unknown access`). Das Produkt favorisiert fail-closed/fail-loud; ein stillschiegender
Fallback für eine korrumpierte Config wäre ein Open-End-Risiko.

Änderungen in `internal/deployment/target.go`:

- `LoadConfig()`: nach `os.ReadFile` —
  - `os.ErrNotExist` am aufgelösten Pfad: wenn der Config-Root belegt ist (siehe Helfer), `ErrConfigMissing`
    laut zurückgeben; sonst sauberer leerer Default (unverändert). Schließt den Evidence-Repro.
  - leere/whitespace-only Datei: sauberer leerer Default statt `version 0`-Fehler (kein klares Signal).
- Neue Sentinel-Variable `ErrConfigMissing`: "BaseHarbor config root is configured but the config.yaml is missing".
- Neue Helfer `dirExistsAndHasBaseharborState(dir)`: zwei präzise Signale, KEIN spekulatives Hochklettern
  über eine Ebene hinaus (sonst False-Positive auf leere Roots / fremde Temp-Dirs):
  1. `config.yaml` genau eine Ebene über dem aufgelösten Pfad (XDG-Doppel-Append),
  2. aufgelöster Config-Dir trägt Deployment-Marker (`active-target`, `.installation.lock`).
  Nur Deployment-Marker zählen; `active.json`/`organization/` (separates orgconfig-System) zählt NICHT —
  verhindert Regression in orgconfig-Scoping-Tests.

**Warum minimal:** kein Umbau von `ConfigPath()`/XDG-Konvention, kein neuer Parse-Pfad, nur die
Missing/Empty-Fälle werden hörbar. `decodeConfig` bleibt alleiniger Parse-Enforcer.

## 3. Regression — defekte Datei -> expected Verhalten, CI-Zuordnung

Neue Tests in `internal/deployment/config_fail_loud_test.go` (Package `deployment`):

- `TestLoadConfigFailsLoudOnUnparseableConfig` — korrumpierte Config aufgelöst -> laut fehlschlagend.
- `TestLoadConfigMissingUnderPopulatedRootFailsLoud` — Config-Root belegt, `config.yaml` fehlt -> `ErrConfigMissing`.
- `TestLoadConfigMissingUnderEmptyRootSucceeds` — leerer Config-Root -> sauberer Default (keine Regression).
- `TestLoadConfigEmptyFileSucceeds` — leere Datei -> sauberer Default statt `version 0`.
- `TestLoadConfigValidStillLoads` — gültige Config lädt normal.
- `TestDirExistsAndHasBaseharborState` — Helfer: belegt ja, org-config-only nein, leer nein, weg nein.

**CI-Aufnahme (Owner-Direktive 2026-11-07):** der Test liegt im Package `internal/deployment` und
wird von der Go-test-Gruppe in `.github/workflows/ci.yml` Zeile 124 ausgeführt
(`go test ./contracts/... ./internal/... ./spec/...`). Diese Gruppe feuert per
`pull_request` auf `develop`/`main`/`lane-*` (ci.yml Zeilen 12-18, inkl.
`converted_to_draft`), also auch an PR #1666. Der neue Test ist damit dauerhafte
CI-Evidence; der Workflow selbst bleibt Owner-Scope und wurde nicht editiert.

## 4. build / vet / gofmt

```
go build -o baha ./cmd/baha            # exit 0
go vet ./internal/deployment/... ./cmd/baha/   # clean
gofmt -l internal/deployment/target.go internal/deployment/config_fail_loud_test.go  # (leer = sauber)
```

**Testergebnisse (lokal, go1.26.8):**

- `./internal/deployment/...` ok
- `./internal/orgconfig/...` ok
- `./cmd/baha/` target + org-scope (inkl. `TestOrganizationTargetOverrideCannotBypassManagedConstraint`) ok

## 5. Terminaler CI-Run (PR #1666, Run 43952223844)

Die Go-unit-Shards, die `internal/deployment` abdeckten, liefen an und sind grün:

- `Draft Go · cli-0` pass (3m50s), `cli-1` pass (2m15s), `cli-2` pass (5m4s), `cli-3` pass (3m3s)
- `Draft Go · packages` pass (3m21s); `Draft source and routing` pass
- Run-ID: https://github.com/mcpdev80/baseharbor/actions/runs/43952223844

Kein roter Pflicht-Check.

## 5. End-to-End-Verifikation (eigener Build, absoluter Pfad)

```
# Evidence-Repro -> jetzt laut:
$ env HOME=$H XDG_CONFIG_HOME=$H/.config/baseharbor baha target list
Error: BaseHarbor config root is configured but the config.yaml is missing: .../baseharbor/baseharbor/config.yaml
exit=1

# Standard, leer, kein Config -> weiterhin sauber:
$ env HOME=$H XDG_CONFIG_HOME=$H/.config baha target list   # exit 0, implicit local
# leere config.yaml -> weiterhin sauber:                      # exit 0, implicit local
```

## Repo-Rule-Compliance

- Write-Set auf `internal/deployment/target.go` + `internal/deployment/config_fail_loud_test.go` — nur Produkt, kein `.github/**`.
- Kein Merge, kein `ready_for_review`, kein force-push, kein workflow_dispatch, kein subagent (§4.8).
- Build-Artefakte unter `.tmpbuild-094/` (Scratch, NICHT committen; nur staged: die zwei Source-Dateien).
- Evidence lebt in baseharbor-plan, nirgends im Produkt-Repo.

## Branch-Provenanz

```
$ git rev-parse HEAD                 # 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95
$ git ls-remote origin develop ...   # develop-Tip 34c2ede5; 14d8f17d ist Ancestor davon
$ git merge-base --is-ancestor 14d8f17d origin/develop && echo YES
YES
```

Base `14d8f17d` ist Ancestor von `origin/develop` (DSR3: HEAD = Merge #1624, nicht develop-Tip).
Kein foreign candidate auf der Lane.

## Cleanliness

Build-Zone `.tmpbuild-094/` unter dem Produkt-Repo (Scratch, wird nicht committet). Keine
Container/Compose/Volumes gestartet (kein Docker/Podman-Testrequired). Kein fremder Arbeitsbaum
berührt.

## END

END_DONE mission-094-config-quiet.md: Fix implementiert + lokal green (build/vet/gofmt, deployment +
cmd/baha + orgconfig). Branch `lane-0428-094-config-fail` = `5b0197a9` (Base `14d8f17d`, Ancestor
von develop), PR #1666 DRAFT, Base develop. Terminaler CI Run 43952223844: Go-unit-Shards
cli-0/1/2/3 + packages alle pass. Evidence auf origin/main (`27677405`). Kein Merge, kein
force-push.
