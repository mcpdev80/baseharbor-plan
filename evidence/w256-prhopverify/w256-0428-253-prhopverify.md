# PR-HOP + Commit-Identity verification — w256 (read-only sweep)

- Mission tag `prhopverify`, supporting cards `t-20261121-stale-pr-hop-and-baserefs` (0428-216) and `t-20261121-candidate-commit-identity` (0428-224).
- Read-only. NO writes, NO pushes, NO CI triggers, NO merges, NO reruns. No card writes.
- Date: 2026-11-27 (shift r28-welle6). Session `e6ca7696-b1f8-492d-b226-876b16925fc5`.

## PLAN

- Establish plan repo read worktree from origin/main (isolated, planrem remote).
- List all open PRs in baseharbor and baseharbor-demo (gh pr list --state open).
- Ancestry test per PR: `git merge-base --is-ancestor origin/BASE PRHEAD` against the exact fetched base head (ls-remote witness), classify CURRENT vs STALE.
- Identity test per PR: `.commit.author.name` of each PR head commit vs the owning card's frontmatter owner (verbatim), classify CANONICAL / SHORTENED-SAME-LANE / FOREIGN / UNKNOWN-LANE.
- Deliver two tables + counts and a recommendation per violating PR.
- Write akte via plan-PR branch path (evidence/... on origin/main) with post-merge git show witness.
- No product-repo writes, no plan-dir mutations, no container starts.

## Method

- Remote guard: in this workspace `origin` = `ssh://git@github.com/mcpdev80/baseharbor.git` (github URL confirmed). All remote measurements taken via `git ls-remote` or a throwaway clone, never the quarantined checkout.
- Open PRs: `gh pr list --repo mcpdev80/baseharbor --state open` and `--repo mcpdev80/baseharbor-demo --state open`.
- Ancestry: exact base head fetched with `git ls-remote ssh://git@github.com/mcpdev80/baseharbor.git refs/heads/develop` and compared with `git merge-base --is-ancestor <develop-sha> <prhead-sha>` in a throwaway clone. BASE attestate = the `develop` SHA each PR is opened against.
- Identity: `gh api repos/mcpdev80/<repo>/pulls/<n>/commits --paginate` -> `.commit.author.name` (sole signal; `.author.login`/GitHub login ignored; null on unsigned commits is not a finding). Expected lane = owning card frontmatter `owner:` field (verbatim). Exact-equality rule under card t-20261121 / w155.
- Plan-repo remote witness: `git -C <worktree> remote -v` -> `planrem  https://github.com/mcpdev80/baseharbor-plan.git`.

## Base attestation

- baseharbor `develop` (exact head compared against): `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (`git ls-remote ssh://git@github.com/mcpdev80/baseharbor.git refs/heads/develop`).
- baseharbor-demo `develop` (exact head): `5ca92a7cd2f746934890cfd7096a48068bdf218e` (`git ls-remote ssh://git@github.com/mcpdev80/baseharbor-demo.git refs/heads/develop`).

## (1) Ancestry / hop table (baseharbor)

All 7 open baseharbor PRs open against `develop`. BASE = `develop` head `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (ls-remote witness).

- PR #1842 — head `w177-0428-284-demo-pin-1812` @ `dfd3495858501fe49d9c331c056a4289b780e0f8` — base develop IS ancestor of head -> **CURRENT**. 11 commits ahead of develop.
- PR #1833 — head `lane-0428-288-compose-ids` @ `a7b0a48048c11d20234160eede941532ddc33156` — develop NOT ancestor -> **STALE** (needs absorb hop). 6 commits ahead.
- PR #1820 — head `fix/broker-build-identity` @ `8f6b2444bdc9baabf4f492e930533c7c36406979` — develop NOT ancestor -> **STALE** (needs absorb hop). 18 commits ahead.
- PR #1819 — head `w54-0428-181-export` @ `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` — develop NOT ancestor -> **STALE** (needs absorb hop). 11 commits ahead.
- PR #1818 — head `lane-0428-078-cf-fix` @ `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` — develop NOT ancestor -> **STALE** (needs absorb hop). 4 commits ahead.
- PR #1812 — head `lane-0428-249-runtime-image-fix` @ `0922888af8fd70be4049cec529c69aebc057a356` — develop NOT ancestor -> **STALE** (needs absorb hop). 9 commits ahead.
- PR #1650 — head `lane-0428-078-perses-identity-on-resolver` @ `1c33e910070a07a6d4105f0d38e3c89988a788a3` — develop NOT ancestor -> **STALE** (needs absorb hop). 9 commits ahead.

Count: **1 CURRENT, 6 STALE** (of 7).

Ancestry witness lines (from throwaway clone, base `develop` = `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`):
- `git merge-base --is-ancestor ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee dfd3495858501fe49d9c331c056a4289b780e0f8` -> holds (1842 CURRENT)
- same for a7b0a48048c11d20234160eede941532ddc33156 -> fails (1833 STALE)
- same for 8f6b2444bdc9baabf4f492e930533c7c36406979 -> fails (1820 STALE)
- same for b3c5055ad2566b639c2b0d4f4c2848b045221ebf -> fails (1819 STALE)
- same for 20fc1cb7d49602dc7f8aa0004a7562a81311d78c -> fails (1818 STALE)
- same for 0922888af8fd70be4049cec529c69aebc057a356 -> fails (1812 STALE)
- same for 1c33e910070a07a6d4105f0d38e3c89988a788a3 -> fails (1650 STALE)

## (1b) Ancestry / hop table (baseharbor-demo)

Both demo PRs open against `develop` head `5ca92a7cd2f746934890cfd7096a48068bdf218e` (ls-remote witness).

- PR #179 — head `w198-1842-demo-fixture-fix-forward` @ `cda6aa70e80bec1a1db06d85decdd8833cb63994` — base develop IS ancestor -> **CURRENT**. 1 commit ahead.
- PR #170 — head `lane-0428-250-demo-operator-root` @ `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d` — base develop IS ancestor -> **CURRENT**. 2 commits ahead.

Count: **2 CURRENT, 0 STALE** (of 2).

## (2) Identity table (baseharbor)

Owning card frontmatter owner (verbatim, from baseharbor-plan origin/main):

- 0428-284 (demo-pin/#1842): task `t-20261125-0428-284-1812-postretry-gate-failure.md` owner `w198-0428-284-demo-parser`.
- 0428-288 (#1833): task `t-20261116-r28-bug-compose-service-ids.md` owner `w147-0428-288-pr1833-fix`.
- 0428-271 (#1820): task `t-20261124-r28-broker-build-identity-commit.md` owner `w69-0428-271-brokerid2`.
- 0428-181 (#1819): task `t-20261120-r28-identity-dashboard-catalog-consumer.md` owner `w54-0428-181-export`.
- 0428-078 (#1818, #1650): task `t-20261114-r28-perses-dashboard-identity.md` owner `w165-0428-078-pr1650-basehop`.
- 0428-249 (#1812): card `t-20261122-runtime-image-registry-artifact-unknown.md` owner (blank).

Identity signal = `.commit.author.name` of each PR head commit. Under exact-equality (card t-20261121 / w155), the head author must EXACTLY equal the owning lane.

| PR | head sha (12) | commit author(s) | owning lane (frontmatter owner) | class |
| --- | --- | --- | --- | --- |
| 1842 | dfd349585850 | w177-0428-284-demo-pin-1812 (x2), w198-0428-284-demo-parser (x8), w205-0428-253 (x1) | w198-0428-284-demo-parser (card 0428-284) | SHORTENED-SAME-LANE + FOREIGN (w205-0428-253) |
| 1833 | a7b0a48048c1 | w121 (x3), lv4-verify (x2), w124 (x1) | w147-0428-288-pr1833-fix (card 0428-288) | FOREIGN (w121, lv4-verify, w124) |
| 1820 | 8f6b2444bdc9 | 0428-061-sourcepull, w54-0428-181-export, lv4-verify, Codex, w198-0428-284-demo-parser, w205, w219-0428-271-0428-286-1820hop, w231-0428-285-1820restack | w69-0428-271-brokerid2 (card 0428-271) | FOREIGN (none of these is w69-0428-271-brokerid2) |
| 1819 | b3c5055ad2566 | w54-0428-181-export (x2), lv4-verify, Codex, w198-0428-284-demo-parser, w205 | w54-0428-181-export (card 0428-181) | SHORTENED-SAME-LANE (w54-0428-181-export present) + FOREIGN (lv4-verify, Codex, w198, w205) |
| 1818 | 20fc1cb7d496 | w21-pr1702-0428-246-footprint (x3), w53-0428-152-alertfix (x1) | w165-0428-078-pr1650-basehop (card 0428-078) | FOREIGN |
| 1812 | 0922888af8fd7 | w198-0428-284-demo-parser (x4), lv4-verify (x5) | (blank owner, card 0428-249) | UNKNOWN-LANE owner; authors foreign to a 249 card |
| 1650 | 1c33e910070a | w165-0428-078-pr1650-basehop (x8), w181-0428-doclink-sweep (x2) | w165-0428-078-pr1650-basehop (card 0428-078) | SHORTENED-SAME-LANE (w165-0428-078-pr1650-basehop present) + FOREIGN (w181-0428-doclink-sweep) |

- Foreign authors observed across the 7 PRs: `w177-0428-284-demo-pin-1812`, `w205-0428-253`, `w121`, `lv4-verify`, `w124`, `0428-061-sourcepull`, `Codex`, `w198-0428-284-demo-parser`, `w205`, `w219-0428-271-0428-286-1820hop`, `w231-0428-285-1820restack`, `w21-pr1702-0428-246-footprint`, `w53-0428-152-alertfix`, `w181-0428-doclink-sweep`. None equals `w69-0428-271-brokerid2`.
- The 0428-249 cards have a blank owner (`owner:` empty), so there is no canonical lane string to compare against -> UNKNOWN-LANE by the mission's own vocabulary (not a violation, but unclassifiable under exact-equality).

## (2b) Identity table (baseharbor-demo)

| PR | head sha (12) | commit author(s) | owning lane | class |
| --- | --- | --- | --- | --- |
| 179 | cda6aa70e80b | w198-0428-284-demo-parser (x1) | w198-0428-284-demo-parser (card 0428-284, demo) | CANONICAL |
| 170 | b086cf58bb2f | Flash (x2) | w50-0428-250-corefixture (card 0428-250) | FOREIGN (Flash) |

- Demo PR #179 head author `w198-0428-284-demo-parser` == owning lane -> CANONICAL.
- Demo PR #170 head author `Flash` != owning lane `w50-0428-250-corefixture` -> FOREIGN.

## (3) Counts

- baseharbor open PRs: **7**. CURRENT: **1** (#1842). STALE: **6** (#1833, #1820, #1819, #1818, #1812, #1650).
- baseharbor-demo open PRs: **2**. CURRENT: **2** (#179, #170). STALE: **0**.
- baseharbor commits canonical-vs-foreign (per PR head, exact-equality vs owning lane): **0 CANONICAL**, **1 SHORTENED-SAME-LANE** (#1819 has its own lane in some commits + foreign), **5 with foreign authors on every commit** (#1833, #1820, #1818, #1812), **1 SHORTENED-SAME-LANE** (#1650 has its own lane in most commits + foreign), **1 UNKNOWN-LANE-owner** (#1812 card owner blank). No PR head is authored exclusively by its owning lane.
- demo: **1 CANONICAL** (#179), **1 FOREIGN** (#170 author `Flash`).

## (4) Recommendation per violating PR

Read-only only — these are recommendations for the owning lane / coordinator; nothing executed here.

- #1833 (0428-288, STALE, foreign authors w121/lv4-verify/w124): absorb hop to current develop, then re-land any new commits under the verbatim card owner `w147-0428-288-pr1833-fix` (`git -c user.name=w147-0428-288-pr1833-fix -c user.email=w147-0428-288-pr1833-fix@baseharbor.local`). Push the existing lane branch; do NOT cut a second branch.
- #1820 (0428-271, STALE, foreign authors; head is a stacked develop-merge): absorb hop onto develop (guarding the forward-diamond already in the log), then re-land under `w69-0428-271-brokerid2`. Stacked on #1819 in the chain #1812 -> #1819 -> #1820 — keep the stack, rebase via hop, do not flatten.
- #1819 (0428-181, STALE, mixed own-lane + foreign): absorb hop onto develop, re-land foreign commits under `w54-0428-181-export`. Stacked behind #1820 in the same chain.
- #1818 (0428-078, STALE, foreign authors w21-pr1702/w53-0428-152): absorb hop onto develop, re-land under `w165-0428-078-pr1650-basehop`.
- #1812 (0428-249, STALE, foreign authors; card owner blank): absorb hop onto develop, re-land under the verbatim owning lane. NOTE: 0428-249 card owner is blank; per the coordinator ownership-transfer record on card t-20261125-0428-284-1812-postretry-gate-failure, #1812 requalification runs under card 0428-284 owner `w198-0428-284-demo-parser`. The re-land identity for #1812 must therefore be confirmed with the coordinator (blank owner -> UNKNOWN-LANE by exact-equality; do not guess).
- #1650 (0428-078, STALE, mixed own-lane w165-0428-078-pr1650-basehop + foreign w181-0428-doclink-sweep): absorb hop onto develop, re-land foreign commit under `w165-0428-078-pr1650-basehop`.
- demo #179 (0428-284, CURRENT, CANONICAL): none.
- demo #170 (0428-250, CURRENT, FOREIGN author `Flash`): re-land future commits under `w50-0428-250-corefixture`; no hop needed (base is current).

## Root cause (consistent with card 0428-224 / prior w155 audit)

- Candidate commit authorship is NOT lane-deterministic across lanes sharing the checkout (last-writer-wins on `user.name`). This sweep reproduces the exact 0428-224 symptom: 0 of 7 baseharbor PR heads authored exclusively by their owning lane; every head carries at least one foreign author. Demo: 1 of 2 canonical.
- The fix is a prompt-only change to `coordinator/scripts/dispatch-lane.sh` (Owner scope: scripts/**) — the CANDIDATE COMMIT IDENTITY ADMISSION RULE (card t-20261121 / w155). Fix-forward: any new commit uses `git -c user.name=<lane> -c user.email=<lane>@baseharbor.local commit ...` with a pre-push `git show -s --format=%an HEAD` gate. No history rewrite, no head rewrite, no merge — all Owner decisions.

## Scope / rules compliance

- Read-only mission: no product commit, no plan-dir mutation, no push, no CI trigger, no rerun, no merge, no force-push.
- No `.github/**` edits; no runner build/register/repair.
- No subagents: every step executed in this own session.
- No container/compose project started on any host; nothing to bring down.
- Plan reads via isolated worktree `workers/w256-plan` (planrem remote, detached HEAD), removed at END. The plan-dir `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` was only `git ls-tree`-read against origin/main, never modified.

## Evidence witnesses

- baseharbor `develop` exact head: `git ls-remote ssh://git@github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`.
- baseharbor-demo `develop` exact head: `git ls-remote ssh://git@github.com/mcpdev80/baseharbor-demo.git refs/heads/develop` -> `5ca92a7cd2f746934890cfd7096a48068bdf218e`.
- baseharbor open PRs (count 7): 1842, 1833, 1820, 1819, 1818, 1812, 1650 (`gh pr list --repo mcpdev80/baseharbor --state open`).
- baseharbor-demo open PRs (count 2): 179, 170 (`gh pr list --repo mcpdev80/baseharbor-demo --state open`).
- Ancestry: `git merge-base --is-ancestor <develop-sha> <prhead-sha>` in throwaway clone at /tmp/w256-sweep (clone removed at END). 1842 + demo 179/170 -> holds; 1833/1820/1819/1818/1812/1650 -> fails.
- Identity via `gh api repos/mcpdev80/baseharbor[/baseharbor-demo]/pulls/<n>/commits --paginate --jq '.[] | .commit.author.name'`; `.author.login`/GitHub login ignored.
- Owning-card frontmatter owners read from baseharbor-plan origin/main task files (verbatim): 0428-284 `w198-0428-284-demo-parser`; 0428-288 `w147-0428-288-pr1833-fix`; 0428-271 `w69-0428-271-brokerid2`; 0428-181 `w54-0428-181-export`; 0428-078 `w165-0428-078-pr1650-basehop`; 0428-250 `w50-0428-250-corefixture`; 0428-249 (blank).

## Cleanliness

- `docker ps -a` (no daemon started): n/a — no docker/podman used.
- `docker compose ls` / `podman ps -a`: n/a — no compose project started.
- Scratch clone `/tmp/w256-sweep` removed at END (not in the ecosystem root).
- Plan read-worktree `workers/w256-plan` removed at END.
- No orphans anywhere.

## END

END_DONE w256-0428-253-prhopverify: read-only PR-hop + identity sweep complete; 1 CURRENT + 6 STALE (baseharbor), 2 CURRENT + 0 STALE (demo); 0 of 7 baseharbor PR heads authored exclusively by owning lane; tables + recommendations delivered in this akte.
