# Review-Compliance Audit — mission `review-compliance` (card 0428-139)

Date: 2026-11-19
Lane: review-compliance. Read-only admission verification ("ZULASSUNGSPRUEFUNG") of ALL cards in state `review` for release v0.4.28.

## PLAN

1. Verify environment: planning repo path (`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`), gh auth, `scripts/plan.py`.
2. Enumerate all cards with `kanban_status: review` for release v0.4.28.
3. Per card: extract PR number(s) from `prs`/links.
4. Per card: fetch remote truth — `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.state,.draft,.mergeable_state,.head.sha'`.
5. Per card: compare `git ls-remote origin <head-ref>` against PR head sha; record divergence.
6. Per card: locate last terminal workflow run on EXACTLY that head sha; record run id, status, conclusion.
7. Per card: count executed vs skipped jobs in that run; confirm `PR Selected Checks` (or the affected group equivalent) actually executed.
8. Per card: render ZULASSUNG (yes/no) with evidence (run id, gate file:line, or "kein lauf auf diesem kopf").
9. Host cleanliness: docker/podman ps -a before/after, "cleanliness:" line.
10. Write this evidence file (exceptions first, then compliant, command witnesses), commit + push to origin/main, verify path present on origin/main.
11. END post to coordinator session.

## Environment witnesses

- Planning repo (correct zone, per mission warning): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `https://github.com/mcpdev80/baseharbor-plan.git`).
- Enumeration: `grep -rl '^kanban_status: review' tasks/` in baseharbor-plan -> 22 cards; `python3 scripts/plan.py list --status review` agrees. All cards carry `release: v0.4.28`.
- ls-remote lane used `git ls-remote origin` through the gh-authenticated git transport (the quarantined checkout `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` was NOT cited for remote truth; all remote facts came from `gh api` + `git ls-remote origin` against github.com).
- No product repo was edited, no PR touched, no `gh pr ready`, no comment, no merge, no rerun/dispatch, no card status change, no subagent. Scratch zone: `/var/tmp/review-compliance` only.

## Verdict criteria (mission)

ZULASSUNG = `state=open` AND `draft=false` AND `mergeable_state != 'dirty'` AND a terminal run SUCCESS on EXACTLY the PR head sha AND in that run `PR Selected Checks` (or the affected group's equivalent) actually EXECUTED — draft-only cells do not suffice (precedent #1613, akte `evidence/r28-welle4-2026-11-19/gate-routing/probe-1.md`).

## Summary

- 22 review cards, 23 PR links (card 0428-083 lists #1608 superseded + #1684 current).
- ZULASSUNG JA: 8 cards (0428-073, -077, -083, -086, -088, -089, -110, -124).
- Exceptions: 14 cards.
- Systemic exception class A (10 cards): PR is a DRAFT — by workflow policy the normal cells are skipped (`draft == false` guards at `.github/workflows/ci.yml` lines 514/956/980/1012/1055/1094/1137/1160/1282/1313/1332/1349/1386; Draft cells at 1481/1535, per gate-routing probe akte). Draft-only green is NOT verification.
- Systemic exception class B (6 cards): NO CI run exists at all on the current head sha (`head_sha`-filtered run listing empty; `mergeable_state: unknown`). Witnessed for #1625, #1623, #1627, #1620, #1615, #1610.
- Exception class C (5 cards): `mergeable_state: dirty` (conflict with base) — #1580, #1597, #1603, #1665, #1610.
- Exception class D (3 cards): PR is CLOSED while the card sits in `review` — #1603, #1619, #1610. Card must point at the successor PR or move out of review.

## Ausnahmen (exceptions first)

| Card | PR | state | draft | mergeable | head sha | ls-remote | run on head | executed cells | ZULASSUNG | Grund (belegt) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0428-065 cli2-app-export | #1625 | open | TRUE | clean | `da7a4e62cda17bcc167cd659c24f81bdff9f0d15` | match | KEIN LAUF auf diesem kopf | none (0 jobs) | NO | draft + kein lauf auf diesem kopf |
| 0428-063 cli2-app-interact | #1623 | open | TRUE | clean | `8014d71eaac422ed44c8fcf2c28a784c0cb0a044` | match | KEIN LAUF auf diesem kopf | none | NO | draft + kein lauf auf diesem kopf |
| 0428-062 cli2-app-status | #1614 | open | TRUE | clean | `80d4df52e913e4472334a5f257fe868d26d5976e` | match | 43840657678 success | 6/30 (Draft cells only) | NO | draft; PR Selected Checks = skipped |
| 0428-055 cli2-env-delete | #1627 | open | TRUE | clean | `49e164ccbd6552a98854ceceaabfafa748775ed1` | match | KEIN LAUF auf diesem kopf | none | NO | draft + kein lauf auf diesem kopf |
| 0428-057 cli2-identity-secrets | #1615 | open | false | clean | `f93564a0d707983bfe6a8b59375c1c1c914d7827` | match | KEIN LAUF auf diesem kopf | none | NO | kein lauf auf diesem kopf (head committed 2026-11-19T10:27:34Z, CI never fired on it) |
| 0428-059 cli2-source-model | #1595 | open | TRUE | clean | `818d572b982a69e2caebd5474a4ba270ed21fd41` | match | 43814664405 success | 6/30 (Draft cells only) | NO | draft; PR Selected Checks = skipped |
| 0428-052 cli2-uid-target | #1580 | open | TRUE | DIRTY | `ae0602e02882619dea151dc82d62b98b72481566` | match | 43812464881 success | 6/30 (Draft cells only) | NO | draft + mergeable_state dirty; PR Selected Checks = skipped |
| 0428-067 cli2-wizard-platform | #1620 | open | TRUE | clean | `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d` | match | KEIN LAUF auf diesem kopf | none | NO | draft + kein lauf auf diesem kopf |
| 0428-076 perses-dashboard-databases | #1597 | open | TRUE | DIRTY | `540ed13cec363a231241a17baa68c8d32ebdae63` | match | 43810693985 success | 6/30 (Draft cells only) | NO | draft + mergeable_state dirty; PR Selected Checks = skipped |
| 0428-079 perses-messaging | #1603 | CLOSED | TRUE | DIRTY | `fed843492482b26572f093049a28e8bdcd19f777` | REF-MISSING (branch deleted) | 43794628957 success (draft cells only) | 6/30 | NO | card shows closed PR + dirty + draft; kein offener kandidat |
| 0428-082 perses-dashboards | #1665 | open | TRUE | DIRTY | `e580d32414565442376f23ace9a4a2dd7ed03838` | match | KEIN PR-lauf; nur dispatch 43999100666 FAILURE | 2 (dispatch) | NO | draft + dirty + kein terminaler PR-erfolg auf diesem kopf |
| 0428-084 perses-lifecycle | #1598 | open | false | blocked | `831c2bea8bd9b87aac71588353318e66d582c901` | match | 44499778660 FAILURE | 13/33 | NO | letzter terminaler lauf auf diesem kopf failed: `PR · Go unit · cli-0` + `PR · Go unit · cli-3` failed (step "Execute selected Go tests with isolated PostgreSQL"), `PR Selected Checks` = "Require complete selected Go shard coverage" failure |
| 0428-085 perses-log-trace-dash | #1619 | CLOSED | TRUE | unknown | `fbffb965f72585b160d4fee7bcc6050287c10fc2` | ref present | 43796266469 (dispatch) FAILURE | 2 (dispatch) | NO | card shows closed PR + draft; kein terminaler PR-erfolg auf diesem kopf |
| 0428-091 perses-tempo-source | #1610 | CLOSED | TRUE | DIRTY | `d57ab527524048bddc0af7bb08009edbb4d32033` | ref present | KEIN LAUF auf diesem kopf | none | NO | card shows closed PR + dirty + kein lauf auf diesem kopf |

## Erfuellte (ZULASSUNG JA)

| Card | PR | state | draft | mergeable | head sha | ls-remote | terminal run (success) | executed cells | witness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0428-073 perses-alerts | #1613 | open | false | clean | `d8838f622b551cdc8a7f8e8320c3f122b2ae5783` | match | 44495425072 | 15/33, incl. `PR Selected Checks` success | run 44495425072 |
| 0428-077 perses-dashboard-hosts | #1602 | open | false | behind | `b6c9702ba490d5d3fbdd52ef8d6dfbfad04e5318` | match | 44408040964 | 15/33, incl. `PR Selected Checks` success | run 44408040964 |
| 0428-083 perses-datasources | #1684 (supersedes closed #1608) | open | false | clean | `ab6932296f1f24c2024810f10b155633d931f7d4` | match | 44505333646 | 15/33, incl. `PR Selected Checks` success | run 44505333646 |
| 0428-086 perses-loki-source | #1616 | open | false | behind | `7d6538b45cac40f4e8fa0de8aa97fcede7893e6c` | match | 44052892273 | 14/33, incl. `PR Selected Checks` success | run 44052892273 |
| 0428-088 perses-runtime | #1592 | open | false | behind | `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9` | match | 44467712113 | 14/33, incl. `PR Selected Checks` success | run 44467712113 |
| 0428-089 perses-secure-access | #1599 | open | false | behind | `31adf08fa1d0dc77f3698dad23bde3654d2f5967` | match | 44408326474 | 20/33, incl. `PR Selected Checks` success | run 44408326474 |
| 0428-110 hunt-uid-docs | #1682 | open | false | behind | `fb6f36936924ca07a9de512c113dc138d38360f1` | match | 44407800144 | 20/33, incl. `PR Selected Checks` + `PR · Selected Runtime (docker · lifecycle)` success | run 44407800144 |
| 0428-124 metrics-verification-none | #1695 | open | false | clean | `4f0d5e9f7036aed3d54b67e2f79096b43db9f29c` | match | 44478473607 | 15/33, incl. `PR Selected Checks` success | run 44478473607 |

Notes for the JA set: `mergeable_state: behind` is not a disqualifier under the mission criteria (only `dirty` is). The runs 44408040964 / 44408326474 / 44407800144 / 44478473607 date from 2026-11-18/19 and are the latest terminal runs on the CURRENT head sha (verified by `head_sha` filter); all Draft cells are `skipped` in them, i.e. these are non-draft routed runs.

## Command witnesses (per step, exactly as run)

Enumeration (step 2):

```
$ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ grep -rl '^kanban_status: review' tasks/ | wc -l
22
$ python3 scripts/plan.py list --status review
<22 lines, all v0.4.28>
```

PR truth (step 4), all 23 links:

```
$ while IFS=$'\t' read -r id pr; do
    gh api "repos/mcpdev80/baseharbor/pulls/$pr" --jq '[.state,(.draft|tostring),.mergeable_state,.head.sha,.head.ref,.base.ref,.mergeable]|join("|")'
  done < prs.tsv
1625	open|true|clean|da7a4e62...|lane-0428-065-cli2-app-export|cli2-identity-secrets-head|true
1623	open|true|clean|8014d71e...|lane-0428-063-cli2-app-interact|cli2-identity-secrets-head|true
1614	open|true|clean|80d4df52...|lane-0428-062-cli2-app-status|lane-0428-059-cli2-source-model|true
1627	open|true|clean|49e164cc...|cli2-env-delete|cli2-env-policy-head|true
1615	open|false|clean|f93564a0...|cli2-identity-secrets-head|cli2-env-policy-head|true
1595	open|true|clean|818d572b...|lane-0428-059-cli2-source-model|lane-0428-uid-target|true
1580	open|true|dirty|ae0602e0...|lane-0428-uid-target|lane-0428-uid-environment|false
1620	open|true|clean|e7eeeb58...|w067-cli2-wizard-platform|cli2-env-policy-head|true
1613	open|false|clean|d8838f62...|w073-perses-alerts|develop|true
1597	open|true|dirty|540ed13c...|perses-dashboard-databases-lane|develop|false
1602	open|false|behind|b6c9702b...|lane-0428-077-r28-perses-dashboard-hosts|develop|true
1603	closed|true|dirty|fed84349...|lane-0428-079-r28-perses-messaging|develop|false
1665	open|true|dirty|e580d324...|lane-0428-082-perses-dashboards|w083-perses-datasources|false
1608	closed|false|unknown|ed55d893...|w083-perses-datasources|develop|
1684	open|false|clean|ab693229...|lane-0428-083-datasources-r2|develop|true
1598	open|false|blocked|831c2bea...|lane-0428-084-perses-lifecycle|develop|true
1619	closed|true|unknown|fbffb965...|lane-0428-085-perses-log-trace-dash|w091-0428-091|
1616	open|false|behind|7d6538b4...|lane-0428-086-perses-loki-source|develop|true
1592	open|false|behind|76331c7d...|lane-0428-088-perses-runtime|develop|true
1599	open|false|behind|31adf08f...|lane-welle2-089-perses-secure-access|develop|true
1610	closed|true|dirty|d57ab527...|w091-0428-091|lane-0428-075-perses-seam|false
1682	open|false|behind|fb6f3693...|lane-0428-110-mutation-loud|develop|true
1695	open|false|clean|4f0d5e9f...|lane-0428-124-metrics-verification-none|develop|true
```

ls-remote comparison (step 5):

```
$ while ...; do ref=$(gh api repos/mcpdev80/baseharbor/pulls/$pr --jq '.head.ref')
    git ls-remote origin "refs/heads/$ref"; done
(23 lines) — every head-ref sha equals .head.sha EXCEPT refs/heads/lane-0428-079-r28-perses-messaging:
  1603	lane-0428-079-r28-perses-messaging	REF-MISSING   (branch deleted with the closed PR)
```

Run lookup on exact head sha (step 6):

```
$ gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=<40>" --jq '.workflow_runs[]|[.id,.name,.event,.status,.conclusion,.created_at]|@tsv'
(Everything not listed below was [] — "kein lauf auf diesem kopf".)
43840657678	CI · PR #1614	pull_request	completed	success	2026-11-16T09:32:28Z
43816873125	CI · lane-0428-059...	workflow_dispatch	completed	failure	2026-11-16T06:27:29Z
43814664405	CI · PR #1595	pull_request	completed	success	2026-11-16T06:07:43Z
43812835617	CI · lane-0428-uid-target	workflow_dispatch	completed	failure	2026-11-16T05:50:32Z
43812464881	CI · PR #1580	pull_request	completed	success	2026-11-16T05:47:03Z
44495425072	CI · PR #1613	pull_request	completed	success	2026-11-19T09:19:57Z
43810693985	CI · PR #1597	pull_request	completed	success	2026-11-16T05:30:34Z
44408040964	CI · PR #1602	pull_request	completed	success	2026-11-18T22:05:01Z
43794628957	CI · PR #1603	pull_request	completed	success	2026-11-16T02:51:09Z
43999100666	CI · lane-0428-082...	workflow_dispatch	completed	failure	2026-11-17T01:54:45Z
44505333646	CI · PR #1684	pull_request	completed	success	2026-11-19T10:24:14Z
44499778660	CI · PR #1598	pull_request	completed	failure	2026-11-19T09:48:23Z
44499770541	CI · PR #1598	pull_request	completed	cancelled	2026-11-19T09:48:20Z
43796266469	CI · lane-0428-085...	workflow_dispatch	completed	failure	2026-11-16T03:07:45Z
44052892273	CI · PR #1616	pull_request	completed	success	2026-11-17T09:09:01Z
44467712113	CI · PR #1592	pull_request	completed	success	2026-11-19T05:48:44Z
44408326474	CI · PR #1599	pull_request	completed	success	2026-11-18T22:06:40Z
44407800144	CI · PR #1682	pull_request	completed	success	2026-11-18T22:03:34Z
44478473607	CI · PR #1695	pull_request	completed	success	2026-11-19T07:17:30Z
```

Job census per candidate run (step 7; `n/m` = executed/total):

```
$ gh api "repos/mcpdev80/baseharbor/actions/runs/<id>/jobs?per_page=100" --jq '.jobs[]|select(.conclusion!="skipped")|[.conclusion,.name]|@tsv'
43840657678 (#1614)   6/30   only Draft cells (Draft Go cli-0..3/packages + Draft source and routing); PR Selected Checks = skipped
43814664405 (#1595)   6/30   Draft cells only; PR Selected Checks = skipped
43812464881 (#1580)   6/30   Draft cells only; PR Selected Checks = skipped
43810693985 (#1597)   6/30   Draft cells only; PR Selected Checks = skipped
43794628957 (#1603)   6/30   Draft cells only; PR Selected Checks = skipped
44495425072 (#1613)  15/33   SUCCESS incl. PR Selected Checks, Go unit cli-0..3/owner/packages, go-build, go-vet, Source format, Focused Python, Native gate plan, Trusted Plan, Workflow policy; Draft cells skipped
44408040964 (#1602)  15/33   SUCCESS incl. PR Selected Checks; Draft cells skipped
44505333646 (#1684)  15/33   SUCCESS incl. PR Selected Checks; Draft cells skipped
44052892273 (#1616)  14/33   SUCCESS incl. PR Selected Checks; Draft cells skipped
44467712113 (#1592)  14/33   SUCCESS incl. PR Selected Checks; Draft cells skipped
44408326474 (#1599)  20/33   SUCCESS incl. PR Selected Checks + 8 extra Validation cells; Draft cells skipped
44407800144 (#1682)  20/33   SUCCESS incl. PR Selected Checks + PR · Selected Runtime (atomic/docker/lifecycle -> docker · lifecycle); Draft cells skipped
44478473607 (#1695)  15/33   SUCCESS incl. PR Selected Checks; Draft cells skipped
44499778660 (#1598)  13/33   FAILURE: PR · Go unit · cli-0 and cli-3 fail at step "Execute selected Go tests with isolated PostgreSQL"; PR Selected Checks fails at "Require complete selected Go shard coverage"
43999100666 (#1665)   2/2    workflow_dispatch FAILURE (job `validate`) — not a PR run, not success
43796258280 (#1603)   dispatch FAILURE (same sha; superseded observation, PR run above)
43796266469 (#1619)   dispatch FAILURE — no PR run at all on this head
43816873125 / 43812835617 (dispatches on #1595/#1580 shas) FAILURE — superseded by nothing: still no successful NON-draft run on those heads
```

## Findings for the coordinator

1. #1615 (0428-057): head `f93564a0` was committed 2026-11-19T10:27:34Z — minutes before this audit; the only check-suite on it is a queued third-party `claude` app suite; no Actions run yet. Re-check after CI fires.
2. Draft-stacked CLI2 chain (#1580 -> #1595 -> #1614; #1615 -> #1627/#1620/#1623/#1625): per AGENTS 3.8 the chain only gets real coverage once lanes are non-draft; today NONE of the chain heads has a successful non-draft run. The gate-routing mechanics (draft guard, ci.yml `draft == false` lines) are documented in `evidence/r28-welle4-2026-11-19/gate-routing/probe-1.md`; the fix is Owner scope (mark ready / Option A) — this lane made no change.
3. #1665 (0428-082) bases on `w083-perses-datasources`, the CLOSED #1608 branch, not on the successor #1684 branch `lane-0428-083-datasources-r2`. If #1608 was superseded by #1684, this base is stale — flag for the coordinator's chain bookkeeping.
4. Card 0428-083 lists two PRs (#1608 closed, #1684 open). The live candidate is #1684; audit used it.
5. Three review-cards point at closed PRs (#1603, #1610, #1619) — either successor PRs exist that the cards do not list, or the cards are mis-filed in `review`.

## Cleanliness

- before docker ps -a: 7 containers (ambient: `bh-local-shared-openbao-*`, `bh-local-shared-postgres-*`, pre-existing, not this lane's).
- before podman ps -a: `podman: command not found` on this host (0 podman state).
- after docker ps -a: 7 containers, identical list; after podman ps -a: same (not installed).
- This lane started NO container/network/volume/compose project (read-only `gh api`/git audit).
- cleanliness: clean — no docker/podman artifacts created by this lane; scratch confined to /var/tmp/review-compliance.

## Scope compliance

- Read-only admission check per mission GRENZEN: no `gh pr ready`, no PR comment, no merge, no rerun/workflow_dispatch, no card status changes, no `.github/**` edits, no product repo writes, no subagents (AGENTS 4.8), isolated work under /var/tmp only.
- Evidence lives only in baseharbor-plan (this file).

## Handoff

END_DONE mission-review-compliance.md: 22 review-cards audited — 8 ZULASSUNG JA (#1613 #1602 #1684 #1616 #1592 #1599 #1682 #1695, each with terminal success run incl. executed `PR Selected Checks` on exact head), 14 exceptions (10 draft-only-green, 6 with NO run on head, incl. #1615 head pushed minutes ago; dirty: #1580 #1597 #1603 #1665 #1610; closed-PR cards: #1603 #1610 #1619; failing run: #1598 44499778660 cli-0/cli-3 shards).
