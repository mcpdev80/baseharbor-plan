# BF-05 — bad config quiet (0428-094), round 2 (Luna batch17 REQUEST CHANGES, Object 2)

- Mission: `/var/tmp/missions/mission-094-config-quiet-r2-luna.md` (karte 0428-094, Korrektur-Runde)
- Akte: `evidence/r28-welle3-2026-11-16/batch17/act-luna-batch17.md` — Verdict Object 2: **REQUEST CHANGES**
- Rolle: Worker — Implementierung + Regression, keine Prüfung
- Basis der Lane: `lane-0428-094-config-fail` @ `5b0197a9c` (fix #1666, Object 1)
- Ziel-Branche: `lane-0428-094-config-fail`, PR #1666 DRAFT (frost)
- Build-Zeugnis: `go1.26.8`, `go build -o baha ./cmd/baha` exit 0

## STATUS: fertig — korrektur-push fe00c7f1 belegt, exact-head CI #43958812007 SUCCESS, END_READY

## 1. Rezept-Punkt-Punkt (Luna batch17, Verdict Object 2)

Luna beanstandete an `5b0197a9c` zwei Dinge an **Object 2 / PR #1666**:

1. **leere config.yaml nicht fail-laut.** `LoadConfig()` lieferte für eine existierende, leere
   `config.yaml` den impliziten Default zurück — genau das BF-05-Still-schieben. Luna forderte:
   clean-default **nur** wenn die Datei ABWESENT und der resolved root genuin empty; eine existierende
   leere Datei -> handlungsfähiger Fehler der `ErrConfigMissing`-Familie.
2. **End-to-End-Regression im echten XDG-Pfad**, nicht nur gegen die Prüfhelfer-Legende.
   Konkrete 4-Fall-Matrix: exists+empty vs missing vs corrupt vs valid — je einer, am aufgelösten
   XDG-Pfad (`XDG_CONFIG_HOME/baseharbor/config.yaml`).

Entscheidend: der Fix muss minimal und konsistent zur bestehenden fail-closed-Präzedenz sein, und die
Regression muss am realen Auflösungspfad laufen — die Prüfhelfer-Legende allein zählt nicht als Evidence.

## 2. Fix — fail-laut-entscheidung (file:line)

`internal/deployment/target.go`:

- **Neues Sentinel `ErrConfigEmpty`** (Zeile ~25f), in der `ErrConfigMissing`-Familie:
  `"BaseHarbor config root is configured but the config.yaml is empty"`.
- **`LoadConfig()` umstrukturiert** (alte Zeilen ~155-176):
  - `os.ReadFile(path)` — `os.ErrNotExist`: belegter Root -> `ErrConfigMissing` laut, leerer Root ->
    sauberer leerer Default (unverändert).
  - **`len(bytes.TrimSpace(data)) == 0` (existierende Datei):** zurück `ErrConfigEmpty` laut — **kein
    sauberer Default mehr**. Nur noch eine ABWESENDE Datei erreicht den Default. Schließt Luna-Bestand 1.
  - gültige Datei -> `decodeConfig(data)` als einziger Parse-Enforcer (unverändert).
- `ErrConfigMissing`-Doku um Hinweis auf Schwester `ErrConfigEmpty` ergänzt.

**Minimal, kein Umbau:** `ConfigPath()`/XDG-Konvention, `decodeConfig`, Target-Referenz-Fehler
unverändert. Nur der Missing-/Empty-Fall wird hörbar; `bytes` bleibt im Einsatz (Empty-Check).

## 3. Regression — 4-Fall-Matrix am realen XDG-Pfad + Test-Matrix

`internal/deployment/config_fail_loud_test.go` (Package `deployment`):

- **`TestLoadConfigExistingEmptyFileFailsLoud`** — zwei Subfälle `empty` (0 Byte) und `whitespace`
  (`"   \n\t \n"`) am aufgelösten Pfad; verlangt `err != nil` **und** `errors.Is(err, ErrConfigEmpty)`.
- **`TestLoadConfigEndToEndXDGPath`** — 4 Fälle, jeder gegen denselben aufgelösten XDG-Pfad
  (`XDG_CONFIG_HOME/<tmp>/.config/baseharbor/config.yaml`), nacheinander:
  1. exists+empty → `ErrConfigEmpty` (fail-laut, nicht Default).
  2. missing → sauberer leerer Default (`len(Targets)==0 && len(Access)==0`).
  3. corrupt (`version: 1\n\tBAD INDENT {{{\n`) → laut fehlschlagend.
  4. valid (1 Access `local`, 1 Target `first`, docker) → lädt seinen Target.
- Stabilität der Familie/Semantik weitergeerbt: `TestLoadConfigFailsLoudOnUnparseableConfig`,
  `TestLoadConfigMissingUnderPopulatedRootFailsLoud`, `TestLoadConfigMissingUnderEmptyRootSucceeds`,
  `TestLoadConfigValidStillLoads`, `TestDirExistsAndHasBaseharborState`.

**CI-Aufnahme (Owner-Direktive 2026-11-07):** beide Tests laufen im Package `internal/deployment` und
werden von der Go-test-gruppe in `.github/workflows/ci.yml` (Zeile 124, `go test ./contracts/...
./internal/... ./spec/...`) ausgeführt; Gruppe feuert per `pull_request` auf
`develop`/`main`/`lane-*` inkl. `converted_to_draft` (ci.yml Zeilen 12-18). Der neue Test ist damit
durhafte CI-Evidence; `.github/**` **unberührt**.

## 4. build / vet / gofmt (lokal)

```
gofmt -l internal/deployment/target.go internal/deployment/config_fail_loud_test.go   # (leer = sauber)
go vet ./internal/deployment/...     # clean
go build -o baha ./cmd/baha          # exit 0
```

- `./internal/deployment/...` ok (30,5s)
- `./cmd/baha/` target + org-scope ok (31,6s)
- End-to-End-Manuellprobe mit eigenem Build (`fe00c7f1`):
  - existierende leere `config.yaml` am XDG-Pfad ->
    `Error: BaseHarbor config root is configured but the config.yaml is empty: .../baseharbor/config.yaml`, exit=1.
  - abwesende `config.yaml` an leerem Root -> impliziter `local`-Target, exit=0.

## 5. Terminaler CI-Run (PR #1666, Run 43958812007)

Exact-Head-Candidate `fe00c7f1` auf PR #1666 (DRAFT, base `f590fbf0`):

- Run-ID: **43958812007** — status `completed`, conclusion `success`
- erstellt `2026-11-16T21:18:56Z`, abgeschlossen `2026-11-16T21:23:57Z` (≈5 min)
- https://github.com/mcpdev80/baseharbor/actions/runs/43958812007
- Branch head bestätigt: `git ls-remote origin lane-0428-094-config-fail` -> `fe00c7f1...`.

Kein roter Pflicht-Check.

## End-to-End-Verifikation (eigener Build, absoluter Pfad)

```
# existierende LEERE config am XDG-Pfad -> jetzt LAUT:
$ env HOME=$H XDG_CONFIG_HOME=$H/.config baha target list
Error: BaseHarbor config root is configured but the config.yaml is empty: $H/.config/baseharbor/config.yaml
exit=1

# ABWESENDE config an leerem Root -> weiterhin sauber (impliziter local):
$ env HOME=$H XDG_CONFIG_HOME=$H/.config-nope baha target list
# ... exit=0, implicit local
```

## Repo-Rule-Compliance

- Write-Set auf `internal/deployment/target.go` + `internal/deployment/config_fail_loud_test.go` — nur
  Produkt, kein `.github/**`.
- Kein Merge, kein `ready_for_review`, kein force-push, kein workflow_dispatch, kein subagent (§4.8).
- PR #1666 bleibt DRAFT; Push über Refspec, HEAD über `ls-remote` bestätigt.
- Build-Artefekte unter Scratch (`baha` in `.tmpb/`), nur die zwei Source-Dateien committet.
- Evidence lebt in baseharbor-plan, nirgends im Produkt-Repo.

## Branch-Provenanz

```
$ git rev-parse HEAD                 # fe00c7f180dc373d64a919e8aa74193a4db548bb
$ git log --oneline -2
fe00c7f1 fix(deployment): existing empty config.yaml fails loud (BF-05 r2)
5b0197a9 fix(deployment): fail loud on corrupt/missing base config (BF-05)
$ git ls-remote origin lane-0428-094-config-fail
fe00c7f180dc373d64a919e8aa74193a4db548bb refs/heads/lane-0428-094-config-fail
$ git merge-base --is-ancestor 14d8f17d HEAD && echo YES
YES
```

Base `14d8f17d` (develop / DSR3, Merge PR #1624) ist Ancestor; Lane enthält nur zwei eigene Commits
(`5b0197a9` + `fe00c7f1`), kein foreign candidate.

## Cleanliness

Scratch `baha` unter `.tmpb/` im Produkt-Repo; beide Scratch-Verzeichnisse `.gc/` (GOCACHE) und
`.tmpb/` (TMPDIR) nach Commit entfernt und per `git status --short` als sauber verifiziert. Keine
Container/Compose/Volumes gestartet (kein Docker/Podman-Testrequired). Kein fremder Arbeitsbaum
berührt.

## END

END_DONE mission-094-config-quiet-r2-luna.md: Korrektur implementiert (fail-laut-entscheidung,
`ErrConfigEmpty` + restringierter `LoadConfig`), 4-Fall-XDG-Regression am realen Auflösungsmpfad.
Build/vet/gofmt lokal clean, `internal/deployment` + `cmd/baha` green. Branch
`lane-0428-094-config-fail` = `fe00c7f1` (Base `14d8f17d`, Ancestor von develop), PR #1666 DRAFT,
base `f590fbf0`. Terminaler exact-head CI Run **43958812007: SUCCESS** (21:18→21:23 UTC, ≈5 min).
Evidence auf origin/main. Kein Merge, kein ready_for_review, kein force-push.
