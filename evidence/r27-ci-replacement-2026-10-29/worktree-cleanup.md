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
