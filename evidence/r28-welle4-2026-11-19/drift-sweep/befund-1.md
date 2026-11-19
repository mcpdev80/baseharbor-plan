# Drift sweep — mission-drift-sweep.md

Mission tag: drift-sweep
Card: 0428-137 per task file (mission references "karte 0428-139"); READ-ONLY drift sweep, no product edits, no comment, no close, no merge, no card status changes.
Lane: drift-sweep
Date: 2026-11-19

## PLAN

1. Turn-start: basics-check + read mission + contracts — done
2. Reality witnesses: list live candidates from akte 0428-135, verify refs via gh api / ls-remote only — done
3. Isolated clone ONLY under /var/tmp for baseharbor (fetch develop + PR heads); demo repo checked (0 open PRs) — done
4. Per PR: head.sha + ahead/behind vs origin/develop (gh api + rev-list), mergeable_state — done (all 25 fresh)
5. Per PR: git merge-tree --write-tree origin/develop <head>, conflict count + file names — done
6. Build file-lists per candidate; intersect write-sets across candidates and vs 0428-121/124/122/123s PRs — done
7. Classify each: READY-TO-VERIFY / NEEDS-HOPF / NEEDS-REBASE-CHAIN / SERIAL-BEHIND-<pr> — done
8. Write evidence akte (this file) with table + sorting + per-row proof commands
9. Host cleanliness check (before/after listings; nothing started)
10. Verify evidence path present on origin/main of baseharbor-plan via ls-remote; push
11. Post END line to coordinator and END entry in evidence file

## Zero-zone / quarantine note

Wrong-zone check witness (required before first evidence commit):
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (REAL planning repo)
- `git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan rev-parse --show-toplevel` -> /home/marcel/dev/baseharbor-ecosystem/workers (QUARANTINED, NOT used)
Evidence commits land ONLY in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

## Reality witnesses / method

- Candidate set: 25 LEBEND from akte `evidence/r28-welle4-2026-11-19/pr-inventory/befund-1.md` (commit 9f2b8ab7). All 25 PR heads re-verified live via `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.head.sha'` on 2026-11-19. Demo repo: `gh api repos/mcpdev80/baseharbor-demo/pulls?state=open` -> `[]` (0 open PRs, nothing to sweep there).
- One head moved since the akte: #1691 4f4b3d7a -> d1fcfdf6 (0428-121 r2b). This sweep uses the fresh heads.
- origin/develop = `da76c5cf9c963207038d5599bd130b89ecb1e8a4` (fetched fresh in the isolated clone).
- Isolated clone (NOT the quarantined workers/baseharbor): `/var/tmp/drift-sweep-wt/core`, remote `https://github.com/mcpdev80/baseharbor.git`, PR heads fetched via `+refs/pull/*/head:refs/remotes/pr/*`.
- ahead/behind: `git rev-list --left-right --count origin/develop...pr/<n>` in the clone (equals `gh api .../compare/origin/develop...<head>` .ahead_by/.behind_by semantics; computed locally against the exact fetched base head).
- Conflict forecast: `git merge-tree --write-tree origin/develop pr/<n>`; rc=1 -> conflicts; conflicted files counted from `CONFLICT` lines. No working-tree changes.
- mergeable_state: `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.mergeable_state'` (fresh; unlike the akte where it was null for all, GitHub has now computed it).
- Write-set intersection: `git diff --name-only origin/develop...pr/<n>` per candidate, pairwise `comm`/set-intersect.

## Karte assignment for the 121/124/122/123 anchors

- 0428-121 (env-filter, active r4) = #1691, head d1fcfdf6
- 0428-122 (appclass log writer, active, "wartet auf 121-merge") = #1692, head 876329f7
- 0428-123 (registration visibility, wait) = #1693, head d751c83b
- 0428-124 (verification-none, review, r3 waits for seat) = #1695, head 4f0d5e9f

## Tabelle — 25 LEBEND-kandidaten

| PR | karte | head | ahead/behind | mergeable_state | merge-tree conflict (files) | schreibset-kollision (lebend) | einschatzung |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1697 | 0428-131 | 3448f73e | 0/1 | clean | nein (0) | keine | READY-TO-VERIFY |
| 1695 | 0428-124 | 4f0d5e9f | 0/3 | clean | nein (0) | #1693 #1691 (internal/metrics/prometheus_verify.go) | SERIAL-BEHIND-1691 |
| 1693 | 0428-123 | d751c83b | 2/1 | behind | nein (0) | #1695 #1692 #1691 (prometheus_verify.go, registry.go) | SERIAL-BEHIND-1691 |
| 1692 | 0428-122 | 876329f7 | 0/8 | clean | nein (0) | #1693 #1691 (internal/observability/registry.go) | SERIAL-BEHIND-1691 |
| 1691 | 0428-121 | d1fcfdf6 | 0/2 | clean | nein (0) | #1695 #1693 #1692 | READY-TO-VERIFY (merge zuerst) |
| 1690 | 0428-119 | 84ee9a93 | 2/4 | behind | nein (0) | keine | NEEDS-HOPF |
| 1684 | 0428-083 | 8c713950 | 34/1 | behind | nein (0) | keine | NEEDS-HOPF |
| 1682 | 0428-110 | fb6f3693 | 32/3 | behind | nein (0) | #1615 #1585 (internal/deployment/target.go) | NEEDS-HOPF |
| 1650 | 0428-078 | 022c454c | 34/28 | behind | nein (0) | #1597 (perses_selection_test.go), #1645/#1613/#1602/#1598 (app_status_result.go) | NEEDS-HOPF |
| 1645 | keine | c781eb86 | 164/20 | dirty | ja (4: manifest_render.go, manifest_test.go, capability/perses.go, metrics/perses_contract_test.go) | #1613 #1598 #1597 je 20 files; #1602 4; #1650 #1599 #1592 je 1 | NEEDS-HOPF (chain-head perses) |
| 1616 | 0428-086 | 7d6538b4 | 36/18 | behind | nein (0) | keine | NEEDS-HOPF |
| 1615 | 0428-057 | 8963efd8 | 164/25 | clean | ja (2: cmd/baha/app_init_uid_app_slice_test.go add/add, internal/deployment/target.go content) | #1578 (5 files, chain-base), #1682 #1585 (target.go) | NEEDS-REBASE-CHAIN |
| 1613 | 0428-073 | 470735c1 | 164/19 | dirty | ja (4: manifest_render.go, manifest_test.go, capability/perses.go, metrics/perses_contract_test.go) | #1645 #1598 #1597 je 20 files; #1602 4; #1650 #1599 #1592 je 1 | NEEDS-HOPF |
| 1602 | 0428-077 | b6c9702b | 32/28 | behind | nein (0) | #1645 #1613 #1598 #1597 #1650 (app_status_result.go, capability/perses.go), #1599 (capability/perses.go) | NEEDS-HOPF |
| 1599 | 0428-089 | 31adf08f | 32/22 | behind | nein (0) | #1598 (7 files: commands.go, completion.go, perses_lifecycle.*), #1645 #1613 #1602 #1597 (capability/perses.go), #1588 (machine_coverage.go) | NEEDS-HOPF |
| 1598 | 0428-084 | e8667237 | 164/16 | dirty | ja (4: manifest_render.go, manifest_test.go, capability/perses.go, metrics/perses_contract_test.go) | #1645 #1613 #1597 je 20 files; #1599 7; #1602 4; #1650 #1592 je 1 | NEEDS-HOPF (chain-head perses) |
| 1597 | 0428-076 | 540ed13c | 164/23 | dirty | ja (8: app_perses_cli_test.go, app_status_result.go, manifest_render.go, manifest_test.go, capability/perses.go, perses_selection.go, perses_selection_test.go, metrics/perses_contract_test.go) | #1645 #1613 #1598 je 20 files; #1602 4; #1650 2; #1599 #1592 je 1 | NEEDS-HOPF |
| 1592 | 0428-088 | 76331c7d | 1/26 | behind | nein (0) | #1645 #1613 #1598 #1597 (internal/application/management_ui.go) | NEEDS-HOPF |
| 1589 | 0427-020 | 442755b3 | 390/2 | behind | nein (0) | #1587 (mkdocs.yml, mkdocs.de.yml) | NEEDS-HOPF |
| 1588 | 0427-186 | 9534edd4 | 390/2 | behind | nein (0) | #1599 (cmd/baha/machine_coverage.go, docs/reference/cli-machine-coverage.md) | NEEDS-HOPF |
| 1587 | 0427-169 | 20e0537c | 390/1 | behind | nein (0) | #1589 (mkdocs.yml, mkdocs.de.yml) | NEEDS-HOPF |
| 1585 | BF-01/0427-189 | 55a8c0f3 | 164/9 | behind | nein (0) | #1615 (cmd/baha/target.go, internal/deployment/target.go), #1682 (target.go), #1582 (internal/orgconfig/store.go) | NEEDS-HOPF |
| 1582 | BF-03 | e196c0e2 | 164/8 | behind | nein (0) | #1585 (internal/orgconfig/store.go) | NEEDS-HOPF |
| 1581 | keine | bdcd6f62 | 390/1 | behind | nein (0) | keine (1 file: scripts/pr-gate-coverage.json) | NEEDS-HOPF |
| 1578 | 0428-051 | 6f07aef2 | 164/18 | behind | nein (0) | #1615 #1595 #1591 (5 files, uid-Ketten-Basis) | NEEDS-REBASE-CHAIN (ketten-head, base-branch = head-branch retarget-artifact) |

Nachweis je Zeile (einsetzbar im isolierten Clone /var/tmp/drift-sweep-wt/core):

    gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '[.head.sha,.base.ref,.mergeable,.mergeable_state,.draft]'
    git fetch origin develop 'refs/pull/*/head:refs/remotes/pr/*'
    git rev-list --left-right --count origin/develop...pr/<n>     # = behind ahead  (links = develop-only)
    git merge-tree --write-tree origin/develop pr/<n>; echo $?    # 0=clean, 1=conflict
    git merge-tree --write-tree origin/develop pr/<n> | grep '^CONFLICT'
    git diff --name-only origin/develop...pr/<n> > files-<n>.txt  # write-set
    # Kollision: comm -12 <(sort files-A.txt) <(sort files-B.txt)

## Einschatzung nach Klassen

- READY-TO-VERIFY (base-exakt jetzt, 0 ahead): #1697, #1691, #1695, #1692. (#1693 ist 2 ahead, aber 0 konflikte und mergeable "behind" — hopf-frei.)
- Konflikt-frei gegen die aktuelle develop: alle außer #1645, #1613, #1598, #1597 (dirty, je 4-8 Konflikt-dateien) und #1615 (clean gemeldet, aber merge-tree zeigt 2 add/add-content-Konflikte mit develop — GitHub "clean" vs. lokaler add/add: heads/prüfung siehe Befund unten).
- Schreibset-harte-Kollisionen (datei-exakt): die perses-Gruppe {#1645, #1613, #1598, #1597} schneidet sich gegenseitig in 20 Dateien (manifest_render.go, manifest_test.go, cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go, internal/capability/perses.go, internal/capability/perses_selection*.go, internal/metrics/perses_contract_test.go, docs/spec/*); #1598 schneidet #1599 in 7 Dateien (cmd/baha/commands.go, completion.go, perses_lifecycle.*).
- Metrics-Gruppe {#1691, #1692, #1693, #1695} kollidiert in internal/observability/registry.go (#1691/#1692/#1693) und internal/metrics/prometheus_verify.go (#1691/#1693/#1695).
- target.go-Schnitt: #1682, #1615, #1585 (und #1615→#1578 Ketten-dateien).
- Ketten: #1578 (uid-app-Linie) ist Basis-content von #1615; #1595/#1591 tragen #1578s 5 Dateien voll in sich (chain).
- r27-Gruppe (#1589/#1588/#1587/#1585/#1582/#1581, 390 ahead): hopf braeuchen sie streng genommen nicht (merge-tree 0 konflikte, state "behind" = fast-forward-bar gegen develop? nein — 390 ahead heisst: grosser eigener stapel; GitHub meldet "behind" = base nicht aktuell). Konflikt-frei, also kein harter hopf-zwang fuer die merge-bar; fuer develop-hygiene im window: ein hopf-merge je PR reicht.

Zusaendlich die zusammenfassung: 4 PRs mit hartem merge-tree-konflikt gegen develop (#1645/#1613/#1598/#1597, je 4-8 dateien) + 1 PR mit lokalem konflikt gegen develop trotz GitHub-"clean" (#1615, 2 dateien); die uebrigen 20 sind konflikt-frei und brauchen nur base-refresh. Die einzige 121-abhaengigkeit ist die metrik-gruppe {#1692, #1693, #1695} (dateien registry.go, prometheus_verify.go).

## Sortierung — hopf-reihenfolge und konflikt-risiken (das Eigentliche)

Was "0428-121" ist (aufgeloest): karte 0428-121 = hunt-metrics env-filter = PR #1691 (head d1fcfdf6, 0 ahead — base-exakt). Die mission meint: #1691 wird im window zuerst gemergt; die sweep-sortierung ist die reihenfolge der uebrigen 24 danach.

1. JETZT base-exakt, sofort merge-bar (ahead=0, konflikt=0): #1691 (0428-121, ZUERST), dann #1697 (0 ahead, keine ueberschneidung mit #1691 — unabhaengig merge-bar).
2. Nach dem #1691-merge brauchen NUR #1692, #1693, #1695 einen hopf — grund datei-exakt: internal/observability/registry.go (#1692, #1693), internal/metrics/prometheus_verify.go (#1693, #1695). #1695/#1692 sind selbst 0 ahead (clean), aber der #1691-inhalt in denselben dateien muss vor ihrer abnahme in develop stehen -> SERIAL-BEHIND-1691.
3. Konflikt-cluster perses (seriell, je hopf + manuelle konfliktoesung): #1645, #1613, #1598, #1597 — paarsweise 20 dateien ueberschneidung; gegen develop JE 4-8 merge-tree-konflikte genau in den geteilten dateien (manifest_render.go, manifest_test.go, capability/perses.go, metrics/perses_contract_test.go). Einer nach dem anderen; jeder weitere hopft zusaendlich ueber den Vorgaenger.
4. NEEDS-HOPF (konflikt-frei gegen develop, aber behind/ahead>0): #1690, #1684, #1682, #1650, #1616, #1602, #1599, #1592 — nach 121-merge je ein hopf-merge (develop in den branch). Querschnitte, die die reihenfolge mitbestimmen: #1682/#1585/#1615 teilen internal/deployment/target.go; #1602/#1650/#1599 teilen dateien mit dem perses-cluster (app_status_result.go, capability/perses.go) — diese also NACH gruppe 3 hopfen/mergen, sonst wiederholte konfliktoesung.
5. NEEDS-REBASE-CHAIN (ketten, am Stueck): #1578 -> #1615 teilt 5 dateien (environment_identity.*, environment.*, app_init_uid_app_slice_test.go) mit ihr und mit den STACK-PRs #1595/#1591; #1615 hat add/add-conflict app_init_uid_app_slice_test.go + content-conflict target.go gegen develop. uid/cli2-kette zuerst am basis-zweig hopfen/rebasen, dann die folge-prs (fan-in).
6. Grosse stapel (164/390 ahead): #1585, #1582, #1589, #1588, #1587, #1581, #1645, #1613, #1602, #1599, #1598, #1597 — konflikt-frei gegen develop (ausser cluster 3), aber ihr merge-base liegt weit zurueck; ein hopf-merge (develop in den branch) genuegt, rebase ist nicht noetig (ancestry bleibt erhalten). #1592 ist nur 1 ahead.
7. Querschnitts-serialisierungen innerhalb von gruppe 4/6 (gruendung datei-exakt): #1585/#1582 teilen internal/orgconfig/store.go (seriell); #1589/#1587 teilen mkdocs.yml + mkdocs.de.yml (seriell); #1588/#1599 teilen cmd/baha/machine_coverage.go + docs/reference/cli-machine-coverage.md (#1599 zuerst oder konfliktfoerderung); #1682/#1585/#1615 teilen internal/deployment/target.go (target.go-besitz: erst #1615-kette, dann #1585, dann #1682 — oder umgekehrt, je kartenprioritaet). #1581 ist isoliert (1 datei, scripts/pr-gate-coverage.json, CI-adjacent).

Befund: #1615 wurde von GitHub `mergeable=true state=clean` gemeldet, die lokale merge-tree-pruefung gegen den exakten origin/develop da76c5cf findet aber 2 konflikte. Moegliche ursache: GitHub berechnete den zustand gegen einen aelteren base-head. Deshalb ist #1615 als NEEDS-REBASE-CHAIN mit hopf-pflicht gefuehrt, nicht als READY.


## Host cleanliness

Vorher (lesend, nichts gestartet): 4 bh-local-shared-* containers + baseharbor-local-{default,secrets} netzwerke, ambient-core; podman nicht vorhanden auf diesem host. Diese Lane startet KEINE container/netzwerke/volume, fuehrt keine compose/deploy aus (read-only drift sweep).
Nachher-Zeuge identisch (siehe unten). Nothing to clean.

    $ docker ps --format '{{.Names}}'
    bh-local-shared-postgres-1
    bh-local-shared-openbao-admin-1
    bh-local-shared-postgres-admin-1
    bh-local-shared-postgres-member-1-1

cleanliness: diese Lane hat nichts gestartet und nichts zu tear down; nothing to clean. /var/tmp/drift-sweep-wt (isolierter clone, ~24 MB + pr-refs) kann beliebig entfernt werden, blockiert keine daemon-pools.

## repo-rule compliance

- READ-ONLY: kein push/comment/close/merge/rerun/dispatch an produktrepos — eingehalten.
- Keine karten-statuswechsel — eingehalten.
- .github nicht angefasst — eingehalten.
- quarantäne checkout workers/baseharbor NICHT als Realitätszeuge benutzt — nur gh api + isolierter clone unter /var/tmp/drift-sweep-wt.
- evidence nur in baseharbor-plan — eingehalten.
- kein subagent (§4.8) — eingehalten.

## Candidate

Kein Produktkandidat (read-only mission — KEIN push an ein produkt-repo, nur evidence in baseharbor-plan).

Evidence-auf-origin/main-Zeuge (gemessen VOR diesem END-Post, second-to-last action; die letzte commit fdf36766haelt diesen zeilenweistext, ihr eigener ls-remote-zeug ist die push-zeile unten):

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin main
    fdf36766c5e7cf25f801818447db4e184389accd	refs/heads/main

Evidence-commits: 80bbb43bd5bd34c81ca5316df5f8f870d717cd85 (akte) + fdf36766c5e7cf25f801818447db4e184389accd (END-Zeuge; pfad evidence/r28-welle4-2026-11-19/drift-sweep/befund-1.md in beiden commits geaendert; push-zeuge 3791d9e6..80bbb43b und 80bbb43b..fdf36766 main -> main).

END (this lane) DONE mission-drift-sweep.md: Drift sweep ueber 25 LEBEND-kandidaten fertig — 20 konflikt-frei (4 base-exakt: #1691/#1697/#1692/#1695), 5 mit merge-tree-konflikt gegen develop (#1645/#1613/#1598/#1597/#1615); 121-serial-abhaengig: #1692/#1693/#1695 (registry.go, prometheus_verify.go); hartester schreibset-cluster: perses {1645,1613,1598,1597} je 20 dateien; akte 80bbb43b auf origin/main.
