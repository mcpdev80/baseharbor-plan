# Board reconciliation evidence — w255

## PLAN

- 1. Verify canonical card identity for PR #1879 and refresh exact PR heads, run witnesses, and Plan main.
- 2. Correct only the source-transfer and runtime-identity task metadata/wait evidence; preserve owners and PR lists, and align 0428-307 to `wait` because its accurate explanation is a `wait_reason`.
- 3. Run `card-status.py --no-push` for the 0428-307 status transition, then full Plan render/check; inspect the exact diff.
- 4. Commit with the canonical lane identity, open a Plan PR, and verify exact-head Hosted Plan validation.
- 5. Merge the Plan PR only after current-main ancestry, green validation, and review; record PR and resulting main SHA.

## Visible commit identity and base attestation

- Source-transfer card owner, verbatim from current `origin/main` frontmatter: `w392-0428-284-demo183fix5`.
- Runtime-identity card owner, verbatim from current `origin/main` frontmatter: `w397-0428-307-idfallback`.
- This lane's canonical Git `user.name`: `w255-0428-251-demo170codex`.
- This lane's Git `user.email`: `w255-0428-251-demo170codex@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.
- Planning remote verified before branch creation: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
- Exact Plan `origin/main` base fetched before branch creation: `395b663807fcb141b41a712f68074e71d1a09b71`.

## Findings and actions

### Source-transfer identity (#1879)

Canonical Plan identity is 0428-346. The current main card `tasks/t-20261128-hunt48-source-transfers-contract.md` has `card_number: "0428-346"` and `kanban_title: 0428-346 · source-transfers routes doc`. The separately existing `tasks/t-20261128-hunt48-unify-runtime-error-envelope.md` owns 0428-343. Therefore 0428-343 must not be added as an alias for the source-transfer card; the mismatched PR title/branch label is a PR-side label only and is not changed in this board-only scope.

Fresh PR API: #1879 is OPEN, title `docs(machine-http): register source-transfer routes in v1 contract (0428-343)`, branch `w392-0428-343-sctransfer`, head `7d3ca40a485cdc1162c41dd98736aa33a448777b`. `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1879/head refs/heads/w392-0428-343-sctransfer` returned that same SHA for both refs:

```text
7d3ca40a485cdc1162c41dd98736aa33a448777b refs/heads/w392-0428-343-sctransfer
7d3ca40a485cdc1162c41dd98736aa33a448777b refs/pull/1879/head
```

Its files are `docs/spec/machine-http-v1.md`, `internal/machinehttp/source_transfer_test.go`, and `scripts/pr-gate-coverage.json`. The card is explicitly titled 0428-346 · source-transfer contract; `aliases: []` avoids claiming 0428-343, which belongs to the distinct runtime-error-envelope card.

Exact-head run `46010924212`: https://github.com/mcpdev80/baseharbor/actions/runs/46010924212; event `pull_request`, head `7d3ca40a485cdc1162c41dd98736aa33a448777b`, completed/failure. `PR · Trusted Plan` and `PR Selected Checks` failed; `PR · Source format`, `Workflow policy`, and `PR · Native gate plan` succeeded. The wait text must not say “otherwise green.”

### Runtime-identity witnesses (0428-307)

Card owner verbatim: `w397-0428-307-idfallback`; state remains blocked; PR list remains #1875/#1876/#1877. Current product PR heads verified through `gh pr view` and `git ls-remote`:

- #1875 head `254621f5655051d087d79fb7668b683dcfda5b93`; run [45993507477](https://github.com/mcpdev80/baseharbor/actions/runs/45993507477) completed/failure on that exact head; `PR · Trusted Plan` and `PR Selected Checks` failed.
- #1876 head `98cb8a725ac78e56959ead4dd6b7757ebabde856`; runs [45993371732](https://github.com/mcpdev80/baseharbor/actions/runs/45993371732) and [45996668742](https://github.com/mcpdev80/baseharbor/actions/runs/45996668742) completed/success on that exact head. These are catalog-only PR receipts; the candidate catalog registration remains unmerged to develop, so they do not clear #1875/#1877's trusted-base blocker.
- #1877 head `013fdfb82cf9dcab862aa430459bd880c0a806fd`; run [45998693008](https://github.com/mcpdev80/baseharbor/actions/runs/45998693008) completed/failure on that exact head; `PR · Trusted Plan` and `PR Selected Checks` failed.
- Runs [45993109149](https://github.com/mcpdev80/baseharbor/actions/runs/45993109149) and [45994654068](https://github.com/mcpdev80/baseharbor/actions/runs/45994654068) are on #1874 head `b143395545bd2c5c4bd637ad476a5c4cc78630a4`, not any 0428-307 PR head, and are excluded as 0428-307 witnesses.

## Scope

Only the two named task cards, generated Plan views, and this evidence are in scope. 0428-307 moves from `blocked` to `wait` through the required `card-status.py` path: the underlying hold is pending external catalog/freeze-lift action and its explanation belongs in `wait_reason`; the planner rejects `wait_reason` on non-wait cards. Its owner and PR list remain unchanged. No product PR, product branch, or workflow changes are authorized.

## Validation and renderer footprint

- `card-status.py t-20261125-hunt37-runtime-identity-fallback wait --wait-reason ... --no-push` completed successfully against the isolated clone using a temporary runtime config pointed at this clone; it preserved owner and PR list, cleared the now-inapplicable blocker field, and rendered/checked the full Plan tree.
- Final `python3 scripts/plan.py render && python3 scripts/plan.py check`: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 existing accepted-dependency warnings.
- The full renderer refreshed generated previews in `tasks/t-20261116-r28-bug-apply-consent-ux.md` and `tasks/t-20261125-hunt42-timeout-constant-matrix.md`; `plan.py check` reported both stale generated previews as errors when reverted, so those generated-only preview changes are retained. Their frontmatter/status is untouched.

## Branch provenance and commit receipt

- `git merge-base --is-ancestor origin/main HEAD` passed; the branch was cut from Plan main `395b663807fcb141b41a712f68074e71d1a09b71` and contains only this lane's work.
- `git diff origin/main...HEAD --name-only`:

```text
evidence/2026-11-27/board-reconcile-w255/akte.md
releases/v0.4.28.md
roadmap/cards.md
tasks/t-20261116-r28-bug-apply-consent-ux.md
tasks/t-20261125-hunt37-runtime-identity-fallback.md
tasks/t-20261125-hunt42-timeout-constant-matrix.md
tasks/t-20261128-hunt48-source-transfers-contract.md
views/kanban-dashboard.md
views/overview.md
views/releases/v0.4.28.md
```

- `git log --oneline origin/main..HEAD` lists only this lane's commits: `df47132 place board reconciliation akte in canonical evidence tree`; `b76ded5 record pre-push identity receipt`; `6ebe1fd record board reconciliation provenance`; `8f0b7c9 reconcile source-transfer identity and runtime receipts`.
- Commit `8f0b7c92c1ad23137afb150bf733b250f615c74c` author and committer are both `w255-0428-251-demo170codex`; pre-push author gate is `git show -s --format=%an HEAD` → `w255-0428-251-demo170codex`.
- Before the evidence-provenance commit push, `git log --format='%h an=%an cn=%cn' -1` printed `6ebe1fd an=w255-0428-251-demo170codex cn=w255-0428-251-demo170codex`; `git show -s --format=%an HEAD` printed `w255-0428-251-demo170codex`.
- Before the evidence-path push, `git log --format='%h an=%an cn=%cn' -1` printed `b76ded5 an=w255-0428-251-demo170codex cn=w255-0428-251-demo170codex`; `git show -s --format=%an HEAD` printed `w255-0428-251-demo170codex`.
- After that push, `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w255-0428-251-demo170codex-board-reconcile` returned `df471323b7b9ebdfca1da52280007858ca50237b refs/heads/w255-0428-251-demo170codex-board-reconcile`.
- END w255-0428-251-demo170codex DONE — reconciliation and review handoff completed; final Plan main SHA is reported in the coordinator END.
