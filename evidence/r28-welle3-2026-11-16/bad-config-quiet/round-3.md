# BF-05 — bad config quiet (0428-094), round 3 (Luna batch18 REQUEST CHANGES, Object 1)

- Mission: `/var/tmp/missions/mission-094-config-quiet-r3-luna2.md` (karte 0428-094, Korrektur-Runde)
- Akte: `evidence/r28-welle3-2026-11-16/batch18/act-luna-batch18.md` — Verdict Object 1: **REQUEST CHANGES**
- Rolle: Worker — Implementierung + Regression, keine Prüfung
- Basis der Lane: `lane-0428-094-config-fail` @ `fe00c7f18` (fix #1666, BF-05 r2)
- Ziel-Branche: `lane-0428-094-config-fail`, PR #1666 DRAFT (base `develop`)
- Build-Zeugnis: `go1.26.8`, `go build -o baha ./cmd/baha` exit 0

## STATUS: fertig — korrektur-push 4f2906c6 belegt, exact-head CI #43979087744 SUCCESS, END_READY

## 1. Rezept-Punkt-Punkt (Luna batch18, Verdict Object 1)

Batch18 beanstandete an `fe00c7f18`, dass der **URSPRUNGLICHE double-append-Fall** nicht end-to-end abgedeckt ist: `XDG_CONFIG_HOME` endet bereits in `/baseharbor`, also aufgelöst `ConfigPath()` `<root>/baseharbor/baseharbor/config.yaml` (verschachtelt, fehlt), die intendierte `config.yaml` liegt eine Ebene höher. Der bestehende `TestDirExistsAndHasBaseharborState` prüft nur die Prädikat-Helferfunktion, ruft nie `LoadConfig()` mit dieser XDG-Konstellung auf.

Konkrete Rezept-Anforderung:
1. `LoadConfig`-Integration: `XDG_CONFIG_HOME=<temp>/.config/baseharbor`, intendierte `config.yaml` auf DIESEM Root ablegen, verschachtelter aufgelöster Pfad **fehlt**, `errors.Is(err, ErrConfigMissing)` asserts.
2. Bestehende 4-Fall-Matrix + gültig-Assertion **behalten**.
3. Betroffenes deployment-package durch exact-head PR/draft-Go-Run ausführen, run-id/status in die Akte.

## 2. Fix — Test-only (kein Produktcode nötig)

Keine Produktänderung: die korrigierte Semantik ist in r2 bereits in `internal/deployment/target.go` implementiert (`LoadConfig()` → `ErrConfigMissing` über Signal 1, `config.yaml` eine Ebene über dem aufgelösten Pfad). Die Korrektur ergänzt die fehlende **end-to-end-Abdeckung**, die batch18 forderte.

`internal/deployment/config_fail_loud_test.go`, neuer Integrationstest `TestLoadConfigDoubleAppendResolvedPathMissingFailsLoud`:

- `XDG_CONFIG_HOME=<tmp>/.config/baseharbor`, intendierte `config.yaml` auf `<root>/baseharbor/config.yaml` (eine Ebene über dem aufgelösten Pfad) ablegen.
- Verschachtelter aufgelöster Pfad `<root>/baseharbor/baseharbor/config.yaml` bleibt abwesend.
- `LoadConfig()` → `errors.Is(err, ErrConfigMissing)` asserts (fail-laut, nicht impliziter Default).

Dadurch ruft die Matrix die echte `ConfigPath()`/`LoadConfig()`-Auflösung gegen die reproduzierte mismatch — die source deckt nun den end-to-end-Fall, den batch18 beanstandete.
Bestehende Tests unverändert weiter erhalten: `TestLoadConfigEndToEndXDGPath` (4-Fall-Matrix exists+empty/missing/corrupt/valid), `TestLoadConfigValidStillLoads`, `TestLoadConfigExistingEmptyFileFailsLoud` (empty + whitespace).

## 3. build / vet / gofmt (lokal)

```
gofmt -l internal/deployment/target.go internal/deployment/config_fail_loud_test.go   # (leer = sauber)
go vet ./internal/deployment/     # clean
go build -o baha ./cmd/baha          # exit 0
```

- `./internal/deployment/...` ok (15,0s)
- Einzelfalle verifiziert (lokal, -v):
  - `TestLoadConfigDoubleAppendResolvedPathMissingFailsLoud` PASS
  - `TestLoadConfigEndToEndXDGPath` PASS (4-Fall-Matrix)
  - `TestLoadConfigExistingEmptyFileFailsLoud` PASS (empty + whitespace)
- End-to-End-Manuellprobe mit eigenem Build (`4f2906c6`):
  - `XDG_CONFIG_HOME=<tmp>/.config/baseharbor`, intendierte `config.yaml` an Root, verschachtelter Pfad fehlt →
    `Error: BaseHarbor config root is configured but the config.yaml is missing: .../.config/baseharbor/baseharbor/config.yaml`, exit=1 (fail-laut).

## 4. Terminaler CI-Run (PR #1666, Run 43979087744)

Exact-Head-Candidate `4f2906c6` auf PR #1666 (DRAFT, base `develop`):

- Run-ID: **43979087744** — status `completed`, conclusion `success`
- erstellt `2026-11-16T23:25:02Z`, aktualisiert `2026-11-16T23:29:59Z` (≈5 min)
- https://github.com/mcpdev80/baseharbor/actions/runs/43979087744
- Branch head bestätigt: `git ls-remote origin lane-0428-094-config-fail` → `4f2906c6bf9f1c1e5c95f7b88e79c1aa5e110ecc`.

## End-to-End-Verifikation (eigener Build, absoluter Pfad — double-append)

```
# XDG_CONFIG_HOME endet bereits in /baseharbor -> verschachtelter aufgelöster Pfad fehlt -> laut:
$ env XDG_CONFIG_HOME=$H/.config/baseharbor baha target list
Error: BaseHarbor config root is configured but the config.yaml is missing: $H/.config/baseharbor/baseharbor/config.yaml
exit=1
```

## Repo-Rule-Compliance

- Write-Set auf `internal/deployment/config_fail_loud_test.go` — nur Produkt, kein `.github/**`.
- Kein Merge, kein `ready_for_review`, kein force-push, kein workflow_dispatch-Rerun-Sinnlosigkeit (ein Run genügt), kein subagent (§4.8).
- PR #1666 bleibt DRAFT; Push über Refspec, HEAD über `ls-remote` bestätigt.
- Build-Artefekte unter Scratch (`baha` in `.tmpb/`), nur die Testdatei committet.
- Evidence lebt in baseharbor-plan, nirgends im Produkt-Repo.

## Branch-Provenanz

```
$ git rev-parse HEAD                 # 4f2906c6bf9f1c1e5c95f7b88e79c1aa5e110ecc
$ git log --oneline -3
4f2906c6 fix(deployment): end-to-end double-append missing config fails loud (BF-05 r3)
fe00c7f1 fix(deployment): existing empty config.yaml fails loud (BF-05 r2)
5b0197a9 fix(deployment): fail loud on corrupt/missing base config (BF-05)
$ git ls-remote origin lane-0428-094-config-fail
4f2906c6bf9f1c1e5c95f7b88e79c1aa5e110ecc refs/heads/lane-0428-094-config-fail
```

Lane enthält drei eigene Commits (`5b0197a9` + `fe00c7f1` + `4f2906c6`), kein foreign candidate.

## Cleanliness

Scratch `baha` unter `.tmpb/` im Produkt-Repo; beide Scratch-Verzeichnisse `.gc/` (GOCACHE) und `.tmpb/` (TMPDIR) nach Commit entfernt und per `git status --short` als sauber verifiziert. Keine Container/Compose/Volumes gestartet ( kein Docker/Podman-Testrequired). Kein fremder Arbeitsbaum berührt.

## END

END_DONE mission-094-config-quiet-r3-luna2.md: batch18-REQUEST-CHANGES Object 1 korrektiert — end-to-end double-append missing config abgedeckt, `LoadConfig` läuft echte XDG-Auflösung, `ErrConfigMissing` statt stillschiegendem Default. 4-Fall-Matrix + gültig-Assertion erhalten. Build/vet/gofmt lokal clean, `internal/deployment` green. Branch
`lane-0428-094-config-fail` = `4f2906c6` (Base `fe00c7f18`, base develop), PR #1666 DRAFT. Terminaler exact-head CI Run **43979087744: SUCCESS** (23:25→23:29 UTC, ≈5 min). Evidence round-3.md auf origin/main. Kein Merge, kein ready_for_review, kein force-push.
