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

- 1. done - Vorbereiten: gh/git/plan.py Reichweite, Zonen; Schreibpfad ausschliesslich diese Akte
- 2. done - Zelle 1: pro PR state/isDraft/base-ref/head-SHA + ls-remote-HEAD der head-Ref; Abweichung = DRIFT-BEFUND
- 3. done - Zelle 2: Basis-Treue: base-ref jedes gestapelten PRs gegen die deklarierte Basis-Lane (uid-, perses-, cli2-Kette)
- 4. done - Zelle 3: Sync-Stand pro Branch: merge-base --is-ancestor gegen origin/develop 14d8f17d1aa; Liste nicht-syncter Pfade
- 5. done - Zelle 4: Draft-Guard: alle PRs mit draft=false im Faecher; die 8 Release-Welt-Pfade nur als fremd notiert
- 6. done - Akte auf origin/main der baseharbor-plan pushen, origin-Zeuge, END-Post

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
