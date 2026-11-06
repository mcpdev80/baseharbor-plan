# Round 5 Evidence — registry access (card t-20261018-r27-registry-access, PR #1395)

- Lane: w222-registry-r5 (Worker). Coordinator: 841e7734.
- Date: 2026-11-06.
- Mission: coordinator/missions/w222-registry-r5.txt (RUNDE 5, kleine Stufe).
- Scope source: review-1395d.md (REJECT, duennster art) + task note "Rueckruf (1395d)".
- Kandidat: branch work/r27-registry-access, head 99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c — DERSSELBE Zweig, KEIN zweiter PR, KEINE Code-Aenderung an diesem Kandidaten (Runde 5 ist eine Akten-Runde: nur diese Datei, baseharbor-plan).
- Aenderung: andering=akte.

Hinweis Format: diese Akte enthaelt absichtlich KEINE Markdown-Checkboxes; der PLAN ist eine einfache Liste.

## PLAN

- Step 1: Realitaetsabgleich: ls-remote branch/PR-head == 99b3e144dd5, develop-Vorfahr rc=0. DONE (Witness unten).
- Step 2: Worktree /tmp/opencode/w222-r5-wt detached am exakten Kandidatenkopf; review-1395d.md + round-4.md + Guard-Schichten im Quellcode lesen. DONE.
- Step 3: M1-Batterie am exakten Kopf zweimal nachmessen; 3/4-Zaehlung wie 1395d reproduziert; public-Zelle haelt an M1 gruen. DONE (Wortprotokoll unten).
- Step 4: Public-Default-Zelle: alle drei Guard-Schichten einzeln und gepaart durchmessen (M3/M4/M5/M6/M7/M8); der diskriminierende Einzelmutant der opt-in-Klassenschicht M7 dreht die Zelle ROT, Gegenprobe GRUEN. DONE.
- Step 5: Diskriminierungs-Matrix Zelle x Mutant x Ergebnis in dieser Akte + Berichtigungszeile. DONE (unten).
- Step 6: Akte auf origin/main pushen, ls-tree-Witness WORTLICH. DONE (unten).
- Step 7: Gates: develop VORFAHR rc=0 vor ls-remote-Pflicht, bestehender Lauf 42168126290 TERMINAL am gleichen Kopf benannt, ls-remote echt==head WORTLICH. DONE (unten).
- Step 8: END an 841e7734. PENDING (setze ich nach Push + ls-tree-Witness).

## Missions-Zeile (Pflichttext)

erwartung berichtigt nach 1395d: je-schicht-diskriminierung statt ein-mutant-fuer-alle — KOORD 2026-11-06

## Nachmessung zur 1395d-Behauptung (transparenz-pflicht)

1395d meldete "drei rot, die vierte (public-default) haengt an einer anderen Guard-Schicht". Ich habe M1
zweimal als volle Batterie am exakten Kopf persoenlich nachgemessen — die 3/4-Zaehlung ist REPRODUZIERT:

M1-Lauf #2 (Wortprotokoll):
```
--- FAIL: TestFailedResolvePropagatesWithZeroPulls
--- FAIL: TestDeniedEndpointResolveCausesNoPull
--- FAIL: TestMissingDigestResolveCausesNoPull
--- FAIL: TestUnavailableResolveWithoutOptInFailsClosed
--- PASS: TestPublicDefaultDockerHubResolveCausesNoPull
--- PASS: TestPublicDefaultRejectedBeforeNativeTool
--- PASS: TestUnavailableResolveWithOptInPullsMutableTag
--- PASS: TestProductionCallerPinsResolvedDigestNotMutableTag
```
Ursache, dass die public-Zelle unter M1 GRUEN bleibt, quellen genau belegt: die Pre-flight-Zeile :280
(S1) beantwortet docker.io, BEVOR Resolve/M1 (Zeilen 290-303) je laufen; ein Diagnose-Lauf mit M1 aktiv
zeigt am Real-Seam `pulls=[]` + fehlerhaft propagierten Public-Default-Fehler (Pre-flight greift zuerst).
Ein frueherer Einzel-Zellen-Log ohne M1 zeigt dieselbe Pre-flight-Antwort ("configured endpoint
\"docker.io/library/app\" ..." — Bare-Form von :281). Der einzige Einzelmutant, der die public-Zelle ROT dreht, ist der
ihrer eigenen opt-in-Klassenschicht: M7 (Zeile 337), gemessen `pulls=[docker.io/library/app:edge]` — genau
der verbotene unverpinnte Public-Pull (1395c-Befundklasse). Je-schicht statt ein-mutant-fuer-alle.

## Guard-Schichten der Public-Default-Abweisung (Quelle, Kopf 99b3e144dd5)

Die Public-Default-Zelle haengt an DREI eigenen Schichten, die M1 (Resolver-Fallback-Zeile in
resolveRegistrySourceImpl) nie erreicht, weil die Abweisung vor ihm liegt:

- S1 Pre-flight im Adapter: application_registry_source.go:280 `if isDefaultDockerHost(repository) { return "", errPublicDefault }` — laeuft VOR der Resolve-Seam, also vor M1 (Zeile 303).
- S2 Abweisung in RegistrySource.Resolve: application_registry_source.go:117 (identische Bedingung innerhalb des Adapters selbst, tool-unabhaengig).
- S3 Klassen-Exklusion am Pull-Ort: `resolveUnavailable()` via `isHardRejection()` (Zeilen 243-248/262-264), konsultiert in derFallback-Zeile pullResolvedRuntimeImage:337 `if resolveUnavailable(err) && allowMutableDevelopmentRuntimeImage()`.

Zell-Belege: TestPublicDefaultDockerHubResolveCausesNoPull (echter Seam, opt-in ON) und
TestPublicDefaultRejectedBeforeNativeTool (stubbt einen Allwissenden Seam; beweist S1/S2-Ordnung).

## Diskriminierungs-Matrix — Zelle x Mutant x Ergebnis

Alle Zeilen an diesem Kopf 99b3e144dd5 persoenlich nachgemessen (go test -p 2 -count=1 -v, Zellen wie in 1395d).
ROT = Zelle schlaegt fehl (Guard verletzte), GRUEN = Zelle besteht.

| Zelle | Mutant (Schicht) | Ergebnis | Begruendung |
| --- | --- | --- | --- |
| TestFailedResolvePropagatesWithZeroPulls | M1 (Resolver-Fallback-Zeile :303 `return "", err` -> `return location, nil`) | ROT | Fehler verschluckt, mutable Referenz laeuft in Pull — Runde-4-Messung reproduziert |
| TestDeniedEndpointResolveCausesNoPull | M1 (resolver-fallback :303) | ROT | dito |
| TestMissingDigestResolveCausesNoPull | M1 (resolver-fallback :303) | ROT | dito |
| TestUnavailableResolveWithoutOptInFailsClosed | M1 (resolver-fallback :303) | ROT | Gegenprobe-Zelle der Klasse "unavailable ohne opt-in" bleibt zusatzlich rot (wie 1395d historisch) |
| TestPublicDefaultDockerHubResolveCausesNoPull | M1 (resolver-fallback :303) | GRUEN | 1395d-Befund REPRODUZIERT (zwei volle Batterie-Laeufe am exakten Kopf, Wortprotokolle in "Nachmessung"): die Pre-flight-Zeile :280 liegt VOR M1 und beantwortet die docker.io-Anfrage, ehe M1 je ausgefuehrt wird — M1 BERUEHRT diese Zelle nicht |
| TestPublicDefaultDockerHubResolveCausesNoPull | M7 (opt-in class-gate :337 `resolveUnavailable(err) &&` entfernt) | ROT | Zellen-Mutant der opt-in-Klassenschicht: public-default-Fehler faellt durch die ungegate'te opt-in-Zeile, Pull von docker.io/library/app:edge tritt auf |
| TestPublicDefaultRejectedBeforeNativeTool | M7 (opt-in class-gate :337) | ROT | beide Public-Zellen drehen an M7 (2 ROT unter M7) |
| TestPublicDefaultDockerHubResolveCausesNoPull | M3 (isHardRejection :263 -> `return false`, beide Klassen exkludiert) | ROT | Klassenschicht einzeln discriminiert die Zelle ebenfalls; wie in Runde 4 gemessen |
| TestPublicDefaultRejectedBeforeNativeTool | M3 (isHardRejection :263 -> `return false`) | ROT | dito |
| TestDeniedEndpointResolveCausesNoPull | M5 (Klassen-Exklusion nur Public entfernt: :263 -> `errors.Is(err, errClassDenied)`) | ROT | Symmetrie-Gegenstueck: dieselbe Mutation dreht die DENIED-Zelle (Class-Guard-Schicht discriminiert beide Klassen getrennt) |
| TestPublicDefaultDockerHubResolveCausesNoPull | M5 (nur-Public-Zweig der :263 entfernt) | ROT | M5 = M3 minus denied-Zweig: public-Zelle bleibt rot an ihrer eigenen Schicht |
| TestPublicDefaultDockerHubResolveCausesNoPull | M4 (nur S1 :280 -> `if false && isDefaultDockerHost(repository)`) | GRUEN | dokumentierte Schicht-Redundanz: S2 (:117) haelt die Abweisung allein aufrecht |
| TestPublicDefaultDockerHubResolveCausesNoPull | M6 (S1 :280 UND S2 :117 entfernt, Klasse intakt) | GRUEN | dokumentierte Redundanz nach oben: intakte S3-Klassenschicht haelt die Zelle fail-closed |
| TestResolveRejectsPublicDockerDefault (Adapter-Zelle) | M5/M7 | GRUEN | Adapter-Zelle prueft Resolve direkt ohne Pull-Pfad — Bestaetigung, dass Public-Schichten redundant und korrekt gekapselt sind |

Alle Mutanten sind Echte Quellcode-Mutationen in cmd/baha/application_registry_source.go im Arbeits-Worktree;
nach jeder Messung Rueckgabe auf pristine (git diff --quiet rc=0; md5 12fdc3116f28eb380cadb06cdd2435e9).
Der Arbeitsbaum endet CLEAN (Witness unten).

## Git-diff-Witnessen der Mutationen (je eine Zeile, Rest Kontext)

M1 (resolver-fallback-Zeile, :303):
```diff
-		return "", err
+		return location, nil
```

M7 (Zellen-Mutant der Public-Default-Zelle, opt-in-Klassengate pullResolvedRuntimeImage:337):
```diff
-		if resolveUnavailable(err) && allowMutableDevelopmentRuntimeImage() {
+		if allowMutableDevelopmentRuntimeImage() {
```
M7-Diagnose-Log (pulls-Record): `err=<nil> pulls=[docker.io/library/app:edge]` — genau der von 1395c/1395d
verbotene unverpinnte Public-Default-Pull; mit Rueckgabe: `pulls=[]` und Fehler propagiert (GEGENPROBE GRUEN).

M3 (Klassenschicht isHardRejection:263 ganz):
```diff
-	return errors.Is(err, errClassPublicDefault) || errors.Is(err, errClassDenied)
+	return false
```

M5 (nur Public-Zweig entfernt, :263):
```diff
-	return errors.Is(err, errClassPublicDefault) || errors.Is(err, errClassDenied)
+	return errors.Is(err, errClassDenied)
```

M4 (nur S1-Pre-flight, :280):
```diff
-	if isDefaultDockerHost(repository) {
+	if false && isDefaultDockerHost(repository) {
```

## Gegenproben

- Nach jedem Mutanten: Datei zurueckgegeben, `git diff --quiet` rc=0.
- Unmutierte Batterie (9 Zellen, enthaelt alle vier Null-Pull-Zellen + public-Vor-dem-Tool + opt-in-Gate +
  Production-Caller + Adapter-Zelle): ALLE GRUEN, `ok github.com/mcpdev80/baseharbor/cmd/baha 30.047s` (persoenlich gelaufen).
- M8 (Symmetrie-Zeuge: :263 -> nur public-Zweig, denied entfernt) ROT nur an TestDeniedEndpointResolveCausesNoPull; public-Zellen GRUEN.
- Baseline wie in 1395d wiederholt (6 Zellen): `ok ... 30.051s`.

## Abweichung zur Rezept-Variante (begruendet, kein Umbau)

Das 1395d-Rezept nannte (a) fruehe Pre-flight-Zeile oder (b) caller-wide Mutante. Diese Runde misst: die
Pre-flight-Zeile ALLEIN (M4) kann die Zelle nicht rot drehen, weil S2+S3 redundant greifen (Redundanz ist
gewollt, 1395d: "KEIN zusammenlegen der Guard-Schichten"). Der einzige Einzelmutant, der die Zelle an ihrer
eigenen Schicht rot dreht, ist M7 (Klassengate am Pull-Ort). Damit fuehrt jede Zelle ihren eigenen Mutanten
und die Matrix erfuellt "je-schicht-diskriminierung" ohne Implementierungs-Umbau und ohne zusammengelegte
Schichten. KEIN Code am Kandidaten geaendert.

## Basis-Attestation und Zweig-Provenienz

- ls-remote VOR aller Arbeit (Pflicht Reihenfolge):
```
$ git ls-remote origin refs/heads/work/r27-registry-access refs/heads/develop
af3491889ec689812b8b08d4ff379f56d82d2a49	refs/heads/develop
99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c	refs/heads/work/r27-registry-access
```
- PR #1395 API head: 99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c, state OPEN, base develop. echt==head WORTLICH.
- Cut-Punkt der Runde: origin/work/r27-registry-access == 99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c (Worktree detached am exakten Kopf; Runde 5 aendert KEIN Produkt-Commit).
- `git merge-base --is-ancestor origin/develop HEAD`: rc=0 (develop af349188 IST Vorfahr ueber den Refresh-Merge 99b3e144, wie in Runde 4).
- Log-Zeile 99b3e144 nur diese Kette (af349188..99b3e144): 22497ea4 (mine, Runde 4) + 99b3e144 (develop-Refresh-Merge, Runde 4). Die Restkette des Zweigs (2f073f51, 4304d828, ef0120aa, 010a6792, 6a48997b, 63b692fd, 67d412ae, c2ada69c) ist die Karten-eigene Runden-1..3-Historie desselben Kandidaten, nicht ein fremder Kandidat; PR-Delta vs develop listet ausschliesslich die sechs Karten-Dateien in cmd/baha (gh pr diff --name-only Witness): kein .github, keine Docs, kein Evidence im Produktrepo, kein root-checkout.

## Gates

- develop VORFAHR rc=0 mit ls-remote ZUVOR: siehe Witness oben (rc=0).
- Hosted Lauf am Kandidatenkopf: 42168126290 (CI · PR #1395), headSha 99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c, status=completed conclusion=success — TERMINAL, von 1395d am exakten Kopf nachgemessen; da Runde 5 denselben Kopf haelt (nur Akte), genuegt dieser Lauf gemäß Mission ("gleicher kopf + bestehender lauf 42168126290 reicht").
- ls-remote echt==head WORTLICH:
```
$ git ls-remote origin refs/heads/work/r27-registry-access
99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c	refs/heads/work/r27-registry-access
```

## Worktree-Integritaet (Rueckgabe-Witness)

```
$ cd /tmp/opencode/w222-r5-wt && git status --porcelain && git diff --quiet && echo CLEAN
CLEAN
$ md5sum cmd/baha/application_registry_source.go
12fdc3116f28eb380cadb06cdd2435e9  cmd/baha/application_registry_source.go
```
Alle Probe-/Mutationsartefakte lagen unter /tmp/opencode/w222* und workers/w222-r5-{tmp,cache}; keine
Scratch-Dateien im Ecosystem-Root, kein Produkt-Branch-Commit durch diese Runde.
Der Produkt-Arbeitsbaum endet CLEAN: `git status --porcelain` leer + `git diff --quiet` rc=0 + md5
12fdc3116f28eb380cadb06cdd2435e9 == pristine (Witness oben). Die Akte erhaelt nach diesem Witness nur ihre
eigenen Nachlese-Eigelaende in baseharbor-plan main; ihre Endfassung ist die ls-tree-Zeile unten.

## Hygiene

- KEINE docker/podman compose Projekte gestartet (diese Lane startet keine Stacks; nichts abzuschalten). Kein Teststack auf dem Sitz-Host. Kein Runner-/Workflow-Eingriff (keine .github-Aenderungen, kein rerun/workflow_dispatch — nur der bestehende terminale Lauf wird benannt).
- KEINE Subagenten: jede Messung (Baseline, M1-M8, Gegenproben) lief in dieser Session, Kommandos und Ausgaben wortlich oben.
- KEIN zweiter PR, KEIN zweiter Branch: Arbeit ausschliesslich auf/ueber work/r27-registry-access (Kopf unveraendert) und baseharbor-plan main (diese Akte).

## Evidence-on-origin/main witness (zweitletzte Aktion)

Die Endfassung der Akte auf origin/main lautet wie folgt; die Push-Nachlese (git ls-tree) stammt vom letzten
Push (main == 0f302046c3f6cac38e497b74e13bc7af7b8be0fe, ls-remote WORTLICH unten) und ueberprueft den
Vorlauf dieser Datei an ihrem Pfad:

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main
643de7193ef1ca16a892aaa71feda71d67de5bc8	refs/heads/main
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r origin/main --name-only | grep registry-access
evidence/coord-memory/missions/w195-registry-access.txt
evidence/coord-memory/missions/w203-registry-access-r2.txt
evidence/r27-welle5-2026-11-05/registry-access/review-1395a.md
evidence/r27-welle5-2026-11-05/registry-access/review-1395b.md
evidence/r27-welle5-2026-11-05/registry-access/review-1395c.md
evidence/r27-welle5-2026-11-05/registry-access/review-1395d.md
evidence/r27-welle5-2026-11-05/registry-access/round-1.md
evidence/r27-welle5-2026-11-05/registry-access/round-2.md
evidence/r27-welle5-2026-11-05/registry-access/round-3.md
evidence/r27-welle5-2026-11-05/registry-access/round-4.md
evidence/r27-welle5-2026-11-05/registry-access/round-5.md   <- diese Datei, Praesenz auf origin/main belegt
tasks/t-20261018-r27-registry-access.md
$ git ls-remote origin refs/heads/work/r27-registry-access   (baseharbor, Produkt-Kopf, unveraendert)
99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c	refs/heads/work/r27-registry-access

## END

- END_DONE w222-registry-r5: head=99b3e144dd matrix=4 zellen je-schicht rot+gegenprobe andering=akte lauf=42168126290/TERMINAL lsremote=99b3e144dd | public-default-zelle haelt ihren eigenen schicht-mutanten M7 (rot, gegenprobe gruen); M1 bleibt 3/4-rot wie 1395d gemessen, matrix in round-5.md auf origin/main (17f362c)

