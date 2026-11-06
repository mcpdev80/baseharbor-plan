# t-20261018-r27-version-view · Runde 1 · Lane w226

Karte: t-20261018-r27-version-view (v0.4.27, Welle 5). Mission:
`coordinator/missions/w226-version-view.txt`. Sitzung: 841e7734.
Repo: mcpdev80/baseharbor · Zweig `work/r27-version-view` → PR #1403 gegen `develop`.

## PLAN

- Karte + Vorgänger-Schnittstellen aus origin/develop lesen (stage_versions.go, Read-Model-artifacts.go)
- Board-Datei + Evidenz-PLAN mit Basis-Attest ea656d1f anlegen
- Red-first: failinge Tests für getrennte wanted/applied/observed-Zellen + UNCLEAR-Zustand
- Implementierung cmd/baha/app_version_view.go + internal/machinereadmodels/release.go (read-only, verbraucht die merged stage versions)
- Echter Mutationstest gegen die Trennlinie (Spalten mischen ⇒ ROT)
- Tore lokal: gofmt, vet, build, race ×20
- Branch pushen, PR gegen develop, Ancestry + eigene Commits belegen
- PR selbst draft→ready (gh pr ready) + push; Hosted-Run bis TERMINAL beobachten (kein rerun/dispatch — Coordinator-Pflicht)
- Evidenz nach baseharbor-plan origin/main veröffentlichen (ls-tree-Zeuge), END an 841e7734

## Basis-Attest

- `git ls-remote origin refs/heads/develop` → `ea656d1fcfce9ee14145a8dfaffb9e993fd29497 refs/heads/develop`
- Branch-Punkt: exakt `ea656d1f` (Merge PR #1395, work/r27-registry-access).
- Ancestry-Beweis: `git merge-base --is-ancestor ea656d1f HEAD` → rc=0.
- Eigene Commits auf der Basis (`git log --oneline ea656d1f..HEAD`), Liste vollständig:
  - `df3ded33` feat(r27 version-view): readable wanted/applied/observed version view as separated cells
  - `57cf82a0` docs(r27 version-view): regenerate human EN/DE command index from the shipped command tree
- Head: `57cf82a0cfc334d510f2b727d7d8bd46e6dfb46a`; `git ls-remote origin refs/heads/work/r27-version-view` == Head (verifiziert).

## Erzeugnis ↔ Lieferung

- **getrennt (3 Spalten Zellen):** `ViewStages{Wanted,Applied,Observed}` in
  `internal/machinereadmodels/release.go`, 1:1 gemappt aus den drei
  `deployment.ReferenceDimension`-Dimensionen des persisted Records
  (`ReleaseViewFromRecord`). Das Struct-Typ selbst ist die Trennlinie.
  Zeuge-Tests: `TestVersionViewThreeCellsAlwaysSeparated`
  (`cmd/baha/app_version_view_test.go:48`), `TestVersionViewDimensionIsolation`,
  `TestVersionViewJSONShapeSeparatesCells` (eigene JSON-Keys wanted/applied/observed),
  `TestAppVersionCommandCallable` (:217), `TestAppVersionsCommandCallable` (:353).
- **unklar (UNCLEAR-Zelle):** `machinereadmodels.UnclearValue` =
  `"UNCLEAR (no version recorded in this dimension)"` + `MissingData`-Flag;
  nie ein leeres Feld (empty-render-Guard in allen Zellen).
  Zeugen: `TestVersionViewMissingDimensionIsUnclear` (:75),
  `TestRenderAppVersionHumanUnclearCells` (:183), und der Command-Test wischt
  die persistierte observed-Dimension via `deployment.ClearReference` und
  verlangt danach die UNCLEAR-Zelle (`TestAppVersionsCommandCallable`).
- **mutante (echt rot + Gegenprobe):** `TestStagesViewMutationAgainstSeparationLine`
  (:306) baut den echten Spaltenmisch-Mutanten (observed liest die
  applied-Dimension) gegen denselben Fixture-Felderzugriff wie der ausgelieferte
  Mapper; der Mutant verletzt genau eine Zelle (ROT erzwungen, `t.Fatal` bei
  0 Verletzungen), die ehrliche ausgelieferte Map-Funktion ist die
  Gegenprobe auf exakt demselben Fixture.
- **redfirst (belegt):** Die Dateien `cmd/baha/app_version_view.go`,
  `cmd/baha/app_versions_command.go`, `internal/machinereadmodels/release.go(+_test.go)`
  existieren auf origin/develop nicht (`git ls-tree -r origin/develop` → rc=1);
  der_callable_ Command-Test (`runWithIO … "app versions"` →
  "app versions must be callable") und der Mutant-Test sind am
  unveränderten develop notwedwendig rot (Kommando fehlt / Trennlinie fehlt),
  am Kandidaten grün. Erst Tests, dann Implementation.
- **lauf:** `42194394030` "CI · PR #1403" → `completed success` am head
  `57cf82a0` (TERMINAL, alle Nicht-Skip-Jobs success). Vorher: 42193416728
  (draft, trivial success), 42193475439 (wizard-registration-tests rot →
  durch Doku-Regenerations-Commit `57cf82a0` behoben, Run superseded/cancelled).
- **lsremote:** == head `57cf82a0cfc334d510f2b727d7d8bd46e6dfb46a` (oben belegt).

## Lokale Tore am Kandidaten

- `go build ./...` rc=0 · `go vet` rc=0 · `gofmt -l` leer.
- `race -count=20` über alle version-view Tests (9 in `cmd/baha` + 1 read-model): PASS.
- Vollsuite `cmd/baha`-binär: 89 failinge Tests; identical zur pristine
  Baseline `ea656d1f` (comm-Diff: 0 NEW / 0 GONE) ⇒ alle vorbestehend,
  keiner von diesem Lane verursacht. Ebenso reproduziert
  `internal/machinehttp TestRound3BoundedRetentionAndNoPayloads` (240s-Hang)
  identisch am pristine Baseline-Checkout — baseline-preexisting (lokal am
  Host), am hosted run success.
- `scripts/documentation-audit.sh` PASS (EN/DE integrity),
  `scripts/source-readability-audit.sh` PASS.
- Golden-fixtures + Doku regeneriert mit `scripts/tools/machine-control-fixtures`
  und `scripts/tools/machine-read-models` (+schema) und
  `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run TestMachineDocumentation…`;
  Kommando-Index-Doku analog (Commit `57cf82a0`), damit
  `TestHumanCommandIndexTracksExactCommandMetadata` grün bleibt.

## Scope-Hygiene

- Keine `.github/**`-Änderungen. Kein workflow_dispatch, kein rerun (Coordinator-Pflicht
  laut Owner-Auflösung). Lane-Aktionen: push + `gh pr ready 1403`.
- Keine Konfliktschreiber: `app_context.go`, `stage_versions.go`, `app_broker.go`,
  registry-transfer-Dateien unangetastet (konsumiert nur die merged
  reference dimensions über die public read API `LoadDeploymentRecord`/`ClearReference` in Tests).

## PR-Zustand

- https://github.com/mcpdev80/baseharbor/pull/1403 — OPEN, ready (draft→ready selbst),
  base develop `ea656d1f` (unverändert), head `57cf82a0`.

## Koordination

Letzte Posts an 841e7734 (wörtliche Ausgaben):

```
$ codeman agent post 841e7734 "END_DONE w226-version-view: head=57cf82a0cfc3 getrennt=3-spalten-zellen unklar=zelle mutante=echt-rot+gegenprobe redfirst=belegt lauf=42194394030-TERMINAL-SUCCESS lsremote=57cf82a0cfc3 | Readable version view as strictly separated wanted/applied/observed cells with UNCLEAR fallback, delivered via PR #1403 (ready, hosted CI green on head); base develop ea656d1f untouched by this lane."
✓ posted to 841e7734 (46 pending, 1 unseen)
```

```
$ codeman agent post 841e7734 "END_DONE w226-version-view: head=57cf82a0cfc3 getrennt=3-spalten-zellen unklar=zelle mutante=echt-rot+gegenprobe redfirst=belegt lauf=42194394030-TERMINAL-SUCCESS lsremote=57cf82a0cfc3 | Readable wanted/applied/observed version view with separated cells and UNCLEAR fallback delivered; PR #1403 ready with green hosted CI on head, akte on baseharbor-plan main (4082f00, ls-tree-Zeuge in der Akte)."
✓ posted to 841e7734 (47 pending, 1 unseen)
```

## Push-Zeuge (origin/main)

`git ls-tree -r --name-only origin/main | grep version-view` (nach push, wörtlich):

```
evidence/coord-memory/missions/w226-version-view.txt
evidence/r27-welle5-2026-11-06/version-view/round-1.md
tasks/t-20261018-r27-version-view.md
```

Push: `e1e2bb8..d82005a  main -> main` (nur diese Akte committet; die
unverfeuerten Anderungen anderer Lanes in `releases/v0.4.27.md`,
`roadmap/cards.md` und `evidence/.../vm-smoke/` wurden nicht angefasst).
Folge-Commits: `942692b` erganzt die wortliche END_DONE-Ausgabe, `3bdd269`
den erneut verifizierten ls-tree-Zeuge (jeweils nur diese Akte; die
unverfeuerten Anderungen anderer Lanes in `releases/v0.4.27.md`,
`roadmap/cards.md` und `evidence/.../vm-smoke/` wurden nicht angefasst).

