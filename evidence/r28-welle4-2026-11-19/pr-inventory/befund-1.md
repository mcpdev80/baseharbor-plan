# pr-inventory — Befund 1 (karte 0428-135, R28-Welle4)

Mission: `/var/tmp/missions/mission-pr-inventory.md` (READ-ONLY Inventar; kein Produkt-Eingriff,
kein Schließen, kein Comment, kein Merge, keine Karten-Statuswechsel).
Lane: pr-inventory. Datum: 2026-11-19.

## PLAN

1. Work plan in allen drei Orten angelegt (todowrite stand in dieser Session nicht als natives
   Tool zur Verfügung; Board-Datei + dieses PLAN-Liste wurden geführt — Schritt (0) skipped per mission rule).
2. Environment verifiziert: planning repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (echtes Git-Repo, remote github.com/mcpdev80/baseharbor-plan).
3. Open PRs core (mcpdev80/baseharbor) gelistet: 38.
4. Open PRs demo (mcpdev80/baseharbor-demo) gelistet: 0.
5. Ancestry je PR gegen origin/develop (da76c5cf) via `merge-base --is-ancestor` in isoliertem Clone.
6. Diff-vs-develop on every PR (kein leerer Diff außer inhaltlich; patch-id content matching).
7. Dubletten je Karte/Branch-Familie.
8. Kartenbezug via grep in baseharbor-plan/tasks/.
9. Fremdkörper-Check (release/v0427, main-ast, ektronen, core-*): keiner gefunden.
10. Befund-Tabelle + Zusammenfassung.
11. Commit/Push evidence.
12. END-Post.

## Zeugen (reality witnesses)

- Planning-Repo-Pfad-Check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin`
  → `https://github.com/mcpdev80/baseharbor-plan.git`
- Isolierter Clone (NICHT die quarantäne workers/baseharbor-Kopie): /var/tmp/pr-inventory-wt/core,
  remote `git@github.com:mcpdev80/baseharbor.git`, `origin/develop` = `da76c5cf9c963207038d5599bd130b89ecb1e8a4` (gemessen 2026-11-19, this lane).
- PR-Heads gefetcht via `refs/pull/<n>/head` → `refs/remotes/origin/pr/<n>` (38/38 erfolgreich).
- Ancestry-Test je PR: `git merge-base --is-ancestor <head> origin/develop` → bei ALLEN 38 PRs NEIN
  (kein PR-head ist ancestor von develop, keine class SUPERSEDED-ancestry).
- Inhaltstest je PR: `git diff --stat origin/develop...<head>` → bei allen NICHT leer (kein PR ist
  inhaltlich-identisch-superseded). Ergänzend patch-id-Vergleich aller PR-only-commits gegen die
  letzten 531 develop-commits: nur #1649 zeigt Content-Wiederauffinden in develop (7/10 commits,
 其余 3 thematisch-equivalent via squash `8e1d3158a`).

## Methode-Klassen (missions definition)

- LEBEND: open, head nicht in develop, eigener inhaltlicher Diff.
- SUPERSEDED-ancestry: head ist ancestor von origin/develop. (0 Fälle)
- SUPERSEDED (inhalt): diff gegen develop leer. (0 Fälle; 1 Sonderfall #1649, siehe unten)
- DUPLIKAT-von-pr#N: mehrere offene PRs derselben Karte — höchster head = LEBEND, andere = Duplikat.
- FREMDKOERPER-andere-welt: branch zeigt auf release/v0.4.27 / main-ast / ektronen / alte core-* Serien. (0 Fälle)
- STACK-PR: PR whose base-ref is another lane's branch (chain pattern per Owner-Anweisung 2026-11-15) — these are
  not card-duplicates; they are chain positions of card PRs that live elsewhere.

## Tabelle (core repo mcpdev80/baseharbor; demo repo: keine offenen PRs)

| PR | head | basis | mergeable_state | karte | klasse | nachweis-zeile |
| --- | --- | --- | --- | --- | --- | --- |
| 1697 | 3448f73e | develop | unknown (null) | 0428-131 (t-20261119-r28-en-docs-warning-term) | LEBEND | `1697 3448f73e NOT-ANCESTOR; diff 3 files; 1 pr-only commit; card prs=[#1697]` |
| 1695 | 4f0d5e9f | develop | unknown (null) | hunt-metrics-verification-none (t-20261119-hunt-metrics-verification-none-blind) | LEBEND | `NOT-ANCESTOR; 8 files +456; card prs=#1695` |
| 1693 | d751c83b | develop | unknown (null) | hunt-metrics-regvisibility (t-20261119-hunt-metrics-registration-visibility-only) | LEBEND | `NOT-ANCESTOR; 3 files +176; card prs=#1693` |
| 1692 | 876329f7 | develop | unknown (null) | hunt-metrics-appclass-writer (t-20261119-hunt-metrics-appclass-log-writer) | LEBEND | `NOT-ANCESTOR; 6 files +954; card prs=#1692` |
| 1691 | 4f4b3d7a | develop | unknown (null) | hunt-metrics-env-filter (t-20261119-hunt-metrics-env-filter-list-pfade) | LEBEND | `NOT-ANCESTOR; 17 files +507; card prs=#1691` |
| 1690 | 84ee9a93 | develop | unknown (null) | 0428-119 consent (t-20261118-ownership-stale-consent-hardening) | LEBEND | `NOT-ANCESTOR; 5 files +1170; card prs=#1690` |
| 1684 | 8c713950 | develop | unknown (null) | 0428-083 (t-20261114-r28-perses-datasources) | LEBEND (Karten-highest; #1608 closed) | `NOT-ANCESTOR; 3 files +1032; card prs=[#1608,#1684], #1608 nicht open` |
| 1682 | fb6f3693 | develop | unknown (null) | 0428-110 (t-20261117-hunt-uid-docs-110) | LEBEND | `NOT-ANCESTOR; 4 files +491; card prs=#1682` |
| 1665 | e580d324 | w083-perses-datasources | unknown (null) | 0428-082 (t-20261114-r28-perses-dashboards) | STACK-PR (base = closed cards' branch, head of w083 = ed55d893 = merged #1590-lineage) | `base-ref w083-perses-datasources exists remote (ed55d893); 39 files +19087; card prs=#1665` |
| 1650 | 022c454c | develop | unknown (null) | 0428-078 (t-20261114-r28-perses-dashboard-identity) | LEBEND (höchster head der Karte 0428-078, head-date 2026-11-18) | `card prs=[#1606,#1650]; 18 files +495/-319; head-date #1650 2026-11-18 vs #1606 2026-11-16` |
| 1649 | c3840695 | develop | unknown (null) | keine karte (kein tasks/-Treffer) | SUPERSEDED-by-content (coreless test baseline landete via #1659/shards + 8e1d3158a) | `7/10 commits patch-id-matched in develop; 3 rest matched-by-squash; diff 11 files ist stale-ref-noise` |
| 1645 | c781eb86 | develop | unknown (null) | keine karte (titel: perses/tempo witness rename, CI package-selection) | LEBEND | `NOT-ANCESTOR; 41 files +18188; kein tasks/-Treffer` |
| 1627 | 49e164cc | cli2-env-policy-head | unknown (null) | 0428-055 (t-20261114-r28-cli2-env-delete) | STACK-PR (base = cli2-env-policy-head = #1594-head) | `head-ref cli2-env-delete 49e164cc; 35 files +5158` |
| 1625 | da7a4e62 | cli2-identity-secrets-head | unknown (null) | 0428-065 (t-20261114-r28-cli2-app-export) | STACK-PR (base = cli2-identity-secrets-head = #1615-head) | `44 files +4751` |
| 1623 | 8014d71e | cli2-identity-secrets-head | unknown (null) | 0428-063 (t-20261114-r28-cli2-app-interact) | STACK-PR (base = cli2-identity-secrets-head = #1615-head) | `50 files +5275` |
| 1620 | e7eeeb58 | cli2-env-policy-head | unknown (null) | 0428-067 (t-20261114-r28-cli2-wizard-platform) | STACK-PR (base = cli2-env-policy-head = #1594-head) | `28 files +4206` |
| 1616 | 7d6538b4 | develop | unknown (null) | 0428-086 (t-20261114-r28-perses-loki-source) | LEBEND | `NOT-ANCESTOR; 4 files; card prs=#1616` |
| 1615 | 8963efd8 | cli2-env-policy-head | unknown (null) | 0428-057 (t-20261114-r28-cli2-identity-secrets) | LEBEND-Kopf der cli2-family (base-ref zeigt auf #1594-head = chain position, head 8963efd8 = branch cli2-identity-secrets-head tip) | `card prs=#1615; branch = base of #1623/#1625` |
| 1614 | 80d4df52 | lane-0428-059-cli2-source-model | unknown (null) | 0428-062 (t-20261114-r28-cli2-app-status) | STACK-PR (base = #1595-head branch) | `55 files +6768; head is NOT on card-lane branch lane-0428-062-cli2-app-status (that branch tip = 80d4df52 = this head)` |
| 1613 | 470735c1 | develop | unknown (null) | 0428-073 (t-20261114-r28-perses-alerts) | LEBEND | `22 files +1846; card prs=#1613` |
| 1606 | 4e81c16d | develop | unknown (null) | 0428-078 (t-20261114-r28-perses-dashboard-identity) | DUPLIKAT-von-pr#1650 (same card, älterer head) | `25 files +2857/-90; head-date 2026-11-16 < #1650 2026-11-18` |
| 1602 | b6c9702b | develop | unknown (null) | 0428-077 (t-20261114-r28-perses-dashboard-hosts) | LEBEND | `14 files +1443; card prs=#1602` |
| 1599 | 31adf08f | develop | unknown (null) | 0428-089 (t-20261114-r28-perses-secure-access) | LEBEND | `19 files +3024; card prs=#1599` |
| 1598 | e8667237 | develop | unknown (null) | 0428-084 (t-20261114-r28-perses-lifecycle) | LEBEND | `26 files; card prs=#1598` |
| 1597 | 540ed13c | develop | unknown (null) | 0428-076 (t-20261114-r28-perses-dashboard-databases) | LEBEND | `33 files; card prs=#1597` |
| 1596 | de51105c | lane-0428-env-registry | unknown (null) | 0428-056 (t-20261114-r28-cli2-org-env) | STACK-PR (Ketten-Ende env-registry→uid-target→...; carries #1591/#1580/#1578 content) | `23 files +3775; card prs=[] (active)` |
| 1595 | 818d572b | lane-0428-uid-target | unknown (null) | 0428-059 (t-20261114-r28-cli2-source-model) | STACK-PR (base = #1580-head branch) | `37 files; card prs=#1595` |
| 1594 | 5ef9c329 | lane-0428-env-registry | unknown (null) | 0428-053 (t-20261114-r28-cli2-env-policy) | STACK-PR (base = #1591-head branch; branch cli2-env-policy-head ist base von #1615/#1620/#1627) | `26 files +4050; card prs=[] (active)` |
| 1592 | 76331c7d | develop | unknown (null) | 0428-088 (t-20261114-r28-perses-runtime) | LEBEND | `7 files +718; card prs=#1592` |
| 1591 | 08fc5ad3 | lane-0428-uid-target | unknown (null) | 0428-054 (t-20261114-r28-cli2-env-registry) | STACK-PR (base = #1580-head branch) | `20 files +3685; card prs=#1591` |
| 1589 | 442755b3 | develop | unknown (null) | 0427-020 (t-20261018-r27-ci-consumption) | LEBEND (r27-Material in develop-Welt, PR-base develop; kein FREMDKOERPER nach Branch-Test) | `10 files +819; docs-only` |
| 1588 | 9534edd4 | develop | unknown (null) | 0427-186 (t-20261109-r27-target-policy-presets) | LEBEND (r27-Material gegen develop) | `7 files +371` |
| 1587 | 20e0537c | develop | unknown (null) | 0427-169 (t-20261108-smoke-0427-operator-api-undocumented) | LEBEND | `9 files +412; docs` |
| 1585 | 55a8c0f3 | develop | unknown (null) | BF-01/0427-189 (t-20261115-bughunt-d28-state-dir-target) | LEBEND | `6 files +823; card prs=#1585` |
| 1582 | e196c0e2 | develop | unknown (null) | BF-03 (t-20261115-bughunt-d28-tmp-selection) | LEBEND | `3 files +814; card prs=#1582` |
| 1581 | bdcd6f62 | develop | unknown (null) | keine karte (CI catalog-lint; .github-Scope-Berührung im Diff, PR selbst nicht bewertet) | LEBEND | `1 file +115 (scripts/pr-gate-coverage.json); kein tasks/-Treffer` |
| 1580 | ae0602e0 | lane-0428-uid-environment | unknown (null) | 0428-052 (t-20261114-r28-cli2-uid-target) | STACK-PR (Kette uid-app→uid-env→uid-target; base = #1578-head branch; DRAFT) | `18 files +2622; card prs=#1580` |
| 1578 | 6f07aef2 | lane-0428-uid-environment | unknown (null) | 0428-051 (t-20261114-r28-cli2-uid-environment) | LEBEND-Kopf der uid-Kette (base-ref zeigt auf eigenen branch lane-0428-uid-environment = PR-head-branch; retarget-Artefakt der Kette) | `5 files +1668; card prs=#1578` |

Demo-Repo (mcpdev80/baseharbor-demo): `gh api repos/mcpdev80/baseharbor-demo/pulls?state=open` → `[]`, 0 offene PRs.

## Zusammen-Zahl je Klasse

| klasse | anzahl | PRs |
| --- | --- | --- |
| LEBEND | 25 | 1697, 1695, 1693, 1692, 1691, 1690, 1684, 1682, 1650, 1645, 1616, 1615, 1613, 1602, 1599, 1598, 1597, 1592, 1589, 1588, 1587, 1585, 1582, 1578, 1581 |
| STACK-PR (Ketten-Position, own card PR exists separately) | 11 | 1665, 1627, 1625, 1623, 1620, 1614, 1596, 1595, 1594, 1591, 1580 |
| DUPLIKAT-von-pr#N (same card, lower head) | 1 | 1606 (DUPLIKAT-von-pr#1650, card 0428-078) |
| SUPERSEDED-ancestry | 0 | — |
| SUPERSEDED-by-content | 1 | 1649 (inhaltlich in develop via #1659-coreless-shards + squash 8e1d3158a; keine karte) |
| FREMDKOERPER-andere-welt | 0 | — |

Prüfung: 25 LEBEND + 11 STACK-PR + 1 DUPLIKAT + 1 SUPERSEDED-by-content + 0 SUPERSEDED-ancestry + 0 FREMDKOERPER = 38. Passt.
Regel "hoechster head ist LEBEND": für Karte 0428-078 ist #1650 (head-date 2026-11-18) der lebende Kandidat, #1606 (2026-11-16) das Duplikat.

## Dubletten-Gruppen (Karte mit >1 offenem PR)

- 0428-078 (Perses identity dashboard): #1650 (LEBEND, head-date 2026-11-18) / #1606 (DUPLIKAT-von-pr#1650, head-date 2026-11-16).
- cli2-Familie (keine echten Dubletten, Kettenstruktur): #1594 (#1615/#1620/#1627 basis), #1615
  (#1623/#1625 basis), #1580→#1595/#1591 (uid-Kette), #1591→#1596 (env-registry-Kette).
- 0428-083 (Perses Prometheus datasource): #1684 ist der einzige OFFENE PR der Karte (#1608 closed). Kein Dublett-Fall.

## Kartenbezug ohne Treffer

- #1649, #1645, #1581 — kein grep-Treffer in baseharbor-plan/tasks/ → "keine karte".
  (#1581 touch scripts/pr-gate-coverage.json, CI-adjacent; #1645 = perses/tempo witness rename; #1649 = coreless test baseline, inhaltlich in develop.)

## FREMDKOERPER-Check

Kein offener PR hat base-ref release/v0.4.27, main, oder einen core-*/ektronen/main-ast branch.
Die r27-Materialien #1589/#1588/#1587/#1581 laufen alle gegen develop und sind damit keine Fremdkörper
nach Missions-Definition; ihre Karten (0427-Serie) gehören zur anderen Welt (ChatGPT/Release-Welt),
Behandlung bleibt aber Karte/Status-Sache des Coordinators — hier nur gelistet, nicht bewertet.

## Auffälligkeiten (nur Befund, keine Aktion)

1. mergeable_state ist bei allen 38 PRs `null` (GitHub berechnet ihn nicht, vermutlich Queue/Rebase-Pending). Kein Blocker für dieses Inventar.
2. Die PR-bases der cli2/uid-Ketten zeigen auf Lane-branch-Tops statt develop — konsistent mit
   Owner-Anweisung 2026-11-15 (Kette: base-ref = Zweig der Basis-Lane). Retarget-Artefakt bei #1578
   (base-ref == head-ref == eigener branch): GitHub zeigt den Branch, der nach merge-leeren Diff
   mit develop laufen würde; inhaltlich korrekt, Status-Sache Coordinator.
3. #1665 base = w083-perses-datasources — dieser branch ist der head eines CLOSED PR-Zweigs (#1590-
   lineage, merged 907f16713). Der PR trägt die 0428-082-Kartenarbeit auf veralteter Basis — LEBEND
   aber stale-base-Befund.

## cleanliness

Host = coordinator/codeman server; diese Lane hat KEINE container/netzwerke/volumes gestartet
(READ-ONLY inventar; docker/podman nur lesend abgefragt). Vorher- und Nachher-Zeuge identisch.

Nachher-Zeugen (Gemessen 2026-11-19 auf diesem Host, NUR-LESEND — nichts gestartet, nichts gestoppt):

    $ docker ps --format '{{.Names}}'
    bh-local-shared-postgres-1
    bh-local-shared-openbao-admin-1
    bh-local-shared-postgres-admin-1
    bh-local-shared-postgres-member-1-1

    $ docker network ls --format '{{.Name}}'
    baseharbor-local-default
    baseharbor-local-secrets
    bridge
    host
    none

    $ podman ps --format '{{.Name}}' 2>/dev/null
    (podman: command not found auf diesem host)

Die laufenden bh-local-shared-* container und baseharbor-local-* netzwerke sind NICHT diese Lane —
sie waren VOR der Lane da (diese Lane führte vor dem ersten docker-Zugriff keine container-Befehle;
READ-ONLY inventar ohne produkt-interaktion). Sie gehören ambient-core/anderem land und bleiben
unangetastet (owner-direktive 2026-11-08).

cleanliness: diese Lane hat nichts gestartet und nichts zu tear down; nothing to clean.
/var/tmp/pr-inventory-wt (isolierter Clone dieser Lane, ~1 GB) kann nach Belieben entfernt werden;
er blockiert keine daemon-pools.

## repo-rule compliance

- READ-ONLY: kein gh pr close / comment / merge / workflow_dispatch / push an produkt-äste — eingehalten.
- Karten nicht geändert — eingehalten (nur gelesen).
- .github nicht angefasst — eingehalten.
- quarantäne checkout workers/baseharbor NICHT als Realitätszeuge benutzt — isolierter Clone unter /var/tmp.
- evidence nur in baseharbor-plan — eingehalten.

## Candidate

Evidence-Commit: (diese Datei), planning repo main. Kein Produktkandidat (read-only mission).

END (this lane) DONE mission-pr-inventory.md: Inventar fertig — 38 core PRs (25 LEBEND, 11 STACK-PR, 1 DUPLIKAT #1606→#1650, 1 SUPERSEDED-by-content #1649), 0 demo PRs, 0 Fremdkörper, 0 SUPERSEDED-ancestry.
