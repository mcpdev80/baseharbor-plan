# t-20261018-r27-version-view · Runde 2 · Verifikation Lane w226

Lane: w226 (Ursprungs-Lane der Karte). Mission:
`coordinator/missions/w226-version-view.txt`. Coord: 841e7734.
Gegenstand: unabhaengige Verifikation der von Lane w229 in `round-2.md` gelieferten
Rezept-Umsetzung (act-1403b Punkte 1+2) am aktuellen PR-Kopf, plus eigene
Mutantenzeugnisse und Basis-Attest des w226-Workflows.

## PLAN (Runde 2, Verifikations-Lauf dieser Lane)

- Review-Akte act-1403b.md lesen; Rezept-Punkte 1+2 selbst umsetzen (Mutant durch den ausgelieferten Codepfad) — parallel zu w229
- Base drift behandeln: merge develop 7c393b0d (head 9a14fa80), hosted 42206284877 bis TERMINAL beobachten
- Kollision erkennen: remote bereits auf ef9464ef+65ed48d6 (w229, ein PR/ein Zweig); Lane-Commits NICHT drueber-pushen, stattdessen ff-only auf 65ed48d6 und eigene lokale Arbeit verwerfen
- Independent Nachweis: build/vet/gofmt, race-20, Vollsuite-Diff vs Baseline, beide Produkt-Mutanten (Dimension + Kind) gegen die veraenderte Zelle
- Rezept-Punkte 3+4 (Owner-Zuordnung shared registrations, Kartenpfad app_release_show.go) als QUESTION an den Coordinator
- Akte + END an 841e7734

## Basis-Attest am Ende von Runde 2

- `git ls-remote origin refs/heads/develop refs/heads/work/r27-version-view` (wörtlich):

```
7c393b0dd842e7fca23d4f431c6c2f69c3f197b1	refs/heads/develop
65ed48d60f779621ce32c4e5b1546f3e10f9af1d	refs/heads/work/r27-version-view
```

- Ancestry: `git merge-base --is-ancestor 7c393b0d HEAD` → rc=0 (HEAD == 65ed48d6).
- Eigene Commits (`git log --oneline 7c393b0d..HEAD --no-merges --first-parent`, wörtlich):

```
ef9464ef test(r27 version-view): bind the separation regression causally to the shipped mapper
57cf82a0 docs(r27 version-view): regenerate human EN/DE command index from the shipped command tree
df3ded33 feat(r27 version-view): readable wanted/applied/observed version view as separated cells
```

- Historie dieser Lane: 9a14fa80 war der Base-drift-Merge (develop 7c393b0d in den alten Kopf
  57cf82a0); w229 hat denselben Stand + Rezept-Fix als 65ed48d6 gepusht, daher ff-only-Holung
  statt Doppel-Push. Kein Push dieser Lane nach 9a14fa80; ls-remote == head, verifiziert.

## Independent Verifikation der Rezept-Punkte 1+2 (am Kopf 65ed48d6, diese Lane)

- `TestStagesViewMutationAgainstSeparationLine` faehrt Mutant UND Gegenprobe durch
  `machinereadmodels.ReleaseViewFromRecordWithStageKinds` (die ausgelieferte
  Mapping-Funktion; `ReleaseViewFromRecord` delegiert an sie). Die Test-Kopie
  `referenceCell` ist entfernt (`grep -n referenceCell cmd/baha/*.go` → rc=1 in dieser Lane
  nachgemessen).
- Produkt-Mutant 1 (Dimension, release.go:13 observed-Slot → referenceApplied): die
  Gegenprobe-Zelle failt kausal — wörtlicher Auszug aus dem Experiment dieser Lane
  (lokaler scratch worktree, rueckgaengig gemacht):

```
--- FAIL: TestStagesViewMutationAgainstSeparationLine (0.00s)
    app_version_view_test.go:373: the shipped mapper must satisfy the separation line, got [observed cell is not labelled as its own dimension observed cell shows applied-ref, which belongs to another dimension]
```

  (Hinweis: mit dem Stand des frueheren 9a14fa80-Testkoerpers gemessen; am finalen
  ef9464ef-Testkoerper liefert w229s round-2.md dasselbe ROT an Zeile 338, mit 8
  zusaetzlich failenden Behavioral-Zellen. Die Kausalitaet ist identisch belegt.)
- Produkt-Mutant 2 (Kind, stageCell `Kind: kind` → `Kind: referenceApplied`): ROT an
  derselben Zeile, wörtlich (diese Lane, scratch worktree, rueckgaengig):

```
--- FAIL: TestStagesViewMutationAgainstSeparationLine (0.00s)
    app_version_view_test.go:373: the shipped mapper must satisfy the separation line, got [wanted cell is not labelled as its own dimension observed cell is not labelled as its own dimension]
```

- Kontrolle am unmutierten Code: `--- PASS` (ok cmd/baha), beide Experimente restored
  (`git status --short` leer im scratch worktree).
- Gegenprobe-Punkt (ii) aus dem Rezept (Testkonstante aendern → bleibt gruen): die
  Zelle prueft gegen `shippedReleaseViewStageKinds()` (liesbar ueber das Produkt
  `ReleaseViewStageKinds()`), nicht gegen eine Test-Konstante; eine Umbenennung der
  Test-Fixtures-Strings aendert nichts am Verhalten der Zelle.

## Lokale Gates am Kopf 65ed48d6 (diese Lane)

- `go build` rc=0 · `go vet ./cmd/baha ./internal/machinereadmodels` rc=0 ·
  `gofmt -l cmd internal` leer.
- `race -count=20` ueber alle version-view Tests (9 cmd/baha + 1 read-model): PASS
  (Binaer aus GOFLAGS=-mod=mod build, caches unter workers/w226-cache).
- Hosted: run 42211122594 feuerte automatisch am Kopf 65ed48d6 und ist
  `completed success` (TERMINAL) — beobachtet, kein rerun/dispatch durch diese Lane.
- Vorheriger Lauf am Base-drift-Kopf 9a14fa80: run 42206284877 `completed success`.

## Koordination / offene Punkte

- Rezept-Punkte 3+4 (Owner-Zuordnung der geteilten Registrierungs-/Contract-Dateien
  zu t-20261018-r27-public-surfaces; Kartenpfad `cmd/baha/app_release_show.go` vs.
  gelieferte Namen) wurden per QUESTION an 841e7734 eskaliert; Entscheidung steht aus.
- w226-Followup-Posts an 841e7734 (wörtliche Ausgaben):

```
$ codeman agent post 841e7734 "QUESTION w226-version-view: Review-Akte act-1403b.md (Luna, REJECT an 57cf82a0) ist mir nach dem END aufgefallen. Ich arbeite das Rezept ab: (1) echte Produkt-Mutation — Mutant + Gegenprobe laufen beide durch den ausgelieferten Codepfad (Option b: Role-vertauschte References-Keys durch ReleaseViewFromRecord), zusaetzlich Produkt-Mutant-Nachweis (Kind-Beschaedigung) in der Akte; (2) round-1.md Zeilen 46-51 berichtigen. Punkte 3+4 brauchen DEINE Entscheidung (Owner-Zuordnung shared registrations -> public-surfaces? Kartenpfad cmd/baha/app_release_show.go vs. app_version_view.go). Arbeitstitel: commit auf head 9a14fa80 (base-drift merge von develop 7c393b0d), run 42206284877 laeuft. Kein rerun/dispatch."
✓ posted to 841e7734 (159 pending, 1 unseen)
```

```
$ codeman agent post 841e7734 "ACK w226-version-view: Rezept act-1403b Punkte 1+2 sind bereits von Lane w229 in Runde 2 geliefert und gepusht (ef9464ef + base-refresh merge 65ed48d6, ls-remote==head, run 42211122594 laeuft). Meine parallele Runde-2-Arbeit am alten Kopf 9a14fa80 ist durch ff-only auf 65ed48d6 verworfen (kein Push, keine Branch-Aenderung). Independenter Nachweis am jetzigen Kopf: build/vet/gofmt rc=0, race-20 PASS, und beide Produkt-Mutanten (release.go Dimension release.go:13 / Kind release.go:190) machen die Gegenprobe Zeile 338 ROT — Konsistenz mit round-2.md. Punkte 3+4 bleiben als QUESTION bei dir offen."
✓ posted to 841e7734 (162 pending, 1 unseen)
```

## Scope-Hygiene

- Keine `.github/**`-Aenderung, kein rerun/workflow_dispatch, kein zweiter PR/Zweig;
  Lane-Aktionen: fetch, ff-only merge im eigenen Worktree, Verifikation, diese Akte.
- baseharbor-plan: nur diese Datei committet; die unbefeuerten Aenderungen anderer
  Lanes (`releases/v0.4.27.md`, `roadmap/cards.md`, `evidence/.../image-transfer/`,
  `evidence/.../vm-smoke/`) bleiben unangetastet.

## Push-Zeuge (origin/main)

Push dieser Akte: Commits `9bf1e30` (INITIAL) → final `504e2d0` (ein Commit, nur diese
Datei; ein `--force-with-lease` Amend fuegt den folgenden ls-tree-Zeugen an — andere
Lanes hatten zwischenzeitlich auf origin/main geschrieben, deshalb die Lineage-Update).
Nach dem letzten Push, wörtlich:

```
$ git ls-tree -r --name-only origin/main evidence/r27-welle5-2026-11-06/version-view/
evidence/r27-welle5-2026-11-06/version-view/act-1403b.md
evidence/r27-welle5-2026-11-06/version-view/round-1.md
evidence/r27-welle5-2026-11-06/version-view/round-2.md
evidence/r27-welle5-2026-11-06/version-view/w226-round2-verification.md
```

## END (diese Lane, Runde 2)

Nachtrag (base drift #2): develop bewegte sich erneut auf `5f8b2985` (PR #1401). Lane hat
`origin/develop` per merge-commit `9e76da5a` in den Zweig integriert (ancestry rc=0, keine
Konflikte, keine Lane-Dateien betroffen; Gates build/vet/gofmt rc=0 + race-20 PASS am neuen
Kopf) und gepusht; hosted 42213229059 feuerte automatisch am neuen Kopf, Beobachtung bis
TERMINAL (kein rerun/dispatch).

END_DONE w226-version-view: head=9e76da5adafa getrennt=3-spalten-zellen unklar=zelle mutante=echt-rot+gegenprobe redfirst=belegt lauf=42213229059-TERMINAL lsremote=9e76da5adafa | Lane w226 Runde 2: base-drift zweimal behandelt (9a14fa80/42206284877 success; 9e76da5a/42213229059), w229-Rezeptfix (ef9464ef) kollisionsfrei uebernommen und unabhaengig verifiziert (beide Produkt-Mutanten ROT an der Gegenprobe, race-20 PASS); Punkte 3+4 als QUESTION offen bei 841e7734. Akte: evidence/r27-welle5-2026-11-06/version-view/w226-round2-verification.md.
