# t-20261018-r27-version-view · Runde 2 · Lane w229

Karte: t-20261018-r27-version-view (v0.4.27, Welle 5). Mission:
`coordinator/missions/w229-version-view-r2.txt`. Coord: 841e7734.
Repo: mcpdev80/baseharbor · Zweig `work/r27-version-view` → PR #1403 gegen `develop`.
Vorlage: REJECT-Akte `act-1403b.md` (Luna) — Blocker war die nicht-kausale
Rotgegenprobe in `TestStagesViewMutationAgainstSeparationLine`.

## PLAN

1. Mission + Akten (act-1403b.md, round-1.md) lesen; Board-Datei und diesen PLAN anlegen
2. Basis-Attest: ls-remote develop/candidate, Ancestor-Test, eigene Commits belegen
3. Gegenprobe umbauen: echter Produkt-Mutant über Schnittstelle/Parameter (release.go), keine Mapper-Kopie im Testfile
4. Mutantenzeugnis A: Dimension-Mutant (release.go:13) lokal, rückgängig — Zelle failt
5. Mutantenzeugnis B: Kind-Mutant (release.go:190) lokal, rückgängig — Zelle failt
6. round-1.md Mechanismus-Beschreibung berichtigen (Luna-Befund)
7. Tore: gofmt/vet/build, race count=10 targetiert
8. Push auf demselben Zweig (ein PR), ls-remote echt==head, Hosted-Lauf bis TERMINAL beobachten
9. Akte auf baseharbor-plan origin/main veröffentlichen (ls-tree-Zeuge), END an 841e7734
10. AGENTS-Compliance-Selfcheck + Arbeitsplatten-Cleanup

Status: alle Schritte ausgeführt; END-LINE am Dateiende.

## Basis-Attest

- Cut-Punkt dieser Lane: exakt der bisherige Kandidatenkopf `57cf82a0cfc334d510f2b727d7d8bd46e6dfb46a`
  (`git worktree add … 57cf82a0…`; kein Schnitt von einem anderen PR-Kopf).
- Vor dem Push: `origin/develop` = `7c393b0dd842e7fca23d4f431c6c2f69c3f197b1` (develop hat sich seit
  Runde 1 von `ea656d1f` nach vorne bewegt). Der Remote-Zweig war zwischenzeitlich per
  Base-Refresh-Merge `9a14fa80` (anderer Lane, Maintainer-Fluss) auf develop aktualisiert worden;
  `57cf82a0` ist Vorfahre von `9a14fa80` (Prüfung rc=0), also kein Schnittverlust. Diese Lane hat
  ihren Commit `ef9464ef` auf `9a14fa80` aufgesetzt und den Base auf den aktuellen develop
  `7c393b0d` aufgefrischt (Merge `65ed48d6`), wie von AGENTS verlangt (ferne Änderungen vor dem
  Push integrieren).
- Ancestor-Test am Endkopf: `git merge-base --is-ancestor origin/develop HEAD` → rc=0
  (`7c393b0d` ist Vorfahre von `65ed48d6`).
- `git log --oneline origin/develop..HEAD --no-merges --first-parent` (wörtlich, nur eigene Commits):

```
ef9464ef test(r27 version-view): bind the separation regression causally to the shipped mapper
57cf82a0 docs(r27 version-view): regenerate human EN/DE command index from the shipped command tree
df3ded33 feat(r27 version-view): readable wanted/applied/observed version view as separated cells
```

- Write-Set gegen develop (`git diff --name-only 7c393b0d HEAD`): exakt die 19 Dateien von Runde 1,
  keine neuen Dateien, kein `.github/**`, keine Fremd-Lane-Datei. Der PR-Files-API-Zähler
  (`changed_files = 19`) deckt sich damit.

## (1) Gegenprobe jetzt kausal — Mechanismus

- Vergleich Base: `cmd/baha/app_version_view_test.go` existiert an develop `7c393b0d` nicht
  (`git log --oneline -2 -- cmd/baha/app_version_view_test.go` am Base-Checkout: leer) — der
  ganze Test wohnt ausschließlich auf diesem Kandidatenzweig; die Gegenprobe vergleicht
  develop gegen den Kandidaten, nicht zwei Kandidaten.

- Produktseite (`internal/machinereadmodels/release.go`): die Dreier-Zuordnung des ausgelieferten
  Mappers wohnt jetzt in einer produktsichtigen, dokumentierten Tabelle
  `releaseViewStageKinds` (Zeile 13), ist über `ReleaseViewStageKinds()` (Zeile 17-23)
  ablesbar und wird von `ReleaseViewFromRecord` (Zeile 116-118) an die neue, explizite
  Parameter-Form `ReleaseViewFromRecordWithStageKinds(record, kinds)` (Zeile 126) weitergegeben.
  Die Parameter-Form IST der ausgelieferte Mapping-Code (Identität, kein Alias: die
  Gegenprobe ruft dieselbe Funktion mit genau der ausgelieferten Tabelle auf).
- Testseite (`cmd/baha/app_version_view_test.go`): die zweite Mapper-Kopie `referenceCell` ist
  gelöscht (überprift: `grep -n "referenceCell" cmd/baha/*.go` → keine Treffer).
  `TestStagesViewMutationAgainstSeparationLine` (Zeile 311) fährt beide Zweige durch
  `ReleaseViewFromRecordWithStageKinds`:
  - GRÜN-Gegenprobe: `shipped := ReleaseViewFromRecordWithStageKinds(record, shippedReleaseViewStageKinds())`
    — Kopie der ausgelieferten Tabelle über das Produkt (`ReleaseViewStageKinds()`), roter Zweig
    bleibt grün.
  - ROT-Mutant 1 (Dimension, recipe 1b): `mutantKinds[2] = mutantKinds[1]` — dieselbe
    Produktfunktion, derselbe Record, nur die übergebene Zuordnungstabelle vertauscht;
    genau eine Verletzung, `t.Fatal` bei 0 Verletzungen.
  - ROT-Mutant 2 (Provenienz/Kind-Klasse, recipe 1a-Hälfte): die Zelle trägt eine fremde
    Dimensions-Aufschrift; die Linie prüft Kind gegen die Soll-Dimension, damit der in der
    Akte gemessene blinde Fleck (release.go Kind-Loop) nicht nochmal durchrutscht.
- Kausalität: jede Mutation an `release.go` (Tabelle, Parameter-Durchgabe oder Zellen-Kind)
  färbt direkt auf die Zelle durch — nachgemessen in den beiden Zeugnissen unten.

## Mutantenzeugnis A — echter Produkt-Mutant Dimension (release.go:13, lokal, rückgängig)

Mutation: `var releaseViewStageKinds = [3]string{referenceIntended, referenceApplied, referenceObserved}`
→ `…, referenceApplied}` (observed-Slot liest die applied-Dimension), Zelle unverändert, danach
Restore (`git diff` leer auf Zeile 13, Tests wieder grün). Auszug, wörtlich:

```
--- FAIL: TestReleaseViewExampleShapeKeepsEveryCellReadable (0.00s)
    release_test.go:47: missing dimensions must read UNCLEAR: {Wanted:0x3b62e0ec8200 Applied:0x3b62e0ec8240 Observed:0x3b62e0ec8280}
FAIL	github.com/mcpdev80/baseharbor/internal/machinereadmodels	0.009s
--- FAIL: TestVersionViewThreeCellsAlwaysSeparated (0.00s)
    app_version_view_test.go:66: cell 2 reads dimension "applied", want "observed"
--- FAIL: TestVersionViewMissingDimensionIsUnclear (0.00s)
    app_version_view_test.go:89: unrecorded dimension must be marked missing-data
--- FAIL: TestVersionViewDimensionIsolation (0.00s)
    app_version_view_test.go:123: observed must not be copied from applied, got "applied-only"
--- FAIL: TestRenderAppVersionHumanUnclearCells (0.00s)
    app_version_view_test.go:209: human view must contain "UNCLEAR", got:
--- FAIL: TestAppVersionCommandCallable (0.00s)
    app_version_view_test.go:285: the cleared observed cell must read UNCLEAR, got "sha256:applied-only"
--- FAIL: TestStagesViewMutationAgainstSeparationLine (0.00s)
    app_version_view_test.go:338: the shipped mapper must satisfy the separation line, got [observed cell does not read the observed dimension]
--- FAIL: TestAppVersionsCommandCallable (0.00s)
    app_version_view_test.go:439: an unrecorded observation must read UNCLEAR, got "sha256:applied-only"
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.026s
```

Die Gegenprobenzelle selbst failt am Produkt-Mutanten (Zeile 338) — exakt der Nachweis,
den die Akte forderte; zusätzlich failen 7 echte Behavioral-Zellen mit.

## Mutantenzeugnis B — echter Produkt-Mutant Kind (release.go:190, lokal, rückgängig)

Mutation: `cell := &ViewStageCell{Kind: kind}` → `cell := &ViewStageCell{Kind: referenceApplied}`
(stillschweigende Dimensions-Aufschrift in der ausgelieferten Zellen-Funktion), danach Restore
(Zeile 190 wieder `Kind: kind`, Tests wieder grün). Auszug, wörtlich:

```
ok  	github.com/mcpdev80/baseharbor/internal/machinereadmodels	0.004s
--- FAIL: TestVersionViewThreeCellsAlwaysSeparated (0.00s)
    app_version_view_test.go:66: cell 0 reads dimension "applied", want "intended"
--- FAIL: TestStagesViewMutationAgainstSeparationLine (0.00s)
    app_version_view_test.go:338: the shipped mapper must satisfy the separation line, got [wanted cell does not read the intended dimension observed cell does not read the observed dimension]
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.026s
```

Beide Zeugnisse zeigen: die veröffentlichte Zelle hängt jetzt kausal von
`internal/machinereadmodels/release.go` ab; kein Testfile-Mapper mehr beteiligt.

## (2) round-1.md berichtigt

`evidence/r27-welle5-2026-11-06/version-view/round-1.md`, Abschnitt "mutante": die
faktisch falsche Mechanismus-Beschreibung ("gegen denselben Fixture-Felderzugriff wie der
ausgelieferte Mapper") ist durch die Berichtigung mit Luna-Verweis und dem runde-2-Mechanismus
ersetzt. Diff nur diese Datei in diesem Commit.

## (3) PR und Lauf

- PR #1403 bleibt EIN Antrag auf `work/r27-version-view`; kein zweiter PR, kein zweiter Zweig
  (`git branch --list` in dieser Lane: nur der Namenszweig; ls-remote-Zeugen unten). Ein bei der
  Worktree-Erzeugung kurzlebiger lokaler Helper-Branch `work/r27-version-view-checkout` (nur
  lokal, nie gepusht; `git ls-remote origin 'refs/heads/work/*version-view*'` zeigt nur den
  einen Kandidatenzweig) wurde vor dem END gelöscht.
- Hosted-Lauf am FINAL-KOPF, selbst bis TERMINAL beobachtet (Poll 1..11, kein rerun,
  kein workflow_dispatch):

```
$ gh api repos/mcpdev80/baseharbor/actions/runs/42211122594 --jq '{status,conclusion,head_sha,event,run_started_at,updated_at,html_url}'
{"conclusion":"success","event":"pull_request","head_sha":"65ed48d60f779621ce32c4e5b1546f3e10f9af1d","html_url":"https://github.com/mcpdev80/baseharbor/actions/runs/42211122594","run_started_at":"2026-11-06T11:33:22Z","status":"completed","updated_at":"2026-11-06T11:41:45Z"}
```

  Run 42211122594 = "CI · PR #1403", `head_sha` exakt der Endkopf `65ed48d6…`,
  `status=completed`, `conclusion=success` → TERMINAL SUCCESS. Jobs: 19 success, 10 skipped,
  0 failure, 0 cancelled (`gh run view … --json jobs` Gruppierung, wörtlich
  `{"skipped":10,"success":19}`; Fail/Cancel-Liste leer `[]`).

- Kopf nach Push: `65ed48d60f779621ce32c4e5b1546f3e10f9af1d`.

```
$ git ls-remote origin refs/heads/work/r27-version-view refs/heads/develop refs/pull/1403/head
7c393b0dd842e7fca23d4f431c6c2f69c3f197b1	refs/heads/develop
65ed48d60f779621ce32c4e5b1546f3e10f9af1d	refs/heads/work/r27-version-view
65ed48d60f779621ce32c4e5b1546f3e10f9af1d	refs/pull/1403/head
```

`ls-remote` echt == head: `refs/heads/work/r27-version-view` == `refs/pull/1403/head` ==
`65ed48d60f779621ce32c4e5b1546f3e10f9af1d` == lokaler Kopf. Der PR zeigt auf denselben einen
Zweig (ein Antrag).

## Lokale Tore am Kandidaten

- `gofmt -l cmd internal` leer · `go vet ./cmd/baha/ ./internal/machinereadmodels/` rc=0 (nach
  Restore beider Mutanten) · `go build ./...` rc=0.
- `go test -race -count=10 ./cmd/baha -run 'TestVersionView|TestAppVersion|TestRenderAppVersion|
  TestStagesViewMutation|TestSplitImageReference'` → ok 2.165s;
  `go test -race -count=10 ./internal/machinereadmodels -run TestReleaseView` → ok 1.021s.
- Wizard-Registration-Zellmenge (die der Doku-Drift in Runde 1 gerissen hat): ok 0.071s.
- Arbeitsplatte: Scratch unter `/home/marcel/dev/baseharbor-ecosystem/workers/w229-wt`,
  Caches `/dev/shm/w229-*` und `/tmp/opencode/w229*` (Mission: caches /tmp/opencode/w229*;
  /tmp hatte zur Lane-Zeit ein per-user-Quota-Erschöpfungsfenster, deshalb der
  Build-Cache-Ausweichort /dev/shm/w229-gocache; wird am Ende gelöscht).
- Kein Container/compose/VM gestartet (Mission nennt keinen VM-Smoke-Test);
  keine `.github/**`-Änderung; kein rerun/workflow_dispatch; keine Subagenten.

## AGENTS-Compliance-Selfcheck

- Read before acting: workers/AGENTS.md + baseharbor-plan/AGENTS.md + task note + both akten gelesen.
- Product repo schreibt nur auf dem einen Karten-Zweig; kein root-checkout-Commit
  (der Workers-Checkout wurde auf `--detach` gestellt, alle Commits im Lane-Worktree).
- Kein `.github/**`, kein rerun/workflow_dispatch, keine Subagenten, kein root-Scratch im
  Oekosystem-Root; Scratch/Caches unter `workers/w229-wt` + `/dev/shm/w229-*` + `/tmp/opencode/w229*`.
- Keine Markdown-Checkboxes in dieser Akte und keinem Akten-Theater im Produktrepo:
  `grep -c '^[[:space:]]*- \['` in round-2.md und round-1.md = 0.
- CI-Discipline: ein Push, ein eigener Hosted-Lauf am Endkopf, bis TERMINAL selbst beobachtet;
  lokale Vorpruefung (build/vet/gofmt/race count=10/wizard-Zellmenge/doku-audit/readability)
  vor dem Push.
- Name-only disjunkt: Write-Set == die 19 Dateien von Runde 1, nur `release.go` und
  `app_version_view_test.go` in dieser Runde veraendert (`git diff 9a14fa80 HEAD --name-only`).

## Push-Zeuge (origin/main)

Vor dem Push, wörtlich:

```
$ git fetch origin main && git rev-parse HEAD && git merge-base --is-ancestor HEAD origin/main && echo HEAD-IN-MAIN && git ls-tree -r --name-only origin/main | grep version-view
64aaa6a evidence(r27 version-view round 2): terminal hosted run witness, compliance selfcheck, END line
90852855d57d69b77403be0084fbda86fa2f462e
HEAD-IN-MAIN
evidence/coord-memory/missions/w226-version-view.txt
evidence/r27-welle5-2026-11-06/version-view/act-1403b.md
evidence/r27-welle5-2026-11-06/version-view/round-1.md
evidence/r27-welle5-2026-11-06/version-view/round-2.md
tasks/t-20261018-r27-version-view.md
```

Die Akten-Commits dieser Lane (`d90620f`, gefolgt von den Folgeschuessen, am Ende linear
auf `origin/main` = `90852855d57d…` rebasiert als `64aaa6a`) sind auf origin/main verifiziert;
round-1.md und round-2.md liegen dort.

## END

END_DONE w229-version-view-r2: head=65ed48d60f gegenprobe-kausal=JA+2 mutantenbelege lauf=42211122594 TERMINAL-SUCCESS lsremote=65ed48d60f | Gegenprobe laeuft jetzt durch den ausgelieferten Mapper (releaseViewStageKinds-Tabelle + ReleaseViewFromRecordWithStageKinds), Testfile-Kopie referenceCell geloescht; Dimension- (release.go:13) und Kind-Mutant (release.go:190) failen die Zelle je lokal und sind rueckgaengig; round-1.md berichtigt; PR #1403 bleibt EIN Antrag, ein Push, ein terminal gruener Hosted-Lauf am Endkopf.
