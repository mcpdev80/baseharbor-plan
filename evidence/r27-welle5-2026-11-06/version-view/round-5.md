# t-20261018-r27-version-view · Runde 5 · Lane w238 (Konflikt-Beseitigung)


Karte: t-20261018-r27-version-view (v0.4.27, Welle 5) — nur Konfliktloesung, KEINE
Funktionsaenderung. Mission: `coordinator/missions/w238-vv-conflict-fix.txt`.
Coord: 841e7734. Repo: mcpdev80/baseharbor · Zweig `work/r27-version-view` → PR #1403 gegen `develop`.

## PLAN

1. Mission + Akten (round-1/2, act-1403c) lesen; Board-Datei und diesen PLAN anlegen
2. Zustand: ls-remote develop/candidate, PR mergeable, Autor von 9e76da5a belegen (Drift-Zeugnis)
3. Lane-Worktree einrichten (kein Root-Checkout; Caches unter workers/w238-cache, /tmp war quota-bedroht)
4. Merge origin/develop bc8670c1 in den Kandidaten; machine_coverage.go als Union loesen
5. Nachweis: vv-Baum inhaltlich == 65ed48d6 (Diff leer), kein Rueckbau, keine Fremd-Eintraege
6. Tore lokal: go build, go vet (voll), gofmt, targetierte vv-/coverage-/doc-Tests
7. Ahnenschaft + Log-Liste (nur eigene Commits), Push auf denselben Zweig, ls-remote vor/nach
8. Hosted-Run 42216124051 bis TERMINAL beobachten (nicht feuern; bei Fail QUESTION an Coord)
9. Akte round-5.md auf baseharbor-plan origin/main veröffentlichen (ls-tree-Zeuge)
10. AGENTS-Compliance-Selfcheck + Platten-Cleanup, END an 841e7734

Status: alle Schritte ausgefuehrt; END-LINE am Dateiende.

## Drift-Zeugnis (Pflichtteil)

- Vor Lane-Beginn: `git ls-remote` → `work/r27-version-view` = `9e76da5adafaa1670365ff811d8b3a8679d16146`,
  `develop` = `bc8670c1dc6a2d7b5bf602ae7450f2e778a6f97a` (Zeuge `/tmp/opencode/w238-lsremote-before.txt`).
- PR #1403 damals: `mergeable=CONFLICTING` in `cmd/baha/machine_coverage.go` (gh pr view, 2026-11-06).
- Der Kopf `9e76da5a` ist ein Merge von `origin/develop` (Anc `5f8b2985`) mit Autor
  `Worker w224 <w224@baseharbor.local>` — w224 ist eine GELOESCHTE Lane; sie hat nach dem
  AKZEPTIERT-Urteil ueber Kopf `65ed48d60f7` fremd auf den Zweig gezogen. Zeuge:
  `git log --format='%h %an <%ae> %s' -3 9e76da5a` →
  `9e76da5a Worker w224 <w224@baseharbor.local> Merge remote-tracking branch 'origin/develop' into work/r27-version-view`.
- Inhaltlich war dieser Fremd-Merge fuer den vv-Baum unschaedlich: `git diff 65ed48d60f7 9e76da5a`
  betraf nur develop-Dateien (secure-profile-export, orgconfig OCI) — kein vv-Rueckbau.
- Regelkonform gemeldet statt selbst geheilt wurde hier nicht noetig: die Mission selbst
  beauftragt die Konfliktloesung auf diesem Zweig. SEIT dieser Lane ist der Zweigkopf wieder
  diese Lane (`f89cf7a5`); ls-remote nach dem Push unten. Jeder WEITERE fremde Push waere eine
  QUESTION an den Coord (Hinweis Sicherheit, Mission Zeile 11-12).

## Loesung

- Basis dieser Lane (Attest): der bestehende Kandidatenkopf `9e76da5a` (kein Schnitt von einem
  anderen PR-Kopf; Cut von der Remote-Spitze desselben Zweigs). Ahnen in `f89cf7a5`:
  - `git merge-base --is-ancestor 65ed48d60f7 HEAD` → rc=0 (angenommener Kopf erhalten)
  - `git merge-base --is-ancestor bc8670c1 HEAD` → rc=0 (develop eingearbeitet)
  - `git merge-base --is-ancestor 9e76da5a HEAD` → rc=0 (kein Content-Verlust des Vorgaengers)
- Einziger Konflikt: `cmd/baha/machine_coverage.go`, Map `cliPresentationCommands`.
  Loesung = Union beider Seiten in der Eintrag-Reihenfolge des develop-Stils, vv-Eintrag
  `baha app version` erhalten, develop-Eintrag `baha app secure-profile export` uebernommen.
  Keine Duplikate, keine fehlenden Schluessel (go build + `TestMachineCoverageCIRealTreeAndJSONClassification`
  plus doc-Tests gruen).
- Einarbeitung ohne Rueckbau — Nachweis:
  - `git diff 65ed48d60f7 HEAD -- cmd/baha/app_version_view.go cmd/baha/app_version_view_test.go cmd/baha/app_versions_command.go internal/machinereadmodels/ contracts/ cmd/baha/mcp_tools.go` → 0 Zeilen
    (vv-Baum inhaltlich identisch zum akzeptierten Kopf 65ed48d60f7).
  - Gegen `origin/develop bc8670c1` zeigt der PR-Diff exakt die 19 vv-Dateien der Runden 1-4
    (`git diff origin/develop HEAD --stat`: 19 files, 1459 insertions), keine `.github/**`, keine
    Fremd-Lane-Datei.
  - `git log --oneline --no-merges --first-parent origin/develop..HEAD` listet NUR eigene Commits:
    `ef9464ef`, `57cf82a0`, `df3ded33` (Runden 1-2 der vv-Lane) — kein fremder Candidate im Schlepptau.

## Tore (lokal)

- `go build ./...` → OK; `go vet ./...` → OK (voll, keine Ausgabe); `gofmt -l cmd internal contracts` → leer.
- Targetiert vv/unit gruen: `TestVersionViewThreeCellsAlwaysSeparated`,
  `TestVersionViewMissingDimensionIsUnclear`, `TestVersionViewDimensionIsolation`,
  `TestVersionViewJSONShapeSeparatesCells`, `TestRenderAppVersionHumanUnclearCells`,
  `TestAppVersionCommandCallable`, `TestAppVersionsCommandCallable`,
  `TestNodeMachineCoverageIsSemantic`, `TestMachineCoverageCIRealTreeAndJSONClassification`,
  humane/machine-documentation tests, `./internal/machinereadmodels`, `./internal/machine`,
  `./internal/capability` → alle ok.
- Randbefund (NICHT von dieser Lane verursacht): `TestRetainedTempoVersionChangeRequiresConcreteCurrentConsent`
  ist in diesem checkout-Umfeld flaky (TMPDIR-/Worktree-Abhaengigkeit); er failt auch am nackten
  develop-Worktree mit Build-Fehler unter /tmp-Quota und besteht im zweiten Anlauf im Lane-Tree.
  Kein vv-Bezug, keine vv-Datei involvement — hier als STATE notiert.

## Hosted-Lauf

- Push: `9e76da5a..f89cf7a5 refs/heads/work/r27-version-view` (fast-forward auf demselben Zweig,
  kein zweiter PR, kein neuer Branch).
  - ls-remote VOR dem Push: `/tmp/opencode/w238-lsremote-prepush.txt` → `9e76da5a…`
  - ls-remote NACH dem Push: `/tmp/opencode/w238-lsremote-postpush.txt` → `f89cf7a5e6ece67c494422c156c4c160f4af9db4`
- PR #1403 danach: `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN` (develop ist inzwischen auf
  `46ea6c73` weitergewandert — irrelevant, Ahn bc8670c1 reicht laut Mission).
- Lauf-id: `42216124051` (CI · PR #1403) am exakten Kopf `f89cf7a5` — STATUS: **completed / success**,
  terminal; 21 jobs success, 8 skipped (HA/Release-Gates triggern hier nicht), 0 failed.
  KEIN rerun, KEIN workflow_dispatch durch diese Lane (Coord-Hand).

## Compose-/Container-Zeuge (Owner-Hygiene)

Diese Lane hat keinen Container und kein compose-Projekt gestartet und keine VM angesprochen
(Mission nennt keinen VM-Smoke-Test). Nichts zum herunterfahren; ps-Zeuge: `ps -eo pid,comm | grep -c 'docker\|podman'` zur Kontrolle:
0 Lane-eigene Prozesse; nichts zum herunterfahren. Caches/Worktree:
`/home/marcel/dev/baseharbor-ecosystem/workers/w238-cache/{wt,gocache,gopath,tmp}` — /tmp war mit
82 % Fuellung quota-bedroht (`compile: writing output: disk quota exceeded`), daher Caches unter
workers/w238-cache statt /tmp/opencode/w238*; Mission-GATES erlauben explizit "caches" als Lane-Pfad
unter workers/. Root-Checkout wurde nicht angefasst (nur `git ls-remote`/`gh` von dort). Der
temporaere develop-Vergleichs-Worktree `w238-devchk` ist entfernt.

## Base-Zeuge (wortliche Ausgabe, direkt vor dem Evidence-Push)

```
$ git ls-remote origin refs/heads/work/r27-version-view
f89cf7a5e6ece67c494422c156c4c160f4af9db4	refs/heads/work/r27-version-view
```

## Selbstcheck

- AGENTS: Beweislage (ls-remote vor/nach, Ahnenschaft, Log-Liste nur eigene Commits) komplett.
- Kein Pfad in diesem Repo ausserhalb der Akte angelegt; kein Produktrepo-Checkout beschmutzt.

## END

END_DONE w238-vv-conflict-fix: head=f89cf7a5e6 conflict-frei=JA lauf=42216124051 SUCCESS | machine_coverage.go Union-geloest (vv- + secure-profile-Eintrag), vv-Baum == 65ed48d6 (Diff 0), develop bc8670c1 Ahn, PR #1403 MERGEABLE/CLEAN, Drift-Zeugnis 9e76da5a Autor w224-ghost in Akte.
