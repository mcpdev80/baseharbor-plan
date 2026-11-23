# H-V36 — TRUE content-loss subset (cards 085/091/198/202/213/244)

Lane: w36-hvtrueloss (flash), read-only hunt desk. Date: 2026-11-23.
Scope: finalise the exact subset of the H-V35 "closed-unmerged LOSS class" where card
content is genuinely absent from `develop`, plus re-landable ranges for 0428-221.

## PLAN

1. Resolve the real GitHub remote (URL contains github.com/mcpdev80) and re-measure develop.
2. Fetch PR heads for #1619, #1610, #1726, #1732, #1737, #1766 via refs/pull/<N>/head.
3. Per card: is-ancestor test, rev-list --count ahead, diff --name-only delta.
4. Check sibling merged PRs delivering the same files per card.
5. Content-prove 1-2 distinctive symbols per card, develop vs branch.
6. Verdict per card (LOST-RECOVER / LANDED-VIA-SIBLING / WAIT-HOP / NO-LOSS).
7. Compute re-landable commit ranges for every LOST-RECOVER card for 0428-221.
8. Write this evidence into baseharbor-plan (real repo), push, verify on origin/main.

## Reality witnesses

Remote resolution (product repo, per REMOTE GUARD — every configured remote URL here is GitHub):

```
$ git -C baseharbor remote -v
lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin  https://github.com/mcpdev80/baseharbor.git (push)
origin       https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin       https://github.com/mcpdev80/baseharbor.git (push)
upstream     https://github.com/mcpdev80/baseharbor.git (fetch)
upstream     https://github.com/mcpdev80/baseharbor.git (push)
```

Planning repo (verified BEFORE first evidence commit, per wrong-zone rule):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Develop attestation:

```
$ git ls-remote lane-origin refs/heads/develop
dc8626e9c52be07a8ea5b87b468c5991b7540c4f        refs/heads/develop
```

PR heads (all fetched read-only via `refs/pull/<N>/head`; ls-remote re-verified after analysis,
all still present; `refs/pull/<N>/merge` does not exist for any of them):

| PR | head SHA | PR state | PR base | head branch on refs/heads? |
| --- | --- | --- | --- | --- |
| #1619 (085) | fbffb965f72585b160d4fee7bcc6050287c10fc2 | CLOSED | lane-0428-091 | yes — fbffb965f |
| #1610 (091) | d57ab527524048bddc0af7bb08009edbb4d32033 | CLOSED | lane-0428-075-perses-seam | no (branch deleted) |
| #1726 (198) | e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 | CLOSED | develop | no (branch deleted) |
| #1732 (202) | bddb27e6251ec6bc76574a1dcdb13fc7ce017f24 | CLOSED | develop | yes — bddb27e62 |
| #1737 (213) | 37587b0ed6fc8803856f3b394ae37b2ff4a03f47 | CLOSED | lane-0428-198 | no (branch deleted) |
| #1766 (244) | 405be63ff01061cdb3d5eeb0562ef441d6b89e6e | MERGED | develop | no (branch deleted) |

## Per-card analysis

Common ancestry facts:

```
$ git merge-base --is-ancestor <sha> lane-origin/develop   # develop = dc8626e9c
fbffb965f (1619) NOT in develop        37587b0ed (1737) NOT in develop
d57ab5275 (1610) NOT in develop        bddb27e62 (1732) NOT in develop
e45430f2f (1726) NOT in develop        405be63ff (1766) NOT in develop
                                       64eab13e2 (#1766 merge commit) IS in develop
```

`git rev-list --count lane-origin/develop..<sha>`: 1619 → 22, 1610 → 1, 1726 → 11,
1732 → 1, 1737 → 13, 1766 → 1 (all counts include chain-merge noise from stacked bases).

Stack topology (merge-base probes):
- 1619 = 0428-075 chain + 086 + 091 (unmerged rendering) + 085 on top; merge-base with
  develop = 14d8f17d1 (2026-11-16).
- 1737 (213) has 1726 (198) head e45430f2f as ancestor (chain stacked on 198).
- bddb27e62 (1732/202) is not an ancestor of develop; the 0428-212 lineage (#1734, merge
  7fbb2d2c6) IS in develop and supersedes it (see below).
- #1645 (091 sibling) merge commit 8629450ef IS in develop; d57ab5275 is NOT an ancestor
  of 8629450ef (independent rendering of the same adapter).

### 0428-085 — #1619 — Perses log/trace views

- Files added by the branch that are ABSENT from develop (29-file delta, `--diff-filter=A`):
  `internal/logs/perses_log_views.go(+test)`, `internal/traces/perses_trace_views.go(+test)`,
  `cmd/baha/app_perses_cli_test.go` — the card's own deliverable.
- Symbol proof: `git grep -c PersesLogViewNow origin/develop` → 0 hits; branch → present
  (`func PersesLogViewNow`, `func PersesTraceViewNow` in the two view files).
- The rest of the 22-commit delta (075/086/091 commits) was delivered by merged siblings
  (#1597, #1645 chain, #1789); the tempo/loki files on 1619 are the PRE-#1645 rendering
  (branch dated 2026-11-16, develop side dated 2026-11-22+), i.e. stale, not lost.
- Verdict: **LOST-RECOVER** (view files + CLI wiring only).
- Re-landable range: cherry-pick `937b8a747` ("view(0428-085): Perses-native log + trace
  views", 2026-11-16) onto current develop — do NOT rebase the whole 1619 branch (it would
  regress the 086/091 files to their 2026-11-16 state). Recoverable content witness:
  `git ls-tree hv36/pr1619 internal/logs/perses_log_views.go` etc., or `git show 937b8a747`.

### 0428-091 — #1610 — Perses Tempo datasource

- Sibling #1645 (w091-tempo-r5-fix) MERGED 2026-11-22 into develop; all tempo files present:
  `internal/metrics/perses_tempo_{contract,datasource,errors,upstream,verify,witness…}.go`,
  testdata incl. `perses-pin.json`, `spec-*-model.go.txt`.
- The 1610 tip's distinctive claim ("validate against the pinned upstream model") exists on
  develop: `perses_tempo_upstream.go` and `perses-pin.json` are in develop.
- 1610 head is unreachable except through `refs/pull/1610/head` (branch deleted, no merge
  base with develop — a root-commit orphan).
- Verdict: **LANDED-VIA-SIBLING**.

### 0428-198 — #1726 — CLI-shard operator identity

- Symbol proof: `withoutOperatorAuthTestContext` → develop: 0 files; branch: 11 files.
  `operator_test_fixture_test.go` (the whole-package seam): absent from develop, present on
  branch (new file in `--diff-filter=A`).
- The sibling that could have absorbed it, #1761 ("fan the CLI operator-auth fixture onto
  one exported helper", head 1e9c9b145), is reported merged at 2026-11-22T21:57 but its head
  is NOT an ancestor of develop dc8626e9c and develop contains no `OperatorAuthTestContext`
  seam → the seam content is genuinely absent from develop.
- #1737 (213) commits are descendants of 1726's head, so the 198 chain content is also
  recoverable from 37587b0ed; but the exact 1726 tip is `e45430f2f`.
- Verdict: **LOST-RECOVER**.
- Re-landable range: `e45430f2f` (= 8b2cb2a97..e45430f2f single tip; full chain
  7546b1806 → e45430f2f, 11 commits ahead of develop incl. merge noise) — re-land via
  cherry-pick of e45430f2f, or take the 1737 tip which supersedes it (see 213).

### 0428-202 — #1732 — Loki PKI client keypair

- The branch's commit (bddb27e62, 2026-11-20 22:13) materializes the mTLS client
  certificate/key in `materializeLokiServiceAccessPKI`.
- Sibling #1734 ("lane-0428-212-loki-verify-probe", MERGED 2026-11-21 08:25, merge
  7fbb2d2c6) delivered the same fix superseding: develop's `loki_test.go` contains the
  client-identity signing inside `materializeLokiServiceAccessPKI` (16 client lines in that
  function vs 0 on the 1732-base lineage) plus the stronger two-subtest probe witness
  (`assertProbeRejectionOnUnreachableLoki`, 3 hits in develop, 0 on branch).
- The only literal the branch adds beyond develop is a 2-line `strings.Contains` idiom
  tightening that develop expresses with the equivalent `err := …; err == nil` form; the
  123-insert/296-delete diff of 1732-vs-develop is 1732 REMOVING newer 0428-212 witness
  code (branch predates it), i.e. a stale inverse, not a loss.
- Verdict: **NO-LOSS** (content landed via sibling #1734; the branch itself is stale).

### 0428-213 — #1737 — trust-uninstall abort proof

- Per the coordinator's board state 0428-213 sits on `wait` → base verdict **WAIT-HOP**.
- Content truth (so the wait can close truthfully): the 37587b0ed tip carries
  `trustTestOperatorContext`, `TestTrustUninstallGateReachableInBothDirections` and
  `containsGateDenial` — develop has 0 hits for these symbols → card-213 content LOST-RECOVER.
- The same tip also carries the entire unlanded 198 chain (seam file `operator_test_fixture_test.go`
  is an add-only vs develop), and its `internal/logs/loki_test.go` is a REGRESSION against
  develop (drops the 0428-212 client-PKI materialization, −32 lines vs #1732's file).
- Verdict: **WAIT-HOP**; underlying content **LOST-RECOVER** (213-unique delta is small).
- Re-landable range: chain tip `37587b0ed` (= 1726 range + 3010b212c + 37587b0ed); cleanest
  213-only extraction = the trust-uninstall hunks of `git diff e45430f2f 37587b0ed` restricted
  to `cmd/baha/trust_uninstall_test.go` (plus the seam dependency from 198).
  Re-land must NOT take the branch's `loki_test.go` (regression).

### 0428-244 — #1766 — core-network owner diagnostic test

- PR state MERGED 2026-11-22T12:06, merge commit 64eab13e2 IS an ancestor of develop.
- `git diff lane-origin/develop 405be63ff -- cmd/baha/operator_core_network_binding_native_test.go`
  is empty (head content equals develop; later merged #1779/#1789 touched metrics surfaces only).
- Verdict: **NO-LOSS** (already merged — H-V35's loss bucket was wrong for this card).

## Verdict table

| Card | PR | ancestor of develop? | ahead | sample symbol | verdict |
| --- | --- | --- | --- | --- | --- |
| 0428-085 | #1619 | no (fbffb965f) | 22 | `PersesLogViewNow` (develop 0, branch yes) | LOST-RECOVER |
| 0428-091 | #1610 | no (d57ab5275, orphan) | 1 | `perses_tempo_upstream.go` (develop yes) | LANDED-VIA-SIBLING |
| 0428-198 | #1726 | no (e45430f2f) | 11 | `withoutOperatorAuthTestContext` (develop 0, branch 11 files) | LOST-RECOVER |
| 0428-202 | #1732 | no (bddb27e62) | 1 | `assertProbeRejectionOnUnreachableLoki` (develop 3, branch 0) | NO-LOSS |
| 0428-213 | #1737 | no (37587b0ed) | 13 | `TestTrustUninstallGateReachableInBothDirections` (develop 0) | WAIT-HOP (content LOST-RECOVER) |
| 0428-244 | #1766 | head no, merge 64eab13e2 YES | 1 | test file equal to develop | NO-LOSS |

## Recommendation for 0428-221

RE-LAND (content genuinely absent, branches recoverable via refs/pull/N/head):

1. 0428-198 — cherry-pick `e45430f2f` (or the 198-chain part of `37587b0ed`) onto develop
   `dc8626e9c`. Delivers `cmd/baha/operator_test_fixture_test.go` + the 28 cmd/baha call-site
   stamps.
2. 0428-213 — rebase/cherry-pick `37587b0ed` on top of the 198 re-land, then fix its
   `internal/logs/loki_test.go` to keep the develop (0428-212) version instead of the
   branch's regression. 213 stays card-status `wait` until this lands; no reopen needed.
3. 0428-085 — cherry-pick `937b8a747` ONLY (the view-files commit) onto develop; do not
   rebase the whole 1619 branch. Reopen card 085.

DO NOT reopen / no action:

- 0428-091 — LANDED-VIA-SIBLING (#1645 merged 2026-11-22).
- 0428-202 — NO-LOSS (#1734 merged supersedes; the branch is stale-inverse).
- 0428-244 — NO-LOSS (#1766 merged, content on develop).

Side finding (coordinator awareness, no action by this lane): #1761 (0428-231 auth-helper)
is listed MERGED at 2026-11-22T21:57 but its head `1e9c9b145` is not an ancestor of develop
`dc8626e9c` and the seam symbols are absent — same loss pattern as 198/213.

## cleanliness

- Read-only mission: no files touched in any product repo, no containers/networks/volumes/
  stacks started, no branches created or pushed, no PR or CI actions, no subagents.
- Only side effect: local fetch refs `hv36/pr*` + two fetched SHAs in the shared baseharbor
  object store (read-only artifacts of measurement).
- docker not invoked; host unchanged.

END_DONE hunt-hv36: develop dc8626e9c; 3 LOST-RECOVER (085←937b8a747, 198←e45430f2f, 213←37587b0ed-minus-loki-regression); 091 landed-via-sibling #1645; 202+244 NO-LOSS (#1734/#1766 merged).
