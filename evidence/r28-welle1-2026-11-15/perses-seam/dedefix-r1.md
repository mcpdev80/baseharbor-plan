# r28-welle1 Perses-Naht — Korrekturrunde dedefix-r1 (mission-seam-dedefix.md)

Karte: t-20261114-r28-perses-contract-seam, Kandidaten-Branch `lane-0428-075-perses-seam`
(PR #1575, Draft, base develop; PR #1590/#1592 tragen denselben Branch als base-Ref).
Auslöser: base-parity-akte `evidence/r28-welle1-2026-11-15/base-parity/round-1.md`, Signatur D
(FINDING-3): 7 verlorene DE-Literale in `docs/spec/management-access-v1.md`.
Lane: flash worker. Datum: 2026-11-15 (MESZ).

## Planungszonen- und Zonen-Zeugen (Pflicht)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel`
  = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`,
  `git remote get-url origin` = `https://github.com/mcpdev80/baseharbor-plan.git`
  (echtes Planning-Repo; das verwarnte `workers/baseharbor-plan` wurde nicht verwendet).
- Product-Zeuge ausschließlich `git ls-remote https://github.com/mcpdev80/baseharbor.git …`
  und ein eigener Worktree unter `/tmp/opencode/mission-seam-dedefix-wt`; das
  quarantänebehaftete `workers/baseharbor` wurde nicht zitiert und nicht geschrieben.
- Worktree-Erzeugung: `git worktree add --track -b lane-0428-075-perses-seam-dedefix
  /tmp/opencode/mission-seam-dedefix-wt origin/lane-0428-075-perses-seam` nach
  `git fetch --prune origin refs/heads/lane-0428-075-perses-seam refs/heads/develop`.

## Remote-Wahrheit vor der Arbeit (ls-remote)

```
aff1532c2f6c6782a8c13afad83245d1351815e7  HEAD            (baseharbor main)
0e9ccb582f5bdcdc74049bbe3996263cdce6500c  refs/heads/develop
af308e66d38ad1204345bbe83d066dd7548ea6e6  refs/heads/lane-0428-075-perses-seam
b001e1d2f7dd4760b8560e4032271c07f12afe56  baseharbor-plan refs/heads/main
```

Der Mission-Head `af308e66d` ist exakt der Remote-Tip des Kandidaten-Branches.
PR-Head-Zeugen (read-only `gh pr view --json headRefOid,baseRefName,isDraft`):

- #1575 OPEN draft base=develop head=`af308e66d…` (branch `lane-0428-075-perses-seam`)
- #1590 OPEN draft base=`lane-0428-075-perses-seam` head=`85b4cbb59…`
- #1592 OPEN draft base=`lane-0428-075-perses-seam` head=`f55d9f94c…`

## PLAN

Hinweis: diese Lane exponiert kein natives `todowrite`-Werkzeug; die nummerierte
Planliste liegt hier und in der Live-Boarddatei
`workers/todos/mission-seam-dedefix.md.json` (identische 7 Schritte).

- Schritt 1: Realitätsabgleich (ls-remote develop/main/seam, base-parity-Akte, PR-Heads) — erledigt
- Schritt 2: Worktree auf `lane-0428-075-perses-seam`, Head `af308e66d` verifiziert — erledigt
- Schritt 3: Diff EN gegen develop-stand, Verwurzelung der 7 Literale bestätigt — erledigt
- Schritt 4: Minimaler DE-Fix in `docs/de/spec/management-access-v1.md` — erledigt
- Schritt 5: Lokales Gate („DE technical integrity") + Doku-Audit nachgefahren — erledigt
- Schritt 6: Commit + Push auf denselben Branch, PR-Head gefolgt — erledigt
- Schritt 7: ls-remote-Zeugnis des neuen Heads + diese Akte + END post — erledigt

## Fund und Wurzel (Vorher-Zeuge)

Vorher, direkt auf dem Kandidaten-Head `af308e66d` (Worktree, Python 3.14):

```
$ python3 scripts/check_de_translation_integrity.py
spec/management-access-v1.md: literal lost: baha app status --json
spec/management-access-v1.md: literal lost: baha status --json
spec/management-access-v1.md: literal lost: configured_unverified
spec/management-access-v1.md: literal lost: management-ui
spec/management-access-v1.md: literal lost: not_configured
spec/management-access-v1.md: literal lost: perses
spec/management-access-v1.md: literal lost: verified
DE technical integrity: FAIL (7 findings across 167 paired pages)
gate-exit=1
```

Gate-Logik (read-only): `scripts/check_de_translation_integrity.py:34-36`
(Inline-Backticks EN ⊆ DE, Meldung `literal lost`), `:40` die FAIL-Zeile; aufgerufen
von `scripts/documentation-audit.sh:160`, das im Job `validate` im Step
„Validate documentation" läuft (`.github/workflows/ci.yml:315-320`, develop-Stand).

Verwurzelung, unabhängig wiederholt gegen das fetchte Repo:

- `git log --oneline origin/develop..origin/lane-0428-075-perses-seam -- docs/spec/management-access-v1.md`
  = `af308e66d`, `a5a5abedc`, `181872c90`, `61f76fa18` (alle 0428-075 auf dem Seam-Branch).
- `git log --oneline origin/develop..origin/lane-0428-075-perses-seam -- docs/de/spec/management-access-v1.md`
  = leer (0 Treffer) → die DE-Seite wurde nie gespiegelt.
- Der gesamte Perses-Abschnitt fehlt auf develop:
  `git show origin/develop:docs/spec/management-access-v1.md` hat nur
  `Scope / Authentication integration classes / Management roles / Environment policy / Surface acceptance`;
  `git log -S'Optional Perses management surface' --all -- docs/spec/management-access-v1.md`
  = `61f76fa18` einzig.

## Änderung (Nachher)

Datei: ausschließlich `docs/de/spec/management-access-v1.md` (+14 Zeilen, 0 Löschungen).

Der EN-Abschnitt „Optional Perses management surface" (EN-Zeilen 33-64) ist an
derselben Stelle — nach „Authentication integration classes", vor „Management roles" —
als „Optionale Perses-Management-Oberfläche" gespiegelt, mit identlichen
Inline-Literalen in Backticks: `management-ui`, `not_configured`,
`configured_unverified`, `verified`, `perses`, `baha status --json`,
`baha app status --json`. Die EN-Seite (authoritative Quelle,
`docs/STYLE_GUIDE.md:77`) ist unangetastet; bestehende, bereits vor der Basis
existierende Übersetzungsunterschiede (z. B. `## Authentifizierungsintegration`
statt `## Authentication integration classes`) wurden bewusst NICHT mitgenommen,
weil das Gate nur Backtick-Literale und Fences prüft und die Mission einen
minimalen Fix verlangt.

Der Nachher-Diff ist identisch mit `git show 219a0a24d` im Produktrepo
(Abschnitts-Add von 14 Zeilen); der Vorher-Zustand ist die Datei in `af308e66d`.

## Gate-Zeugnis (nach dem Fix, lokale Nachfahrt des CI-Schritts)

```
$ python3 scripts/check_de_translation_integrity.py
DE technical integrity: PASS (167 paired pages)
gate-exit=0
$ python3 scripts/check_docs_locale_parity.py
EN/DE page coverage OK: 167 matched Markdown pages
$ bash scripts/documentation-audit.sh
(exit 0; letzte Zeilen: Runtime docs PASS / Task/domain information architecture PASS /
 Podman release CI PASS / Brand identity PASS; keine FAIL-Zeile im Log)
$ mkdocs build --strict --config-file mkdocs.de.yml   # exit=0
$ mkdocs build --strict --config-file mkdocs.yml      # exit=0
```

Der vollständige `documentation-audit.sh` (nicht nur das Teilskript) wurde lokal
ausgeführt und ist grün; das ist mehr als der betroffene Step verlangt.
`.github/workflows/ci.yml` wurde ausschließlich gelesen (Step-Lokalisierung
Zeilen 315-320), nicht geändert.

## Provenienz des Kandidaten (Pflichtzeugen)

- Base-Attestation: geschnitten von `origin/lane-0428-075-perses-seam` =
  `af308e66d38ad1204345bbe83d066dd7548ea6e6` (exakt der ls-remote-Tip vor dem Push).
- Ancestry: `git merge-base --is-ancestor af308e66d38ad1204345bbe83d066dd7548ea6e6 HEAD` → YES.
- Eigene Commits (Liste muss NUR eigene zeigen):
  `git log --oneline af308e66d38ad1204345bbe83d066dd7548ea6e6..HEAD`
  = `219a0a24d docs(0428-075): mirror Perses management-surface spec section into the German page`
  (ein Commit, kein fremder Kandidat obenauf).
- Push: `git push origin HEAD:refs/heads/lane-0428-075-perses-seam` →
  `af308e66d..219a0a24d  HEAD -> lane-0428-075-perses-seam` (Fast-Forward, kein
  Force, kein Reset, kein zweiter Branch für dieselbe Kette; kein
  `ready_for_review`, kein Merge, keine PR-Kommentar-Aktion).
- Neuer Head (ls-remote-Zeugnis nach dem Push):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-075-perses-seam
219a0a24d5687552556b094223e5e4bcfa2eebc4  refs/heads/lane-0428-075-perses-seam
```

- PR-Head-Zeuge danach: #1575 `headRefOid = 219a0a24d5687552556b094223e5e4bcfa2eebc4`,
  weiter OPEN und Draft, base develop. #1590/#1592 haben unveränderte Heads
  (`85b4cbb59…`, `f55d9f94c…`) und folgen dem korrigierten base-Ref automatisch;
  ihre Signatur D ist damit auf ihrer Base-Kette behoben, ihre eigene O/R-Lane
  bleibt unberührt (base-seitig, siehe FINDING-1/-2 der Base-Parity-Akte).

## Gehosteter Lauf (Eigenes-Run-Pflicht §4.6, read-only beobachtet)

Der Push hat den PR-Lauf der Kette selbst ausgelöst:

- Run `43760586692`, workflow `CI · PR #1575`, event `pull_request`,
  `headSha = 219a0a24d5687552556b094223e5e4bcfa2eebc4`, `created_at =
  2026-11-15T20:53:32Z`, Status `in_progress` zum Zeitpunkt dieser Akte.
- Die Mission untersagt `workflow_dispatch` und alles unter `.github/**`;
  es wurde nichts manuell angestoßen oder umgeschaltet. Der Laufabschluss ist
  der nächste Trigger für eine Abnahme dieser Kette (`gh run view 43760586692`).
- Erwartung aus der Base-Parity-Akte: nach D-Fix läuft der Docs-Step grün und
  die Zelle erreicht „Run runtime integration tests serially", wo die
  base-seitigen Signaturen O (ORAS fehlt im validate-Job) und R
  (postgres-analytics läuft als root) weiterhin greifen — Kandidaten-seitig
  nicht behebbar,Owner-Scope (FINDING-1/-2).

## cleanliness

- Eigene Zone: `/tmp/opencode/mission-seam-dedefix-wt` (git worktree des
  Produktrepos `/home/marcel/dev/baseharbor-ecosystem/baseharbor`). Nach dem
  letzten Audit-Lauf wurde `site/` (mkdocs-Output) gelöscht;
  `git status --porcelain` im Worktree ist leer außer dem commiteten Fix.
- Kein Scratch außerhalb der Zone: nur `/tmp/opencode/mission-seam-en-develop.md`
  und `/tmp/opencode/{daudit*.log,mkdocs-*.log}` — alles unter /tmp/opencode,
  nichts im Ecosystem-Root.
- Keine Container, Netzwerke, Volumes oder Compose-Projekte gestartet; keine
  Docker-/Podman-/SSH-Testläufe nötig (reine Doku-Korrektur, Missionsschritt 3
  sind ausschließlich lokale Skript-Läufe).
  `docker ps -a --format '{{.Names}}' | grep -E 'bh-|baseharbor'` → keine von
  dieser Lane erzeugten Einträge (Lane hat keinen Container erzeugt).
- Product-Repo-Schreibaktionen: genau ein Fast-Forward-Push auf den
  Kandidaten-Branch der Karte. Keine Refs, Branches oder PRs angelegt,
  umbenannt oder gelöscht; keine Fremd-Session-Änderung angefasst.
- Planning-Repo: nur diese Akte (neues Verzeichnis
  `evidence/r28-welle1-2026-11-15/perses-seam/`), keine Fremddatei committet.

## repo-rule compliance

- §4.2 Scope: nur die in FINDING-3 gemeldeten 7 Literale, nur die
  Spiegelseite `docs/de/spec/management-access-v1.md`; die Mission erlaubt
  „bzw. die pair-Seite korrigieren — MINIMALER fix, genau die gemeldeten
  Literale, kein Umfeld-Umbau". Produkt-, Contract- und Workflow-Dateien:
  keine Änderung (`git show --stat 219a0a24d` = 1 Datei).
- Owner-Scope `.github/**`: nicht editiert; die nötigen Änderungen an ci.yml sind
  bereits in FINDING-1 der Base-Parity-Akte mit file:line gemeldet und werden
  hier nicht wiederholt oder „mitgenommen".
- Neue Tests: keine erzeugt (Doku-Fix; das bestehende Gate
  `check_de_translation_integrity.py` läuft bereits im `validate`-Job unter
  „Validate documentation", Trigger: `pull_request` auf die betroffenen Pfade,
  Zeuge `.github/workflows/ci.yml:315-320`). Damit ist keine CI-Triggeränderung
  nötig.
- §4.6 Eigenes-Run-Pflicht: der durch den Push ausgelöste Run 43760586692 ist
  identifiziert und wird bis zum Abschluss nur read-only beobachtet (§4.7
  verlangt keine Wiederholung bereits grüner Unchanged-Tests).
- §4.8 keine Subagenten; alle Schritte in dieser Session ausgeführt.
- Zustandsangabe: Karte bleibt auf `review`-Kandidat mit neuer SHA; kein
  Board-Statuswechsel durch diese Lane (Coordinator-Aktion), kein Merge, kein
  Release, kein Tag.

## Evidence-Push-Zeuge (zweitletzte Aktion)

```
$ git ls-remote origin refs/heads/main
c451f6862110b551b89fa29c5c9e390e3b28a9ac	refs/heads/main
```

Verifiziert im Frisch-Clone `/tmp/opencode/plan-check-dedefix` (gleicher SHA,
Pfad `evidence/r28-welle1-2026-11-15/perses-seam/dedefix-r1.md` vorhanden,
12106 Bytes). Im selben Verzeichnis liegt `act-1575-review-r8.md` einer anderen
Lane; die wurde nicht angefasst.

## END

END_DONE mission-seam-dedefix.md: 7 DE-Literale in docs/spec/management-access-v1.md
durch Spiegelung des Perses-Abschnitts nach docs/de/spec/management-access-v1.md
behoben; Gate „DE technical integrity" lokal PASS (167 paired pages) plus volles
documentation-audit.sh und mkdocs --strict (beide Locales) PASS; Kandidat
lane-0428-075-perses-seam neuer Head 219a0a24d5687552556b094223e5e4bcfa2eebc4
(PR #1575 Draft folgt automatisch, #1590/#1592 base-Ref korrigiert; PR-Lauf
43760586692 beobachtet offen).
