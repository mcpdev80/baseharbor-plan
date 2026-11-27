# Akte w383-0428-275-136rows — Baseline-Zeilen-Gap-Analyse fuer plan PR #136

**Lane:** w383-0428-275-136rows
**Karte:** 0428-275 existiert NICHT als Karte unter diesem Namen (Befund unten, Abschnitt f). Mission: `coordinator/missions/w383-0428-275-136rows.txt`
**ART:** NUR Analyse + evidence-only. Kein Produkt-/Katalog-Edit, kein Push an baseharbor, kein hosted run, kein Merge.
**Ausgefuehrt:** 2026-11-27, read-only gegen origin-refs.

## PLAN

1. Mission und AGENTS lesen; Plan-Repo-Identitaet via `git remote -v` attestieren; isoliertes plan-worktree `workers/w383-0428-275-136rows-plan` aus `origin/main` anlegen; diese Akte mit ## PLAN erstellen.
2. (a) Vorarbeits-Akten der Familie auf plan main (w376/w377/w378/w379/w380/w381); fehlende Akten gemeldet (Abschnitt (a)).
3. (b) Geforderte Quellen zusammenstellen (namentlich + datei:zeile) aus den Akten und den PR-Diffs gegen develop.
4. (c) Vergleich mit dem, was #136 auf seinem head liefert (gh api + `git diff origin/main...origin/pr-136`); develop-`scripts/pr-gate-coverage.json` vs Kandidaten-heads; Klassifikation (i)/(ii)/(iii).
5. (d) Schluessel pruefen, den das Gate erwartet: baseharbor `scripts/pr-gate-plan.py:1952` ValueError + `scripts/validate-pr-gate-coverage.py` (nur festhalten).
6. Akte fertigstellen (Tabelle + Owner-Satz + 4-Feld), under Lane-Identitaet committen, pushen, plan PR oeffnen, origin/main-Witness, END-Post.

## Visible ANSATZ block

- Lane canonical identity: `w383-0428-275-136rows`
- git user.name: `w383-0428-275-136rows`; git user.email: `w383-0428-275-136rows@baseharbor.local`
- Invocation: `git -c user.name=w383-0428-275-136rows -c user.email=w383-0428-275-136rows@baseharbor.local commit ...`
- Pre-push gate: `git show -s --format=%an HEAD` muss exakt `w383-0428-275-136rows` liefern; sonst STOP + Meldung.
- Karten-Frontmatter owner: die Mission stellt fest, dass Karte `0428-275` nicht als Karte existiert (Befund); daher Lane-Identitaet aus der Mission massgeblich.

## Realitaets-Zeugen

- Plan-Repo (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) (push)` — NICHT das workers/-Unterverzeichnis (Quarantaene-Check beachtet).
- Plan worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w383-0428-275-136rows-plan`, base `origin/main = 9b05cb986f5721a193a30c7e8f44a5addfec196b` (ls-remote-equivalent via fetch; Ancestor des ersten eigenen Commits).
- Plan main enthaelt KEIN `scripts/pr-gate-coverage.json` und KEIN `scripts/pr-gate-plan.py` (`git -C baseharbor-plan ls-tree -r --name-only origin/main | grep pr-gate` => leer; `ls scripts/` = plan.py, release_cycles.py, snapshot.py, migrate_bases_kanban.py, tests/). Der Katalog, um den es geht, lebt ausschliesslich im Produktrepo baseharbor.
- Plan PR #136 (`gh api repos/mcpdev80/baseharbor-plan/pulls/136`): state open, draft false, base `main`@`ef0bcbcf...`(ef0bcfbcf), head `c4e4400174dc3fe5c04082c7c85483db9b82543f` (branch `w267-0428-359-recovery-catalog`), changed_files 577.
- Produkt-Refs (nur github.com/mcpdev80-Remotes, im geteilten baseharbor-Checkout nach `git remote -v`-Aufloesung, alle pointing https://github.com/mcpdev80/baseharbor.git):
  - develop = `ea5218d72e263f21e79853b679af50074dab8c25`
  - #1860 head = `057ce8c55416f8970a40e88af3dbaf7115ec26ec`; #1861 head = `ade7dab3cf06658efd9a172ce3a674b887bd3c79`; #1862 head = `5c20c2e322c5a2bf465b101d843be2f358e7da5a`; #1863 head = `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`; #1869 head = `467913b72f07ed9ee0ebbe3e981682e83753cbce`.

## (a) Familien-Vorarbeits-Akten — Bestand auf plan main

- PRESENT: `evidence/w376-0428-273-1819pre/akte.md`, `evidence/w377-0428-329-1861pre/akte.md` (Kommit 87a574948), `evidence/w380-0428-312-1860pre/akte.md`.
- GEMELDET (nicht erfunden), Mission nannte falsche Pfade:
  - w378-0428-299-1863pre: die Akte existiert, aber auf einem ANDEREN Pfad und UNCOMMITTED im geteilten Plan-Checkout: `baseharbor-plan/evidence/2026-11-27/0428-299/w378-0428-299-1863pre.md` (`git status --porcelain` => `?? evidence/2026-11-27/`). NICHT auf origin/main. Inhalt gelesen (siehe (b)); Publishing steht aus.
  - w379-0428-318-1862pre: die Akte war bei Schichtbeginn uncommitted im geteilten Checkout (`?? evidence/w379-0428-318-1862pre/`); INZWISCHEN von Lane w379 selbst auf main publischt (main-Kommit `9757bb969`). Inhalt identisch zur hier gelesenen Fassung; Fundstellen (b)(5) gelten. Damit sind beide Familien-Akten (w378 und w379) analysierbar; die w378-Akte bleibt uncommitted im geteilten Checkout und ist dort NICHT angefasst worden.
  - w381-0428-328-1869pre: bei meinem Scan FEHLTE die Akte vollständig (kein Pfad auf main, kein uncommitted Fund). INZWISCHEN publiziert (main `e5a87f25e`, author `w381-0428-328-1869pre`) — aber in der WRONG ZONE: Pfad `w381-0428-328-1869pre-plan/evidence/w381-0428-328-1869pre/akte.md` statt `evidence/w381-0428-328-1869pre/akte.md`. Befund an den Coordinator: umziehen (content-identisch, nur Pfad). Inhalt fuer (c) ausgewertet; #1869 ist eine ANDERE Fehlerklasse (release-label `pr-gate-map-v1.json`, Owner-Freigabe laut ihrer Akte :13,:101,:111), kein Zeilenbedarfler fuer #136.

## (b) Geforderte Quellen (namentlich + Fundstelle)

Die sieben Zeilen, die plan #136 laut PR-Body und Karte 0428-359 (`tasks/t-20261126-trusted-catalog-baseline-recovery-manifest.md` auf `origin/pr-136`, Abschnitt "Required catalog rows") als develop-Baseline verlangt, mit Ursprung:

- `internal/applicationbackup/recovery_manifest_workload_test.go` (#1860) — Fundstellen: `evidence/w380-0428-312-1860pre/akte.md:95` (ValueError-Zitat) und `:108-121` (Einfuegepunkt "nach scripts/pr-gate-coverage.json:2718", content-Block :112-120). Achtung: die Mission schreibt `internal/applicationbackup_recovery_manifest_workload_test.go` — dieser Pfad existiert nicht; korrekt ist `internal/applicationbackup/recovery_manifest_workload_test.go` (Datei existiert auf #1860-head; `git diff --name-only origin/develop...057ce8c55` = genau `internal/applicationbackup/recovery_manifest_workload_test.go` + `scripts/pr-gate-coverage.json`).
- `internal/runtime/repository_volume_inventory.go` + `internal/runtime/repository_volume_inventory_test.go` (#1861, Akte 87a574948) — Fundstelle `evidence/w377-0428-329-1861pre/akte.md:80-87` (ValueError nennt alle drei Pfade + abgeleitete IDs) und `:91` (321 components, keine der drei present).
- `cmd/baha/app_destroy_volumes_recovery_backup_test.go` (#1861) — dieselbe Fundstelle `akte.md:81`; diff-Bestaetigung: `git diff --name-only origin/develop...ade7dab3c` = genau diese drei Pfade (#1861 aendert den Katalog NICHT kandidatenseitig).
- `internal/runtimeexecutor/compose.go` + `internal/runtimeexecutor/compose_test.go` (#1862) — Fundstelle uncommitted `evidence/w379-0428-318-1862pre/akte.md:56` (ValueError) und `:67-68` (abgeleitete IDs).
- `internal/stableid/lock_probe.go` + `internal/stableid/lock_probe_platform_test.go` (#1863) — Fundstelle uncommitted `evidence/2026-11-27/0428-299/w378-0428-299-1863pre.md:43` (ValueError) und `:53-54` (die zwei Zeilen).
- `cmd/baha/app_init_runtime_permission_scope_test.go` mit `runtime_specific` (#1863/#1864) — BEFUND (siehe (c) Zeile 8): die Datei ist auf develop bereits katalogisiert (`baseharbor/scripts/pr-gate-coverage.json:2736-2737` auf develop `ea5218d72`), aber OHNE `runtime_specific`-Feld; sie ist in KEINEM der Familien-PRs geaendert (nicht im Diff `origin/develop...0eafa9f5`). Die Mission fuehrt sie "namentlich" als Familienquelle — das ist faktisch falsch; #1863 aendert nur die zwei stableid-Quellen. #1864 (`evidence/2026-11-28/w247-0428-285-1820hop.md`, `evidence/2026-11-27/w372b-...`) ist eine 1820-Hop-Akte, kein Zeilenbedarfler.
- Zusatzbefund: die sieben geforderten Zeilen sind NICHT das, was #136 selbst aendert — siehe (c).

## (c) Vergleich mit dem, was #136 auf seinem head liefert

Methodik: `gh pr diff 136` scheitert an GitHub 406 (>300 files) — Zeug `git -C baseharbor-plan diff --name-only origin/main...origin/pr-136`: 577 Dateien, ausschliesslich `tasks/`, `releases/`, `epics/`, `evidence/`, `views/`, `roadmap*`; KEINE einzige Produkt-Datei (plan main hat per Konstruktion keinen `scripts/pr-gate-coverage.json`). Der PR-Body selbst bestaetigt: die sieben Zeilen sind als separates catalog-only PRODUKT-PR zu develop zu publizieren ("published together by a separate catalog-only product PR to develop"); #136 liefert die Karte/Spec dieser Zeilen, nicht die Zeilen. `fe586a8da` (letzter bekannter #136-Content-Stand) ist Ancestor von `c4e440017` (getestet via `git merge-base --is-ancestor`).

Gap-Tabelle: geforderte Quelle -> Status in/#136 -> Fundstelle (develop-Katalogzeilen-nummern auf `ea5218d72`; "Zeile" = components-Eintrag in baseharbor `scripts/pr-gate-coverage.json`):

| # | Quelle (develop-Katalog Zeile fehlt/da) | Klasse | Fundstelle |
|---|---|---|---|
| 1 | internal/applicationbackup/recovery_manifest_workload_test.go | (ii) fehlt in develop; NICHT in #136 (plan-only); (iii) kandidatenseitig in #1860: ja | develop grep 0 Treffer; #1860 head `scripts/pr-gate-coverage.json:2720-2721` (diff `origin/develop...057ce8c55` M auf dieser Datei); w380-Akte :108 |
| 2 | internal/runtime/repository_volume_inventory.go | (ii) fehlt in develop; nicht in #136; (iii) NICHT kandidatenseitig (#1861 aendert den Katalog nicht) | develop grep 0 Treffer; `git diff --name-only origin/develop...ade7dab3c` ohne pr-gate-coverage.json; w377-Akte :91 |
| 3 | internal/runtime/repository_volume_inventory_test.go | wie Zeile 2 | wie Zeile 2 |
| 4 | cmd/baha/app_destroy_volumes_recovery_backup_test.go | (ii) fehlt in develop; nicht in #136; (iii) NICHT kandidatenseitig | develop grep 0 Treffer; Datei nur im #1861-Diff |
| 5 | internal/runtimeexecutor/compose.go | (ii) fehlt in develop; nicht in #136; (iii) NICHT kandidatenseitig | develop grep 0 Treffer; #1862-Diff = nur die zwei compose-Dateien; w379-Akte :65 |
| 6 | internal/runtimeexecutor/compose_test.go | wie Zeile 5 | wie Zeile 5 |
| 7 | internal/stableid/lock_probe.go | (ii) fehlt in develop; nicht in #136; (iii) kandidatenseitig in #1863: ja | develop `git grep stableid origin/develop -- scripts/pr-gate-coverage.json` => 0 Treffer; #1863 head `scripts/pr-gate-coverage.json:2536-2537` (insertiert 2536-2545); w378-Akte :51 |
| 8 | internal/stableid/lock_probe_platform_test.go | wie Zeile 7 (kandidatenseitig :2544-2545) | wie Zeile 7 |
| 9 | cmd/baha/app_init_runtime_permission_scope_test.go | FEHLERHAFTE Anforderung der Mission: auf develop PRÄSENT (`pr-gate-coverage.json:2735-2741`, id-Zeile :2736), aber ohne `runtime_specific: true`; in keinem #18xx-Diff; nicht in #136 | develop-Zeugen oben; #1863-Diff enthaelt die Datei nicht |

Ergebnis in den Mission-Klassen: (i) schon in #136: KEINE der Zeilen (und keine Zeile kann in #136 sein — #136 ist plan-only); (ii) fehlen: alle acht Familien-Quellen (7 Karten-Zeilen + die eine feld-Korrektur, s. Owner-Satz); (iii) irrtuemlich kandidatenseitig gefuehrt: #1860 (`pr-gate-coverage.json:2720` auf head `057ce8c55`) und #1863 (`pr-gate-coverage.json:2536-2545` auf head `0eafa9f5`); #1861 und #1862 fuehren KEINE kandidatenseitigen Katalogzeilen — Befund gegen die verbreitete Annahme.

## (d) Schluessel, den das Gate erwartet (nur festgehalten)

- Fail-Punkt: baseharbor `scripts/pr-gate-plan.py:1952-1954` (raise-Statement) innerhalb des Guards ab `:1949` — `source_unowned = [p for p in unowned if p.startswith('cmd/') or p.startswith('internal/')]`; `raise ValueError('invalid trusted PR gate coverage catalog: ' + _coverage_module().unresolved_source_error(source_unowned))` (Datei insg. 2063 Zeilen). Basis des unowned-Setzes: `scripts/pr-gate-plan.py:1846-1848` — die Quelle gilt als katalogisiert, wenn sie als `path` in `components` ODER `packages` des Dokuments erscheint.
- IDs werden NICHT im Planner definiert, sondern aus dem Pfad abgeleitet: `source.<pfad-mit-underscores>` laut `unresolved_source_error`-Ausgabe (z.B. w377-Akte :81-83).
- Validierung der components-Form: baseharbor `scripts/validate-pr-gate-coverage.py:102` — jede component-Zeile braucht `id` (gegen `source\.(\w+)\.go`), `path` und `surfaces` (Pflichtfelder `{'id','path','surfaces'}`); `runtime_specific` ist als optionales Flag beruecksichtigt (`:189,:201,:225`), aber NICHT strukturell erzwungen — die Karte verlangt es inhaltlich ("required so the resolver does not collapse the Podman sibling", `tasks/t-20261126-trusted-catalog-baseline-recovery-manifest.md` Acceptance), und die develop-Zeile 9 (permission scope) zeigt den Fall ohne das Flag.
- Der "gate catalog: no gate with id ..."-Fehler aus w377/w379-Akten stammt NICHT aus baseharbor/scripts/*.py (`grep -rln 'gate catalog:' baseharbor/scripts/` => leer; auch ecosystem-weit nur in plan-task-Notizen: `baseharbor-plan/tasks/t-20261123-gate-catalog-residual-unblock-prs.md`) — Fundstelle dieser Zitate ist die jeweilige Job-Log-Ausgabe eines frueheren Laufs; fuer die Gegenwart massgeblich ist der ValueError-Pfad oben.

## (e) Was der Owner als naechstes in #136 ergaenzen muss (ein Satz)

#136 bleibt der richtige Ort fuer die Spec: die Karte 0428-359 muss in ihrem Required-catalog-rows-Block die achte develop-Aenderung ergaenzen — das Feld `"runtime_specific": true` am vorhandenen develop-Eintrag `source.cmd_baha_app_init_runtime_permission_scope_test_go` (`baseharbor/scripts/pr-gate-coverage.json:2736-2741`) — und klarstellen, dass die sieben Zeilen selbst NIE in #136 landen koennen (plan main fuehrt das Produktcatalog-Datei nicht), sondern nur via das separate catalog-only Produkt-PR, das #136 vorschreibt.

## (f) Befund Kartenname

Die Mission nennt "Karte 0428-359 existiert nicht als Karte": korrekt auf origin/main (`ls tasks/` => kein 0428-359-File); sie existiert als `tasks/t-20261126-trusted-catalog-baseline-recovery-manifest.md` (card_number 0428-359) erst im #136-head. Karte 0428-275 existiert nicht als Nummer: die Nummer 0428-275 traegt laut Frontmatter die Datei `tasks/t-20261124-gate-catalog-baseline-0428-270.md` (`card_number: "0428-275"`, title "add #1820-sib catalog rows" — andere Quellenfamilie); die #136-Karte heisst 0428-359. PR-Identitaet im Lane-Namen ist damit begruendet.

## Cleanliness

- Keine Container/compose gestartet (pure Analyse; `docker ps -a` nicht einschlägig — keine docker-Kommandos dieser Lane).
- Kein Push an baseharbor; kein hosted run; kein Merge; keine `.github/**`-, keine Kartenfeld- oder View-Editen; nur read-only fetches in den geteilten baseharbor-Checkout (lokale bookkeeping-refs `refs/lane/1860` und `refs/cand/*`; kein Remote wurde dadurch veraendert) und dieses isolierte plan-worktree.
- Fremd-Worktrees unangetastet; die Fremd-Akten (w378 uncommitted im geteilten Checkout, w379/w381 auf main) wurden NUR gelesen, nicht veraendert.
- MAIN-REWIND-BEFUND an den Coordinator (wichtige Wahrheit, nicht von dieser Lane verursacht): main wurde zweimal zurueckgesetzt. (i) Mein Squash-Merge von PR #190 landete zuerst auf `e5a87f25e` (parent 9757bb969, enthielt die w381-Akte); eine fremde force-push (`forced-update`, reflog origin/main@{0..1}) ersetzte es durch `b43d5b83b` (parent ef0bcfbcf) und LOESCHTE damit die w381- und w379-Akten von main; danach kehrte 9757bb969 (w379) zurueck und w381 wurde erneut als `e4b0735bd` gepusht — diesmal in die WRONG ZONE (Pfad Praefix `w381-0428-328-1869pre-plan/`). Beide Akten sind jetzt wieder auf main; der w381-Pfad muss bereinigt werden. Zeugen: `git -C baseharbor-plan reflog origin/main` (fetch entries: e4b0735bd forced-update, e5a87f25e fast-forward, 9757bb969 storing head) und `git ls-remote ... refs/heads/main` = e4b0735bd. Diese Lane hat KEINEN force-push und KEIN rewind durchgefuehrt.

## 4-Feld

- Lane: w383-0428-275-136rows
- Karte: 0428-359 (via #136) / 0428-275-Befund (Nummer gehoert zu t-20261124-gate-catalog-baseline-0428-270)
- Repo/PR: baseharbor-plan #136 @ head `c4e4400174dc3fe5c04082c7c85483db9b82543f`; Produktzaehlen gegen develop `ea5218d72`
- Status: END_DONE (Gap-Liste fertig, alle Fundstellen belegt, fehlende Akten gemeldet)

END_DONE w383-0428-275-136rows: #136 liefert nul Zeilen (plan-only), 8 geforderte Quellen fehlen auf develop, 2 falsch kandidatenseitig gefuehrt (#1860 :2720, #1863 :2536), permission_scope bereits auf develop ohne runtime_specific; w378-Akte uncommitted, w379- und w381-Akten inzwischen auf main (w381 in wrong zone unter `w381-...-plan/`).
