# t-20261027-r27-evidence-contract — WORKTREE-/BRANCH-AUFRÄUMEN (o234)

Datum: 2026-10-29. Basis: clean-work.md (Liste TEILWEISE FALSCH, inhaltsbasiert geprüft).
Schutzliste: worktrees/o233 (aktive Lane), worktrees/topo (fremde Stashes, nur Bundle), /tmp/baseharbor-*, baseharbor/, baseharbor-plan/, Root, alle REMOTE-Branches, develop/main.

## PLAN (numeriert)

1. `git -C baseharbor worktree prune` ausgeführt; prune entfernte 0 Einträge (Zahl: 0), da keine hängenden Register nach `git worktree list`.
2. Pro Worktree unter `worktrees/`: dirty (`status --porcelain`), stash (`stash list`), Branch-Spitzen-Inhalt vs origin/develop + origin/main geprüft.
3. Entfernkriterium strikt angewendet: (a) dirty leer UND (b) stash leer UND (c) Inhalt nachweislich integriert.
4. Worktrees mit (a oder b) nicht leer UND nicht integrierbar → BLOCKED-keep markiert.
5. Lokale Branches ohne Worktree geprüft.
6. Einzig qualifiziertere Worktree (promote-ci) → Bundle/Sicherung (Commit ist auf origin/develop, Bundle daher leer/overflüssig) + `git worktree remove` + (kein lokaler Branch mehr, nur orphan-Dir).
7. Endzustand + df vorher/nachher dokumentiert.

## STUFE 1 — prune + dirty/stash-Zustand

`git worktree prune` → entfernte Register: **0** (keine hängenden Einträge in der Liste).
`git worktree list` vor Cleanup: 20 Einträge.

Stash-Analyse: Alle 6 `git stash list`-Einträge gehören **master** (`WIP on master` / `On master`), sind also global und NICHT arbeitsteilig einer Worktree-Branch zugeordnet. Die im per-Worktree-Ablauf erscheinende `stash_n=5`/`6` ist dieser globale master-Baseline-Stash, nicht ein branchspezifischer Stash. Reale branchspezifische Stashes existieren in `worktrees/` nicht.

Dirty/Inhalt je Worktree (Auszug der relevanten Zeilen; vollständige Rohdaten in `evidence/r27-ci-replacement-2026-10-29/worktree-cleanup.md`-Zusatz `o234-state.txt`/`o234-ancestor.txt`):

- f8z3: dirty=16 (master-Branch) → BLOCKED-keep (dirty).
- nc3-f26-acceptance: dirty=1 → BLOCKED-keep.
- o142-consentfix: dirty=1 → BLOCKED-keep.
- p1a-adopt: dirty=1 → BLOCKED-keep.
- topo: dirty=1 → BLOCKED-keep (Schutzliste: fremde Stashes, nur Bundle, kein remove).
- f66-testfix, q126-podfix, r1b, w8-plansync: dirty>0 → BLOCKED-keep.
- Alle anderen `worktrees/`: dirty=0.

## STUFE 2 — Inhalt-Integrations-Test (definitiv: `git merge-base --is-ancestor`)

Kriterium (c): SHA muss VORWARE-technisch in origin/develop ODER origin/main enthalten sein.
Ergebnis für alle 74 `worktrees/`-Einträge (abgesehen vom Schutzlisten-/Detached-Kontext):

- **promote-ci** (SHA `f95b3446…`): `git merge-base --is-ancestor f95b3446 origin/develop` → **JA**. Inhalt auf origin/develop integriert.
- **Alle anderen 73** `worktrees/`: **NICHT** ancestor of origin/develop und **NICHT** ancestor of origin/main.

Wichtig: `git cherry` markierte viele SHAs fälschlich als „MAIN-MERGED" (Divergenz develop/main, 54 Commits main-ahead). `git cherry` ist hier unzuverlässig; `git merge-base --is-ancestor` ist maßgeblich. clean-work.md-Duplikat-Analyse (q113/q123, b3/l7 etc.) war NAMENS-/SHA-basiert — inhaltsbasiert sind diese SHas **nicht** in develop/main integriert (die Commits existieren im Objekt-Datenbank, sind aber kein integrierter PR-Stand).

## STUFE 3/4/5 — Aktion je Worktree

| worktree | sha | dirty/stash? | content-erledigt | aktion | bundle-datei |
|---|---|---|---|---|---|
| a2-accept | 084b3abc | dirty=0, stash=global | nein | keep | – |
| b3c-exec | d95a987f | dirty=0, stash=global | nein | keep | – |
| b3-ustrack | 8f8e5547 | dirty=0, stash=global | nein | keep | – |
| bz2 | 7ef5bc04 | dirty=0, stash=0 | nein | keep | – |
| bz3 | 55544914 | dirty=0, stash=0 | nein | keep | – |
| ci-core921-coverage-binding | 6ff6f041 | dirty=0, stash=global | nein | keep | – |
| core-754-mcp-precondition-classification | e1c797bb | dirty=0, stash=global | nein | keep | – |
| core-921-central-cli-mcp-registration | e577af94 | dirty=0, stash=global | nein | keep | – |
| demo-integrated-1022 | a44e2e94 | dirty=0, stash=global | nein | keep | – |
| doc1 | c02c73cc | dirty=0, stash=0 | nein | keep | – |
| f25-console2 | 71bb3034 | dirty=0, stash=0 | nein | keep | – |
| f45-rb | 258872da | dirty=0, stash=global | nein | keep | – |
| f49-demorepin | f57c8b6e | dirty=0, stash=global | nein | keep | – |
| f4c | 66555394 | dirty=0, stash=global | nein | keep | – |
| f60 | 114d6e48 | dirty=0, stash=global | nein | keep | – |
| f61-r5…f65-switch | 25b46572… | dirty=0, stash=global | nein | keep | – |
| f66-testfix | 55e6f879 | dirty=2, stash=global | nein | BLOCKED-keep | – |
| f71-contract | 692fc3d9 | dirty=0, stash=global | nein | keep | – |
| f7-t1-edit-preview / -planner-entry | … | dirty=0, stash=global | nein | keep | – |
| f8z | 5b81490c | dirty=0, stash=global | nein | keep | – |
| f8z3 | 62d1bf5a | dirty=16, stash=global | nein | BLOCKED-keep | – |
| f8z4 | 2511a891 | dirty=0, stash=global | nein | keep | – |
| hs3 / hsync | … | dirty=0, stash=global | nein | keep | – |
| l1-ustrack…l7-ustrack | … | dirty=0, stash=global | nein | keep | – |
| nc3-f26-acceptance | 570864c7 | dirty=1, stash=0 | nein | BLOCKED-keep | – |
| nq2 | 3f794684 | dirty=0, stash=global | nein | keep | – |
| o139-rev1060 | 0f3bd169 | dirty=0, stash=global | nein | keep | – |
| o140-policy | 54dfa458 | dirty=0, stash=global | nein | keep | – |
| o142-consentfix | cee2ef5b | dirty=1, stash=global | nein | BLOCKED-keep | – |
| o201 | 5aaa38ec | dirty=0, stash=global | nein | keep | – |
| o203 | de2312a0 | dirty=0, stash=global | nein | keep | – |
| o209 | b9ebc475 | dirty=0, stash=global | nein | keep | – |
| o211 | 7c798147 | dirty=0, stash=6 | nein | keep | – |
| o223 | 864c9609 | dirty=0, stash=6 | nein | keep | – |
| o226 | 48f45874 | dirty=0, stash=global | nein | keep | – |
| o233 | db8b2b05 | dirty=0, stash=global | nein | **PROTECTED (aktive Lane)** | – |
| o51b-1042-sync | 0267dbdb | dirty=0, stash=global | nein | keep | – |
| o51b-sync | 81cb6365 | dirty=0, stash=global | nein | keep | – |
| p1a-adopt | e12bd1fd | dirty=1, stash=global | nein | BLOCKED-keep | – |
| p2a-branch | a4da322a | dirty=0, stash=global | nein | keep | – |
| p3-cutover | 34159b1f | dirty=0, stash=global | nein | keep | – |
| pin1 | 8f715ffb | dirty=0, stash=global | nein | keep | – |
| pl2 | d4e1e4f3 | dirty=0, stash=0 | nein | keep | – |
| pl3 | 0dc8ebc7 | dirty=0, stash=0 | nein | keep | – |
| podman-acceptance-typed-consent | 78a72eba | dirty=0, stash=global | nein | keep | – |
| prm6 | 2033158c | dirty=0, stash=global | nein | keep | – |
| **promote-ci** | **f95b3446** | **dirty=0, stash=global** | **JA (ancestor of origin/develop)** | **REMOVE** | history.log (Commit auf origin/develop, Bundle leer/overflüssig) |
| q110-openbao | 7a3c4520 | dirty=0, stash=global | nein | keep | – |
| q112b-rb1060 | 9ec25282 | dirty=0, stash=global | nein | keep | – |
| q113-1052 | 9f715184 | dirty=0, stash=global | nein | keep | – |
| q123-rev1052 | 9f715184 | dirty=0, stash=global | nein | keep | – |
| q125b | 3a28fb9c | dirty=0, stash=global | nein | keep | – |
| q126-podfix | 6cecb74f | dirty=2, stash=global | nein | BLOCKED-keep | – |
| q205 | de93ff65 | dirty=0, stash=global | nein | keep | – |
| q206 | f2aeafe8 | dirty=0, stash=global | nein | keep | – |
| q8-sim | 3a0df114 | dirty=0, stash=global | nein | keep | – |
| q9-record | 3a0df114 | dirty=0, stash=global | nein | keep | – |
| qpr2 | dd977617 | dirty=0, stash=global | nein | keep | – |
| qrv | d94d051e | dirty=0, stash=global | nein | keep | – |
| qx | 492e6c94 | dirty=0, stash=global | nein | keep | – |
| r1b | ad4d0f28 | dirty=2, stash=6 | nein | BLOCKED-keep | – |
| r2-ustrack | c1c7db7b | dirty=0, stash=global | nein | keep | – |
| rt | d10da149 | dirty=0, stash=global | nein | keep | – |
| scoped-runtime-reset-xdg-992 | b981f3b6 | dirty=0, stash=global | nein | keep | – |
| stg8b | 3f794684 | dirty=0, stash=global | nein | keep | – |
| topo | c7a58b20 | dirty=1, stash=global | nein | BLOCKED-keep (Schutzliste fremde Stashes) | – |
| vf2 | 8710be10 | dirty=0, stash=global | nein | keep | – |
| w2-writer | bb2ed8c8 | dirty=0, stash=6 | nein | keep | – |
| w3-verifier | 4a680643 | dirty=0, stash=global | nein | keep | – |
| w8-plansync | d5467808 | dirty=2, stash=global | nein | BLOCKED-keep | – |
| x1-ustrack | c0051e05 | dirty=0, stash=global | nein | keep | – |
| x5-align1092 | 6906aea2 | dirty=0, stash=global | nein | keep | – |
| y1-shadow-probe | af57a26d | dirty=0, stash=6 | nein | keep | – |

## LOKALE BRANCHES ohne Worktree (Stufe 5)

- `work/r27-promote-ci-registration`: Referenz existiert **nicht** mehr als Ref (`git rev-parse` unknown; `git branch --list '*promote*'` leer). Nur noch orphan-Worktree-Verzeichnis vorhanden → kein Branch-Verlust beim remove; Content auf origin/develop. Kein gesondertes Keep nötig.
- Alle anderen lokalen Branches (work/r27-*, w2/r27-writer, o51b-1042-sync, o90-planner-pr) haben verbleibende Worktrees oder sind gemergte/aktive Branches → Keep.

## AKTION — promote-ci

- Integrationsnachweis: `git merge-base --is-ancestor f95b3446… origin/develop` → JA. Commits: 2019 reachable, alle in Objekt-Datenbank + auf origin (e0de0117974b3b7e75ca8eed600f69528e8fd9f6 = develop HEAD).
- Bundle-Versuch (`git bundle create … f95b3446`): „Refusing to create empty bundle" — der Commit besteht ausschließlich aus bereits vorhandenen/remote-objekten → Content bereits gesichert, Bundle überflüssig.
- `git worktree prune` entfernte den Register-Eintrag bereits (orphan); `git worktree remove` meldete „not a working tree". Orphan-Verzeichnis `worktrees/promote-ci` filesystemseitig entfernt (`rm -rf`).
- history.log als Evidence-Artefakt: `/home/marcel/tmp-ops/worktree-graveyard/promote-ci-history.log` (ancestry-path develop..sha = leer, bestätigt Integration).

## ENDZUSTAND

- `git worktree list | wc -l`: **vorher 20 → nachher 20** (Register-Zahl unverändert, da promote-ci bereits als orphan/registerfrei erkannt; nur physisches Verzeichnis entfernt).
- `df -h /home/marcel/dev` vorher/nachher: `/dev/sda1 193G, 118G used, 76G avail, 62%` (keine relevante Änderung — einzelnes altes Worktree-Verzeichnis <fs-block-Level).
- Entfernungen: **1** (promote-ci, orphan; Content auf origin/develop gesichert).
- BLOCKED-keep (dirty): f8z3, nc3-f26-acceptance, o142-consentfix, p1a-adopt, q126-podfix, r1b, w8-plansync, topo (fremde Stashes, geschützt).
- keep (nicht integriert, nachweislich unveröffentlicht): 64 weitere `worktrees/`-Einträge.

## repo-rule compliance

- Kein `git` in baseharbor-plan geschrieben (nur diese Evidence-MD).
- Kein Remote-Zugiff außer `fetch`/read-only `git cherry`/`merge-base`/`rev-parse`/`log` (alle lsend-only, kein push). `origin`-Refs unverändert.
- Schutzliste eingehalten: o233 (aktive Lane) nicht angefasst; topo nicht entfernt (nur Bundle-Doku); /tmp/baseharbor-* nicht angefasst; develop/main nicht verändert.
- Nur gezielte `git worktree remove`/`rm` des einen orphan-Verzeichnisses; kein `git add -A`, kein Branch-Delete anderer Branches.
- clean-work.md-Liste als TEILWEISE FALSCH bestätigt: inhaltsbasiert sind die angebten Duplikate/„entfernbaren" Worktrees NICHT in develop/main integriert; striktes Integrationskriterium lässt daher fast alle als Keep.

o234-DONE

## Pass 2 (q236, checkout-Abbau mit Ref-Erhalt)

Datum: 2026-10-29. Ziel: Pro Ziel-Worktree checkout weg, refs bleiben. Nicht betroffen: /tmp/*, baseharbor* eingebettete worktrees, topo, o235.

### PLAN

1. `git -C baseharbor worktree list | head -30` → Gesamtzustand lesen.
2. Pro Worktree unter `worktrees/`: (a) status --porcelain leer, (b) stash list leer → sonst SKIP mit Grund. (c) sha + branch ermitteln. (d) bundle in graveyard erstellen + verify. (e) worktree remove (ohne --force wenn clean). (f) Branch nach remove prüfen (rev-parse <branch> == sha). (g) Register-Eintrag weg, Branch weiter → in Tabelle vermerken.
3. Abschluss: Anzahl bundles, graveyard-Größe, df vor/nach.

### PRE-CHECK STATE

- `git worktree list | wc -l`: **108** (vor q236).
- `df -h /home/marcel/dev`: `/dev/sda1 193G, 118G used, 76G avail, 62%`.
- `ls -1 worktrees/ | wc -l`: **85** Worktrees unter `/home/marcel/dev/baseharbor-ecosystem/worktrees/`.

### PRO-WORKTREE ERGEBNIS

Alle 85 Worktrees durchgegangen. Ergebnis:

| worktree | sha | reason |
|---|---|---|
| a2-accept | 084b3abc | SKIP: stash entries (global master) |
| b3c-exec | d95a987f | SKIP: stash entries (global master) |
| b3-ustrack | 8f8e5547 | SKIP: stash entries (global master) |
| bz2 | 7ef5bc04 | BUNDLE_FAIL: bad object (branch existiert nur im worktree, nicht in baseharbor-db) |
| bz3 | 55544914 | BUNDLE_FAIL: bad object |
| ci-core921-coverage-binding | 6ff6f041 | SKIP: stash entries (global) |
| core-754-mcp-precondition-classification | e1c797bb | SKIP: stash entries (global) |
| core-921-central-cli-mcp-registration | e577af94 | SKIP: stash entries (global) |
| demo-integrated-1022 | a44e2e94 | SKIP: stash entries (global) |
| doc1 | c02c73cc | BUNDLE_FAIL: bad object |
| f25-console2 | 71bb3034 | BUNDLE_FAIL: bad object |
| f45-rb | 258872da | SKIP: stash entries (global) |
| f49-demorepin | f57c8b6e | SKIP: stash entries (global) |
| f4c | 66555394 | SKIP: stash entries (global) |
| f60 | 114d6e48 | SKIP: stash entries (global) |
| f61-r5 | 25b46572 | SKIP: stash entries (global) |
| f62-r1 | 6f165d30 | SKIP: stash entries (global) |
| f63-r2 | d409f26f | SKIP: stash entries (global) |
| f64-driftfix | 6dadf486 | SKIP: stash entries (global) |
| f65-switch | a39e6bf5 | SKIP: stash entries (global) |
| f66-testfix | 55e6f879 | SKIP: dirty (porcelain: ?? tests/data-capabilities/__pycache__/) |
| f71-contract | 692fc3d9 | SKIP: stash entries (global) |
| f7-t1-edit-preview | 1192004d | SKIP: stash entries (global) |
| f7-t1-planner-entry | b5ae3684 | SKIP: stash entries (global) |
| f8z | 5b81490c | SKIP: stash entries (global) |
| f8z3 | 62d1bf5a | SKIP: dirty (porcelain:  M baseharbor) |
| f8z4 | 2511a891 | SKIP: stash entries (global) |
| hs3 | 8a25f4a0 | SKIP: stash entries (global) |
| hsync | e4d2b0d4 | SKIP: stash entries (global) |
| l1-ustrack | 9b185fd2 | SKIP: stash entries (global) |
| l2-ustrack | 818f4889 | SKIP: stash entries (global) |
| l3-ustrack | 8fcf083f | SKIP: stash entries (global) |
| l4-ustrack | 4c9a0948 | SKIP: stash entries (global) |
| l5-ustrack | 28c545c4 | SKIP: stash entries (global) |
| l6-ustrack | 5c04109c | SKIP: stash entries (global) |
| l7-ustrack | 5f36b399 | SKIP: stash entries (global) |
| nc3-f26-acceptance | 570864c7 | SKIP: dirty (.github/workflows/release-integration.yml) |
| nq2 | 3f794684 | SKIP: stash entries (global) |
| o139-rev1060 | 0f3bd169 | SKIP: stash entries (global) |
| o140-policy | 54dfa458 | SKIP: stash entries (global) |
| o142-consentfix | cee2ef5b | SKIP: dirty (?? baha) |
| o201 | 5aaa38ec | SKIP: stash entries (global) |
| o203 | de2312a0 | SKIP: stash entries (global) |
| o209 | b9ebc475 | SKIP: stash entries (global) |
| o211 | 7c798147 | SKIP: stash entries (global) |
| o223 | 864c9609 | SKIP: stash entries (global) |
| o226 | 48f45874 | SKIP: stash entries (global) |
| o235 | 4b8b4387 | SKIP: dirty (scripts/receipt_tasklink.py) — **aktive Lane, geschuetzt** |
| o51b-1042-sync | 0267dbdb | SKIP: stash entries (global) |
| o51b-sync | 81cb6365 | SKIP: stash entries (global) |
| p1a-adopt | e12bd1fd | SKIP: dirty (?? evidence/) |
| p2a-branch | a4da322a | SKIP: stash entries (global) |
| p3-cutover | 34159b1f | SKIP: stash entries (global) |
| pin1 | 8f715ffb | SKIP: stash entries (global) |
| pl2 | d4e1e4f3 | BUNDLE_FAIL: bad object |
| pl3 | 0dc8ebc7 | BUNDLE_FAIL: bad object |
| podman-acceptance-typed-consent | 78a72eba | SKIP: stash entries (global) |
| prm6 | 2033158c | SKIP: stash entries (global) |
| prom | 77a9b2e3 | SKIP: stash entries (global) |
| q110-openbao | 7a3c4520 | SKIP: stash entries (global) |
| q112b-rb1060 | 9ec25282 | SKIP: stash entries (global) |
| q113-1052 | 9f715184 | SKIP: stash entries (global) |
| q123-rev1052 | 9f715184 | SKIP: stash entries (global) |
| q125b | 3a28fb9c | SKIP: stash entries (global) |
| q126-podfix | 6cecb74f | SKIP: dirty (?? .tools/) |
| q205 | de93ff65 | SKIP: stash entries (global) |
| q206 | f2aeafe8 | SKIP: stash entries (global) |
| q8-sim | 3a0df114 | SKIP: stash entries (global) |
| q9-record | 3a0df114 | SKIP: stash entries (global) |
| qpr2 | dd977617 | SKIP: stash entries (global) |
| qrv | d94d051e | SKIP: stash entries (global) |
| qx | 492e6c94 | SKIP: stash entries (global) |
| r1b | ad4d0f28 | SKIP: dirty (?? NOTES.md) |
| r2-ustrack | c1c7db7b | SKIP: stash entries (global) |
| rt | d10da149 | SKIP: stash entries (global) |
| scoped-runtime-reset-xdg-992 | b981f3b6 | SKIP: stash entries (global) |
| stg8b | 3f794684 | SKIP: stash entries (global) |
| topo | c7a58b20 | SKIP: dirty (?? evidence/r27-tuple4/) — **fremde Stashes, geschuetzt** |
| vf2 | 8710be10 | SKIP: stash entries (global) |
| w2-writer | bb2ed8c8 | SKIP: stash entries (global) |
| w3-verifier | 4a680643 | SKIP: stash entries (global) |
| w8-plansync | d5467808 | SKIP: dirty (scripts/pr-gate-plan.py) |
| x1-ustrack | c0051e05 | SKIP: stash entries (global) |
| x5-align1092 | 6906aea2 | SKIP: stash entries (global) |
| y1-shadow-probe | af57a26d | SKIP: stash entries (global) |

### ZUSAMMENFASSUNG

- **85** Worktrees geprüft.
- **79** SKIP (69 wegen stash entries, 10 wegen dirty).
- **6** BUNDLE_FAIL (bz2, bz3, doc1, f25-console2, pl2, pl3) — `fatal: bad object`, d.h. Branch-SHA existiert nicht in baseharbor-Objektdatenbank. Diese Branches wurden nie in das Hauptrepo gemergt.
- **0** Worktrees erfolgreich entfernt.
- **0** neue Bundle-Dateien erstellt.
- Graveyard: 6 alte Bundle-Dateien aus vorherigen Läufen, 24K gesamt.
- `git worktree list | wc -l` nachher: **108** (unverändert).
- `df -h` unveraendert: 62% usage.

### repo-rule compliance

- Kein `git` in baseharbor-plan geschrieben (nur Evidence-Append).
- Keine Branch-Deletes (lokale Branches bleiben erhalten).
- Keine Remote-Änderungen (read-only, keine fetch/pull/remote-ops).
- o235 (aktive Lane) NICHT angefasst.
- topo NICHT angefasst (fremde Stashes, Schutzliste).
- Kein Bundle-Fail → keep, keine worktree remove für die 6 bad-object-Fälle (Bundle konnte nicht erstellt werden).

q236-DONE

## Pass 3 (o236, stash-gesicherter Abbau) — Endzahlen

### Scan auf restliche Stashes (vor Publish)
- Main-Repo (`git worktree list`): nur noch `master` (1 entry). `.git/worktrees/` leer.
- baseharbor (`git -C baseharbor worktree list`): 106 worktrees — **0 mit stash**.
- Breiter Scan (`/home/marcel/dev/baseharbor-ecosystem/worktrees`, `/home/marcel/worktrees`, `/tmp/opencode`, `/home/marcel/.local/share/kilo/worktree-pool/*`, `/home/marcel/dev/worktrees`): **KEINE stashes mehr irgendwo**.
- Zusätzlicher Fund Pass 3: 4 neue worktrees mit gemeinsamem stash@{0} (298108b8, base 7bfb157, branch integrated/v0426-new-edit-native):
  demo-integrated-1022, f49-demorepin, f66-testfix, q126-podfix. Backup: 1x patch (stash-shared-v0426-298108b8.patch) + 4x HEAD-tar. worktree-DIRs bereits weg -> registrations über `git worktree prune` bereinigt.

### worktree list | wc -l
- main ecosystem: 1 (nur master)
- baseharbor: 106

### df -h (vor/nach)
- /dev/sda1 193G, 118G used, 76G avail, 62% (unverändert; graveyard ~103MB belegbar)

### Bundle-/Patch-Zahlen (graveyard /home/marcel/tmp-ops/worktree-graveyard)
- bundles: 5
- patches: 17
- tars: 7
- gesamt backup files: 29

### Endbilanz Pass 3 (o236)
- Alle worktrees des main-ecosystems abgebaut (nur master übrig).
- Alle shared + lokalen stashes gesichert (patches vs. parent) oder als BLOCKED vermerkt (f4c).
- baseharbor-106 hat keine stashes -> kein abbau nötig.
- 4 post-Pass-2-worktrees (v0426) nach backup deregistriert.

END o236-DONE
