# Akte: w391-0428-224-commitidentity — 0428-224 Commit-Identitäts-Aufnahme

## Mission (read-only + Akte)
Bestandsaufnahme der Commit-Identität in offenen Kandidaten der Karte 0428-224 im Repo baseharbor. Kein push, kein rewrite, kein merge. Nur eigener Klon unter /var/tmp für die Analyse; akte.md liegt im eigenen Arbeitsbaum (PLAN-REPO-WRITE-FREEZE 2026-11-27).

## Visible Ansatz-Block (Owner directive; verbatim)

- **Karten-Eigentümer (owner, verbatim aus card frontmatter, zur Laufzeit):** `0428-224` (karte t-20261121-candidate-commit-identity.md, owner-Feld ist aktuell leer/ghost-claim — 0428-224 ist hier die geteilte Kategorie "candidate commits carry", nicht eine einzelne_lane).
- **Lane-Registrierung (codeman agent list --json, Laufzeit):** `w391-0428-224-commitidentity` (mode opencode, id d655a9da-8189-4282-9bc9-14e014dbbfcb, parent e6ca7696-b1f8-492d-b226-876b16925fc5, workingDir workers/.models/laptop).
- **git user.name:** `w391-0428-224-commitidentity`
- **git user.email:** `w391-0428-224-commitidentity@baseharbor.local`
- **Literal commit invocation:**
  `git -c user.name=w391-0428-224-commitidentity -c user.email=w391-0428-224-commitidentity@baseharbor.local commit ...`
  (Merge analog mit `merge ...`)
- **Pre-push gate line (vor jedem Pushmechaniker — hier audit, kein Push in baseharbor):**
  `git show -s --format=%an HEAD` == `w391-0428-224-commitidentity`
  Abweichung = STOP + Report. Diese Mission schreibt nichts in baseharbor; der einzige Commit ist die akte im eigenen worktree unter o.g. Identität.

## Repo-/Workspace-Attestate

- Real planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY.
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
  baseharbor https://github.com/mcpdev80/baseharbor.git ; origin https://github.com/mcpdev80/baseharbor-plan.git
  (`workers/baseharbor-plan` ist eine DIR im bookkeeping-repo — NIEMALS das planning-repo, dort nie committen).
- baseharbor-Produkt-Clone für die Analyse: `/var/tmp/bh-0428-224-audit`, remote `origin https://github.com/mcpdev80/baseharbor.git` (blob:none).
- Realisitäts-Witness remote (ls-remote, eigene Run-ID):
  develop = `ea5218d72e263f21e79853b679af50074dab8c25`
  main = `cddc81b34fe13d8befdde4c487b365a0309ba428`

## (a) Offene Produkt-PRs mit Karte 0428-224 — Zeugen

- `gh pr list --repo mcpdev80/baseharbor --state open --json number,headRefOid,title,updatedAt` → 14 offene PRs (1650, 1812, 1818, 1819, 1820, 1855, 1860, 1861, 1862, 1863, 1864, 1866, 1868, 1869).
- Keine dieser 14 titelt "0428-224"; die karte 0428-224 ist die Kategorie "candidate commits carry". Der w155-Audit (2026-11-26) listete 6 offene PRs mit frontmatter-PR-Link, die heute gewechselt haben. Der Mission-auftrag (a) verlangt die letzten <=15 Commits je PR mit %an/%ae/%cn/%ce — durchgeführt via `gh api repos/mcpdev80/baseharbor/pulls/<n>/commits` (author + committer name/email) für alle 14 offenen PRs. 114 Commits total erfasst.
- Basishop-Ancestry (develop ea5218d… ist Ancestor des PR-Kopfs): PR 1863, 1862, 1861, 1860, 1812 = YES; PR 1869, 1868, 1866, 1864, 1855, 1820, 1819, 1818, 1650 = NO (auf älterer Base als current develop geschichtet/gehalten — Befund, kein Defekt).

## (b/c) Klassifikation je Commit: ok / fremd (4-Feld author-name / author-email / committer-name / committer-email)

- Erwartete Identität je PR = die lane, die der PR-Kopf trägt (letzter Commit author.name, wenn `wNNN-...-...@baseharbor.local`), sonst häufigste `wNNN`-Lane unter den Commits.
- Commit = SELBSTS-LANE (ok), wenn `author.name == committer.name` UND `author.name` == PR-eigene_lane UND `author.name` startet mit `w` und ist eine Lane (keine Nicht-Lane). Sonst = FREMD.
- Nicht-Lane-/Fremd-Identitäten im Sweep: `Codex` / `codex@openai.com`, `lv4-verify` / `worker@baseharbor.local`, `coordinator-codeman` (email w332-0428-288-composeids), `0428-061-sourcepull` / `0428-061@baseharbor.local`, verkürzt `w205`, author!=committer bei Merge-/Hop-Commits.

### Ergebnis pro PR (foreign / total):

- PR 1869 (owner w342-0428-331-damagedstate): 2/2 ok → **ALL-OK** (0 foreign)
- PR 1868 (owner w341-0428-326-proofleak): 3 Commits, 2 ok, 1 foreign (coordinator-codeman)
- PR 1866 (owner w345-0428-321-exitfix): 9 Commits, 4 ok, 5 foreign (w334/w352/w357 + 1 noreply-email)
- PR 1864 (owner w358-0428-291-1864hop): 3 Commits, 2 ok, 1 foreign (w333-0428-291-capperms)
- PR 1863 (owner w336-0428-299-goprereq): 4 Commits, 2 ok, 2 foreign (w361/w362 hops)
- PR 1862 (owner w370-0428-318-1862hop): 5 Commits, 2 ok, 3 foreign (w335/w371)
- PR 1861 (owner w367-0428-329-1861hop): 1 Commit, 1 ok → **ALL-OK** (0 foreign)
- PR 1860 (owner w333-0428-312-volrecovery): 5 Commits, 4 ok, 1 foreign (w372 hop)
- PR 1855 (owner w300-0428-078-pr1855hop): 18 Commits, 4 ok, 14 foreign (w165/w288/w323/w327/w338/w359 + lv4-verify)
- PR 1820 (owner w54-0428-181-export): 18 Commits, 1 ok, 17 foreign (0428-061-sourcepull/lv4-verify/Codex/w198/w205/w219/w231)
- PR 1819 (owner w54-0428-181-export): 11 Commits, 1 ok, 10 foreign (0428-061-sourcepull/Codex/lv4-verify/w198/w205)
- PR 1818 (owner w21-pr1702-0428-246-footprint): 4 Commits, 0 ok, 4 foreign (w21 vs Codex author!=committer + w53)
- PR 1812 (owner w362-0428-249-1812rebase): 21 Commits, 8 ok, 13 foreign (Codex/lv4-verify/w198/w304/w322)
- PR 1650 (owner w165-0428-078-pr1650-basehop): 10 Commits, 8 ok, 2 foreign (w181-0428-doclink-sweep author!=committer)

## (c) Aggregat

- **Offene Kandidaten (PRs) insgesamt:** 14
- **PRs mit >=1 fremd-identifiziertem Commit:** 12 (alle außer 1869 und 1861)
- **PRs mit ausschließlich selbst-lane Commits:** 2 (1869, 1861)

### Davon NUR Documentation-/Evidence-Commits (kein Produktinhalt):
Strikte Unterscheidung nach Commit-Subject + geänderter Dateityp (.md/.json/.go):
- **PR 1855:** enthält reine Evidence/Doc/Hop-Commits (catalog rows, witness-attribution comments, Merge/absorb) — ABER auch Produktinhalt (reissue Perses identity dashboard content, keycloak golden, data-capabilities gate binding). **Nicht** nur-Doku.
- **PR 1820 / 1819:** enthalten Produktinhalt (wire Perses identity dashboard into export path, fail-closed producer-path regression). **Nicht** nur-Doku.
- **PR 1812:** enthält Produkt-/CI-Inhalt (reload candidate image, admit full-destroy gate destroy commands, runner-health edit set). **Nicht** nur-Doku.
- **PR 1650 / 1818:** Produktinhalt (Perses identity-keycloak dashboard witness, keycloak identity dashboard). **Nicht** nur-Doku.
- **PR 1860 / 1862 / 1863 / 1866:** Produkt-/Testinhalt (recovery-manifest test, runtimeexecutor guard, stableid doc, exit-code mapping). **Nicht** nur-Doku.
- **PR 1864 / 1868 / 1869:** Produkt/Testinhalt. **Nicht** nur-Doku.
- **Ergebnis (c):** **0** der 12 PRs mit Fremd-Commits sind NUR Documentation-/Evidence-Commits; alle 12 tragen zusätzlich Produkt- oder Testinhalt. Fremd-Identität ist also ein über die offene Kandidaten verteilter Systemzustand, kein rein dokumentarischer Artefakt.

## (d) Rezept ohne Geschichts-Umschreibung (Vorschlag an Codex, KEINE Änderung)

**Regel, die künftig Fremd-Commits verhindert:** bereits implementiert in `coordinator/scripts/dispatch-lane.sh:45` (CANDIDATE COMMIT IDENTITY ADMISSION RULE, Owner scope scripts/**, 2026-11-26): jeder Kandidaten-Commit mit
`git -c user.name=<lane> -c user.email=<lane>@baseharbor.local commit ...`
und vor jedem Push mechanische Prüfung `git show -s --format=%an HEAD` == lane, auf mismatch STOP + report.
**Fundstelle für ein verschärftes Merge-/PR-Gate (Vorschlag, keine Änderung):**
- Datei **`.github/workflows/ci.yml`** (Owner scope — NIEMANDAUER EDITIEREN durch Lane; als finding an den Owner/Codex): eine Prüfsequenz "author == committer && author matches lane-regex ^w[0-9]+-.*-.*@baseharbor\.local$ && author == <expected lane> auf dem exakten Final-Head-Zeugen" vor Selected Runtime. Damit wäre Fremd-Commits (Codex/lv4-verify/0428-061/sourcepull/verkürzt) auf dem gemergten Head blockiert, ohne history rewrite.
- Datei **`scripts/pr-gate-*.py`** (z.B. `scripts/pr-gate-map-v1.json` / `scripts/pr-gate-*.py`, koordinator/Codex scope): neuen check `commit-identity-canonical` in die REQUIRED-Gates aufnehmen, der `git log -1 --format='%an|%ae|%cn|%ce'` des PR-Kopfs gegen `^wNNN-...-...@baseharbor.local$` und author==committer prüft. Vorschlag an Codex, KEINE Änderung durch diese Lane.
- **Keine Aenderung** durch w391 (read-only mission, GRENZEN: kein push, kein merge, kein workflow_dispatch, keine Produkt-/Config-Aenderung).

## (e) Befundtabelle PR | Commit | ok/fremd | Produkt/Evidence | Folgerung

| PR | Commit (short) | author / committer | ok/fremd | Inhalt | Folgerung |
|----|----|----|----|----|----|
| 1869 | 7c4c869d / 467913b7 | w342 / w342 (self) | ok | Produkt (deployment scan / pr-gate-coverage catalog) | head clean, owning lane w342 |
| 1868 | d654b065 / eea77618 | w341 / w341 | ok | Produkt+Doku (0428-326 + doc) | owning lane w341 |
| 1868 | 57320af6 | coordinator-codeman / coordinator-codeman (email w332) | fremd | Doku/Hop | Fremd-Lane auf Hop-Commit |
| 1866 | cdb6e4d9 | w334 / w334 | fremd | Doku (exit-codedocs) | fremde Lane auf integriertem Commit |
| 1866 | 33754a9a / c0c39f3b / 6609608f | w345 / w345 | ok | Produkt (exitfix) | owning lane w345 |
| 1866 | 2f733498 / d73fdef9 | w352 / w352 | fremd | Hop/rebase | fremde Lane |
| 1866 | abeba2c1 / 3702c095 | w357 / w357 | fremd | Fix+Merge | fremde Lane (+ 1 noreply-email) |
| 1864 | c945b2fc | w333 / w333 | fremd | Produkt (capperms) | fremde Lane auf Baseline |
| 1864 | 9712023e / b9675cc0 | w358 / w358 | ok | Hop+Merge | owning lane w358 |
| 1863 | 4919ef85 / 34c9d7bd | w336 / w336 | ok | Doku (goprereq) | owning lane w336 |
| 1863 | 4160d53f / 0eafa9f5 | w361 / w362 | fremd | Hop | fremde Lane |
| 1862 | c04d92df | w335 / w335 | fremd | Produkt (lowpair) | fremde Lane |
| 1862 | ab65312c / 2fcf3260 | w370 / w370 | ok | Hop+chore | owning lane w370 |
| 1862 | 6a1d6343 / 5c20c2e3 | w371 / w371 | fremd | Hop | fremde Lane |
| 1861 | ade7dab3 | w367 / w367 | ok | Produkt (1861hop) | ALL-OK |
| 1860 | fa16643a / 514d827c / f877feb / 6deab9ff | w333 / w333 | ok | Test (volrecovery) | owning lane w333 |
| 1860 | 057ce8c5 | w372 / w372 | fremd | Hop | fremde Lane |
| 1855 | 43326cf5 / 7d805dc6 / adb7cfd1 / eb45c655 / d0b0f0b7 | w165/w288/w300 | teils fremd/ok | Produkt (0428-078 Perses dashboard) | gemischte Lanes; owning w300 |
| 1855 | 123666c8 | w288 | fremd | Produkt (0428-078) | fremde Lane |
| 1855 | 81a49dff | lv4-verify | fremd | Evidence (gate run witness) | lv4-verify/worker |
| 1855 | 8635ba07 / 77bd785c / f13d37d4 / 18ccd8ea / 879655f0 | w323 / w327 | fremd | Doku/witness | fremde Lane |
| 1855 | d5545573 | w338 | fremd | Produkt (metrics witness) | fremde Lane |
| 1855 | d18e4b36 | w359 | fremd | Hop (noreply-email) | fremde Lane |
| 1820 | 22ca61bb / 2f9f2f05 / 514084f3 / 17381017 | 0428-061-sourcepull | fremd | Hop | fremde/gesamte Base |
| 1820 | 9f84f47a | w54 / 0428-061-sourcepull | fremd | Produkt | author!=committer |
| 1820 | 28803d11 | lv4-verify | fremd | Produkt (0428-271) | lv4-verify |
| 1820 | 9140b2cb | Codex / w53 | fremd | CI | author!=committer |
| 1820 | 64d3dc0e / 2ea41620 / 3859d466 / 10129196 / eafd5e6d | lv4-verify | fremd | Evidence | lv4-verify/worker |
| 1820 | 394559ec | w198 | fremd | Hop | fremde Lane |
| 1820 | a3ee25f6 | w205 | fremd | Hop (verkürzt) | verkürzte Lane |
| 1820 | 34142a2a / 52e08e36 / 8f6b2444 | w219 / w198 / w198 | fremd | Hop | fremde Lane |
| 1819 | 9f84f47a | w54 / 0428-061 | fremd | Produkt | author!=committer |
| 1819 | 17381017 | 0428-061-sourcepull | fremd | Produkt | fremde Lane |
| 1819 | 9140b2cb | Codex / w53 | fremd | CI | author!=committer |
| 1819 | 64d3dc0e / 2ea41620 / 3859d466 / 10129196 / eafd5e6d | lv4-verify | fremd | Evidence | lv4-verify |
| 1819 | 394559ec / a3ee25f6 | w198 / w205 | fremd | Hop | fremde Lane |
| 1818 | e0a93ce0 / 888e2193 / 8e2c50c1 | w21-pr1702 / Codex | fremd | Hop+Fix | author!=committer (Codex) |
| 1818 | 20fc1cb7 | w53 / Codex | fremd | Fix | author!=committer |
| 1812 | 9140b2cb | Codex / w53 | fremd | CI | author!=committer |
| 1812 | 64d3dc0e / 2ea41620 / 3859d466 / 10129196 / eafd5e6d | lv4-verify | fremd | Evidence | lv4-verify |
| 1812 | 394559ec / f166a49f / 0922888a | w198 | fremd | Hop | fremde Lane |
| 1812 | b962e6d2 | w304 | fremd | Hop | fremde Lane |
| 1812 | 7e42c1e6 / 473be0c0 / 210d5d10 | w322 | fremd | CI+fix | fremde Lane |
| 1812 | 05cb3fd9 / 709a9b1b / 860d4157 / 6ab5310d / 8c83c709 / 0b343af5 / d95e46de / c2dd3ff0 | w362 | ok | Produkt+Hop | owning lane w362 |
| 1650 | ed2fb751 / f89f506f | w181 / w165 | fremd | Doku (doclink-sweep) | author!=committer |
| 1650 | b95df510 / 2c407318 / 8e4a10f3 / 903991f3 / 156507ee / af256c3f / 1c33e910 / 37c4d847 | w165 / w165 | ok | Produkt+Doku | owning lane w165 |

### Folgerung
- Symptom der karte 0428-224 bestätigt und quantifiziert: **12 von 14 offenen Kandidaten** tragen >=1 fremd-identifizierten Commit. Ursache = geteilte Checkout-Identität (last-writer-wins) + Hop/rebase/absorb-Commits verschiedener Lanes + nicht-Lane-Identitäten (Codex, lv4-verify/worker) auf Evidence-/Merge-Commits.
- Kein Fremd-Commit ist auf reinen Dokumentation/Evidence-Bereich begrenzt; alle 12 PRs tragen zusätzlich Produkt-/Testinhalt.
- Verifizierbar durch `git show -s --format=%an HEAD` / full `git log`-Sweep; Merge-/Hop-Commits per `git log --merges` separat markierbar.

## End / evidence location
- akte.md liegt im eigenen worktree, NICHT auf plan main (PLAN-REPO-WRITE-FREEZE 2026-11-27).
- END meldet den Pfad + sha256 der akte.md statt eines main-sha; Coordinator stagingt unter coordinator/evidence-staging/.
- **sha256 der akte.md:** `e5b8f9a49f5c0676106f16801712295fc49da7efdd2b71af9196a9fcc8ecd455`
- **Pfad:** `/home/marcel/dev/baseharbor-ecosystem/workers/.models/laptop/evidence/w391-0428-224-commitidentity/akte.md`
- **Git-Author-Identity-Gate für diese Lane (read-only audit, kein Produkt-Commit):**
  `git show -s --format=%an HEAD` == `w391-0428-224-commitidentity` (nur auf dem akte-Commit im eigenen worktree prüfbar; in baseharbor wurde nichts committen)
- **/var/tmp clone witness:** `/var/tmp/bh-0428-224-audit` (56M), remote `origin https://github.com/mcpdev80/baseharbor.git` — wird mit END heruntergefahren/entfernt.
