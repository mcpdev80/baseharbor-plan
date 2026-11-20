# PR Duplicate / Superseded Hunt — Round 1

**Card / lane:** w219-0428-198-duples (coordinated hunt, read-only, no writes to baseharbor)
**Date:** 2026-11-20
**Session model:** worker-ornith1.5 (verified, own session)

## Zweck

Read-only inventory and triage of all open PRs in `mcpdev80/baseharbor` to find superseded or duplicate PRs. This lane does EXACTLY ONE thing among four parallel lanes (others check gate cells, CLI test list, native cell). No PR is closed, no file edited, no `gh pr edit`, no retarget, no rerun, no `workflow_dispatch`, no subagents. The two instruction-cited precedents (#1727 = duplicate of #1728; #1702 = hangs on a now-closed card) are re-verified against current remote truth.

## Base attestation

Planning repo `baseharbor-plan` origin (verified `git remote -v` first):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

`baseharbor-plan` origin/main HEAD: `7366f885a2374115c7e21eb55c3fb60d427742b6`

Product develop HEAD (via `git ls-remote` on the real GitHub remote, `git@github.com:mcpdev80/baseharbor.git`):

```
40cb28c758b02960356434b630086a341ebe1738	refs/heads/develop
```

baseharbor checkout remote (`git remote -v`, first git action):

```
origin	git@github.com:mcpdev80/baseharbor.git (fetch)
origin	git@github.com:mcpdev80/baseharbor.git (push)
```

Only origin (URL contains github.com/mcpdev80) is used; no fetch/push through an unresolved remote name. `lane-origin` does not exist in this checkout.

## Methode

1. Inventory: `gh api "repos/mcpdev80/baseharbor/pulls?state=open&per_page=100"` -> number, head-sha, base.ref, draft, changed_files, title, updated_at.
2. Duplicate test (patch-id) between two PRs targeting the same card: `git diff 40cb28c758b0 <head> | git patch-id --stable`. Same patch-id = duplicate.
3. Content-on-develop test: `git cat-file -e 40cb28c758b0:<newfile>` / `git grep -n -a "<symbol>" 40cb28c758b0 -- <path>`. Hit = content already on develop.
4. Card reference: `git -C baseharbor-plan grep -l -a "#<number>" origin/main -- tasks/` + `kanban_status`.

## Inventory table (28 open PRs)

| PR | head(12) | base.ref | draft | card | title |
| --- | --- | --- | --- | --- | --- |
| 1585 | 55a8c0f3550d | develop | yes | 0427-189 | fix(cli): state-dir override owns target-selection state (BF-01) |
| 1587 | 20e0537cc333 | develop | yes | 0427-169 | docs(0427-169): Core operator API route runbook (EN/DE) |
| 1588 | 9534edd49c20 | develop | yes | 0427-186 | feat(r27): editable Target policy presets |
| 1596 | c90c3b89007e | develop | yes | 0428-056 | Organization environment reconciliation |
| 1597 | 90063f6ec66c | develop | no | 0428-076 | Perses database dashboards |
| 1614 | 80d4df52e913 | develop | yes | 0428-062 | unify app status + versions over the source-model read view |
| 1615 | 5675c23047fa | develop | no | 0428-057 | Separate human/runtime secret reveal |
| 1620 | fcba5d25ce8b | develop | yes | 0428-067 | per-reveal audit for `baha app creds --reveal` |
| 1623 | 4cbf92960cb5 | cli2-identity-secrets-head | yes | 0428-063 | guided app logs/exec/urls over the status read view |
| 1625 | 010db47dae0e | cli2-identity-secrets-head | yes | 0428-065 | guided baha app export of selected local credentials |
| 1627 | 96deb1f1597d | develop | yes | 0428-055 | baha env destroy (env-scoped identity removal) |
| 1645 | 4d73aa97808d | develop | no | 0428-091 | rename .go witnesses to .go.txt (CI package-selection fix) |
| 1650 | 9add5e8a2122 | develop | no | 0428-078 | wire Perses identity-keycloak into 080 resolver fan-in |
| 1665 | db27880c108a | lane-0428-083-datasources-r2 | no | 0428-082 | native Perses infrastructure dashboard |
| 1684 | b71c6da27e8b | perses-tmpfs-mountpoint-wt | no | 0428-083 | Connect Perses Prometheus datasource |
| 1702 | 6740299f91c0 | develop | no | 0428-142 | perses per-signal backend-witness (manifest-only) |
| 1704 | f5dcf1288548 | develop | no | 0428-073 | honest fail-closed Perses alert health verifier |
| 1714 | 5159192dadee | develop | no | 0428-183 | valkey dashboards gated on real availability |
| 1718 | ce5aa9633630 | develop | no | 0428-178 | prove context precedence through the real baha context show path |
| 1723 | 26755fc1edfb | develop | no | 0428-199 | respect --workload-port on local apply/up path |
| 1724 | 408b18d2dc7b | develop | no | 0428-177 | perses tmpfs mountpoint + advertised_address schema |
| 1725 | 9bf4a72f742b | develop | no | 0428-201 | name shared backend state version mismatch |
| 1726 | bf6f10aff6fe | develop | no | 0428-198 | give CLI unit tests an in-test operator identity |
| 1728 | 6e3122344f87 | develop | no | 0428-200 | surface deployment record version mismatch |
| 1729 | 809a8196e1cf | develop | no | 0428-143 | skip Verification=none in application metrics verifier loop |
| 1730 | c90a73ac8128 | lane-0428-143-verify-none | no | 0428-203 | retirement guard for stale target on Verification=none |
| 1731 | f90b3f448caf | develop | no | 0428-179 | require zsh and fish wrapper paths in CI |
| 1732 | bddb27e6251e | develop | no | 0428-202 | materialize mTLS client keypair in internal/logs Loki PKI fixture |

Note: `gh api` reports 28 open PRs; the earlier truncated shell listing showed 27 rows. The inventory above is authoritative (28).

## Duplicate test (patch-id)

Card mapping shows every card number appears EXACTLY ONCE among the 28 open PRs. There are no two open PRs targeting the same card, so no patch-id comparison between competing candidates is needed — there is nothing to compare. The only genuine duplicate pair named by the instruction is #1727 (duplicate of #1728, patch-id equal), and #1727 is already CLOSED — verified below via `git ls-remote`:

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1727/head
(no output — PR #1727 has no open head ref; already closed)
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1728/head
6e3122344f87bd84f0632a30e91817ea1b9748a5	refs/pull/1728/head
```

1728 patch-id against develop:

```
$ git diff 40cb28c758b0 6e3122344f87 | git patch-id --stable
c0253bdb2b1a93838870989efdd0d27b5a2cb81e 0000000000000000000000000000000000000000
```

Result: **no NEW duplicates found** among the 28 open PRs. #1727/#1728 already resolved (1727 closed, 1728 open).

## Content-on-develop test (symbol test)

| PR | file/symbol | develop hit? | note |
| --- | --- | --- | --- |
| 1702 | `cmd/baha/app_status_result.go` Perses witness comment (`git cat-file -e 40cb28c758b0:cmd/baha/app_status_result.go`) | YES exists on develop | content partially landed; card still OPEN (see below) |
| 1702 | `internal/metrics/verify_none_red_test.go` | YES exists on develop | red-test file already in develop tree |
| 1650 | Perses identity-keycloak wiring | — | card 0428-078 = **planned** (active) |

## Card reference

| PR | card | kanban_status |
| --- | --- | --- |
| 1702 | t-20261119-r28-perses-status-backend-witness | **wait** (OPEN) |
| 1704 | t-20261114-r28-perses-alerts | review (CODEX verdict: DIRTY/CONFLICTING, needs rebase/rerun) |
| 1650 | t-20261120-r28-identity-dashboard-catalog-consumer | planned |
| 1614 | t-20261114-r28-cli2-app-status | wait |

The instruction claimed card 0428-142 is CLOSED (matching the #1702 precedent). Current `origin/main` shows it **kanban_status: wait** — OPEN. The #1702 case does NOT match the "card closed + PR open" superseded pattern; it is live work-in-progress with some content already on develop.

## Befund-listen

### (a) Close on my own judgment (with witness per line)
None. No open PR is a confirmed duplicate of another open PR, and no open PR hangs on a closed card. The instruction's two precedents are: #1727 already closed (not in the open set); #1702's card is OPEN (wait), so it is not superseded. Closing is a coordinator/Codex action anyway (boundaries: do not close, do not edit).

### (b) Owner / Codex cards — NOT touched (per instruction §2, list 0428-057/062/073/078)
- #1615 (0428-057) — secret reveal: owner/codex. Untouched.
- #1614 (0428-062) — app status: owner/codex. Untouched.
- #1704 (0428-073) — Perses alert health verifier: owner/codex. CODEX-REVIEW verdict on card: "PR is DIRTY/CONFLICTING against current develop and needs rebase/rerun" (also a stale exact run). Do not touch.
- #1650 (0428-078) — resolver fan-in: owner/codex. Untouched.

### (c) Live work (active cards, real work)
All remaining open PRs (#1585, #1587, #1588, #1596, #1597, #1620, #1623, #1625, #1627, #1645, #1665, #1684, #1714, #1718, #1723, #1724, #1725, #1726, #1728, #1729, #1730, #1731, #1732) are live work on active cards. None is a duplicate or superseded.

## Stale-PR note (informational, not a close)
Oldest by `updated_at` (potential churn to watch next wave):
- #1587 (0427-169) — 2026-11-15, draft
- #1588 (0427-186) — 2026-11-15, draft
- #1585 (0427-189) — 2026-11-16, draft
- #1614 (0428-062) — 2026-11-19, draft
- #1625 (0428-065) — 2026-11-20, draft
These are drafts on active cards; flagged only, not acted on.

## repo-rule compliance

Read-only hunt. No product-file edits. No PR closed, no `gh pr edit`, no retarget, no rerun, no `workflow_dispatch`, no subagents. All evidence gathered via `git ls-remote` / `gh api` / read-only `git diff --stat` against verified remote refs.

```
$ git -C baseharbor status --porcelain
(empty — no changes)
```

## container / network / volumes cleanliness (3.3.5)

No containers, networks, volumes or state directories were created (no docker/podman used; read-only hunt).

```
$ docker ps --format '{{.Names}}' --filter ancestor=none
(empty)
cleanliness: clean — no container/network/volume/state created this lane
```

## PLAN

- Read instruction file (first action)
- Attest planning repo origin/main and develop HEAD via git ls-remote
- Inventory all 28 open PRs
- Duplicate test (patch-id): no same-card pairs exist
- Content-on-develop symbol test on #1702, #1650
- Card reference + kanban_status lookup
- Verdict lists (a/b/c)
- Write evidence file
- Commit evidence to baseharbor-plan origin/main, verify path present via ls-tree
- Post END_DONE to coordinator session

## END

w219-0428-198-duples: read-only PR duplicate/superseded hunt, no NEW duplicates among 28 open PRs (#1727 already closed; #1702 card is OPEN/wait not closed as instruction claimed). Evidence committed to baseharbor-plan.
