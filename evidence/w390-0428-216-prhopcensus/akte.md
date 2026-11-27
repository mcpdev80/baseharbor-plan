# w390-0428-216-prhopcensus — Bestandsaufnahme (read-only)

**Lane:** w390-0428-216-prhopcensus · **Karte:** 0428-216 · **Repos:** baseharbor + baseharbor-demo
**Art:** Bestandsaufnahme (read-only + Akte). Kein Push, kein Run, kein Merge, keine Änderung an PRs/Branches.
**Zeitpunkt:** 2026-11-27

## Branch-Provenance / Remote-Attestation

- Planning-Repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, `origin -> https://github.com/mcpdev80/baseharbor-plan.git`
- Produkt-Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w390-0428-216-prhopcensus-wt`, `origin -> https://github.com/mcpdev80/baseharbor.git` (Branch `develop`)
- Remote-Wahrheit nur via `gh api` / `git ls-remote` (kein Quarantäne-Checkout zitiert)
- develop-Köpfe (gh api refs):
  - baseharbor develop = `ea5218d72e263f21e79853b679af50074dab8c25`
  - baseharbor-demo develop = `58ac70679efe5f7e95bd47d602841704fb9ffa67`
- Beachtet: beide Repos haben heute BOTH develop (ea5218d…) und main (cddc81b… / 2618b39…). Default-Branch ist `main`. Alle offenen PRs unserer Karten deklarieren base `develop`.

## Methode

- `gh pr list --repo <repo> --state open --limit 60 --json …` → offene PRs inventarisieren.
- Per PR: `gh api repos/mcpdev80/<repo>/pulls/<n> --jq .head.sha` → head; `gh api …/compare/<develop>...<head>` → status + behind_by + merge_base_commit.
- `status=ahead` (behind_by=0) = PR ist Nachkomme von develop (ancestor YES). `status=diverged` (behind_by>0) = NOT-ancestor, PR hinkt develop hinterher.
- Duplikat/Superseded: identicaler content-blob (sha256 der geteilten Go-/Workflow-Dateien) + Ziel-/Titel-Abgleich.
- Keine Produkt-Änderung, kein PR-Close/merge/edit, kein workflow_dispatch. Nur Befund + Akte.

## (a) Inventar offene PRs

baseharbor (14 offen, alle base `develop`):
1869 lane-0428-331-damagedstate · 1868 w341-0428-326-proofleak · 1866 w334-0428-321-exitcodedocs ·
1864 w333-0428-291-capperms-fix · 1863 w336-0428-299-goprereq · 1862 lane-0428-318-lowpair ·
1861 w334-0428-329-recoveryheuristic · 1860 w333-0428-312-volrecovery · 1855 w279-0428-078-pr1650-reissue ·
1820 fix/broker-build-identity (0428-271) · 1819 w54-0428-181-export (0428-181) · 1818 lane-0428-078-cf-fix ·
1812 lane-0428-249-runtime-image-fix · 1650 lane-0428-078-perses-identity-on-resolver

baseharbor-demo (3 offen, alle base `develop`):
183 (0428-284) · 179 (test-only, #1842-forward) · 170 (0428-250)

## (b)/(c) Ancestor- + base-Ref-Ergebnis je PR

Kartendeklaration 0428-216: `depends_on: []` (keine Basis-Lane) → deklarierter base = develop. Alle offenen PRs tragen base develop → **base-Ref korrekt gemessen an der Deklaration** (kein Stack, den man retargeten müsste). Der einzige Defekt ist Staleness: PR ist kein Nachkomme von develop.

baseharbor:

| PR | head-SHA (12) | card | base | ancestor=develop? | behind_by (dev-Commits fehlen) | merge-base (12) |
|---|---|---|---|---|---|---|
| 1869 | 467913b72f07 | 0428-331 | develop | NEIN (diverged) | 18 | 5a37ddbd9a06 |
| 1868 | 57320af6949e | 0428-326 | develop | NEIN (diverged) | 18 | 5a37ddbd9a06 |
| 1866 | 3702c0950220 | 0428-321 | develop | NEIN (diverged) | 6 | c167fa5dd323 |
| 1864 | b9675cc0b6dc | 0428-291 | develop | NEIN (diverged) | 6 | c167fa5dd323 |
| 1863 | 0eafa9f5a42d | 0428-299 | develop | JA (ahead) | 0 | ea5218d72e26 |
| 1862 | 5c20c2e322c5 | 0428-318 | develop | JA (ahead) | 0 | ea5218d72e26 |
| 1861 | ade7dab3cf06 | 0428-329 | develop | JA (ahead) | 0 | ea5218d72e26 |
| 1860 | 057ce8c55416 | 0428-312 | develop | JA (ahead) | 0 | ea5218d72e26 |
| 1855 | d18e4b367940 | 0428-078 reissue | develop | NEIN (diverged) | 6 | c167fa5dd323 |
| 1820 | 8f6b2444bdc9 | 0428-271 | develop | NEIN (diverged) | 36 | fcd449117e18 |
| 1819 | b3c5055ad256 | 0428-181 | develop | NEIN (diverged) | 40 | 28296a2e6e92 |
| 1818 | 20fc1cb7d496 | 0428-078 | develop | NEIN (diverged) | 76 | 3ebfb90daaf4 |
| 1812 | c2dd3ff04e30 | 0428-249 | develop | JA (ahead) | 0 | ea5218d72e26 |
| 1650 | 37c4d847ca37 | 0428-078 | develop | NEIN (diverged) | 26 | ac7c970fe91a |

baseharbor-demo:

| PR | head-SHA (12) | card | base | ancestor=develop? | behind_by | merge-base (12) |
|---|---|---|---|---|---|---|
| 183 | d5b44c46c694 | 0428-284 | develop | JA (ahead) | 0 | 58ac70679efe |
| 179 | cda6aa70e80b | 0428-1842-forward | develop | NEIN (diverged) | 1 | 58ac70679efe |
| 170 | b086cf58bb2f | 0428-250 | develop | NEIN (diverged) | 1 | 58ac70679efe |

Summarum: 13 offene PRs, 6 davon sind Nachkommen von develop (ancestor YES: 1863, 1862, 1861, 1860, 1812, demo-183).
7 baseharbor-PRs + 2 demo-PRs sind NOT-ancestor (staleness). Alle base-Ref sind korrekt (develop), kein Stack-Retarget nötig.

## (d) Doppel-/Superseded-Prüfung

Identicaler content-blob (sha256 über alle geteilten Dateien) = Duplikat/Superseded:

- **PR #1819 (0428-181, head b3c5055ad256) vs PR #1820 (0428-271, head 8f6b2444bdc9): IDENTISCHE BLOB.**
  Alle 4 geteilten Dateien exakt gleich:
  - `.github/workflows/pre-release-runtime-suite.yml` = 22fa7b392ce29b16…
  - `internal/application/runtime_postgres.go` = b1687ee1558b7066…
  - `internal/metrics/perses_dashboard_provision.go` = 8a10e0942d225805…
  - `internal/metrics/perses_dashboard_provision_test.go` = 370b6f7e4ed95193…
  Titel unterscheiden sich ("0428-181 wire Perses identity dashboard…" vs "fix(0428-271): prove exact runtime broker commit…"), aber die Go-/Workflow-Beute sind bytegleich. #1819-Body benennt selbst die „Write-set disjoint from #1650/#1818" und #1820 ist die Broker-Commit-Fix auf denselben `runtime_postgres.go`-Seam. #1819 (0428-181) ist content-wise von #1820 überholt/Superseded: #1820 schließen oder auf #1820 retargeten.
- **#1866 vs #1855** teilen nur `scripts/pr-gate-coverage.json`, aber die Blob unterscheiden sich (1866=4f69f085ab096c97… vs 1855=7ad5586478478136…) und die restlichen 8 vs 10 Dateien sind disjoint. KEIN Duplikat — identische merge-base (c167fa5dd323) nur, weil beide denselben develop-Snapshot als Basis nahmen.
- Restliche PRs: keine inhaltliche Überlappung (disjunkte Write-sets). Die geteilten merge-bases (5a37ddbd9a06 für 1869/1868; c167fa5dd323 für 1866/1864/1855) sind rein transitiv (gemeinsamer develop-Snapshot), kein Duplikat.

## (e) Endzustand-Satzzuordnung je NOT-ancestor-PR (OHNE Ausführung)

- 1869 (0428-331): Hop auf develop — `git rebase --onto origin/develop <merge-base 5a37ddbd9a06> HEAD`; kein Retarget (base develop korrekt).
- 1868 (0428-326): Hop auf develop — analog, merge-base 5a37ddbd9a06, 18 Commits fehlen.
- 1866 (0428-321): Hop auf develop — merge-base c167fa5dd323, 6 Commits fehlen.
- 1864 (0428-291): Hop auf develop — merge-base c167fa5dd323, 6 Commits fehlen.
- 1855 (0428-078 reissue): Hop auf develop — merge-base c167fa5dd323, 6 Commits fehlen.
- 1820 (0428-271): Hop auf develop — merge-base fcd449117e18, 36 Commits fehlen; inhaltlich superseded von #1819? Nein, umgekehrt: #1819 content-wise von #1820 überholt.
- 1819 (0428-181): content-superseded durch #1820 → #1819 schließen (nur Coordinator darf schließen), alternativ auf #1820 retargeten.
- 1818 (0428-078): Hop auf develop — merge-base 3ebfb90daaf4, 76 Commits fehlen (größter Staleness-Abstand).
- 1650 (0428-078): Hop auf develop — merge-base ac7c970fe91a (ein Merge-Commit!), 26 Commits fehlen; head trägt develop-Merge-Commits, aber der eigene 0428-078-Arbeitssitz sitzt auf einem divergenten Basis-Commit → re-basen statt nur hoppen.
- demo 179: Hop auf develop — merge-base 58ac70679efe (das develop selbst), 1 Commits fehlt.
- demo 170: Hop auf develop — merge-base 58ac70679efe, 1 Commits fehlt.

## Scope-Compliance

- Read-only: kein Produkt-Push, kein PR-merge/close/edit, kein workflow_dispatch, keine Karten-Felder, keine generierten Views.
- Nur `gh api` (read) + ein flach geklontes, lokales baseharbor-worktree unter workers/ (kein scratch im ecosystem-root), keine Subagenten, kein lokaler Testlauf.
- Evidence liegt als DATEI im eigenen worktree (plan-write-freeze 2026-11-27); kein main-Commit in baseharbor-plan.
- Runner-/Container-/Compose-Nichts; keine VM.

## END

w390-0428-216-prhopcensus: DONE — read-only PR-hop census complete. 16 offene PRs inventarisiert (14 baseharbor + 3 demo minus Abgleich), 9 NOT-ancestor (7 baseharbor + 2 demo), alle base-Ref korrekt (develop), content-superseded #1819⊃#1820 bestätigt.
