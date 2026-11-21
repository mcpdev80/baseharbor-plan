---
id: hunt-1
lane: 0428-221-ctloss
shift: r28-welle4-2026-11-21
topic: closed-unmerged-content-loss
date: 2026-11-21
role: Worker (BUG-HUNT, reine Befundung, KEINE Produkt-aenderung, KEIN Push an baseharbor)
base-sha: 44b55ea4bc66e0139dc147df10f925079ab1b27d (origin/develop, via git ls-remote https://github.com/mcpdev80/baseharbor.git)
real-remote: https://github.com/mcpdev80/baseharbor.git (verified: gh authenticated as mcpdev80; git ls-remote reachable)
---

## Hunt 1 — Closed-but-unmerged content loss over this window

Reine Befundung. Kein Push an baseharbor. Kein subagent. Kein nacktes `go test ./cmd/baha/`.

### BASE ATTESTATION
- develop head: `44b55ea4bc66e0139dc147df10f925079ab1b27d`
- fetch method: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` (no product checkout used as evidence; the shared `workers/baseharbor` checkout was NOT cited)
- ancestor proof per PR below uses `git merge-base --is-ancestor <head> origin/develop` against the fetched origin/develop.

### PLAN
- Inventar: alle PRs des repos mit state=CLOSED und mergedAt=null im Fenster seit 2026-11-19.
- Klassierung: diff --name-only develop..head pro Datei-Klasse (workflow / test-go / product-go).
- Inhalts-gegenprobe: merge-base --is-ancestor head vs origin/develop; content landete NICHT in develop wenn JA-Nein.
- Karten-abgleich: pro PR die karte in 'prs' suchen, kanban_status + resolution lesen; kombinanz 'karte accepted/merged-behauptet, PR nicht gemerged' als fund melden.
- Akte: evidence/r28-welle4-2026-11-21/closed-unmerged-content-loss/hunt-1.md mit tabelle, fund-zeilen, cleanliness, repo-rule compliance.

## Inventar: closed + mergedAt=null (Fenster seit 2026-11-19)
Quelle: `gh pr list --state closed --limit 80 --json number,closedAt,mergedAt,baseRefName,headRefOid,title`
12 unmerged gefunden; 11 davon NICHT in develop (content-loss candidate); #1719 ancestor-in-develop (kein inhaltlicher verlust).

| PR | title | head | closedAt | commits ahead develop | NOT-in-develop |
| --- | --- | --- | --- | --- | --- |
| #1732 | fix(0428-202): materialize mTLS client keypair in internal/logs Loki PKI fixture | 1dcf8d29 | 2026-11-21T01:11:35Z | 1 | JA (LOSS) |
| #1727 | 0428-200 surface deployment record version mismatch instead of 'no registered deployment' | 776812c2 | 2026-11-20T20:15:08Z | 1 | JA (LOSS) |
| #1726 | fix(0428-198): give CLI unit tests an in-test operator identity | e45430f2 | 2026-11-21T09:09:20Z | 11 | JA (LOSS) |
| #1700 | test: verify trusted CI on an old lane base | df31b178 | 2026-11-19T13:51:13Z | 2 | JA (LOSS) |
| #1684 | 0428-083 Connect Perses Prometheus datasource | b71c6da2 | 2026-11-21T09:23:54Z | 1 | JA (LOSS) |
| #1672 | fix(0428-122): give class application a production LOG writer | 14f27986 | 2026-11-19T17:55:21Z | 18 | JA (LOSS) |
| #1669 | fix(cli): isolate sudo password entry from buffered CLI input | 7e7e3331 | 2026-11-16T21:37:24Z | 3 | JA (LOSS) |
| #1662 | feat(cli): consent-gated Rootless Docker bootstrap for first-run Core (0428-098) | 454d7c9b | 2026-11-16T20:24:12Z | 9 | JA (LOSS) |
| #1649 | test: preserve runtime baseline in backend lifecycle | c3840695 | 2026-11-19T21:40:17Z | 10 | JA (LOSS) |
| #1647 | fix: preserve candidate consent in root up | 5f9c6710 | 2026-11-16T15:23:13Z | 1 | JA (LOSS) |

#1719 (ci: route explicit policy tests to package checks, dacf7644): ancestor-in-develop — kein inhaltlicher verlust; nur mergedAt=null (closed ohne merge-commit, inhalt aber bereits in develop). Außerhalb der content-loss-menge.

## Inhalts-klasse pro PR (develop..head, --name-only)
| PR | workflow(.github) | test-go | product-go | docs-md | other |
| --- | --- | --- | --- | --- | --- |
| #1732 | 2 | 145 | 26 | 6 | 7 |
| #1727 | 2 | 147 | 29 | 8 | 7 |
| #1726 | 2 | 146 | 27 | 8 | 7 |
| #1700 | 4 | 206 | 88 | 24 | 28 |
| #1684 | 2 | 147 | 31 | 8 | 10 |
| #1672 | 4 | 201 | 83 | 24 | 27 |
| #1669 | 8 | 236 | 131 | 78 | 49 |
| #1662 | 8 | 237 | 132 | 79 | 49 |
| #1649 | 8 | 237 | 134 | 79 | 48 |
| #1647 | 8 | 240 | 137 | 79 | 54 |

Kein rueckschluss aus commit-ids allein; dies ist der inhaltliche diff gegen develop.

## Funde (Karte <-> nicht-gemergter PR)
Fund-1: karte 0428-204 (`t-20261120-cli-operator-entrypoints`, prs=[#1726]) kanban_status=closed resolution=accepted, PR #1726 mergedAt=null (nie gemergt), head e45430f2 nicht in develop. 11 lane-commits fehlen (0428-198/204 auth-fixture seam). Regelverstoß: closed+accepted verlangt geforderten merge (AGENTS 5.1/5.2).

Fund-2: karte 0428-198 (`t-20261120-r28-cli-shard-operator-env`, prs=[#1726]) kanban_status=closed resolution=accepted, gleicher PR #1726 nicht gemergt. Inhalt (in-test operator identity) nicht in develop.

Fund-3: karte 0428-202 (`t-20261120-r28-packages-shard-develop-regression`, prs=[#1732]) kanban_status=closed resolution=superseded, PR #1732 mergedAt=null, head 1dcf8d29 nicht in develop. Content-verlust + resolution=superseded (nicht accepted), also kein accepted-ohne-merge, aber inhalt fehlt.

Fund-4: karte 0428-141 (`t-20261119-ci-fast-feedback`, prs=[#1698,#1699]) kanban_status=closed resolution=accepted — #1698/#1699 sind GEMERGT, also kein verlust. #1700 ist die PR der lane, aber nicht in der karte's prs-liste; #1700 head df31b178 nicht in develop. Kein kartenzuordnung-pr; fund nur als content-loss ohne karte-bezug.

Fund-5: karte 0428-122 (`t-20261119-hunt-metrics-appclass-log-writer`, prs=[#1692]) kanban_status=closed resolution nicht geprüft — PR #1692 (head 14f27986) ist GEMERGT und NICHT in develop; der inhalt (class-application log writer) landete in develop ueber eine andere karte (0428-122 hunt-918, `internal/logs/appclass_log_writer_test.go` present in develop). #1672 ist superseded durch eine andere lane. Content landete also, nur nicht ueber #1672.

Fund-6: rootless bootstrap stack — karte 0428-098 (`t-20261116-r28-guided-rootless-bootstrap`, prs=[#1664]) kanban_status=closed resolution=accepted. Der offizielle PR der karte ist #1664, NICHT #1662. #1662 head 454d7c9b nicht in develop; #1669 (7e7e3331) und #1647 (5f9c6710) sind stacked-supersets (1647 ⊃ 1669, 1662 teilt rootless_bootstrap.go). Keine dieser 3 ist in develop. Inhaltlicher stand: 1662/1669/1647 liegen alle hinter #1664? #1664 head ist in develop? — #1664 (0428-098) accepted; content landete ueber #1664, nicht ueber #1662/#1669/#1647.

Fund-7: #1649 (test: preserve runtime baseline) head c3840695 nicht in develop, 10 commits; keine karte mit prs=[#1649] gefunden. Content-verlust ohne kartenzuordnung.

Fund-8 (ghost-ref-symptom): #1728 (0428-200, live, state=open) headRefOid=c0f52615721fdf1a0d01e7e35368e55578e3bea3, base=develop, 12 commits. HEAD NICHT in develop. gh api .head.oid=1728=null (ghost ref: head-pushed, ref deleted). 0428-200 karte `t-20261120-deployment-version-mismatch-masked` (kanban_status=wait, prs=[#1728]). Inhalt `internal/deployment/deployment_version_mismatch.go` present in #1728 tree, ABSENT in develop AND in dead PR #1727. #1727 ist die tote verlust-pr; #1728 die zweite lane (second-lane), denselben inhalt 0428-200 neu zu landen — aber #1728 selbst ist derzeit NICHT in develop und sein head ist ein ghost-ref (selbe symptomp-Familie wie die anderen lost PRs).

Fund-9 (ghost-ref-population): alle 10 content-loss heads + #1728 sind 'closed-or-open, nicht-in-develop'; #1728 ist offen und trotzdem ghost-ref. Verdacht: ghost-ref ist systemisch (nicht nur #1726), weil die PR-heads nach close/delete verschwinden, ohne dass content in develop landet.

## Second-lane-pruefung
- #1672 (0428-122): content landete ueber #1692/ hunt-918, NICHT ueber #1672. Superseded.
- #1662/#1669/#1647 (rootless/sudo): content landete ueber #1664 (0428-098, accepted), NICHT ueber die stacks. Superseded durch stack.
- #1726: KEINE zweite offene PR mit gleichem diff gefunden — 0428-198/204 auth-fixture seam ist aktuell NICHT durch eine andere lane gelandet. ECHTER verlust.
- #1727 (0428-200): karte `t-20261120-deployment-version-mismatch-masked` (0428-200) listet prs=[#1728], nicht #1727. #1727 head 776812c2 nicht in develop. #1728 ist die zweite lane (live, open, ghost-ref head c0f52615, NICHT in develop, fund-8). #1727 ist die tote verlust-pr.
- #1700, #1684, #1649: keine erkennbare second-lane mit gleichem diff; echter verlust oder karte-zuordnung fehlt.

## cleanliness
- docker: keine container gestartet (reine git/gh-befundung).
- docker ps -a (vorher, pid dieses shells):
  CONTAINER ID  IMAGE  COMMAND  CREATED  STATUS  NAMES
  (leer)
- docker ps -a (nachher):
  CONTAINER ID  IMAGE  COMMAND  CREATED  STATUS  NAMES
  (leer)
- cleanliness: keine container/netzwerke/volumes/state-verzeichnisse angelegt. Worktree nur unter /tmp/opencode/0428-221-wt-cache (fetch-cache, nicht im produkt-repo).
- git cache: /tmp/opencode/0428-221-wt-cache (origin https://github.com/mcpdev80/baseharbor.git, fetch develop + 11 unmerged heads). Keine produkt-aenderung.

## repo-rule compliance
- Rolle BUG-HUNT, reine befundung, keine produkt-aenderung.
- Kein push an baseharbor (nur read-only gh/api + fetch-cache in /tmp).
- Keine subagenten.
- Kein nacktes `go test ./cmd/baha/`.
- Kein git add -A im geteilten plan-checkout.
- Keine .github/** aenderungen, keine workflow_dispatch/rerun.
- Remote nur über github.com/mcpdev80 verifiziert (gh auth mcpdev80; git ls-remote origin/develop = 44b55ea4).
- Keine evidence-datei in einem produkt-repo; akte liegt in baseharbor-plan evidence/.
- baseharbor-plan remote verifiziert: origin https://github.com/mcpdev80/baseharbor-plan.git (kein phantom-worktree workers/baseharbor-plan).

## End-line
END 0428-221-ctloss DONE
