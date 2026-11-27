# w390-0428-216-prhopcensus — HOP-PLAN (read-only, Folgeauftrag)

**Lane:** w390-0428-216-prhopcensus · **Karte:** 0428-216 · **Repos:** baseharbor + baseharbor-demo
**Art:** Hop-Plan für die 9 NOT-ancestor-PRs aus der Census. Read-only, KEIN push/merge/run.
**Zeitpunkt:** 2026-11-27

## Scope-Compliance

- Read-only: kein Produkt-Push, kein PR-merge/close/edit, kein workflow_dispatch, keine Karten-Felder, keine generierten Views, kein lokaler Testlauf.
- Reiner Befund + Plan; die eiglichen Hops sind Coordinator-/Codex-Aktion (Owner: nur Coordinator schließt PRs).
- Plan-Repo FREEZE: Akte als DATEI im eigenen worktree, END meldet PFAAD + SHA256 statt main-sha.
- Remote-Wahnheit nur via `gh api` + ein throwaway `--filter=blob:none`-Klon unter /tmp (kein scratch im ecosystem-root, kein workers/baseharbor-plan).
- Remote-Attestation: planning `origin -> https://github.com/mcpdev80/baseharbor-plan.git`; baseharbor-worktree `origin -> https://github.com/mcpdev80/baseharbor.git`.
- Develop-Köpfe: baseharbor develop = `ea5218d72e263f21e79853b679af50074dab8c25`, demo develop = `58ac70679efe5f7e95bd47d602841704fb9ffa67`.

## Korrektur: 17 offene PRs (nicht 16)

Gemessen mit `gh pr list --repo <repo> --state open --limit 60 --json number | jq length`:
- baseharbor = **14**, demo = **3**, gesamt = **17** (census-akte hatte demo-#183 fälschlich als verschoben gelesen; demo-#183 head ist heute `335ef5e54c59`, im census `d5b44c46c694` — der PR ist weitergewachsen, aber dev-synced).
- 9 NOT-ancestor (baseharbor) + 2 NOT-ancestor (demo) = 11 offen-hopping, 6 dev-synced (baseharbor: 1863,1862,1861,1860,1812; demo: 183).

## (a) Je NOT-ancestor-PR: head, fehlende develop-Commits (rev-list), merge-base

Berechnet mit `git fetch` der 9 PR-heads + develop in einem blob-filtered Klon, dann `git rev-list --count <head>..origin/develop` über die compare-API (behind_by) + merge_base_commit.

| PR | head (12) | fehlende develop-Commits (rev-list behind_by) | merge-base (12) | klasse |
|---|---|---|---|---|
| 1869 | 467913b72f07 | 18 | 5a37ddbd9a06 | hopfaehig, conflict-free |
| 1868 | 57320af6949e | 18 | 5a37ddbd9a06 | hopfaehig, conflict-free |
| 1866 | 3702c0950220 | 6 | c167fa5dd323 | hopfaehig, conflict-free |
| 1864 | b9675cc0b6dc | 6 | c167fa5dd323 | hopfaehig, conflict-free |
| 1855 | d18e4b367940 | 6 | c167fa5dd323 | hopfaehig, conflict-free |
| 1820 | 8f6b2444bdc9 | 36 | fcd449117e18 | hopfaehig, conflict-free |
| 1819 | b3c5055ad256 | 40 | 28296a2e6e92 | content-superseded durch #1820 |
| 1818 | 20fc1cb7d496 | 76 | 3ebfb90daaf4 | hopfaehig, conflict-free |
| 1650 | 37c4d847ca37 | 26 | ac7c970fe91a | hopfaehig, conflict-free (merge-base = Merge-Commit) |
| demo 179 | cda6aa70e80b | 1 | 5ca92a7cd2f7 | hopfaehig, conflict-free |
| demo 170 | b086cf58bb2f | 1 | 5ca92a7cd2f7 | hopfaehig, conflict-free |

## (b) Klassifikation je PR

### (i) hopfaehig durch `git merge origin/develop` ohne Konflikt — ALL 9 baseharbor + 2 demo

Getestet in einem throwaway `--filter=blob:none`-Klon: `git checkout -B scratch <pr-head>`, `git merge --no-commit --no-ff origin/develop`, `git ls-files -u` (Index-Konflikte) → **0 Konflikte bei allen 11**. Danach scratch branch + in-progress merge zurückgesetzt, kein Push. Kein Konflikt, weil die PRs ausschließlich neue/andere Dateien schreiben und develop die touched Pfade nicht überlappt.

Klasse = **hopfaehig, conflict-free** für: 1869, 1868, 1866, 1864, 1855, 1820, 1818, 1650, demo-179, demo-170.

### (ii) Konflikt zu erwarten — NONE nachgewiesen

Kein PR der 11 erwartet einen Merge-Konflikt mit develop (Index-Konfliktliste leer in allen 11 Fällen). Kein Konflikt-Find nach file:line.

### (iii) content-superseded — #1819 durch #1820 (der census-Befund)

- **PR #1819 (0428-181, head b3c5055ad256) vs PR #1820 (0428-271, head 8f6b2444bdc9): IDENTISCHE content-blobs** über alle 4 geteilten Dateien:
  - `.github/workflows/pre-release-runtime-suite.yml` = 22fa7b392ce29b16…
  - `internal/application/runtime_postgres.go` = b1687ee1558b7066…
  - `internal/metrics/perses_dashboard_provision.go` = 8a10e0942d225805…
  - `internal/metrics/perses_dashboard_provision_test.go` = 370b6f7e4ed95193…
  Titel verschillen ("0428-181 wire Perses identity…" vs "fix(0428-271): prove exact runtime broker commit…"), aber die Go-/Workflow-Beute sind bytegleich. #1820 ist #1819 content-wise überholt → **#1819 schließen (nur Coordinator), oder auf #1820 retargeten**. #1819 ist content-superseded (Nicht-Hopfall).
- **Keine weiteren content-superseded-Paare** unter den 17. Die geteilten merge-bases (5a37ddbd9a06 für 1869/1868; c167fa5dd323 für 1866/1864/1855) sind rein transitiv (gemeinsamer alter develop-Snapshot), kein inhaltlicher Überschneidung. #1866/#1855 teilen nur `scripts/pr-gate-coverage.json` mit DIFFERENTEN blob (1866=4f69f085ab096c97 vs 1855=7ad5586478478136) → kein Superseded.

## (c) Hop-Reihenordnung (vor/nach #183/#136)

Voraussetzung: #1812 (0428-249) ist bereits dev-synced (ancestor YES) und bildet die Basis der Kette.

**Kette #1812 -> #1819 -> #1820 (linear, max. 3 Ebenen nach PR-Disziplin 0.4.28+):**
- #1812 (base, dev-synced) darf HOPPELLOS bleiben.
- #1819 ist content-superseded durch #1820 → #1819 wird GESCHLOSSEN, nicht gehoppt. #1820 (0428-271) ist der Nachfolger auf der Kette; er hoppt auf develop (36 fehlende Commits), erst NACH dem #1812-Merge in der Merge-Reihenfolge der Kette.
- #1820 ist das letzte Glied; der "frühester erlaubter Hop" für #1820 = nach #1812-Merge (Ketten-Ordnung #1812 → #1819 → #1820). Da #1819 content-superseded ist, ist die operative Kette #1812 → #1820.

**Katalog-Zeilen (t-20261121-stale-pr-hop-and-baserefs §Scope):**
- Erlaubt: `git push --force-with-lease` auf Lane-Branches unserer eigenen Karten + `gh pr edit --base` nur bei deklariertem Stack (hier: kein Stack, base=develop korrekt → kein Retarget).
- Verboten: PRs mit Owner-held card (#1614,#1615,#1650/#1606-0428-078,#1731,#1704-0428-073) — #1650 (0428-078) ist Owner-held. **Achtung: #1650 ist in meiner NOT-ancestor-Liste, aber die Karte 0428-078 ist owner-held → #1650 darf NICHH von dieser Lane gehoppt werden; als STATE melden, Hop gehört in den Coordinator-/Owner-Scope.** (In der Akte als Owner-held-Exception vermerkt.)
- Verboten: PRs schließen (./**- und scripts/** Änderungen); nur Coordinator schließt PRs.

**Reihenordnung:**
- **VOR #183/#136 hoppen dürfen** (eigene Karten, kein owner-held, conflict-free): #1869, #1868, #1866, #1864, #1855, #1818, demo-179, demo-170. Linear, keine Ketten-Abhängigkeit untereinander, alle base=develop.
- **NACH #183/#136 (bzw. nach #1812-Merge in der Kette):** #1820 (0428-271), Nachfolger auf #1812-Kette.
- **NICHH von dieser Lane (owner-held / koordinierungsbedürftig):** #1650 (0428-078, owner-held nach §Scope). Hop gehört in den Coordinator-/Owner-Scope.
- **Neu angeschnitten auf develop-Basis** müssten PRs, die nicht hopfaehig sind — hier: KEIN Fall (alle conflict-free), also kein Fresh-cut nötig; #1819 content-superseded statt Fresh-cut.

## (d) Akte-Tabelle (4-Feld w390-0428-216-prhopcensus)

| PR | head | fehlende develop-Commits | merge-base | klasse | frühester erlaubter hop-zeitpunkt |
|---|---|---|---|---|---|
| 1869 | 467913b72f07 | 18 | 5a37ddbd9a06 | hopfaehig conflict-free | sofort (eigene Karte, vor #183/#136) |
| 1868 | 57320af6949e | 18 | 5a37ddbd9a06 | hopfaehig conflict-free | sofort (eigene Karte) |
| 1866 | 3702c0950220 | 6 | c167fa5dd323 | hopfaehig conflict-free | sofort (eigene Karte) |
| 1864 | b9675cc0b6dc | 6 | c167fa5dd323 | hopfaehig conflict-free | sofort (eigene Karte) |
| 1855 | d18e4b367940 | 6 | c167fa5dd323 | hopfaehig conflict-free | sofort (eigene Karte) |
| 1820 | 8f6b2444bdc9 | 36 | fcd449117e18 | hopfaehig conflict-free | nach #1812-Merge (Kette) |
| 1819 | b3c5055ad256 | 40 | 28296a2e6e92 | content-superseded durch #1820 | kein Hop; #1819 durch #1820 schließen (Coordinator) |
| 1818 | 20fc1cb7d496 | 76 | 3ebfb90daaf4 | hopfaehig conflict-free | sofort (eigene Karte) |
| 1650 | 37c4d847ca37 | 26 | ac7c970fe91a | hopfaehig ABER owner-held (0428-078) | NICHH von dieser Lane; Hop in Coordinator-/Owner-Scope |
| demo 179 | cda6aa70e80b | 1 | 5ca92a7cd2f7 | hopfaehig conflict-free | sofort (eigene Karte) |
| demo 170 | b086cf58bb2f | 1 | 5ca92a7cd2f7 | hopfaehig conflict-free | sofort (eigene Karte) |

## Hop-Methode (für den ausführenden Coordinator/Codex, NICHH von dieser Lane ausgeführt)

`git fetch origin develop` + `git fetch origin "+refs/pull/<n>/head:refs/remotes/origin/pr_<n>"`; dann auf dem PR-Branch `git merge --no-commit --no-ff origin/develop` (force-with-lease push), base bleibt develop. Für #1650: re-basen statt nur hoppen (merge-base ac7c970fe91a ist ein Merge-Commit, der 0428-078-Arbeitssitz sitzt auf einem divergenten Basis-Commit).

## END

w390-0428-216-prhopcensus: DONE — read-only hop-plan complete. 17 offene PRs korrigiert (14 baseharbor + 3 demo). 11 NOT-ancestor: 9 baseharbor (1869,1868,1866,1864,1855,1820,1819,1818,1650) + 2 demo (179,170). Alle 11 hopfaehig conflict-free (getestet in throwaway blob-filtered Klon, kein Push). #1819 content-superseded durch #1820 (identische content-blobs). #1650 owner-held (0428-078) → Hop nur im Coordinator-/Owner-Scope. Kette #1812->#1819->#1820: #1820 hoppt nach #1812-Merge.
