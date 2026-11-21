# CODEX-REVIEW — PR #1625, card 0428-065

## PLAN
1. Verify live PR #1625 head and its branch ref match the mission SHA `6585feaac37`; stop if they differ.
2. Verify run 44952948703 is terminal success on that exact head and inventory actual versus skipped jobs.
3. Inspect the exact candidate diff for secret-safe stdout/stderr, operator-denial attribution to `baha login`, and fail-first proof.
4. Verify author/committer identity and candidate ancestry/parity against its stated base.
5. Record the per-case receipt as `open item, owner-scope receipt-tooling`; it is non-blocking under the sequence correction.
6. Publish a complete review-only verdict in this lane-owned Planning worktree; no product changes, comments, merges, closes, or local suite tests.

## Planning remote
`origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push). Raw `git remote -v` output:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```, previously verified before evidence commits in this worktree.

## Exact head, identity, and CI

- Product remote: `https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote` at review: `513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop`, `6585feaac37c8d634f6de6be1079a17caf89d107 refs/heads/lane-0428-065-cli2-app-export`, and `6585feaac37c8d634f6de6be1079a17caf89d107 refs/pull/1625/head`.
- PR #1625 is OPEN, non-draft, base `develop`, mergeable, merge state CLEAN. Head is exactly `6585feaac37c8d634f6de6be1079a17caf89d107`.
- The exact head is a merge commit with parent `513488eeb6d788f0e5eec054be89807505f05e08` (develop) and prior candidate `b91d6e971afc43ff29c426b195bb60a829faeace`; develop is therefore an immediate parent. The live branch and PR refs both match the tested head.
- PR commit API lists seven candidate commits. Every listed commit has author and committer `0428-065-export <0428-065@baseharbor.local>`; the hop adds no new identity.
- Run [44952948703](https://github.com/mcpdev80/baseharbor/actions/runs/44952948703) is `pull_request`, exact head `6585feaac37c8d634f6de6be1079a17caf89d107`, terminal `completed/success`, 41 jobs, 20 success, 21 skipped, 0 failed. `PR Selected Checks` job `136997373653` completed success. Skips are not counted as passes.
- Focused CLI shard job `136994756761` (`PR · Go unit · cli-3`) completed success. Its log reports `PASS cli-3: 426 passed / 16 intentionally skipped / 442 discovered; CLI inventory total=1843`. The candidate's `scripts/pr-go-unit-shard.py:60-72` deterministically assigns `TestAppExportManagedSecretWithoutOperatorFailsClosed` to cli-3 (SHA-256 first eight bytes modulo four = 3). The test body has no skip branch. The hosted runner emits aggregate rather than per-test receipts, so this proves the matching selected shard ran, not an individual per-case duration receipt.
- `PR · Validation · go-build`, `go-vet`, documentation audit, and package/CLI unit shards were among the executed successful jobs; no job failed.

## Content and security review

- Current task is `tasks/t-20261114-r28-cli2-app-export.md` (0428-065). PR scope has eight paths: `cmd/baha/app_export.go`, `cmd/baha/app_export_command_test.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, and four command-index/machine-coverage documentation files. No workflow or shared `scripts/**` change is present.
- The previous request-changes gap on the unauthorized managed-secret test is corrected at `cmd/baha/app_export_command_test.go:316-341`: it requires the fixed noninteractive operator-auth denial, checks captured stdout and stderr, and proves the explicit output file is absent. The production boundary at `cmd/baha/operator_auth_boundary.go:112-118` fails before managed-secret discovery when operator setup is absent/noninteractive; the denial text is asserted exactly. This is the fail-first cause, rather than a generic backend or output error.
- Secret-value access remains separately guarded by `authorizeHumanReveal` in `cmd/baha/app_export.go:325-357`; values are fetched only after authorization. The authorized-path test at `cmd/baha/app_export_command_test.go:416-456` decrypts the produced archive and confirms the managed sentinel is absent from stdout and ciphertext. Backend error redaction is covered at lines 458-483.
- The denial test's output substring list is based on its password-file fixture, not a managed-secret sentinel; however, the exact early operator-auth denial plus absent output artifact and the separate authorized sentinel/redaction tests cover the stated fail-first and output-protection behavior. No remaining candidate-owned security gap found.
- Verdict: APPROVE for the exact head. The previous denial-test finding is fixed. Receipt gap remains `open item, owner-scope receipt-tooling`, non-blocking per the sequence correction; no lane has set its own proof entrance. This is review-only: no comment, merge, or close.

## Repo-rule compliance and cleanliness

- No product files changed; no local suite tests, workflow dispatch/rerun, PR comment, merge, or close. No subagents used.
- Planning remote identity was checked before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).
- `docker ps -a` before inspection, shell PID 547571: eight pre-existing `bh-itest-*` containers, all exited; this review started no containers or compose projects.
- `docker ps -a` after inspection: same eight pre-existing exited containers; no Docker state was changed.
- Evidence checkbox scan: clear. Planning `render`/`check` outcome and origin/main publication witness will be added after review evidence is complete.

## END

END_DONE codex-rev-1747: APPROVE PR #1625 at `6585feaac37c8d634f6de6be1079a17caf89d107`; run 44952948703 success (41 jobs); receipt: owner-scope open item; Planning evidence publication recorded below; candidate remains `6585feaac37c8d634f6de6be1079a17caf89d107`.
- `docker ps -a` before and after, shell PID 578947: the same eight pre-existing `bh-itest-*` containers were listed both times, all exited; no containers or compose projects were started.

## Live revalidation — revorder2 sequence

- Refreshed GitHub API and `git ls-remote https://github.com/mcpdev80/baseharbor.git` on 2026-11-21: PR #1625 remains OPEN, non-draft, based on `develop`, mergeable/CLEAN; branch and PR head both remain `6585feaac37c8d634f6de6be1079a17caf89d107`. Current `develop` is `513488eeb6d788f0e5eec054be89807505f05e08`.
- Run 44952948703 remains terminal `completed/success`, `pull_request`, exact head `6585feaac37c8d634f6de6be1079a17caf89d107`: 41 total jobs, 20 success, 21 skipped, 0 failures. `PR Selected Checks` job 136995879740 and CLI shard `PR · Go unit · cli-3` job 136994756761 are completed/success. Skipped jobs are not treated as passes.
- The per-case CI receipt remains an `open item, owner-scope receipt-tooling`; per the explicit owner sequence correction it is non-blocking for this verdict. The selected shard ran successfully, but it does not emit an individual per-case duration receipt.
- Current review sequence: #1625 full-content verdict is APPROVE. No merge, PR comment, or close was performed.


END_DONE codex-rev-1747: APPROVE PR #1625; exact candidate 6585feaac37c8d634f6de6be1079a17caf89d107; run 44952948703 completed/success; receipt remains owner-scope open item and non-blocking.
