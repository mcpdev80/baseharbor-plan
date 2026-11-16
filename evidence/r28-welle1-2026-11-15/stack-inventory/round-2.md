# Mission: stack-inventory round-2 (stackaudit2 lane)

Mission date: 2026-11-16. Coordination-nahe Pruef-Arbeit, KEIN feature-scope.
Nur lesen (gh + git ls-remote + plan.py). Kein Produkt-Write, kein gh pr
edit/retarget/close, kein Karten-Write, kein .github/**, kein Subagent (AGENTS §4.8).

## Mission scope (verbatim aus /tmp/opencode/mission-stackaudit2.md)

AUFGABE (read-only stack-inventur r2): systematischer zeuge ueber den Zustand des
0.4.28-faechers NACH der develop-sync-welle. Nur lesen (gh + git ls-remote + plan.py
show), KEINE aenderungen an produktdateien/PRs/karten.

LIEFER-PRUEFLISTE:
1) fuer JE offenes 0.4.28-PR (#1575 #1577 #1578 #1579 #1580 #1582 #1585 #1590 #1591
   #1592 #1594 #1595 #1596 #1597 #1598 #1599 #1600 #1602 #1603 #1604 #1606 #1608 #1610
   #1613 #1614 #1615 #1616 #1619 #1620 #1623): state, isDraft, base-ref-name, head-SHA,
   ls-remote-HEAD desselben branch - Abweichung (PR-head != branch-head) = DRIFT-BEFUND.
2) basis-treue: base-ref jedes gestapelten PRs zeigt auf den zweig der deklarierten
   basis-lane.
3) sync-stand: pro branch ein zeuge, ob origin/develop (14d8f17d1aa oder neuer) im
   verlauf enthalten ist (git merge-base --is-ancestor nach fetch) - liste NICHT-syncter
   pfade.
4) draft-guard-befunde: jedes PR mit draft=false im 0.4.28-faecher (aussen vor: die
   release-welt-pfade #1574/#1611/#1612/#1622/#1581/#1587/#1588/#1589 bleiben unbewertet,
   nur als fremd notiert).

Realitaetsabgleich: die Mission nummeriert genau 30 PRs auf, und diese 30 wurden exakt
so erhoben. Der gh-Label-/Base-Filter "0.4.28" allein trifft nur 5 PRs; die 30 genannten
betreffen durchweg Zweige der r28-Welle (lane-0428-*, cli2-*, wt-0428-*, perses-*,
w0*-*, perf/0428-*). Die 8 Release-Welt-PRs bleiben unbewertet, nur als fremd notiert.

## PLAN

- 1. done - Vorbereiten: gh/git/plan.py Reichweite, Zonen, kein Schreibpfad ausser der einen Akte
- 2. done - Zelle 1: pro PR state/isDraft/base-ref/head-SHA + ls-remote-HEAD der head-Ref; Drift = Befund
- 3. done - Zelle 2: Basis-Treue base-ref gegen deklarierte Basis-Lane (uid-, perses-, cli2-Kette)
- 4. done - Zelle 3: Sync-Stand pro Branch gegen origin/develop 14d8f17d1aa (merge-base --is-ancestor), Liste nicht-syncter Pfade
- 5. done - Zelle 4: Draft-Guard-Befunde (draft=false im Faecher), ausser den 8 unbewerteten Release-Welt-Pfaden
- 6. done - Akte auf origin/main der baseharbor-plan pushen, origin-Zeuge, Endpost

## Repo-rule compliance

- Read-only auf baseharbor (gh api + git ls-remote + ein Fetch in eine eigene Scratch-Zone unter /tmp/opencode/stackaudit2-r2/wt). Kein Write im Produkt-Repo, kein gh pr edit/close/retarget.
- Kein Subagent (AGENTS §4.8): alle Schritte in dieser Session ausgefuehrt.
- Kein .github/** (Owner-Scope); keine Workflow-Aenderungen, keine Reruns, kein workflow_dispatch.
- Keine Container/Compose gestartet; keine VM genutzt (baha-docker / baha-podman unberuehrt). Rein lokale Lesezugriffe auf GitHub + git.
- Evidence nur in baseharbor-plan unter evidence/r28-welle1-2026-11-15/stack-inventory/round-2.md; kein .evidence/ im Produkt-Repo.
- Zone-Check (Wrong-Zone-Regel): Evidence-Repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (einziger Pfad); /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan ist NICHT das Planungsrepo und wurde nicht verwendet.

## BASE ATTESTATION / origin-Zeugen (gemessen vor der Akte, alles read-only)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse origin/main   # nach fetch
65eeda4f0b2f5935c8280497da6c75522d83367e
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse HEAD
65eeda4f0b2f5935c8280497da6c75522d83367e
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan status --porcelain
?? evidence/cli-redesign-20261114/r28-welle1-2026-11-16/
?? evidence/r28-welle1-20261115/
```

Die beiden untracked Evidence-Verzeichnisse gehoeren anderen Lanes (cli2-app-export,
cli2-env-delete); sie wurden nicht angefasst, nicht gestoerst und nicht committet.
Diese Akte wurde als einziger Pfad staged (`git add evidence/r28-welle1-2026-11-15/stack-inventory/round-2.md`, kein `git add -A`).

Produkt-Repo-Zeuge (Quarantaene-Hinweis befolgt; keine Zitation aus workers/baseharbor):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor HEAD refs/heads/develop refs/heads/main
<sha>	HEAD
14d8f17d1aa61496db9ed4d57bd4c22eda34ae95	refs/heads/develop
```

Frischer Fetch in der eigenen Zone:

```
$ mkdir -p /tmp/opencode/stackaudit2-r2/wt && cd /tmp/opencode/stackaudit2-r2/wt
$ git init -q . && git remote add origin https://github.com/mcpdev80/baseharbor.git
$ git fetch -q --prune origin 'refs/heads/*:refs/remotes/origin/*'
$ git rev-parse origin/develop
14d8f17d1aa61496db9ed4d57bd4c22eda34ae95
$ git ls-remote origin 'refs/heads/*' | wc -l
192
$ git rev-parse --is-shallow-repository
false
$ git rev-list --count origin/develop
3562
```

Der Mission-Anker 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95 ist der aktuelle
origin/develop-HEAD; `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (develop vor der
Sync-Welle, commit-date 2026-11-14T20:11:39+01:00) ist ein Vorfahre von ihm
(`git merge-base --is-ancestor` -> YES, 226 Commits Abstand).

## Commands (Zellen 1-3, verbatim)

```bash
# PR-Zeugen (API; identisch zu gh pr view --json state/isDraft/baseRefName/headRefName/headRefOid)
for n in <30 PRs>; do gh api repos/mcpdev80/baseharbor/pulls/$n \
  --jq '[.number,.state,(.draft|tostring),.base.ref,.head.ref,.head.sha]|@tsv'; done

# Branch-Wahrheit (ls-remote)
git ls-remote https://github.com/mcpdev80/baseharbor 'refs/heads/*'

# Sync-Stand pro Branch-HEAD (nach fetch in /tmp/opencode/stackaudit2-r2/wt)
git merge-base --is-ancestor 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95 <branch-head> \
  && echo SYNCED || echo NOT-SYNCED
git rev-list --count <merge-base>..<branch-head>   # ahead
git rev-list --count <merge-base>..14d8f17d1aa61496db9ed4d57bd4c22eda34ae95   # behind

# PR-Head vs Branch-Head
join prs.tsv branchheads.tsv auf head-ref und vergleichen sha-Felder
```

## Zelle 1 - Inventur + DRIFT-Pruefung (30 PRs)

Spalten: PR | state | isDraft | base-ref-name | head-ref | PR-head-SHA (gh) | ls-remote-HEAD desselben Branch | Ergebnis

| 1575 | open | true | `develop` | `lane-0428-075-perses-seam` | `66ff93d1cfe1` | `66ff93d1cfe1` | ok |
| 1577 | open | true | `develop` | `0428-092-perses-boundary` | `ab9086f5fc39` | `ab9086f5fc39` | ok |
| 1578 | open | true | `lane-0428-uid-app` | `lane-0428-uid-environment` | `36c90e270a92` | `36c90e270a92` | ok |
| 1579 | open | true | `develop` | `lane-0428-uid-app` | `22c545d8242f` | `22c545d8242f` | ok |
| 1580 | open | true | `lane-0428-uid-environment` | `lane-0428-uid-target` | `ae79d1bc7b4d` | `ae79d1bc7b4d` | ok |
| 1582 | open | true | `develop` | `lane-0428-fix-bf03` | `e196c0e2e07c` | `e196c0e2e07c` | ok |
| 1585 | open | true | `develop` | `lane-0428-fix-bf01-v2` | `55a8c0f355` | `55a8c0f355` | ok |
| 1590 | open | true | `lane-0428-075-perses-seam` | `lane-0428-080-r28-perses-selection` | `e6f5e650d048` | `e6f5e650d048` | ok |
| 1591 | open | true | `lane-0428-uid-target` | `lane-0428-env-registry` | `bdacdf392dc1` | `bdacdf392dc1` | ok |
| 1592 | open | true | `lane-0428-075-perses-seam` | `lane-0428-088-perses-runtime` | `2cc8bf6952ad` | `2cc8bf6952ad` | ok |
| 1594 | open | true | `lane-0428-env-registry` | `cli2-env-policy-head` | `e5ad8a688255` | `e5ad8a688255` | ok |
| 1595 | open | true | `lane-0428-uid-target` | `lane-0428-059-cli2-source-model` | `0963d08d022c` | `0963d08d022c` | ok |
| 1596 | open | true | `lane-0428-env-registry` | `cli2-org-env-reconcile` | `b651e614a9f0` | `b651e614a9f0` | ok |
| 1597 | open | true | `lane-0428-080-r28-perses-selection` | `perses-dashboard-databases-lane` | `22d72f3e4349` | `22d72f3e4349` | ok |
| 1598 | open | true | `lane-0428-075-perses-seam` | `lane-0428-084-perses-lifecycle` | `e866723746a5` | `e866723746a5` | ok |
| 1599 | open | true | `lane-0428-075-perses-seam` | `lane-welle2-089-perses-secure-access` | `85b01f0ff6df` | `85b01f0ff6df` | ok |
| 1600 | open | true | `develop` | `perf/0428-095-podman-runtime-batching` | `b150fd3fed38` | `b150fd3fed38` | ok |
| 1602 | open | true | `lane-0428-080-r28-perses-selection` | `lane-0428-077-r28-perses-dashboard-hosts` | `3634321d7ebc` | `d558acea55e6` | **DRIFT** |
| 1603 | open | true | `lane-0428-080-r28-perses-selection` | `lane-0428-079-r28-perses-messaging` | `62c35c9a4505` | `fed843492482` | **DRIFT** |
| 1604 | open | true | `lane-0428-080-r28-perses-selection` | `wt-0428-081` | `d681e1810791` | `bf58a9cf7254` | **DRIFT** |
| 1606 | open | true | `lane-0428-080-r28-perses-selection` | `lane-0428-078-perses-identity` | `1c124c47dc06` | `1c124c47dc06` | ok |
| 1608 | open | true | `lane-0428-075-perses-seam` | `w083-perses-datasources` | `c77c76870dc0` | `c77c76870dc0` | ok |
| 1610 | open | true | `lane-0428-075-perses-seam` | `w091-0428-091` | `4b222b1dd5b5` | `4b222b1dd5b5` | ok |
| 1613 | open | true | `lane-0428-075-perses-seam` | `w073-perses-alerts` | `53300858e21f` | `53300858e21f` | ok |
| 1614 | open | true | `lane-0428-059-cli2-source-model` | `lane-0428-062-cli2-app-status` | `63468454fe24` | `63468454fe24` | ok |
| 1615 | open | true | `cli2-env-policy-head` | `cli2-identity-secrets-head` | `22e0404c44b8` | `22e0404c44b8` | ok |
| 1616 | open | true | `lane-0428-075-perses-seam` | `lane-0428-086-perses-loki-source` | `fdb4f84b47e4` | `fdb4f84b47e4` | ok |
| 1619 | open | true | `w091-0428-091` | `lane-0428-085-perses-log-trace-dash` | `937b8a747cd7` | `937b8a747cd7` | ok |
| 1620 | open | true | `cli2-env-policy-head` | `w067-cli2-wizard-platform` | `5fadbf1c5c90` | `5fadbf1c5c90` | ok |
| 1623 | open | true | `cli2-identity-secrets-head` | `lane-0428-063-cli2-app-interact` | `1004ecd5f155` | `1004ecd5f155` | ok |

Zelle-1-Ergebnis: 30/30 PRs OPEN, 30/30 draft=true, 27 PRs ohne Drift, 3 DRIFT-Befunde
(#1602, #1603, #1604). Bei allen drei DRIFTs ist der PR-head ein Vorfahre des
Branch-heads (`merge-base --is-ancestor pr-head branch-head` -> YES); die Branches sind
also voraus, der PR zeigt auf einenaelteren Commit desselben Zweigs.

## Zelle 2 - Basis-Treue (base-ref vs deklarierte Basis-Lane)

Erwartungshorizont aus der Mission: uid-app->develop, uid-env->uid-app,
uid-target->uid-env; perses: seam->develop, kinder->seam, selection-kinder->selection,
085->tempo; cli2: source-model->uid-target, env-registry->uid-target, policy->registry,
secrets->policy, wizard->policy, interact->secrets, status->source-model.

| PR | Lane | base-ref (live) | erwartete Basis | Ergebnis |
| --- | --- | --- | --- | --- |
| 1575 | perses-seam | `develop` | `develop` | ok |
| 1577 | perses-seam (docs boundary) | `develop` | `develop` | ok |
| 1578 | uid-env | `lane-0428-uid-app` | `lane-0428-uid-app` | ok |
| 1579 | uid-app | `develop` | `develop` | ok |
| 1580 | uid-target | `lane-0428-uid-environment` | `lane-0428-uid-environment` | ok |
| 1591 | cli2-env-registry | `lane-0428-uid-target` | `lane-0428-uid-target` | ok |
| 1594 | cli2-policy | `lane-0428-env-registry` | registry-head `lane-0428-env-registry` | ok |
| 1595 | cli2-source-model | `lane-0428-uid-target` | `lane-0428-uid-target` | ok |
| 1614 | cli2-status | `lane-0428-059-cli2-source-model` | `source-model` | ok |
| 1615 | cli2-secrets | `cli2-env-policy-head` | `policy` | ok |
| 1619 | perses-085 | `w091-0428-091` | `tempo` | ok |
| 1620 | cli2-wizard | `cli2-env-policy-head` | `policy` | ok |
| 1623 | cli2-interact | `cli2-identity-secrets-head` | `secrets` | ok |
| 1590 | perses-selection-kinder | `lane-0428-075-perses-seam` | selection-Lane 1590 base = seam | ok (1590 ist selbst selection-Kind an seam; "selection-kinder->selection" betrifft 1597/1602/1603/1604/1606) |
| 1592 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1596 | (org-env-reconcile) | `lane-0428-env-registry` | registry | ok |
| 1597 | perses-selection-kinder | `lane-0428-080-r28-perses-selection` | `selection` | ok |
| 1598 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1599 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1602 | perses-selection-kinder | `lane-0428-080-r28-perses-selection` | `selection` | ok |
| 1603 | perses-selection-kinder | `lane-0428-080-r28-perses-selection` | `selection` | ok |
| 1604 | perses-selection-kinder | `lane-0428-080-r28-perses-selection` | `selection` | ok |
| 1606 | perses-selection-kinder | `lane-0428-080-r28-perses-selection` | `selection` | ok |
| 1608 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1610 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1613 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1616 | perses-kinder | `lane-0428-075-perses-seam` | `seam` | ok |
| 1582 | (bf03 fix) | `develop` | develop | ok |
| 1585 | (bf01 fix) | `develop` | develop | ok |
| 1600 | (perf 0428-095) | `develop` | develop | ok |

Zelle-2-Ergebnis: KEINE Basis-Abweichung. Alle 30 base-refs zeigen auf den Zweig der
deklarierten Basis-Lane.

## Zelle 3 - Sync-Stand nach der develop-sync-welle

Anker: origin/develop = 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95 (committiert
2026-11-16T03:26:12+01:00). Gemessen an den 30 Branch-HEADs aus Zelle 1 (frischer fetch
in /tmp/opencode/stackaudit2-r2/wt, nicht shallow, 3562 Commits auf origin/develop).
"contains-old-HEAD" prueft zusaetzlich den develop-HEAD vor der Welle
(0e9ccb582f5bd, 2026-11-14T20:11:39+01:00) als Abgrenzung "gar nicht gesynct" vs.
"teil-/alt-synct".

| Branch-Ref | Branch-HEAD | develop 14d8f17d1aa drin? | alte develop 0e9ccb582f drin? | own commits ahead | behind |
| --- | --- | --- | --- | --- | --- |
| `lane-0428-uid-app` | `22c545d8242f` | SYNCED | yes | 5 | 0 |
| `lane-0428-uid-environment` | `36c90e270a92` | SYNCED | yes | 13 | 0 |
| `lane-0428-uid-target` | `ae79d1bc7b4d` | SYNCED | yes | 16 | 0 |
| `lane-0428-fix-bf03` | `e196c0e2e07c` | SYNCED | yes | 8 | 0 |
| `lane-0428-fix-bf01-v2` | `55a8c0f3550d` | SYNCED | yes | 9 | 0 |
| `perf/0428-095-podman-runtime-batching` | `b150fd3fed38` | SYNCED | yes | 6 | 0 |
| `lane-0428-075-perses-seam` | `66ff93d1cfe1` | SYNCED | yes | 13 | 0 |
| `lane-0428-080-r28-perses-selection` | `e6f5e650d048` | SYNCED | yes | 17 | 0 |
| `perses-dashboard-databases-lane` | `22d72f3e4349` | SYNCED | yes | 21 | 0 |
| `lane-0428-084-perses-lifecycle` | `e866723746a5` | SYNCED | yes | 16 | 0 |
| `lane-0428-088-perses-runtime` | `2cc8bf6952ad` | SYNCED | yes | 15 | 0 |
| `lane-welle2-089-perses-secure-access` | `85b01f0ff6df` | SYNCED | yes | 19 | 0 |
| `w083-perses-datasources` | `c77c76870dc0` | SYNCED | yes | 16 | 0 |
| `w091-0428-091` | `4b222b1dd5b5` | SYNCED | yes | 16 | 0 |
| `w073-perses-alerts` | `53300858e21f` | SYNCED | yes | 16 | 0 |
| `lane-0428-086-perses-loki-source` | `fdb4f84b47e4` | SYNCED | yes | 15 | 0 |
| `lane-0428-077-r28-perses-dashboard-hosts` | `d558acea55e6` | SYNCED | yes | 20 | 0 |
| `lane-0428-079-r28-perses-messaging` | `fed843492482` | SYNCED | yes | 20 | 0 |
| `wt-0428-081` | `bf58a9cf7254` | SYNCED | yes | 20 | 0 |
| `lane-0428-env-registry` | `bdacdf392dc1` | SYNCED | yes | 17 | 0 |
| `cli2-org-env-reconcile` | `b651e614a9f0` | SYNCED | yes | 18 | 0 |
| `cli2-env-policy-head` | `e5ad8a688255` | SYNCED | yes | 18 | 0 |
| `cli2-identity-secrets-head` | `22e0404c44b8` | SYNCED | yes | 20 | 0 |
| `lane-0428-059-cli2-source-model` | `0963d08d022c` | SYNCED | yes | 17 | 0 |
| `lane-0428-062-cli2-app-status` | `63468454fe24` | SYNCED | yes | 18 | 0 |
| `lane-0428-063-cli2-app-interact` | `1004ecd5f155` | SYNCED | yes | 22 | 0 |
| `w067-cli2-wizard-platform` | `5fadbf1c5c90` | SYNCED | yes | 19 | 0 |
| `0428-092-perses-boundary` | `ab9086f5fc39` | **NOT-SYNCED** | yes | 8 | 226 |
| `lane-0428-078-perses-identity` | `1c124c47dc06` | **NOT-SYNCED** | yes | 14 | 226 |
| `lane-0428-085-perses-log-trace-dash` | `937b8a747cd7` | **NOT-SYNCED** | yes | 16 | 226 |

Zelle-3-Ergebnis: 27/30 Branches tragen develop 14d8f17d1aa als Vorfahren
(merge-base == 14d8f17d1aa, behind=0). 3 Branches sind NICHT gesynct; alle drei haengen
an der alten develop-Spitze 0e9ccb582f (merge-base == 0e9ccb582f, behind=226) und sind
ein Vorfahr des jeweiligen sync-erfahrenen Branch-HEADs.

## Zelle 4 - Draft-Guard

Alle 30 PRs des Faechers sind draft=true -> KEIN draft-guard-Verstoss.

Nur als fremd notiert, unbewertet gemäss Mission: die Release-Welt-Pfade #1574
(draft=false, base main), #1611 (draft=false, base develop), #1612 (draft=false, base
develop), #1622 (draft=false, base develop), #1581 (draft=false, base develop) sowie
#1587, #1588, #1589 (alle draft=true, base develop).

## Befunde (du aenderst NICHTS)

B1 DRIFT-BEFUND #1602. Feld: PR-head vs branch-head. Erwartung: identisch
(Missionsregel 1). Wirklichkeit: PR #1602 zeigt auf 3634321d7ebc5227c1d3086009ee1fb610b88885
("Merge Perses selection head 8ce0df914 into perses-dashboard-hosts (r4 rebase-wave
step4)", 2026-11-16T00:47:02+01:00); der Branch lane-0428-077-r28-perses-dashboard-hosts
steht auf d558acea55e664847de6d4003d8748245b6622ca ("Merge commit
'e6f5e650d048c28004cdc59608e9205c648bb509' into HEAD", enthaelt develop 14d8f17d1aa).
Der PR-head ist Vorfahr des Branch-heads; die sync-Welle hat den Branch nach dem letzten
PR-push bewegt, der PR zeigt auf den r4-Stand ohne develop-Inhalt.
Zeuge: Zelle-1-Tabelle; `git -C wt log --oneline 3634321d7ebc..d558acea55e6`;
`git merge-base --is-ancestor` (pr-head ist ancestor of branch-head).

B2 DRIFT-BEFUND #1603. Wie B1, Lane lane-0428-079-r28-perses-messaging: PR-head
62c35c9a4505fd195a2b500530dc338150698c9a vs branch-head fed843492482b26572f093049a28e8bdcd19f777.

B3 DRIFT-BEFUND #1604. Wie B1, Lane wt-0428-081: PR-head d681e181079152e4577328b22ae39c98a0b67253
vs branch-head bf58a9cf7254f6f5ebc3d9b7f9c8679e13f54ce8.

B4 SYNC-BEFUND #1577. Lane 0428-092-perses-boundary. Erwartung nach Sync-Welle: develop
14d8f17d1aa enthaelten. Wirklichkeit: Branch-HEAD ab9086f5fc39d34348c7a5db49525cd14566c52a
(2026-11-15T11:32:21+01:00) enthaelt nur 0e9ccb582f (behind 226). PR-head == Branch-head
(kein drift): die Sync-Welle hat diesen Branch nicht erfasst.

B5 SYNC-BEFUND #1606. Lane lane-0428-078-perses-identity. Branch-HEAD 1c124c47dc06073f1cee38944a697829caee4369
(2026-11-16T00:34:58+01:00) haengt bei 0e9ccb582f fest (behind 226), trotz same-day-Commit;
nicht von der Welle erfasst.

B6 SYNC-BEFUND #1619. Lane lane-0428-085-perses-log-trace-dash. Branch-HEAD 937b8a747cd7b6e95e620f0e90cbe6f1bdba90f0
(2026-11-16T03:08:43+01:00) enthaelt develop 14d8f17d1aa NICHT, obwohl dieser erst 17
Minuten spaeter (03:26:12) auf develop gelandet war - die Welle hat also auch einen
spaeten Branch-HEAD nicht erfasst bzw. die Reihenfolge hat das verpasst. Basis von #1619
ist w091-0428-091 (der gesynct ist); 937b8a747cd7 enthaelt aber dessen sync-HEAD
bf58a9cf7254 (wt-0428-081) / 4b222b1dd5b5 nicht als develop-Inhalt: `merge-base --is-ancestor`
gegen develop -> NO, merge-base mit develop = 0e9ccb582f.

B7 DRIFT-IN-SYNC (niedrig). Die drei DRIFT-Lanes (1602/1603/1604) zeigen PR-head-seitig
auf den ungesyncten r4-Stand (3634321d/62c35c9a/d681e181, jeweils "no" bei
`merge-base --is-ancestor 14d8f17d1aa <pr-head>`), waehrend ihre Branches gesynct sind.
Der GitHub-Review/CI-Kontext dieser PRs prueft damit weiterhin den alten Stand; ein
Push/PR-sync (z. B. `gh pr sync`-Action oder ein pushloses refetch) ist faellig, bevor
Luna diese drei Kandidaten gegen develop-Grundlage reviewed.

B8 NAMENS-/LANESPRACHE (niedrig, Vorwurf-frei). Die Branches wt-0428-081,
w067-cli2-wizard-platform, w073-perses-alerts, w083-perses-datasources, w091-0428-091,
cli2-env-policy-head, cli2-identity-secrets-head, cli2-org-env-reconcile und
perf/0428-095-podman-runtime-batching folgen nicht dem lane-0428-NNN-Muster der Kette.
Keine Missionsnummer verletzt; nur als Beobachtung notiert.

Keine Befunde: Basis-Treue (Zelle 2: 30/30 ok), Draft-Guard (Zelle 4: 30/30 draft).

## Follow-up witness - a later sync wave closed the three gaps (measured at END-preparation)

While the Akte was being finalized, the three NOT-SYNCED Branches received their own
develop-merge (measured again via fresh ls-remote + fetch, no product write):

```
CHANGED 0428-092-perses-boundary: was ab9086f5fc39... now 5e8d138cd659cbd7a72fde4713b3b1389b95dcdb
CHANGED lane-0428-078-perses-identity: was 1c124c47dc06... now e38ed06d24a341db3920e79c9dc3a75215bec498
CHANGED lane-0428-085-perses-log-trace-dash: was 937b8a747cd7... now fbffb965f72585b160d4fee7bcc6050287c10fc2
```

All three new HEADs: SYNCED (develop 14d8f17d1aa is an ancestor; the old r4-HEAD is an
ancestor of the new one). The other 27 Branch-HEADs were unchanged at re-measurement.
PR-side effect measured in the same pass: #1577 and #1602 #1603 #1604 now show PR-head ==
branch-head (drift cleared as the merge landed on the PR Branch), while #1606 and #1619
show the reverse pattern (PR-head 1c124c47dc06 / 937b8a747cd7 older than their synced
Branch-heads e38ed06d24a3 / fbffb965f725):

| PR | base-ref | head-ref | PR-head (gh) | ls-remote Branch-HEAD | Ergebnis |
| --- | --- | --- | --- | --- | --- |
| 1577 | `develop` | `0428-092-perses-boundary` | `5e8d138cd659` | `5e8d138cd659` | ok (war ok, jetzt synced) |
| 1602 | `lane-0428-080-r28-perses-selection` | `lane-0428-077-r28-perses-dashboard-hosts` | `d558acea55e6` | `d558acea55e6` | ok (Drift behoben) |
| 1603 | `lane-0428-080-r28-perses-selection` | `lane-0428-079-r28-perses-messaging` | `fed843492482` | `fed843492482` | ok (Drift behoben) |
| 1604 | `lane-0428-080-r28-perses-selection` | `wt-0428-081` | `bf58a9cf7254` | `bf58a9cf7254` | ok (Drift behoben) |
| 1606 | `lane-0428-080-r28-perses-selection` | `lane-0428-078-perses-identity` | `1c124c47dc06` | `e38ed06d24a3` | **DRIFT (neu)** |
| 1619 | `w091-0428-091` | `lane-0428-085-perses-log-trace-dash` | `937b8a747cd7` | `fbffb965f725` | **DRIFT (neu)** |

Befund-Status zum END-Zeitpunkt: B1/B2/B3 durch die spaetere Welle behoben; B4/B5/B6
(Sync-Luecken) behoben; dafuer zwei neue DRIFT-Befunde (#1606, #1619) mit derselben
Ursache (Merge-Welle schreibt den Branch, PR-Ref hinkt nach). Da die Mission
read-only ist, wurde NICHTS nachgezogen; dies ist der reine Zeugnis-Stand.

Nachziehen des PR-Zeugs im selben Zeitraum (gh api, 30 PRs): die PR-heads folgen den
Branch-Merges, sodass zuletzt KEIN PR mehr driftet und KEIN Branch mehr ungesynct ist.
Die zwei neuen Drifts (#1606 #1619) waren ein Moment des laufenden Wellenprozesses und
sind behoben; B1-B7 gelten damit als erledigt, B8 bleibt als Beobachtung stehen.

## Final witness (END-Vorbereitung, 2026-11-16 ~04:25 UTC+1)

```
$ gh api repos/mcpdev80/baseharbor/pulls/<n> ... (30 PRs, 30 Aufrufe)
  30/30: state=open, draft=true, base-ref unveraendert (Zelle-2-Erwartungen alle erfuellt)
$ git -C wt ls-remote origin 'refs/heads/*'   # 192 refs
  PR-head == branch-head fuer alle 30 head-refs: 0 DRIFT
$ git -C wt merge-base --is-ancestor 14d8f17d1aa <branch-head>   # 30 Branches
  30/30 SYNCED (0 nicht-synct)
```

## Summary (counts)

Messzeitpunkt A (Erstinventur, ~03:50 UTC+1):
- PRs untersucht: 30 (alle offen, alle draft)
- DRIFT-Befunde: 3 (#1602 #1603 #1604)
- nicht-syncte Branches: 3 (0428-092-perses-boundary, lane-0428-078-perses-identity,
  lane-0428-085-perses-log-trace-dash; alle bei 0e9ccb582f, behind 226)
- draft-verstoesse im Faecher: 0
- basis-abweichungen: 0

Messzeitpunkt B (END-Vorbereitung, ~04:15 UTC+1): 0 nicht-syncte Branches, aber 2 neue
DRIFT-Befunde (#1606 #1619) durch die nachlaufende Sync-Welle; 3 alte Drifts behoben.

## GRENZEN / cleanliness witnesses (read-only)

- Kein Write auf baseharbor (Produkt): nur `gh api` (read) + `git ls-remote` + Fetch in
  die eigene Zone /tmp/opencode/stackaudit2-r2. `git -C .../workers/baseharbor` wurde
  NICHT fuer Remote-Realitaet zitiert (Quarantine-Regel).
- Kein Write auf baseharbor-plan-Karten (`git show --name-only` des Evidence-Commits: nur
  die Akte), kein plan.py claim/render, keine .github/**-Aenderung, kein Rerun/dispatch.
- Keine Subagenten; keine docker/podman/compose-Projekte gestartet (Host-Container-Liste
  unveraendert, keine VM genutzt).
- Scratch: /tmp/opencode/stackaudit2-r2/{wt,prs.tsv,branchheads.tsv,sync.tsv,...};
  Board-Datei: /home/marcel/dev/baseharbor-ecosystem/workers/todos/mission-stackaudit2.md.json.

## origin/main witness (second-to-last action)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse HEAD
39241a59f1333684363600c4a491d477c2a34c71
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse origin/main
39241a59f1333684363600c4a491d477c2a34c71
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan merge-base --is-ancestor b42d5c49 HEAD
yes   # base attestation: develop-Sync-Stand vor dieser Akte, b42d5c49, ist Vorfahr
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan log --oneline --author-date-order b42d5c49..HEAD
39241a59 evidence(stackaudit r2): final candidate line in END block
7cfd5687 evidence(stackaudit r2): cells 3-4 complete, findings B1-B8, follow-up sync-wave witness, END block
277be4e7 evidence(stackaudit r2): refresh origin/main witness to final SHA ecf2a967
ecf2a967 evidence(stackaudit r2): complete cells 3-4, findings B1-B8, origin witness and END block
acda8a06 evidence(stackaudit r2): stack inventory 0.4.28 fan after develop sync wave - 3 drift, 3 not-synced, 0 base deviations, 0 draft violations
fa9d734c evidence(perses sync-welle r28 r1): add seam-integrity STOP-check; all 159 seam-only files preserved where develop untouched
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only HEAD | grep -i stack-inventory
evidence/r28-welle1-2026-11-15/stack-inventory/round-1.md
evidence/r28-welle1-2026-11-15/stack-inventory/round-2.md
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main
39241a59f1333684363600c4a491d477c2a34c71	refs/heads/main
```

Die Akte ist auf origin/main (ls-tree bestaetigt den Pfad), ls-remote zeugt 39241a59 als
remote main. Die funf Commits acda8a06..39241a59 sind ausschliesslich diese Akte
(round-2.md); fa9d734c gehoert einer anderen Lane (sync-welle seam-integrity) und wurde
per pull --rebase vor dem Push integriert - keine Aenderung an meiner Akte, kein Einfluss
auf die Zeugen dieser Mission.

## END

END_DONE mission-stackaudit2.md: 0.4.28-Faecher r2-Inventur (30 PRs) abgeschlossen,
read-only, 0 Karten-/PR-/Produkt-Aenderungen. Messzeitpunkt A: 3 DRIFT-Befunde (#1602
#1603 #1604 - PR-head auf altem r4-Stand, Branch bereits develop-synced), 3 nicht-syncte
Branches (0428-092-perses-boundary, lane-0428-078-perses-identity,
lane-0428-085-perses-log-trace-dash; alle bei 0e9ccb582f, behind 226), 0 draft-verstoesse,
0 basis-abweichungen. Messzeitpunkte B/C (END-Vorbereitung): eine nachlaufende Sync-Welle
hat alle Branches auf develop 14d8f17d1aa gehoben und die PR-heads nachgezogen; Final-Zeugnis:
0 Drift, 0 nicht-synct, 0 draft-verstoesse, 0 basis-abweichungen. Candidate:
baseharbor-plan c5ac6dcfe754076c78164241b7a574d5d45a31f2 (evidence only, base-Zeuge
b42d5c49..: nur eigene Akten-Commits + ein fremder, unveraenderter Lane-Commit fa9d734c).
Hinweis: ein parallel aktiver Pfad evidence/r28-welle1-20261115/cli2-app-export/round-1.md
(andere Lane, 04:12) wurde nicht angefasst, nicht committet und nicht gestasht.
