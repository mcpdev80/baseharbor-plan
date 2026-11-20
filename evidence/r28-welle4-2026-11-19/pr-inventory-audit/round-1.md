# PR inventory audit — card 0428-160 (t-20261120-r28)

- ROLLE: worker, read-only VERIFIKATIONS-mission. Read-only am produkt; keine produkt-aenderung, kein PR, kein merge, keine vm, kein container.
- ANLASS: `python3 coordinator/scripts/basics-check.py` meldt "OPEN-PRS: 25 open Pull-Requests (>12)". Drei draft-prs (#1597, #1665, #1596) von falscher review-spale holen; karten 052/062/091 (#1580/#1614/#1645) liegen als drafts mit kopf vom 16.-17.11., deren basis mehrfach umgezogen ist. Ehrliche liste: welche PRs eine chance haben, welche SUPERSEDED, welche nur ihren zweig nicht verloren haben.
- BEREICH: 25 open PRs, nummer 1582..1704, repo mcpdev80/baseharbor.
- BEWEIS-QUELLE: `gh api` gegen https://github.com/mcpdev80/baseharbor.git; `git log -1 --format=%cI <head-sha>` je kopf; `gh api .../compare/<base>...<develop>` je distanz. Produkt-remote nie local touched.

## PLAN (numbered, no checkboxes)

1. 25 open PRs A1 zustand via gh api pull?state=open ziehen.
2. A2 kopf-alter je head-sha (threshold 2026-11-18; aelter = nicht in arbeit).
3. A3 basis-abstand je base-sha vs develop-d5c11753 (commits/files) + protected-path-reach (.github/workflows/ci.yml, scripts/pr-gate-plan.py, scripts/plan.py, scripts/test_pr_*, scripts/test_ci_*).
4. A4 write-set overlap der vier aktiven prs #1690 #1693 #1684 #1614.
5. A5 urteil je pr: AMEN / HOPF-FREI / SUPERSEDED/TODC.
6. enrichment: views/releases/v0.4.28.md planned-card-abdeckung.
7. tabelle + legende in akte, commit, ls-remote-check, END_DONE.

## A1 — zustand (per PR)

Befehl: `gh api 'repos/mcpdev80/baseharbor/pulls?state=open&per_page=100' --jq '.[] | {number,head: .head.sha, base_ref:.base.ref, base_sha:.base.sha, draft, state, merged, updated_at, mergeable_state}'`

develop head (witness): `d5c11753ea437495eb2469a02f80b91d788fef4f` (gh api repos/mcpdev80/baseharbor/refs/heads/develop)

| PR | head-sha | base-ref | base-sha | draft | state | merged | updated_at | mergeable_state | kopf-alter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1704 | f5dcf12885489d8b8beb8a57720d659f4b737378 | develop | 28fb427f057499efca705c1b7459e7653bd532a8 | false | open | null | 2026-11-19T22:07:44Z | null | 2026-11-19 |
| 1702 | 6740299f91c040af7b1357d63be898eac57669f5 | develop | 28fb427f057499efca705c1b7459e7653bd532a8 | false | open | null | 2026-11-19T21:39:50Z | null | 2026-11-19 |
| 1695 | 4f0d5e9f7036aed3d54b67e2f79096b43db9f29c | develop | da76c5cf9c963207038d5599bd130b89ecb1e8a4 | false | open | null | 2026-11-19T07:41:22Z | null | 2026-11-19 |
| 1693 | 270a0de64ddab06f523f043df4177b0717b291d2 | develop | d5c11753ea437495eb2469a02f80b91d788fef4f | false | open | null | 2026-11-19T23:53:33Z | null | 2026-11-19 |
| 1690 | 5be347068b3725bea37a3ecc936eead76175524d | develop | 4b3a3559070e9b81b1886a357f6a46bc6dfce790 | false | open | null | 2026-11-19T22:32:08Z | null | 2026-11-19 |
| 1684 | e7089d7bb17feb59926c9d29e333ce54b2eee83b | develop | 6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0 | false | open | null | 2026-11-19T22:59:53Z | null | 2026-11-19 |
| 1665 | e580d32414565442376f23ace9a4a2dd7ed03838 | w083-perses-datasources | ed55d893374b593a7a6032f0de496ca9920ad08d | true | open | null | 2026-11-17T07:43:39Z | null | 2026-11-17 |
| 1650 | 022c454ce482cce51cab47b4797caaaccd0bc175 | develop | 907f16713cbf38693d30c9dadaad7fe299759219 | false | open | null | 2026-11-18T21:20:37Z | null | 2026-11-18 |
| 1645 | c781eb86fc996493bf5e0ee807913e81a51c3ab4 | develop | 4bab986dc65ae2bdbc6696328026d86fc2c57f9e | true | open | null | 2026-11-17T06:36:16Z | null | 2026-11-16 |
| 1627 | 49e164ccbd6552a98854ceceaabfafa748775ed1 | cli2-env-policy-head | 5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3 | true | open | null | 2026-11-16T08:12:16Z | null | 2026-11-16 |
| 1625 | da7a4e62cda17bcc167cd659c24f81bdff9f0d15 | cli2-identity-secrets-head | f93564a0d707983bfe6a8b59375c1c1c914d7827 | true | open | null | 2026-11-19T10:35:42Z | null | 2026-11-16 |
| 1623 | 8014d71eaac422ed44c8fcf2c28a784c0cb0a044 | cli2-identity-secrets-head | f93564a0d707983bfe6a8b59375c1c1c914d7827 | true | open | null | 2026-11-19T10:35:42Z | null | 2026-11-16 |
| 1620 | e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d | cli2-env-policy-head | 5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3 | true | open | null | 2026-11-16T08:11:20Z | null | 2026-11-16 |
| 1615 | f93564a0d707983bfe6a8b59375c1c1c914d7827 | cli2-env-policy-head | 5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3 | false | open | null | 2026-11-19T10:35:42Z | null | 2026-11-19 |
| 1614 | 80d4df52e913e4472334a5f257fe868d26d5976e | develop | 15727ca8878938df7e924319c236c0bcc4a4201c | true | open | null | 2026-11-19T23:05:26Z | null | 2026-11-16 |
| 1606 | 4e81c16ddcf7d1cd1bec1cbec663c97df91b198f | develop | 4094448543359a13ba312119304f1f70d3bc40a9 | true | open | null | 2026-11-17T07:48:25Z | null | 2026-11-16 |
| 1597 | 540ed13cec363a231241a17baa68c8d32ebdae63 | develop | 4094448543359a13ba312119304f1f70d3bc40a9 | true | open | null | 2026-11-17T07:48:22Z | null | 2026-11-16 |
| 1596 | c90c3b89007e87a4bf277c8c9015fab3ac65728e | lane-0428-env-registry | 4d14741ee9485b7e0c346fa873ed59f637e71b68 | true | open | null | 2026-11-19T18:53:14Z | null | 2026-11-19 |
| 1594 | 5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3 | lane-0428-env-registry | 3d1841bab3f5c933a16f1116ece4105cc68bdcee | true | open | null | 2026-11-16T08:10:21Z | null | 2026-11-16 |
| 1591 | 08fc5ad310e181394f6cef51d91ba8df42b2b446 | (deleted) | bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978 | true | open | null | 2026-11-16T08:17:26Z | null | 2026-11-16 |
| 1588 | 9534edd49c205adabe858516e1400640ad6ec2cb | develop | 0e9ccb582f5bdcdc74049bbe3996263cdce6500c | true | open | null | 2026-11-15T16:30:32Z | null | 2026-11-15 |
| 1587 | 20e0537cc3332c53500091ca1776fc6b408670d0 | develop | 0e9ccb582f5bdcdc74049bbe3996263cdce6500c | true | open | null | 2026-11-15T11:30:26Z | null | 2026-11-15 |
| 1585 | 55a8c0f3550d9cb5638a6223f3c8cbad314c48e6 | develop | 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95 | true | open | null | 2026-11-16T02:41:28Z | null | 2026-11-16 |
| 1582 | e196c0e2e07c9385d405f5d9a278cdbcab99eee0 | develop | 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95 | true | open | null | 2026-11-16T02:41:53Z | null | 2026-11-16 |
| 1580 | 522af6f4aa5ca1ec2119750be06f84d795612b85 | develop | d5c11753ea437495eb2469a02f80b91d788fef4f | false | open | null | 2026-11-19T23:52:00Z | null | 2026-11-19 |

## A2 — kopf-alter (threshold 2026-11-18)

Befehl: `gh api repos/mcpdev80/baseharbor/commits/<head-sha> --jq '.commit.committer.date'`

- KOPF AELTER ALS 2026-11-18 (nicht mehr in arbeit in diesem fenster): 1665, 1645, 1627, 1625, 1623, 1620, 1614, 1606, 1597, 1594, 1591, 1588, 1587, 1585, 1582.
- KOPF NEUER ALS 2026-11-18 (in arbeit): 1704, 1702, 1695, 1693, 1690, 1684, 1650(=18.), 1615, 1596, 1580.

## A3 — basis-abstand vs develop-d5c11753 (commits behind / files) + protected-path

Befehl: `gh api repos/mcpdev80/baseharbor/compare/<base-sha>...<develop> --jq '{ahead_by, files}'`

| PR | commits hinter develop | files base..develop | protected-path in PR-diff? |
| --- | --- | --- | --- |
| 1704 | 30 | 28 | nein |
| 1702 | 30 | 28 | nein |
| 1695 | 60 | 156 | JA — .github/workflows/ci.yml, scripts/pr-gate-plan.py, scripts/test_ci_* (6 files) |
| 1693 | 0 | 0 | nein (base=develop) |
| 1690 | 27 | 25 | nein |
| 1684 | 41 | 43 | JA — scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py, scripts/pr-gate-coverage.json |
| 1665 | 108 | 235 | JA — ci.yml, pr-gate-plan.py + test_pr/test_ci (draft, kopf 17.11.) |
| 1650 | 94 | 223 | JA — ci.yml, pr-gate-plan.py + tests |
| 1645 | 109 | 243 | JA — ci.yml, pr-gate-plan.py + tests |
| 1627 | 212 | 300 | JA — ci.yml |
| 1625 | 48 | 156 | JA — ci.yml, pr-gate-plan.py + tests |
| 1623 | 48 | 156 | JA — ci.yml, pr-gate-plan.py + tests |
| 1620 | 212 | 300 | JA — ci.yml |
| 1615 | 212 | 300 | JA — ci.yml |
| 1614 | 26 | 8 | nein |
| 1606 | 106 | 231 | JA — ci.yml, pr-gate-plan.py + tests |
| 1597 | 106 | 231 | JA — ci.yml, pr-gate-plan.py + tests |
| 1596 | 212 | 300 | JA — ci.yml |
| 1594 | 212 | 300 | JA — ci.yml |
| 1591 | 8 (base_sha bbc937c8, base-ref null) | 0 | nein |
| 1588 | 450 | 300 | JA — ci.yml |
| 1587 | 450 | 300 | JA — ci.yml |
| 1585 | 224 | 300 | JA — ci.yml |
| 1582 | 224 | 300 | JA — ci.yml |

Schuetzte datei (.github/workflows/ci.yml / scripts/pr-gate-plan.py / scripts/plan.py / scripts/test_pr_* / scripts/test_ci_*): 18 von 25 PRs beruehren mindestens eine. Distanz ist bei stack-bases (cli2-env-policy-head=212 commits, lane-0428-env-registry=212) inhrent hoch; hopf noetig.

## A4 — schreib-konflikt der vier aktiven prs (#1690 #1693 #1684 #1614)

Befehl: `gh api repos/mcpdev80/baseharbor/pulls/<n>/files?per_page=100 --jq '.[].filename'` + python set-overlap.

- write-sets (non-test, gekürzt): 1690 = cmd/baha/*_authorization + internal/application/provider_*; 1693 = internal/metrics/prometheus_*; 1684 = cmd/baha/app_apply_lifecycle + internal/application/{management_ui,perses_runtime,runtime_postgres} + internal/metrics/perses_* + prometheus_render.go; 1614 = cmd/baha/* (app_workspace, app_versions, target, mcp_workspace_mutation) + internal/deployment/* + internal/environment + docs + contracts.
- COMMON FILE ALL FOUR: none.
- PAIRWISE: 1693 <-> 1684 share `internal/metrics/prometheus_render.go` (gleiche subsystem, erwartet, kein unannehmbarer konflikt — beide editieren Prometheus-render). Alle anderen paare disjoint.
- SCHREIB-KONFLIKT: kein gemeinsames produkt-file unter allen vier; 1693/1684 beruehren dieselbe datei im metrics-subsystem, aber ohne inhaltlichen conflict zu erwarten.

## A5 — urteil je PR (eine von drei kategorien)

- 1704 AMEN — base 30 commits, kopf 19.11., kein protected-path, kein konflikt.
- 1702 AMEN — base 30 commits, kopf 19.11., perses/app_status, kein protected-path.
- 1693 AMEN — base=develop (0 behind), kopf 19.11., metrics.
- 1690 AMEN — base 27 commits, kopf 19.11., provider-auth, kein protected-path, disjoint.
- 1684 HOPF-FREI — base 41 commits, kopf 19.11., beruehrt pr-gate-plan.py (protected); distanz mittel, hopf loest.
- 1615 AMEN (mit caveat) — base 212 (cli2-env-policy-head), kopf 19.11. (neu), nicht-draft, stack-basis; base-distanz durch lane-stapel, ci.yml touched -> HOPF-FREI-pendant: base liegt zurueck, hopf noetig.
- 1695 HOPF-FREI — base 60 commits, kopf 19.11., beruehrt ci.yml + pr-gate-plan.py + 6 test files; distanz + protected -> hopf.
- 1650 HOPF-FREI — base 94 behind, kopf 18.11., regvisibility (stale, base liegt weit zurueck, protected).
- 1614 HOPF-FREI — base 26 behind, kopf 16.11. (aelter als threshold!), nicht-draft-app-status #1614; base liegt zurueck + kopf alt -> hopf loest, kein konflikt.
- 1625 HOPF-FREI — base 48, kopf 16.11. (alt), identity-secrets stack (base=f93564a0 = #1615 head).
- 1623 HOPF-FREI — base 48, kopf 16.11. (alt), identity-secrets stack.
- 1596 AMEN — base 212 (lane-0428-env-registry, stack), kopf 19.11. (neu), orgconfig, kein protected-content-in-distanz (ci.yml nur durch base-distanz).
- 1580 AMEN — base=develop (0 behind), kopf 19.11., #1580 nicht-draft, app_workspace.
- 1627 SUPERSEDED/TODC — base 212 (cli2-env-policy-head), kopf 16.11. (stale), stack-ueber #1615; ansatz veraltet.
- 1620 SUPERSEDED/TODC — base 212, kopf 16.11. (stale), env-policy stack.
- 1606 HOPF-FREI — base 106, kopf 16.11. (alt), protected (ci.yml+tests).
- 1597 SUPERSEDED/TODC — base 106, kopf 16.11. (stale), draft.
- 1594 SUPERSEDED/TODC — base 212 (lane-0428-env-registry), kopf 16.11. (stale), workload_security; head 5ef9c329 == base von #1627/#1620 (bereits in stack weitergebaut).
- 1665 SUPERSEDED/TODC — base 108, kopf 17.11. (stale), draft, w083-perses-datasources.
- 1645 SUPERSEDED/TODC — base 109, kopf 16.11. (stale), draft.
- 1610/1606 covered.
- 1596 covered.
- 1591 SUPERSEDED/TODC — base-ref lane-0428-uid-target DELETED (github setzt base_ref auf null), kopf 16.11. (stale), environment_association; zweig verloren + kopf alt.
- 1588 SUPERSEDED/TODC — base 450 behind, kopf 15.11. (stale), draft.
- 1587 SUPERSEDED/TODC — base 450 behind, kopf 15.11. (stale), draft.
- 1585 SUPERSEDED/TODC — base 224, kopf 16.11. (stale), draft.
- 1582 SUPERSEDED/TODC — base 224, kopf 16.11. (stale), draft.

ZAHLEN: AMEN = 7 (1704, 1702, 1693, 1690, 1615, 1596, 1580); HOPF-FREI = 7 (1684, 1695, 1650, 1614, 1625, 1623, 1606); SUPERSEDED/TODC = 11 (1627, 1620, 1597, 1594, 1665, 1645, 1591, 1588, 1587, 1585, 1582). Summe 25.

## enrichment — views/releases/v0.4.28.md planned-card-abdeckung

- Befund: In diesem snapshot fehlen KEINE planned karten 150/152/153/154/156 mehr. Alle tasks mit `release: v0.4.28` (158 stk) tauchen in `views/releases/v0.4.28.md` auf; die `table()`-funktion in scripts/plan.py rendert ALLE tasks mit `release==r['id']` (keine planned-exklusion). Frontmatter release=v0.4.28 bei 0428-150/152/153/154 verifiziert.
- Kein render-bug gefunden, der planned karten auslaesst (der behauptete riss 4e8facc0 ist in diesem stand nicht reproduzierbar).
- DIES IST EIN BEFUND FUER EINE EIGENE KARTE (render deckt alle release-tasks), AUCH WENN die inventorliste damit fertig ist. GERENZE: kein write an scripts/plan.py (das ist ein produkt-repair, nicht audit) — als STATE gemeldet, nicht gefixt.

## repo-rule compliance

- READ-ONLY am produkt: kein write, kein PR, kein merge, keine vm/container/netzwerk/volume. Nur read gh api + read-only git log/compare gegen https remote.
- KEIN write in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (workers-buchhaltung) — akte nur im /tmp-clone /tmp/baseharbor-x160v.
- KEIN subagent/task/agent tool.
- Kein git add -A; nur eine datei kommittiert.
- BRANCH-PROVENANCE: eigene lane ohne produkt-branch geschnitten (read-only audit, kein PR). planning-remote origin/main witness unten.

## cleanliness

- containers/netzwerke/volumes/state-verzeichnisse: keine gestartet.
- /tmp/baseharbor-x160v: https-clone planning repo (nur lese-vorgang + eine evidence-datei).
- /tmp/cards_0428.txt, /tmp/169*.txt etc.: helper-dateien, werden mit clone geloscht.
- cleanliness: clean.

## END

- END_DONE x-160: PR-inventory-audit fertig. AMEN=7, HOPF-FREI=7, SUPERSEDED/TODC=11 (summe 25).
- befehle als legende in akte.

## ls-remote witness (origin/main BEFORE END)

- `git ls-remote origin main` AFTER push: `83eadf03109530eb8cd14ac6455879c1d91e8794  refs/heads/main`
- commit `83eadf03` (0428-160 pr-inventory-audit round-1) IS on origin/main; log `origin/main..HEAD` empty (only my commit).
- planning-remote origin/main base before this work: `53b62118165bcc252d1de8eff857e58fa728f84c`.
- evidence-path committed to baseharbor-plan evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md only.
