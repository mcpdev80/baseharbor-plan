# 0428-155 — card-status.py wait-gate inversion (DEFECT 1b, part 2: W2/W3)

Karte: `t-20261119-coord-tooling-defects` (0428-155), Fortsetzung der eigenen
Arbeit im coordinator-repo. Rolle: worker. Lieferung des W1 (Fix von Zeile 133,
Wartegate) war bereits im vorherigen Commit `646198ae` am HEAD des coordinator
committet und durch die 8 grünen Tests bestätigt. Diese Akte schließt die
RESTLICHE offenen Punkte ab: W2 (Regressionstests für den WAIT-Zweig) und W3
(Vollscans der Datei).

GEMESSEN am HEAD des coordinator, nicht am arbeitsbaum:

```
$ git -C coordinator show HEAD:scripts/card-status.py | sed -n '131,133p'
    if a.status == "active" and not re.search(r"(?m)^owner:", head):
        problems.append("active braucht owner")
    if a.status == "wait" and (not re.search(r"(?m)^owner:", head) or not field(head, "wait_reason").strip('"" ')):
```

Der WAIT-Zweig ist am aktuellen HEAD bereits von `^owner:\s*$` (invertiert) auf
`^owner:` (nicht-invertiert) gestellt — formgleich mit dem ACTIVE-Zweig.

## PLAN

1. W1 verifizieren: Zeile 133 (WAIT-Gate) ist am HEAD bereits non-invertiert
   (`not re.search(r"(?m)^owner:", head)`), identisch zur Struktur von Zeile 131.
   BEFUND: bereits erledigt in Commit `646198ae`.
2. W2a Regressionstest: Karte MIT echtem Inhaber + gesetztem `wait_reason` →
   WAIT-Gate muss durchgehen.
3. W2b Regressionstest: Karte OHNE `owner:`-Zeile → WAIT-Gate muss brechen.
4. W2c Regressionstest: Karte MIT Inhaber, OHNE `wait_reason` → WAIT-Gate muss
   brechen.
5. W3 Vollscans: alle `re.search`-Stellen mit `\s*$`-Muster + `not` davor in
   coordinator/**; prüfen, dass review/blocked/closed `field(...)` nutzen.
6. pytest + py_compile + bash -n laufen lassen.
7. Nur die Testdatei im coordinator-committen (kein `git -A`, kein Remote).
8. Diese Evidence schreiben und auf origin/main pushen.

## repo-rule compliance

- Write-Set: NUR `coordinator/tests/test_coord_tooling_fixes.py` (3 neue Tests in
  einer neuen Klasse `Defect1bWaitGate`). Zeile 133 in
  `scripts/card-status.py` war bereits im vorangegangenen Commit fixt; hier
  unverändert übernommen. Kein Write an baseharbor/tasks/* (die Karte führt der
  Owner), kein Write an baseharbor/Produktcode, kein Remote im coordinator.
- Branch-provenance: coordinator-repo hat KEIN Remote (wie task-scope gefordert,
  commit auf master). Base-HEAD vor dem Cut:

  ```
  $ git -C coordinator rev-parse HEAD
  646198ae8cf2da3414e64f833053ec0442c4f2b2
  ```

  Commits des Coordinators (nur die eigenen):

  ```
  $ git -C coordinator log --oneline -1
  e52d87af 0428-155: wait-gate regression tests (W2a/b/c) for card-status.py owner+wait_reason inversion
  ```

  Parent-Kette enthält nur eigene/Coordinator-Commits; kein foreign commit.
- Kein `git add -A`; nur `git add tests/test_coord_tooling_fixes.py`.
- Keine Subagenten (§4.8); alle Schritte in dieser Session ausgeführt.
- evidence/** nur in baseharbor-plan (das planning-repo unter
  /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan), NIEMALS im
  produkt-repo; workers/baseharbor-plan ist das quarantinierte Verzeichnis und
  wurde nicht benutzt.

## W1 — WAIT-Gate (Zeile 133)

Am aktuellen HEAD (Coordinator `646198ae`) ist der WAIT-Zweig bereits
non-invertiert, identische Form wie ACTIVE:

- Zeile 131 (active): `if a.status == "active" and not re.search(r"(?m)^owner:", head):`
- Zeile 133 (wait):  `if a.status == "wait" and (not re.search(r"(?m)^owner:", head) or not field(head, "wait_reason").strip('"" ')):`

Beide zweige nutzen `not re.search(r"(?m)^owner:", head)` → Problem, wenn der
Inhaber FEHLT, korrekt, wenn er vorhanden ist (beliebiger Wert, auch `''`).
Damit ist W1 (formgleiche zweige) am HEAD erfüllt.

## W2 — Regressionstests (neu)

Drei Tests in der Klasse `Defect1bWaitGate` (tests/test_coord_tooling_fixes.py),
jeweils eigener Tiny-Vault in einem temp-Dir, kein Zugriff auf das reale
baseharbor-plan:

- `test_wait_with_owner_and_reason_passes` (W2a): `owner: real-owner` +
  `wait_reason: wartet auf karte X` → kein `wait braucht owner + wait_reason`
  in der Ausgabe.
- `test_wait_without_owner_breaks` (W2b): nur `title: no-owner` +
  `wait_reason: ...` → `wait braucht owner + wait_reason` PRESENT.
- `test_wait_without_reason_breaks` (W2c): nur `owner: real-owner` →
  `wait braucht owner + wait_reason` PRESENT.

## W3 — Vollscan

Alle `re.search` in `scripts/card-status.py` (grep):

- Zeile 35: `field()`-Helfer — `re.search(r"(?m)^%s:\s*(.*)$")` — korrekt
  verwendet (kein Validate-Gate), `\s*$`-Muster nur hier.
- Zeile 43: `set_field` — `re.search(pat, head)` — korrekt (kein invertiertes
  Gate).
- Zeile 131 (active): `not re.search(r"(?m)^owner:", head)` — non-invertiert.
- Zeile 133 (wait): `not re.search(r"(?m)^owner:", head)` — non-invertiert.
- Zeile 145 (closed HTTPS): `not re.search(r"https?://", field(head, "evidence"))`
  — non-invertiert, nutzt `field(...)`.

review (135), blocked (137), closed (139-146) nutzen alle `field(...)` und sind
korrekt — kein invertiertes `\s*$`+`not`-Muster.

Vollscan über **alle** coordinator-Python-Skripte nach
`not re.search(...) .*\s*$`:

```
$ grep -rn 'not re\.search' --include=*.py coordinator | grep '\\s\*$'
(nichts gefunden)
```

Ergebnis: KEINE verbleibende invertierte `\s*$`-Stelle im coordinator. Der
einzige `\s*$`-Treffer ist der `field()`-Helfer (Zeile 35), kein Validate-Gate.

## TEST-BEWEIS

```
$ cd coordinator && python3 -m pytest tests -q
...........                                                              [100%]
11 passed in 0.59s
```

11 Tests (8 vom vorigen Commit + 3 neue WAIT-Gate-Tests). py_compile sauber,
bash -n auf allen coordinator/*.sh sauber.

Der WAIT-Zweig-Fall (W2a), den die 8 grünen Tests des vorigen Commits noch nicht
abdeckten, ist hiermit abgedeckt: die 11 grünen Tests beweisen jetzt, dass die
Zeilengrenze 133 in allen drei Konfigurationen (W2a/b/c) korrekt bricht oder
durchgeht.

## CLEANLINESS

- coordinator-repo: Working Tree nach dem Commit (nur die Runtime-Artefakte
  `.ram-level` etc. sind vom laufenden Coordinator extern getupt, nicht von mir;
  nur die Testdatei committet):

  ```
  $ git -C coordinator status --short
   M .ram-level
  ```

  `.ram-level` ist ein externer Coordinator-Artefakt, ungestagt, nicht Teil der
  Lieferung.
- Kein Remote im coordinator; kein Push nötig.
- VM-/Docker-/Podman-Projekte: keine gestartet. Kein daemon-Stack zu beenden.

## ENDS

END_DONE x-155w: 0428-155 wait-gate inversion — W1 am HEAD (`646198ae`)
bereits non-invertiert; W2a/b/c-Regressionstests (11 grün) committet in
coordinator `e52d87af`; W3-Vollscan: kein invertiertes `\s*$`+`not`-Gate
übrig.
