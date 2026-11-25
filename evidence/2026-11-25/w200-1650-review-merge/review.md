# Core PR #1650 exact-head review

## PLAN

1. Refresh BaseHarbor refs and resolve ancestry of the two disputed commits.
2. Compare PR #1650 exact head with the 0428-078 contract, prior isolation fix, catalog row, runtime gates, and author identity chain.
3. If all gates pass, merge normally and verify merge SHA and develop tip; otherwise record the blocker and prescribed next action.
4. Publish this evidence akte on baseharbor-plan origin/main and post the terminal lane status.

## Visible owner and commit ansatz

Fresh `origin/main` frontmatter verbatim: `owner: w165-0428-078-pr1650-basehop`.

Evidence commit identity: git user.name `w200-1650-review-merge`; git user.email `w200-1650-review-merge@baseharbor.local`.

Literal commit invocation: `git -c user.name='w200-1650-review-merge' -c user.email='w200-1650-review-merge@baseharbor.local' commit -m 'evidence: review core PR 1650'`.

Pre-push author gate: `git show -s --format=%an HEAD` must equal `w200-1650-review-merge`.

## Base and remotes

BaseHarbor remote audit repo: `origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `(push)`.
Planning repo remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
Planning evidence worktree base: `6b61a0e8c92bed0e00b075811cd214f2e4e1e9c0`.

## Ancestry and candidate provenance

Fresh BaseHarbor fetch refs: `origin/main=7bdeae95ccf0ce0d2fe39ae6d4c884402268995d`; `origin/develop=3a2ae6b1139570c98b8924e3b19975c56a289400`; `origin/pr/1650=1c33e910070a07a6d4105f0d38e3c89988a788a3`.

`git branch -r --contains ed2fb751` output:

```text
origin/lane-0428-078-perses-identity-on-resolver
origin/pr/1650
```

`git branch -r --contains f89f506f` output:

```text
origin/lane-0428-078-perses-identity-on-resolver
origin/pr/1650
```

Ancestor checks: `ed2fb751` in `origin/develop`: exit 1; in `origin/main`: exit 1. `f89f506f` in `origin/develop`: exit 1; in `origin/main`: exit 1. Therefore the disputed commits are not absorbed by current develop. Current PR base equals current develop, and `git merge-base --is-ancestor origin/develop origin/pr/1650` exits 0; no additional base hop is required for up-to-date status. The existing base-hop merge does not remove the foreign commits from the PR history.

`git log --oneline origin/develop..origin/pr/1650`:

```text
1c33e910 Merge remote-tracking branch 'origin/develop' into w206-0428-288-catalog
af256c3f fix(0428-078): correct identity_dashboard_witness.go catalog row to data.capabilities (CODEX-CONFIRMED v2)
156507ee fix(0428-078): declare runtime-gate owner for identity_dashboard_witness.go
903991f3 test(0428-078): per-test temp STATE_DIR in Perses dashboard fixtures
8e4a10f3 test(0428-078): isolate BASEHARBOR_TARGET/STATE_DIR in Perses dashboard fixtures
2c407318 fix(0428-078): reintroduce #1650 identity-keycloak dashboard witness on new develop (rebase-drop recovery)
b95df510 style(0428-078): retrigger full CI on hop head c6ba608f6 (second same-head run)
f89f506f docs: remove stray top-level file from #1843 (keep docs/**-only)
ed2fb751 docs: reconcile PR #1843 row count from 40 to itemized 38 (H-V44 arithmetic)
```

All 0428-078 commits shown above are authored/committed by `w165-0428-078-pr1650-basehop`; `ed2fb751` and `f89f506f` are authored by `w181-0428-doclink-sweep`. Tip author and committer are `w165-0428-078-pr1650-basehop`.

`git merge-base --is-ancestor origin/develop origin/pr/1650` exits 0. `git diff origin/develop...origin/pr/1650 --name-only`:

```text
cmd/baha/app_perses_cli_test.go
cmd/baha/app_status_result.go
internal/metrics/identity_dashboard_witness.go
scripts/pr-gate-coverage.json
```

## Exact-head review and qualification

Current PR API state: open, head `1c33e910070a07a6d4105f0d38e3c89988a788a3`, base `3a2ae6b1139570c98b8924e3b19975c56a289400`, mergeable true, merged false, no reviewDecision.

Run `45663047993` is `pull_request`, conclusion success, exact head `1c33e910070a07a6d4105f0d38e3c89988a788a3`. The four selected runtime jobs executed and passed: Docker data-capabilities `139378867270`, Docker observability `139378867469`, Podman data-capabilities `139378867487`, Podman observability `139378867660`. `PR · Trusted Plan` `139377732756` and terminal `PR Selected Checks` `139393082202` succeeded. The run census reported 27 success, 0 failure, 16 skipped by design.

Card contract was read fresh from baseharbor-plan `origin/main`: card `t-20261114-r28-perses-dashboard-identity`, number 0428-078, verbatim owner `w165-0428-078-pr1650-basehop`, goal “Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions.” The PR diff includes the earlier fixture isolation (`BASEHARBOR_TARGET` cleared and per-test temporary `BASEHARBOR_STATE_DIR`), the target-bound fail-closed Keycloak witness and derived eligibility, and no additional catalog row beyond the already collapsed single develop row (catalog file differs only by trailing newline). The exact-head content review is acceptable against this contract.

## Verdict and required handling

Verdict: CHANGES / merge blocked by candidate provenance. Do not rewrite foreign commits. The candidate is already up to date with current develop, so no further base-hop is needed and no base-hop run is ordered. Since the two commits remain unrelated to 0428-078 and outside current develop, resolve through owner escalation or the authorized fix-forward/transfer process; do not merge until the foreign-history disposition is resolved. No PR review or merge action was submitted.

END w200-1650-review-merge BLOCKED — foreign commits remain outside current develop; exact head 1c33e910070a07a6d4105f0d38e3c89988a788a3.
