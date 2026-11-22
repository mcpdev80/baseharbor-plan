# CODEX-REVIEW: PR #1627 exact-head review

## PLAN

1. Verify PR #1627 exact remote head, base pointer, merge state, and the specified hosted run.
2. Compare the exact candidate diff with develop and isolate commit fe4027f7 parent-to-child changes.
3. Confirm the fix changes only the test expectation and does not alter product semantics.
4. Inspect app_coreless_runtime_test.go:209 and app_capability_runtime_test.go:314 as contract witnesses.
5. Check candidate history and paths for foreign PR #1723/#1725 content, then publish the review evidence.

Role: CODEX-REVIEW, read-only. No merge, close, comment, tests, or subagents were performed by this review.

## Verdict

REQUEST CHANGES — post-merge provenance finding. The precise `fe4027f7986502a825b2c701fb53725f39434435` fix is correct and changes only a test expectation, but the candidate also contains foreign commit `0768274c6f692bc0779202a1b9dc1fb222fce2ef`, which is an ancestor shared by both referenced PR #1723 and PR #1725. It is not in the specified base `52a3c5446f41a1dd8678d99875e4cb1eee67874c`. This fails the mission's requirement that the branch history contain only its own commits and develop content and that foreign PR content not appear as an ancestor. The exact PR heads themselves (`12a62523fc5f2259220aece4cc5619dcb8f4ae4d`, `485103523b93d23877e2103974d7af22ef95f831`) are not ancestors of this candidate. The PR has already merged, so this is a post-merge scope finding; this review made no repository or PR changes.

The intended fix itself is sound. Parent-to-child comparison of `fe4027f7` shows changes only in `cmd/baha/env_destroy_integration_test.go`: the persisted deployment record expectation changes from `stopped` to `runtime-retired`, the assertion message follows that stored state, and the test adds a separate user-facing status assertion for `stopped` with `Ready=false`. No product source or runtime behavior changes in that commit.

Contract witnesses support this distinction. In `cmd/baha/app_coreless_runtime_test.go:204-210`, the `down` path asserts the collected user status is `stopped` while the retained persisted owner is `runtime-retired` and not ready. In `cmd/baha/app_capability_runtime_test.go:309-315`, the Core-backed Secrets case likewise asserts user status `stopped`, persisted state `runtime-retired`, readiness false, and retained retirement intent. The previous assertion in the env-destroy test conflated those two layers; the updated expectation corrects the test rather than changing product semantics.

### Exact-head hosted run

Run `44996713389` is terminal `completed/success` at the exact requested head `fe4027f7986502a825b2c701fb53725f39434435`: 32 jobs succeeded, 73 were skipped, and zero failed. `PR Selected Checks` job `137132582868` succeeded. The Docker aggregate `137132416299` and Podman aggregate `137132563518` succeeded; all eight visible Docker/Podman coreless-lifecycle component slices succeeded. `PR · Selected Runtime` job `137129281964` was skipped, so it is not evidence for runtime-selected coverage; the task record attributes that skip to the lagging base pointer (0428-235), not a rejection of this candidate.

At review time the PR was already closed as merged at `2026-11-22T07:24:02Z`, merge commit `acc343239681feb235a33cf00c8ea754c537291f`. The merge commit's parents are exactly base `52a3c5446f41a1dd8678d99875e4cb1eee67874c` and candidate `fe4027f7986502a825b2c701fb53725f39434435`; the remote `develop` ref points to that merge commit. The PR API currently reports closed/merged and records base SHA `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7`, which differs from the mission's base pointer; the merge commit parent proves the integration base actually used for this merge was the specified `52a3c544...`.

### Diff and ancestry

`git diff 52a3c5446f41a1dd8678d99875e4cb1eee67874c...fe4027f7986502a825b2c701fb53725f39434435 --name-only` returns:

```text
cmd/baha/application_provider_authorization.go
cmd/baha/commands.go
cmd/baha/env_destroy.go
cmd/baha/env_destroy_integration_test.go
cmd/baha/machine_coverage.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
internal/application/provider_preferences.go
internal/deployment/environment_destroy_scope.go
internal/deployment/environment_destroy_scope_test.go
```

No `.github/**`, `scripts/**`, or forbidden paths appear in this specified-base diff. The two provider-preferences files are the content of commit `0768274`, titled `fix(app): tolerate nil-vs-empty providerPreferences in revalidate`, authored by `0428-061-sourcepull`. The commit is not an ancestor of the specified base (`git merge-base --is-ancestor 0768274 52a3c544...` fails), but is an ancestor of candidate `fe4027...`, PR #1723 head `12a625...`, and PR #1725 head `485103...`. It is also in the current develop history only because the merge commit `acc343...` brought in this candidate; it was not base content at the review's integration point.

The full PR #1723 and #1725 heads are not ancestors of candidate `fe4027...`; the shared foreign commit `0768274` is. Thus the exact-head ancestry check passes while the stricter foreign-content requirement does not.

The candidate log after the specified base is:

```text
fe4027f7 test: match env destroy keep owner state
bfd01276 Merge commit '0768274c6f692bc0779202a1b9dc1fb222fce2ef' into HEAD
0768274c fix(app): tolerate nil-vs-empty providerPreferences in revalidate
2f0f8078 Merge commit '8b9a8f50645db1dbaad4a5e1f2140930436d3ea7' into HEAD
b3b0c2c9 test: prepare consent through destroy resolver
38be89aa test: bind env destroy consent to stop plan
ac05cc4e test: authenticate env destroy native fixture
62dd38f9 Merge develop 42da7128 into env destroy PR
8de37f58 ci: validate env destroy against coreless gates
d0616fc2 docs: retain env destroy rows in German coverage
5dd34a37 hop(0428-055): merge develop 513488eeb6d into cli2-env-delete for PR #1627
e24bd481 docs: sync environment destroy command indexes
3d8aff0d test: fix native env destroy test imports
81aa4ca8 fix: process selected environment deployments independently
dff06723 Merge remote-tracking branch 'origin/develop' into cli2-env-delete
202b984e revert(test): preserve active 1615 runtime test ownership
cf82fe45 test(cli): cover environment destroy on native runtime
bb0424da Merge current develop into 0428-055
e4777ac5 fix(cli): emit one confirmed environment destroy result
96deb1f1 fix(cli): destroy environment scoped deployments safely
49e164cc Merge commit '5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3' into cli2-env-delete
```

`merge-empfehlung:` The candidate's `fe4027f7` test-only correction is valid and its named Docker/Podman gates plus `PR Selected Checks` passed. However, the overall candidate fails the requested foreign-content ancestry rule because of `0768274`; it is already merged, so record and triage this as a post-merge scope finding rather than treating the PR as unmerged or attempting a correction here.

## Evidence and provenance

- Product remote: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push).
- `git ls-remote` observed `acc343239681feb235a33cf00c8ea754c537291f refs/heads/develop` and `fe4027f7986502a825b2c701fb53725f39434435 refs/pull/1627/head`.
- `git merge-base --is-ancestor 52a3c5446f41a1dd8678d99875e4cb1eee67874c fe4027f7986502a825b2c701fb53725f39434435` succeeded.
- `git diff 52a3c5446f41a1dd8678d99875e4cb1eee67874c...fe4027f7986502a825b2c701fb53725f39434435 --name-only` is the 12-path list above.
- Parent-to-child diff `fe4027f^..fe4027f` changes only `cmd/baha/env_destroy_integration_test.go`.
- `git merge-base --is-ancestor refs/remotes/review/pr1723 refs/remotes/review/pr1627` failed; `git merge-base --is-ancestor refs/remotes/review/pr1725 refs/remotes/review/pr1627` failed.
- `git merge-base --is-ancestor 0768274 refs/remotes/review/pr1723`, `...review/pr1725`, and `...review/pr1627` all succeeded.
- Planning remote `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` output:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## repo-rule compliance

- This was a read-only CODEX-REVIEW; no product files, PR state, tests, workflows, scripts, or branches were changed by the reviewer.
- No tests were run. Hosted CI facts above were read from the specified run.
- No Docker or Podman containers or compose projects were started.

## cleanliness

- `docker ps -a` before review completion, shell PID 3139823: output was the header only, no containers listed.
- `docker ps -a` after review inspection, shell PID 3140182: output was the header only, no containers listed. No containers were started or changed.

END_BLOCKED codex-rev2-1736: REQUEST CHANGES as a post-merge scope finding for #1627 at fe4027f7986502a825b2c701fb53725f39434435; test-only fix correct, run 44996713389 succeeded, but shared foreign commit 0768274 is ancestor of both #1723 and #1725; review evidence published on Planning main; shared commit 0768274 fails the foreign-content ancestry rule.


Exact output of `git fetch origin main && git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/cli-sourcepull/review-1627-headfe4027f7986.md'`:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
   794446b94..0dea01464  main       -> origin/main
evidence/r28-welle5-2026-11-22/cli-sourcepull/review-1627-headfe4027f7986.md
```
