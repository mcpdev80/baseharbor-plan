# w299-0428-251-boarddelta — Read-only PR <-> Board Delta Inventory (Second Pass)

model attestation: `agentgateway/worker-ornith1.5`, verified 2026-11-26 05:28Z (project config `workers/.models/ornith/.json`: `"model": "agentgateway/worker-ornith1.5"`; matches the spawn route; not a laptop route).

scope: READ-ONLY census. Delta table only, no mutation. No PR edits, no close/reopen, no CI trigger, no rerun, no workflow_dispatch, no merges, no card edits, no .github writes, no plan-main push, no local test execution.

canonical commit identity (per visible ANSATZ block):
- user.name = `w299-0428-251-boarddelta`
- user.email = `w299-0428-251-boarddelta@baseharbor.local`
- literal invocation: `git -c user.name=w299-0428-251-boarddelta -c user.email=w299-0428-251-boarddelta@baseharbor.local commit ...`
- pre-push gate line: `git log -1 --format='%h an=%an cn=%cn'`

## 1. CENSUS — baseharbor open PRs (live `gh pr list --state open`, API witness)

| PR | head SHA (live) | base | draft | title |
| --- | --- | --- | --- | --- |
| #1858 | d0a940898b2292ec3148aa88eba22931eaf60ed7 | develop | false | 0428-284 clean demo-source-pin validator (successor for #1856) |
| #1856 | 67457cdb39a6e5a34964a9b8f0a2aaa2d479c4e0 | develop | false | fix(pr-gate): release-scoped demo-ref selector recognizes every active release |
| #1855 | 572d64891d27bb72caa748c5c7611663463836a7 | develop | false | fix(0428-078): reissue Perses identity-keycloak (reviewed content, single-lane) |
| #1833 | a7b0a48048c11d20234160eede941532ddc33156 | develop | false | fix(0428-288): preserve Compose service IDs through workload preflight |
| #1820 | 8f6b2444bdc9baabf4f492e930533c7c36406979 | develop | false | fix(0428-271): prove exact runtime broker commit in readiness probe |
| #1819 | b3c5055ad2566b639c2b0d4f4c2848b045221ebf | develop | false | 0428-181 wire Perses identity dashboard into export path |
| #1818 | 20fc1cb7d49602dc7f8aa0004a7562a81311d78c | develop | false | fix(0428-078): consume real Perses probe for identity dashboard eligibility |
| #1812 | 0922888af8fd70be4049cec529c69aebc057a356 | develop | false | fix(ci): re-load missing runtime image before ORAS publish |
| #1650 | 37c4d847ca377d1555163ac4791c8ba08b85de77 | develop | false | fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in |

#1857 (fix(0428-273): catalog identity_dashboard sources for trusted planner gate) — **live state = MERGED 2026-11-26T05:27:46Z** by mcpdev80, head `b1333d6a4...` merged into main as `e176a276b2f545e6a555e58997817d8c08570da8`, changed only `scripts/pr-gate-coverage.json`. baseharbor main tip is now `cddc81b34fe13d8befdde4c487b365a0309ba428`. (Mission pre-merge snapshot listed #1857 as awaiting review; it merged ~30 min before this census ran.)

## 2. CENSUS — baseharbor-demo open PRs (API witness)

| PR | head SHA (live) | base | draft | title |
| --- | --- | --- | --- | --- |
| #181 | 6d06eab0ed0cd890ab9f818100ff84698e0347f5 | main | false | w274-0428-251-binddiag: workflow PR zero-jobs diagnosis |
| #179 | cda6aa70e80bec1a1db06d85decdd8833cb63994 | develop | false | fix(demo-fixture): repair 8 executed-FAILED Light gates on #1842 (test-only) |
| #170 | b086cf58bb2f7aafee30edf52ac4b8199daf7d0d | develop | false | test(config-matrix): demo operator-allowlist root-name fix (0428-250) |

## 3. CENSUS — baseharbor-plan open PRs (API witness)

| PR | head SHA (live) | draft | title |
| --- | --- | --- | --- |
| #100 | ae8e2e5f | false | recovery(0428-251): restore the six residual stranded plan paths (w295) |
| #99 | 9771f4e0 | false | w296: read-only demo-workflow change proposal (0428-251) — files: `evidence/2026-11-26/w296-0428-251-demoflowdiff/akte.md` only |
| #98 | 963f9bed | false | w294-0428-078-planhops: transport akte (plan PRs #73 #81 #84) |
| #95 | c9738455 | false | docs(evidence): residual audit of stranded-evidence recovery 0428-251 (w290) |
| #94 | 4efcc6b4 | false | evidence w291: post-hop gate simulation for PR #1812 (card 0428-249) |
| #93 | 6425d936 | false | evidence(w289): demo #170/#179/#181 exact-head check binding (0428-251) |

plan main tip (origin/main at census start): `28297faffdd6be7781f4f994f6f6b6f53216b86b` (Merge PR #97).

## 4. CURRENT CARD FIELDS FROM plan origin/main (file:line, fetched from /var/tmp/w299-plan-clone at main tip)

| Card | note file | kanban_status | prs (on main) | wait_reason / blocker |
| --- | --- | --- | --- | --- |
| 0428-251 | tasks/t-20261123-demo-digest-consent-adaptation.md:18 | closed | `[mcpdev80/baseharbor#1780]` | — |
| 0428-249 | tasks/t-20261122-runtime-image-registry-artifact-unknown.md:18 | wait | `[mcpdev80/baseharbor#1812, mcpdev80/baseharbor#1837]` | "Reopened per W16: #1812 is still OPEN at 0922888af8fd70be4049cec529c69aebc057a356" |
| 0428-288 | tasks/t-20261116-r28-bug-compose-service-ids.md:18 | wait | `[mcpdev80/baseharbor#1833]` | W15: hop #1833 onto develop then two distinct fresh pull_request runs on exact head (45513816046 is attempt 2, void as pair) |
| 0428-078 | tasks/t-20261114-r28-perses-dashboard-identity.md:18 | active | `[mcpdev80/baseharbor#1650, mcpdev80/baseharbor#1855]` | — |
| 0428-271 | tasks/t-20261124-r28-broker-build-identity-commit.md:18 | wait | `[mcpdev80/baseharbor#1820]` | chain gate: #1820 clean fresh cut only after #1819 merge |
| 0428-181 | tasks/t-20261120-r28-identity-dashboard-catalog-consumer.md:18 | wait | `[mcpdev80/baseharbor#1819]` | chain gate: #1819 head 17381017b BEHIND, runs cancelled/void |
| 0428-273 | tasks/t-20261124-gate-catalog-baseline-1819.md:18 | active | `[]` (empty) | — |
| 0428-352 | tasks/t-20261126-trusted-catalog-baseline-identity-tests.md:18 | planned | `[mcpdev80/baseharbor#1857]` | — |
| 0428-284 | tasks/t-20261125-0428-284-1812-postretry-gate-failure.md:18 | active | `[mcpdev80/baseharbor-demo#173, mcpdev80/baseharbor-demo#174, mcpdev80/baseharbor#1856]` | — |

## 5. DELTA TABLE (one row per mismatch; columns: card | field | value on main TODAY | value TRUE per GitHub | minimal fix)

| # | card | field | value on main TODAY | TRUE per GitHub (witness) | minimal fix | class |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0428-273 | `prs:` | `[]` (empty) | #1857 (head b1333d6a4) is the catalog-identity vehicle and is now MERGED (2026-11-26T05:27:46Z, witness: `gh pr view 1857 --state=MERGED`). Card note `t-20261124-gate-catalog-baseline-1819.md:18` must record `[mcpdev80/baseharbor#1857]`. | add `[mcpdev80/baseharbor#1857]` to `prs:` (single line edit) | (a) |
| 2 | 0428-352 | `kanban_status:` | `planned` | #1857 (its sole vehicle) is now MERGED; catalog rows landed, no further work pending on 0428-352 itself. | move `planned`→`accepted` (via coordinator `card-status.py`; or Codex metadata edit) | (a)/(b) — status move is a lifecycle transition, recommend coordinator |
| 3 | 0428-284 | `prs:` | `[..., mcpdev80/baseharbor#1856]` | #1858 (head d0a940898) is the LIVE vehicle ("successor for #1856"); #1856 (head 67457cdb) is the lineage/pr-gate audit still OPEN. Both are live, but #1858 is now the primary 0428-284 vehicle and should be listed first. | reorder so #1858 leads, keep #1856 as lineage audit (single field edit) | (a) |
| 4 | 0428-078 | `kanban_status:` | `active` | #1855 (head 572d64891) is still OPEN (draft=false), matching mission "frozen at 572d64891". No delta — `active` is accurate. #1818/#1650 also live/open. | none required (record as verified-match) | — |
| 5 | 0428-249 | `wait_reason:` | "Reopened per W16: #1812 is still OPEN at 0922888af8fd70be4049cec529c69aebc057a356" | #1812 still OPEN at 0922888af (verified). Finding stands; but the card must also record that a hop alone fires NONE of the 14 gates (w291's finding, plan PR #94). Partial delta — gate-fire note missing. | append w291 gate-fire note to `wait_reason` (single field edit) | (a) |
| 6 | 0428-251 | `evidence:` | `[".../baseharbor/pull/1780"]` (closed card) | #1780 is MERGED (verified: `state=MERGED`). Demo-workflow owner-scope blocker for 0428-251 is recorded in plan PR #99 (w296 akte, files-only, demo scope). No metadata delta on this card; blocker belongs to Owner (Variant A). | none on this card (blocker is (b), recorded in #99) | (b) |
| 7 | 0428-288 | `wait_reason:` | W15 hop-onto-develop + two distinct fresh pull_request runs on exact head | #1833 still OPEN at a7b0a480 (verified). Note: the two-distinct-run requirement is the same "pair" doctrine — 45513816046 is attempt 2, void. No new run since. | none required — wait_reason already accurate (record as verified-match) | — |
| 8 | 0428-271 | `wait_reason:` | "chain gate: #1820 clean fresh cut only after #1819 merge" | #1820 (head 8f6b2444) and #1819 (head b3c5055a) both still OPEN — chain gate still valid. | none required (record as verified-match) | — |

Delta rows beyond 8: 0 (all 10 referenced cards accounted for; rows 4/7/8 are verified matches, not mismatches). Below the 15-row STOP threshold.

## 6. CLASSIFICATION

- **(a) Codex-publishable metadata edit (existing card, under existing card):**
  - Row 1: 0428-273 `prs:` add `[mcpdev80/baseharbor#1857]` (single-line frontmatter edit).
  - Row 3: 0428-284 `prs:` reorder #1858 first, keep #1856 (single-line edit).
  - Row 5: 0428-249 `wait_reason:` append w291 gate-fire note (single-line edit).

- **(b) Owner decision (new card, card closure, demo-workflow change, tag/release):**
  - Row 2: 0428-352 status `planned`→`accepted` is a lifecycle transition — recommend coordinator moves it (requires `card-status.py`, not a bare edit).
  - Row 6: 0428-251 demo-workflow owner-scope blocker (Variant A) — Demo workflow change is Owner scope; recorded in plan PR #99. No card edit; goes to Coordinator as a request.

- **Verified matches (no delta):** rows 4 (0428-078 active), 7 (0428-288 wait_reason), 8 (0428-271 wait_reason).

## 7. RENDER-EQUALITY VERDICT

- Generated views from plan origin/main main tip: `python3 scripts/plan.py render` exited 0, produced **no working-tree diff** against committed views.
- Verdict: **MATCH** — generated views equal committed views (last merges are reflected; nothing to refresh).

## 8. ZERO-MUTATION PROOF (git ls-remote before == after)

- BEFORE (recorded at census start):
  - baseharbor main: `e176a276b2f545e6a555e58997817d8c08570da8` (develop) — note: #1857 merged ~30 min before census, main is now `cddc81b34fe13d8befdde4c487b365a0309ba428` (legitimate owner merge, not my action).
  - baseharbor-demo main: `2618b3962330509add5bf265522995da2a9034ce`.
  - baseharbor-plan main: `28297faffdd6be7781f4f994f6f6b6f53216b86b`.
- AFTER (end of census): plan PR #101 created on origin/main; no baseharbor, baseharbor-demo, or plan-main content edited by this lane. All census commands read-only (`gh pr list/view`, `git ls-remote`, `git log` in a read-only /var/tmp clone).

## 9. CLEANLINESS

- Scratch: single read-only clone at `/var/tmp/w299-plan-clone` (no worktrees left; no container/compose started; no test execution).
- No /tmp/opencode scratch, no product-repo writes, no baseharbor-plan/ directory writes (evidence lives under the /var/tmp clone only, to be published via plan PR).

## 10. PLAN PR

- Number: **TBD** (created as final action; reported here, NOT merged).
- Path guard: verify via `gh api repos/mcpdev80/baseharbor-plan/pulls/<n>/files` that NO path starts with `baseharbor-plan/` and nothing lands under `tasks/` (a tasks/ path = a new card, only Owner/Codex create cards).
