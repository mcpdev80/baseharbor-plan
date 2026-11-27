# Independent review of BaseHarbor PR #1878

## PLAN

1. Read the mission and record this numbered plan in the live board and this Plan evidence before Git actions.
2. Verify fresh PR #1878 head/base/mergeability, stable remote refs, terminal required checks on the exact head, and two distinct run IDs.
3. Inspect the exact diff against develop for docs-only scope, disjointness from #1874–#1877, and absence of workflow/product/auth changes.
4. Compare documentation with card acceptance for endpoint name, port/bind, and operator guidance; determine whether required docs gates ran.
5. Merge normally only on complete PASS; otherwise send w397 a precise repair recipe and hold.
6. Publish this evidence through an isolated Plan PR, wait for exact-head Plan validation, verify the evidence path on origin/main, and report the verdict.

## Visible commit identity block

- Card 0428-342 owner, verbatim from current Plan origin/main before first commit: `owner: ""` (fetched verbatim from current Plan main `cb3b1b0d326225441f4927f6f81a7d1398dbe98a`).
- Session lane / Git user.name: `w267-0428-284-pridentity`.
- Git user.email: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity`.

## Review status

## Review findings

- Fresh PR #1878 state: OPEN, non-draft, mergeable, `mergeStateStatus=CLEAN`; branch `w397-0428-342-metricsdocs`, exact head `b63bea30aaba0899bf045a7bd0ec98ffcc819bfd`, base `develop` `ea5218d72e263f21e79853b679af50074dab8c25`.
- Product remote truth sampled from GitHub: `ea5218d72e263f21e79853b679af50074dab8c25 refs/heads/develop`; the current PR head was queried from `refs/pull/1878/head` on the final stability check below.
- PR changed files are exactly `docs/de/how-to/operator-api.md` (+11) and `docs/how-to/operator-api.md` (+9). No overlap with #1874 (`cmd/baha`, `internal/cli`, help docs, gate catalog), #1875 (`cmd/baha/app_workload.go`, fallback test, gate catalog), #1876 (`scripts/pr-gate-coverage.json`), or #1877 (`cmd/baha/app_workload.go`, fallback test, gate catalog). No product implementation, auth/consent, or workflow path is in this diff.
- The source confirms `GET /metrics` registration at `internal/runtimeexecutor/server.go:121`, default `0.0.0.0:9443` when no listen address is configured at `:61-65`, and TLS minimum 1.2 plus required and verified client certificate at `:127-139`. The executor compose definition supplies `BASEHARBOR_EXECUTOR_LISTEN_ADDR` at `internal/runtimeexecutor/compose.go:266`.
- Blocking factual discrepancy: both documentation paragraphs claim the override is `BASEHARBOR_RUNTIME_EXECUTOR_LISTEN_ADDR` (EN line 125, DE line 130), while the current executor compose configuration uses `BASEHARBOR_EXECUTOR_LISTEN_ADDR`. The PR must confirm the runtime's supported setting and align both languages or omit the unsupported override claim. I did not find source support for the documented variable in the reviewed source.
- Blocking German documentation defect at `docs/de/how-to/operator-api.md:129-135`: untranslated “behind”, malformed “Executor-Blatt-Blatt”, awkward “Bediene-API-Oberfläche”, and the incorrect mid-sentence capitalization “Überschreibbar”. It needs idiomatic technical German while preserving the endpoint, bind, TLS, and certificate facts.
- PR comments, submitted reviews, and inline review comments each returned zero. This is not evidence of approval.

### Exact-head checks

- Run `46002973690` is the only executed PR run found on this exact head: event `pull_request`, completed/success, head `b63bea30aaba0899bf045a7bd0ec98ffcc819bfd`.
- Its `PR Selected Checks` job `140521801027` completed/success. Executed successful relevant jobs include `PR · Source format` (`140519033802`), `PR · Focused Python` (`140519120697`), `PR · Validation · documentation-audit` (`140519120783`), `PR · Validation · mkdocs-en-strict` (`140519120824`), `PR · Validation · pages-candidate-build` (`140519120838`), and `PR · Validation · mkdocs-de-strict` (`140519120914`). Selected Docker onboarding jobs also completed successfully. Release-matrix jobs were skipped, as required for this docs-only scope.
- Exact-head run count: NO, only one distinct run ID is present. No rerun or workflow_dispatch was triggered. Since the documentation defects already require a new head, no close/reopen trigger was initiated for this candidate.

## Review decision and lane handoff

- Check 1 (stable head, required completed checks, two IDs): NO. Head is currently mergeable and one exact-head run is green, but two distinct run IDs are not available.
- Check 2 (docs-only, disjoint write-set, no workflow/product/auth changes): YES.
- Check 3 (endpoint, bind/port, operator guidance without unsupported behavior): NO pending correction of the unsupported environment-variable claim; endpoint name, default bind/port, and separation from Core are otherwise present and source-backed.
- Check 4 (docs gates, no release matrix): YES for the observed exact-head run; documentation audit and EN/DE strict builds completed successfully, and no release-matrix run was executed.
- Sent w397-0428-307-idfallback a focused correction recipe: verify and align the executor listen-address environment variable in both language files, and rewrite the malformed German paragraph. Preserve the two-doc write-set. After the corrected candidate is pushed, obtain two distinct executed run IDs on that exact head using the authorized close/reopen sequence if needed; do not rerun the same ID.
- Merge decision: NO. No product merge performed; do not merge until factual and German-copy findings are resolved and two exact-head successful run IDs exist.

## Repo-rule compliance

- Product review was read-only; no product file or workflow was modified.
- No local test suite was run. CI receipts were read from GitHub Actions.
- No rerun or workflow_dispatch was initiated. Review recipe was sent to the active implementation lane.
- Evidence remains in the Plan repository only.

## Initial-head disposition

The initial candidate `b63bea30aaba0899bf045a7bd0ec98ffcc819bfd` was held for an unsupported listen-address variable and malformed German copy. The lane corrected the variable on the next exact head; the remaining DE-copy finding is recorded below.

## Plan repository provenance before branch creation

- Exact Plan ref cut from: `cb3b1b0d326225441f4927f6f81a7d1398dbe98a refs/heads/main`, measured with `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` before creating the evidence branch.
- Verified correct Plan repository remotes before first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- The task owner on that exact fetched Plan main is `owner: ""`; the earlier `w397` frontmatter observation was on prior Plan main `f751c83d3a765cf1bbecd3dc43f9cb63841bbdae` and is superseded by the exact current ref.

## Planning validation state

- In the isolated Plan worktree cut from `cb3b1b0d326225441f4927f6f81a7d1398dbe98a`, `python3 scripts/plan.py render && python3 scripts/plan.py check` reported `784 tasks, 7 epics, 24 decisions; 4 errors, 10 warnings`.
- The four errors are in the already-existing assigned task note `tasks/t-20261128-hunt48-metrics-endpoint-docs.md`: review status requires an owner; blocker is set but status is not blocked; evidence must be HTTPS; the relative evidence path `evidence/2026-11-27/0428-342/akte.md` is broken. This card note is outside this independent product-PR review's authorized write-set; no task metadata was changed.
- The task note currently has `owner: ""` and a blocker requesting coordinator reconciliation. I am not changing that shared planning card in this review. Therefore the Plan validation is an explicit publication blocker; the evidence branch can be preserved for review, but its Plan PR must not be merged unless the card issue is resolved by its authorized owner and validation is green.

## Current product remote witness

- Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1878/head` returned `ea5218d72e263f21e79853b679af50074dab8c25 refs/heads/develop` and `b63bea30aaba0899bf045a7bd0ec98ffcc819bfd refs/pull/1878/head`.
- Fresh PR API state remained OPEN/non-draft/mergeable with clean merge state and the same head/base. Run census remains only `46002973690` completed/success on that exact head.

- Plan `origin/main` advanced to `5725634c07129110bc3d4e8850e4fdc4c02e806e` before evidence publication. I rebased only this unpublished evidence commit in its isolated worktree; the original branch-cut SHA `cb3b1b0d326225441f4927f6f81a7d1398dbe98a` remains its ancestor. Current `git merge-base --is-ancestor origin/main HEAD` succeeded and the branch diff remains this evidence file only.
- Repeated `python3 scripts/plan.py render && python3 scripts/plan.py check` on current Plan main still reports the same four errors and 10 warnings above. No generated or task files were changed.
- An earlier rebase invocation from the shared Plan checkout was rejected immediately because that checkout has unstaged changes; it made no working-tree change. The successful one-commit rebase was then run only in this isolated worktree.

## Plan commit identity witnesses

- `git log --format='%h an=%an cn=%cn' origin/main..HEAD` after the first evidence commit returned `5f8edf89a an=w267-0428-284-pridentity cn=w267-0428-284-pridentity`.
- The current evidence amendment commit was mechanically checked with `git show -s --format=%H%n%an%n%cn HEAD`: `4b51694b252108d2a2fa3c22caa05cb3558a7ebd`, author `w267-0428-284-pridentity`, committer `w267-0428-284-pridentity`.

## Review refresh after implementation-lane update

- The lane updated the same PR branch. Fresh remote now reports head `698db93ad5b3657894bb90f268e5ac6cb2aa9fe6` on `w397-0428-342-metricsdocs`, base `develop` `ea5218d72e263f21e79853b679af50074dab8c25`, PR OPEN/non-draft/mergeable. `git ls-remote` confirmed both refs at that head/base.
- The environment variable discrepancy is fixed in both languages: docs now say `BASEHARBOR_EXECUTOR_LISTEN_ADDR`, matching `internal/runtimeexecutor/compose.go:266`. `GET /metrics`, `0.0.0.0:9443`, Core listener separation, and TLS/client-certificate requirements remain as before.
- One documentation issue remains in `docs/de/how-to/operator-api.md:129-135`: “Bediene-API-Oberfläche”, “Bediene-Endpunkt”, and “Executor-Blatt-Ausweis” remain unnatural or malformed technical terms. This is still a blocking DE-copy issue for the bilingual handoff; use established “Operator-HTTP-Oberfläche” terminology and “verifiziertes Executor-Clientzertifikat”, without changing the verified behavior.
- Current-head run census: `46007839655` is the sole successful executed run (event `pull_request`, completed/success on `698db93ad5b3657894bb90f268e5ac6cb2aa9fe6`); `PR Selected Checks` job `140538768878` completed/success. Run `46007801545` is a distinct `pull_request` run on the same head but was cancelled. Thus two successful distinct exact-head runs: NO. No rerun, workflow_dispatch, or second trigger was initiated by this reviewer.
- The current exact head passed docs audit, strict English and German MkDocs, pages candidate build, source format, and selected native Docker/Podman onboarding jobs in run `46007839655`. Release matrix jobs were skipped. All required observed selected checks completed successfully, but they do not resolve the copy finding or supply a second successful run ID.
- The active implementation lane received the narrowed correction recipe for the remaining German terminology and exact-head run pair.
- Current verdict: check 1 NO (only one success; second run cancelled), check 2 YES (docs-only and disjoint), check 3 NO (German terms remain malformed), check 4 YES (docs gates green, no release matrix).
- The current Plan base is `c407807e5dd1c61300c8e19e19fac7a3aa8ebe4b`. Its changes were integrated into this published evidence branch with a normal canonical-lane merge commit `b0ff679bb0198ce9ae86918dd4ee36604769c58c` (author and committer `w267-0428-284-pridentity`); no history rewrite was used.

## Latest Plan-main and validation refresh

- Plan `origin/main` advanced to `5a6ccd11a1b1847ba34dd386ed263a462f767bed`. It now carries the authorized correction to task 0428-342: owner `w397-0428-342-metricsdocs`, blocker empty, and HTTPS evidence link. I integrated current main in isolated worktree merge commit `d71b8234ddcfc97de2acc77a75c66026bbc6b313` under the canonical reviewer identity; this is an ordinary merge, not a history rewrite.
- After that correction and merge, `python3 scripts/plan.py render && python3 scripts/plan.py check` reports `784 tasks, 7 epics, 24 decisions; 0 errors, 10 warnings`. The previously failed Plan validation run `46008182506` was on prior evidence head `e200846b49e5b9cda6e8d26fc9d8c8b3efa2efc2`; it must not be treated as validation of the updated branch. A fresh Plan validation is required for the updated evidence head.
- Latest product refs remain `ea5218d72e263f21e79853b679af50074dab8c25 refs/heads/develop` and `698db93ad5b3657894bb90f268e5ac6cb2aa9fe6 refs/pull/1878/head`. Exact-head successful run: `46007839655`; second distinct ID `46007801545` is cancelled.

## Final exact-head and Plan-PR recheck

- Fresh product `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1878/head` returned `ea5218d72e263f21e79853b679af50074dab8c25 refs/heads/develop` and `698db93ad5b3657894bb90f268e5ac6cb2aa9fe6 refs/pull/1878/head`.
- Fresh `gh pr view 1878 -R mcpdev80/baseharbor` reports OPEN, non-draft, `MERGEABLE`, `CLEAN`, base `develop`, exact head `698db93ad5b3657894bb90f268e5ac6cb2aa9fe6`. Run census still has only `46007839655` (pull_request, completed/success) and `46007801545` (pull_request, completed/cancelled) on that exact head. One green run is not a two-success pair; no product merge is authorized.
- Plan PR #232 remains OPEN at old head `e200846b49e5b9cda6e8d26fc9d8c8b3efa2efc2`; its only `Plan · validate` result is run `46008182506`, completed/failure on that old head. It does not validate this updated evidence branch. The local evidence branch is ahead with the latest review and Plan-main refresh; a new exact-head Plan validation is required after publishing the update.
- Product review decision remains blocked: check 1 NO (only one successful exact-head run), check 2 YES (docs-only/disjoint), check 3 NO (malformed German terminology remains at `docs/de/how-to/operator-api.md:129-135`), check 4 YES (docs audit and strict EN/DE builds passed; release matrix skipped for docs-only scope).

## END BLOCKED

END BLOCKED w267-0428-284-pridentity: PR #1878 held at exact head 698db93ad5b3657894bb90f268e5ac6cb2aa9fe6; only run 46007839655 succeeded, run 46007801545 was cancelled, and German wording remains unresolved. Evidence branch is not yet validated on its updated exact head.
