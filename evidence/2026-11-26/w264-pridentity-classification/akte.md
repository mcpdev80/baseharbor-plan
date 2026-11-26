# PR commit-author identity classification — w264

- Mission: `coordinator/missions/w264-pridentity-class.txt`
- Role: `REVIEW`
- Date: 2026-11-26
- Scope: read-only classification of the seven named open `mcpdev80/baseharbor` PR heads. No product repository changes, branch updates, force-pushes, history rewrites, card edits, or product CI runs were made.
- Planning publication: this file is carried by a branch based on live `baseharbor-plan` `main`; it is not a direct-main write.
- GitHub identity checked: `gh api user` returned `mcpdev80`.
- Model/session: Codex TUI reports thread kind `codex`; its available session metadata does not expose a gateway model string. No model name is inferred here.

## Rule applied

The expected identity is the exact `owner:` value in the owning card's frontmatter on live Planning `main`. For each PR, I fetched `refs/pull/<number>/head` and read every commit's `.commit.author.name`. An identity unequal to the card owner is class (i) only where the commit is an explicitly documented shortened spelling of that same lane. Otherwise it is class (ii), a genuinely foreign lane commit. No class-(i) exception was established in these seven candidates. A different lane on the same card remains a different lane; a merge/rebase commit or green CI does not admit its author identity.

## Live candidate and owner table

| PR | branch | fetched head | card / task | canonical `owner:` | commit identities and classification |
| --- | --- | --- | --- | --- | --- |
| #1833 | `lane-0428-288-compose-ids` | `a7b0a48048c11d20234160eede941532ddc33156` | 0428-288 / `t-20261116-r28-bug-compose-service-ids` | `w147-0428-288-pr1833-fix` | 6/6 foreign: `w121` (3), `lv4-verify` (2), `w124` (1) |
| #1820 | `fix/broker-build-identity` | `8f6b2444bdc9baabf4f492e930533c7c36406979` | 0428-271 / `t-20261124-r28-broker-build-identity-commit` | `w69-0428-271-brokerid2` | 18/18 foreign: `0428-061-sourcepull` (4), `w54-0428-181-export` (2), `lv4-verify` (6), `Codex` (1), `w198-0428-284-demo-parser` (2), `w205` (1), `w219-0428-271-0428-286-1820hop` (1), `w231-0428-285-1820restack` (1) |
| #1819 | `w54-0428-181-export` | `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` | 0428-181 / `t-20261120-r28-identity-dashboard-catalog-consumer` | `w54-0428-181-export` | 2 canonical (`w54`); 9 foreign: `0428-061-sourcepull` (1), `Codex` (1), `lv4-verify` (5), `w198-0428-284-demo-parser` (1), `w205` (1) |
| #1818 | `lane-0428-078-cf-fix` | `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` | 0428-078 / `t-20261114-r28-perses-dashboard-identity` | `w165-0428-078-pr1650-basehop` | 4/4 foreign: `w21-pr1702-0428-246-footprint` (3), `w53-0428-152-alertfix` (1) |
| #1812 | `lane-0428-249-runtime-image-fix` | `0922888af8fd70be4049cec529c69aebc057a356` | 0428-249 / `t-20261122-runtime-image-registry-artifact-unknown` | `w170-0428-249-demo-pr175-fixup` | 9/9 foreign: `Codex` (1), `lv4-verify` (5), `w198-0428-284-demo-parser` (3) |
| #1650 | `lane-0428-078-perses-identity-on-resolver` | `37c4d847ca377d1555163ac4791c8ba08b85de77` | 0428-078 / `t-20261114-r28-perses-dashboard-identity` | `w165-0428-078-pr1650-basehop` | 8 canonical (`w165`); 2 foreign: `w181-0428-doclink-sweep` (2) |
| #1842 | `w177-0428-284-demo-pin-1812` | `dfd3495858501fe49d9c331c056a4289b780e0f8` | 0428-284 / `t-20261125-0428-284-1812-postretry-gate-failure` | `w198-0428-284-demo-parser` | 8 canonical (`w198`); 3 foreign: `w177-0428-284-demo-pin-1812` (2), `w205-0428-253` (1) |

**Result:** 0/7 heads are authored exclusively by their card's canonical lane. There are 51 genuinely foreign commits across the seven heads. No shortened-same-lane documented exception was found. The `w205` author on #1820/#1819 is not admitted as shortened documentation: its commit is a merge of PR #1812 into another candidate, not documentation of card 0428-253. The two `w177` commits on #1842 are a separate lane, not a shortened spelling of owner lane `w198`.

## Foreign commit witnesses

Short SHAs below are unique within the fetched PR histories. They preserve a direct path from each classification to the exact commit object.

| PR | foreign commit SHAs |
| --- | --- |
| #1833 | `4064a6317b0c`, `92d3267ebf5e`, `3926495324a6`, `9e6b2957f02f`, `b9d312bce8ec`, `a7b0a48048c1` |
| #1820 | `22ca61bb97b9`, `2f9f2f050bda`, `514084f3c9be`, `9f84f47a7678`, `17381017be98`, `28803d110271`, `9140b2cbdf3c`, `64d3dc0e764e`, `2ea416209952`, `3859d4663489`, `101291960531`, `eafd5e6d641a`, `394559ec6cf5`, `a3ee25f63c5f`, `b3c5055ad256`, `34142a2a0a81`, `52e08e365b0d`, `8f6b2444bdc9` |
| #1819 | `17381017be98`, `9140b2cbdf3c`, `64d3dc0e764e`, `2ea416209952`, `3859d4663489`, `101291960531`, `eafd5e6d641a`, `394559ec6cf5`, `a3ee25f63c5f` |
| #1818 | `e0a93ce0347b`, `888e2193b3f2`, `8e2c50c10a53`, `20fc1cb7d496` |
| #1812 | `9140b2cbdf3c`, `64d3dc0e764e`, `2ea416209952`, `3859d4663489`, `101291960531`, `eafd5e6d641a`, `394559ec6cf5`, `f166a49f2634`, `0922888af8fd` |
| #1650 | `ed2fb751a45e`, `f89f506f50c2` |
| #1842 | `28b82c00bf2c`, `50c6d84e6e4a`, `9b5f4976d422` |

## Coordinator reissue missions

These are dispositions only; no reissue was dispatched or product branch modified. Each reissue uses a fresh lane/branch and the card's exact `owner:` identity for every new commit. Keep the old PR head intact as audit evidence; do not rewrite, force-push, or cherry-pick. Recreate only the scoped changes on the appropriate current dependency base. A green run or base hop alone cannot close an identity finding.

| PR | concrete reissue mission |
| --- | --- |
| #1833 | Proposed fresh lane branch `wNNN-pr1833-0428-288-identity-reissue`; card 0428-288, owner `w147-0428-288-pr1833-fix`: after its recorded sequencing gate (Demo pin advance and #1842), reimplement the Compose workload-ID fix and regression (`internal/application/workload.go`, `internal/application/manifest_validation.go`, `internal/application/workload_test.go`) plus the needed trusted gate catalog delta (`scripts/pr-gate-coverage.json`). Use owner identity for each new commit; preserve the task's current wait/requalification state until the dependency is actually satisfied. `NNN` is assigned only when the coordinator dispatches the fresh lane. |
| #1820 | Proposed fresh lane branch `wNNN-pr1820-0428-271-identity-reissue`; card 0428-271, owner `w69-0428-271-brokerid2`: after #1819 is resolved in the required chain, reimplement the broker exact-commit readiness behavior and acceptance regressions (`cmd/baha/app_broker.go`, `cmd/baha/app_broker_compat_test.go`), with the necessary 0428-271 catalog rows. Keep #1812/#1819/#1820 as separate scoped PRs; do not carry their foreign commits as 0428-271 work. `NNN` is assigned only when the coordinator dispatches the fresh lane. |
| #1819 | Proposed fresh lane branch `wNNN-pr1819-0428-181-identity-reissue`; card 0428-181, owner `w54-0428-181-export`: after the #1812 prerequisite is resolved, reimplement the Perses export producer and byte/hash-stability regressions (`internal/metrics/perses_dashboard_provision.go` and its tests). New implementation and regression commits use the exact owner identity; keep #1820's dependent stack ordered after this card. `NNN` is assigned only when the coordinator dispatches the fresh lane. |
| #1818 | Proposed fresh lane branch `wNNN-pr1818-0428-078-identity-reissue`; card 0428-078, owner `w165-0428-078-pr1650-basehop`: reimplement the Keycloak provider-class dashboard queries, JSON dashboard, and catalog wiring (`internal/metrics/perses_dashboards_keycloak.go`, dashboard tests, `docs/perses-dashboards/keycloak-identity.json`, `internal/metrics/perses_dashboards.go`). Do not include the foreign #1650 history; coordinate the two open PRs against the same card before publication. `NNN` is assigned only when the coordinator dispatches the fresh lane. |
| #1812 | Proposed fresh lane branch `wNNN-pr1812-0428-249-identity-reissue`; card 0428-249, owner `w170-0428-249-demo-pr175-fixup`: re-publish only the 0428-249 runtime-image/manifest failure fix, including the workflow ordering/reload change in `.github/workflows/pre-release-runtime-suite.yml` and its card-scoped acceptance reference. Reconcile the current closed card and open PR before dispatch; exclude the foreign 0428-284 app-init commits (`cmd/baha/app_init_*`) and unrelated release-catalog merge history. `NNN` is assigned only when the coordinator dispatches the fresh lane. |
| #1650 | Proposed fresh lane branch `wNNN-pr1650-0428-078-identity-reissue`; card 0428-078, owner `w165-0428-078-pr1650-basehop`: re-publish the current 0428-078 identity witness, fallback behavior, and regression coverage from the 0428-078 scope with owner-authored commits. Exclude the two unrelated #1843 arithmetic documentation commits (`w184-arithmetic.md`, added then removed by `w181-0428-doclink-sweep`). Keep any pre-existing #1650 work intact as audit evidence. `NNN` is assigned only when the coordinator dispatches the fresh lane. |
| #1842 | Proposed fresh lane branch `wNNN-pr1842-0428-284-identity-reissue`; card 0428-284, owner `w198-0428-284-demo-parser`: reimplement the release-aware demo pin selector and its gate coverage (`scripts/pr-gate-plan.py`, `scripts/test_pr_gate_coverage.py`, `docs/releases/v0.4.28.demo-ref`). Recreate the current develop integration with a normal merge authored by the owner lane; do not carry the separate `w177` lane commits or the #0428-253 merge commit. `NNN` is assigned only when the coordinator dispatches the fresh lane. |

## Evidence and method

- Plan `main` observed at publication setup: `264e2632319bdab152e7b03b7bd8bd0b3656bce9` (fetched from `origin/main`; later than the previously observed `8ae7436de854c4aa5c3ae55412390d91b4d6339e`).
- Product `develop` observed by `git ls-remote`: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`.
- PR heads fetched into an isolated bare repository from `https://github.com/mcpdev80/baseharbor.git` using `refs/pull/{1833,1820,1819,1818,1812,1650,1842}/head`; resulting SHAs are in the table above.
- Per-commit author names and messages cross-checked with `gh api repos/mcpdev80/baseharbor/pulls/<n>/commits`; commit files cross-checked from the fetched objects with `git show --stat`.
- Canonical owner values read from the corresponding task frontmatter on live Planning `origin/main`, including 0428-249 owner `w170-0428-249-demo-pr175-fixup`.
- Account witness: `gh api user --jq .login` -> `mcpdev80`.
- The shared `baseharbor-plan` checkout was not changed. Its existing tracked modification to `tasks/t-20261122-runtime-broker-health-unhealthy.md` was preserved. Planning validation/publication uses this clean isolated clone and a branch from live main.

## Addendum — author-level ruling for #1842 and #1650

Classification is relative to the owning PR card's exact frontmatter owner. The class-(i) exception is only for a same-lane spelling variant used to document that same lane's own card. A commit from another lane remains class (ii), even if its lane name contains the same card number or its change is useful to the PR.

| PR / SHA | author name | author email | subject | author lane's card mapping | class relative to this PR |
| --- | --- | --- | --- | --- | --- |
| #1842 `28b82c00bf2c` | `w177-0428-284-demo-pin-1812` | `w177-0428-284-demo-pin-1812@baseharbor.local` | `chore(release): bump demo_ref pin to merged develop tip 1a3c055 (post #175 consent retry)` | 0428-284 lane `w177-0428-284-demo-pin-1812`; PR card owner is `w198-0428-284-demo-parser` at `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md:10` | **(ii) GENUINELY FOREIGN** — different lane from the card's frontmatter owner; not a shortened spelling of `w198-0428-284-demo-parser`. |
| #1842 `50c6d84e6e4a` | `w177-0428-284-demo-pin-1812` | `w177-0428-284-demo-pin-1812@baseharbor.local` | `chore(pr-gate): make demo-ref pin selection release-aware (v0.4.28)` | 0428-284 lane `w177-0428-284-demo-pin-1812`; PR card owner is `w198-0428-284-demo-parser` at `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md:10` | **(ii) GENUINELY FOREIGN** — different lane from the card's frontmatter owner; not a shortened spelling of `w198-0428-284-demo-parser`. |
| #1842 `9b5f4976d422` | `w205-0428-253` | `w205-0428-253@baseharbor.local` | `Merge commit 'ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee' into HEAD` | Card 0428-253, owner frontmatter `w205 (lane w205-0428-253)` at `tasks/t-20261123-planner-deleted-source-advisory.md:10` | **(ii) GENUINELY FOREIGN** relative to PR #1842's owner `w198-0428-284-demo-parser`. It is a long-form identity for the separate 0428-253 lane, not a short form of the 0428-284 owner. Any case-specific 0428-253 shortened-form admission does not transfer this commit to card 0428-284. |
| #1650 `ed2fb751a45e` | `w181-0428-doclink-sweep` | `w181-0428-doclink-sweep@baseharbor.local` | `docs: reconcile PR #1843 row count from 40 to itemized 38 (H-V44 arithmetic)` | Card 0428-319, owner `w181-0428-doclink-sweep` at `tasks/t-20261125-hunt44-doclink-repair-sweep.md:10`; PR #1650 card owner is `w165-0428-078-pr1650-basehop` at `tasks/t-20261114-r28-perses-dashboard-identity.md:10` | **(ii) GENUINELY FOREIGN** — different card/lane; not a shortened spelling of the 0428-078 owner. |
| #1650 `f89f506f50c2` | `w181-0428-doclink-sweep` | `w181-0428-doclink-sweep@baseharbor.local` | `docs: remove stray top-level file from #1843 (keep docs/**-only)` | Card 0428-319, owner `w181-0428-doclink-sweep` at `tasks/t-20261125-hunt44-doclink-repair-sweep.md:10`; PR #1650 card owner is `w165-0428-078-pr1650-basehop` at `tasks/t-20261114-r28-perses-dashboard-identity.md:10` | **(ii) GENUINELY FOREIGN** — different card/lane; not a shortened spelling of the 0428-078 owner. |

No one of these five commits is admissible class (i) documentation for the respective PR's owner lane. For #1842, a forward-only identity-attesting commit on the existing branch would leave these foreign ancestors in the PR history and therefore cannot cure the finding. The admissible reissue is a fresh single-lane branch under the exact frontmatter owner `w198-0428-284-demo-parser`, re-applying only card 0428-284's write-set; keep the old #1842 head intact as contaminated-lineage audit evidence and close the old PR only after the replacement is reviewable. This does not rewrite history or force-push.
